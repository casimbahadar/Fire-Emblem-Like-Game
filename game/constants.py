'''
Game constants for Sengoku Tactics: Age of the Warring States
Inspired by Fire Emblem and Samurai Warriors
'''

# Screen settings
SCREEN_WIDTH  = 1024
SCREEN_HEIGHT = 768
TILE_SIZE     = 48
FPS           = 60

# Map area / UI
UI_PANEL_WIDTH = 290

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
SILVER      = (192, 192, 210)
CRIMSON     = (180, 20,  50)
INDIGO      = (60,  30,  130)
SAGE        = (140, 170, 120)
IVORY       = (240, 235, 215)
COPPER      = (180, 100, 50)
SLATE       = (80,  90,  110)
SCARLET     = (210, 40,  40)
EMERALD     = (30,  160, 80)
VIOLET      = (140, 60,  180)
AMBER       = (200, 150, 30)

# ─── Terrain types ────────────────────────────────────────────────────────────
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
TERRAIN_RUINS    = "ruins"
TERRAIN_DESERT   = "desert"
TERRAIN_PEAK     = "peak"
TERRAIN_THICKET  = "thicket"
TERRAIN_GATE     = "gate"

# Terrain properties: color, def bonus, avoid bonus, move cost, name
TERRAIN_DATA = {
    TERRAIN_PLAIN:    {"color": (140, 195, 100), "def": 0, "avo": 0,  "move": 1, "name": "Plain"},
    TERRAIN_FOREST:   {"color": (40,  120, 40),  "def": 1, "avo": 20, "move": 2, "name": "Forest"},
    TERRAIN_MOUNTAIN: {"color": (140, 120, 100), "def": 2, "avo": 30, "move": 4, "name": "Mountain"},
    TERRAIN_CASTLE:   {"color": (160, 160, 200), "def": 3, "avo": 30, "move": 1, "name": "Castle"},
    TERRAIN_RIVER:    {"color": (80,  140, 210), "def": 0, "avo": 0,  "move": 5, "name": "River"},
    TERRAIN_ROAD:     {"color": (210, 190, 150), "def": 0, "avo": 0,  "move": 1, "name": "Road"},
    TERRAIN_FORT:     {"color": (170, 150, 130), "def": 2, "avo": 20, "move": 1, "name": "Fort"},
    TERRAIN_VILLAGE:  {"color": (200, 175, 140), "def": 1, "avo": 10, "move": 1, "name": "Village"},
    TERRAIN_SEA:      {"color": (50,  100, 200), "def": 0, "avo": 0,  "move": 99,"name": "Sea"},
    TERRAIN_CLIFF:    {"color": (100, 90,  80),  "def": 0, "avo": 0,  "move": 99,"name": "Cliff"},
    TERRAIN_BRIDGE:   {"color": (190, 170, 130), "def": 0, "avo": 0,  "move": 1, "name": "Bridge"},
    TERRAIN_RUINS:    {"color": (130, 115, 100), "def": 1, "avo": 10, "move": 2, "name": "Ruins"},
    TERRAIN_DESERT:   {"color": (210, 195, 140), "def": 0, "avo": 0,  "move": 3, "name": "Desert"},
    TERRAIN_PEAK:     {"color": (120, 100, 90),  "def": 3, "avo": 40, "move": 99,"name": "Peak"},
    TERRAIN_THICKET:  {"color": (60,  100, 50),  "def": 1, "avo": 30, "move": 3, "name": "Thicket"},
    TERRAIN_GATE:     {"color": (150, 140, 170), "def": 4, "avo": 30, "move": 1, "name": "Gate"},
}

# ─── Weapon types ─────────────────────────────────────────────────────────────
WEAPON_KATANA   = "katana"
WEAPON_YARI     = "yari"
WEAPON_NAGINATA = "naginata"
WEAPON_BOW      = "bow"
WEAPON_TETSUBO  = "tetsubo"
WEAPON_TANTO    = "tanto"
WEAPON_NODACHI  = "nodachi"
WEAPON_STAFF    = "staff"
WEAPON_GUN      = "gun"        # Tanegashima / matchlock
WEAPON_CHAIN    = "chain"      # Kusarigama chain-sickle

# Weapon triangle (attacker type → {defender type: +1 advantage})
WEAPON_TRIANGLE = {
    WEAPON_YARI:     {WEAPON_KATANA: +1,    WEAPON_NODACHI: +1},
    WEAPON_KATANA:   {WEAPON_NAGINATA: +1,  WEAPON_TANTO: +1},
    WEAPON_NAGINATA: {WEAPON_YARI: +1,      WEAPON_TETSUBO: +1},
    WEAPON_NODACHI:  {WEAPON_NAGINATA: +1},
    WEAPON_TANTO:    {WEAPON_BOW: +1},
    WEAPON_BOW:      {WEAPON_GUN: +1},       # archers outrun gun reload
    WEAPON_GUN:      {WEAPON_KATANA: +1,    WEAPON_YARI: +1},  # guns pierce armor
    WEAPON_CHAIN:    {WEAPON_KATANA: +1,    WEAPON_YARI: +1},
    WEAPON_TETSUBO:  {},
    WEAPON_STAFF:    {},
}

# ─── Unit factions ────────────────────────────────────────────────────────────
FACTION_PLAYER = "player"
FACTION_ENEMY  = "enemy"
FACTION_ALLY   = "ally"

