"""
Game constants for Sengoku Tactics: Age of the Warring States
"""

# Screen settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
TILE_SIZE = 48
FPS = 60

# Map display
MAP_OFFSET_X = 0
MAP_OFFSET_Y = 0
UI_PANEL_WIDTH = 280

# Colors
BLACK       = (0,   0,   0)
WHITE       = (255, 255, 255)
RED         = (200, 50,  50)
GREEN       = (50,  180, 50)
BLUE        = (50,  100, 200)
YELLOW      = (230, 200, 40)
ORANGE      = (220, 130, 30)
PURPLE      = (160, 50,  200)
CYAN        = (50,  200, 220)
GREY        = (120, 120, 120)
DARK_GREY   = (60,  60,  60)
LIGHT_GREY  = (180, 180, 180)
DARK_GREEN  = (20,  100, 20)
BROWN       = (120, 70,  30)
DARK_BLUE   = (20,  40,  120)
LIGHT_BLUE  = (150, 200, 255)
CREAM       = (245, 235, 200)
GOLD        = (215, 175, 55)
DARK_RED    = (140, 20,  20)
PINK        = (230, 130, 130)
TEAL        = (20,  160, 140)
MAROON      = (100, 0,   30)

# Terrain types
TERRAIN_PLAIN    = "plain"
TERRAIN_FOREST   = "forest"
TERRAIN_MOUNTAIN = "mountain"
TERRAIN_CASTLE   = "castle"
TERRAIN_RIVER    = "river"
TERRAIN_ROAD     = "road"
TERRAIN_FORT     = "fort"
TERRAIN_VILLAGE  = "village"
TERRAIN_SEA      = "sea"
TERRAIN_CLIFF    = "cliff"
TERRAIN_BRIDGE   = "bridge"

# Terrain properties: (color, defense_bonus, avoid_bonus, move_cost, name)
TERRAIN_DATA = {
    TERRAIN_PLAIN:    {"color": (140, 195, 100), "def": 0, "avo": 0, "move": 1, "name": "Plain"},
    TERRAIN_FOREST:   {"color": (40,  120, 40),  "def": 1, "avo": 20,"move": 2, "name": "Forest"},
    TERRAIN_MOUNTAIN: {"color": (140, 120, 100), "def": 2, "avo": 30,"move": 4, "name": "Mountain"},
    TERRAIN_CASTLE:   {"color": (160, 160, 200), "def": 3, "avo": 30,"move": 1, "name": "Castle"},
    TERRAIN_RIVER:    {"color": (80,  140, 210), "def": 0, "avo": 0, "move": 5, "name": "River"},
    TERRAIN_ROAD:     {"color": (210, 190, 150), "def": 0, "avo": 0, "move": 1, "name": "Road"},
    TERRAIN_FORT:     {"color": (170, 150, 130), "def": 2, "avo": 20,"move": 1, "name": "Fort"},
    TERRAIN_VILLAGE:  {"color": (200, 175, 140), "def": 1, "avo": 10,"move": 1, "name": "Village"},
    TERRAIN_SEA:      {"color": (50,  100, 200), "def": 0, "avo": 0, "move": 99,"name": "Sea"},
    TERRAIN_CLIFF:    {"color": (100, 90,  80),  "def": 0, "avo": 0, "move": 99,"name": "Cliff"},
    TERRAIN_BRIDGE:   {"color": (190, 170, 130), "def": 0, "avo": 0, "move": 1, "name": "Bridge"},
}

# Weapon types
WEAPON_KATANA   = "katana"
WEAPON_YARI     = "yari"
WEAPON_NAGINATA = "naginata"
WEAPON_BOW      = "bow"
WEAPON_TETSUBO  = "tetsubo"
WEAPON_TANTO    = "tanto"
WEAPON_NODACHI  = "nodachi"
WEAPON_STAFF    = "staff"

# Weapon triangle advantages (attacker -> defender)
# Katana > Tanto/Nodachi, Yari > Katana, Naginata > Yari, Tetsubo neutral
WEAPON_TRIANGLE = {
    WEAPON_YARI:     {WEAPON_KATANA: +1,  WEAPON_NODACHI: +1},
    WEAPON_KATANA:   {WEAPON_NAGINATA: +1, WEAPON_TANTO: +1},
    WEAPON_NAGINATA: {WEAPON_YARI: +1,    WEAPON_TETSUBO: +1},
    WEAPON_NODACHI:  {WEAPON_NAGINATA: +1},
    WEAPON_TANTO:    {WEAPON_BOW: +1},
    WEAPON_BOW:      {},
    WEAPON_TETSUBO:  {},
    WEAPON_STAFF:    {},
}

# Unit factions
FACTION_PLAYER = "player"
FACTION_ENEMY  = "enemy"
FACTION_ALLY   = "ally"

# Unit classes
CLASS_SAMURAI    = "Samurai"
CLASS_ASHIGARU   = "Ashigaru"
CLASS_CAVALRY    = "Cavalry"
CLASS_ARCHER     = "Archer"
CLASS_NINJA      = "Ninja"
CLASS_MONK       = "Monk"
CLASS_DAIMYO     = "Daimyo"
CLASS_RONIN      = "Ronin"
CLASS_ONMYOJI    = "Onmyoji"
CLASS_BERSERKER  = "Berserker"
CLASS_SPEARMAN   = "Spearman"
CLASS_SOHEI      = "Sohei"
CLASS_KUNOICHI   = "Kunoichi"

