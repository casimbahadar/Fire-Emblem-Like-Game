'''
Skippable Tutorial System for Sengoku Tactics.
Chapter 0 — "The Way of the Warrior"
Step-by-step Fire Emblem-style tutorial with touch/keyboard support.
'''
from game.constants import *
from game.map import GameMap


# ── Tutorial Stage Definitions ─────────────────────────────────────────────────

class TutorialStage:
    def __init__(self, stage_id, title, body, highlight_tiles=None,
                 highlight_units=None, completion="any_key",
                 arrow_pos=None, action_hint=None):
        self.stage_id       = stage_id
        self.title          = title
        self.body           = body             # list of strings (lines)
        self.highlight_tiles= highlight_tiles or []  # [(x,y), ...] glow gold
        self.highlight_units= highlight_units or []  # unit_ids to highlight
        self.completion     = completion       # "any_key", "moved", "attacked", etc.
        self.arrow_pos      = arrow_pos        # (x,y) tile to draw arrow at
        self.action_hint    = action_hint      # short button label shown in box


TUTORIAL_STAGES = [
    # ── Turn 1: Welcome & basic movement ─────────────────────────────────────
    # ── Turn 1: Welcome & basic movement ─────────────────────────────────────
    TutorialStage(
        "welcome",
        "NOBUNAGA: Fresh Recruit!",
        ["NOBUNAGA: 'So, you are the new commander assigned to",
         "  my army. I am Oda Nobunaga — the Demon King.",
         "  I do not suffer fools, so pay attention.'",
         "",
         "  'I will teach you how war is waged in this era.",
         "  Press S at any time to skip if you dare.'"],
        completion="any_key",
        action_hint="Tap screen or press Z/Enter",
    ),
    TutorialStage(
        "cursor",
        "NOBUNAGA: Survey the Field",
        ["NOBUNAGA: 'First — learn to survey the battlefield.'",
         "",
         "  Keyboard:  ARROW KEYS or WASD",
         "  Touch:     D-PAD buttons (bottom-left corner)",
         "",
         "  'Move the cursor to the GOLD tile. Now.'"],
        highlight_tiles=[(5, 7)],
        arrow_pos=(5, 7),
        completion="cursor_at_highlight",
        action_hint="D-Pad / Arrows → gold tile",
    ),
    TutorialStage(
        "select_unit",
        "NOBUNAGA: Select Your Warrior",
        ["NOBUNAGA: 'Good. Now you must command me directly.'",
         "",
         "  Keyboard:  Move cursor to me, press Z or ENTER",
         "  Touch:     TAP directly on my unit",
         "",
         "  'BLUE borders = your allies.  RED = enemies.",
         "  The ♦ symbol means LORD — that is me.'"],
        highlight_units=["nobunaga"],
        completion="unit_selected",
        action_hint="Tap Nobunaga or Z/Enter on him",
    ),
    TutorialStage(
        "move_unit",
        "NOBUNAGA: Advance!",
        ["NOBUNAGA: 'The BLUE tiles show where I can move.'",
         "",
         "  Keyboard:  Move cursor to a blue tile, press Z",
         "  Touch:     TAP any blue tile directly",
         "",
         "  'Plains = 1 move, Forest = 2, Mountain = 4.",
         "  Move me toward the enemy. Go!'"],
        completion="unit_moved",
        action_hint="Tap a blue tile or press Z on it",
    ),

    # ── Turn 1: Combat — broken into sub-steps ───────────────────────────────
    TutorialStage(
        "attack_intro",
        "NOBUNAGA: Time to Fight!",
        ["NOBUNAGA: 'An enemy Ashigaru is nearby. Pitiful.",
         "  After moving, you can ATTACK an adjacent enemy.'",
         "",
         "  Keyboard:  Press the A key",
         "  Touch:     Tap the ⚔ ATTACK button (right side)",
         "",
         "  'Do it now while I am selected!'"],
        highlight_units=["nobunaga"],
        completion="attack_pressed",
        action_hint="Tap ⚔ Attack or press A",
    ),
    TutorialStage(
        "attack_forecast",
        "NOBUNAGA: The Combat Forecast",
        ["NOBUNAGA: 'This is the COMBAT FORECAST. Study it!",
         "  It shows Damage, Hit%, and Crit% for both sides.'",
         "",
         "  Keyboard:  Z/ENTER = confirm, X/ESC = cancel",
         "  Touch:     TAP the OK button (✓) to confirm",
         "",
         "  'Strike now! Confirm the attack!'"],
        completion="enemy_defeated",
        action_hint="Tap ✓ or press Z to confirm",
    ),
    TutorialStage(
        "first_blood",
        "NOBUNAGA: First Blood!",
        ["NOBUNAGA: 'Ha! That is how the Oda army fights!",
         "  You gained EXP from combat. Enough EXP and",
         "  your unit will LEVEL UP — growing stronger.'",
         "",
         "  'After attacking, a unit's turn is DONE.",
         "  They turn darker to show they have acted.'"],
        completion="any_key",
        action_hint="Tap or press Z/Enter",
    ),

    # ── Turn 1: Other units ──────────────────────────────────────────────────
    TutorialStage(
        "wait_explain",
        "NOBUNAGA: Commanding Other Units",
        ["NOBUNAGA: 'You have more warriors to command.",
         "  Select another unit, move them, then WAIT.'",
         "",
         "  Keyboard:  Select unit → move → press W",
         "  Touch:     Tap unit → tap blue tile → tap Zz WAIT",
         "",
         "  'Not every unit needs to fight each turn.'"],
        completion="wait_used",
        action_hint="Tap unit → move → tap Zz Wait",
    ),
    TutorialStage(
        "end_turn",
        "NOBUNAGA: End the Turn",
        ["NOBUNAGA: 'All units have acted. Now end your turn.'",
         "",
         "  Keyboard:  Press SPACE",
         "  Touch:     Tap the END TURN button (▶▶)",
         "",
         "  'After you end, the enemy takes their turn.",
         "  Then a new round begins. End your turn!'"],
        completion="turn_ended",
        action_hint="Tap ▶▶ End Turn or press Space",
    ),

    # ── Turn 2+: Advanced concepts ───────────────────────────────────────────
    TutorialStage(
        "enemy_phase",
        "NOBUNAGA: The Enemy Strikes Back",
        ["NOBUNAGA: 'The enemy has moved. They attack on THEIR",
         "  turn automatically — you cannot control them.'",
         "",
         "  'If an enemy attacks your unit, YOUR unit fights",
         "  back automatically. This is called a COUNTER.",
         "  Position your units where they can counter!'"],
        completion="any_key",
        action_hint="Tap or press Z/Enter",
    ),
    TutorialStage(
        "weapon_triangle",
        "NOBUNAGA: The Weapon Triangle",
        ["NOBUNAGA: 'Weapons have strengths and weaknesses:",
         "  YARI (Spear) beats KATANA (Sword)",
         "  KATANA beats NAGINATA (Polearm)",
         "  NAGINATA beats YARI'",
         "",
         "  'BOW strikes from range but cannot hit adjacent.",
         "  Always check the COMBAT FORECAST before striking.'"],
        completion="any_key",
        action_hint="Tap or press Z/Enter",
    ),
    TutorialStage(
        "terrain",
        "NOBUNAGA: Use the Land",
        ["NOBUNAGA: 'A wise commander uses terrain.",
         "  FORESTS:  +1 DEF, +20 Avoid",
         "  FORTS:    +2 DEF, heals HP each turn!",
         "  CASTLES:  +3 DEF, +30 Avoid'",
         "",
         "  'The right panel shows terrain bonuses when you",
         "  hover over a tile. Use this to your advantage!'"],
        highlight_tiles=[(4, 4), (4, 5), (2, 5)],
        completion="any_key",
        action_hint="Tap or press Z/Enter",
    ),
    TutorialStage(
        "healing",
        "NOBUNAGA: Heal Your Wounded",
        ["NOBUNAGA: 'Nene carries a healing staff.'",
         "",
         "  Keyboard:  Select Nene → move near ally → H",
         "  Touch:     Tap Nene → tap blue tile → tap ♥ HEAL",
         "",
         "  'Healers keep your army alive. Protect them!",
         "  Heal any wounded ally with Nene now.'"],
        highlight_units=["nene"],
        completion="heal_used",
        action_hint="Tap Nene → move → tap ♥ Heal",
    ),
    TutorialStage(
        "recruit",
        "NOBUNAGA: Recruit the Willing",
        ["NOBUNAGA: 'That Ashigaru with the GREEN marker",
         "  wishes to join the Oda. Talk to him!'",
         "",
         "  Keyboard:  Move adjacent to him → press T",
         "  Touch:     Move adjacent → tap ! TALK button",
         "",
         "  'Recruited units fight for you permanently!'"],
        highlight_tiles=[(6, 3)],
        arrow_pos=(6, 3),
        completion="unit_recruited",
        action_hint="Move adjacent → tap ! Talk",
    ),
    TutorialStage(
        "stat_sheet",
        "NOBUNAGA: Know Your Warriors",
        ["NOBUNAGA: 'View a unit's full stats and weapons.'",
         "",
         "  Keyboard:  Move cursor to unit → press I",
         "  Touch:     Select unit → tap i INFO button",
         "",
         "  'A commander who does not know their own army",
         "  is no commander at all. View my stats now!'"],
        highlight_units=["nobunaga"],
        completion="stat_sheet_opened",
        action_hint="Select Nobunaga → tap i Info",
    ),
    TutorialStage(
        "seize",
        "NOBUNAGA: Claim Victory!",
        ["NOBUNAGA: 'The GOLD tile is the SEIZE point.",
         "  Only I, the LORD (♦), can seize it.'",
         "",
         "  Keyboard:  Move me onto it → press E",
         "  Touch:     Move me onto it → tap ★ SEIZE",
         "",
         "  'Take the castle! Move me there now!'"],
        highlight_tiles=[(7, 8)],
        arrow_pos=(7, 8),
        completion="chapter_seize",
        action_hint="Move Nobunaga → tap ★ Seize",
    ),
    TutorialStage(
        "complete",
        "NOBUNAGA: You May Yet Survive",
        ["NOBUNAGA: 'Not terrible, for a beginner.",
         "  Remember these commands:'",
         "  ⚔=Attack ♥=Heal Zz=Wait !=Talk i=Info ★=Seize",
         "  ▶▶=End Turn    ✓=Confirm    ✕=Cancel",
         "",
         "  'The real war begins now. Chapter 1 awaits.",
         "  Do not disappoint me, commander.'"],
        completion="any_key",
        action_hint="Tap or press Z/Enter to begin Ch.1",
    ),
]