# ─── Unit classes ─────────────────────────────────────────────────────────────
# Original
CLASS_SAMURAI        = "Samurai"
CLASS_ASHIGARU       = "Ashigaru"
CLASS_CAVALRY        = "Cavalry"
CLASS_ARCHER         = "Archer"
CLASS_NINJA          = "Ninja"
CLASS_MONK           = "Monk"
CLASS_DAIMYO         = "Daimyo"
CLASS_RONIN          = "Ronin"
CLASS_ONMYOJI        = "Onmyoji"
CLASS_BERSERKER      = "Berserker"
CLASS_SPEARMAN       = "Spearman"
CLASS_SOHEI          = "Sohei"
CLASS_KUNOICHI       = "Kunoichi"
# New
CLASS_PEGASUS_KNIGHT = "Pegasus Knight"   # Flying
CLASS_WYVERN_KNIGHT  = "Wyvern Knight"    # Flying (heavy)
CLASS_GENERAL        = "General"           # Heavy armored foot
CLASS_HATAMOTO       = "Hatamoto"          # Elite mounted samurai
CLASS_MOUNTED_ARCHER = "Mounted Archer"    # Cavalry + bow
CLASS_GUNNER         = "Gunner"            # Firearms
CLASS_PIRATE         = "Pirate"            # Can cross water
CLASS_TACTICIAN      = "Tactician"         # Magic support
CLASS_NOBLE_LADY     = "Noble Lady"        # Unique support class
CLASS_KUSARIGAMA     = "Kusarigama"        # Chain-sickle fighter
# ── Additional Flying Classes ──────────────────────────────────────────────────
CLASS_FALCON_KNIGHT  = "Falcon Knight"    # Promoted Pegasus — fastest healer/attacker
CLASS_EAGLE_ARCHER   = "Eagle Archer"     # Flying bow unit — anti-flyer specialist
CLASS_STORM_RIDER    = "Storm Rider"      # Ultra-fast dual-blade sky assassin
CLASS_TENGU_MASTER   = "Tengu Master"     # Ninja-style magic flyer
CLASS_SKY_LANCER     = "Sky Lancer"       # Heavy armored flying spearman
CLASS_DRAGON_KNIGHT  = "Dragon Knight"    # Mounted on war-dragon — supreme flyer
# ── Magical classes (12 new) ──────────────────────────────────────────────────
CLASS_SPIRIT_DANCER  = "Spirit Dancer"    # Flying — offensive wind/spirit magic
CLASS_KITSUNE_SAGE   = "Kitsune Sage"     # Flying — fox-spirit illusionist
CLASS_VOID_PROPHET   = "Void Prophet"     # Foot — dark curse caster, AoE debuffer
CLASS_SHRINE_ORACLE  = "Shrine Oracle"    # Foot — light healing + barrier magic
CLASS_CELESTIAL_MONK = "Celestial Monk"   # Foot — promoted Monk, strongest healer
CLASS_JADE_SORCERESS = "Jade Sorceress"   # Foot — high magic offensive, fragile
CLASS_THUNDER_SHAMAN = "Thunder Shaman"   # Mounted — lightning magic on horseback
CLASS_BLOOD_ASCETIC  = "Blood Ascetic"    # Foot — sacrifices HP to deal magic damage
CLASS_MOON_RIDER     = "Moon Rider"       # Flying — lunar magic + naginata, fast
CLASS_PHANTOM_KNIGHT = "Phantom Knight"   # Mounted — cursed cavalry, magic + melee
CLASS_STAR_DANCER    = "Star Dancer"      # Flying — offensive celestial magic
CLASS_DEATH_ORACLE   = "Death Oracle"     # Foot — ultimate dark mage, frail glass cannon
# ── Additional Mounted Classes ─────────────────────────────────────────────────
CLASS_LANCE_CAVALRY  = "Lance Cavalry"    # Spear-specialist cavalry
CLASS_WAR_ELEPHANT   = "War Elephant"     # Massive, slow, devastating (Korean/Ming)
CLASS_LIGHT_CAVALRY  = "Light Cavalry"    # Scout — blazing speed, low attack
CLASS_GREAT_KNIGHT   = "Great Knight"     # Heavy armored cavalry, powerful but slow
CLASS_NOBLE_CAVALRY  = "Noble Cavalry"    # Lord cavalry — high all-around stats
# ── New Unpromoted Classes (15) ────────────────────────────────────────────────
CLASS_SHIRABYOSHI    = "Shirabyoshi"     # Dancer/refresher — grants ally extra action
CLASS_YAMABUSHI      = "Yamabushi"       # Mountain ascetic warrior-monk
CLASS_MIKO           = "Miko"           # Shrine maiden healer-mage
CLASS_NOMAD          = "Nomad"          # Light mounted archer-scout
CLASS_FOOT_GUARD     = "Foot Guard"     # Shield-bearing armored foot soldier
CLASS_MERCHANT       = "Merchant"       # Trade/item specialist support
CLASS_MUSHA          = "Musha"          # Traveling warrior — versatile fighter
CLASS_YOJIMBO        = "Yojimbo"        # Mercenary bodyguard swordsman
CLASS_WATER_WITCH    = "Water Witch"    # Water/ice elemental mage
CLASS_FIRE_ACOLYTE   = "Fire Acolyte"   # Fire elemental attacker
CLASS_BLADE_MONK     = "Blade Monk"     # Offensive sword-wielding monk
CLASS_ROGUE          = "Rogue"          # Outlaw/thief scout
CLASS_COURT_NOBLE    = "Court Noble"    # Aristocratic tactical support
CLASS_SEA_SOLDIER    = "Sea Soldier"    # Naval foot warrior — water-capable
CLASS_KENIN          = "Kenin"          # Young retainer/squire — trainee warrior
# ── New Promoted Classes (4) ───────────────────────────────────────────────────
CLASS_SWORD_SAINT    = "Sword Saint"    # Supreme swordmaster (promoted Ronin/Musha/Yojimbo)
CLASS_VALKYRIE       = "Valkyrie"       # Mounted healer-mage (promoted Noble Lady/Miko)
CLASS_GREAT_GENERAL  = "Great General"  # Ultimate armored foot (promoted General/Foot Guard)
CLASS_WARLORD        = "Warlord"        # Military overlord (promoted Berserker/Fire Acolyte)
# ── Game States ────────────────────────────────────────────────────────────────
STATE_BOSS_DIALOG    = "boss_dialog"
STATE_TUTORIAL       = "tutorial"

# Flying & mounted sets (for movement rules)
FLYING_CLASSES  = {CLASS_PEGASUS_KNIGHT, CLASS_WYVERN_KNIGHT, CLASS_FALCON_KNIGHT,
                   CLASS_EAGLE_ARCHER, CLASS_STORM_RIDER, CLASS_TENGU_MASTER,
                   CLASS_SKY_LANCER, CLASS_DRAGON_KNIGHT,
                   # Magical flying
                   CLASS_SPIRIT_DANCER, CLASS_KITSUNE_SAGE, CLASS_MOON_RIDER,
                   CLASS_STAR_DANCER}
MOUNTED_CLASSES = {CLASS_CAVALRY, CLASS_HATAMOTO, CLASS_MOUNTED_ARCHER,
                   CLASS_LANCE_CAVALRY, CLASS_LIGHT_CAVALRY, CLASS_GREAT_KNIGHT,
                   CLASS_NOBLE_CAVALRY,
                   # Magical mounted
                   CLASS_THUNDER_SHAMAN, CLASS_PHANTOM_KNIGHT,
                   # New mounted
                   CLASS_NOMAD, CLASS_VALKYRIE}
WATER_CLASSES   = {CLASS_PIRATE, CLASS_SEA_SOLDIER}   # Can traverse rivers/sea at normal cost

# Promotion level threshold (like Fire Emblem GBA)
PROMOTION_LEVEL = 10

# Classes that are "promoted" tier (cannot be promoted further; entered via promotion or join promoted)
PROMOTED_CLASSES = {
    CLASS_RONIN, CLASS_GENERAL, CLASS_HATAMOTO, CLASS_MOUNTED_ARCHER,
    CLASS_FALCON_KNIGHT, CLASS_EAGLE_ARCHER, CLASS_STORM_RIDER, CLASS_TENGU_MASTER,
    CLASS_SKY_LANCER, CLASS_DRAGON_KNIGHT, CLASS_LANCE_CAVALRY, CLASS_WAR_ELEPHANT,
    CLASS_GREAT_KNIGHT, CLASS_NOBLE_CAVALRY,
    # Magical promoted
    CLASS_SPIRIT_DANCER, CLASS_KITSUNE_SAGE, CLASS_VOID_PROPHET, CLASS_SHRINE_ORACLE,
    CLASS_CELESTIAL_MONK, CLASS_JADE_SORCERESS, CLASS_THUNDER_SHAMAN, CLASS_BLOOD_ASCETIC,
    CLASS_MOON_RIDER, CLASS_PHANTOM_KNIGHT, CLASS_STAR_DANCER, CLASS_DEATH_ORACLE,
    # New promoted
    CLASS_SWORD_SAINT, CLASS_VALKYRIE, CLASS_GREAT_GENERAL, CLASS_WARLORD,
    # Lord class — never promotes
    CLASS_DAIMYO,
}