# Class base stats: hp, str, mag, skl, spd, lck, def, res, move, weapons_allowed
CLASS_DATA = {
    CLASS_SAMURAI: {
        "hp": 32, "str": 11, "mag": 2,  "skl": 10, "spd": 9,  "lck": 5, "def": 8,  "res": 3,
        "move": 5, "weapons": [WEAPON_KATANA, WEAPON_NODACHI],
        "color": BLUE, "symbol": "S"
    },
    CLASS_ASHIGARU: {
        "hp": 28, "str": 8,  "mag": 0,  "skl": 6,  "spd": 6,  "lck": 5, "def": 6,  "res": 2,
        "move": 4, "weapons": [WEAPON_YARI, WEAPON_TETSUBO],
        "color": GREY, "symbol": "A"
    },
    CLASS_CAVALRY: {
        "hp": 30, "str": 12, "mag": 0,  "skl": 8,  "spd": 10, "lck": 5, "def": 9,  "res": 2,
        "move": 8, "weapons": [WEAPON_KATANA, WEAPON_YARI],
        "color": ORANGE, "symbol": "C"
    },
    CLASS_ARCHER: {
        "hp": 25, "str": 9,  "mag": 0,  "skl": 12, "spd": 8,  "lck": 6, "def": 5,  "res": 2,
        "move": 5, "weapons": [WEAPON_BOW],
        "color": GREEN, "symbol": "R"
    },
    CLASS_NINJA: {
        "hp": 22, "str": 10, "mag": 3,  "skl": 14, "spd": 14, "lck": 8, "def": 4,  "res": 5,
        "move": 6, "weapons": [WEAPON_TANTO, WEAPON_BOW],
        "color": DARK_GREY, "symbol": "N"
    },
    CLASS_MONK: {
        "hp": 24, "str": 5,  "mag": 12, "skl": 8,  "spd": 7,  "lck": 9, "def": 4,  "res": 10,
        "move": 5, "weapons": [WEAPON_STAFF],
        "color": YELLOW, "symbol": "M"
    },
    CLASS_DAIMYO: {
        "hp": 40, "str": 14, "mag": 4,  "skl": 12, "spd": 10, "lck": 8, "def": 12, "res": 6,
        "move": 6, "weapons": [WEAPON_KATANA, WEAPON_NODACHI, WEAPON_YARI],
        "color": GOLD, "symbol": "D"
    },
    CLASS_RONIN: {
        "hp": 28, "str": 13, "mag": 0,  "skl": 15, "spd": 12, "lck": 3, "def": 6,  "res": 2,
        "move": 5, "weapons": [WEAPON_KATANA, WEAPON_NODACHI],
        "color": MAROON, "symbol": "Ro"
    },
    CLASS_ONMYOJI: {
        "hp": 20, "str": 3,  "mag": 15, "skl": 10, "spd": 8,  "lck": 10,"def": 3,  "res": 14,
        "move": 5, "weapons": [WEAPON_STAFF],
        "color": PURPLE, "symbol": "O"
    },
    CLASS_BERSERKER: {
        "hp": 38, "str": 16, "mag": 0,  "skl": 7,  "spd": 7,  "lck": 3, "def": 10, "res": 1,
        "move": 5, "weapons": [WEAPON_TETSUBO, WEAPON_NODACHI],
        "color": RED, "symbol": "B"
    },
    CLASS_SPEARMAN: {
        "hp": 30, "str": 10, "mag": 0,  "skl": 8,  "spd": 7,  "lck": 4, "def": 8,  "res": 2,
        "move": 4, "weapons": [WEAPON_YARI, WEAPON_NAGINATA],
        "color": CYAN, "symbol": "Sp"
    },
    CLASS_SOHEI: {
        "hp": 34, "str": 12, "mag": 6,  "skl": 9,  "spd": 7,  "lck": 6, "def": 9,  "res": 8,
        "move": 5, "weapons": [WEAPON_NAGINATA, WEAPON_STAFF],
        "color": TEAL, "symbol": "So"
    },
    CLASS_KUNOICHI: {
        "hp": 20, "str": 8,  "mag": 5,  "skl": 14, "spd": 15, "lck": 10,"def": 3,  "res": 7,
        "move": 6, "weapons": [WEAPON_TANTO, WEAPON_BOW],
        "color": PINK, "symbol": "K"
    },
}

# Game states
STATE_TITLE        = "title"
STATE_CHAPTER_INTRO= "chapter_intro"
STATE_PLAYER_TURN  = "player_turn"
STATE_ENEMY_TURN   = "enemy_turn"
STATE_ALLY_TURN    = "ally_turn"
STATE_COMBAT       = "combat"
STATE_GAME_OVER    = "game_over"
STATE_VICTORY      = "victory"
STATE_MENU         = "menu"

# Cursor / selection modes
CURSOR_FREE     = "free"
CURSOR_UNIT_SEL = "unit_selected"
CURSOR_ATTACK   = "attack"
CURSOR_MOVE     = "move"

# Chapter objectives
OBJ_ROUT_ENEMY  = "rout_enemy"
OBJ_SEIZE       = "seize"
OBJ_SURVIVE     = "survive"
OBJ_DEFEAT_BOSS = "defeat_boss"
OBJ_ESCORT      = "escort"