STAGE_INDEX = {s.stage_id: i for i, s in enumerate(TUTORIAL_STAGES)}


# ── Tutorial Map ───────────────────────────────────────────────────────────────
def make_tutorial_map():
    P = TERRAIN_PLAIN;   F = TERRAIN_FOREST; M = TERRAIN_MOUNTAIN
    T = TERRAIN_FORT;    V = TERRAIN_VILLAGE; C = TERRAIN_CASTLE
    R = TERRAIN_RIVER;   B = TERRAIN_BRIDGE;  D = TERRAIN_ROAD
    tiles = [
        [P, P, P, P, P, P, P, P, P, P, P, P],
        [P, P, V, P, P, P, P, P, V, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P],
        [P, F, F, F, P, P, P, P, P, P, P, P],   # forest terrain demo
        [P, F, T, P, P, P, P, P, P, P, P, P],   # fort demo
        [P, P, P, P, P, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, P, C, C, P, P, P],   # castle seize point
        [P, P, P, P, P, P, P, P, P, P, P, P],
    ]
    gmap = GameMap(12, 10, tiles, name="Tutorial — Way of the Warrior")
    gmap.seize_points   = [(7, 8)]
    gmap.village_points = [(2, 1), (8, 1)]
    gmap.fort_points    = [(2, 5)]
    return gmap


