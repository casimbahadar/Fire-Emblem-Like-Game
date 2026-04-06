## Save/Load system — persists campaign state to user:// as JSON.
class_name SaveSystem
extends RefCounted

const SAVE_PATH := "user://sengoku_save.json"
const MAX_SLOTS := 3


## Save the current game state to a slot (0-2).
static func save_game(slot: int = 0) -> bool:
	var all_saves := _load_all_saves()

	var save_data := {
		"slot": slot,
		"timestamp": Time.get_datetime_string_from_system(),
		"chapter_index": GameData.chapter_index,
		"turn_number": GameData.turn_number,
		"gold": GameData.gold,
		"classic_mode": GameData.classic_mode,
		"casualty_list": GameData.casualty_list.duplicate(),
		"roster": _serialize_roster(),
	}

	all_saves[str(slot)] = save_data

	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if not file:
		push_error("SaveSystem: Could not open save file for writing")
		return false

	file.store_string(JSON.stringify(all_saves, "\t"))
	file.close()
	return true


## Load a game from a slot. Returns true if successful.
static func load_game(slot: int = 0) -> bool:
	var all_saves := _load_all_saves()
	var key := str(slot)

	if not all_saves.has(key):
		push_error("SaveSystem: No save data in slot %d" % slot)
		return false

	var save_data: Dictionary = all_saves[key]

	GameData.chapter_index = save_data.get("chapter_index", 0)
	GameData.turn_number = save_data.get("turn_number", 1)
	GameData.gold = save_data.get("gold", 0)
	GameData.classic_mode = save_data.get("classic_mode", true)
	GameData.casualty_list = save_data.get("casualty_list", [])

	# Rebuild roster from saved data
	var roster_base: Dictionary = Roster.create_roster()
	var saved_roster: Dictionary = save_data.get("roster", {})

	GameData.roster.clear()
	for uid in saved_roster:
		var sdata: Dictionary = saved_roster[uid]
		var unit: UnitData
		if roster_base.has(uid):
			unit = roster_base[uid]
		else:
			unit = UnitData.new()
			unit.unit_id = uid

		# Apply saved stats
		unit.name = sdata.get("name", uid.capitalize())
		unit.unit_class = sdata.get("unit_class", unit.unit_class)
		unit.level = sdata.get("level", unit.level)
		unit.exp = sdata.get("exp", 0)
		unit.max_hp = sdata.get("max_hp", unit.max_hp)
		unit.hp = sdata.get("hp", unit.max_hp)
		unit.str_ = sdata.get("str", unit.str_)
		unit.mag = sdata.get("mag", unit.mag)
		unit.skl = sdata.get("skl", unit.skl)
		unit.spd = sdata.get("spd", unit.spd)
		unit.lck = sdata.get("lck", unit.lck)
		unit.def_ = sdata.get("def", unit.def_)
		unit.res = sdata.get("res", unit.res)
		unit.mov = sdata.get("mov", unit.mov)
		unit.faction = sdata.get("faction", Constants.Faction.PLAYER)
		unit.equipped_weapon_index = sdata.get("equipped_weapon_index", 0)
		unit.alive = sdata.get("alive", true)

		GameData.roster[uid] = unit

	return true


## Check if a save slot has data.
static func has_save(slot: int = 0) -> bool:
	var all_saves := _load_all_saves()
	return all_saves.has(str(slot))


## Get save slot info for display (returns dict with chapter, timestamp, etc.)
static func get_save_info(slot: int = 0) -> Dictionary:
	var all_saves := _load_all_saves()
	var key := str(slot)
	if not all_saves.has(key):
		return {}
	var sd: Dictionary = all_saves[key]
	return {
		"chapter_index": sd.get("chapter_index", 0),
		"gold": sd.get("gold", 0),
		"timestamp": sd.get("timestamp", ""),
		"turn_number": sd.get("turn_number", 1),
	}


## Delete a save slot.
static func delete_save(slot: int = 0) -> void:
	var all_saves := _load_all_saves()
	all_saves.erase(str(slot))
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(all_saves, "\t"))
		file.close()


# ── Internal helpers ─────────────────────────────────────────────────────────

static func _load_all_saves() -> Dictionary:
	if not FileAccess.file_exists(SAVE_PATH):
		return {}
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if not file:
		return {}
	var text := file.get_as_text()
	file.close()
	var json := JSON.new()
	if json.parse(text) != OK:
		return {}
	if json.data is Dictionary:
		return json.data
	return {}


static func _serialize_roster() -> Dictionary:
	var result := {}
	for uid in GameData.roster:
		var u: UnitData = GameData.roster[uid]
		result[uid] = {
			"name": u.name,
			"unit_class": u.unit_class,
			"level": u.level,
			"exp": u.exp,
			"max_hp": u.max_hp,
			"hp": u.hp,
			"str": u.str_,
			"mag": u.mag,
			"skl": u.skl,
			"spd": u.spd,
			"lck": u.lck,
			"def": u.def_,
			"res": u.res,
			"mov": u.mov,
			"faction": u.faction,
			"equipped_weapon_index": u.equipped_weapon_index,
			"alive": u.alive,
		}
	return result
