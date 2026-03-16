"""
Sengoku Tactics: Age of the Warring States
Fire Emblem-style tactical RPG · Samurai Warriors characters
20 Chapters · Tutorial · Boss Dialogs · Touch/Mouse Controls

Keyboard:          Touch/Mouse:
  Arrows/WASD        D-Pad (bottom-left)
  Z/Enter: OK        ✓ button / tap unit or tile
  X/Esc: Cancel      ✕ button
  A: Attack          ⚔ button
  H: Heal            ♥ button
  W: Wait            Zz button
  T: Talk/Recruit    ! button
  I: Stat Sheet      i button
  E: Seize           ★ button
  Space: End Turn    ▶▶ button
  S: Skip tutorial
"""
import sys
import asyncio
import pygame
from game.constants import *
from game.state      import GameState
from game.renderer   import Renderer
from game.touch      import TouchControls
from game.tutorial   import (TUTORIAL_STAGES, TUTORIAL_PLAYER_DEFS,
                              TUTORIAL_ENEMY_DEFS, TUTORIAL_RECRUIT_DEF,
                              make_tutorial_map, TUTORIAL_CHAPTER_TITLE,
                              TUTORIAL_CHAPTER_SUBTITLE, TUTORIAL_INTRO)
from game.chapter    import CHAPTERS


def _build_tutorial_chapter(gs):
    """Inject a lightweight tutorial 'chapter' into the game state."""
    import copy
    gs.game_map     = make_tutorial_map()
    gs.player_units = []
    gs.enemy_units  = []
    gs.ally_units   = []
    gs.reinforce_waves = []

    for uid, x, y in TUTORIAL_PLAYER_DEFS:
        if uid in gs.roster:
            u = copy.deepcopy(gs.roster[uid])
            u.faction = FACTION_PLAYER; u.x=x; u.y=y
            gs.player_units.append(u)

    for uid, x, y in TUTORIAL_ENEMY_DEFS:
        if uid in gs.roster:
            u = copy.deepcopy(gs.roster[uid])
            u.faction = FACTION_ENEMY; u.x=x; u.y=y
            gs.enemy_units.append(u)

    # Recruitable unit
    uid, rx, ry = TUTORIAL_RECRUIT_DEF
    if uid in gs.roster:
        u = copy.deepcopy(gs.roster[uid])
        u.faction = FACTION_ENEMY; u.x=rx; u.y=ry
        u.can_recruit = True; u.recruit_by = ["any"]
        gs.enemy_units.append(u)

    from game.ai import EnemyAI
    gs.ai_controller = EnemyAI(gs)
    gs.turn = 1; gs.phase = FACTION_PLAYER
    gs.victory = gs.defeat = False
    gs.message_queue = []; gs.combat_log = []
    for u in gs.all_units(): u.reset_turn()