# ── Tutorial Chapter Definition ────────────────────────────────────────────────
# Returns dicts compatible with Chapter.build() output structure.

TUTORIAL_PLAYER_DEFS = [
    ("nobunaga", 2, 9),
    ("nene",     1, 9),
    ("nagahide", 3, 9),
    ("ranmaru",  2, 8),
]

TUTORIAL_ENEMY_DEFS = [
    ("e_ash1", 4, 7),   # nearby enemy — for first combat lesson
    ("e_ash2", 9, 5),   # farther enemy
]

TUTORIAL_RECRUIT_DEF = ("oda_ash1", 6, 3)   # positioned separately; flagged recruitable

TUTORIAL_CHAPTER_TITLE   = "Tutorial"
TUTORIAL_CHAPTER_SUBTITLE = "The Way of the Warrior"
TUTORIAL_INTRO = (
    "Before the first battle, every commander must learn\n"
    "the language of war.\n\n"
    "NOBUNAGA: 'Pay attention. I only explain once.'\n"
    "RANMARU:  'Yes, my lord! ...What if we forget?'\n"
    "NOBUNAGA: 'Then you'll learn the hard way. Like everyone else.'"
)


# ── Tutorial State Machine ─────────────────────────────────────────────────────

class TutorialManager:
    def __init__(self):
        self.active          = False
        self.skipped         = False
        self.stage_idx       = 0
        self.completed_flags = set()   # flags set by game events
        self._stat_opened    = False

    @property
    def current_stage(self):
        if self.stage_idx < len(TUTORIAL_STAGES):
            return TUTORIAL_STAGES[self.stage_idx]
        return None

    def start(self):
        self.active    = True
        self.skipped   = False
        self.stage_idx = 0
        self.completed_flags.clear()
        self._stat_opened = False

    def skip(self):
        self.skipped = True
        self.active  = False

    def advance(self):
        '''Move to next stage.'''
        self.stage_idx += 1
        if self.stage_idx >= len(TUTORIAL_STAGES):
            self.active = False

    def check_completion(self, gs, event_type=None):
        '''
        Call every frame. Pass event_type for action events:
        "any_key", "cursor_at_highlight", "unit_selected", "unit_moved",
        "attack_pressed", "enemy_defeated", "heal_used", "wait_used",
        "unit_recruited", "stat_sheet_opened", "turn_ended", "chapter_seize"
        '''
        if not self.active or self.current_stage is None:
            return False
        stage = self.current_stage

        cond = stage.completion

        if cond == "any_key":
            return event_type == "any_key"

        if cond == "cursor_at_highlight" and stage.highlight_tiles:
            return (gs.cursor_x, gs.cursor_y) in stage.highlight_tiles

        if cond == "unit_selected":
            return event_type == "unit_selected"

        if cond == "unit_moved":
            return event_type == "unit_moved"

        if cond == "attack_pressed":
            return event_type == "attack_pressed"

        if cond == "enemy_defeated":
            return event_type == "enemy_defeated"

        if cond == "wait_used":
            return event_type == "wait_used"

        if cond == "heal_used":
            return event_type == "heal_used"

        if cond == "unit_recruited":
            return event_type == "unit_recruited"

        if cond == "stat_sheet_opened":
            return event_type == "stat_sheet_opened"

        if cond == "turn_ended":
            return event_type == "turn_ended"

        if cond == "chapter_seize":
            return event_type == "chapter_seize"

        return False
