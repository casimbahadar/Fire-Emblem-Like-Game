"""
Skippable Tutorial System for Sengoku Tactics.
Chapter 0 — "The Way of the Warrior"
Step-by-step Fire Emblem-style tutorial with touch/keyboard support.
"""
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
    TutorialStage(
        "welcome",
        "Welcome, Commander!",
        ["Sengoku Tactics is a turn-based strategy game in the",
         "spirit of Fire Emblem. You command historical samurai",
         "officers on detailed battle maps.",
         "",
         "This tutorial will teach you the basics.",
         "If you already know Fire Emblem, press SKIP (S)."],
        completion="any_key",
        action_hint="Z/Enter or tap to continue",
    ),
    TutorialStage(
        "cursor",
        "Moving the Cursor",
        ["Use the ARROW KEYS or WASD to move the cursor.",
         "On mobile/touch: use the on-screen D-PAD (bottom-left).",
         "",
         "Move the cursor to the GOLD-HIGHLIGHTED tile."],
        highlight_tiles=[(5, 5)],
        arrow_pos=(5, 5),
        completion="cursor_at_highlight",
        action_hint="Move cursor to gold tile",
    ),
    TutorialStage(
        "select_unit",
        "Selecting a Unit",
        ["Move your cursor over a unit and press Z or ENTER.",
         "On mobile: tap the unit directly.",
         "",
         "Units show: class symbol, HP bar, and faction color.",
         "BLUE border = your unit. RED border = enemy.",
         "",
         "Select Nobunaga (gold ♦ icon) now."],
        highlight_units=["nobunaga"],
        completion="unit_selected",
        action_hint="Z/Enter or tap Nobunaga",
    ),
    TutorialStage(
        "move_unit",
        "Moving a Unit",
        ["BLUE tiles show where the unit can move.",
         "Move your unit to a highlighted tile: Z or tap it.",
         "",
         "FOREST tiles cost 2 movement. MOUNTAINS cost 4.",
         "FLYING units ignore all terrain costs — they move freely!",
         "",
         "Move Nobunaga to any blue tile."],
        completion="unit_moved",
        action_hint="Select a blue tile to move",
    ),
    TutorialStage(
        "attack",
        "Attacking Enemies",
        ["RED tiles show your attack range after moving.",
         "Press A or the ATTACK button to see targets.",
         "",
         "A COMBAT FORECAST appears showing:",
         "  Damage, Hit%, and Crit% for both sides.",
         "Press Z to confirm — X/ESC to cancel.",
         "",
         "Defeat the enemy Ashigaru!"],
        highlight_tiles=[(8, 6)],
        completion="enemy_defeated",
        action_hint="A = Attack, then Z to confirm",
    ),
    TutorialStage(
        "weapon_triangle",
        "The Weapon Triangle",
        ["Weapons have advantages over each other:",
         "  YARI (Spear) beats KATANA",
         "  KATANA beats NAGINATA",
         "  NAGINATA beats YARI",
         "",
         "GUN (Firearms) pierce through KATANA and YARI armor.",
         "BOW has extended range but cannot attack adjacent enemies.",
         "",
         "Check the COMBAT FORECAST for advantage indicators."],
        completion="any_key",
        action_hint="Z/Enter to continue",
    ),
    TutorialStage(
        "terrain",
        "Using Terrain",
        ["Terrain gives Defense and Avoid bonuses:",
         "  Plain:    No bonus",
         "  Forest:   +1 DEF, +20 AVO  (2 move cost)",
         "  Mountain: +2 DEF, +30 AVO  (4 move cost)",
         "  Fort:     +2 DEF, +20 AVO  (heals HP each turn!)",
         "  Castle:   +3 DEF, +30 AVO",
         "",
         "Position units on terrain to survive longer!"],
        highlight_tiles=[(4, 4), (4, 5), (5, 4)],
        completion="any_key",
        action_hint="Z/Enter to continue",
    ),
    TutorialStage(
        "healing",
        "Healing Allies",
        ["MONKS and NOBLE LADIES can heal allies.",
         "Select your healer, then press H or the HEAL button.",
         "Choose an adjacent ally with low HP.",
         "",
         "STAFF weapons used for healing:",
         "  Heal Staff:   Restores ~15 HP",
         "  Mend Staff:   Restores ~25 HP",
         "  Physic Staff: Heals at range (no adjacency needed)",
         "",
         "Heal Nobunaga with Nene."],
        highlight_units=["nene", "nobunaga"],
        completion="heal_used",
        action_hint="Select Nene → H → choose target",
    ),
    TutorialStage(
        "flying",
        "Flying & Mounted Units",
        ["FLYING units (purple ring) ignore ALL terrain move costs.",
         "They can cross rivers, mountains, and forests freely.",
         "However: BOW attacks deal +5 bonus damage to flyers!",
         "",
         "MOUNTED units are fast but can't enter dense forests.",
         "Cavalry: best on open plains and roads.",
         "",
         "Class types shown on the unit card (right panel)."],
        completion="any_key",
        action_hint="Z/Enter to continue",
    ),
    TutorialStage(
        "recruit",
        "Recruiting Enemies",
        ["Some enemies have a GREEN ! marker — they can join you!",
         "Move a unit ADJACENT to them, then press T (Talk).",
         "On mobile: tap the TALK button when adjacent.",
         "",
         "A recruit dialog shows the unit's bio and quote.",
         "Press Z to recruit — X to decline.",
         "",
         "The marked Ashigaru can be recruited — try it!"],
        highlight_tiles=[(6, 3)],
        completion="unit_recruited",
        action_hint="T = Talk/Recruit",
    ),
    TutorialStage(
        "stat_sheet",
        "Viewing Unit Stats",
        ["Press I (Info) or the INFO button to open a unit's",
         "full STAT SHEET. It shows:",
         "  HP, STR, MAG, SKL, SPD, LCK, DEF, RES, MOV",
         "  All weapons in inventory with details",
         "  Character bio and battle quote",
         "  EXP bar and level",
         "",
         "Press I now to view Nobunaga's stat sheet."],
        highlight_units=["nobunaga"],
        completion="stat_sheet_opened",
        action_hint="I = Info/Stat Sheet",
    ),
    TutorialStage(
        "end_turn",
        "Ending Your Turn",
        ["Once all your units have moved and acted,",
         "press SPACE or the END TURN button.",
         "",
         "Units that have acted turn darker (greyed out).",
         "You can still WAIT (W) to end a unit's turn early.",
         "",
         "After your turn: enemies move automatically.",
         "Then ALLY units act (if present).",
         "",
         "End your turn now!"],
        completion="turn_ended",
        action_hint="Space / END TURN button",
    ),
    TutorialStage(
        "seize",
        "Seizing Objectives",
        ["The GOLD-OUTLINED tile is a SEIZE point.",
         "Move your LORD unit (♦ marker) onto it and press E.",
         "On mobile: tap the SEIZE button.",
         "",
         "Other objectives include:",
         "  Rout Enemy: defeat all enemies",
         "  Defeat Boss: kill the enemy lord (♦)",
         "  Defend:     survive for N turns",
         "",
         "Move Nobunaga to the gold tile and seize it to win!"],
        highlight_tiles=[(7, 8)],
        arrow_pos=(7, 8),
        completion="chapter_seize",
        action_hint="E = Seize (stand on gold tile)",
    ),
    TutorialStage(
        "complete",
        "Tutorial Complete!",
        ["Excellent! You have mastered the basics of Sengoku Tactics.",
         "",
         "Remember:",
         "  ♦ = Lord unit — protect at all costs!",
         "  ! = Recruitable enemy — talk to them",
         "  I = Full stat sheet for any unit",
         "  T = Talk/Recruit adjacent unit",
         "  A = Attack    H = Heal    W = Wait",
         "  E = Seize     Space = End Turn",
         "",
         "Chapter 1 begins now. For the honor of Oda!"],
        completion="any_key",
        action_hint="Z/Enter to begin Chapter 1",
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
    ("e_ash1", 8, 6),   # normal enemy
    ("e_ash2", 9, 5),   # normal enemy
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
        """Move to next stage."""
        self.stage_idx += 1
        if self.stage_idx >= len(TUTORIAL_STAGES):
            self.active = False

    def check_completion(self, gs, event_type=None):
        """
        Call every frame. Pass event_type for action events:
        "any_key", "cursor_at_highlight", "unit_selected", "unit_moved",
        "enemy_defeated", "heal_used", "unit_recruited", "stat_sheet_opened",
        "turn_ended", "chapter_seize"
        """
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

        if cond == "enemy_defeated":
            return event_type == "enemy_defeated"

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