# Promotion options: unpromoted class → list of promoted classes player can choose
PROMOTION_CHAINS = {
    CLASS_SAMURAI:        [CLASS_RONIN, CLASS_HATAMOTO],
    CLASS_ASHIGARU:       [CLASS_SPEARMAN, CLASS_GENERAL],
    CLASS_SPEARMAN:       [CLASS_GENERAL, CLASS_SKY_LANCER],
    CLASS_CAVALRY:        [CLASS_GREAT_KNIGHT, CLASS_NOBLE_CAVALRY, CLASS_LANCE_CAVALRY, CLASS_PHANTOM_KNIGHT],
    CLASS_ARCHER:         [CLASS_MOUNTED_ARCHER, CLASS_EAGLE_ARCHER],
    CLASS_NINJA:          [CLASS_STORM_RIDER, CLASS_TENGU_MASTER],
    CLASS_KUNOICHI:       [CLASS_STORM_RIDER, CLASS_KITSUNE_SAGE],
    CLASS_MONK:           [CLASS_CELESTIAL_MONK, CLASS_SHRINE_ORACLE],
    CLASS_ONMYOJI:        [CLASS_VOID_PROPHET, CLASS_JADE_SORCERESS, CLASS_DEATH_ORACLE],
    CLASS_BERSERKER:      [CLASS_WAR_ELEPHANT, CLASS_WARLORD],
    CLASS_SOHEI:          [CLASS_CELESTIAL_MONK, CLASS_BLOOD_ASCETIC],
    CLASS_PEGASUS_KNIGHT: [CLASS_FALCON_KNIGHT, CLASS_MOON_RIDER, CLASS_SPIRIT_DANCER],
    CLASS_WYVERN_KNIGHT:  [CLASS_DRAGON_KNIGHT, CLASS_SKY_LANCER],
    CLASS_TACTICIAN:      [CLASS_THUNDER_SHAMAN, CLASS_PHANTOM_KNIGHT],
    CLASS_NOBLE_LADY:     [CLASS_SHRINE_ORACLE, CLASS_STAR_DANCER, CLASS_VALKYRIE],
    CLASS_KUSARIGAMA:     [CLASS_TENGU_MASTER, CLASS_STORM_RIDER],
    CLASS_PIRATE:         [CLASS_LANCE_CAVALRY, CLASS_NOBLE_CAVALRY],
    CLASS_GUNNER:         [CLASS_MOUNTED_ARCHER, CLASS_LIGHT_CAVALRY],
    CLASS_LIGHT_CAVALRY:  [CLASS_HATAMOTO, CLASS_NOBLE_CAVALRY],
    # New unpromoted
    CLASS_SHIRABYOSHI:    [CLASS_STAR_DANCER, CLASS_KITSUNE_SAGE],
    CLASS_YAMABUSHI:      [CLASS_TENGU_MASTER, CLASS_CELESTIAL_MONK],
    CLASS_MIKO:           [CLASS_SHRINE_ORACLE, CLASS_SPIRIT_DANCER],
    CLASS_NOMAD:          [CLASS_MOUNTED_ARCHER, CLASS_LIGHT_CAVALRY],
    CLASS_FOOT_GUARD:     [CLASS_GENERAL, CLASS_GREAT_KNIGHT],
    CLASS_MERCHANT:       [CLASS_TACTICIAN, CLASS_PIRATE],
    CLASS_MUSHA:          [CLASS_RONIN, CLASS_HATAMOTO],
    CLASS_YOJIMBO:        [CLASS_RONIN, CLASS_SWORD_SAINT],
    CLASS_WATER_WITCH:    [CLASS_VOID_PROPHET, CLASS_MOON_RIDER],
    CLASS_FIRE_ACOLYTE:   [CLASS_THUNDER_SHAMAN, CLASS_BLOOD_ASCETIC],
    CLASS_BLADE_MONK:     [CLASS_CELESTIAL_MONK, CLASS_SWORD_SAINT],
    CLASS_ROGUE:          [CLASS_NINJA, CLASS_KUSARIGAMA],
    CLASS_COURT_NOBLE:    [CLASS_TACTICIAN, CLASS_NOBLE_CAVALRY],
    CLASS_SEA_SOLDIER:    [CLASS_PIRATE, CLASS_LANCE_CAVALRY],
    CLASS_KENIN:          [CLASS_SAMURAI, CLASS_CAVALRY],
}

