"""
Rendering system for Sengoku Tactics using Pygame
"""
import pygame
from game.constants import *


class Renderer:
    def __init__(self, screen, font_small, font_med, font_large, font_title):
        self.screen     = screen
        self.font_sm    = font_small
        self.font_md    = font_med
        self.font_lg    = font_large
        self.font_title = font_title

        # Camera / viewport offset
        self.cam_x = 0
        self.cam_y = 0

        # Map area (left portion of screen)
        self.map_rect = pygame.Rect(0, 0, SCREEN_WIDTH - UI_PANEL_WIDTH, SCREEN_HEIGHT)
        # UI panel (right portion)
        self.ui_rect  = pygame.Rect(SCREEN_WIDTH - UI_PANEL_WIDTH, 0, UI_PANEL_WIDTH, SCREEN_HEIGHT)

        self._build_terrain_surfaces()

    def _build_terrain_surfaces(self):
        """Pre-render tile base surfaces for performance."""
        self._tile_surfs = {}
        for terrain, data in TERRAIN_DATA.items():
            s = pygame.Surface((TILE_SIZE, TILE_SIZE))
            color = data["color"]
            s.fill(color)
            # Add subtle border
            pygame.draw.rect(s, _darken(color, 20), s.get_rect(), 1)
            # Add texture marks
            self._add_terrain_texture(s, terrain, color)
            self._tile_surfs[terrain] = s

    def _add_terrain_texture(self, surf, terrain, base_color):
        """Simple procedural texture per terrain type."""
        if terrain == TERRAIN_FOREST:
            # Draw little tree dots
            for pos in [(12, 10), (28, 8), (20, 22), (10, 32), (34, 28)]:
                pygame.draw.circle(surf, _darken(base_color, 30), pos, 5)
        elif terrain == TERRAIN_MOUNTAIN:
            # Draw triangle peaks
            pygame.draw.polygon(surf, _darken(base_color, 40),
                                [(8, 40), (16, 18), (24, 40)])
            pygame.draw.polygon(surf, _darken(base_color, 30),
                                [(22, 40), (32, 16), (44, 40)])
        elif terrain == TERRAIN_RIVER or terrain == TERRAIN_SEA:
            # Wavy lines
            for i in range(0, TILE_SIZE, 8):
                pygame.draw.arc(surf, _lighten(base_color, 30),
                                pygame.Rect(i-4, 16, 12, 10), 0, 3.14, 2)
        elif terrain == TERRAIN_CASTLE:
            # Battlements outline
            pygame.draw.rect(surf, _darken(base_color, 40),
                             pygame.Rect(4, 4, TILE_SIZE-8, TILE_SIZE-8), 2)
            for bx in range(6, TILE_SIZE-6, 8):
                pygame.draw.rect(surf, _darken(base_color, 40),
                                 pygame.Rect(bx, 2, 5, 6))
        elif terrain == TERRAIN_ROAD:
            pygame.draw.rect(surf, _darken(base_color, 15),
                             pygame.Rect(0, TILE_SIZE//2-4, TILE_SIZE, 8))
        elif terrain == TERRAIN_FORT:
            pygame.draw.rect(surf, _darken(base_color, 35),
                             pygame.Rect(8, 8, TILE_SIZE-16, TILE_SIZE-16), 3)
        elif terrain == TERRAIN_VILLAGE:
            # Simple house shape
            pygame.draw.polygon(surf, _darken(base_color, 40),
                                [(TILE_SIZE//2, 8), (10, 28), (TILE_SIZE-10, 28)])
            pygame.draw.rect(surf, _darken(base_color, 30),
                             pygame.Rect(14, 28, 20, 16))
        elif terrain == TERRAIN_BRIDGE:
            pygame.draw.rect(surf, _darken(base_color, 20),
                             pygame.Rect(0, 18, TILE_SIZE, 12))
            for bx in range(0, TILE_SIZE, 10):
                pygame.draw.rect(surf, _darken(base_color, 35),
                                 pygame.Rect(bx, 18, 4, 12))

    # ── Camera ────────────────────────────────────────────────────────────────

    def center_camera(self, gmap, cursor_x, cursor_y):
        """Keep cursor tile near center of map view."""
        map_view_w = self.map_rect.width // TILE_SIZE
        map_view_h = self.map_rect.height // TILE_SIZE

        target_cam_x = cursor_x - map_view_w // 2
        target_cam_y = cursor_y - map_view_h // 2

        self.cam_x = max(0, min(target_cam_x, gmap.width  - map_view_w))
        self.cam_y = max(0, min(target_cam_y, gmap.height - map_view_h))

    def tile_to_screen(self, tx, ty):
        sx = (tx - self.cam_x) * TILE_SIZE
        sy = (ty - self.cam_y) * TILE_SIZE
        return sx, sy

    def screen_to_tile(self, sx, sy):
        tx = sx // TILE_SIZE + self.cam_x
        ty = sy // TILE_SIZE + self.cam_y
        return tx, ty

    # ── Full Frame Render ─────────────────────────────────────────────────────

    def render(self, gs):
        self.screen.fill(BLACK)
        state = gs.state

        if state == STATE_TITLE:
            self._render_title(gs)
        elif state == STATE_CHAPTER_INTRO:
            self._render_chapter_intro(gs)
        elif state in (STATE_PLAYER_TURN, STATE_ENEMY_TURN, STATE_ALLY_TURN,
                       STATE_COMBAT, STATE_MENU):
            self._render_map(gs)
            self._render_units(gs)
            self._render_overlays(gs)
            self._render_cursor(gs)
            self._render_ui_panel(gs)
            if gs.message_queue:
                self._render_message_box(gs)
        elif state == STATE_VICTORY:
            self._render_map(gs)
            self._render_units(gs)
            self._render_end_screen(gs, victory=True)
        elif state == STATE_GAME_OVER:
            self._render_map(gs)
            self._render_units(gs)
            self._render_end_screen(gs, victory=False)

    # ── Title Screen ─────────────────────────────────────────────────────────

    def _render_title(self, gs):
        self.screen.fill((20, 10, 5))
        # Gradient sky
        for i in range(SCREEN_HEIGHT):
            t = i / SCREEN_HEIGHT
            r = int(20 + t * 60)
            g = int(10 + t * 20)
            b = int(5 + t * 10)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))

        # Title text
        title1 = self.font_title.render("SENGOKU TACTICS", True, GOLD)
        title2 = self.font_lg.render("Age of the Warring States", True, CREAM)
        sub    = self.font_md.render("Press ENTER to Begin  |  ESC to Quit", True, LIGHT_GREY)

        cx = SCREEN_WIDTH // 2
        self.screen.blit(title1, title1.get_rect(center=(cx, 200)))
        self.screen.blit(title2, title2.get_rect(center=(cx, 290)))
        self.screen.blit(sub,    sub.get_rect(center=(cx, 420)))

        # Controls hint
        controls = [
            "ARROW KEYS / WASD: Move cursor",
            "Z / ENTER: Confirm / Select",
            "X / ESC:   Cancel / Menu",
            "SPACE:     End Turn",
        ]
        y = 520
        for line in controls:
            s = self.font_sm.render(line, True, LIGHT_GREY)
            self.screen.blit(s, s.get_rect(center=(cx, y)))
            y += 26

        # Decorative divider
        pygame.draw.line(self.screen, GOLD, (cx-300, 340), (cx+300, 340), 2)
        pygame.draw.line(self.screen, GOLD, (cx-300, 350), (cx+300, 350), 1)

    # ── Chapter Intro Screen ──────────────────────────────────────────────────

    def _render_chapter_intro(self, gs):
        self.screen.fill((10, 10, 20))
        ch = gs.current_chapter
        cx = SCREEN_WIDTH // 2

        # Chapter title
        t1 = self.font_lg.render(ch.title, True, GOLD)
        t2 = self.font_md.render(ch.subtitle, True, CREAM)
        self.screen.blit(t1, t1.get_rect(center=(cx, 80)))
        self.screen.blit(t2, t2.get_rect(center=(cx, 130)))

        # Narrative
        pygame.draw.rect(self.screen, (20, 20, 40),
                         pygame.Rect(80, 170, SCREEN_WIDTH-160, 380))
        pygame.draw.rect(self.screen, GOLD,
                         pygame.Rect(80, 170, SCREEN_WIDTH-160, 380), 2)
        y = 195
        for line in ch.narrative_intro.split("\n"):
            s = self.font_sm.render(line, True, CREAM)
            self.screen.blit(s, (100, y))
            y += 28

        # Objective box
        pygame.draw.rect(self.screen, (30, 20, 10),
                         pygame.Rect(80, 570, SCREEN_WIDTH-160, 60))
        pygame.draw.rect(self.screen, GOLD,
                         pygame.Rect(80, 570, SCREEN_WIDTH-160, 60), 2)
        obj_label = self.font_sm.render("Objective: " + ch.objective_detail, True, YELLOW)
        self.screen.blit(obj_label, (100, 590))

        prompt = self.font_sm.render("Press ENTER to begin", True, LIGHT_GREY)
        self.screen.blit(prompt, prompt.get_rect(center=(cx, 650)))

    # ── Map Layer ─────────────────────────────────────────────────────────────

    def _render_map(self, gs):
        gmap = gs.game_map
        # Fill map area
        pygame.draw.rect(self.screen, (30, 30, 30), self.map_rect)

        view_w = self.map_rect.width  // TILE_SIZE + 2
        view_h = self.map_rect.height // TILE_SIZE + 2

        for ty in range(self.cam_y, min(self.cam_y + view_h, gmap.height)):
            for tx in range(self.cam_x, min(self.cam_x + view_w, gmap.width)):
                terrain = gmap.get_terrain(tx, ty)
                surf    = self._tile_surfs[terrain]
                sx, sy  = self.tile_to_screen(tx, ty)
                self.screen.blit(surf, (sx, sy))

        # Map border
        pygame.draw.rect(self.screen, DARK_GREY, self.map_rect, 2)

    # ── Overlay (movement/attack range) ──────────────────────────────────────

    def _render_overlays(self, gs):
        move_surf   = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        attack_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        seize_surf  = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

        move_surf.fill((60, 100, 220, 100))
        attack_surf.fill((220, 60, 60, 80))
        seize_surf.fill((220, 180, 30, 100))

        # Seize points
        for (sx, sy) in gs.game_map.seize_points:
            px, py = self.tile_to_screen(sx, sy)
            self.screen.blit(seize_surf, (px, py))
            pygame.draw.rect(self.screen, GOLD, (px, py, TILE_SIZE, TILE_SIZE), 2)

        if gs.selected_unit:
            # Move range
            for (tx, ty) in getattr(gs, 'move_range_land', set()):
                px, py = self.tile_to_screen(tx, ty)
                if self.map_rect.collidepoint(px + TILE_SIZE//2, py + TILE_SIZE//2):
                    self.screen.blit(move_surf, (px, py))

            # Attack range
            for (tx, ty) in gs.attack_range:
                px, py = self.tile_to_screen(tx, ty)
                if self.map_rect.collidepoint(px + TILE_SIZE//2, py + TILE_SIZE//2):
                    self.screen.blit(attack_surf, (px, py))

    # ── Units ─────────────────────────────────────────────────────────────────

    def _render_units(self, gs):
        for unit in gs.all_units():
            if not unit.alive:
                continue
            sx, sy = self.tile_to_screen(unit.x, unit.y)
            if not self.map_rect.collidepoint(sx + TILE_SIZE//2, sy + TILE_SIZE//2):
                continue
            self._draw_unit(unit, sx, sy, gs)

    def _draw_unit(self, unit, sx, sy, gs):
        # Base circle
        cx_ = sx + TILE_SIZE // 2
        cy_ = sy + TILE_SIZE // 2
        radius = TILE_SIZE // 2 - 3

        # Determine color based on state
        color = unit.color
        if unit.has_acted and unit.faction == FACTION_PLAYER:
            color = _darken(color, 80)

        # Shadow
        pygame.draw.circle(self.screen, _darken(color, 50),
                           (cx_ + 2, cy_ + 2), radius)
        # Main circle
        pygame.draw.circle(self.screen, color, (cx_, cy_), radius)
        # Border by faction
        border_color = {
            FACTION_PLAYER: (80, 180, 255),
            FACTION_ENEMY:  (255, 80,  80),
            FACTION_ALLY:   (80, 255, 120),
        }.get(unit.faction, WHITE)
        pygame.draw.circle(self.screen, border_color, (cx_, cy_), radius, 2)

        # Class symbol
        sym = unit.symbol[:2]
        sym_surf = self.font_sm.render(sym, True, WHITE)
        self.screen.blit(sym_surf, sym_surf.get_rect(center=(cx_, cy_ - 2)))

        # HP bar
        bar_w   = TILE_SIZE - 8
        bar_h   = 4
        bar_x   = sx + 4
        bar_y   = sy + TILE_SIZE - 7
        hp_pct  = unit.hp / unit.max_hp
        hp_color = GREEN if hp_pct > 0.5 else YELLOW if hp_pct > 0.25 else RED
        pygame.draw.rect(self.screen, DARK_GREY,  (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(self.screen, hp_color,   (bar_x, bar_y, int(bar_w * hp_pct), bar_h))

        # Selected unit highlight
        if gs.selected_unit == unit:
            pygame.draw.rect(self.screen, WHITE,
                             (sx+1, sy+1, TILE_SIZE-2, TILE_SIZE-2), 2)

        # Lord crown indicator
        if unit.is_lord:
            crown = self.font_sm.render("♦", True, GOLD)
            self.screen.blit(crown, (sx + TILE_SIZE - 14, sy + 1))

    # ── Cursor ────────────────────────────────────────────────────────────────

    def _render_cursor(self, gs):
        sx, sy = self.tile_to_screen(gs.cursor_x, gs.cursor_y)
        if not self.map_rect.collidepoint(sx + TILE_SIZE//2, sy + TILE_SIZE//2):
            return

        # Animated pulsing cursor (use a simple rect)
        ticks = pygame.time.get_ticks()
        alpha = int(160 + 80 * abs((ticks % 1000) / 500 - 1))
        cursor_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        cursor_surf.fill((255, 255, 255, 0))
        pygame.draw.rect(cursor_surf, (255, 255, 255, min(255, alpha)),
                         pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE), 3)
        self.screen.blit(cursor_surf, (sx, sy))

    # ── UI Panel ──────────────────────────────────────────────────────────────

    def _render_ui_panel(self, gs):
        panel = self.ui_rect
        pygame.draw.rect(self.screen, (20, 20, 35), panel)
        pygame.draw.rect(self.screen, GOLD, panel, 2)

        x0 = panel.x + 10
        y  = panel.y + 10

        # Phase / Turn info
        phase_str = {
            FACTION_PLAYER: "Player Phase",
            FACTION_ENEMY:  "Enemy Phase",
            FACTION_ALLY:   "Ally Phase",
        }.get(gs.phase, "")
        phase_col = {
            FACTION_PLAYER: LIGHT_BLUE,
            FACTION_ENEMY:  PINK,
            FACTION_ALLY:   (100, 255, 150),
        }.get(gs.phase, WHITE)

        turn_surf = self.font_md.render(f"Turn {gs.turn}", True, GOLD)
        phase_surf = self.font_sm.render(phase_str, True, phase_col)
        self.screen.blit(turn_surf,  (x0, y));  y += 30
        self.screen.blit(phase_surf, (x0, y));  y += 24

        # Map name
        map_surf = self.font_sm.render(gs.game_map.name, True, LIGHT_GREY)
        self.screen.blit(map_surf, (x0, y)); y += 22

        pygame.draw.line(self.screen, GOLD, (x0, y), (panel.right-10, y), 1); y += 8

        # Hovered / selected unit info
        hovered_unit = gs.unit_at(gs.cursor_x, gs.cursor_y)
        display_unit = gs.selected_unit or hovered_unit

        if display_unit:
            y = self._render_unit_card(display_unit, x0, y, panel.right - 10)
        else:
            # Terrain info
            terrain = gs.game_map.get_terrain(gs.cursor_x, gs.cursor_y)
            td = TERRAIN_DATA[terrain]
            y = self._render_terrain_info(terrain, td, x0, y)

        pygame.draw.line(self.screen, GOLD, (x0, panel.bottom - 140),
                         (panel.right-10, panel.bottom - 140), 1)

        # Controls reminder at bottom
        y = panel.bottom - 130
        controls = [
            "Arrows: Move cursor",
            "Z/Enter: Select/Confirm",
            "X/Esc:  Cancel",
            "Space:  End Turn",
            "A:      Attack",
            "H:      Heal",
            "W:      Wait",
        ]
        ctrl_title = self.font_sm.render("Controls", True, GOLD)
        self.screen.blit(ctrl_title, (x0, y)); y += 20
        for line in controls:
            s = self.font_sm.render(line, True, LIGHT_GREY)
            self.screen.blit(s, (x0, y))
            y += 17

        # Chapter objective
        ch = gs.current_chapter
        if ch:
            pygame.draw.line(self.screen, GOLD, (x0, panel.bottom - 260),
                             (panel.right-10, panel.bottom - 260), 1)
            obj_y = panel.bottom - 252
            obj_t = self.font_sm.render("Objective:", True, YELLOW)
            self.screen.blit(obj_t, (x0, obj_y)); obj_y += 18
            # Word-wrap objective text
            words = ch.objective_detail.split()
            line_  = ""
            for w in words:
                test = line_ + w + " "
                if self.font_sm.size(test)[0] > panel.width - 20:
                    s = self.font_sm.render(line_.strip(), True, CREAM)
                    self.screen.blit(s, (x0, obj_y))
                    obj_y += 16
                    line_ = w + " "
                else:
                    line_ = test
            if line_:
                s = self.font_sm.render(line_.strip(), True, CREAM)
                self.screen.blit(s, (x0, obj_y))

    def _render_unit_card(self, unit, x0, y, x1):
        # Name
        name_surf = self.font_md.render(unit.name, True, WHITE)
        self.screen.blit(name_surf, (x0, y)); y += 26
        # Class / Level
        cl_surf = self.font_sm.render(f"{unit.unit_class}  Lv{unit.level}", True, LIGHT_GREY)
        self.screen.blit(cl_surf, (x0, y)); y += 20
        # Faction badge
        fc_color = {FACTION_PLAYER: LIGHT_BLUE, FACTION_ENEMY: PINK, FACTION_ALLY: (100,255,150)}.get(unit.faction, WHITE)
        fc_surf = self.font_sm.render(unit.faction.upper(), True, fc_color)
        self.screen.blit(fc_surf, (x0, y)); y += 22

        # HP bar
        bar_w  = x1 - x0
        bar_h  = 10
        hp_pct = unit.hp / unit.max_hp
        hp_col = GREEN if hp_pct > 0.5 else YELLOW if hp_pct > 0.25 else RED
        pygame.draw.rect(self.screen, DARK_GREY, (x0, y, bar_w, bar_h))
        pygame.draw.rect(self.screen, hp_col,    (x0, y, int(bar_w * hp_pct), bar_h))
        hp_txt = self.font_sm.render(f"HP: {unit.hp}/{unit.max_hp}", True, WHITE)
        self.screen.blit(hp_txt, (x0, y + 12)); y += 30

        # Stats grid
        stats = [
            ("STR", unit.str_), ("MAG", unit.mag),
            ("SKL", unit.skl),  ("SPD", unit.spd),
            ("LCK", unit.lck),  ("DEF", unit.def_),
            ("RES", unit.res),  ("MOV", unit.move),
        ]
        col_w = (x1 - x0) // 2
        for i, (label, val) in enumerate(stats):
            col = i % 2
            row = i // 2
            stat_x = x0 + col * col_w
            stat_y = y + row * 16
            lbl_s = self.font_sm.render(f"{label}:{val:3d}", True, LIGHT_GREY)
            self.screen.blit(lbl_s, (stat_x, stat_y))
        y += (len(stats) // 2) * 16 + 8

        # Equipped weapon
        if unit.equipped:
            w = unit.equipped
            pygame.draw.line(self.screen, GOLD, (x0, y), (x1, y), 1); y += 6
            eq_t = self.font_sm.render("Equipped:", True, GOLD)
            self.screen.blit(eq_t, (x0, y)); y += 18
            wname = self.font_sm.render(w.name, True, WHITE)
            self.screen.blit(wname, (x0, y)); y += 16
            wstats = self.font_sm.render(
                f"Mt:{w.might} Hit:{w.hit} Crit:{w.crit}", True, LIGHT_GREY)
            self.screen.blit(wstats, (x0, y)); y += 16
            wtype = self.font_sm.render(
                f"Type:{w.weapon_type}  Rng:{w.min_range}-{w.max_range}", True, LIGHT_GREY)
            self.screen.blit(wtype, (x0, y)); y += 16

        # EXP bar
        pygame.draw.line(self.screen, GOLD, (x0, y), (x1, y), 1); y += 4
        bar_w = x1 - x0
        pygame.draw.rect(self.screen, DARK_GREY, (x0, y, bar_w, 6))
        pygame.draw.rect(self.screen, CYAN, (x0, y, int(bar_w * unit.exp / 100), 6))
        exp_t = self.font_sm.render(f"EXP: {unit.exp}/100", True, LIGHT_GREY)
        self.screen.blit(exp_t, (x0, y + 8)); y += 22

        return y

    def _render_terrain_info(self, terrain, td, x0, y):
        name_s = self.font_md.render(td["name"], True, WHITE)
        self.screen.blit(name_s, (x0, y)); y += 26
        def_s  = self.font_sm.render(f"Def Bonus: +{td['def']}", True, LIGHT_GREY)
        avo_s  = self.font_sm.render(f"Avo Bonus: +{td['avo']}", True, LIGHT_GREY)
        mov_s  = self.font_sm.render(f"Move Cost: {td['move']}", True, LIGHT_GREY)
        self.screen.blit(def_s, (x0, y)); y += 18
        self.screen.blit(avo_s, (x0, y)); y += 18
        self.screen.blit(mov_s, (x0, y)); y += 18
        return y

    # ── Message Box ───────────────────────────────────────────────────────────

    def _render_message_box(self, gs):
        if not gs.message_queue:
            return
        msg = gs.message_queue[0]
        box = pygame.Rect(SCREEN_WIDTH//2 - 280, SCREEN_HEIGHT - 90, 560, 70)
        pygame.draw.rect(self.screen, (15, 15, 30), box)
        pygame.draw.rect(self.screen, GOLD, box, 2)
        msg_surf = self.font_md.render(msg, True, WHITE)
        self.screen.blit(msg_surf, msg_surf.get_rect(center=box.center))
        prompt = self.font_sm.render("Press Z/Enter to continue", True, LIGHT_GREY)
        self.screen.blit(prompt, (box.x + 10, box.bottom - 20))

    # ── Combat Preview ────────────────────────────────────────────────────────

    def render_combat_preview(self, attacker, defender, gmap):
        """Show combat forecast overlay."""
        box = pygame.Rect(200, SCREEN_HEIGHT//2 - 100, SCREEN_WIDTH - 400, 200)
        pygame.draw.rect(self.screen, (10, 10, 25), box)
        pygame.draw.rect(self.screen, GOLD, box, 2)

        x0 = box.x + 15
        y  = box.y + 10

        title = self.font_md.render("Combat Forecast", True, GOLD)
        self.screen.blit(title, (box.centerx - title.get_width()//2, y)); y += 30

        att_w = attacker.equipped
        def_w = defender.equipped

        # Attacker side
        att_atk   = attacker.attack_power(def_w)
        att_hit   = max(0, min(100, attacker.hit_rate(def_w) - defender.avoid()))
        att_crit  = max(0, attacker.crit_rate(def_w) - defender.crit_avoid())
        att_dmg   = max(0, att_atk - defender.defense())
        tri_att = att_w.get_triangle_bonus(def_w) if att_w else 0

        # Defender counter
        if def_w and "heal" not in getattr(def_w, 'weapon_id', ''):
            def_atk  = defender.attack_power(att_w)
            def_hit  = max(0, min(100, defender.hit_rate(att_w) - attacker.avoid()))
            def_crit = max(0, defender.crit_rate(att_w) - attacker.crit_avoid())
            def_dmg  = max(0, def_atk - attacker.defense())
        else:
            def_hit = def_crit = def_dmg = 0

        # Render two columns
        mid = box.centerx
        for side, name, dmg, hit, crit, col in [
            ("ATT", attacker.name, att_dmg, att_hit, att_crit, LIGHT_BLUE),
            ("DEF", defender.name, def_dmg, def_hit, def_crit, PINK),
        ]:
            cx = x0 if side == "ATT" else mid + 10
            name_s = self.font_sm.render(name, True, col)
            self.screen.blit(name_s, (cx, y))
            d = self.font_sm.render(f"Dmg: {dmg}", True, WHITE)
            h = self.font_sm.render(f"Hit: {hit}%", True, WHITE)
            c = self.font_sm.render(f"Crit: {crit}%", True, YELLOW if crit > 0 else LIGHT_GREY)
            self.screen.blit(d, (cx, y + 20))
            self.screen.blit(h, (cx, y + 36))
            self.screen.blit(c, (cx, y + 52))

        # Weapon triangle notice
        if tri_att != 0:
            tri_str = "Weapon Advantage!" if tri_att > 0 else "Weapon Disadvantage"
            tri_col = YELLOW if tri_att > 0 else RED
            tri_s = self.font_sm.render(tri_str, True, tri_col)
            self.screen.blit(tri_s, (box.centerx - tri_s.get_width()//2, y + 80))

        # Confirm hint
        conf = self.font_sm.render("Z/Enter: Attack   X/Esc: Cancel", True, LIGHT_GREY)
        self.screen.blit(conf, (box.centerx - conf.get_width()//2, box.bottom - 22))

    # ── Combat Result Animation ───────────────────────────────────────────────

    def render_combat_result(self, result, screen_x, screen_y):
        """Show damage numbers / miss flash (simple version)."""
        for rnd in result.rounds:
            if rnd.hit:
                color = RED if rnd.crit else WHITE
                label = f"-{rnd.damage}" + (" CRIT!" if rnd.crit else "")
            else:
                label = "Miss!"
                color = LIGHT_GREY
            surf = self.font_md.render(label, True, color)
            self.screen.blit(surf, (screen_x, screen_y))
            screen_y -= 20

    # ── End Screen ────────────────────────────────────────────────────────────

    def _render_end_screen(self, gs, victory=True):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        cx = SCREEN_WIDTH // 2
        if victory:
            t1 = self.font_title.render("VICTORY", True, GOLD)
            t2 = self.font_md.render(gs.current_chapter.narrative_victory.split("\n")[0], True, CREAM)
        else:
            t1 = self.font_title.render("DEFEAT", True, DARK_RED)
            t2 = self.font_md.render(gs.current_chapter.narrative_defeat.split("\n")[0], True, CREAM)

        self.screen.blit(t1, t1.get_rect(center=(cx, 250)))
        self.screen.blit(t2, t2.get_rect(center=(cx, 330)))

        # Full narrative
        y = 380
        narrative = (gs.current_chapter.narrative_victory if victory
                     else gs.current_chapter.narrative_defeat)
        for line in narrative.split("\n")[1:]:
            s = self.font_sm.render(line, True, LIGHT_GREY)
            self.screen.blit(s, s.get_rect(center=(cx, y)))
            y += 24

        if victory:
            prompt = "Press ENTER for next chapter  |  ESC to return to title"
        else:
            prompt = "Press ENTER to retry  |  ESC to return to title"
        p = self.font_sm.render(prompt, True, LIGHT_GREY)
        self.screen.blit(p, p.get_rect(center=(cx, 650)))


# ── Color helpers ─────────────────────────────────────────────────────────────

def _darken(color, amount):
    return tuple(max(0, c - amount) for c in color[:3])

def _lighten(color, amount):
    return tuple(min(255, c + amount) for c in color[:3])
