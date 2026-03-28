## Unit data resource — stores all stats for one unit.
## Can be instanced from roster definitions or saved/loaded.
class_name UnitData
extends Resource

@export var unit_id: String = ""
@export var name: String = ""
@export var unit_class: String = ""
@export var level: int = 1
@export var exp: int = 0

# ── Base stats ───────────────────────────────────────────────────────────────
@export var max_hp: int = 20
@export var hp: int = 20
@export var str_: int = 5
@export var mag: int = 0
@export var skl: int = 5
@export var spd: int = 5
@export var lck: int = 3
@export var def_: int = 3
@export var res: int = 1
@export var mov: int = 5

# ── Growth rates (% chance to gain +1 on level up) ──────────────────────────
@export var growth_hp: int = 60
@export var growth_str: int = 40
@export var growth_mag: int = 10
@export var growth_skl: int = 35
@export var growth_spd: int = 35
@export var growth_lck: int = 30
@export var growth_def: int = 25
@export var growth_res: int = 15

# ── Weapons ──────────────────────────────────────────────────────────────────
@export var weapons: Array[Dictionary] = []  # Array of weapon dicts
@export var equipped_weapon_index: int = 0

# ── Faction & flags ──────────────────────────────────────────────────────────
@export var faction: int = Constants.Faction.PLAYER
@export var can_recruit: bool = false
@export var recruit_by: Array[String] = []
@export var is_boss: bool = false

# ── Visual ───────────────────────────────────────────────────────────────────
@export var symbol: String = "★"
@export var color: Color = Color.WHITE
@export var portrait_quote: String = ""
@export var bio: String = ""

# ── Turn state (not saved) ──────────────────────────────────────────────────
var has_moved: bool = false
var has_acted: bool = false
var alive: bool = true
var grid_pos: Vector2i = Vector2i.ZERO


# ── Computed properties ──────────────────────────────────────────────────────
var equipped: Dictionary:
	get:
		if weapons.is_empty() or equipped_weapon_index >= weapons.size():
			return {}
		return weapons[equipped_weapon_index]

var is_flying: bool:
	get: return unit_class in Constants.FLYING_CLASSES

var is_mounted: bool:
	get: return unit_class in Constants.MOUNTED_CLASSES

var water_walk: bool:
	get: return unit_class == Constants.CLASS_PIRATE


func attack_power(enemy_weapon: Dictionary = {}, target = null) -> int:
	var w := equipped
	if w.is_empty():
		return 0
	var base: int = w.get("might", 0)
	var stat: int = mag if w.get("weapon_type", 0) == Constants.WeaponType.STAFF else str_
	var total := base + stat

	# Weapon triangle bonus
	if not enemy_weapon.is_empty():
		var tri := Constants.weapon_triangle(
			w.get("weapon_type", -1), enemy_weapon.get("weapon_type", -1))
		total += tri  # +1 or -1

	# Anti-type bonuses
	if target and w.get("weapon_type", -1) == Constants.WeaponType.BOW:
		if target.is_flying:
			total += 5  # Bow bonus vs flying

	return total


func defense() -> int:
	return def_


func hit_rate(enemy_weapon: Dictionary = {}) -> int:
	var w := equipped
	if w.is_empty():
		return 0
	var base: int = w.get("hit", 80)
	var total := base + skl * 2 + lck
	if not enemy_weapon.is_empty():
		var tri := Constants.weapon_triangle(
			w.get("weapon_type", -1), enemy_weapon.get("weapon_type", -1))
		total += tri * 10
	return total


func avoid() -> int:
	return spd * 2 + lck


func crit_rate(enemy_weapon: Dictionary = {}) -> int:
	var w := equipped
	if w.is_empty():
		return 0
	var base_crit: int = w.get("crit", 0)
	return base_crit + skl / 2


func crit_avoid() -> int:
	return lck


func attack_range() -> Vector2i:
	var w := equipped
	if w.is_empty():
		return Vector2i(1, 1)
	var mn: int = w.get("min_range", 1)
	var mx: int = w.get("max_range", 1)
	return Vector2i(mn, mx)


func take_damage(amount: int) -> void:
	hp = max(0, hp - amount)
	if hp <= 0:
		alive = false


func heal(amount: int) -> void:
	hp = min(max_hp, hp + amount)


func gain_exp(amount: int) -> bool:
	exp += amount
	if exp >= 100:
		exp -= 100
		_level_up()
		return true
	return false


func _level_up() -> void:
	level += 1
	if randf() * 100 < growth_hp:  max_hp += 1; hp += 1
	if randf() * 100 < growth_str: str_ += 1
	if randf() * 100 < growth_mag: mag += 1
	if randf() * 100 < growth_skl: skl += 1
	if randf() * 100 < growth_spd: spd += 1
	if randf() * 100 < growth_lck: lck += 1
	if randf() * 100 < growth_def: def_ += 1
	if randf() * 100 < growth_res: res += 1


func reset_turn() -> void:
	has_moved = false
	has_acted = false


func done() -> void:
	has_moved = true
	has_acted = true