# Stat bonuses granted on promotion (added on top of current stats)
PROMOTION_BONUSES = {
    # To Ronin / Sword Saint
    CLASS_RONIN:          {"hp": 3, "str": 3, "mag": 0, "skl": 3, "spd": 3, "lck": 1, "def": 2, "res": 1, "move": 0},
    CLASS_SWORD_SAINT:    {"hp": 4, "str": 4, "mag": 1, "skl": 4, "spd": 4, "lck": 2, "def": 2, "res": 2, "move": 1},
    # To General / Great General
    CLASS_GENERAL:        {"hp": 5, "str": 2, "mag": 0, "skl": 2, "spd": 1, "lck": 1, "def": 5, "res": 2, "move": 0},
    CLASS_GREAT_GENERAL:  {"hp": 6, "str": 3, "mag": 0, "skl": 2, "spd": 1, "lck": 1, "def": 6, "res": 3, "move": 0},
    # To Hatamoto
    CLASS_HATAMOTO:       {"hp": 3, "str": 3, "mag": 0, "skl": 2, "spd": 2, "lck": 2, "def": 3, "res": 1, "move": 2},
    # To Mounted Archer
    CLASS_MOUNTED_ARCHER: {"hp": 2, "str": 2, "mag": 0, "skl": 3, "spd": 3, "lck": 2, "def": 2, "res": 1, "move": 2},
    # To Falcon Knight
    CLASS_FALCON_KNIGHT:  {"hp": 2, "str": 2, "mag": 2, "skl": 2, "spd": 3, "lck": 2, "def": 2, "res": 3, "move": 1},
    # To Eagle Archer
    CLASS_EAGLE_ARCHER:   {"hp": 2, "str": 1, "mag": 1, "skl": 4, "spd": 3, "lck": 2, "def": 1, "res": 2, "move": 2},
    # To Storm Rider
    CLASS_STORM_RIDER:    {"hp": 2, "str": 3, "mag": 1, "skl": 4, "spd": 4, "lck": 2, "def": 1, "res": 2, "move": 2},
    # To Tengu Master
    CLASS_TENGU_MASTER:   {"hp": 2, "str": 1, "mag": 4, "skl": 2, "spd": 3, "lck": 2, "def": 1, "res": 4, "move": 1},
    # To Sky Lancer
    CLASS_SKY_LANCER:     {"hp": 3, "str": 4, "mag": 0, "skl": 2, "spd": 2, "lck": 1, "def": 4, "res": 1, "move": 1},
    # To Dragon Knight
    CLASS_DRAGON_KNIGHT:  {"hp": 4, "str": 4, "mag": 1, "skl": 2, "spd": 1, "lck": 1, "def": 4, "res": 2, "move": 1},
    # To Great Knight
    CLASS_GREAT_KNIGHT:   {"hp": 4, "str": 3, "mag": 0, "skl": 2, "spd": 1, "lck": 1, "def": 5, "res": 2, "move": 1},
    # To Noble Cavalry
    CLASS_NOBLE_CAVALRY:  {"hp": 3, "str": 2, "mag": 2, "skl": 2, "spd": 2, "lck": 3, "def": 3, "res": 3, "move": 2},
    # To Lance Cavalry
    CLASS_LANCE_CAVALRY:  {"hp": 3, "str": 3, "mag": 0, "skl": 2, "spd": 2, "lck": 1, "def": 3, "res": 1, "move": 2},
    # To War Elephant
    CLASS_WAR_ELEPHANT:   {"hp": 8, "str": 5, "mag": 0, "skl": 1, "spd": 0, "lck": 0, "def": 6, "res": 1, "move": 0},
    # To Light Cavalry
    CLASS_LIGHT_CAVALRY:  {"hp": 2, "str": 1, "mag": 0, "skl": 2, "spd": 4, "lck": 2, "def": 1, "res": 1, "move": 2},
    # Magical promoted
    CLASS_SPIRIT_DANCER:  {"hp": 2, "str": 1, "mag": 4, "skl": 2, "spd": 4, "lck": 3, "def": 1, "res": 4, "move": 1},
    CLASS_KITSUNE_SAGE:   {"hp": 2, "str": 1, "mag": 5, "skl": 2, "spd": 3, "lck": 4, "def": 1, "res": 5, "move": 0},
    CLASS_VOID_PROPHET:   {"hp": 3, "str": 0, "mag": 4, "skl": 2, "spd": 1, "lck": 1, "def": 1, "res": 4, "move": 0},
    CLASS_SHRINE_ORACLE:  {"hp": 3, "str": 1, "mag": 3, "skl": 2, "spd": 2, "lck": 4, "def": 2, "res": 5, "move": 0},
    CLASS_CELESTIAL_MONK: {"hp": 4, "str": 2, "mag": 4, "skl": 2, "spd": 2, "lck": 3, "def": 3, "res": 6, "move": 0},
    CLASS_JADE_SORCERESS: {"hp": 2, "str": 0, "mag": 6, "skl": 3, "spd": 2, "lck": 2, "def": 0, "res": 4, "move": 0},
    CLASS_THUNDER_SHAMAN: {"hp": 3, "str": 2, "mag": 4, "skl": 2, "spd": 2, "lck": 1, "def": 2, "res": 3, "move": 2},
    CLASS_BLOOD_ASCETIC:  {"hp": 4, "str": 1, "mag": 4, "skl": 1, "spd": 1, "lck": 0, "def": 1, "res": 2, "move": 0},
    CLASS_MOON_RIDER:     {"hp": 3, "str": 2, "mag": 3, "skl": 2, "spd": 3, "lck": 2, "def": 2, "res": 3, "move": 1},
    CLASS_PHANTOM_KNIGHT: {"hp": 3, "str": 3, "mag": 3, "skl": 2, "spd": 2, "lck": 1, "def": 3, "res": 3, "move": 2},
    CLASS_STAR_DANCER:    {"hp": 2, "str": 1, "mag": 5, "skl": 2, "spd": 4, "lck": 3, "def": 1, "res": 4, "move": 2},
    CLASS_DEATH_ORACLE:   {"hp": 2, "str": 0, "mag": 6, "skl": 3, "spd": 1, "lck": 0, "def": 0, "res": 3, "move": 0},
    # New promoted
    CLASS_VALKYRIE:       {"hp": 3, "str": 1, "mag": 4, "skl": 2, "spd": 2, "lck": 3, "def": 2, "res": 5, "move": 2},
    CLASS_WARLORD:        {"hp": 5, "str": 4, "mag": 1, "skl": 2, "spd": 2, "lck": 1, "def": 3, "res": 1, "move": 0},
    # Spearman (promoted from Ashigaru)
    CLASS_SPEARMAN:       {"hp": 3, "str": 2, "mag": 0, "skl": 2, "spd": 2, "lck": 1, "def": 2, "res": 1, "move": 0},
    # Pirate (promoted from Sea Soldier/Merchant)
    CLASS_PIRATE:         {"hp": 3, "str": 2, "mag": 0, "skl": 2, "spd": 2, "lck": 2, "def": 1, "res": 1, "move": 0},
    # Ninja (promoted from Rogue)
    CLASS_NINJA:          {"hp": 2, "str": 2, "mag": 1, "skl": 3, "spd": 3, "lck": 2, "def": 1, "res": 1, "move": 1},
    # Kusarigama (promoted from Rogue)
    CLASS_KUSARIGAMA:     {"hp": 2, "str": 2, "mag": 1, "skl": 4, "spd": 3, "lck": 2, "def": 1, "res": 2, "move": 0},
    # Samurai / Cavalry (promoted from Kenin)
    CLASS_SAMURAI:        {"hp": 3, "str": 2, "mag": 0, "skl": 2, "spd": 2, "lck": 1, "def": 2, "res": 1, "move": 0},
    CLASS_CAVALRY:        {"hp": 3, "str": 3, "mag": 0, "skl": 2, "spd": 2, "lck": 1, "def": 2, "res": 1, "move": 2},
    # Tactician (promoted from Merchant/Court Noble)
    CLASS_TACTICIAN:      {"hp": 2, "str": 1, "mag": 3, "skl": 2, "spd": 2, "lck": 2, "def": 1, "res": 3, "move": 0},
}

