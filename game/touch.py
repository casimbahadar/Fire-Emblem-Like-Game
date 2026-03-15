"""
On-screen touch/mouse controls for Sengoku Tactics.
Renders a virtual D-pad and action button grid over the map area.
Works with both mouse clicks and touchscreen taps via pygame.
"""
import pygame
from game.constants import *


# ── Button definitions ─────────────────────────────────────────────────────────

class TouchButton:
    """A single on-screen button."""
    def __init__(self, action, label, icon, rect, color=(60, 60, 90)):
        self.action  = action   # string: "up","down","left","right","confirm","cancel","attack",
                                #         "heal","wait","talk","info","seize","end_turn"
        self.label   = label
        self.icon    = icon     # single char / emoji-replacement string
        self.rect    = pygame.Rect(rect)
        self.color   = color
        self.pressed = False

    def hit(self, mx, my):
        return self.rect.collidepoint(mx, my)


# ── Layout constants ───────────────────────────────────────────────────────────
BTN = 52          # button size px
PAD = 4           # gap between buttons

MAP_W = SCREEN_WIDTH - UI_PANEL_WIDTH   # 734

# D-pad (bottom-left of map area)
_DX = 12
_DY = SCREEN_HEIGHT - BTN*3 - PAD*2 - 8

# Action grid (bottom-right of map area — left of UI panel)
_AX = MAP_W - BTN*4 - PAD*3 - 12
_AY = SCREEN_HEIGHT - BTN*2 - PAD - 8


def _dpad_rect(col, row):
    return (_DX + col*(BTN+PAD), _DY + row*(BTN+PAD), BTN, BTN)

def _action_rect(col, row):
    return (_AX + col*(BTN+PAD), _AY + row*(BTN+PAD), BTN, BTN)


def _end_turn_rect():
    # Centered between D-pad and action grid
    cx = (_DX + BTN*2 + PAD) + ((_AX) - (_DX + BTN*2 + PAD)) // 2
    return (cx - BTN - PAD//2, _AY + BTN + PAD, BTN*2 + PAD, BTN)


ALL_BUTTONS = [
    # D-pad
    TouchButton("up",    "Up",    "▲", _dpad_rect(1,0), (50,60,100)),
    TouchButton("left",  "Left",  "◄", _dpad_rect(0,1), (50,60,100)),
    TouchButton("down",  "Down",  "▼", _dpad_rect(1,2), (50,60,100)),
    TouchButton("right", "Right", "►", _dpad_rect(2,1), (50,60,100)),

    # Confirm / Cancel (center of d-pad area)
    TouchButton("confirm","OK",   "✓", _dpad_rect(1,1), (40,90,50)),

    # Action row 1: Attack | Heal | Talk | Info
    TouchButton("attack",   "Attack",   "⚔",  _action_rect(0,0), (160,40,40)),
    TouchButton("heal",     "Heal",     "♥",  _action_rect(1,0), (40,120,80)),
    TouchButton("talk",     "Talk",     "!",  _action_rect(2,0), (40,160,80)),
    TouchButton("info",     "Info",     "i",  _action_rect(3,0), (80,80,160)),

    # Action row 2: Wait | Seize | Cancel | —
    TouchButton("wait",   "Wait",   "Zz", _action_rect(0,1), (80,80,80)),
    TouchButton("seize",  "Seize",  "★",  _action_rect(1,1), (160,140,30)),
    TouchButton("cancel", "Cancel", "✕",  _action_rect(2,1), (120,40,40)),

    # End Turn — wide button below everything
    TouchButton("end_turn","End Turn","▶▶", _end_turn_rect(), (40,60,120)),
]

# Quick lookup by action
BUTTON_MAP = {b.action: b for b in ALL_BUTTONS}


# ── Renderer ──────────────────────────────────────────────────────────────────

class TouchControls:
    def __init__(self, font_sm, font_md):
        self.font_sm = font_sm
        self.font_md = font_md
        self.visible = True
        self._pressed = set()   # actions currently held

    def handle_mouse_down(self, mx, my):
        """Call on MOUSEBUTTONDOWN. Returns action string or None."""
        for btn in ALL_BUTTONS:
            if btn.hit(mx, my):
                btn.pressed = True
                self._pressed.add(btn.action)
                return btn.action
        return None

    def handle_mouse_up(self, mx, my):
        for btn in ALL_BUTTONS:
            btn.pressed = False
        self._pressed.clear()

    def tile_at_click(self, mx, my, renderer):
        """Convert a map-area click to tile coordinates."""
        if mx >= MAP_W:
            return None, None   # clicked UI panel
        # Make sure no button was hit
        for btn in ALL_BUTTONS:
            if btn.hit(mx, my):
                return None, None
        tx, ty = renderer.screen_to_tile(mx, my)
        return tx, ty

    def render(self, screen):
        if not self.visible:
            return

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        for btn in ALL_BUTTONS:
            # Background
            alpha = 220 if btn.pressed else 170
            bc    = tuple(min(255, c + (40 if btn.pressed else 0)) for c in btn.color)
            pygame.draw.rect(overlay, (*bc, alpha), btn.rect, border_radius=8)
            # Border
            border_col = (255,255,255,200) if btn.pressed else (180,180,220,160)
            pygame.draw.rect(overlay, border_col, btn.rect, width=2, border_radius=8)

        screen.blit(overlay, (0, 0))

        # Labels (drawn after overlay for crisp text)
        for btn in ALL_BUTTONS:
            # Icon line
            icon_s = self.font_md.render(btn.icon, True, WHITE)
            cx = btn.rect.centerx
            cy = btn.rect.centery - 8
            screen.blit(icon_s, icon_s.get_rect(center=(cx, cy)))
            # Label
            lbl_s = self.font_sm.render(btn.label, True, (200,210,230))
            screen.blit(lbl_s, lbl_s.get_rect(center=(cx, btn.rect.bottom - 10)))
