## Game constants — autoloaded as Constants.
extends Node

# ── Display ──────────────────────────────────────────────────────────────────
const SCREEN_WIDTH := 1024
const SCREEN_HEIGHT := 768
const TILE_SIZE := 48
const UI_PANEL_WIDTH := 290

# ── Factions ─────────────────────────────────────────────────────────────────
enum Faction { PLAYER, ENEMY, ALLY }

# ── Game states ──────────────────────────────────────────────────────────────
enum GameState {
	TITLE,
	MODE_SELECT,
	MODE_CONFIRM,
	PROLOGUE,
	SCENE,
	CHAPTER_INTRO,
	PREP,
	PLAYER_TURN,
	ENEMY_TURN,
	ALLY_TURN,
	COMBAT,
	COMBAT_ANIM,
	MENU,
	TUTORIAL,
	REINFORCE,
	VICTORY,
	GAME_OVER,
}

# ── Cursor modes ─────────────────────────────────────────────────────────────
enum CursorMode { FREE, UNIT_SELECTED, ATTACK, HEAL, TALK }

# ── Terrain types ────────────────────────────────────────────────────────────
enum Terrain {
	PLAIN, FOREST, MOUNTAIN, RIVER, BRIDGE, FORT,
	VILLAGE, CASTLE, ROAD, WALL, GATE, SEA, DESERT,
}

# ── Terrain data: {move_cost, def_bonus, avo_bonus, heals} ──────────────────
const TERRAIN_DATA := {
	Terrain.PLAIN:    {"move": 1, "def": 0, "avo": 0,  "heals": false},
	Terrain.FOREST:   {"move": 2, "def": 1, "avo": 20, "heals": false},
	Terrain.MOUNTAIN: {"move": 4, "def": 2, "avo": 30, "heals": false},
	Terrain.RIVER:    {"move": 3, "def": 0, "avo": 10, "heals": false},
	Terrain.BRIDGE:   {"move": 1, "def": 0, "avo": 0,  "heals": false},
	Terrain.FORT:     {"move": 1, "def": 2, "avo": 20, "heals": true},
	Terrain.VILLAGE:  {"move": 1, "def": 1, "avo": 10, "heals": false},
	Terrain.CASTLE:   {"move": 1, "def": 3, "avo": 30, "heals": true},
	Terrain.ROAD:     {"move": 1, "def": 0, "avo": 0,  "heals": false},
	Terrain.WALL:     {"move": 99,"def": 0, "avo": 0,  "heals": false},
	Terrain.GATE:     {"move": 1, "def": 2, "avo": 20, "heals": false},
	Terrain.SEA:      {"move": 99,"def": 0, "avo": 0,  "heals": false},
	Terrain.DESERT:   {"move": 3, "def": 0, "avo": 5,  "heals": false},
}

# ── Terrain names / colors for rendering ─────────────────────────────────────
const TERRAIN_NAMES := {
	Terrain.PLAIN: "Plain", Terrain.FOREST: "Forest",
	Terrain.MOUNTAIN: "Mountain", Terrain.RIVER: "River",
	Terrain.BRIDGE: "Bridge", Terrain.FORT: "Fort",
	Terrain.VILLAGE: "Village", Terrain.CASTLE: "Castle",
	Terrain.ROAD: "Road", Terrain.WALL: "Wall",
	Terrain.GATE: "Gate", Terrain.SEA: "Sea",
	Terrain.DESERT: "Desert",
}

const TERRAIN_COLORS := {
	Terrain.PLAIN:    Color(0.45, 0.65, 0.30),
	Terrain.FOREST:   Color(0.15, 0.40, 0.12),
	Terrain.MOUNTAIN: Color(0.45, 0.38, 0.28),
	Terrain.RIVER:    Color(0.20, 0.40, 0.70),
	Terrain.BRIDGE:   Color(0.50, 0.38, 0.22),
	Terrain.FORT:     Color(0.35, 0.30, 0.25),
	Terrain.VILLAGE:  Color(0.55, 0.45, 0.30),
	Terrain.CASTLE:   Color(0.30, 0.28, 0.35),
	Terrain.ROAD:     Color(0.55, 0.50, 0.35),
	Terrain.WALL:     Color(0.30, 0.30, 0.30),
	Terrain.GATE:     Color(0.40, 0.30, 0.20),
	Terrain.SEA:      Color(0.12, 0.25, 0.55),
	Terrain.DESERT:   Color(0.70, 0.60, 0.35),
}

# ── Weapon types ─────────────────────────────────────────────────────────────
enum WeaponType { KATANA, YARI, NAGINATA, NODACHI, TANTO, BOW, TETSUBO, GUN, CHAIN, STAFF }