# Class base stats: hp, str, mag, skl, spd, lck, def, res, move, weapons_allowed, color, symbol
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
        "color": ORANGE, "symbol": "Cv"
    },
    CLASS_ARCHER: {
        "hp": 25, "str": 9,  "mag": 0,  "skl": 12, "spd": 8,  "lck": 6, "def": 5,  "res": 2,
        "move": 5, "weapons": [WEAPON_BOW],
        "color": GREEN, "symbol": "Ar"
    },
    CLASS_NINJA: {
        "hp": 22, "str": 10, "mag": 3,  "skl": 14, "spd": 14, "lck": 8, "def": 4,  "res": 5,
        "move": 6, "weapons": [WEAPON_TANTO, WEAPON_BOW],
        "color": DARK_GREY, "symbol": "N"
    },
    CLASS_MONK: {
        "hp": 24, "str": 5,  "mag": 12, "skl": 8,  "spd": 7,  "lck": 9, "def": 4,  "res": 10,
        "move": 5, "weapons": [WEAPON_STAFF],
        "color": YELLOW, "symbol": "Mo"
    },
    CLASS_DAIMYO: {
        "hp": 40, "str": 14, "mag": 4,  "skl": 12, "spd": 10, "lck": 8, "def": 12, "res": 6,
        "move": 6, "weapons": [WEAPON_KATANA, WEAPON_NODACHI, WEAPON_YARI],
        "color": GOLD, "symbol": "Da"
    },
    CLASS_RONIN: {
        "hp": 28, "str": 13, "mag": 0,  "skl": 15, "spd": 12, "lck": 3, "def": 6,  "res": 2,
        "move": 5, "weapons": [WEAPON_KATANA, WEAPON_NODACHI],
        "color": MAROON, "symbol": "Ro"
    },
    CLASS_ONMYOJI: {
        "hp": 20, "str": 3,  "mag": 15, "skl": 10, "spd": 8,  "lck": 10,"def": 3,  "res": 14,
        "move": 5, "weapons": [WEAPON_STAFF],
        "color": PURPLE, "symbol": "On"
    },
    CLASS_BERSERKER: {
        "hp": 38, "str": 16, "mag": 0,  "skl": 7,  "spd": 7,  "lck": 3, "def": 10, "res": 1,
        "move": 5, "weapons": [WEAPON_TETSUBO, WEAPON_NODACHI],
        "color": RED, "symbol": "Be"
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
        "color": PINK, "symbol": "Ku"
    },
    # ── New classes ────────────────────────────────────────────────────────────
    CLASS_PEGASUS_KNIGHT: {
        "hp": 24, "str": 10, "mag": 6,  "skl": 13, "spd": 14, "lck": 9, "def": 5,  "res": 10,
        "move": 7, "weapons": [WEAPON_NAGINATA, WEAPON_STAFF],
        "color": (200, 180, 255), "symbol": "Pg",
        "flying": True
    },
    CLASS_WYVERN_KNIGHT: {
        "hp": 34, "str": 15, "mag": 0,  "skl": 10, "spd": 9,  "lck": 4, "def": 13, "res": 4,
        "move": 7, "weapons": [WEAPON_YARI, WEAPON_KATANA],
        "color": (160, 80, 40), "symbol": "Wy",
        "flying": True
    },
    CLASS_GENERAL: {
        "hp": 46, "str": 13, "mag": 0,  "skl": 8,  "spd": 5,  "lck": 4, "def": 18, "res": 6,
        "move": 4, "weapons": [WEAPON_YARI, WEAPON_TETSUBO, WEAPON_NAGINATA],
        "color": SILVER, "symbol": "Gn"
    },
    CLASS_HATAMOTO: {
        "hp": 34, "str": 14, "mag": 0,  "skl": 12, "spd": 11, "lck": 6, "def": 11, "res": 4,
        "move": 8, "weapons": [WEAPON_KATANA, WEAPON_NODACHI, WEAPON_YARI],
        "color": COPPER, "symbol": "Ha",
        "mounted": True
    },
    CLASS_MOUNTED_ARCHER: {
        "hp": 26, "str": 10, "mag": 0,  "skl": 13, "spd": 12, "lck": 6, "def": 7,  "res": 3,
        "move": 7, "weapons": [WEAPON_BOW, WEAPON_KATANA],
        "color": SAGE, "symbol": "MA",
        "mounted": True
    },
    CLASS_GUNNER: {
        "hp": 26, "str": 11, "mag": 2,  "skl": 10, "spd": 6,  "lck": 5, "def": 6,  "res": 3,
        "move": 4, "weapons": [WEAPON_GUN, WEAPON_TANTO],
        "color": SLATE, "symbol": "Gu"
    },
    CLASS_PIRATE: {
        "hp": 30, "str": 12, "mag": 0,  "skl": 8,  "spd": 10, "lck": 6, "def": 7,  "res": 4,
        "move": 5, "weapons": [WEAPON_KATANA, WEAPON_NODACHI],
        "color": INDIGO, "symbol": "Pi",
        "water_walk": True
    },
    CLASS_TACTICIAN: {
        "hp": 22, "str": 4,  "mag": 14, "skl": 12, "spd": 9,  "lck": 8, "def": 4,  "res": 12,
        "move": 5, "weapons": [WEAPON_STAFF, WEAPON_TANTO],
        "color": VIOLET, "symbol": "Ta"
    },
    CLASS_NOBLE_LADY: {
        "hp": 20, "str": 5,  "mag": 10, "skl": 10, "spd": 11, "lck": 14,"def": 3,  "res": 12,
        "move": 5, "weapons": [WEAPON_STAFF, WEAPON_BOW],
        "color": (240, 160, 200), "symbol": "NL"
    },
    CLASS_KUSARIGAMA: {
        "hp": 24, "str": 11, "mag": 4,  "skl": 15, "spd": 13, "lck": 7, "def": 5,  "res": 6,
        "move": 5, "weapons": [WEAPON_CHAIN, WEAPON_TANTO],
        "color": (80, 60, 100), "symbol": "Ks"
    },
    # ── Additional Flying Classes ─────────────────────────────────────────────
    CLASS_FALCON_KNIGHT: {
        "hp": 26, "str": 12, "mag": 8,  "skl": 15, "spd": 17, "lck": 11,"def": 7,  "res": 12,
        "move": 8, "weapons": [WEAPON_NAGINATA, WEAPON_STAFF],
        "color": (220, 200, 255), "symbol": "FK",
        "flying": True,
        "description": "Promoted Pegasus. Fastest flyer. Healer and attacker combined."
    },
    CLASS_EAGLE_ARCHER: {
        "hp": 22, "str": 10, "mag": 2,  "skl": 16, "spd": 14, "lck": 9, "def": 6,  "res": 8,
        "move": 7, "weapons": [WEAPON_BOW],
        "color": (180, 220, 160), "symbol": "EA",
        "flying": True,
        "description": "Rides a giant war eagle. Bow specialist — deadly vs other flyers."
    },
    CLASS_STORM_RIDER: {
        "hp": 20, "str": 14, "mag": 5,  "skl": 17, "spd": 19, "lck": 10,"def": 5,  "res": 7,
        "move": 8, "weapons": [WEAPON_TANTO, WEAPON_KATANA],
        "color": (160, 210, 255), "symbol": "SR",
        "flying": True,
        "description": "Lightning-fast aerial duelist. The fastest unit in the army."
    },
    CLASS_TENGU_MASTER: {
        "hp": 22, "str": 8,  "mag": 14, "skl": 14, "spd": 14, "lck": 12,"def": 5,  "res": 14,
        "move": 7, "weapons": [WEAPON_TANTO, WEAPON_STAFF],
        "color": (100, 60, 160), "symbol": "TM",
        "flying": True,
        "description": "Supernatural ninja-monk of the mountain. Magic and blade in sky."
    },
    CLASS_SKY_LANCER: {
        "hp": 32, "str": 16, "mag": 0,  "skl": 11, "spd": 10, "lck": 5, "def": 14, "res": 5,
        "move": 6, "weapons": [WEAPON_YARI, WEAPON_NAGINATA],
        "color": (180, 120, 60), "symbol": "SL",
        "flying": True,
        "description": "Heavily armored flying lancer. Slower but nearly unstoppable."
    },
    CLASS_DRAGON_KNIGHT: {
        "hp": 40, "str": 18, "mag": 4,  "skl": 12, "spd": 8,  "lck": 4, "def": 16, "res": 6,
        "move": 6, "weapons": [WEAPON_YARI, WEAPON_NODACHI, WEAPON_KATANA],
        "color": (200, 80, 30), "symbol": "DK",
        "flying": True,
        "description": "Mounts a fearsome war-dragon. The pinnacle of flying power."
    },
    # ── Additional Mounted Classes ────────────────────────────────────────────
    CLASS_LANCE_CAVALRY: {
        "hp": 30, "str": 13, "mag": 0,  "skl": 9,  "spd": 11, "lck": 5, "def": 10, "res": 2,
        "move": 8, "weapons": [WEAPON_YARI, WEAPON_NAGINATA],
        "color": (220, 140, 60), "symbol": "LC",
        "mounted": True,
        "description": "Spear-mounted cavalry. Strong anti-infantry charge specialists."
    },
    CLASS_WAR_ELEPHANT: {
        "hp": 56, "str": 20, "mag": 0,  "skl": 5,  "spd": 4,  "lck": 3, "def": 18, "res": 4,
        "move": 4, "weapons": [WEAPON_TETSUBO, WEAPON_YARI],
        "color": (100, 80, 60), "symbol": "WE",
        "mounted": True,
        "description": "Korean/Ming war elephant. Mountainous HP and DEF. Extremely slow."
    },
    CLASS_LIGHT_CAVALRY: {
        "hp": 24, "str": 9,  "mag": 0,  "skl": 10, "spd": 15, "lck": 8, "def": 6,  "res": 3,
        "move": 9, "weapons": [WEAPON_TANTO, WEAPON_BOW],
        "color": (200, 200, 120), "symbol": "LtC",
        "mounted": True,
        "description": "Scout cavalry. Blinding speed but limited combat power."
    },
    CLASS_GREAT_KNIGHT: {
        "hp": 38, "str": 15, "mag": 0,  "skl": 9,  "spd": 7,  "lck": 4, "def": 17, "res": 6,
        "move": 6, "weapons": [WEAPON_KATANA, WEAPON_YARI, WEAPON_TETSUBO],
        "color": (140, 140, 180), "symbol": "GK",
        "mounted": True,
        "description": "Full-plate armored cavalry. Immense defense. Can't enter forests."
    },
    CLASS_NOBLE_CAVALRY: {
        "hp": 36, "str": 14, "mag": 5,  "skl": 12, "spd": 12, "lck": 10,"def": 12, "res": 8,
        "move": 8, "weapons": [WEAPON_KATANA, WEAPON_NODACHI, WEAPON_YARI],
        "color": (220, 200, 80), "symbol": "NC",
        "mounted": True,
        "description": "Lord-class cavalry. Balanced, fast, and commanding on horseback."
    },
    # ── Magical Classes ───────────────────────────────────────────────────────
    CLASS_SPIRIT_DANCER: {
        "hp": 22, "str": 4,  "mag": 16, "skl": 13, "spd": 16, "lck": 12,"def": 4,  "res": 16,
        "move": 8, "weapons": [WEAPON_STAFF, WEAPON_NAGINATA],
        "color": (180, 230, 255), "symbol": "SD",
        "flying": True,
        "description": "Airborne spirit medium. Channels wind kami into offensive bursts. Fragile but blazing fast."
    },
    CLASS_KITSUNE_SAGE: {
        "hp": 20, "str": 3,  "mag": 18, "skl": 14, "spd": 14, "lck": 16,"def": 3,  "res": 18,
        "move": 7, "weapons": [WEAPON_STAFF, WEAPON_TANTO],
        "color": (255, 210, 140), "symbol": "KS",
        "flying": True,
        "description": "Fox-spirit illusionist. Highest magic stat of all flying units. Can confuse enemies with illusions."
    },
    CLASS_VOID_PROPHET: {
        "hp": 24, "str": 2,  "mag": 17, "skl": 11, "spd": 8,  "lck": 5, "def": 4,  "res": 15,
        "move": 4, "weapons": [WEAPON_STAFF],
        "color": (60, 20, 80), "symbol": "VP",
        "description": "Dark curse weaver. Deploys AoE debuffs that linger on the battlefield. Cannot attack physically."
    },
    CLASS_SHRINE_ORACLE: {
        "hp": 26, "str": 3,  "mag": 14, "skl": 12, "spd": 9,  "lck": 15,"def": 5,  "res": 16,
        "move": 5, "weapons": [WEAPON_STAFF],
        "color": (255, 240, 200), "symbol": "SO",
        "description": "Sacred shrine priestess. Strongest healer in the game. Can bestow a barrier that absorbs one hit."
    },
    CLASS_CELESTIAL_MONK: {
        "hp": 30, "str": 6,  "mag": 16, "skl": 13, "spd": 11, "lck": 12,"def": 8,  "res": 17,
        "move": 5, "weapons": [WEAPON_STAFF, WEAPON_NAGINATA],
        "color": (230, 220, 255), "symbol": "CM",
        "description": "Promoted Monk touched by heaven. Combines powerful healing with melee capability. Rare and powerful."
    },
    CLASS_JADE_SORCERESS: {
        "hp": 18, "str": 2,  "mag": 20, "skl": 15, "spd": 10, "lck": 8, "def": 2,  "res": 14,
        "move": 4, "weapons": [WEAPON_STAFF],
        "color": (140, 220, 160), "symbol": "JS",
        "description": "Channeller of jade dragon magic. Highest raw MAG in the game but almost no physical defence."
    },
    CLASS_THUNDER_SHAMAN: {
        "hp": 28, "str": 8,  "mag": 14, "skl": 11, "spd": 11, "lck": 7, "def": 8,  "res": 12,
        "move": 7, "weapons": [WEAPON_STAFF, WEAPON_YARI],
        "color": (255, 240, 80), "symbol": "TS",
        "mounted": True,
        "description": "Storms the battlefield on horseback calling down lightning. Mobile magic that can counter with spear."
    },
    CLASS_BLOOD_ASCETIC: {
        "hp": 34, "str": 5,  "mag": 15, "skl": 10, "spd": 9,  "lck": 4, "def": 6,  "res": 10,
        "move": 4, "weapons": [WEAPON_STAFF, WEAPON_TANTO],
        "color": (160, 20, 20), "symbol": "BA",
        "description": "Self-mortifying sorcerer who converts own HP into devastating magic blasts. High risk, high reward."
    },
    CLASS_MOON_RIDER: {
        "hp": 24, "str": 10, "mag": 13, "skl": 13, "spd": 15, "lck": 11,"def": 7,  "res": 13,
        "move": 8, "weapons": [WEAPON_NAGINATA, WEAPON_STAFF],
        "color": (180, 180, 255), "symbol": "MR",
        "flying": True,
        "description": "Rides a silver-furred celestial steed through the night sky. Balances magic and naginata in equal measure."
    },
    CLASS_PHANTOM_KNIGHT: {
        "hp": 30, "str": 12, "mag": 12, "skl": 11, "spd": 10, "lck": 6, "def": 10, "res": 11,
        "move": 7, "weapons": [WEAPON_KATANA, WEAPON_STAFF],
        "color": (80, 80, 120), "symbol": "PK",
        "mounted": True,
        "description": "Cursed samurai bound by dark spirit contract. Equally dangerous with blade or with magic. Eerie and relentless."
    },
    CLASS_STAR_DANCER: {
        "hp": 20, "str": 5,  "mag": 17, "skl": 14, "spd": 17, "lck": 13,"def": 4,  "res": 15,
        "move": 9, "weapons": [WEAPON_STAFF, WEAPON_TANTO],
        "color": (255, 240, 120), "symbol": "StD",
        "flying": True,
        "description": "Celestial spell-weaver who soars on starlight. Fastest magical unit in the game. Pure offensive caster."
    },
    CLASS_DEATH_ORACLE: {
        "hp": 16, "str": 1,  "mag": 22, "skl": 16, "spd": 7,  "lck": 3, "def": 1,  "res": 13,
        "move": 4, "weapons": [WEAPON_STAFF],
        "color": (40, 0, 40), "symbol": "DO",
        "description": "Master of forbidden death arts. Absolute highest MAG in the game. Will die from a single strong hit."
    },
    # ── New Unpromoted Classes (15) ────────────────────────────────────────────
    CLASS_SHIRABYOSHI: {
        "hp": 18, "str": 4,  "mag": 8,  "skl": 8,  "spd": 14, "lck": 16,"def": 2,  "res": 10,
        "move": 5, "weapons": [WEAPON_TANTO],
        "color": (255, 180, 200), "symbol": "Sb",
        "description": "Ritual dancer and spirit medium. Can spend her turn to grant an adjacent ally an extra action."
    },
    CLASS_YAMABUSHI: {
        "hp": 28, "str": 10, "mag": 8,  "skl": 10, "spd": 8,  "lck": 8, "def": 8,  "res": 10,
        "move": 4, "weapons": [WEAPON_NAGINATA, WEAPON_STAFF],
        "color": (120, 80, 40), "symbol": "Yb",
        "description": "Mountain ascetic who blends warrior discipline with spiritual power. Sturdy and spiritually versatile."
    },
    CLASS_MIKO: {
        "hp": 22, "str": 4,  "mag": 11, "skl": 10, "spd": 10, "lck": 12,"def": 3,  "res": 12,
        "move": 5, "weapons": [WEAPON_STAFF, WEAPON_BOW],
        "color": (255, 220, 220), "symbol": "Mk",
        "description": "Shrine maiden of Shinto rites. Heals allies and can shoot arrows blessed with spiritual power."
    },
    CLASS_NOMAD: {
        "hp": 24, "str": 8,  "mag": 0,  "skl": 11, "spd": 12, "lck": 7, "def": 5,  "res": 3,
        "move": 7, "weapons": [WEAPON_BOW, WEAPON_TANTO],
        "color": (180, 160, 100), "symbol": "Nm",
        "mounted": True,
        "description": "Light horse archer from the steppe tradition. Mobile and accurate, though lightly armored."
    },
    CLASS_FOOT_GUARD: {
        "hp": 36, "str": 10, "mag": 0,  "skl": 7,  "spd": 5,  "lck": 4, "def": 14, "res": 5,
        "move": 4, "weapons": [WEAPON_YARI, WEAPON_KATANA, WEAPON_TETSUBO],
        "color": (160, 160, 140), "symbol": "FG",
        "description": "Shield-bearing armored foot soldier. Excellent defense but slow. A living barricade."
    },
    CLASS_MERCHANT: {
        "hp": 22, "str": 6,  "mag": 4,  "skl": 9,  "spd": 10, "lck": 12,"def": 4,  "res": 6,
        "move": 5, "weapons": [WEAPON_TANTO, WEAPON_BOW],
        "color": (200, 170, 100), "symbol": "Mc",
        "description": "Savvy trader turned warrior. Carries extra items and can trade across wider distances than other units."
    },
    CLASS_MUSHA: {
        "hp": 28, "str": 10, "mag": 0,  "skl": 11, "spd": 10, "lck": 8, "def": 7,  "res": 3,
        "move": 5, "weapons": [WEAPON_KATANA, WEAPON_YARI],
        "color": (120, 100, 80), "symbol": "Mw",
        "description": "Traveling warrior — the wandering mercenary of the Sengoku age. Versatile and resilient."
    },
    CLASS_YOJIMBO: {
        "hp": 30, "str": 11, "mag": 0,  "skl": 12, "spd": 10, "lck": 7, "def": 9,  "res": 3,
        "move": 5, "weapons": [WEAPON_KATANA, WEAPON_NODACHI],
        "color": (80, 80, 60), "symbol": "Yj",
        "description": "Skilled mercenary bodyguard. High skill and solid defense make them dependable in any position."
    },
    CLASS_WATER_WITCH: {
        "hp": 20, "str": 2,  "mag": 12, "skl": 10, "spd": 9,  "lck": 10,"def": 3,  "res": 13,
        "move": 5, "weapons": [WEAPON_STAFF],
        "color": (100, 160, 220), "symbol": "Wt",
        "description": "Elemental mage of water and ice. Heals and attacks with cold spiritual force."
    },
    CLASS_FIRE_ACOLYTE: {
        "hp": 22, "str": 3,  "mag": 11, "skl": 9,  "spd": 8,  "lck": 6, "def": 3,  "res": 11,
        "move": 4, "weapons": [WEAPON_STAFF, WEAPON_GUN],
        "color": (220, 100, 40), "symbol": "Fa",
        "description": "Fire elemental attacker. Combines spiritual fire magic with gunpowder — a dangerous combination."
    },
    CLASS_BLADE_MONK: {
        "hp": 28, "str": 10, "mag": 5,  "skl": 11, "spd": 9,  "lck": 7, "def": 7,  "res": 8,
        "move": 5, "weapons": [WEAPON_KATANA, WEAPON_NAGINATA],
        "color": (160, 100, 60), "symbol": "BM",
        "description": "Offensive sword-wielding monk who channels spiritual force into devastating blade strikes."
    },
    CLASS_ROGUE: {
        "hp": 20, "str": 7,  "mag": 2,  "skl": 13, "spd": 14, "lck": 11,"def": 4,  "res": 5,
        "move": 6, "weapons": [WEAPON_TANTO, WEAPON_CHAIN],
        "color": (60, 50, 40), "symbol": "Ro",
        "description": "Outlaw with nimble hands and fast feet. Expert at infiltration, scouting, and quick strikes."
    },
    CLASS_COURT_NOBLE: {
        "hp": 22, "str": 6,  "mag": 10, "skl": 10, "spd": 9,  "lck": 14,"def": 5,  "res": 12,
        "move": 5, "weapons": [WEAPON_STAFF, WEAPON_KATANA],
        "color": (200, 190, 160), "symbol": "Cn",
        "description": "Aristocratic warrior-courtier who commands through strategy and political influence."
    },
    CLASS_SEA_SOLDIER: {
        "hp": 28, "str": 10, "mag": 0,  "skl": 8,  "spd": 9,  "lck": 6, "def": 8,  "res": 4,
        "move": 5, "weapons": [WEAPON_KATANA, WEAPON_YARI],
        "color": (60, 80, 140), "symbol": "Ss",
        "water_walk": True,
        "description": "Naval foot warrior comfortable on sea and shore. Moves freely through rivers and coastal waters."
    },
    CLASS_KENIN: {
        "hp": 24, "str": 8,  "mag": 0,  "skl": 8,  "spd": 8,  "lck": 8, "def": 6,  "res": 2,
        "move": 5, "weapons": [WEAPON_KATANA],
        "color": (140, 160, 190), "symbol": "Kn",
        "description": "Young retainer in training. Eager and loyal, but still honing their skill. Great growth potential."
    },
    # ── New Promoted Classes (4) ─────────────────────────────────────────────
    CLASS_SWORD_SAINT: {
        "hp": 32, "str": 17, "mag": 2,  "skl": 20, "spd": 16, "lck": 8, "def": 8,  "res": 4,
        "move": 6, "weapons": [WEAPON_KATANA, WEAPON_NODACHI, WEAPON_TANTO],
        "color": (220, 60, 60), "symbol": "SwS",
        "description": "The pinnacle of swordsmanship. Their blade technique is so refined it borders on the supernatural."
    },
    CLASS_VALKYRIE: {
        "hp": 26, "str": 6,  "mag": 16, "skl": 13, "spd": 12, "lck": 14,"def": 7,  "res": 16,
        "move": 8, "weapons": [WEAPON_STAFF, WEAPON_BOW],
        "color": (240, 200, 240), "symbol": "Vk",
        "mounted": True,
        "description": "Mounted healer and battle-mage. Combines the mobility of cavalry with powerful restorative magic."
    },
    CLASS_GREAT_GENERAL: {
        "hp": 52, "str": 17, "mag": 2,  "skl": 11, "spd": 6,  "lck": 6, "def": 22, "res": 10,
        "move": 4, "weapons": [WEAPON_YARI, WEAPON_TETSUBO, WEAPON_NAGINATA, WEAPON_KATANA],
        "color": (210, 210, 220), "symbol": "GG",
        "description": "The ultimate armored commander. Nearly impenetrable on foot. A fortress that walks."
    },
    CLASS_WARLORD: {
        "hp": 48, "str": 20, "mag": 3,  "skl": 12, "spd": 10, "lck": 5, "def": 14, "res": 3,
        "move": 5, "weapons": [WEAPON_TETSUBO, WEAPON_NODACHI, WEAPON_YARI],
        "color": (220, 50, 30), "symbol": "WL",
        "description": "Military overlord of terrifying power. Combines the Berserker's ferocity with battlefield authority."
    },
}

