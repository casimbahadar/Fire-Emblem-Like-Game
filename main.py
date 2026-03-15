"""
Sengoku Tactics: Age of the Warring States
A Fire Emblem-style tactical RPG set in Sengoku-era Japan.

Controls:
  Arrow Keys / WASD  - Move cursor
  Z / Enter          - Select / Confirm
  X / Escape         - Cancel / Back
  Space              - End player turn
  A                  - Attack (when unit selected and adjacent to enemy)
  H                  - Heal (when healer selected and adjacent to ally)
  W                  - Wait (unit ends turn without acting)
  I                  - Toggle unit info
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
        font_sm    = pygame.font.SysFont("dejavusans",   14, bold=False)
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

    # ── Game mode: combat preview state ───────────────────────────────────────
    preview_target   = None   # unit being targeted in combat preview
    attack_targets   = []     # list of attackable units
    attack_cursor    = 0      # index into attack_targets
    heal_targets     = []
    heal_cursor      = 0
    showing_preview  = False
    showing_heal_sel = False

    def handle_player_input(event):
        nonlocal preview_target, attack_targets, attack_cursor
        nonlocal heal_targets, heal_cursor, showing_preview, showing_heal_sel

        # ── Message queue ──────────────────────────────────────────────────
        if gs.message_queue:
            if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_z, pygame.K_RETURN, pygame.K_SPACE, pygame.K_x, pygame.K_ESCAPE):
                gs.message_queue.pop(0)
            return

        if event.type != pygame.KEYDOWN:
            return
        key = event.key

        # ── Combat preview mode ────────────────────────────────────────────
        if showing_preview and preview_target:
            if key in (pygame.K_z, pygame.K_RETURN):
                # Confirm attack
                gs.attack(gs.selected_unit, preview_target)
                gs.selected_unit  = None
                gs.move_range     = set()
                gs.attack_range   = set()
                gs.cursor_mode    = CURSOR_FREE
                preview_target    = None
                attack_targets    = []
                showing_preview   = False
            elif key in (pygame.K_x, pygame.K_ESCAPE):
                showing_preview   = False
                preview_target    = None
            elif key == pygame.K_LEFT:
                attack_cursor = (attack_cursor - 1) % len(attack_targets)
                preview_target = attack_targets[attack_cursor]
                gs.cursor_x = preview_target.x
                gs.cursor_y = preview_target.y
            elif key == pygame.K_RIGHT:
                attack_cursor = (attack_cursor + 1) % len(attack_targets)
                preview_target = attack_targets[attack_cursor]
                gs.cursor_x = preview_target.x
                gs.cursor_y = preview_target.y
            return

        # ── Heal target selection ──────────────────────────────────────────
        if showing_heal_sel:
            if key in (pygame.K_z, pygame.K_RETURN) and heal_targets:
                target = heal_targets[heal_cursor]
                gs.heal_action(gs.selected_unit, target)
                gs.selected_unit  = None
                gs.move_range     = set()
                gs.attack_range   = set()
                gs.cursor_mode    = CURSOR_FREE
                heal_targets      = []
                showing_heal_sel  = False
            elif key in (pygame.K_x, pygame.K_ESCAPE):
                showing_heal_sel = False
            elif key in (pygame.K_LEFT, pygame.K_UP):
                heal_cursor = (heal_cursor - 1) % max(1, len(heal_targets))
                if heal_targets:
                    gs.cursor_x = heal_targets[heal_cursor].x
                    gs.cursor_y = heal_targets[heal_cursor].y
            elif key in (pygame.K_RIGHT, pygame.K_DOWN):
                heal_cursor = (heal_cursor + 1) % max(1, len(heal_targets))
                if heal_targets:
                    gs.cursor_x = heal_targets[heal_cursor].x
                    gs.cursor_y = heal_targets[heal_cursor].y
            return

        # ── Cursor movement ────────────────────────────────────────────────
        dx, dy = 0, 0
        if key in (pygame.K_LEFT,  pygame.K_a): dx = -1
        if key in (pygame.K_RIGHT, pygame.K_d): dx =  1
        if key in (pygame.K_UP,    pygame.K_w): dy = -1
        if key in (pygame.K_DOWN,  pygame.K_s): dy =  1

        if dx != 0 or dy != 0:
            nx = max(0, min(gs.game_map.width  - 1, gs.cursor_x + dx))
            ny = max(0, min(gs.game_map.height - 1, gs.cursor_y + dy))
            gs.cursor_x = nx
            gs.cursor_y = ny
            renderer.center_camera(gs.game_map, gs.cursor_x, gs.cursor_y)
            return

        # ── End turn ──────────────────────────────────────────────────────
        if key == pygame.K_SPACE:
            gs.end_player_turn()
            return

        # ── Confirm / Select ──────────────────────────────────────────────
        if key in (pygame.K_z, pygame.K_RETURN):
            if gs.cursor_mode == CURSOR_FREE:
                # Try to select a player unit
                if gs.select_unit(gs.cursor_x, gs.cursor_y):
                    pass
                # Or check seize
                elif gs.cursor_mode == CURSOR_FREE:
                    pass

            elif gs.cursor_mode == CURSOR_UNIT_SEL:
                unit = gs.selected_unit
                cx, cy = gs.cursor_x, gs.cursor_y
                tile_unit = gs.unit_at(cx, cy)

                if tile_unit == unit:
                    # Confirm position — show action menu equivalent
                    pass
                elif (cx, cy) in getattr(gs, 'move_range_land', set()):
                    # Move there
                    gs.move_unit(unit, cx, cy)
                elif tile_unit and tile_unit.faction in (FACTION_ENEMY,):
                    # Attack directly
                    dist = abs(unit.x - tile_unit.x) + abs(unit.y - tile_unit.y)
                    mn, mx = unit.attack_range()
                    if mn <= dist <= mx:
                        attack_targets  = gs.get_attackable_targets(unit)
                        if attack_targets:
                            # Find clicked in list
                            if tile_unit in attack_targets:
                                attack_cursor   = attack_targets.index(tile_unit)
                            else:
                                attack_cursor   = 0
                            preview_target  = attack_targets[attack_cursor]
                            gs.cursor_x     = preview_target.x
                            gs.cursor_y     = preview_target.y
                            showing_preview = True
                else:
                    # Deselect
                    gs.selected_unit = None
                    gs.move_range    = set()
                    gs.attack_range  = set()
                    gs.cursor_mode   = CURSOR_FREE

        # ── Cancel / Deselect ─────────────────────────────────────────────
        elif key in (pygame.K_x, pygame.K_ESCAPE):
            gs.selected_unit = None
            gs.move_range    = set()
            gs.attack_range  = set()
            gs.cursor_mode   = CURSOR_FREE
            showing_preview  = False
            preview_target   = None
            showing_heal_sel = False

        # ── Attack shortcut ───────────────────────────────────────────────
        elif key == pygame.K_a:
            unit = gs.selected_unit
            if unit and unit.faction == FACTION_PLAYER and not unit.has_acted:
                targets = gs.get_attackable_targets(unit)
                if targets:
                    attack_targets  = targets
                    attack_cursor   = 0
                    preview_target  = targets[0]
                    gs.cursor_x     = preview_target.x
                    gs.cursor_y     = preview_target.y
                    showing_preview = True
                    gs.cursor_mode  = CURSOR_ATTACK

        # ── Heal shortcut ─────────────────────────────────────────────────
        elif key == pygame.K_h:
            unit = gs.selected_unit
            if unit and unit.faction == FACTION_PLAYER and not unit.has_acted:
                targets = gs.get_healable_targets(unit)
                if targets:
                    heal_targets     = targets
                    heal_cursor      = 0
                    gs.cursor_x      = targets[0].x
                    gs.cursor_y      = targets[0].y
                    showing_heal_sel = True

        # ── Wait ──────────────────────────────────────────────────────────
        elif key == pygame.K_w:
            unit = gs.selected_unit
            if unit and unit.faction == FACTION_PLAYER:
                unit.done()
                gs.selected_unit = None
                gs.move_range    = set()
                gs.attack_range  = set()
                gs.cursor_mode   = CURSOR_FREE

        # ── Seize ─────────────────────────────────────────────────────────
        elif key == pygame.K_e:
            unit = gs.selected_unit or gs.unit_at(gs.cursor_x, gs.cursor_y)
            if unit and unit.faction == FACTION_PLAYER and unit.is_lord:
                gs.check_victory()

    # ── Main Loop ─────────────────────────────────────────────────────────────
    running = True
    while running:
        dt = clock.tick(FPS)

        # ── Events ────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # ── Title screen ──────────────────────────────────────────
                if gs.state == STATE_TITLE:
                    if event.key in (pygame.K_RETURN, pygame.K_z):
                        gs.load_chapter(0)
                    elif event.key == pygame.K_ESCAPE:
                        running = False

                # ── Chapter intro ─────────────────────────────────────────
                elif gs.state == STATE_CHAPTER_INTRO:
                    if event.key in (pygame.K_RETURN, pygame.K_z, pygame.K_SPACE):
                        gs.start_player_turn()
                        renderer.center_camera(gs.game_map, gs.cursor_x, gs.cursor_y)

                # ── Player turn ───────────────────────────────────────────
                elif gs.state == STATE_PLAYER_TURN:
                    handle_player_input(event)

                # ── End screens ───────────────────────────────────────────
                elif gs.state == STATE_VICTORY:
                    if event.key == pygame.K_RETURN:
                        if gs.chapter_index + 1 < len(__import__('game.chapter', fromlist=['CHAPTERS']).CHAPTERS):
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

        # ── Auto enemy turn ────────────────────────────────────────────────
        if gs.state == STATE_ENEMY_TURN:
            gs.run_enemy_turn()
            if not gs.defeat:
                # Now player turn
                pass  # run_enemy_turn calls start_player_turn internally

        # ── Render ─────────────────────────────────────────────────────────
        renderer.render(gs)

        # Combat preview overlay
        if showing_preview and preview_target and gs.selected_unit:
            renderer.render_combat_preview(
                gs.selected_unit, preview_target, gs.game_map)

        # Heal selection overlay
        if showing_heal_sel and heal_targets:
            _render_heal_overlay(screen, font_sm, font_md, heal_targets, heal_cursor)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def _render_heal_overlay(screen, font_sm, font_md, targets, cursor):
    box = pygame.Rect(200, 300, 400, 180)
    pygame.draw.rect(screen, (15, 20, 35), box)
    pygame.draw.rect(screen, (50, 200, 100), box, 2)
    title = font_md.render("Select Heal Target", True, (50, 220, 100))
    screen.blit(title, (box.x + 10, box.y + 10))
    y = box.y + 40
    for i, t in enumerate(targets):
        color = WHITE if i == cursor else LIGHT_GREY
        bg = (40, 80, 40) if i == cursor else (15, 20, 35)
        pygame.draw.rect(screen, bg, (box.x + 5, y - 2, box.width - 10, 22))
        hp_str = f"HP: {t.hp}/{t.max_hp}"
        s = font_sm.render(f"  {t.name}  ({hp_str})", True, color)
        screen.blit(s, (box.x + 10, y))
        y += 24
    hint = font_sm.render("Z/Enter: Heal   X/Esc: Cancel", True, LIGHT_GREY)
    screen.blit(hint, (box.x + 10, box.bottom - 24))


if __name__ == "__main__":
    main()
