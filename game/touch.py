'''
On-screen touch/mouse controls for Sengoku Tactics.
Renders a virtual D-pad, action buttons, and zoom controls.

Mobile features:
  - Drag-to-scroll the map (swipe panning)
  - +/- zoom buttons (scales TILE_SIZE)
  - Tap to select/act as before
  - All buttons sized for finger touch (min 52px)
  - Drag threshold: 8px — moves under threshold are treated as taps
'''
import math
import pygame
from game.constants import *


# ── Button definitions ─────────────────────────────────────────────────────────

class TouchButton:
    '''A single on-screen button.'''
    def __init__(self, action, label, icon, rect, color=(60, 60, 90)):
        self.action  = action
        self.label   = label
        self.icon    = icon
        self.rect    = pygame.Rect(rect)
        self.color   = color
        self.pressed = False

    def hit(self, mx, my):
        return self.rect.collidepoint(mx, my)


# ── Layout constants ───────────────────────────────────────────────────────────
BTN = 56          # button size px (larger for fat-finger friendliness)
PAD = 5           # gap between buttons

MAP_W = SCREEN_WIDTH - UI_PANEL_WIDTH

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
    cx = (_DX + BTN*2 + PAD) + ((_AX) - (_DX + BTN*2 + PAD)) // 2
    return (cx - BTN - PAD//2, _AY + BTN + PAD, BTN*2 + PAD, BTN)

# Zoom buttons — top-right corner of map area
_ZX = MAP_W - BTN*2 - PAD - 8
_ZY = 8

ALL_BUTTONS = [
    # D-pad
    TouchButton("up",    "Up",    "▲", _dpad_rect(1,0), (50,60,100)),
    TouchButton("left",  "Left",  "◄", _dpad_rect(0,1), (50,60,100)),
    TouchButton("down",  "Down",  "▼", _dpad_rect(1,2), (50,60,100)),
    TouchButton("right", "Right", "►", _dpad_rect(2,1), (50,60,100)),

    # Confirm / Cancel (center of d-pad area)
    TouchButton("confirm","OK",  "✓", _dpad_rect(1,1), (40,90,50)),

    # Action row 1: Attack | Heal | Talk | Info
    TouchButton("attack",   "Attack",   "⚔",  _action_rect(0,0), (160,40,40)),
    TouchButton("heal",     "Heal",     "♥",  _action_rect(1,0), (40,120,80)),
    TouchButton("talk",     "Talk",     "!",  _action_rect(2,0), (40,160,80)),
    TouchButton("info",     "Info",     "i",  _action_rect(3,0), (80,80,160)),

    # Action row 2: Wait | Seize | Cancel | Help
    TouchButton("wait",   "Wait",   "Zz", _action_rect(0,1), (80,80,80)),
    TouchButton("seize",  "Seize",  "★",  _action_rect(1,1), (160,140,30)),
    TouchButton("cancel", "Cancel", "✕",  _action_rect(2,1), (120,40,40)),
    TouchButton("help",   "Help",   "?",  _action_rect(3,1), (60,80,120)),

    # End Turn — wide button below everything
    TouchButton("end_turn","End Turn","▶▶", _end_turn_rect(), (40,60,120)),

    # Zoom buttons (top-right of map area)
    TouchButton("zoom_in",  "Zoom+", "+", (_ZX + BTN + PAD, _ZY, BTN, BTN), (40,50,80)),
    TouchButton("zoom_out", "Zoom-", "-", (_ZX, _ZY, BTN, BTN), (40,50,80)),
]

# Quick lookup by action
BUTTON_MAP = {b.action: b for b in ALL_BUTTONS}

# Drag threshold in pixels — less than this → treated as a tap
DRAG_THRESHOLD = 10


# ── TouchControls ─────────────────────────────────────────────────────────────

class TouchControls:
    def __init__(self, font_sm, font_md):
        self.font_sm = font_sm
        self.font_md = font_md
        self.visible = True
        self._pressed = set()

        # Drag-scroll state
        self._drag_start_px  = None   # (mx, my) where finger went down
        self._drag_last_px   = None   # (mx, my) last motion position
        self._is_dragging    = False  # True once drag threshold exceeded
        self.drag_cam_delta  = (0, 0) # tile delta to apply this frame
        self._drag_px_accum  = [0, 0] # sub-tile pixel accumulator

        # Pinch-zoom state (two fingers)
        self._finger_positions = {}   # finger_id → (px, py) in pixels
        self._finger_starts    = {}   # finger_id → (px, py) at finger-down
        self._pinch_start_dist = None

    # ── Button interaction ────────────────────────────────────────────────────

    def handle_mouse_down(self, mx, my):
        '''Call on MOUSEBUTTONDOWN (left button). Returns action string or None.'''
        # Check buttons first
        for btn in ALL_BUTTONS:
            if btn.hit(mx, my):
                btn.pressed = True
                self._pressed.add(btn.action)
                self._drag_start_px = None  # button tap, not drag
                return btn.action
        # Start drag tracking on map area
        if mx < MAP_W:
            self._drag_start_px = (mx, my)
            self._drag_last_px  = (mx, my)
            self._is_dragging   = False
            self._drag_px_accum = [0, 0]
        self.drag_cam_delta = (0, 0)
        return None

    def handle_mouse_motion(self, mx, my):
        '''Call on MOUSEMOTION (with left button held). Updates drag state.
        Returns True if dragging (caller should suppress tile-click logic).'''
        if self._drag_start_px is None:
            return False
        sx, sy = self._drag_start_px
        dx_total = mx - sx
        dy_total = my - sy
        dist = math.hypot(dx_total, dy_total)
        if dist >= DRAG_THRESHOLD:
            self._is_dragging = True
        if self._is_dragging and self._drag_last_px:
            lx, ly = self._drag_last_px
            # Raw pixel delta this frame (drag direction → cam moves opposite)
            raw_dx = -(mx - lx)
            raw_dy = -(my - ly)
            self._drag_px_accum[0] += raw_dx
            self._drag_px_accum[1] += raw_dy
            # Convert accumulated pixels to whole tiles
            tile_dx = int(self._drag_px_accum[0] // TILE_SIZE)
            tile_dy = int(self._drag_px_accum[1] // TILE_SIZE)
            if tile_dx != 0:
                self._drag_px_accum[0] -= tile_dx * TILE_SIZE
            if tile_dy != 0:
                self._drag_px_accum[1] -= tile_dy * TILE_SIZE
            self.drag_cam_delta = (tile_dx, tile_dy)
        else:
            self.drag_cam_delta = (0, 0)
        self._drag_last_px = (mx, my)
        return self._is_dragging

    def handle_mouse_up(self, mx, my):
        '''Returns True if this was a drag (not a tap).'''
        was_drag = self._is_dragging
        for btn in ALL_BUTTONS:
            btn.pressed = False
        self._pressed.clear()
        self._drag_start_px = None
        self._drag_last_px  = None
        self._is_dragging   = False
        self.drag_cam_delta = (0, 0)
        self._drag_px_accum = [0, 0]
        return was_drag

    def tile_at_click(self, mx, my, renderer):
        '''Convert a map-area click to tile coordinates. Returns (None,None) if on button.'''
        if mx >= MAP_W:
            return None, None
        for btn in ALL_BUTTONS:
            if btn.hit(mx, my):
                return None, None
        tx, ty = renderer.screen_to_tile(mx, my)
        return tx, ty

    # ── Finger / pinch zoom ───────────────────────────────────────────────────

    def handle_finger_down(self, finger_id, fx, fy, sw, sh):
        '''Track finger for pinch-zoom and tap detection. fx/fy are 0..1 normalized.'''
        px, py = fx * sw, fy * sh
        self._finger_positions[finger_id] = (px, py)
        self._finger_starts[finger_id]    = (px, py)
        if len(self._finger_positions) == 2:
            pts = list(self._finger_positions.values())
            self._pinch_start_dist = math.hypot(pts[0][0]-pts[1][0], pts[0][1]-pts[1][1])

    def handle_finger_motion(self, finger_id, fx, fy, sw, sh):
        '''Returns zoom delta (+1/-1) if pinch detected, else 0.'''
        if finger_id not in self._finger_positions:
            return 0
        self._finger_positions[finger_id] = (fx * sw, fy * sh)
        if len(self._finger_positions) == 2 and self._pinch_start_dist:
            pts = list(self._finger_positions.values())
            cur_dist = math.hypot(pts[0][0]-pts[1][0], pts[0][1]-pts[1][1])
            ratio = cur_dist / max(self._pinch_start_dist, 1)
            if ratio > 1.25:
                self._pinch_start_dist = cur_dist
                return 1    # zoom in
            elif ratio < 0.8:
                self._pinch_start_dist = cur_dist
                return -1   # zoom out
        return 0

    def handle_finger_up(self, finger_id):
        '''Returns (px, py) pixel position if this was a single-finger lift (not a pinch), else None.'''
        tap = None
        if finger_id in self._finger_positions:
            # Only fire a tap when no other finger is currently active (not a pinch gesture)
            if len(self._finger_positions) == 1:
                ex, ey = self._finger_positions[finger_id]
                tap = (int(ex), int(ey))
        self._finger_positions.pop(finger_id, None)
        self._finger_starts.pop(finger_id, None)
        if len(self._finger_positions) < 2:
            self._pinch_start_dist = None
        return tap

    # ── Rendering ─────────────────────────────────────────────────────────────

    def render(self, screen):
        if not self.visible:
            return

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        for btn in ALL_BUTTONS:
            alpha = 230 if btn.pressed else 180
            bc    = tuple(min(255, c + (50 if btn.pressed else 0)) for c in btn.color)
            pygame.draw.rect(overlay, (*bc, alpha), btn.rect, border_radius=10)
            border_col = (255,255,255,210) if btn.pressed else (180,180,220,160)
            pygame.draw.rect(overlay, border_col, btn.rect, width=2, border_radius=10)

        screen.blit(overlay, (0, 0))

        for btn in ALL_BUTTONS:
            icon_s = self.font_md.render(btn.icon, True, WHITE)
            cx = btn.rect.centerx
            cy = btn.rect.centery - 8
            screen.blit(icon_s, icon_s.get_rect(center=(cx, cy)))
            lbl_s = self.font_sm.render(btn.label, True, (200,210,230))
            screen.blit(lbl_s, lbl_s.get_rect(center=(cx, btn.rect.bottom - 10)))