# ─── Game states ──────────────────────────────────────────────────────────────
STATE_TITLE         = "title"
STATE_MODE_SELECT   = "mode_select"
STATE_MODE_CONFIRM  = "mode_confirm"   # confirmation before starting game
STATE_PROLOGUE      = "prologue"       # historical Sengoku era intro (once per new game)
STATE_SCENE         = "scene"          # pre-battle character dialogue cutscene
STATE_CHAPTER_INTRO = "chapter_intro"
STATE_PREP          = "prep"           # pre-battle preparation (deploy / shop / inventory / map)
STATE_PLAYER_TURN   = "player_turn"
STATE_ENEMY_TURN    = "enemy_turn"
STATE_ALLY_TURN     = "ally_turn"
STATE_COMBAT        = "combat"
STATE_GAME_OVER     = "game_over"
STATE_VICTORY       = "victory"
STATE_MENU          = "menu"
STATE_STAT_SHEET    = "stat_sheet"
STATE_RECRUIT       = "recruit"
STATE_REINFORCE     = "reinforce"

# Prep-screen tabs
PREP_TAB_DEPLOY    = 0
PREP_TAB_SHOP      = 1
PREP_TAB_INVENTORY = 2
PREP_TAB_MAP       = 3
PREP_TAB_NAMES     = ["Deploy", "Shop", "Inventory", "Map Preview"]

