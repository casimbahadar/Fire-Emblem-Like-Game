"""
Sengoku Tactics: Age of the Warring States
Fire Emblem-style tactical RPG · Samurai Warriors inspired characters
20 Chapters · 60+ Historical Officers · Flying/Mounted Units
Recruit System · Reinforcement Waves · Character Stat Sheets

Controls:
  Arrow Keys / WASD  — Move cursor
  Z / Enter          — Select unit / Confirm
  X / Escape         — Cancel / Deselect
  Space              — End player turn
  A                  — Attack (with selected unit)
  H                  — Heal (with healer selected)
  W                  — Wait (end unit's turn)
  T                  — Talk / Recruit adjacent recruitable enemy
  I                  — Toggle full stat sheet for hovered unit
  E                  — Seize castle tile (lord standing on it)
"""
import sys
import pygame

from game.constants import *
from game.state     import GameState
from game.renderer  import Renderer


def main():
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
    gs       = GameState()
    gs.state = STATE_TITLE

    # ── Interaction state ─────────────────────────────────────────────────────
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

    def reset_interaction():
        nonlocal preview_target, attack_targets, attack_cursor
        nonlocal heal_targets, heal_cursor, showing_preview
        nonlocal showing_heal_sel, showing_recruit, recruit_target
        preview_target   = None
        attack_targets   = []
        attack_cursor    = 0
        heal_targets     = []
        heal_cursor      = 0
        showing_preview  = False
        showing_heal_sel = False
        showing_recruit  = False
        recruit_target   = None
        gs.selected_unit = None
        gs.move_range    = set()
        gs.move_range_land = set()
        gs.attack_range  = set()
        gs.cursor_mode   = CURSOR_FREE

    def handle_player_input(event):
        nonlocal preview_target, attack_targets, attack_cursor
        nonlocal heal_targets, heal_cursor, showing_preview, showing_heal_sel
        nonlocal showing_stat_sheet, stat_sheet_unit
        nonlocal showing_recruit, recruit_target

        # ── Dismiss messages first ─────────────────────────────────────────
        if gs.message_queue:
            if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_z, pygame.K_RETURN, pygame.K_SPACE,
                    pygame.K_x, pygame.K_ESCAPE):
                gs.message_queue.pop(0)
            return

        if event.type != pygame.KEYDOWN:
            return
        key = event.key

        # ── Stat sheet toggle ─────────────────────────────────────────────
        if key == pygame.K_i:
            target_unit = gs.unit_at(gs.cursor_x, gs.cursor_y)
            if showing_stat_sheet:
                showing_stat_sheet = False
                stat_sheet_unit    = None
            elif target_unit:
                showing_stat_sheet = True
                stat_sheet_unit    = target_unit
            return

        if showing_stat_sheet:
            if key in (pygame.K_i, pygame.K_x, pygame.K_ESCAPE,
                       pygame.K_z, pygame.K_RETURN):
                showing_stat_sheet = False
                stat_sheet_unit    = None
            return

        # ── Recruit dialog ────────────────────────────────────────────────
        if showing_recruit and recruit_target:
            if key in (pygame.K_z, pygame.K_RETURN):
                gs.recruit_unit(gs.selected_unit, recruit_target)
                reset_interaction()
                showing_recruit = False
                recruit_target  = None
            elif key in (pygame.K_x, pygame.K_ESCAPE):
                showing_recruit = False
                recruit_target  = None
            return

        # ── Combat preview ────────────────────────────────────────────────
        if showing_preview and preview_target:
            if key in (pygame.K_z, pygame.K_RETURN):
                gs.attack(gs.selected_unit, preview_target)
                reset_interaction()
                showing_preview = False
            elif key in (pygame.K_x, pygame.K_ESCAPE):
                showing_preview = False
                preview_target  = None
            elif key in (pygame.K_LEFT, pygame.K_a):
                attack_cursor  = (attack_cursor - 1) % len(attack_targets)
                preview_target = attack_targets[attack_cursor]
                gs.cursor_x    = preview_target.x
                gs.cursor_y    = preview_target.y
            elif key in (pygame.K_RIGHT, pygame.K_d):
                attack_cursor  = (attack_cursor + 1) % len(attack_targets)
                preview_target = attack_targets[attack_cursor]
                gs.cursor_x    = preview_target.x
                gs.cursor_y    = preview_target.y
            return

        # ── Heal selection ─────────────────────────────────────────────────
        if showing_heal_sel:
            if key in (pygame.K_z, pygame.K_RETURN) and heal_targets:
                gs.heal_action(gs.selected_unit, heal_targets[heal_cursor])
                reset_interaction()
                showing_heal_sel = False
            elif key in (pygame.K_x, pygame.K_ESCAPE):
                showing_heal_sel = False
            elif key in (pygame.K_LEFT, pygame.K_UP, pygame.K_a, pygame.K_w):
                heal_cursor = (heal_cursor-1) % max(1, len(heal_targets))
                if heal_targets:
                    gs.cursor_x = heal_targets[heal_cursor].x
                    gs.cursor_y = heal_targets[heal_cursor].y
            elif key in (pygame.K_RIGHT, pygame.K_DOWN, pygame.K_d, pygame.K_s):
                heal_cursor = (heal_cursor+1) % max(1, len(heal_targets))
                if heal_targets:
                    gs.cursor_x = heal_targets[heal_cursor].x
                    gs.cursor_y = heal_targets[heal_cursor].y
            return

        # ── Cursor movement ───────────────────────────────────────────────
        dx = dy = 0
        if key in (pygame.K_LEFT,  pygame.K_a): dx = -1
        if key in (pygame.K_RIGHT, pygame.K_d): dx =  1
        if key in (pygame.K_UP,    pygame.K_w): dy = -1
        if key in (pygame.K_DOWN,  pygame.K_s): dy =  1

        if dx or dy:
            gs.cursor_x = max(0, min(gs.game_map.width  - 1, gs.cursor_x + dx))
            gs.cursor_y = max(0, min(gs.game_map.height - 1, gs.cursor_y + dy))
            renderer.center_camera(gs.game_map, gs.cursor_x, gs.cursor_y)
            return

        # ── End turn ──────────────────────────────────────────────────────
        if key == pygame.K_SPACE:
            reset_interaction()
            gs.end_player_turn()
            return

        # ── Confirm / Select ──────────────────────────────────────────────
        if key in (pygame.K_z, pygame.K_RETURN):
            cx, cy = gs.cursor_x, gs.cursor_y

            if gs.cursor_mode == CURSOR_FREE:
                gs.select_unit(cx, cy)

            elif gs.cursor_mode == CURSOR_UNIT_SEL:
                unit     = gs.selected_unit
                tile_u   = gs.unit_at(cx, cy)

                if (cx, cy) in getattr(gs, 'move_range_land', set()):
                    gs.move_unit(unit, cx, cy)
                elif tile_u and tile_u.faction == FACTION_ENEMY:
                    tgts = gs.get_attackable_targets(unit)
                    if tile_u in tgts:
                        attack_targets = tgts
                        attack_cursor  = tgts.index(tile_u)
                        preview_target = tile_u
                        gs.cursor_x    = tile_u.x
                        gs.cursor_y    = tile_u.y
                        showing_preview= True
                else:
                    reset_interaction()

        # ── Cancel / Deselect ─────────────────────────────────────────────
        elif key in (pygame.K_x, pygame.K_ESCAPE):
            reset_interaction()

        # ── Attack ────────────────────────────────────────────────────────
        elif key == pygame.K_a:
            unit = gs.selected_unit
            if unit and unit.faction == FACTION_PLAYER and not unit.has_acted:
                tgts = gs.get_attackable_targets(unit)
                if tgts:
                    attack_targets  = tgts
                    attack_cursor   = 0
                    preview_target  = tgts[0]
                    gs.cursor_x     = tgts[0].x
                    gs.cursor_y     = tgts[0].y
                    gs.cursor_mode  = CURSOR_ATTACK
                    showing_preview = True

        # ── Heal ──────────────────────────────────────────────────────────
        elif key == pygame.K_h:
            unit = gs.selected_unit
            if unit and unit.faction == FACTION_PLAYER and not unit.has_acted:
                tgts = gs.get_healable_targets(unit)
                if tgts:
                    heal_targets     = tgts
                    heal_cursor      = 0
                    gs.cursor_x      = tgts[0].x
                    gs.cursor_y      = tgts[0].y
                    showing_heal_sel = True

        # ── Wait ──────────────────────────────────────────────────────────
        elif key == pygame.K_w:
            unit = gs.selected_unit
            if unit and unit.faction == FACTION_PLAYER:
                unit.done()
                reset_interaction()

        # ── Talk / Recruit ────────────────────────────────────────────────
        elif key == pygame.K_t:
            unit = gs.selected_unit
            if not unit:
                unit = gs.unit_at(gs.cursor_x, gs.cursor_y)
            if unit and unit.faction == FACTION_PLAYER and not unit.has_acted:
                recruitable = gs.get_recruitable_adjacent(unit)
                if recruitable:
                    recruit_target  = recruitable[0]
                    showing_recruit = True
                    gs.cursor_mode  = CURSOR_TALK

        # ── Seize ─────────────────────────────────────────────────────────
        elif key == pygame.K_e:
            unit = gs.selected_unit or gs.unit_at(gs.cursor_x, gs.cursor_y)
            if unit and unit.faction == FACTION_PLAYER:
                gs.check_victory()

    # ── Main Loop ─────────────────────────────────────────────────────────────
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Title
                if gs.state == STATE_TITLE:
                    if event.key in (pygame.K_RETURN, pygame.K_z):
                        gs.load_chapter(0)
                    elif event.key == pygame.K_ESCAPE:
                        running = False

                # Chapter intro
                elif gs.state == STATE_CHAPTER_INTRO:
                    if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                        gs.start_player_turn()
                        renderer.center_camera(gs.game_map, gs.cursor_x, gs.cursor_y)

                # Player turn
                elif gs.state == STATE_PLAYER_TURN:
                    handle_player_input(event)

                # End screens
                elif gs.state == STATE_VICTORY:
                    from game.chapter import CHAPTERS
                    if event.key == pygame.K_RETURN:
                        if gs.chapter_index + 1 < len(CHAPTERS):
                            gs.next_chapter()
                        else:
                            gs.state = STATE_TITLE
                    elif event.key == pygame.K_ESCAPE:
                        gs.state = STATE_TITLE
                elif gs.state == STATE_GAME_OVER:
                    if event.key == pygame.K_RETURN:
                        gs.load_chapter(gs.chapter_index)
                    elif event.key == pygame.K_ESCAPE:
                        gs.state = STATE_TITLE

        # Auto enemy turn
        if gs.state == STATE_ENEMY_TURN:
            gs.run_enemy_turn()

        # Render
        renderer.render(gs)

        # Overlays on top of main render
        if gs.state == STATE_PLAYER_TURN:
            if showing_preview and preview_target and gs.selected_unit:
                renderer.render_combat_preview(
                    gs.selected_unit, preview_target, gs.game_map)
            if showing_heal_sel and heal_targets:
                _render_heal_overlay(screen, font_sm, font_md, heal_targets, heal_cursor)
            if showing_recruit and recruit_target and gs.selected_unit:
                renderer.render_recruit_dialog(gs.selected_unit, recruit_target)
            if showing_stat_sheet and stat_sheet_unit:
                renderer.render_stat_sheet(stat_sheet_unit)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def _render_heal_overlay(screen, font_sm, font_md, targets, cursor):
    box = pygame.Rect(220, 280, 380, 60 + len(targets)*26 + 30)
    pygame.draw.rect(screen, (15,25,20), box)
    pygame.draw.rect(screen, (50,200,100), box, 2)
    screen.blit(font_md.render("Select Heal Target", True, (50,220,100)),
                (box.x+10, box.y+8))
    y = box.y + 36
    for i, t in enumerate(targets):
        bg = (40,80,50) if i == cursor else (15,25,20)
        pygame.draw.rect(screen, bg, (box.x+5, y-2, box.width-10, 24))
        col = WHITE if i==cursor else LIGHT_GREY
        screen.blit(font_sm.render(f"  {t.name}  HP:{t.hp}/{t.max_hp}", True, col),
                    (box.x+10, y))
        y += 26
    hint = font_sm.render("Z/Enter: Heal   X/Esc: Cancel", True, LIGHT_GREY)
    screen.blit(hint, (box.x+10, y+4))


if __name__ == "__main__":
    main()