async def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sengoku Tactics: Age of the Warring States")
    clock = pygame.time.Clock()

    # ── Fonts ─────────────────────────────────────────────────────────────────
    try:
        font_sm    = pygame.font.SysFont("dejavusans",   14)
        font_md    = pygame.font.SysFont("dejavusans",   18, bold=True)
        font_lg    = pygame.font.SysFont("dejavusans",   28, bold=True)
        font_title = pygame.font.SysFont("dejavusans",   56, bold=True)
    except Exception:
        font_sm    = pygame.font.Font(None, 16)
        font_md    = pygame.font.Font(None, 22)
        font_lg    = pygame.font.Font(None, 32)
        font_title = pygame.font.Font(None, 64)

    renderer = Renderer(screen, font_sm, font_md, font_lg, font_title)
    touch    = TouchControls(font_sm, font_md)
    gs       = GameState()
    gs.state = STATE_TITLE

    # ── Interaction flags ─────────────────────────────────────────────────────
    preview_target    = None
    attack_targets    = []
    attack_cursor     = 0
    heal_targets      = []
    heal_cursor       = 0
    showing_preview   = False
    showing_heal_sel  = False
    showing_stat_sheet= False
    stat_sheet_unit   = None
    showing_recruit   = False
    recruit_target    = None
    showing_boss_dialog = False
    in_tutorial       = False
    showing_help      = False   # always-accessible help overlay (?/F1)

    def reset_interaction():
        nonlocal preview_target, attack_targets, attack_cursor
        nonlocal heal_targets, heal_cursor, showing_preview
        nonlocal showing_heal_sel, showing_recruit, recruit_target
        nonlocal showing_boss_dialog
        preview_target    = None
        attack_targets    = []
        attack_cursor     = 0
        heal_targets      = []
        heal_cursor       = 0
        showing_preview   = False
        showing_heal_sel  = False
        showing_recruit   = False
        recruit_target    = None
        showing_boss_dialog = False
        gs.selected_unit  = None
        gs.move_range     = set()
        gs.move_range_land= set()
        gs.attack_range   = set()
        gs.cursor_mode    = CURSOR_FREE

    # ── Tutorial helpers ──────────────────────────────────────────────────────
    def start_tutorial():
        nonlocal in_tutorial
        in_tutorial = True
        gs.tutorial.start()
        _build_tutorial_chapter(gs)
        gs.state = STATE_PLAYER_TURN
        renderer.center_camera(gs.game_map, gs.cursor_x, gs.cursor_y)

    def tutorial_event(event_type):
        """Fire a tutorial event and advance if stage is satisfied."""
        if not gs.tutorial.active:
            return
        if gs.tutorial.check_completion(gs, event_type):
            gs.tutorial.advance()

    def begin_chapter(idx):
        nonlocal in_tutorial
        in_tutorial = False
        gs.chapter_index = idx
        gs.load_chapter(idx)
        # load_chapter sets state to STATE_SCENE or STATE_PREP automatically
        if gs.game_map:
            renderer.center_camera(gs.game_map, gs.cursor_x, gs.cursor_y)

    # ── Action dispatcher (shared between keyboard and touch) ─────────────────
    def do_action(action):
        """
        Execute a game action by name. Called by both keyboard handlers and
        touch button handlers, keeping both paths in sync.
        """
        nonlocal preview_target, attack_targets, attack_cursor
        nonlocal heal_targets, heal_cursor, showing_preview, showing_heal_sel
        nonlocal showing_stat_sheet, stat_sheet_unit
        nonlocal showing_recruit, recruit_target, showing_boss_dialog
        nonlocal showing_help

        # ── Title screen ─────────────────────────────────────────────────────
        if gs.state == STATE_TITLE:
            if action == "confirm":
                gs._mode_cursor   = 0
                gs._deploy_cursor = 0
                gs._mode_row      = 0
                gs.state = STATE_MODE_SELECT
            return

        # ── Mode select screen ────────────────────────────────────────────────
        if gs.state == STATE_MODE_SELECT:
            active_row = getattr(gs, '_mode_row', 0)
            if action == "left":
                if active_row == 0: gs._mode_cursor   = 0
                else:               gs._deploy_cursor  = 0
            elif action == "right":
                if active_row == 0: gs._mode_cursor   = 1
                else:               gs._deploy_cursor  = 1
            elif action == "up":
                gs._mode_row = 0
            elif action == "down":
                gs._mode_row = 1
            elif action == "confirm":
                gs.classic_mode  = (getattr(gs, '_mode_cursor', 0) == 0)
                gs.deploy_mode   = DEPLOY_FREE if getattr(gs, '_deploy_cursor', 0) == 1 else DEPLOY_FORCED
                gs.prologue_idx  = 0
                gs.state         = STATE_PROLOGUE
            elif action == "cancel":
                gs.state = STATE_TITLE
            return

        # ── Prologue ──────────────────────────────────────────────────────────
        if gs.state == STATE_PROLOGUE:
            from game.prologue import PROLOGUE_SLIDES
            if action in ("confirm", "any_key", "cancel"):
                gs.prologue_idx = getattr(gs, 'prologue_idx', 0) + 1
                if gs.prologue_idx >= len(PROLOGUE_SLIDES):
                    start_tutorial()
            return

        # ── Pre-battle scene dialog ───────────────────────────────────────────
        if gs.state == STATE_SCENE:
            if action in ("confirm", "any_key", "cancel"):
                gs.scene_dialog_idx += 1
                if gs.scene_dialog_idx >= len(gs.scene_dialog):
                    # Scene finished → go to prep screen
                    gs.state = STATE_PREP
            return

        # ── Pre-battle prep screen ────────────────────────────────────────────
        if gs.state == STATE_PREP:
            if action == "help":
                showing_help = not showing_help
                return
            avail   = gs.prep_available_units
            tab     = gs.prep_tab
            cur     = gs.prep_cursor
            ch      = gs.current_chapter

            if action in ("left", "right"):
                direction = -1 if action == "left" else 1
                gs.prep_tab    = (tab + direction) % len(PREP_TAB_NAMES)
                gs.prep_cursor = 0
            elif action in ("up", "down"):
                direction = -1 if action == "up" else 1
                if tab == PREP_TAB_DEPLOY:
                    gs.prep_cursor = (cur + direction) % max(1, len(avail))
                elif tab == PREP_TAB_SHOP:
                    from game.constants import SHOP_PRICES
                    gs.prep_cursor = (cur + direction) % max(1, len(SHOP_PRICES))
                elif tab == PREP_TAB_INVENTORY:
                    all_u = gs.prep_selected_units + gs.prep_mercs
                    gs.prep_cursor = (cur + direction) % max(1, len(all_u))
            elif action == "confirm":
                if tab == PREP_TAB_DEPLOY:
                    # Toggle selected unit
                    if avail and cur < len(avail):
                        u = avail[cur]
                        if u in gs.prep_selected_units:
                            gs.prep_selected_units.remove(u)
                        elif len(gs.prep_selected_units) + len(gs.prep_mercs) < ch.deploy_limit:
                            gs.prep_selected_units.append(u)
                elif tab == PREP_TAB_SHOP:
                    from game.constants import SHOP_PRICES
                    from game.unit import create_mercenary
                    items = list(SHOP_PRICES.items())
                    if cur < len(items):
                        merc_id, cost = items[cur]
                        total_dep = len(gs.prep_selected_units) + len(gs.prep_mercs)
                        if (gs.gold >= cost and
                                len(gs.prep_mercs) < gs.prep_max_mercs and
                                total_dep < ch.deploy_limit):
                            gs.gold -= cost
                            gs.prep_mercs.append(
                                create_mercenary(merc_id, gs.chapter_index))
                elif tab == PREP_TAB_INVENTORY:
                    all_u = gs.prep_selected_units + gs.prep_mercs
                    if cur < len(all_u):
                        u = all_u[cur]
                        if u.weapons:
                            u.equipped_weapon_index = (
                                u.equipped_weapon_index + 1) % len(u.weapons)
            elif action in ("battle", "end_turn"):
                # Confirm prep and start battle
                if gs.prep_selected_units or gs.prep_mercs:
                    gs.confirm_prep_and_start()
                    renderer.center_camera(gs.game_map, gs.cursor_x, gs.cursor_y)
            return

        # ── Boss dialog ───────────────────────────────────────────────────────
        if showing_boss_dialog:
            if action in ("confirm","any_key","attack","cancel"):
                done = gs.advance_dialog()
                if done:
                    showing_boss_dialog = False
                    # Now show combat preview
                    if gs.pending_dialog_atk and gs.pending_dialog_def:
                        atk = gs.pending_dialog_atk
                        dfn = gs.pending_dialog_def
                        gs.pending_dialog_atk = gs.pending_dialog_def = None
                        _open_combat_preview(atk, dfn)
            return

        # ── Tutorial skip ─────────────────────────────────────────────────────
        if action == "skip_tutorial":
            gs.tutorial.skip()
            begin_chapter(0)
            return

        # ── Message dismissal ─────────────────────────────────────────────────
        if gs.message_queue:
            if action in ("confirm","cancel","end_turn","any_key"):
                dismissed = gs.message_queue.pop(0)
                tutorial_event("any_key")
            return

        # ── Stat sheet ────────────────────────────────────────────────────────
        if action == "info":
            target_unit = gs.unit_at(gs.cursor_x, gs.cursor_y)
            if showing_stat_sheet:
                showing_stat_sheet = False; stat_sheet_unit = None
            elif target_unit:
                showing_stat_sheet = True; stat_sheet_unit = target_unit
                tutorial_event("stat_sheet_opened")
            return

        if showing_stat_sheet:
            showing_stat_sheet = False; stat_sheet_unit = None
            return

        # ── Recruit dialog ────────────────────────────────────────────────────
        if showing_recruit and recruit_target:
            if action == "confirm":
                gs.recruit_unit(gs.selected_unit, recruit_target)
                reset_interaction()
                tutorial_event("unit_recruited")
            elif action == "cancel":
                showing_recruit = False; recruit_target = None
            return

        # ── Combat preview ────────────────────────────────────────────────────
        if showing_preview and preview_target:
            if action == "confirm":
                result = gs.attack(gs.selected_unit, preview_target)
                if not preview_target.alive:
                    tutorial_event("enemy_defeated")
                reset_interaction()
                showing_preview = False
            elif action == "cancel":
                showing_preview = False; preview_target = None
            elif action in ("left","right"):
                direction = -1 if action == "left" else 1
                attack_cursor  = (attack_cursor + direction) % len(attack_targets)
                preview_target = attack_targets[attack_cursor]
                gs.cursor_x = preview_target.x; gs.cursor_y = preview_target.y
            return

        # ── Heal selection ─────────────────────────────────────────────────────
        if showing_heal_sel:
            if action == "confirm" and heal_targets:
                gs.heal_action(gs.selected_unit, heal_targets[heal_cursor])
                reset_interaction()
                tutorial_event("heal_used")
                showing_heal_sel = False
            elif action == "cancel":
                showing_heal_sel = False
            elif action in ("left","up"):
                heal_cursor = (heal_cursor-1) % max(1,len(heal_targets))
                if heal_targets:
                    gs.cursor_x=heal_targets[heal_cursor].x
                    gs.cursor_y=heal_targets[heal_cursor].y
            elif action in ("right","down"):
                heal_cursor = (heal_cursor+1) % max(1,len(heal_targets))
                if heal_targets:
                    gs.cursor_x=heal_targets[heal_cursor].x
                    gs.cursor_y=heal_targets[heal_cursor].y
            return

        # ── Directional movement ──────────────────────────────────────────────
        if action in ("up","down","left","right"):
            delta = {"up":(0,-1),"down":(0,1),"left":(-1,0),"right":(1,0)}[action]
            gs.cursor_x = max(0,min(gs.game_map.width-1,  gs.cursor_x+delta[0]))
            gs.cursor_y = max(0,min(gs.game_map.height-1, gs.cursor_y+delta[1]))
            renderer.center_camera(gs.game_map, gs.cursor_x, gs.cursor_y)
            if gs.tutorial.active:
                tutorial_event("cursor_at_highlight")
            return

        # ── End turn ─────────────────────────────────────────────────────────
        if action == "end_turn":
            reset_interaction()
            gs.end_player_turn()
            tutorial_event("turn_ended")
            return

        # ── Confirm / Select / Move ────────────────────────────────────────────
        if action == "confirm":
            cx,cy = gs.cursor_x, gs.cursor_y
            if gs.cursor_mode == CURSOR_FREE:
                if gs.select_unit(cx,cy):
                    tutorial_event("unit_selected")
            elif gs.cursor_mode == CURSOR_UNIT_SEL:
                unit    = gs.selected_unit
                tile_u  = gs.unit_at(cx,cy)
                if (cx,cy) in getattr(gs,"move_range_land",set()):
                    gs.move_unit(unit,cx,cy)
                    tutorial_event("unit_moved")
                elif tile_u and tile_u.faction == FACTION_ENEMY:
                    tgts = gs.get_attackable_targets(unit)
                    if tile_u in tgts:
                        _open_combat_preview(unit, tile_u)
                else:
                    reset_interaction()
            return

        # ── Cancel ────────────────────────────────────────────────────────────
        if action == "cancel":
            reset_interaction()
            return

        # ── Attack ────────────────────────────────────────────────────────────
        if action == "attack":
            unit = gs.selected_unit
            if unit and unit.faction==FACTION_PLAYER and not unit.has_acted:
                tgts = gs.get_attackable_targets(unit)
                if tgts:
                    _open_combat_preview(unit, tgts[0])
            return

        # ── Heal ──────────────────────────────────────────────────────────────
        if action == "heal":
            unit = gs.selected_unit
            if unit and unit.faction==FACTION_PLAYER and not unit.has_acted:
                tgts = gs.get_healable_targets(unit)
                if tgts:
                    heal_targets = tgts; heal_cursor = 0
                    gs.cursor_x=tgts[0].x; gs.cursor_y=tgts[0].y
                    showing_heal_sel = True
            return

        # ── Wait ──────────────────────────────────────────────────────────────
        if action == "wait":
            unit = gs.selected_unit
            if unit and unit.faction==FACTION_PLAYER:
                unit.done(); reset_interaction()
            return

        # ── Talk/Recruit ──────────────────────────────────────────────────────
        if action == "talk":
            unit = gs.selected_unit or gs.unit_at(gs.cursor_x,gs.cursor_y)
            if unit and unit.faction==FACTION_PLAYER and not unit.has_acted:
                recruitable = gs.get_recruitable_adjacent(unit)
                if recruitable:
                    recruit_target = recruitable[0]
                    showing_recruit= True
                    gs.cursor_mode = CURSOR_TALK
            return

        # ── Seize ─────────────────────────────────────────────────────────────
        if action == "seize":
            unit = gs.selected_unit or gs.unit_at(gs.cursor_x,gs.cursor_y)
            if unit and unit.faction==FACTION_PLAYER:
                if (unit.x,unit.y) in gs.game_map.seize_points:
                    gs.check_victory()
                    tutorial_event("chapter_seize")
            return

    def _open_combat_preview(atk, dfn):
        nonlocal preview_target, attack_targets, attack_cursor, showing_preview
        nonlocal showing_boss_dialog

        # Check boss dialog first
        if gs.check_and_trigger_dialog(atk, dfn):
            showing_boss_dialog = True
            return

        attack_targets  = gs.get_attackable_targets(atk)
        attack_cursor   = attack_targets.index(dfn) if dfn in attack_targets else 0
        preview_target  = dfn
        gs.cursor_x     = dfn.x; gs.cursor_y = dfn.y
        gs.cursor_mode  = CURSOR_ATTACK
        showing_preview = True

    # ── Map click handler ─────────────────────────────────────────────────────
    def handle_map_click(mx, my):
        tx,ty = touch.tile_at_click(mx, my, renderer)
        if tx is None:
            return
        if not (0<=tx<gs.game_map.width and 0<=ty<gs.game_map.height):
            return
        # Move cursor there
        gs.cursor_x = tx; gs.cursor_y = ty
        renderer.center_camera(gs.game_map, tx, ty)
        # Try to perform context action: select or move
        unit_here = gs.unit_at(tx,ty)
        if showing_stat_sheet:
            do_action("info")  # closes stat sheet
            return
        if gs.cursor_mode == CURSOR_FREE:
            if unit_here and unit_here.faction == FACTION_PLAYER and not unit_here.has_acted:
                do_action("confirm")   # selects unit
        elif gs.cursor_mode == CURSOR_UNIT_SEL:
            if (tx,ty) in getattr(gs,"move_range_land",set()):
                do_action("confirm")   # moves unit
            elif unit_here and unit_here.faction == FACTION_ENEMY:
                tgts = gs.get_attackable_targets(gs.selected_unit)
                if unit_here in tgts:
                    _open_combat_preview(gs.selected_unit, unit_here)
                else:
                    reset_interaction()
            else:
                reset_interaction()

    # ── Main loop ─────────────────────────────────────────────────────────────
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ── Mouse / Touch input ───────────────────────────────────────────
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx,my = event.pos
                if gs.state in (STATE_PLAYER_TURN, STATE_TUTORIAL):
                    btn_action = touch.handle_mouse_down(mx,my)
                    if btn_action:
                        if btn_action == "zoom_in":
                            renderer.zoom_in()
                            if gs.game_map: renderer.center_camera(gs.game_map,gs.cursor_x,gs.cursor_y)
                        elif btn_action == "zoom_out":
                            renderer.zoom_out()
                            if gs.game_map: renderer.center_camera(gs.game_map,gs.cursor_x,gs.cursor_y)
                        elif btn_action == "help":
                            showing_help = not showing_help
                        else:
                            do_action(btn_action)
                    else:
                        handle_map_click(mx,my)
                elif gs.state == STATE_TITLE:
                    do_action("confirm")
                elif gs.state == STATE_MODE_SELECT:
                    # Tap: top half = difficulty row, bottom half = deploy row
                    cy_mid = SCREEN_HEIGHT // 2
                    if my < cy_mid:
                        gs._mode_row = 0
                        gs._mode_cursor = 0 if mx < SCREEN_WIDTH // 2 else 1
                    else:
                        gs._mode_row = 1
                        gs._deploy_cursor = 0 if mx < SCREEN_WIDTH // 2 else 1
                    do_action("confirm")
                elif gs.state == STATE_PROLOGUE:
                    do_action("confirm")
                elif gs.state == STATE_SCENE:
                    do_action("confirm")
                elif gs.state == STATE_PREP:
                    # Clicking right half of screen = "Battle!" shortcut
                    if mx > SCREEN_WIDTH * 3 // 4 and my > SCREEN_HEIGHT - 60:
                        do_action("battle")
                elif gs.state == STATE_CHAPTER_INTRO:
                    gs.start_player_turn()
                    renderer.center_camera(gs.game_map,gs.cursor_x,gs.cursor_y)
                elif gs.state in (STATE_VICTORY, STATE_GAME_OVER):
                    do_action("confirm")

            elif event.type == pygame.MOUSEMOTION:
                # Drag-to-scroll the map
                if gs.state in (STATE_PLAYER_TURN, STATE_TUTORIAL):
                    if pygame.mouse.get_pressed()[0]:
                        is_drag = touch.handle_mouse_motion(*event.pos)
                        if is_drag and gs.game_map:
                            dx, dy = touch.drag_cam_delta
                            if dx != 0 or dy != 0:
                                renderer.cam_x += dx
                                renderer.cam_y += dy
                                renderer.clamp_camera(gs.game_map)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                was_drag = touch.handle_mouse_up(*event.pos)
                # If it was a drag, suppress the tile-click that would normally follow

            # ── Pinch zoom (finger events — mobile browsers/touchscreens) ─────
            elif event.type == pygame.FINGERDOWN:
                touch.handle_finger_down(event.finger_id, event.x, event.y,
                                         SCREEN_WIDTH, SCREEN_HEIGHT)
            elif event.type == pygame.FINGERMOTION:
                zdelta = touch.handle_finger_motion(event.finger_id, event.x, event.y,
                                                    SCREEN_WIDTH, SCREEN_HEIGHT)
                if zdelta > 0:
                    renderer.zoom_in()
                    if gs.game_map: renderer.center_camera(gs.game_map,gs.cursor_x,gs.cursor_y)
                elif zdelta < 0:
                    renderer.zoom_out()
                    if gs.game_map: renderer.center_camera(gs.game_map,gs.cursor_x,gs.cursor_y)
            elif event.type == pygame.FINGERUP:
                touch.handle_finger_up(event.finger_id)

            # ── Mouse wheel zoom ──────────────────────────────────────────────
            elif event.type == pygame.MOUSEWHEEL:
                if gs.state in (STATE_PLAYER_TURN, STATE_TUTORIAL):
                    if event.y > 0:
                        renderer.zoom_in()
                    elif event.y < 0:
                        renderer.zoom_out()
                    if gs.game_map:
                        renderer.center_camera(gs.game_map,gs.cursor_x,gs.cursor_y)

            # ── Keyboard input ────────────────────────────────────────────────
            elif event.type == pygame.KEYDOWN:
                key = event.key

                # ── Title ─────────────────────────────────────────────────────
                if gs.state == STATE_TITLE:
                    if key in (pygame.K_RETURN, pygame.K_z):
                        gs._mode_cursor    = 0
                        gs._deploy_cursor  = 0
                        gs._mode_row       = 0
                        gs.state = STATE_MODE_SELECT
                    elif key == pygame.K_s:
                        gs._mode_cursor    = 0
                        gs._deploy_cursor  = 0
                        gs._mode_row       = 0
                        gs.state = STATE_MODE_SELECT
                    elif key == pygame.K_ESCAPE:
                        running = False

                # ── Mode Select ───────────────────────────────────────────────
                elif gs.state == STATE_MODE_SELECT:
                    if key in (pygame.K_LEFT,  pygame.K_a): do_action("left")
                    elif key in (pygame.K_RIGHT, pygame.K_d): do_action("right")
                    elif key in (pygame.K_UP,   pygame.K_w): do_action("up")
                    elif key in (pygame.K_DOWN, pygame.K_s): do_action("down")
                    elif key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                        do_action("confirm")
                    elif key == pygame.K_ESCAPE:
                        gs.state = STATE_TITLE

                # ── Prologue ──────────────────────────────────────────────────
                elif gs.state == STATE_PROLOGUE:
                    if key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE,
                               pygame.K_x, pygame.K_ESCAPE):
                        do_action("confirm")

                # ── Pre-battle scene dialog ───────────────────────────────────
                elif gs.state == STATE_SCENE:
                    if key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE,
                               pygame.K_x, pygame.K_ESCAPE):
                        do_action("confirm")

                # ── Chapter intro ─────────────────────────────────────────────
                elif gs.state == STATE_CHAPTER_INTRO:
                    if key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                        gs.start_player_turn()
                        renderer.center_camera(gs.game_map,gs.cursor_x,gs.cursor_y)

                # ── Prep screen ───────────────────────────────────────────────
                elif gs.state == STATE_PREP:
                    if key in (pygame.K_SLASH, pygame.K_F1):
                        showing_help = not showing_help
                    elif key in (pygame.K_LEFT,  pygame.K_a): do_action("left")
                    elif key in (pygame.K_RIGHT, pygame.K_d): do_action("right")
                    elif key in (pygame.K_UP,    pygame.K_w): do_action("up")
                    elif key in (pygame.K_DOWN,  pygame.K_s): do_action("down")
                    elif key in (pygame.K_z, pygame.K_RETURN):            do_action("confirm")
                    elif key in (pygame.K_SPACE, pygame.K_b):             do_action("battle")
                    elif key in (pygame.K_x, pygame.K_ESCAPE):            do_action("cancel")

                # ── Player turn (and tutorial) ────────────────────────────────
                elif gs.state in (STATE_PLAYER_TURN, STATE_TUTORIAL):
                    # Help overlay toggle (any time during player turn)
                    if key in (pygame.K_SLASH, pygame.K_F1):
                        showing_help = not showing_help; continue
                    if showing_help:
                        if key in (pygame.K_SLASH, pygame.K_F1,
                                   pygame.K_x, pygame.K_ESCAPE):
                            showing_help = False
                        continue

                    # Tutorial skip
                    if key == pygame.K_s and gs.tutorial.active:
                        gs.tutorial.skip(); begin_chapter(0); continue

                    # Boss dialog advance
                    if showing_boss_dialog:
                        do_action("any_key"); continue

                    # Stat sheet
                    if key == pygame.K_i:
                        do_action("info"); continue
                    if showing_stat_sheet:
                        if key in (pygame.K_i,pygame.K_x,pygame.K_ESCAPE,
                                   pygame.K_z,pygame.K_RETURN):
                            do_action("info")
                        continue

                    # Direction keys
                    dir_map = {pygame.K_LEFT:"left",pygame.K_a:"left",
                               pygame.K_RIGHT:"right",pygame.K_d:"right",
                               pygame.K_UP:"up",pygame.K_w:"up",
                               pygame.K_DOWN:"down",pygame.K_s:"down"}
                    if key in dir_map:
                        do_action(dir_map[key]); continue

                    # Zoom keys (+/-)
                    if key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                        renderer.zoom_in()
                        if gs.game_map: renderer.center_camera(gs.game_map,gs.cursor_x,gs.cursor_y)
                        continue
                    if key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        renderer.zoom_out()
                        if gs.game_map: renderer.center_camera(gs.game_map,gs.cursor_x,gs.cursor_y)
                        continue

                    # Single-key actions
                    act_map = {
                        pygame.K_z:      "confirm",
                        pygame.K_RETURN: "confirm",
                        pygame.K_x:      "cancel",
                        pygame.K_ESCAPE: "cancel",
                        pygame.K_SPACE:  "end_turn",
                        pygame.K_a:      "attack",
                        pygame.K_h:      "heal",
                        pygame.K_w:      "wait",
                        pygame.K_t:      "talk",
                        pygame.K_e:      "seize",
                    }
                    if key in act_map:
                        do_action(act_map[key])

                # ── Victory / Game Over ───────────────────────────────────────
                elif gs.state == STATE_VICTORY:
                    if key == pygame.K_RETURN:
                        if in_tutorial:
                            begin_chapter(0)
                        elif gs.chapter_index+1 < len(CHAPTERS):
                            gs.next_chapter()
                        else:
                            gs.state = STATE_TITLE
                    elif key == pygame.K_ESCAPE:
                        gs.state = STATE_TITLE

                elif gs.state == STATE_GAME_OVER:
                    if key == pygame.K_RETURN:
                        if in_tutorial:
                            start_tutorial()
                        else:
                            gs.load_chapter(gs.chapter_index)
                    elif key == pygame.K_ESCAPE:
                        gs.state = STATE_TITLE

        # ── Auto enemy turn ───────────────────────────────────────────────────
        if gs.state == STATE_ENEMY_TURN:
            gs.run_enemy_turn()

        # ── Render ────────────────────────────────────────────────────────────
        renderer.render(gs, showing_help=showing_help)

        # ── Overlays on top (order matters) ───────────────────────────────────
        if gs.state in (STATE_PLAYER_TURN, STATE_TUTORIAL):
            # Tutorial overlay (lowest priority)
            if gs.tutorial.active:
                renderer.render_tutorial(gs.tutorial, gs)

            # Boss dialog (blocks everything)
            if showing_boss_dialog and gs.pending_dialog:
                renderer.render_boss_dialog(
                    gs.pending_dialog, gs.pending_dialog_idx, gs.roster)

            # Combat preview
            elif showing_preview and preview_target and gs.selected_unit:
                renderer.render_combat_preview(
                    gs.selected_unit, preview_target, gs.game_map)
                # Weapon advantage indicator rendered inside

            # Heal selection
            elif showing_heal_sel and heal_targets:
                _render_heal_overlay(screen, font_sm, font_md, heal_targets, heal_cursor)

            # Recruit dialog
            elif showing_recruit and recruit_target and gs.selected_unit:
                renderer.render_recruit_dialog(gs.selected_unit, recruit_target)

            # Stat sheet (always on top when open)
            if showing_stat_sheet and stat_sheet_unit:
                renderer.render_stat_sheet(stat_sheet_unit)

            # Touch controls (always visible during play)
            touch.render(screen)

        pygame.display.flip()
        await asyncio.sleep(0)   # yield to browser event loop (pygbag requirement)

    pygame.quit()
    sys.exit()


def _render_heal_overlay(screen, font_sm, font_md, targets, cursor):
    bh = 56 + len(targets)*26 + 30
    box = pygame.Rect(220, 270, 400, bh)
    pygame.draw.rect(screen,(12,22,16),box,border_radius=8)
    pygame.draw.rect(screen,(50,200,100),box,2,border_radius=8)
    screen.blit(font_md.render("Select Heal Target",True,(50,220,100)),(box.x+12,box.y+10))
    y = box.y+40
    for i,t in enumerate(targets):
        if i==cursor:
            pygame.draw.rect(screen,(40,90,55),(box.x+6,y-2,box.width-12,24),
                             border_radius=4)
        col=WHITE if i==cursor else LIGHT_GREY
        screen.blit(font_sm.render(f"  {t.name}   HP:{t.hp}/{t.max_hp}",True,col),
                    (box.x+12,y)); y+=26
    screen.blit(font_sm.render("Z/♥ Heal   X/✕ Cancel",True,LIGHT_GREY),
                (box.x+12,y+4))


if __name__ == "__main__":
    asyncio.run(main())
