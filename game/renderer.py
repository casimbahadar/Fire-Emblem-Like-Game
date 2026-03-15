"""
Renderer for Sengoku Tactics — includes stat sheet, recruit dialog,
reinforcement notifications, and Samurai Warriors-style character cards.
"""
import pygame
from game.constants import *


# ── Color helpers ─────────────────────────────────────────────────────────────
def _darken(color, amount):
    return tuple(max(0, c - amount) for c in color[:3])

def _lighten(color, amount):
    return tuple(min(255, c + amount) for c in color[:3])

def _blend(c1, c2, t):
    return tuple(int(c1[i]*(1-t) + c2[i]*t) for i in range(3))


class Renderer:
    def __init__(self, screen, font_small, font_med, font_large, font_title):
        self.screen     = screen
        self.font_sm    = font_small
        self.font_md    = font_med
        self.font_lg    = font_large
        self.font_title = font_title

        self.cam_x = 0
        self.cam_y = 0

        self.map_rect = pygame.Rect(0, 0, SCREEN_WIDTH - UI_PANEL_WIDTH, SCREEN_HEIGHT)
        self.ui_rect  = pygame.Rect(SCREEN_WIDTH - UI_PANEL_WIDTH, 0,
                                    UI_PANEL_WIDTH, SCREEN_HEIGHT)
        self._build_terrain_surfaces()

    def _build_terrain_surfaces(self):
        self._tile_surfs = {}
        for terrain, data in TERRAIN_DATA.items():
            s = pygame.Surface((TILE_SIZE, TILE_SIZE))
            color = data["color"]
            s.fill(color)
            pygame.draw.rect(s, _darken(color, 20), s.get_rect(), 1)
            self._add_terrain_texture(s, terrain, color)
            self._tile_surfs[terrain] = s

    def _add_terrain_texture(self, surf, terrain, bc):
        if terrain == TERRAIN_FOREST:
            for pos in [(12,10),(28,8),(20,22),(10,32),(34,28)]:
                pygame.draw.circle(surf, _darken(bc,30), pos, 5)
        elif terrain in (TERRAIN_MOUNTAIN, TERRAIN_PEAK):
            pygame.draw.polygon(surf, _darken(bc,40), [(8,40),(16,18),(24,40)])
            pygame.draw.polygon(surf, _darken(bc,30), [(22,40),(32,16),(44,40)])
        elif terrain in (TERRAIN_RIVER, TERRAIN_SEA):
            for i in range(0, TILE_SIZE, 8):
                pygame.draw.arc(surf, _lighten(bc,30),
                                pygame.Rect(i-4,16,12,10), 0, 3.14, 2)
        elif terrain == TERRAIN_CASTLE:
            pygame.draw.rect(surf, _darken(bc,40),
                             pygame.Rect(4,4,TILE_SIZE-8,TILE_SIZE-8), 2)
            for bx in range(6, TILE_SIZE-6, 8):
                pygame.draw.rect(surf, _darken(bc,40), pygame.Rect(bx,2,5,6))
        elif terrain == TERRAIN_GATE:
            pygame.draw.rect(surf, _darken(bc,50),
                             pygame.Rect(0,0,TILE_SIZE,TILE_SIZE), 3)
            pygame.draw.rect(surf, _darken(bc,30),
                             pygame.Rect(8,8,TILE_SIZE-16,TILE_SIZE-16), 2)
        elif terrain == TERRAIN_ROAD:
            pygame.draw.rect(surf, _darken(bc,15),
                             pygame.Rect(0,TILE_SIZE//2-4,TILE_SIZE,8))
        elif terrain == TERRAIN_FORT:
            pygame.draw.rect(surf, _darken(bc,35),
                             pygame.Rect(8,8,TILE_SIZE-16,TILE_SIZE-16), 3)
        elif terrain == TERRAIN_VILLAGE:
            pygame.draw.polygon(surf, _darken(bc,40),
                                [(TILE_SIZE//2,8),(10,28),(TILE_SIZE-10,28)])
            pygame.draw.rect(surf, _darken(bc,30), pygame.Rect(14,28,20,16))
        elif terrain == TERRAIN_BRIDGE:
            pygame.draw.rect(surf, _darken(bc,20),
                             pygame.Rect(0,18,TILE_SIZE,12))
            for bx in range(0, TILE_SIZE, 10):
                pygame.draw.rect(surf, _darken(bc,35), pygame.Rect(bx,18,4,12))
        elif terrain == TERRAIN_RUINS:
            for rx in range(4, TILE_SIZE-4, 12):
                h = 8 + (rx % 16)
                pygame.draw.rect(surf, _darken(bc,30),
                                 pygame.Rect(rx, TILE_SIZE-h, 8, h))
        elif terrain == TERRAIN_THICKET:
            for pos in [(8,8),(24,6),(16,20),(6,30),(32,26),(20,36)]:
                pygame.draw.circle(surf, _darken(bc,25), pos, 4)
                pygame.draw.circle(surf, _darken(bc,10), pos, 3)

    # ── Camera ────────────────────────────────────────────────────────────────

    def center_camera(self, gmap, cursor_x, cursor_y):
        view_w = self.map_rect.width  // TILE_SIZE
        view_h = self.map_rect.height // TILE_SIZE
        self.cam_x = max(0, min(cursor_x - view_w//2, gmap.width  - view_w))
        self.cam_y = max(0, min(cursor_y - view_h//2, gmap.height - view_h))

    def tile_to_screen(self, tx, ty):
        return (tx - self.cam_x)*TILE_SIZE, (ty - self.cam_y)*TILE_SIZE

    def screen_to_tile(self, sx, sy):
        return sx//TILE_SIZE + self.cam_x, sy//TILE_SIZE + self.cam_y

    # ── Full Frame ────────────────────────────────────────────────────────────

    def render(self, gs):
        self.screen.fill(BLACK)
        s = gs.state

        if s == STATE_TITLE:
            self._render_title(gs)
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
        elif s in (STATE_VICTORY, STATE_GAME_OVER):
            self._render_map(gs)
            self._render_units(gs)
            self._render_end_screen(gs, victory=(s == STATE_VICTORY))

    # ── Title ─────────────────────────────────────────────────────────────────

    def _render_title(self, gs):
        for i in range(SCREEN_HEIGHT):
            t = i / SCREEN_HEIGHT
            c = (int(20+t*60), int(10+t*20), int(5+t*10))
            pygame.draw.line(self.screen, c, (0, i), (SCREEN_WIDTH, i))

        cx = SCREEN_WIDTH // 2
        t1 = self.font_title.render("SENGOKU TACTICS", True, GOLD)
        t2 = self.font_lg.render("Age of the Warring States", True, CREAM)
        t3 = self.font_sm.render("20 Chapters  ·  60+ Historical Officers  ·  Flying & Mounted Units", True, LIGHT_GREY)
        sub= self.font_md.render("Press ENTER to Begin  |  ESC to Quit", True, LIGHT_GREY)

        self.screen.blit(t1, t1.get_rect(center=(cx, 180)))
        self.screen.blit(t2, t2.get_rect(center=(cx, 260)))
        self.screen.blit(t3, t3.get_rect(center=(cx, 310)))
        self.screen.blit(sub, sub.get_rect(center=(cx, 390)))

        pygame.draw.line(self.screen, GOLD, (cx-320,330),(cx+320,330), 2)

        controls = [
            "Arrows/WASD: Move cursor",
            "Z/Enter: Select/Confirm     X/Esc: Cancel",
            "A: Attack   H: Heal   W: Wait",
            "T: Talk/Recruit adjacent enemy   I: Unit Stat Sheet",
            "Space: End turn   E: Seize castle tile",
        ]
        y = 440
        for line in controls:
            s = self.font_sm.render(line, True, LIGHT_GREY)
            self.screen.blit(s, s.get_rect(center=(cx, y)))
            y += 24

    # ── Chapter Intro ─────────────────────────────────────────────────────────

    def _render_chapter_intro(self, gs):
        self.screen.fill((10, 10, 20))
        ch = gs.current_chapter
        cx = SCREEN_WIDTH // 2

        t1 = self.font_lg.render(ch.title, True, GOLD)
        t2 = self.font_md.render(ch.subtitle, True, CREAM)
        self.screen.blit(t1, t1.get_rect(center=(cx, 70)))
        self.screen.blit(t2, t2.get_rect(center=(cx, 110)))

        pygame.draw.rect(self.screen, (20,20,40),
                         pygame.Rect(60,145,SCREEN_WIDTH-120,380))
        pygame.draw.rect(self.screen, GOLD,
                         pygame.Rect(60,145,SCREEN_WIDTH-120,380), 2)
        y = 165
        for line in ch.narrative_intro.split("\n"):
            s = self.font_sm.render(line, True, CREAM)
            self.screen.blit(s, (80, y))
            y += 26

        # Objective box
        pygame.draw.rect(self.screen, (30,20,10),
                         pygame.Rect(60,540,SCREEN_WIDTH-120,60))
        pygame.draw.rect(self.screen, GOLD,
                         pygame.Rect(60,540,SCREEN_WIDTH-120,60), 2)
        obj = self.font_sm.render("Objective: " + ch.objective_detail, True, YELLOW)
        self.screen.blit(obj, (80, 558))

        # Reinforce warning
        if ch.reinforcements:
            rw = ch.reinforcements[0]
            warn = self.font_sm.render(
                f"⚠ Reinforcements arrive on Turn {rw.turn}!", True, RED)
            self.screen.blit(warn, warn.get_rect(center=(cx, 615)))

        prompt = self.font_sm.render("Press ENTER to begin", True, LIGHT_GREY)
        self.screen.blit(prompt, prompt.get_rect(center=(cx, 650)))

    # ── Map ───────────────────────────────────────────────────────────────────

    def _render_map(self, gs):
        gmap = gs.game_map
        pygame.draw.rect(self.screen, (30,30,30), self.map_rect)
        view_w = self.map_rect.width  // TILE_SIZE + 2
        view_h = self.map_rect.height // TILE_SIZE + 2

        for ty in range(self.cam_y, min(self.cam_y+view_h, gmap.height)):
            for tx in range(self.cam_x, min(self.cam_x+view_w, gmap.width)):
                terrain = gmap.get_terrain(tx, ty)
                surf    = self._tile_surfs.get(terrain, self._tile_surfs[TERRAIN_PLAIN])
                sx, sy  = self.tile_to_screen(tx, ty)
                self.screen.blit(surf, (sx, sy))

        pygame.draw.rect(self.screen, DARK_GREY, self.map_rect, 2)

    # ── Overlays ──────────────────────────────────────────────────────────────

    def _render_overlays(self, gs):
        move_s   = pygame.Surface((TILE_SIZE,TILE_SIZE), pygame.SRCALPHA)
        attack_s = pygame.Surface((TILE_SIZE,TILE_SIZE), pygame.SRCALPHA)
        seize_s  = pygame.Surface((TILE_SIZE,TILE_SIZE), pygame.SRCALPHA)
        talk_s   = pygame.Surface((TILE_SIZE,TILE_SIZE), pygame.SRCALPHA)

        move_s.fill((60,100,220,100))
        attack_s.fill((220,60,60,80))
        seize_s.fill((220,180,30,100))
        talk_s.fill((50,220,100,100))

        # Seize points
        for (sx,sy) in gs.game_map.seize_points:
            px, py = self.tile_to_screen(sx, sy)
            self.screen.blit(seize_s, (px, py))
            pygame.draw.rect(self.screen, GOLD, (px,py,TILE_SIZE,TILE_SIZE), 2)

        if gs.selected_unit:
            for (tx,ty) in getattr(gs,'move_range_land',set()):
                px, py = self.tile_to_screen(tx, ty)
                if self.map_rect.collidepoint(px+TILE_SIZE//2, py+TILE_SIZE//2):
                    self.screen.blit(move_s, (px, py))

            for (tx,ty) in gs.attack_range:
                px, py = self.tile_to_screen(tx, ty)
                if self.map_rect.collidepoint(px+TILE_SIZE//2, py+TILE_SIZE//2):
                    self.screen.blit(attack_s, (px, py))

            # Recruitable adjacent
            for t in gs.get_recruitable_adjacent(gs.selected_unit):
                px, py = self.tile_to_screen(t.x, t.y)
                self.screen.blit(talk_s, (px, py))
                pygame.draw.rect(self.screen, (50,220,100), (px,py,TILE_SIZE,TILE_SIZE), 2)

    # ── Units ─────────────────────────────────────────────────────────────────

    def _render_units(self, gs):
        for unit in gs.all_units():
            if not unit.alive:
                continue
            sx, sy = self.tile_to_screen(unit.x, unit.y)
            if not self.map_rect.collidepoint(sx+TILE_SIZE//2, sy+TILE_SIZE//2):
                continue
            self._draw_unit(unit, sx, sy, gs)

    def _draw_unit(self, unit, sx, sy, gs):
        cx_ = sx + TILE_SIZE//2
        cy_ = sy + TILE_SIZE//2
        r   = TILE_SIZE//2 - 3
        color = unit.color
        if unit.has_acted and unit.faction == FACTION_PLAYER:
            color = _darken(color, 80)

        # Flying units get a slight shadow offset
        if unit.is_flying:
            pygame.draw.circle(self.screen, _darken(color,60), (cx_+3,cy_+4), r)
        else:
            pygame.draw.circle(self.screen, _darken(color,50), (cx_+2,cy_+2), r)

        pygame.draw.circle(self.screen, color, (cx_,cy_), r)

        border = {FACTION_PLAYER:(80,180,255), FACTION_ENEMY:(255,80,80),
                  FACTION_ALLY:(80,255,120)}.get(unit.faction, WHITE)
        pygame.draw.circle(self.screen, border, (cx_,cy_), r, 2)

        # Flying indicator ring
        if unit.is_flying:
            pygame.draw.circle(self.screen, (200,200,255), (cx_,cy_), r+2, 1)

        # Class symbol
        sym = unit.symbol[:2]
        sym_s = self.font_sm.render(sym, True, WHITE)
        self.screen.blit(sym_s, sym_s.get_rect(center=(cx_, cy_-2)))

        # HP bar
        bw = TILE_SIZE-8
        bh = 4
        bx = sx+4
        by = sy+TILE_SIZE-7
        pct = unit.hp / unit.max_hp
        hc  = GREEN if pct>0.5 else YELLOW if pct>0.25 else RED
        pygame.draw.rect(self.screen, DARK_GREY, (bx,by,bw,bh))
        pygame.draw.rect(self.screen, hc,        (bx,by,int(bw*pct),bh))

        # Selected highlight
        if gs.selected_unit == unit:
            pygame.draw.rect(self.screen, WHITE, (sx+1,sy+1,TILE_SIZE-2,TILE_SIZE-2), 2)

        # Lord marker
        if unit.is_lord:
            lc = self.font_sm.render("♦", True, GOLD)
            self.screen.blit(lc, (sx+TILE_SIZE-14, sy+1))

        # Recruitable marker (green !)
        if unit.can_recruit and not unit.recruited:
            rc = self.font_sm.render("!", True, (50,220,100))
            self.screen.blit(rc, (sx+TILE_SIZE-12, sy+TILE_SIZE-16))

    # ── Cursor ────────────────────────────────────────────────────────────────

    def _render_cursor(self, gs):
        sx, sy = self.tile_to_screen(gs.cursor_x, gs.cursor_y)
        if not self.map_rect.collidepoint(sx+TILE_SIZE//2, sy+TILE_SIZE//2):
            return
        ticks = pygame.time.get_ticks()
        alpha = int(160 + 80*abs((ticks%1000)/500-1))
        cs = pygame.Surface((TILE_SIZE,TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(cs, (255,255,255,min(255,alpha)),
                         pygame.Rect(0,0,TILE_SIZE,TILE_SIZE), 3)
        self.screen.blit(cs, (sx, sy))

    # ── UI Panel ──────────────────────────────────────────────────────────────

    def _render_ui_panel(self, gs):
        panel = self.ui_rect
        pygame.draw.rect(self.screen, (20,20,35), panel)
        pygame.draw.rect(self.screen, GOLD, panel, 2)

        x0 = panel.x + 10
        y  = panel.y + 10

        phase_str = {FACTION_PLAYER:"Player Phase",
                     FACTION_ENEMY:"Enemy Phase",
                     FACTION_ALLY:"Ally Phase"}.get(gs.phase,"")
        phase_col = {FACTION_PLAYER:LIGHT_BLUE,
                     FACTION_ENEMY:PINK,
                     FACTION_ALLY:(100,255,150)}.get(gs.phase, WHITE)

        self.screen.blit(self.font_md.render(f"Turn {gs.turn}", True, GOLD), (x0,y)); y+=30
        self.screen.blit(self.font_sm.render(phase_str, True, phase_col), (x0,y)); y+=22
        self.screen.blit(self.font_sm.render(gs.game_map.name, True, LIGHT_GREY),(x0,y)); y+=20

        pygame.draw.line(self.screen, GOLD, (x0,y), (panel.right-10,y), 1); y+=8

        hovered = gs.unit_at(gs.cursor_x, gs.cursor_y)
        display  = gs.selected_unit or hovered
        if display:
            y = self._render_unit_card(display, x0, y, panel.right-10)
        else:
            terrain = gs.game_map.get_terrain(gs.cursor_x, gs.cursor_y)
            y = self._render_terrain_info(terrain, TERRAIN_DATA[terrain], x0, y)

        # Chapter objective
        ch = gs.current_chapter
        if ch:
            pygame.draw.line(self.screen, GOLD,
                             (x0, panel.bottom-270),(panel.right-10,panel.bottom-270), 1)
            oy = panel.bottom - 262
            self.screen.blit(self.font_sm.render("Objective:", True, YELLOW), (x0,oy)); oy+=18
            words = ch.objective_detail.split()
            line_ = ""
            for w in words:
                test = line_ + w + " "
                if self.font_sm.size(test)[0] > panel.width-20:
                    self.screen.blit(self.font_sm.render(line_.strip(),True,CREAM),(x0,oy)); oy+=16
                    line_ = w + " "
                else:
                    line_ = test
            if line_:
                self.screen.blit(self.font_sm.render(line_.strip(),True,CREAM),(x0,oy))

        # Controls
        pygame.draw.line(self.screen, GOLD,
                         (x0,panel.bottom-150),(panel.right-10,panel.bottom-150), 1)
        cy = panel.bottom - 142
        for line in ["Arrows: Move","Z/Enter: Select","X/Esc: Cancel",
                     "A: Attack  H: Heal  W: Wait","T: Talk/Recruit  I: Stat Sheet",
                     "Space: End Turn  E: Seize"]:
            self.screen.blit(self.font_sm.render(line,True,LIGHT_GREY),(x0,cy)); cy+=16

    def _render_unit_card(self, unit, x0, y, x1):
        name_s = self.font_md.render(unit.name, True, WHITE)
        self.screen.blit(name_s, (x0, y)); y+=26
        cl_s = self.font_sm.render(f"{unit.unit_class}  Lv{unit.level}", True, LIGHT_GREY)
        self.screen.blit(cl_s, (x0,y)); y+=18
        fc_col = {FACTION_PLAYER:LIGHT_BLUE,FACTION_ENEMY:PINK,
                  FACTION_ALLY:(100,255,150)}.get(unit.faction,WHITE)
        tag = ""
        if unit.is_flying:  tag += "[Flying] "
        if unit.is_mounted: tag += "[Mounted] "
        if unit.is_lord:    tag += "♦ LORD "
        if unit.can_recruit and not unit.recruited: tag += "! RECRUIT"
        if tag:
            self.screen.blit(self.font_sm.render(tag,True,(150,255,150)),(x0,y)); y+=16
        fc_s = self.font_sm.render(unit.faction.upper(), True, fc_col)
        self.screen.blit(fc_s, (x0,y)); y+=20

        bw = x1-x0; bh = 10
        pct = unit.hp/unit.max_hp
        hc  = GREEN if pct>0.5 else YELLOW if pct>0.25 else RED
        pygame.draw.rect(self.screen,DARK_GREY,(x0,y,bw,bh))
        pygame.draw.rect(self.screen,hc,       (x0,y,int(bw*pct),bh))
        self.screen.blit(self.font_sm.render(f"HP:{unit.hp}/{unit.max_hp}",True,WHITE),(x0,y+12)); y+=28

        stats=[("STR",unit.str_),("MAG",unit.mag),("SKL",unit.skl),("SPD",unit.spd),
               ("LCK",unit.lck),("DEF",unit.def_),("RES",unit.res),("MOV",unit.move)]
        cw = (x1-x0)//2
        for i,(lb,vl) in enumerate(stats):
            self.screen.blit(self.font_sm.render(f"{lb}:{vl:3d}",True,LIGHT_GREY),
                             (x0+(i%2)*cw, y+(i//2)*16))
        y += (len(stats)//2)*16 + 6

        if unit.equipped:
            w = unit.equipped
            pygame.draw.line(self.screen,GOLD,(x0,y),(x1,y),1); y+=5
            self.screen.blit(self.font_sm.render("Equipped:",True,GOLD),(x0,y)); y+=16
            self.screen.blit(self.font_sm.render(w.name,True,WHITE),(x0,y)); y+=14
            self.screen.blit(self.font_sm.render(
                f"Mt:{w.might} Hit:{w.hit} Crit:{w.crit}  {w.min_range}-{w.max_range}rng",
                True,LIGHT_GREY),(x0,y)); y+=14

        pygame.draw.line(self.screen,GOLD,(x0,y),(x1,y),1); y+=3
        bw2=x1-x0
        pygame.draw.rect(self.screen,DARK_GREY,(x0,y,bw2,5))
        pygame.draw.rect(self.screen,CYAN,     (x0,y,int(bw2*unit.exp/100),5))
        self.screen.blit(self.font_sm.render(f"EXP:{unit.exp}/100",True,LIGHT_GREY),(x0,y+7)); y+=20
        return y

    def _render_terrain_info(self, terrain, td, x0, y):
        self.screen.blit(self.font_md.render(td["name"],True,WHITE),(x0,y)); y+=24
        for label, val in [("Def Bonus",f"+{td['def']}"),
                           ("Avo Bonus",f"+{td['avo']}"),
                           ("Move Cost",str(td['move']))]:
            self.screen.blit(self.font_sm.render(f"{label}: {val}",True,LIGHT_GREY),(x0,y)); y+=17
        return y

    # ── Message Box ───────────────────────────────────────────────────────────

    def _render_message_box(self, gs):
        if not gs.message_queue:
            return
        msg = gs.message_queue[0]
        box = pygame.Rect(SCREEN_WIDTH//2-300, SCREEN_HEIGHT-96, 600, 74)
        pygame.draw.rect(self.screen,(15,15,30), box)
        pygame.draw.rect(self.screen, GOLD, box, 2)
        ms = self.font_md.render(msg, True, WHITE)
        self.screen.blit(ms, ms.get_rect(center=box.center))
        ps = self.font_sm.render("Z/Enter to continue", True, LIGHT_GREY)
        self.screen.blit(ps, (box.x+10, box.bottom-20))

    # ── Combat Preview ────────────────────────────────────────────────────────

    def render_combat_preview(self, attacker, defender, gmap):
        box = pygame.Rect(180, SCREEN_HEIGHT//2-110, SCREEN_WIDTH-360, 220)
        pygame.draw.rect(self.screen,(10,10,25), box)
        pygame.draw.rect(self.screen, GOLD, box, 2)

        cx = box.centerx
        y  = box.y + 10
        title = self.font_md.render("Combat Forecast", True, GOLD)
        self.screen.blit(title, title.get_rect(center=(cx, y))); y+=32

        att_w = attacker.equipped
        def_w = defender.equipped

        att_atk  = attacker.attack_power(def_w, target=defender)
        att_hit  = max(0, min(100, attacker.hit_rate(def_w) - defender.avoid()))
        att_crit = max(0, attacker.crit_rate(def_w) - defender.crit_avoid())
        att_dmg  = max(0, att_atk - defender.defense())

        if def_w and not ("heal" in getattr(def_w,'weapon_id','') or
                          "mend" in getattr(def_w,'weapon_id','')):
            def_atk  = defender.attack_power(att_w, target=attacker)
            def_hit  = max(0, min(100, defender.hit_rate(att_w) - attacker.avoid()))
            def_crit = max(0, defender.crit_rate(att_w) - attacker.crit_avoid())
            def_dmg  = max(0, def_atk - attacker.defense())
        else:
            def_hit = def_crit = def_dmg = 0

        mid = box.centerx
        x0  = box.x + 15
        for name, dmg, hit, crit, col in [
            (attacker.name, att_dmg, att_hit, att_crit, LIGHT_BLUE),
            (defender.name, def_dmg, def_hit, def_crit, PINK),
        ]:
            cx_ = x0 if name == attacker.name else mid+10
            self.screen.blit(self.font_sm.render(name,True,col),(cx_, y))
            cl = attacker.unit_class if name==attacker.name else defender.unit_class
            self.screen.blit(self.font_sm.render(f"({cl})",True,LIGHT_GREY),(cx_,y+16))
            self.screen.blit(self.font_sm.render(f"Dmg:  {dmg}",True,WHITE),(cx_,y+32))
            self.screen.blit(self.font_sm.render(f"Hit:  {hit}%",True,WHITE),(cx_,y+48))
            cc = YELLOW if crit>0 else LIGHT_GREY
            self.screen.blit(self.font_sm.render(f"Crit: {crit}%",True,cc),(cx_,y+64))

        pygame.draw.line(self.screen, GOLD, (mid, y-4), (mid, y+96), 1)

        if att_w:
            tri = att_w.get_triangle_bonus(def_w)
            if tri != 0:
                tc  = YELLOW if tri>0 else RED
                ts  = "Weapon Advantage!" if tri>0 else "Weapon Disadvantage"
                self.screen.blit(self.font_sm.render(ts,True,tc),
                                 (cx-80, y+90))

        conf = self.font_sm.render("Z/Enter: Attack   X/Esc: Cancel", True, LIGHT_GREY)
        self.screen.blit(conf, conf.get_rect(center=(cx, box.bottom-22)))

    # ── Stat Sheet Overlay ────────────────────────────────────────────────────

    def render_stat_sheet(self, unit):
        """Full-page stat sheet, Samurai Warriors-style."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,200))
        self.screen.blit(overlay, (0,0))

        box = pygame.Rect(60, 40, SCREEN_WIDTH-120, SCREEN_HEIGHT-80)
        pygame.draw.rect(self.screen, (12,14,28), box)
        pygame.draw.rect(self.screen, GOLD, box, 3)

        # Portrait area (left column)
        port_rect = pygame.Rect(box.x+15, box.y+15, 180, 180)
        pygame.draw.rect(self.screen, _darken(unit.color, 30), port_rect)
        pygame.draw.rect(self.screen, unit.color, port_rect, 4)

        # Large class symbol in portrait
        big_sym = self.font_lg.render(unit.symbol, True, WHITE)
        self.screen.blit(big_sym, big_sym.get_rect(center=port_rect.center))

        # Faction badge
        fc_col = {FACTION_PLAYER:LIGHT_BLUE,FACTION_ENEMY:PINK,
                  FACTION_ALLY:(100,255,150)}.get(unit.faction, WHITE)
        fc_s = self.font_sm.render(unit.faction.upper(), True, fc_col)
        pygame.draw.rect(self.screen, _darken(fc_col,80),
                         (port_rect.x, port_rect.bottom-22, 180, 22))
        self.screen.blit(fc_s, fc_s.get_rect(
            center=(port_rect.centerx, port_rect.bottom-11)))

        # Name and class (right of portrait)
        nx = port_rect.right + 20
        ny = box.y + 18
        name_s = self.font_lg.render(unit.name, True, GOLD)
        self.screen.blit(name_s, (nx, ny)); ny += 38
        cls_s = self.font_md.render(f"{unit.unit_class}  —  Level {unit.level}", True, CREAM)
        self.screen.blit(cls_s, (nx, ny)); ny += 26

        # Tags
        tags = []
        if unit.is_lord:    tags.append(("LORD", GOLD))
        if unit.is_flying:  tags.append(("FLYING", (200,200,255)))
        if unit.is_mounted: tags.append(("MOUNTED", COPPER))
        if unit.water_walk: tags.append(("WATER WALK", BLUE))
        if unit.can_recruit and not unit.recruited:
            tags.append(("RECRUITABLE", (50,220,100)))
        tx_ = nx
        for tag, tc in tags:
            ts = self.font_sm.render(f"[{tag}]", True, tc)
            self.screen.blit(ts, (tx_, ny)); tx_ += ts.get_width()+8
        ny += 22

        # HP bar
        bw_ = 300; bh_ = 12
        pct = unit.hp / unit.max_hp
        hc  = GREEN if pct>0.5 else YELLOW if pct>0.25 else RED
        pygame.draw.rect(self.screen,DARK_GREY,(nx,ny,bw_,bh_))
        pygame.draw.rect(self.screen,hc,       (nx,ny,int(bw_*pct),bh_))
        self.screen.blit(self.font_sm.render(f"HP  {unit.hp} / {unit.max_hp}",
                         True, WHITE), (nx, ny+14)); ny += 34

        # EXP bar
        pygame.draw.rect(self.screen,DARK_GREY,(nx,ny,bw_,8))
        pygame.draw.rect(self.screen,CYAN,     (nx,ny,int(bw_*unit.exp/100),8))
        self.screen.blit(self.font_sm.render(f"EXP  {unit.exp} / 100",True,LIGHT_GREY),(nx,ny+10))

        # Quote (Samurai Warriors style)
        if unit.quote:
            qy = port_rect.bottom + 10
            pygame.draw.rect(self.screen,(20,18,35),
                             pygame.Rect(box.x+15, qy, 180, 70))
            pygame.draw.rect(self.screen, GOLD,
                             pygame.Rect(box.x+15, qy, 180, 70), 1)
            quote_lines = [unit.quote[i:i+22] for i in range(0, len(unit.quote), 22)]
            for ql in quote_lines[:3]:
                qs = self.font_sm.render(f'"{ql}', True, IVORY)
                self.screen.blit(qs, (box.x+20, qy+5)); qy += 18

        # ── Stats grid ────────────────────────────────────────────────────────
        sg_x = box.x + 15
        sg_y = box.y + 280
        pygame.draw.line(self.screen, GOLD, (sg_x, sg_y), (box.right-15, sg_y), 1)
        sg_y += 8

        stats = [
            ("HP",  f"{unit.max_hp}"), ("STR", f"{unit.str_}"),
            ("MAG", f"{unit.mag}"),    ("SKL",  f"{unit.skl}"),
            ("SPD", f"{unit.spd}"),    ("LCK",  f"{unit.lck}"),
            ("DEF", f"{unit.def_}"),   ("RES",  f"{unit.res}"),
            ("MOV", f"{unit.move}"),
        ]
        col_w = (box.width - 30) // 3
        for i, (lb, vl) in enumerate(stats):
            col = i % 3
            row = i // 3
            bx_ = sg_x + col * col_w
            by_ = sg_y + row * 20
            self.screen.blit(self.font_sm.render(lb+":", True, LIGHT_GREY),(bx_,by_))
            vs  = self.font_sm.render(vl, True, WHITE)
            self.screen.blit(vs, (bx_+40, by_))

        sg_y += (len(stats)//3 + 1) * 20 + 8

        # ── Weapon inventory ──────────────────────────────────────────────────
        pygame.draw.line(self.screen, GOLD, (sg_x, sg_y), (box.right-15, sg_y), 1); sg_y+=6
        self.screen.blit(self.font_md.render("Weapons", True, GOLD), (sg_x, sg_y)); sg_y+=22

        for i, w in enumerate(unit.weapons):
            equipped_marker = "► " if i == unit.equipped_weapon_index else "  "
            col_mark = WHITE if i == unit.equipped_weapon_index else LIGHT_GREY
            wline = f"{equipped_marker}{w.name:<20} {w.weapon_type:<10} Mt:{w.might:2d}  Hit:{w.hit:3d}  Crit:{w.crit:2d}  {w.min_range}-{w.max_range}rng"
            self.screen.blit(self.font_sm.render(wline, True, col_mark), (sg_x+5, sg_y)); sg_y+=17
            flags = []
            if w.anti_flying:  flags.append("Anti-Flying")
            if w.anti_mounted: flags.append("Anti-Mounted")
            if w.magic_damage: flags.append("Magic Dmg")
            if flags:
                self.screen.blit(self.font_sm.render("  " + " | ".join(flags),True,AMBER),(sg_x+5,sg_y)); sg_y+=15

        # ── Bio ───────────────────────────────────────────────────────────────
        pygame.draw.line(self.screen, GOLD, (sg_x, sg_y), (box.right-15, sg_y), 1); sg_y+=6
        for line in unit.bio.split("\n"):
            if sg_y > box.bottom - 30:
                break
            self.screen.blit(self.font_sm.render(line, True, CREAM), (sg_x, sg_y)); sg_y+=17

        # Dismiss hint
        close = self.font_sm.render("Press I or X to close", True, LIGHT_GREY)
        self.screen.blit(close, close.get_rect(center=(SCREEN_WIDTH//2, box.bottom-14)))

    # ── Recruit Dialog ────────────────────────────────────────────────────────

    def render_recruit_dialog(self, recruiter, target):
        box = pygame.Rect(120, 200, SCREEN_WIDTH-240, 320)
        pygame.draw.rect(self.screen,(12,20,12), box)
        pygame.draw.rect(self.screen,(50,220,100), box, 2)

        cx = box.centerx
        title = self.font_md.render("Recruit Unit?", True, (50,220,100))
        self.screen.blit(title, title.get_rect(center=(cx, box.y+14)))

        # Target portrait
        pr = pygame.Rect(box.x+20, box.y+40, 80, 80)
        pygame.draw.rect(self.screen, _darken(target.color,30), pr)
        pygame.draw.rect(self.screen, target.color, pr, 3)
        ts = self.font_md.render(target.symbol[:2], True, WHITE)
        self.screen.blit(ts, ts.get_rect(center=pr.center))

        # Info
        ix = pr.right + 16
        iy = box.y + 44
        self.screen.blit(self.font_md.render(target.name, True, WHITE), (ix, iy)); iy+=26
        self.screen.blit(self.font_sm.render(f"{target.unit_class}  Lv{target.level}",
                         True, LIGHT_GREY), (ix, iy)); iy+=20

        # Bio snippet
        bio_snippet = target.bio.split("\n")[0] if target.bio else ""
        self.screen.blit(self.font_sm.render(bio_snippet, True, CREAM), (ix, iy)); iy+=20

        # Quote
        if target.quote:
            qs = self.font_sm.render(f'"{target.quote}"', True, IVORY)
            self.screen.blit(qs, (box.x+20, box.y+140))

        # Weapon preview
        if target.equipped:
            w = target.equipped
            ws = self.font_sm.render(f"Carries: {w.name} ({w.weapon_type})",
                                     True, YELLOW)
            self.screen.blit(ws, (box.x+20, box.y+170))

        # Options
        z_s = self.font_md.render("Z / ENTER — Recruit", True, (50,220,100))
        x_s = self.font_md.render("X / ESC — Decline",   True, PINK)
        self.screen.blit(z_s, z_s.get_rect(center=(cx, box.bottom-60)))
        self.screen.blit(x_s, x_s.get_rect(center=(cx, box.bottom-30)))

    # ── End Screen ────────────────────────────────────────────────────────────

    def _render_end_screen(self, gs, victory=True):
        ov = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SRCALPHA)
        ov.fill((0,0,0,180)); self.screen.blit(ov,(0,0))
        cx = SCREEN_WIDTH//2
        if victory:
            t1 = self.font_title.render("VICTORY", True, GOLD)
        else:
            t1 = self.font_title.render("DEFEAT", True, DARK_RED)
        self.screen.blit(t1, t1.get_rect(center=(cx,220)))

        narrative = (gs.current_chapter.narrative_victory if victory
                     else gs.current_chapter.narrative_defeat)
        y = 300
        for line in narrative.split("\n"):
            s = self.font_sm.render(line, True, CREAM)
            self.screen.blit(s, s.get_rect(center=(cx,y))); y+=22

        if victory:
            p = "ENTER: Next Chapter  |  ESC: Title"
        else:
            p = "ENTER: Retry Chapter  |  ESC: Title"
        ps = self.font_sm.render(p, True, LIGHT_GREY)
        self.screen.blit(ps, ps.get_rect(center=(cx, 660)))