# ── Weapon triangle ─────────────────────────────────────────────────────────
# Returns +1 (advantage), -1 (disadvantage), or 0 (neutral)
static func weapon_triangle(atk_type: int, def_type: int) -> int:
	# Yari > Katana > Naginata > Yari
	if atk_type == WeaponType.YARI and def_type == WeaponType.KATANA:
		return 1
	if atk_type == WeaponType.KATANA and def_type == WeaponType.NAGINATA:
		return 1
	if atk_type == WeaponType.NAGINATA and def_type == WeaponType.YARI:
		return 1
	# Reverse
	if def_type == WeaponType.YARI and atk_type == WeaponType.KATANA:
		return -1
	if def_type == WeaponType.KATANA and atk_type == WeaponType.NAGINATA:
		return -1
	if def_type == WeaponType.NAGINATA and atk_type == WeaponType.YARI:
		return -1
	return 0

# ── Unit classes (base) ──────────────────────────────────────────────────────
const CLASS_LORD       := "Lord"
const CLASS_DAIMYO     := "Daimyo"
const CLASS_SAMURAI    := "Samurai"
const CLASS_RONIN      := "Ronin"
const CLASS_ASHIGARU   := "Ashigaru"
const CLASS_SPEARMAN   := "Spearman"
const CLASS_ARCHER     := "Archer"
const CLASS_CAVALRY    := "Cavalry"
const CLASS_NINJA      := "Ninja"
const CLASS_KUNOICHI   := "Kunoichi"
const CLASS_MONK       := "Monk"
const CLASS_SOHEI      := "Sohei"
const CLASS_ONMYOJI    := "Onmyoji"
const CLASS_NOBLE_LADY := "Noble Lady"
const CLASS_GUNNER     := "Gunner"
const CLASS_GENERAL    := "General"
const CLASS_BERSERKER  := "Berserker"
const CLASS_TACTICIAN  := "Tactician"
const CLASS_MOUNTED_ARCHER := "Mounted Archer"
const CLASS_PEGASUS    := "Pegasus"
const CLASS_WYVERN     := "Wyvern"
const CLASS_PIRATE     := "Pirate"
const CLASS_KUSARIGAMA := "Kusarigama"
const CLASS_HATAMOTO   := "Hatamoto"

# ── Unit class symbols ───────────────────────────────────────────────────────
const CLASS_SYMBOLS := {
	CLASS_LORD: "♦", CLASS_DAIMYO: "♛", CLASS_SAMURAI: "★", CLASS_RONIN: "☆",
	CLASS_ASHIGARU: "▲", CLASS_SPEARMAN: "▼", CLASS_ARCHER: "➶",
	CLASS_CAVALRY: "♞", CLASS_NINJA: "✦", CLASS_KUNOICHI: "✧",
	CLASS_MONK: "✙", CLASS_SOHEI: "⚔", CLASS_ONMYOJI: "☯",
	CLASS_NOBLE_LADY: "♥", CLASS_GUNNER: "⊕", CLASS_GENERAL: "◆",
	CLASS_BERSERKER: "⚡", CLASS_TACTICIAN: "⚙", CLASS_MOUNTED_ARCHER: "♘",
	CLASS_PEGASUS: "♧", CLASS_WYVERN: "♧", CLASS_PIRATE: "☠",
	CLASS_KUSARIGAMA: "⛓", CLASS_HATAMOTO: "♔",
}

# ── Class properties ─────────────────────────────────────────────────────────
const FLYING_CLASSES := [CLASS_PEGASUS, CLASS_WYVERN]
const MOUNTED_CLASSES := [CLASS_CAVALRY, CLASS_MOUNTED_ARCHER]

# ── Deploy modes ─────────────────────────────────────────────────────────────
enum DeployMode { FORCED, FREE }

# ── Economy ──────────────────────────────────────────────────────────────────
const GOLD_PER_CHAPTER := 500
const SHOP_PRICES := {
	"merc_ashigaru": 200,
	"merc_samurai": 400,
	"merc_archer": 350,
	"merc_cavalry": 500,
	"merc_monk": 450,
	"merc_ninja": 600,
}

# ── Colors (UI) ──────────────────────────────────────────────────────────────
const COLOR_GOLD       := Color(0.85, 0.65, 0.13)
const COLOR_CREAM      := Color(1.0, 0.98, 0.90)
const COLOR_LIGHT_BLUE := Color(0.53, 0.81, 0.98)
const COLOR_PINK       := Color(1.0, 0.71, 0.76)
const COLOR_PLAYER     := Color(0.3, 0.5, 0.9)
const COLOR_ENEMY      := Color(0.9, 0.3, 0.3)
const COLOR_ALLY       := Color(0.3, 0.8, 0.4)
const COLOR_MOVE_RANGE := Color(0.3, 0.5, 1.0, 0.35)
const COLOR_ATTACK_RANGE := Color(1.0, 0.3, 0.3, 0.3)
