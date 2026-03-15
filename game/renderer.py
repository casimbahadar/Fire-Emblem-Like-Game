"""
Renderer for Sengoku Tactics
Includes: map, units, overlays, UI panel, combat preview,
          stat sheet (FE-style), boss dialog, tutorial overlay,
          touch/mouse button controls, recruit dialog.
"""
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
        self._build_terrain_surfaces()

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
        vw = self.map_rect.width  // TILE_SIZE
        vh = self.map_rect.height // TILE_SIZE
        self.cam_x = max(0, min(cx - vw//2, gmap.width  - vw))
        self.cam_y = max(0, min(cy - vh//2, gmap.height - vh))

    def tile_to_screen(self, tx, ty):
        return (tx-self.cam_x)*TILE_SIZE, (ty-self.cam_y)*TILE_SIZE

    def screen_to_tile(self, sx, sy):
        return sx//TILE_SIZE + self.cam_x, sy//TILE_SIZE + self.cam_y

    # ── Top-level render dispatcher ───────────────────────────────────────────
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
        gmap = gs.game_map
        pygame.draw.rect(self.screen,(30,30,30),self.map_rect)
        vw = self.map_rect.width  // TILE_SIZE + 2
        vh = self.map_rect.height // TILE_SIZE + 2
        for ty in range(self.cam_y, min(self.cam_y+vh, gmap.height)):
            for tx in range(self.cam_x, min(self.cam_x+vw, gmap.width)):
                t   = gmap.get_terrain(tx, ty)
                s   = self._tile_surfs.get(t, self._tile_surfs[TERRAIN_PLAIN])
                sx, sy = self.tile_to_screen(tx, ty)
                self.screen.blit(s, (sx,sy))
        pygame.draw.rect(self.screen,DARK_GREY,self.map_rect,2)

    # ── Overlays ──────────────────────────────────────────────────────────────
    def _render_overlays(self, gs):
        def stamp(tx, ty, color, alpha, border=None, border_alpha=200):
            sx, sy = self.tile_to_screen(tx, ty)
            if not self.map_rect.collidepoint(sx+TILE_SIZE//2, sy+TILE_SIZE//2):
                return
            ov = pygame.Surface((TILE_SIZE,TILE_SIZE), pygame.SRCALPHA)
            ov.fill((*color, alpha))
            self.screen.blit(ov,(sx,sy))
            if border:
                pygame.draw.rect(self.screen,(*border,border_alpha),
                                 (sx,sy,TILE_SIZE,TILE_SIZE),2)

        # Seize points
        for (sx,sy) in gs.game_map.seize_points:
            stamp(sx,sy,(200,170,20),90,GOLD,220)
            self.screen.blit(
                self.font_sm.render("★",True,GOLD),
                (sx*TILE_SIZE - self.cam_x*TILE_SIZE+2,
                 sy*TILE_SIZE - self.cam_y*TILE_SIZE+2))

        if gs.selected_unit:
            for (tx,ty) in getattr(gs,'move_range_land',set()):
                stamp(tx,ty,(60,100,220),100,(80,130,255))
            for (tx,ty) in gs.attack_range:
                stamp(tx,ty,(220,60,60),80,(255,90,90))
            for t in gs.get_recruitable_adjacent(gs.selected_unit):
                stamp(t.x,t.y,(40,210,90),100,(50,240,110))

    # ── Units ─────────────────────────────────────────────────────────────────
    def _render_units(self, gs):
        for unit in gs.all_units():
            if not unit.alive:
                continue
            sx,sy = self.tile_to_screen(unit.x, unit.y)
            if not self.map_rect.collidepoint(sx+TILE_SIZE//2, sy+TILE_SIZE//2):
                continue
            self._draw_unit(unit, sx, sy, gs)

    def _draw_unit(self, unit, sx, sy, gs):
        cx_ = sx+TILE_SIZE//2; cy_ = sy+TILE_SIZE//2
        r   = TILE_SIZE//2 - 3
        color = unit.color
        if unit.has_acted and unit.faction == FACTION_PLAYER:
            color = _darken(color,80)
        # Shadow / flying altitude shadow
        if unit.is_flying:
            pygame.draw.ellipse(self.screen,_darken(color,80),(sx+4,sy+TILE_SIZE-10,TILE_SIZE-8,8))
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
        bw=TILE_SIZE-8; bh=4; bx=sx+4; by=sy+TILE_SIZE-7
        pct=unit.hp/unit.max_hp
        hc=GREEN if pct>0.5 else YELLOW if pct>0.25 else RED
        pygame.draw.rect(self.screen,DARK_GREY,(bx,by,bw,bh))
        pygame.draw.rect(self.screen,hc,       (bx,by,int(bw*pct),bh))
        # Selected
        if gs.selected_unit==unit:
            pygame.draw.rect(self.screen,WHITE,(sx+1,sy+1,TILE_SIZE-2,TILE_SIZE-2),2)
        if unit.is_lord:
            self.screen.blit(self.font_sm.render("♦",True,GOLD),(sx+TILE_SIZE-14,sy+1))
        if unit.can_recruit and not unit.recruited:
            self.screen.blit(self.font_sm.render("!",True,(50,220,100)),(sx+TILE_SIZE-12,sy+TILE_SIZE-16))

    # ── Cursor ────────────────────────────────────────────────────────────────
    def _render_cursor(self, gs):
        sx,sy = self.tile_to_screen(gs.cursor_x, gs.cursor_y)
        if not self.map_rect.collidepoint(sx+TILE_SIZE//2, sy+TILE_SIZE//2):
            return
        alpha = int(160+80*abs((pygame.time.get_ticks()%1000)/500-1))
        cs = pygame.Surface((TILE_SIZE,TILE_SIZE),pygame.SRCALPHA)
        pygame.draw.rect(cs,(255,255,255,min(255,alpha)),(0,0,TILE_SIZE,TILE_SIZE),3)
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
            pygame.draw.line(self.screen,GOLD,(x0,p.bottom-280),(p.right-10,p.bottom-280),1)
            oy=p.bottom-272
            self.screen.blit(self.font_sm.render("Objective:",True,YELLOW),(x0,oy)); oy+=18
            for w in self._wrap(ch.objective_detail, p.width-20):
                self.screen.blit(self.font_sm.render(w,True,CREAM),(x0,oy)); oy+=16

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
        """
        Render a multi-line cinematic boss dialog.
        lines: list of (speaker_id, text)
        line_idx: current line index
        unit_roster: dict id->Unit for portrait lookup
        """
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
        """
        Render the tutorial stage overlay.
        tm: TutorialManager instance
        """
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

    def _draw_rounded_box(self, x, y, w, h, fill, border, r=6):
        pygame.draw.rect(self.screen, fill,   pygame.Rect(x,y,w,h), border_radius=r)
        pygame.draw.rect(self.screen, border, pygame.Rect(x,y,w,h), 2, border_radius=r)