# Shop mercenary prices (gold cost) — balanced for 300 ryo start
SHOP_PRICES = {
    "merc_ashigaru":  40,   # cheap foot soldier
    "merc_spearman":  50,
    "merc_archer":    60,
    "merc_monk":      65,   # healer
    "merc_gunner":    75,
    "merc_ninja":     80,
    "merc_samurai":   90,
    "merc_cavalry":  110,   # most expensive — mounted mobility
}
STARTING_GOLD   = 300    # 300 ryo ≈ 3 cheap mercs at game start
GOLD_PER_CHAPTER = 150   # base gold at chapter clear
SIDE_OBJ_GOLD_SMALL  =  80   # minor side objective reward
SIDE_OBJ_GOLD_MEDIUM = 150   # mid-tier side objective reward
SIDE_OBJ_GOLD_LARGE  = 250   # major / chain-completion reward

# Deployment modes
DEPLOY_FORCED = "forced"   # chapter pre-selects required units
DEPLOY_FREE   = "free"     # player picks any unlocked units up to deploy_limit

# Cursor / selection modes
CURSOR_FREE     = "free"
CURSOR_UNIT_SEL = "unit_selected"
CURSOR_ATTACK   = "attack"
CURSOR_MOVE     = "move"
CURSOR_TALK     = "talk"

# Chapter objectives
OBJ_ROUT_ENEMY  = "rout_enemy"
OBJ_SEIZE       = "seize"
OBJ_SURVIVE     = "survive"
OBJ_DEFEAT_BOSS = "defeat_boss"
OBJ_ESCORT      = "escort"
OBJ_DEFEND      = "defend"     # survive X turns

# Samurai Warriors-style character archetypes (affects bio flavor)
ARCHETYPE_HERO       = "hero"
ARCHETYPE_RIVAL      = "rival"
ARCHETYPE_STRATEGIST = "strategist"
ARCHETYPE_HOTHEAD    = "hothead"
ARCHETYPE_MYSTIC     = "mystic"
ARCHETYPE_LOYAL      = "loyal"
ARCHETYPE_AMBITIOUS  = "ambitious"
ARCHETYPE_FREE       = "free spirit"
ARCHETYPE_NOBLE      = "noble"
