'''
Renderer for Sengoku Tactics
Includes: map, units, overlays, UI panel, combat preview,
          stat sheet (FE-style), boss dialog, tutorial overlay,
          touch/mouse button controls, recruit dialog.
'''
import pygame
from game.constants import *
from game.tutorial import TUTORIAL_STAGES


def _darken(c, n):  return tuple(max(0, v-n) for v in c[:3])
def _lighten(c, n): return tuple(min(255, v+n) for v in c[:3])

# Fire Emblem full stat names (for stat sheet display)
FE_STAT_LABELS = {
    "HP":  "HP  (Hit Points)",
    "STR": "STR (Strength)",
    "MAG": "MAG (Magic)",
    "SKL": "SKL (Skill)",
    "SPD": "SPD (Speed)",
    "LCK": "LCK (Luck)",
    "DEF": "DEF (Defense)",
    "RES": "RES (Resistance)",
    "MOV": "MOV (Movement)",
}


class Renderer:
    # Zoom tile-size steps (pixels per tile)
    _ZOOM_STEPS = [24, 32, 40, 48, 56, 64]
    _ZOOM_DEFAULT = 3   # index into _ZOOM_STEPS → 48 px (TILE_SIZE)

    def __init__(self, screen, font_sm, font_md, font_lg, font_title):
        self.screen     = screen
        self.font_sm    = font_sm
        self.font_md    = font_md
        self.font_lg    = font_lg
        self.font_title = font_title
        self.cam_x = self.cam_y = 0
        self.map_rect = pygame.Rect(0, 0, SCREEN_WIDTH - UI_PANEL_WIDTH, SCREEN_HEIGHT)
        self.ui_rect  = pygame.Rect(SCREEN_WIDTH - UI_PANEL_WIDTH, 0,
                                    UI_PANEL_WIDTH, SCREEN_HEIGHT)
        self._zoom_idx = self._ZOOM_DEFAULT
        self._scaled_tile_cache = {}   # ts → {terrain: surface}
        self._build_terrain_surfaces()

    @property
    def ts(self):
        '''Current tile size in pixels (zoom-adjusted).'''
        return self._ZOOM_STEPS[self._zoom_idx]

    def zoom_in(self):
        if self._zoom_idx < len(self._ZOOM_STEPS) - 1:
            self._zoom_idx += 1

    def zoom_out(self):
        if self._zoom_idx > 0:
            self._zoom_idx -= 1

    def _get_scaled_tile(self, terrain, ts):
        '''Return terrain surface scaled to ts×ts, cached.'''
        if ts not in self._scaled_tile_cache:
            self._scaled_tile_cache[ts] = {}
        cache = self._scaled_tile_cache[ts]
        if terrain not in cache:
            base = self._tile_surfs.get(terrain, self._tile_surfs[TERRAIN_PLAIN])
            cache[terrain] = pygame.transform.scale(base, (ts, ts))
        return cache[terrain]

    # ── Terrain tile cache ────────────────────────────────────────────────────
    def _build_terrain_surfaces(self):
        self._tile_surfs = {}
        for terrain, data in TERRAIN_DATA.items():
            s = pygame.Surface((TILE_SIZE, TILE_SIZE))
            c = data["color"]
            s.fill(c)
            pygame.draw.rect(s, _darken(c, 20), s.get_rect(), 1)
            self._add_texture(s, terrain, c)
            self._tile_surfs[terrain] = s

    def _add_texture(self, surf, t, bc):
        if t == TERRAIN_FOREST:
            for p in [(12,10),(28,8),(20,22),(10,32),(34,28)]:
                pygame.draw.circle(surf, _darken(bc,30), p, 5)
        elif t in (TERRAIN_MOUNTAIN, TERRAIN_PEAK):
            pygame.draw.polygon(surf, _darken(bc,40), [(8,40),(16,18),(24,40)])
            pygame.draw.polygon(surf, _darken(bc,30), [(22,40),(32,16),(44,40)])
        elif t in (TERRAIN_RIVER, TERRAIN_SEA):
            for i in range(0, TILE_SIZE, 8):
                pygame.draw.arc(surf, _lighten(bc,30),
                                pygame.Rect(i-4,16,12,10), 0, 3.14, 2)
        elif t == TERRAIN_CASTLE:
            pygame.draw.rect(surf, _darken(bc,40),
                             pygame.Rect(4,4,TILE_SIZE-8,TILE_SIZE-8), 2)
            for bx in range(6, TILE_SIZE-6, 8):
                pygame.draw.rect(surf, _darken(bc,40), pygame.Rect(bx,2,5,6))
        elif t == TERRAIN_GATE:
            pygame.draw.rect(surf, _darken(bc,50), surf.get_rect(), 3)
            pygame.draw.rect(surf, _darken(bc,30),
                             pygame.Rect(8,8,TILE_SIZE-16,TILE_SIZE-16), 2)
        elif t == TERRAIN_ROAD:
            pygame.draw.rect(surf, _darken(bc,15),
                             pygame.Rect(0,TILE_SIZE//2-4,TILE_SIZE,8))
        elif t == TERRAIN_FORT:
            pygame.draw.rect(surf, _darken(bc,35),
                             pygame.Rect(8,8,TILE_SIZE-16,TILE_SIZE-16), 3)
        elif t == TERRAIN_VILLAGE:
            pygame.draw.polygon(surf, _darken(bc,40),
                                [(TILE_SIZE//2,8),(10,28),(TILE_SIZE-10,28)])
            pygame.draw.rect(surf, _darken(bc,30), pygame.Rect(14,28,20,16))
        elif t == TERRAIN_BRIDGE:
            pygame.draw.rect(surf, _darken(bc,20), pygame.Rect(0,18,TILE_SIZE,12))
            for bx in range(0, TILE_SIZE, 10):
                pygame.draw.rect(surf, _darken(bc,35), pygame.Rect(bx,18,4,12))
        elif t == TERRAIN_RUINS:
            for rx in range(4, TILE_SIZE-4, 12):
                h = 8+(rx%16)
                pygame.draw.rect(surf, _darken(bc,30), pygame.Rect(rx,TILE_SIZE-h,8,h))
        elif t == TERRAIN_THICKET:
            for p in [(8,8),(24,6),(16,20),(6,30),(32,26),(20,36)]:
                pygame.draw.circle(surf, _darken(bc,25), p, 4)

    # ── Camera ────────────────────────────────────────────────────────────────
    def center_camera(self, gmap, cx, cy):
        ts = self.ts
        vw = self.map_rect.width  // ts
        vh = self.map_rect.height // ts
        self.cam_x = max(0, min(cx - vw//2, gmap.width  - vw))
        self.cam_y = max(0, min(cy - vh//2, gmap.height - vh))

    def clamp_camera(self, gmap):
        '''Clamp camera without centering (used after drag scroll).'''
        ts = self.ts
        vw = self.map_rect.width  // ts
        vh = self.map_rect.height // ts
        self.cam_x = max(0, min(self.cam_x, gmap.width  - vw))
        self.cam_y = max(0, min(self.cam_y, gmap.height - vh))

    def tile_to_screen(self, tx, ty):
        ts = self.ts
        return (tx-self.cam_x)*ts, (ty-self.cam_y)*ts

    def screen_to_tile(self, sx, sy):
        ts = self.ts
        return sx//ts + self.cam_x, sy//ts + self.cam_y

    # ── Top-level render dispatcher ───────────────────────────────────────────
    def render(self, gs, showing_help=False):
        self.screen.fill(BLACK)
        s = gs.state
        if s == STATE_TITLE:
            self._render_title(gs)
        elif s == STATE_MODE_SELECT:
            self._render_mode_select(gs)
        elif s == STATE_PROLOGUE:
            self._render_prologue(gs)
        elif s == STATE_SCENE:
            self._render_scene(gs)
        elif s == STATE_PREP:
            self._render_prep_screen(gs)
        elif s == STATE_CHAPTER_INTRO:
            self._render_chapter_intro(gs)
        elif s in (STATE_PLAYER_TURN, STATE_ENEMY_TURN, STATE_ALLY_TURN,
                   STATE_COMBAT, STATE_MENU, STATE_REINFORCE):
            self._render_map(gs)
            self._render_units(gs)
            self._render_overlays(gs)
            self._render_cursor(gs)
            self._render_ui_panel(gs)
            if gs.message_queue:
                self._render_message_box(gs)
        elif s == STATE_TUTORIAL:
            self._render_map(gs)
            self._render_units(gs)
            self._render_overlays(gs)
            self._render_cursor(gs)
            self._render_ui_panel(gs)
        elif s in (STATE_VICTORY, STATE_GAME_OVER):
            self._render_map(gs)
            self._render_units(gs)
            self._render_end_screen(gs, victory=(s == STATE_VICTORY))
        # Help overlay drawn on top of everything, any state
        if showing_help:
            self._render_help_overlay()

    # ── Title ─────────────────────────────────────────────────────────────────
    def _render_title(self, gs):
        for i in range(SCREEN_HEIGHT):
            t = i/SCREEN_HEIGHT
            pygame.draw.line(self.screen,
                             (int(20+t*60),int(10+t*20),int(5+t*10)),
                             (0,i),(SCREEN_WIDTH,i))
        cx = SCREEN_WIDTH//2
        self._blit_center(self.font_title.render("SENGOKU TACTICS",True,GOLD),cx,150)
        self._blit_center(self.font_lg.render("Age of the Warring States",True,CREAM),cx,230)
        pygame.draw.line(self.screen,GOLD,(cx-340,265),(cx+340,265),2)
        feats = "20 Chapters · 60+ Officers · Flying & Mounted · Touch Controls"
        self._blit_center(self.font_sm.render(feats,True,LIGHT_GREY),cx,280)

        # Mode buttons
        self._draw_rounded_box(cx-180,320,340,46,(20,30,60),GOLD,r=10)
        self._blit_center(self.font_md.render("ENTER / Tap → New Game",True,GOLD),cx,342)
        self._draw_rounded_box(cx-130,376,250,40,(20,30,40),(100,120,180),r=8)
        self._blit_center(self.font_sm.render("S → Skip Tutorial",True,LIGHT_GREY),cx,395)

        controls = [
            "Arrows/WASD or D-Pad: Move cursor",
            "Z/Enter or Tap: Select/Confirm   X/Esc or ✕: Cancel",
            "A/⚔: Attack   H/♥: Heal   W/Zz: Wait",
            "T/!: Talk-Recruit   I/i: Stat Sheet   E/★: Seize",
            "Space/▶▶: End Turn",
        ]
        y = 430
        for line in controls:
            self._blit_center(self.font_sm.render(line,True,LIGHT_GREY),cx,y)
            y += 22

    # ── Mode Select ───────────────────────────────────────────────────────────
    def _render_mode_select(self, gs):
        '''Difficulty + Deploy mode selection screen (two rows).'''
        from game.constants import DEPLOY_FORCED, DEPLOY_FREE
        # Background gradient
        for i in range(SCREEN_HEIGHT):
            t = i / SCREEN_HEIGHT
            pygame.draw.line(self.screen,
                             (int(20+t*60), int(10+t*20), int(5+t*10)),
                             (0, i), (SCREEN_WIDTH, i))
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2

        # _mode_cursor encodes both rows:
        # row 0 = difficulty (0=Classic, 1=Casual), row 1 = deploy (0=Forced, 1=Free)
        # We store them as _mode_cursor (0/1) and _deploy_cursor (0/1)
        mode_sel   = getattr(gs, '_mode_cursor',   0)
        deploy_sel = getattr(gs, '_deploy_cursor',  0)
        active_row = getattr(gs, '_mode_row',       0)   # 0=difficulty row, 1=deploy row

        # ── Header ───────────────────────────────────────────────────────────
        self._blit_center(self.font_lg.render("Choose Your Mode", True, GOLD), cx, cy - 230)
        pygame.draw.line(self.screen, GOLD, (cx-300, cy-202), (cx+300, cy-202), 2)

        # ── Row 0: Difficulty ─────────────────────────────────────────────────
        row0_y = cy - 190

        # Classic
        classic_border = GOLD if (active_row==0 and mode_sel==0) else (80,80,80)
        classic_bg     = (40,20,10) if (active_row==0 and mode_sel==0) else (20,20,20)
        self._draw_rounded_box(cx-260, row0_y, 220, 150, classic_bg, classic_border, r=10)
        self._blit_center(self.font_md.render("⚔  CLASSIC", True,
            GOLD if (active_row==0 and mode_sel==0) else LIGHT_GREY), cx-150, row0_y+22)
        for i, line in enumerate(["Permanent death.", "Fallen officers lost forever.",
                                   "", "True Bushido."]):
            col = CREAM if (active_row==0 and mode_sel==0) else (120,120,120)
            self._blit_center(self.font_sm.render(line, True, col), cx-150, row0_y+50+i*18)

        # Casual
        casual_border  = GOLD if (active_row==0 and mode_sel==1) else (80,80,80)
        casual_bg      = (10,30,50) if (active_row==0 and mode_sel==1) else (20,20,20)
        self._draw_rounded_box(cx+40, row0_y, 220, 150, casual_bg, casual_border, r=10)
        self._blit_center(self.font_md.render("✿  CASUAL", True,
            GOLD if (active_row==0 and mode_sel==1) else LIGHT_GREY), cx+150, row0_y+22)
        for i, line in enumerate(["Units revive next chapter.", "Focus on story",
                                   "and strategy.", ""]):
            col = CREAM if (active_row==0 and mode_sel==1) else (120,120,120)
            self._blit_center(self.font_sm.render(line, True, col), cx+150, row0_y+50+i*18)

        # Active row 0 indicator arrow
        if active_row == 0:
            arr = self.font_md.render("▶", True, GOLD)
            self.screen.blit(arr, (cx-300, row0_y+55))

        # ── Row 1: Deploy Mode ────────────────────────────────────────────────
        row1_y = cy - 20
        pygame.draw.line(self.screen, (80,70,30), (cx-300, row1_y-8), (cx+300, row1_y-8), 1)
        self._blit_center(self.font_sm.render("DEPLOYMENT MODE", True, (160,140,60)), cx, row1_y-18)

        # Forced
        forced_border = GOLD if (active_row==1 and deploy_sel==0) else (80,80,80)
        forced_bg     = (35,15,40) if (active_row==1 and deploy_sel==0) else (20,20,20)
        self._draw_rounded_box(cx-260, row1_y, 220, 130, forced_bg, forced_border, r=10)
        self._blit_center(self.font_md.render("FORCED", True,
            GOLD if (active_row==1 and deploy_sel==0) else LIGHT_GREY), cx-150, row1_y+18)
        for i, line in enumerate(["Chapter pre-selects", "key story units.",
                                   "Curated experience."]):
            col = CREAM if (active_row==1 and deploy_sel==0) else (120,120,120)
            self._blit_center(self.font_sm.render(line, True, col), cx-150, row1_y+44+i*18)

        # Free
        free_border = GOLD if (active_row==1 and deploy_sel==1) else (80,80,80)
        free_bg     = (10,35,20) if (active_row==1 and deploy_sel==1) else (20,20,20)
        self._draw_rounded_box(cx+40, row1_y, 220, 130, free_bg, free_border, r=10)
        self._blit_center(self.font_md.render("FREE CHOICE", True,
            GOLD if (active_row==1 and deploy_sel==1) else LIGHT_GREY), cx+150, row1_y+18)
        for i, line in enumerate(["Pick any units you", "have unlocked.",
                                   "Full strategic freedom."]):
            col = CREAM if (active_row==1 and deploy_sel==1) else (120,120,120)
            self._blit_center(self.font_sm.render(line, True, col), cx+150, row1_y+44+i*18)

        # Active row 1 indicator arrow
        if active_row == 1:
            arr = self.font_md.render("▶", True, GOLD)
            self.screen.blit(arr, (cx-300, row1_y+50))

        # ── Summary label ─────────────────────────────────────────────────────
        diff_str   = "Classic" if mode_sel==0 else "Casual"
        deploy_str = "Forced" if deploy_sel==0 else "Free Choice"
        label = f"{diff_str}  |  {deploy_str} Deployment"
        self._blit_center(self.font_md.render(label, True, GOLD), cx, row1_y + 150)

        # ── Controls hint ─────────────────────────────────────────────────────
        hints = [
            "Up/Down: Switch row   Left/Right: Switch option",
            "Enter / Z: Confirm all selections",
        ]
        hy = row1_y + 175
        for h in hints:
            self._blit_center(self.font_sm.render(h, True, LIGHT_GREY), cx, hy)
            hy += 22

    # ── Pre-battle Scene Dialog ───────────────────────────────────────────────
    def _render_scene(self, gs):
        '''
        Visual-novel style scene: full dark background, left portrait box,
        speaker name bar, and dialogue text box at bottom — like Fire Emblem DS.
        '''
        from game.scene_dialogs import PORTRAIT_COLORS
        ch  = gs.current_chapter
        idx = gs.scene_dialog_idx
        lines = gs.scene_dialog

        if not lines or idx >= len(lines):
            return

        speaker_key, display_name, text = lines[idx]
        total = len(lines)

        W, H = SCREEN_WIDTH, SCREEN_HEIGHT

        # ── Background ────────────────────────────────────────────────────────
        # Dark ink-wash gradient
        for i in range(H):
            t = i / H
            r = int(8  + t * 20)
            g = int(8  + t * 15)
            b = int(18 + t * 30)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (W, i))

        # Subtle chapter label top-left
        ch_surf = self.font_sm.render(f"{ch.title}  ·  {ch.subtitle}", True, (120, 100, 60))
        self.screen.blit(ch_surf, (20, 14))

        # ── Portrait box (left side, mid-screen) ─────────────────────────────
        portrait_color = PORTRAIT_COLORS.get(speaker_key, (60, 60, 80))
        pw, ph = 160, 200
        px, py = 40, H // 2 - ph // 2 - 30

        # Shadow
        shadow = pygame.Surface((pw + 6, ph + 6), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 120))
        self.screen.blit(shadow, (px - 2, py + 4))

        # Portrait panel
        pygame.draw.rect(self.screen, portrait_color, (px, py, pw, ph))
        pygame.draw.rect(self.screen, GOLD, (px, py, pw, ph), 3)

        # Speaker initial / icon centred in portrait
        initial = display_name[0].upper() if display_name else "?"
        ic = self.font_title.render(initial, True, (255, 255, 255, 180))
        self.screen.blit(ic, (px + pw // 2 - ic.get_width() // 2,
                               py + ph // 2 - ic.get_height() // 2))

        # ── Dialogue box (bottom strip) ───────────────────────────────────────
        box_h   = 180
        box_y   = H - box_h - 10
        box_x   = 30
        box_w   = W - 60

        # Semi-transparent backing
        dlg_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        dlg_surf.fill((10, 12, 30, 220))
        self.screen.blit(dlg_surf, (box_x, box_y))
        pygame.draw.rect(self.screen, GOLD, (box_x, box_y, box_w, box_h), 2)

        # Speaker name bar
        name_bar_h = 30
        name_bar_surf = pygame.Surface((200, name_bar_h), pygame.SRCALPHA)
        name_bar_surf.fill((*portrait_color, 230))
        self.screen.blit(name_bar_surf, (box_x + 10, box_y - name_bar_h + 2))
        pygame.draw.rect(self.screen, GOLD,
                         (box_x + 10, box_y - name_bar_h + 2, 200, name_bar_h), 1)
        name_surf = self.font_md.render(display_name, True, WHITE)
        self.screen.blit(name_surf, (box_x + 18, box_y - name_bar_h + 6))

        # Dialogue text (wrapped)
        text_x = box_x + 20
        text_y = box_y + 18
        max_chars = (box_w - 40) // 8   # approximate chars per line at font_md
        wrapped = self._wrap(text, max_chars)
        for wline in wrapped[:5]:   # max 5 lines in box
            self.screen.blit(self.font_md.render(wline, True, CREAM), (text_x, text_y))
            text_y += 28

        # ── Progress dots and advance hint ────────────────────────────────────
        dot_y = box_y + box_h - 22
        dot_spacing = 14
        dot_start_x = box_x + 20
        for i in range(total):
            col = GOLD if i == idx else (80, 70, 40)
            pygame.draw.circle(self.screen, col,
                               (dot_start_x + i * dot_spacing, dot_y), 4)

        hint = "Z / Enter / Tap  ▶  to continue"
        hint_surf = self.font_sm.render(hint, True, (160, 150, 100))
        self.screen.blit(hint_surf,
                         (W - hint_surf.get_width() - 30, dot_y - 6))

        # ── Line counter top-right ─────────────────────────────────────────────
        ctr = self.font_sm.render(f"{idx+1} / {total}", True, (120, 110, 70))
        self.screen.blit(ctr, (W - ctr.get_width() - 20, 14))

    # ── Chapter Intro ─────────────────────────────────────────────────────────
    def _render_chapter_intro(self, gs):
        self.screen.fill((10,10,20))
        ch = gs.current_chapter
        cx = SCREEN_WIDTH//2
        self._blit_center(self.font_lg.render(ch.title,True,GOLD),cx,65)
        self._blit_center(self.font_md.render(ch.subtitle,True,CREAM),cx,105)
        # Narrative
        self._draw_rounded_box(60,135,SCREEN_WIDTH-120,390,(15,15,35),GOLD,r=6)
        y=155
        for line in ch.narrative_intro.split("\n"):
            self.screen.blit(self.font_sm.render(line,True,CREAM),(80,y)); y+=26
        # Objective bar
        self._draw_rounded_box(60,538,SCREEN_WIDTH-120,62,(30,20,10),GOLD,r=6)
        self.screen.blit(
            self.font_sm.render("Objective: "+ch.objective_detail,True,YELLOW),(80,555))
        if ch.reinforcements:
            w = ch.reinforcements[0]
            self._blit_center(
                self.font_sm.render(f"⚠ Reinforcements on Turn {w.turn}!",True,RED),cx,612)
        # Participating units preview
        unit_labels = [f"{uid.split('_')[0].capitalize()}" for uid,_,_ in ch.player_unit_defs[:8]]
        self._blit_center(
            self.font_sm.render("Player units: " + "  ".join(unit_labels),True,LIGHT_BLUE),cx,638)
        self._blit_center(self.font_sm.render("Z/Enter or tap to begin",True,LIGHT_GREY),cx,660)

    # ── Map ───────────────────────────────────────────────────────────────────
    def _render_map(self, gs):
        ts = self.ts
        gmap = gs.game_map
        pygame.draw.rect(self.screen,(30,30,30),self.map_rect)
        vw = self.map_rect.width  // ts + 2
        vh = self.map_rect.height // ts + 2
        for ty in range(self.cam_y, min(self.cam_y+vh, gmap.height)):
            for tx in range(self.cam_x, min(self.cam_x+vw, gmap.width)):
                t  = gmap.get_terrain(tx, ty)
                s  = self._get_scaled_tile(t, ts)
                sx, sy = self.tile_to_screen(tx, ty)
                self.screen.blit(s, (sx, sy))
        pygame.draw.rect(self.screen,DARK_GREY,self.map_rect,2)

    # ── Overlays ──────────────────────────────────────────────────────────────
    def _render_overlays(self, gs):
        ts = self.ts
        def stamp(tx, ty, color, alpha, border=None, border_alpha=200):
            sx, sy = self.tile_to_screen(tx, ty)
            if not self.map_rect.collidepoint(sx+ts//2, sy+ts//2):
                return
            ov = pygame.Surface((ts, ts), pygame.SRCALPHA)
            ov.fill((*color, alpha))
            self.screen.blit(ov,(sx,sy))
            if border:
                pygame.draw.rect(self.screen,(*border,border_alpha),
                                 (sx,sy,ts,ts),2)

        # Seize points
        for (sx,sy) in gs.game_map.seize_points:
            stamp(sx,sy,(200,170,20),90,GOLD,220)
            self.screen.blit(
                self.font_sm.render("★",True,GOLD),
                (sx*ts - self.cam_x*ts+2,
                 sy*ts - self.cam_y*ts+2))

        if gs.selected_unit:
            for (tx,ty) in getattr(gs,'move_range_land',set()):
                stamp(tx,ty,(60,100,220),100,(80,130,255))
            for (tx,ty) in gs.attack_range:
                stamp(tx,ty,(220,60,60),80,(255,90,90))
            for t in gs.get_recruitable_adjacent(gs.selected_unit):
                stamp(t.x,t.y,(40,210,90),100,(50,240,110))

    # ── Units ─────────────────────────────────────────────────────────────────
    def _render_units(self, gs):
        ts = self.ts
        for unit in gs.all_units():
            if not unit.alive:
                continue
            sx,sy = self.tile_to_screen(unit.x, unit.y)
            if not self.map_rect.collidepoint(sx+ts//2, sy+ts//2):
                continue
            self._draw_unit(unit, sx, sy, gs)

    def _draw_unit(self, unit, sx, sy, gs):
        ts  = self.ts
        cx_ = sx+ts//2; cy_ = sy+ts//2
        r   = max(4, ts//2 - 3)
        color = unit.color
        if unit.has_acted and unit.faction == FACTION_PLAYER:
            color = _darken(color,80)
        # Shadow / flying altitude shadow
        if unit.is_flying:
            pygame.draw.ellipse(self.screen,_darken(color,80),(sx+4,sy+ts-10,ts-8,8))
        else:
            pygame.draw.circle(self.screen,_darken(color,50),(cx_+2,cy_+2),r)
        pygame.draw.circle(self.screen,color,(cx_,cy_),r)
        border = {FACTION_PLAYER:(80,180,255),
                  FACTION_ENEMY:(255,80,80),
                  FACTION_ALLY:(80,255,120)}.get(unit.faction,WHITE)
        pygame.draw.circle(self.screen,border,(cx_,cy_),r,2)
        # Flying ring
        if unit.is_flying:
            pygame.draw.circle(self.screen,(200,200,255),(cx_,cy_),r+2,1)
        # Mounted chevrons
        if unit.is_mounted:
            pygame.draw.lines(self.screen,(255,220,100),False,
                              [(cx_-5,cy_+r-5),(cx_,cy_+r-9),(cx_+5,cy_+r-5)],1)
        sym = unit.symbol[:2]
        self.screen.blit(self.font_sm.render(sym,True,WHITE),
                         self.font_sm.render(sym,True,WHITE).get_rect(center=(cx_,cy_-2)))
        # HP bar
        bw=ts-8; bh=4; bx=sx+4; by=sy+ts-7
        pct=unit.hp/unit.max_hp
        hc=GREEN if pct>0.5 else YELLOW if pct>0.25 else RED
        pygame.draw.rect(self.screen,DARK_GREY,(bx,by,bw,bh))
        pygame.draw.rect(self.screen,hc,       (bx,by,int(bw*pct),bh))
        # Selected
        if gs.selected_unit==unit:
            pygame.draw.rect(self.screen,WHITE,(sx+1,sy+1,ts-2,ts-2),2)
        if unit.is_lord:
            self.screen.blit(self.font_sm.render("♦",True,GOLD),(sx+ts-14,sy+1))
        if unit.can_recruit and not unit.recruited:
            self.screen.blit(self.font_sm.render("!",True,(50,220,100)),(sx+ts-12,sy+ts-16))

    # ── Cursor ────────────────────────────────────────────────────────────────
    def _render_cursor(self, gs):
        ts = self.ts
        sx,sy = self.tile_to_screen(gs.cursor_x, gs.cursor_y)
        if not self.map_rect.collidepoint(sx+ts//2, sy+ts//2):
            return
        alpha = int(160+80*abs((pygame.time.get_ticks()%1000)/500-1))
        cs = pygame.Surface((ts,ts),pygame.SRCALPHA)
        pygame.draw.rect(cs,(255,255,255,min(255,alpha)),(0,0,ts,ts),3)
        self.screen.blit(cs,(sx,sy))

    # ── UI Panel ──────────────────────────────────────────────────────────────
    def _render_ui_panel(self, gs):
        p = self.ui_rect
        pygame.draw.rect(self.screen,(20,20,35),p)
        pygame.draw.rect(self.screen,GOLD,p,2)
        x0=p.x+10; y=p.y+10

        phase_str={FACTION_PLAYER:"Player Phase",FACTION_ENEMY:"Enemy Phase",
                   FACTION_ALLY:"Ally Phase"}.get(gs.phase,"")
        phase_col={FACTION_PLAYER:LIGHT_BLUE,FACTION_ENEMY:PINK,
                   FACTION_ALLY:(100,255,150)}.get(gs.phase,WHITE)
        self.screen.blit(self.font_md.render(f"Turn {gs.turn}",True,GOLD),(x0,y)); y+=28
        self.screen.blit(self.font_sm.render(phase_str,True,phase_col),(x0,y)); y+=20
        self.screen.blit(self.font_sm.render(gs.game_map.name,True,LIGHT_GREY),(x0,y)); y+=18
        # Mode badge
        mode_label = "⚔ Classic" if getattr(gs,"classic_mode",True) else "✿ Casual"
        mode_col   = (220,80,40) if getattr(gs,"classic_mode",True) else (80,180,240)
        self.screen.blit(self.font_sm.render(mode_label,True,mode_col),(x0,y)); y+=18
        pygame.draw.line(self.screen,GOLD,(x0,y),(p.right-10,y),1); y+=8

        hovered = gs.unit_at(gs.cursor_x,gs.cursor_y)
        display  = gs.selected_unit or hovered
        if display:
            y=self._render_unit_card(display,x0,y,p.right-10)
        else:
            terrain=gs.game_map.get_terrain(gs.cursor_x,gs.cursor_y)
            y=self._render_terrain_info(terrain,TERRAIN_DATA[terrain],x0,y)

        # Objective
        ch=gs.current_chapter
        if ch:
            pygame.draw.line(self.screen,GOLD,(x0,p.bottom-310),(p.right-10,p.bottom-310),1)
            oy=p.bottom-302
            self.screen.blit(self.font_sm.render("Objective:",True,YELLOW),(x0,oy)); oy+=18
            for w in self._wrap(ch.objective_detail, p.width-20):
                self.screen.blit(self.font_sm.render(w,True,CREAM),(x0,oy)); oy+=16

            # ── Side objectives ──────────────────────────────────────────────
            side_objs = getattr(gs, 'active_side_objectives', [])
            pending_objs = [so for so in side_objs if not so.completed and not so.failed]
            if pending_objs:
                pygame.draw.line(self.screen,(80,70,30),(x0,oy),(p.right-10,oy),1); oy+=4
                self.screen.blit(self.font_sm.render("Side:",True,(180,160,80)),(x0,oy)); oy+=16
                for so in pending_objs[:3]:
                    short = so.description[:22] + ("…" if len(so.description)>22 else "")
                    self.screen.blit(self.font_sm.render(f"▷ {short}",True,(140,200,120)),(x0,oy)); oy+=14

        # Controls hint
        pygame.draw.line(self.screen,GOLD,(x0,p.bottom-155),(p.right-10,p.bottom-155),1)
        cy_=p.bottom-148
        for line in ["Arrows/D-Pad: Move","Z/Enter/Tap: Select",
                     "A:Atk H:Heal W:Wait","T:Talk E:Seize I:Info",
                     "Space/▶▶: End Turn"]:
            self.screen.blit(self.font_sm.render(line,True,LIGHT_GREY),(x0,cy_)); cy_+=17

    def _render_unit_card(self, unit, x0, y, x1):
        self.screen.blit(self.font_md.render(unit.name,True,WHITE),(x0,y)); y+=25
        self.screen.blit(self.font_sm.render(f"{unit.unit_class}  Lv{unit.level}",
                         True,LIGHT_GREY),(x0,y)); y+=18
        # Tags
        tags=[]
        if unit.is_lord:    tags.append(("LORD♦",GOLD))
        if unit.is_flying:  tags.append(("FLY",(200,200,255)))
        if unit.is_mounted: tags.append(("MNT",COPPER))
        if unit.water_walk: tags.append(("SEA",BLUE))
        if unit.can_recruit and not unit.recruited:
            tags.append(("RECRUIT",(50,220,100)))
        tx_=x0
        for tg,tc in tags:
            ts=self.font_sm.render(f"[{tg}]",True,tc)
            self.screen.blit(ts,(tx_,y)); tx_+=ts.get_width()+5
        if tags: y+=16
        fc_col={FACTION_PLAYER:LIGHT_BLUE,FACTION_ENEMY:PINK,
                FACTION_ALLY:(100,255,150)}.get(unit.faction,WHITE)
        self.screen.blit(self.font_sm.render(unit.faction.upper(),True,fc_col),(x0,y)); y+=18
        # HP
        bw=x1-x0
        pct=unit.hp/unit.max_hp
        hc=GREEN if pct>0.5 else YELLOW if pct>0.25 else RED
        pygame.draw.rect(self.screen,DARK_GREY,(x0,y,bw,8))
        pygame.draw.rect(self.screen,hc,(x0,y,int(bw*pct),8))
        self.screen.blit(self.font_sm.render(f"HP {unit.hp}/{unit.max_hp}",True,WHITE),(x0,y+10)); y+=26
        # Stats (FE labels)
        stats=[("STR",unit.str_),("MAG",unit.mag),("SKL",unit.skl),("SPD",unit.spd),
               ("LCK",unit.lck),("DEF",unit.def_),("RES",unit.res),("MOV",unit.move)]
        cw=(x1-x0)//2
        for i,(lb,vl) in enumerate(stats):
            self.screen.blit(self.font_sm.render(f"{lb}:{vl:3d}",True,LIGHT_GREY),
                             (x0+(i%2)*cw, y+(i//2)*16))
        y+=(len(stats)//2)*16+6
        # Equipped weapon
        if unit.equipped:
            w=unit.equipped
            pygame.draw.line(self.screen,GOLD,(x0,y),(x1,y),1); y+=4
            self.screen.blit(self.font_sm.render(w.name,True,WHITE),(x0,y)); y+=14
            self.screen.blit(self.font_sm.render(
                f"Mt:{w.might} Hit:{w.hit}% Crit:{w.crit}% {w.min_range}-{w.max_range}rng",
                True,LIGHT_GREY),(x0,y)); y+=14
        # EXP
        pygame.draw.line(self.screen,GOLD,(x0,y),(x1,y),1); y+=3
        pygame.draw.rect(self.screen,DARK_GREY,(x0,y,bw,5))
        pygame.draw.rect(self.screen,CYAN,(x0,y,int(bw*unit.exp/100),5))
        self.screen.blit(self.font_sm.render(f"EXP {unit.exp}/100",True,LIGHT_GREY),(x0,y+7)); y+=20
        return y

    def _render_terrain_info(self, terrain, td, x0, y):
        self.screen.blit(self.font_md.render(td["name"],True,WHITE),(x0,y)); y+=22
        for lb,vl in [("Def Bonus",f"+{td['def']}"),
                      ("Avo Bonus",f"+{td['avo']}"),
                      ("Move Cost",str(td['move']))]:
            self.screen.blit(self.font_sm.render(f"{lb}: {vl}",True,LIGHT_GREY),(x0,y)); y+=17
        return y

    # ── Message box ───────────────────────────────────────────────────────────
    def _render_message_box(self, gs):
        if not gs.message_queue: return
        msg=gs.message_queue[0]
        box=pygame.Rect(SCREEN_WIDTH//2-310,SCREEN_HEIGHT-100,620,78)
        pygame.draw.rect(self.screen,(12,12,28),box)
        pygame.draw.rect(self.screen,GOLD,box,2)
        ms=self.font_md.render(msg,True,WHITE)
        self.screen.blit(ms,ms.get_rect(center=box.center))
        self.screen.blit(self.font_sm.render("Z / Enter / Tap to continue",True,LIGHT_GREY),
                         (box.x+10,box.bottom-18))

    # ── Combat Preview ────────────────────────────────────────────────────────
    def render_combat_preview(self, attacker, defender, gmap):
        box=pygame.Rect(180,SCREEN_HEIGHT//2-120,SCREEN_WIDTH-360,240)
        pygame.draw.rect(self.screen,(10,10,25),box)
        pygame.draw.rect(self.screen,GOLD,box,2)
        cx=box.centerx; y=box.y+10
        self._blit_center(self.font_md.render("— Combat Forecast —",True,GOLD),cx,y); y+=32

        att_w=attacker.equipped; def_w=defender.equipped
        att_dmg=max(0,attacker.attack_power(def_w,target=defender)-defender.defense())
        att_hit=max(0,min(100,attacker.hit_rate(def_w)-defender.avoid()))
        att_crit=max(0,attacker.crit_rate(def_w)-defender.crit_avoid())

        can_ctr=(def_w and def_w.weapon_type!=WEAPON_STAFF
                 and not any(x in getattr(def_w,'weapon_id','')
                             for x in ("heal","mend","physic","amulet")))
        if can_ctr:
            def_dmg=max(0,defender.attack_power(att_w,target=attacker)-attacker.defense())
            def_hit=max(0,min(100,defender.hit_rate(att_w)-attacker.avoid()))
            def_crit=max(0,defender.crit_rate(att_w)-attacker.crit_avoid())
        else:
            def_dmg=def_hit=def_crit=0

        mid=box.centerx; x0=box.x+15
        for name,dmg,hit,crit,col in [
            (attacker.name,att_dmg,att_hit,att_crit,LIGHT_BLUE),
            (defender.name,def_dmg,def_hit,def_crit,PINK),
        ]:
            cx_=x0 if name==attacker.name else mid+10
            self.screen.blit(self.font_sm.render(name,True,col),(cx_,y))
            cls_=attacker.unit_class if name==attacker.name else defender.unit_class
            self.screen.blit(self.font_sm.render(f"({cls_})",True,LIGHT_GREY),(cx_,y+16))
            self.screen.blit(self.font_sm.render(f"Dmg:  {dmg}",True,WHITE),(cx_,y+32))
            self.screen.blit(self.font_sm.render(f"Hit:  {hit}%",True,WHITE),(cx_,y+48))
            cc=YELLOW if crit>0 else LIGHT_GREY
            self.screen.blit(self.font_sm.render(f"Crit: {crit}%",True,cc),(cx_,y+64))
        pygame.draw.line(self.screen,GOLD,(mid,y-4),(mid,y+90),1)

        if att_w:
            tri=att_w.get_triangle_bonus(def_w)
            if tri!=0:
                tc=YELLOW if tri>0 else RED
                ts="Weapon Advantage!" if tri>0 else "Weapon Disadvantage!"
                self._blit_center(self.font_sm.render(ts,True,tc),cx,y+90)

        self._blit_center(
            self.font_sm.render("Z/Enter/Tap: Confirm   X/Esc/✕: Cancel",True,LIGHT_GREY),
            cx,box.bottom-22)

    # ── Boss Dialog ───────────────────────────────────────────────────────────
    def render_boss_dialog(self, lines, line_idx, unit_roster):
        '''
        Render a multi-line cinematic boss dialog.
        lines: list of (speaker_id, text)
        line_idx: current line index
        unit_roster: dict id->Unit for portrait lookup
        '''
        if not lines or line_idx >= len(lines):
            return
        speaker_id, text = lines[line_idx]

        # Dark overlay
        ov = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,160)); self.screen.blit(ov,(0,0))

        unit = unit_roster.get(speaker_id)
        is_narrator = (speaker_id == "narrator")

        if is_narrator:
            # Simple centered narration box
            box = pygame.Rect(80,SCREEN_HEIGHT//2-70,SCREEN_WIDTH-160,140)
            pygame.draw.rect(self.screen,(15,10,30),box)
            pygame.draw.rect(self.screen,GOLD,box,2)
            self._blit_center(
                self.font_sm.render("— Narrator —",True,LIGHT_GREY),
                SCREEN_WIDTH//2, box.y+18)
            y=box.y+44
            for line in self._wrap(text, box.width-40):
                self._blit_center(self.font_sm.render(line,True,IVORY),
                                  SCREEN_WIDTH//2,y); y+=22
        else:
            # Speaker portrait + speech bubble
            # Determine left/right side: player units speak from left, enemies from right
            if unit and unit.faction == FACTION_ENEMY:
                port_x = SCREEN_WIDTH-230; bubble_x = 90; flip=True
            else:
                port_x = 90; bubble_x = 230; flip=False

            # Portrait box
            pr = pygame.Rect(port_x, SCREEN_HEIGHT-250, 130, 160)
            col = unit.color if unit else GREY
            pygame.draw.rect(self.screen, _darken(col,40), pr)
            pygame.draw.rect(self.screen, col, pr, 4)
            pygame.draw.rect(self.screen, GOLD, pr, 2)
            sym = self.font_lg.render(unit.symbol[:2] if unit else "?",True,WHITE)
            self.screen.blit(sym,sym.get_rect(center=pr.center))
            # Speaker name
            sn = unit.name if unit else speaker_id.title()
            ns = self.font_sm.render(sn,True,GOLD)
            self.screen.blit(ns,ns.get_rect(center=(pr.centerx,pr.bottom+10)))

            # Speech bubble
            bw = SCREEN_WIDTH-bubble_x-110 if not flip else bubble_x+110-90
            bw = max(300, SCREEN_WIDTH-350)
            bx = 220 if not flip else 90
            box = pygame.Rect(bx, SCREEN_HEIGHT-220, bw, 130)
            pygame.draw.rect(self.screen,(15,12,30),box,border_radius=10)
            pygame.draw.rect(self.screen,GOLD,box,2,border_radius=10)

            y=box.y+18
            for line in self._wrap(text, box.width-30):
                self.screen.blit(self.font_sm.render(line,True,CREAM),(box.x+15,y)); y+=22

        # Progress indicator
        prog=self.font_sm.render(
            f"({line_idx+1}/{len(lines)})  Z/Enter/Tap to continue — S to skip all",
            True,LIGHT_GREY)
        self.screen.blit(prog,(SCREEN_WIDTH//2-prog.get_width()//2,SCREEN_HEIGHT-30))

    # ── Tutorial Overlay ──────────────────────────────────────────────────────
    def render_tutorial(self, tm, gs):
        '''
        Render the tutorial stage overlay.
        tm: TutorialManager instance
        '''
        stage = tm.current_stage
        if stage is None or not tm.active:
            return

        # Highlight tiles with a pulsing gold glow
        ticks = pygame.time.get_ticks()
        pulse = abs((ticks % 1200) / 600 - 1)
        glow_alpha = int(60 + 80*pulse)
        for (tx,ty) in stage.highlight_tiles:
            sx,sy = self.tile_to_screen(tx,ty)
            if self.map_rect.collidepoint(sx+TILE_SIZE//2,sy+TILE_SIZE//2):
                gs_ov = pygame.Surface((TILE_SIZE,TILE_SIZE),pygame.SRCALPHA)
                gs_ov.fill((255,220,30,glow_alpha))
                self.screen.blit(gs_ov,(sx,sy))
                pygame.draw.rect(self.screen,(255,220,30,200),
                                 (sx,sy,TILE_SIZE,TILE_SIZE),2)

        # Arrow pointing at target tile
        if stage.arrow_pos:
            ax,ay = self.tile_to_screen(*stage.arrow_pos)
            ax+=TILE_SIZE//2; ay-=8
            pts = [(ax,ay),(ax-10,ay-14),(ax+10,ay-14)]
            pygame.draw.polygon(self.screen,GOLD,pts)
            pygame.draw.polygon(self.screen,WHITE,pts,1)

        # Instruction box (bottom of map area)
        bh = 170
        box = pygame.Rect(8, SCREEN_HEIGHT-bh-8, self.map_rect.width-16, bh)
        pygame.draw.rect(self.screen,(12,14,34,230),box)
        pygame.draw.rect(self.screen,GOLD,box,2)

        # Stage progress bar
        total = len(TUTORIAL_STAGES)
        bar_w = box.width-20
        done  = tm.stage_idx
        pygame.draw.rect(self.screen,DARK_GREY,(box.x+10,box.y+6,bar_w,6))
        pygame.draw.rect(self.screen,GOLD,(box.x+10,box.y+6,int(bar_w*done/total),6))

        # Title
        self.screen.blit(self.font_md.render(stage.title,True,GOLD),
                         (box.x+10,box.y+16)); y=box.y+42
        # Body lines
        for line in stage.body[:5]:
            self.screen.blit(self.font_sm.render(line,True,CREAM),(box.x+12,y)); y+=18

        # Action hint + skip
        if stage.action_hint:
            hint=self.font_sm.render(f"▶ {stage.action_hint}",True,(100,220,100))
            self.screen.blit(hint,(box.x+12,box.bottom-30))
        skip=self.font_sm.render("S = Skip Tutorial",True,LIGHT_GREY)
        self.screen.blit(skip,(box.right-skip.get_width()-10,box.bottom-18))

        # Stage counter
        ctr=self.font_sm.render(f"Step {tm.stage_idx+1}/{total}",True,LIGHT_GREY)
        self.screen.blit(ctr,(box.right-ctr.get_width()-10,box.y+16))

    # ── Stat Sheet (FE-style) ─────────────────────────────────────────────────
    def render_stat_sheet(self, unit):
        ov=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,210)); self.screen.blit(ov,(0,0))

        box=pygame.Rect(40,30,SCREEN_WIDTH-80,SCREEN_HEIGHT-60)
        pygame.draw.rect(self.screen,(10,12,26),box)
        pygame.draw.rect(self.screen,GOLD,box,3)

        # ── Left column: portrait, quote, mini-stats ─────────────────────────
        port=pygame.Rect(box.x+15,box.y+15,190,200)
        pygame.draw.rect(self.screen,_darken(unit.color,40),port)
        pygame.draw.rect(self.screen,unit.color,port,5)
        pygame.draw.rect(self.screen,GOLD,port,2)
        # Class symbol (large)
        sym=self.font_lg.render(unit.symbol,True,WHITE)
        self.screen.blit(sym,sym.get_rect(center=port.center))
        # Faction badge
        fc_col={FACTION_PLAYER:LIGHT_BLUE,FACTION_ENEMY:PINK,
                FACTION_ALLY:(100,255,150)}.get(unit.faction,WHITE)
        pygame.draw.rect(self.screen,_darken(fc_col,80),
                         (port.x,port.bottom-22,190,22))
        fcs=self.font_sm.render(unit.faction.upper(),True,fc_col)
        self.screen.blit(fcs,fcs.get_rect(center=(port.centerx,port.bottom-11)))

        # Quote box
        qy=port.bottom+12
        pygame.draw.rect(self.screen,(18,15,32),
                         pygame.Rect(box.x+15,qy,190,90))
        pygame.draw.rect(self.screen,GOLD,pygame.Rect(box.x+15,qy,190,90),1)
        qlines=self._wrap(f'"{unit.quote}"',24) if unit.quote else []
        for ql in qlines[:4]:
            self.screen.blit(self.font_sm.render(ql,True,IVORY),(box.x+20,qy+6)); qy+=18

        # Class description (if available)
        from game.constants import CLASS_DATA
        cd_desc = CLASS_DATA.get(unit.unit_class,{}).get("description","")
        if cd_desc:
            dly = port.bottom+108
            for dl in self._wrap(cd_desc, 26)[:3]:
                self.screen.blit(self.font_sm.render(dl,True,LIGHT_GREY),(box.x+15,dly)); dly+=16

        # ── Right column: name, class, stats, weapons, bio ───────────────────
        rx=port.right+20; ry=box.y+15

        # Name + class
        self.screen.blit(self.font_lg.render(unit.name,True,GOLD),(rx,ry)); ry+=38
        self.screen.blit(self.font_md.render(
            f"{unit.unit_class}  —  Level {unit.level}",True,CREAM),(rx,ry)); ry+=26

        # Tags
        tags=[]
        if unit.is_lord:    tags.append(("LORD ♦",GOLD))
        if unit.is_flying:  tags.append(("FLYING",(200,200,255)))
        if unit.is_mounted: tags.append(("MOUNTED",COPPER))
        if unit.water_walk: tags.append(("WATER WALK",BLUE))
        if unit.can_recruit and not unit.recruited:
            tags.append(("RECRUITABLE",(50,220,100)))
        tx_=rx
        for tg,tc in tags:
            ts=self.font_sm.render(f"[{tg}]",True,tc)
            self.screen.blit(ts,(tx_,ry)); tx_+=ts.get_width()+8
        if tags: ry+=20

        # HP + EXP bars
        bw_=box.right-rx-15
        pct=unit.hp/unit.max_hp
        hc=GREEN if pct>0.5 else YELLOW if pct>0.25 else RED
        pygame.draw.rect(self.screen,DARK_GREY,(rx,ry,bw_,12))
        pygame.draw.rect(self.screen,hc,(rx,ry,int(bw_*pct),12))
        self.screen.blit(self.font_sm.render(
            f"HP  {unit.hp} / {unit.max_hp}  ({int(pct*100)}%)",True,WHITE),(rx,ry+14)); ry+=32

        pygame.draw.rect(self.screen,DARK_GREY,(rx,ry,bw_,8))
        pygame.draw.rect(self.screen,CYAN,(rx,ry,int(bw_*unit.exp/100),8))
        self.screen.blit(self.font_sm.render(f"EXP  {unit.exp} / 100",True,LIGHT_GREY),(rx,ry+10)); ry+=26

        # ── Full FE stats grid ────────────────────────────────────────────────
        pygame.draw.line(self.screen,GOLD,(rx,ry),(box.right-15,ry),1); ry+=6
        stats=[
            ("STR",unit.str_,"Strength — physical attack power"),
            ("MAG",unit.mag, "Magic — magical attack / heal power"),
            ("SKL",unit.skl, "Skill — accuracy & critical hit rate"),
            ("SPD",unit.spd, "Speed — determines doubles & avoid"),
            ("LCK",unit.lck, "Luck — crit-avoid & stat variance"),
            ("DEF",unit.def_,"Defense — reduces physical damage"),
            ("RES",unit.res, "Resistance — reduces magical damage"),
            ("MOV",unit.move,"Movement — tiles per turn"),
        ]
        col_w=(box.right-rx-15)//2
        for i,(lb,vl,tip) in enumerate(stats):
            col_=i%2; row_=i//2
            bx_=rx+col_*col_w; by_=ry+row_*20
            self.screen.blit(self.font_sm.render(f"{lb}:",True,LIGHT_GREY),(bx_,by_))
            self.screen.blit(self.font_sm.render(f"{vl:3d}",True,WHITE),(bx_+38,by_))
            # Stat bar
            bar_max={"STR":30,"MAG":30,"SKL":30,"SPD":30,"LCK":30,
                     "DEF":30,"RES":30,"MOV":15}.get(lb,30)
            bar_pct=min(1.0,vl/bar_max)
            pygame.draw.rect(self.screen,DARK_GREY,(bx_+62,by_+4,col_w-72,8))
            bar_col={"STR":RED,"MAG":PURPLE,"SKL":CYAN,"SPD":YELLOW,
                     "LCK":GREEN,"DEF":SILVER,"RES":(140,180,255),"MOV":ORANGE}.get(lb,WHITE)
            pygame.draw.rect(self.screen,bar_col,(bx_+62,by_+4,int((col_w-72)*bar_pct),8))
        ry+=(len(stats)//2+1)*20+8

        # ── Weapon inventory ──────────────────────────────────────────────────
        pygame.draw.line(self.screen,GOLD,(rx,ry),(box.right-15,ry),1); ry+=6
        self.screen.blit(self.font_md.render("Weapons",True,GOLD),(rx,ry)); ry+=20
        for i,w in enumerate(unit.weapons):
            marker="► " if i==unit.equipped_weapon_index else "  "
            col_m=WHITE if i==unit.equipped_weapon_index else LIGHT_GREY
            wline=(f"{marker}{w.name:<18} [{w.weapon_type:<8}]  "
                   f"Mt:{w.might:2d}  Hit:{w.hit:3d}%  Crit:{w.crit:2d}%  "
                   f"Rng:{w.min_range}-{w.max_range}")
            self.screen.blit(self.font_sm.render(wline,True,col_m),(rx+4,ry)); ry+=16
            flags=[]
            if w.anti_flying:  flags.append("[Anti-Flying +5]")
            if w.anti_mounted: flags.append("[Anti-Mounted +5]")
            if w.magic_damage: flags.append("[Magic Damage]")
            if flags:
                self.screen.blit(self.font_sm.render("  "+" ".join(flags),True,AMBER),(rx+4,ry)); ry+=14

        # ── Bio ───────────────────────────────────────────────────────────────
        if ry < box.bottom-60:
            pygame.draw.line(self.screen,GOLD,(rx,ry),(box.right-15,ry),1); ry+=6
            for line in unit.bio.split("\n"):
                if ry>box.bottom-36: break
                self.screen.blit(self.font_sm.render(line,True,CREAM),(rx,ry)); ry+=17

        # Close hint
        self.screen.blit(
            self.font_sm.render("I / X / Tap anywhere to close",True,LIGHT_GREY),
            (SCREEN_WIDTH//2-120,box.bottom-18))

    # ── Recruit Dialog ────────────────────────────────────────────────────────
    def render_recruit_dialog(self, recruiter, target):
        box=pygame.Rect(110,190,SCREEN_WIDTH-220,330)
        pygame.draw.rect(self.screen,(10,22,12),box)
        pygame.draw.rect(self.screen,(50,220,100),box,2)
        cx=box.centerx
        self._blit_center(self.font_md.render("— Recruit Unit? —",True,(50,220,100)),cx,box.y+14)

        pr=pygame.Rect(box.x+18,box.y+40,90,100)
        pygame.draw.rect(self.screen,_darken(target.color,30),pr)
        pygame.draw.rect(self.screen,target.color,pr,3)
        ts=self.font_md.render(target.symbol[:2],True,WHITE)
        self.screen.blit(ts,ts.get_rect(center=pr.center))

        ix=pr.right+16; iy=box.y+44
        self.screen.blit(self.font_md.render(target.name,True,WHITE),(ix,iy)); iy+=24
        self.screen.blit(self.font_sm.render(
            f"{target.unit_class}  Lv{target.level}",True,LIGHT_GREY),(ix,iy)); iy+=18
        for line in self._wrap(target.bio.split("\n")[0] if target.bio else "",40)[:2]:
            self.screen.blit(self.font_sm.render(line,True,CREAM),(ix,iy)); iy+=16

        if target.quote:
            self.screen.blit(
                self.font_sm.render(f'"{target.quote[:60]}"',True,IVORY),(box.x+18,box.y+155))

        if target.equipped:
            w=target.equipped
            self.screen.blit(
                self.font_sm.render(f"Carries: {w.name}  [{w.weapon_type}]",True,YELLOW),
                (box.x+18,box.y+180))

        self._blit_center(
            self.font_md.render("Z / ENTER / Tap — Recruit",True,(50,220,100)),cx,box.bottom-62)
        self._blit_center(
            self.font_md.render("X / ESC — Decline",True,PINK),cx,box.bottom-34)

    # ── End screen ────────────────────────────────────────────────────────────
    def _render_end_screen(self, gs, victory=True):
        ov=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.SRCALPHA)
        ov.fill((0,0,0,185)); self.screen.blit(ov,(0,0))
        cx=SCREEN_WIDTH//2
        t1=self.font_title.render("VICTORY" if victory else "DEFEAT",
                                   True, GOLD if victory else DARK_RED)
        self._blit_center(t1,cx,190)
        narrative=(gs.current_chapter.narrative_victory if victory
                   else gs.current_chapter.narrative_defeat)
        y=280
        for line in narrative.split("\n"):
            self._blit_center(self.font_sm.render(line,True,CREAM),cx,y); y+=22
        prompt=("ENTER: Next Chapter | ESC: Title" if victory
                else "ENTER: Retry | ESC: Title")
        self._blit_center(self.font_sm.render(prompt,True,LIGHT_GREY),cx,660)

    # ── Pre-battle Preparation Screen ────────────────────────────────────────
    def _render_prep_screen(self, gs):
        '''Four-tab prep screen: Deploy | Shop | Inventory | Map Preview.'''
        W, H = SCREEN_WIDTH, SCREEN_HEIGHT
        ch = gs.current_chapter
        # Background gradient
        for i in range(H):
            t = i / H
            r = int(10 + t*25); g = int(10 + t*15); b = int(25 + t*40)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (W, i))

        # ── Header ────────────────────────────────────────────────────────────
        self._blit_center(self.font_lg.render("PRE-BATTLE PREPARATION", True, GOLD), W//2, 22)
        ch_text = f"{ch.title}  ·  {ch.subtitle}"
        self._blit_center(self.font_sm.render(ch_text, True, CREAM), W//2, 46)
        # Gold display
        gold_surf = self.font_md.render(f"Gold: {gs.gold} ryo", True, GOLD)
        self.screen.blit(gold_surf, (W - gold_surf.get_width() - 16, 8))
        # Deploy limit
        n_sel = len(gs.prep_selected_units) + len(gs.prep_mercs)
        dep_color = GREEN if n_sel <= ch.deploy_limit else RED
        dep_surf = self.font_sm.render(
            f"Deployed: {n_sel}/{ch.deploy_limit}", True, dep_color)
        self.screen.blit(dep_surf, (W - dep_surf.get_width() - 16, 34))

        # ── Tabs ──────────────────────────────────────────────────────────────
        tab_y = 62
        tab_h = 32
        tab_w = W // 4
        tab = getattr(gs, 'prep_tab', 0)
        for i, name in enumerate(PREP_TAB_NAMES):
            x = i * tab_w
            sel = (i == tab)
            bg  = (40, 50, 80) if sel else (15, 18, 35)
            brd = GOLD if sel else (80, 80, 80)
            self._draw_rounded_box(x+2, tab_y, tab_w-4, tab_h, bg, brd, r=6)
            col = WHITE if sel else LIGHT_GREY
            self._blit_center(self.font_sm.render(name, True, col),
                               x + tab_w//2, tab_y + tab_h//2)
        pygame.draw.line(self.screen, GOLD, (0, tab_y+tab_h), (W, tab_y+tab_h), 1)

        content_y = tab_y + tab_h + 8
        cur = getattr(gs, 'prep_cursor', 0)

        if tab == PREP_TAB_DEPLOY:
            self._render_prep_deploy(gs, content_y, cur)
        elif tab == PREP_TAB_SHOP:
            self._render_prep_shop(gs, content_y, cur)
        elif tab == PREP_TAB_INVENTORY:
            self._render_prep_inventory(gs, content_y, cur)
        elif tab == PREP_TAB_MAP:
            self._render_prep_map(gs, content_y)

        # ── Bottom bar ────────────────────────────────────────────────────────
        bar_y = H - 36
        pygame.draw.line(self.screen, GOLD, (0, bar_y), (W, bar_y), 1)
        hints = "◄►: Tabs   ↑↓: Select   Z/Enter: Toggle/Buy   SPACE/B: BATTLE!"
        self._blit_center(self.font_sm.render(hints, True, LIGHT_GREY), W//2, bar_y+18)

    def _render_prep_deploy(self, gs, y0, cur):
        '''Deploy tab: toggle named units in/out of the battle roster.'''
        ch = gs.current_chapter
        avail = gs.prep_available_units
        selected_ids = {u.unit_id for u in gs.prep_selected_units}
        x0 = 16; col_w = (SCREEN_WIDTH - 32) // 2
        row_h = 44
        for i, u in enumerate(avail):
            row_y = y0 + i * row_h
            if row_y + row_h > SCREEN_HEIGHT - 40:
                break
            sel = u.unit_id in selected_ids
            is_cur = (i == cur)
            bg  = (30, 55, 30) if sel else (20, 20, 40)
            brd = GOLD if is_cur else ((60, 160, 60) if sel else (50, 50, 80))
            self._draw_rounded_box(x0, row_y, SCREEN_WIDTH - 32, row_h - 4, bg, brd, r=6)
            # Colour circle
            pygame.draw.circle(self.screen, u.color,
                               (x0 + 20, row_y + row_h//2 - 2), 12)
            pygame.draw.circle(self.screen, WHITE,
                               (x0 + 20, row_y + row_h//2 - 2), 12, 1)
            sym = self.font_sm.render(u.symbol[:2], True, WHITE)
            self.screen.blit(sym, (x0+14, row_y+11))
            # Name & class
            name_col = GOLD if is_cur else WHITE
            self.screen.blit(self.font_md.render(u.name, True, name_col),
                             (x0+40, row_y+4))
            cls_txt = f"{u.unit_class}  Lv{u.level}  HP:{u.max_hp}"
            self.screen.blit(self.font_sm.render(cls_txt, True, LIGHT_GREY),
                             (x0+40, row_y+24))
            # Status badge
            status = "[DEPLOYED]" if sel else "[ bench ]"
            s_col  = GREEN if sel else (120, 120, 120)
            s_surf = self.font_sm.render(status, True, s_col)
            self.screen.blit(s_surf, (SCREEN_WIDTH - 32 - s_surf.get_width(), row_y+14))

        # Deploy limit hint
        n_sel = len(gs.prep_selected_units)
        hint = (f"Select up to {ch.deploy_limit} units — "
                f"{n_sel}/{ch.deploy_limit} named units chosen. "
                f"Hire mercs in [Shop] to fill remaining slots.")
        hint_surf = self.font_sm.render(hint, True, LIGHT_GREY)
        self.screen.blit(hint_surf, (x0, SCREEN_HEIGHT - 64))

    def _render_prep_shop(self, gs, y0, cur):
        '''Shop tab: hire mercenaries with gold.'''
        from game.constants import SHOP_PRICES
        items = list(SHOP_PRICES.items())
        x0 = 16; row_h = 48
        # Merc limit info
        n_mercs = len(gs.prep_mercs)
        lim_surf = self.font_sm.render(
            f"Hired mercs this chapter: {n_mercs}/{gs.prep_max_mercs}",
            True, GOLD)
        self.screen.blit(lim_surf, (x0, y0))
        y0 += 22

        # Class name map for display
        _display = {
            "merc_ashigaru": ("Ashigaru",   CLASS_ASHIGARU,   "Foot soldier. Cheap, sturdy."),
            "merc_spearman": ("Spearman",   CLASS_SPEARMAN,   "Anti-cavalry specialist."),
            "merc_archer":   ("Archer",     CLASS_ARCHER,     "Ranged attacker. 2-range."),
            "merc_samurai":  ("Samurai",    CLASS_SAMURAI,    "Balanced melee fighter."),
            "merc_cavalry":  ("Cavalry",    CLASS_CAVALRY,    "Fast mounted unit."),
            "merc_ninja":    ("Ninja",      CLASS_NINJA,      "Evasive assassin."),
            "merc_monk":     ("Monk",       CLASS_MONK,       "Healer. Uses staff."),
            "merc_gunner":   ("Gunner",     CLASS_GUNNER,     "Long-range rifleman."),
        }
        for i, (merc_id, cost) in enumerate(items):
            row_y = y0 + i * row_h
            if row_y + row_h > SCREEN_HEIGHT - 48:
                break
            is_cur  = (i == cur)
            can_buy = gs.gold >= cost and n_mercs < gs.prep_max_mercs
            bg  = (30, 30, 60) if is_cur else (15, 15, 35)
            brd = GOLD if is_cur else (50, 50, 80)
            self._draw_rounded_box(x0, row_y, SCREEN_WIDTH//2 - 24, row_h - 4, bg, brd, r=6)
            dname, cls, desc = _display.get(merc_id, (merc_id, CLASS_ASHIGARU, ""))
            cd = CLASS_DATA.get(cls, {})
            col = cd.get("color", GREY)
            pygame.draw.circle(self.screen, col, (x0+20, row_y+row_h//2-2), 12)
            pygame.draw.circle(self.screen, WHITE, (x0+20, row_y+row_h//2-2), 12, 1)
            sym = self.font_sm.render(cd.get("symbol","?")[:2], True, WHITE)
            self.screen.blit(sym, (x0+14, row_y+11))
            name_col = GOLD if is_cur else (WHITE if can_buy else GREY)
            self.screen.blit(self.font_md.render(dname, True, name_col), (x0+40, row_y+4))
            self.screen.blit(self.font_sm.render(desc, True, LIGHT_GREY), (x0+40, row_y+24))
            cost_col = GREEN if can_buy else RED
            cost_surf = self.font_md.render(f"{cost} ryo", True, cost_col)
            self.screen.blit(cost_surf, (SCREEN_WIDTH//2 - 30 - cost_surf.get_width(), row_y+14))

        # Show currently hired mercs on right side
        rx = SCREEN_WIDTH//2 + 8
        self.screen.blit(self.font_md.render("Hired:", True, GOLD), (rx, y0))
        if not gs.prep_mercs:
            self.screen.blit(self.font_sm.render("(none)", True, GREY), (rx, y0+24))
        else:
            for i, m in enumerate(gs.prep_mercs):
                my = y0 + 24 + i * 22
                self.screen.blit(self.font_sm.render(
                    f"{m.name}  Lv{m.level}", True, CREAM), (rx, my))

    def _render_prep_inventory(self, gs, y0, cur):
        '''Inventory tab: view equipped weapons of all deployed units.'''
        units = gs.prep_selected_units + gs.prep_mercs
        x0 = 16; row_h = 56
        if not units:
            self._blit_center(self.font_md.render(
                "No units deployed yet. Go to [Deploy] tab.", True, LIGHT_GREY),
                SCREEN_WIDTH//2, y0+80)
            return
        for i, u in enumerate(units):
            row_y = y0 + i * row_h
            if row_y + row_h > SCREEN_HEIGHT - 48:
                break
            is_cur = (i == cur)
            bg  = (25, 30, 55) if is_cur else (15, 15, 35)
            brd = GOLD if is_cur else (50, 50, 80)
            self._draw_rounded_box(x0, row_y, SCREEN_WIDTH - 32, row_h - 4, bg, brd, r=6)
            pygame.draw.circle(self.screen, u.color, (x0+18, row_y+28), 10)
            self.screen.blit(self.font_md.render(u.name, True, WHITE if is_cur else CREAM),
                             (x0+36, row_y+4))
            self.screen.blit(self.font_sm.render(
                f"{u.unit_class}  Lv{u.level}  HP:{u.hp}/{u.max_hp}",
                True, LIGHT_GREY), (x0+36, row_y+24))
            # Weapons list
            wx = SCREEN_WIDTH//2
            for j, w in enumerate(u.weapons):
                equipped = (j == u.equipped_weapon_index)
                wc = YELLOW if equipped else LIGHT_GREY
                mark = "►" if equipped else " "
                wtext = f"{mark}{w.name}  Mt:{w.might} Hit:{w.hit}% Uses:{w.current_uses}"
                self.screen.blit(self.font_sm.render(wtext, True, wc),
                                 (wx, row_y + 4 + j*18))
        self.screen.blit(self.font_sm.render(
            "Z/Enter: cycle equipped weapon for selected unit", True, LIGHT_GREY),
            (x0, SCREEN_HEIGHT - 60))

    def _render_prep_map(self, gs, y0):
        '''Map Preview tab: shows a zoomed-out view of the chapter map.'''
        gmap = gs.game_map
        W = SCREEN_WIDTH; H = SCREEN_HEIGHT
        avail_h = H - y0 - 40
        avail_w = W

        # Compute tile size to fit whole map
        ts = min(avail_w // max(1, gmap.width), avail_h // max(1, gmap.height), 24)
        ts = max(ts, 4)
        map_px_w = ts * gmap.width
        map_px_h = ts * gmap.height
        ox = (avail_w - map_px_w) // 2
        oy = y0 + (avail_h - map_px_h) // 2

        # Draw tiles
        for ty in range(gmap.height):
            for tx in range(gmap.width):
                t = gmap.get_terrain(tx, ty)
                col = TERRAIN_DATA[t]["color"]
                sx = ox + tx * ts; sy = oy + ty * ts
                pygame.draw.rect(self.screen, col, (sx, sy, ts-1, ts-1))

        # Draw units
        for u in gs.enemy_units + gs.ally_units:
            if not u.alive: continue
            fc = {FACTION_ENEMY: (220,60,60), FACTION_ALLY: (60,220,80)}.get(u.faction, GREY)
            pygame.draw.rect(self.screen, fc, (ox+u.x*ts, oy+u.y*ts, ts-1, ts-1))

        # Draw deployed player units
        for u in gs.prep_selected_units + gs.prep_mercs:
            px = ox + u.x * ts; py_u = oy + u.y * ts
            pygame.draw.rect(self.screen, (80, 160, 255), (px, py_u, ts-1, ts-1))
            if u.is_lord:
                pygame.draw.rect(self.screen, GOLD, (px, py_u, ts-1, ts-1), 1)

        # Seize points
        for (sx, sy) in gmap.seize_points:
            pygame.draw.rect(self.screen, GOLD,
                             (ox+sx*ts, oy+sy*ts, ts-1, ts-1))

        self._blit_center(self.font_sm.render(
            "Map Preview — Blue=Player  Red=Enemy  Green=Ally  Gold=Seize",
            True, LIGHT_GREY), W//2, H-28)

    # ── Help Overlay ──────────────────────────────────────────────────────────
    def _render_help_overlay(self):
        '''Full-screen help reference overlay. Press ? or F1 to toggle.'''
        W, H = SCREEN_WIDTH, SCREEN_HEIGHT
        ov = pygame.Surface((W, H), pygame.SRCALPHA)
        ov.fill((0, 0, 20, 230))
        self.screen.blit(ov, (0, 0))

        cx = W // 2
        self._blit_center(self.font_lg.render("GAME REFERENCE", True, GOLD), cx, 22)
        pygame.draw.line(self.screen, GOLD, (40, 46), (W-40, 46), 1)

        # Two-column layout
        col1_x = 50; col2_x = W//2 + 20; y = 56
        lh = 17   # line height

        def section(title, lines, x, yref):
            self.screen.blit(self.font_md.render(title, True, YELLOW), (x, yref))
            yref += 22
            for line in lines:
                col = LIGHT_GREY if not line.startswith("  ►") else CREAM
                self.screen.blit(self.font_sm.render(line, True, col), (x, yref))
                yref += lh
            return yref + 6

        # ── Left column ───────────────────────────────────────────────────────
        y = section("Controls", [
            "Arrows/WASD  — Move cursor",
            "Z / Enter    — Confirm / Select unit",
            "X / Esc      — Cancel / Deselect",
            "A            — Attack (with selected unit)",
            "H            — Heal (with selected unit)",
            "W            — Wait (end unit's turn)",
            "T            — Talk / Recruit adjacent unit",
            "E            — Seize (lord on seize tile)",
            "I            — Open Stat Sheet",
            "Space        — End Player Turn",
            "?  / F1      — Toggle this Help screen",
        ], col1_x, y)

        y = section("Combat", [
            "Attack = STR + Weapon Might",
            "Hit% = SKL×2 + Weapon Hit + LCK/2",
            "Avoid = SPD×2 + LCK/2 − weight",
            "Crit = SKL/2 + Weapon Crit",
            "Counter-attack if enemy in range",
            "Double-attack if SPD ≥ enemy SPD+4",
            "Weapon triangle gives +1 Dmg / +15 Hit:",
            "  Katana > Chain > Spear > Katana",
            "  Bow / Gun > Flying units",
        ], col1_x, y)

        y = section("Terrain", [
            "Plain: no bonus  Forest: Def+1 Avo+20",
            "Fort: Def+2 Avo+20  Castle/Gate: Def+3-4",
            "Mountain: Def+2 Avo+30  (slow movement)",
            "River/Sea: impassable unless water-walk",
            "Peak/Cliff: impassable",
        ], col1_x, y)

        # ── Right column ──────────────────────────────────────────────────────
        ry = 56
        ry = section("Promotion (UNIQUE to this game!)", [
            "Units promote at Level 10+ — but NOT forced.",
            "Open the Stat Sheet (I) of your unit.",
            "If eligible, a [PROMOTE] button appears.",
            "Choose a promotion class from the options.",
            "Stats increase + new class abilities unlock.",
            "  ► This is NOT like Fire Emblem!",
            "  ► In FE you use an item. Here: Stat Sheet.",
            "Promoted units cannot promote again.",
            "Enemies start promoting in Chapter 13+.",
        ], col2_x, ry)

        ry = section("Pre-Battle Prep Screen", [
            "Appears before every chapter.",
            "Deploy: Pick which named units to send.",
            "Shop: Hire mercenaries with gold (ryo).",
            "  ► Mercs are weaker than named officers.",
            "  ► Gold earned: 150 ryo per chapter clear.",
            "Inventory: View / cycle unit weapons.",
            "Map Preview: Scout the battlefield.",
            "SPACE / B: Confirm and start the battle.",
        ], col2_x, ry)

        ry = section("Objectives & Victory", [
            "Rout Enemy: Defeat ALL enemies.",
            "Defeat Boss: Kill all boss (LORD♦) enemies.",
            "Seize: Move your lord to the seize tile.",
            "Defend: Survive the required turn count.",
            "Defeat = all your lords are dead.",
        ], col2_x, ry)

        ry = section("Recruit / Allies", [
            "Units marked [!] on map can be recruited.",
            "Use Talk (T) with the right unit adjacent.",
            "Recruited units join permanently.",
            "Ally units act automatically each turn.",
        ], col2_x, ry)

        # Close hint at bottom
        pygame.draw.line(self.screen, GOLD, (40, H-34), (W-40, H-34), 1)
        self._blit_center(
            self.font_sm.render("Press ? or F1 to close this screen", True, LIGHT_GREY),
            cx, H - 18)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _blit_center(self, surf, cx, cy):
        self.screen.blit(surf, surf.get_rect(center=(cx,cy)))

    def _wrap(self, text, max_chars):
        words = text.split(); line = ""; lines = []
        for w in words:
            if len(line)+len(w)+1 <= max_chars:
                line += ("" if not line else " ") + w
            else:
                if line: lines.append(line)
                line = w
        if line: lines.append(line)
        return lines

    # ── Prologue ───────────────────────────────────────────────────────────────
    def _render_prologue(self, gs):
        '''Full-screen historical intro slides before Chapter 1.'''
        from game.prologue import PROLOGUE_SLIDES, PROLOGUE_PORTRAIT_COLORS
        idx   = getattr(gs, 'prologue_idx', 0)
        total = len(PROLOGUE_SLIDES)
        if idx >= total:
            return

        speaker_key, display_name, text = PROLOGUE_SLIDES[idx]
        portrait_color = PROLOGUE_PORTRAIT_COLORS.get(speaker_key, (40, 40, 70))

        W, H = SCREEN_WIDTH, SCREEN_HEIGHT

        # ── Background — deep midnight ink wash ──────────────────────────────
        for i in range(H):
            t = i / H
            r = int(5  + t * 15)
            g = int(5  + t * 12)
            b = int(15 + t * 35)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (W, i))

        # ── "PROLOGUE" header ─────────────────────────────────────────────────
        hdr = self.font_sm.render("PROLOGUE — The Age of the Warring States", True, (140, 120, 60))
        self.screen.blit(hdr, (20, 14))
        pygame.draw.line(self.screen, (80, 70, 30), (20, 32), (W - 20, 32), 1)

        # ── Portrait box (left side) ──────────────────────────────────────────
        pw, ph = 160, 200
        px, py = 40, H // 2 - ph // 2 - 30

        shadow = pygame.Surface((pw + 6, ph + 6), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 120))
        self.screen.blit(shadow, (px - 2, py + 4))

        pygame.draw.rect(self.screen, portrait_color, (px, py, pw, ph))
        pygame.draw.rect(self.screen, GOLD, (px, py, pw, ph), 3)

        initial = display_name[0].upper() if display_name else "?"
        ic = self.font_title.render(initial, True, (255, 255, 255, 180))
        self.screen.blit(ic, (px + pw // 2 - ic.get_width() // 2,
                               py + ph // 2 - ic.get_height() // 2))

        # ── Dialogue box (bottom) ─────────────────────────────────────────────
        box_h = 200
        box_y = H - box_h - 10
        box_x = 30
        box_w = W - 60

        dlg_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        dlg_surf.fill((8, 10, 28, 225))
        self.screen.blit(dlg_surf, (box_x, box_y))
        pygame.draw.rect(self.screen, GOLD, (box_x, box_y, box_w, box_h), 2)

        # Speaker name bar
        name_bar_h = 30
        name_bar_surf = pygame.Surface((220, name_bar_h), pygame.SRCALPHA)
        name_bar_surf.fill((*portrait_color, 230))
        self.screen.blit(name_bar_surf, (box_x + 10, box_y - name_bar_h + 2))
        pygame.draw.rect(self.screen, GOLD,
                         (box_x + 10, box_y - name_bar_h + 2, 220, name_bar_h), 1)
        name_surf = self.font_md.render(display_name, True, WHITE)
        self.screen.blit(name_surf, (box_x + 18, box_y - name_bar_h + 6))

        # Dialogue text
        text_x = box_x + 20
        text_y = box_y + 18
        max_chars = (box_w - 40) // 8
        for wline in self._wrap(text, max_chars)[:6]:
            self.screen.blit(self.font_md.render(wline, True, CREAM), (text_x, text_y))
            text_y += 28

        # ── Progress dots ─────────────────────────────────────────────────────
        dot_y = box_y + box_h - 22
        dot_start_x = box_x + 20
        dot_spacing = min(14, (box_w - 60) // max(total, 1))
        for i in range(total):
            col = GOLD if i == idx else (80, 70, 40)
            pygame.draw.circle(self.screen, col,
                               (dot_start_x + i * dot_spacing, dot_y), 4)

        hint = "Z / Enter / Tap  ▶  to continue"
        hint_surf = self.font_sm.render(hint, True, (160, 150, 100))
        self.screen.blit(hint_surf, (W - hint_surf.get_width() - 30, dot_y - 6))

        # ── Slide counter ─────────────────────────────────────────────────────
        ctr = self.font_sm.render(f"{idx+1} / {total}", True, (120, 110, 70))
        self.screen.blit(ctr, (W - ctr.get_width() - 20, 14))

    def _draw_rounded_box(self, x, y, w, h, fill, border, r=6):
        pygame.draw.rect(self.screen, fill,   pygame.Rect(x,y,w,h), border_radius=r)
        pygame.draw.rect(self.screen, border, pygame.Rect(x,y,w,h), 2, border_radius=r)
