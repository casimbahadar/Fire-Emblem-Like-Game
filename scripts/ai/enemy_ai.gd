## Enemy AI — aggressive targeting with terrain awareness.
class_name EnemyAI
extends RefCounted

var grid: Grid
var player_units: Array = []
var enemy_units: Array = []
var ally_units: Array = []


func _init(g: Grid, players: Array, enemies: Array, allies: Array = []):
	grid = g
	player_units = players
	enemy_units = enemies
	ally_units = allies


## Run the full enemy turn. Returns array of actions taken for animation.
func run_turn() -> Array:
	var actions: Array = []
	var active := enemy_units.filter(func(u): return u.alive and not u.has_acted)

	for unit in active:
		var action := _process_unit(unit)
		if action:
			actions.append(action)
		unit.done()

	return actions


func _process_unit(unit) -> Dictionary:
	var reachable := grid.get_movement_range(
		unit.grid_pos, unit.mov, unit.unit_class,
		unit.is_flying, unit.is_mounted, unit.water_walk)

	# Remove tiles occupied by friendly units
	var friendly_tiles := {}
	for u in enemy_units:
		if u.alive and u != unit:
			friendly_tiles[u.grid_pos] = true
	var landing := reachable.filter(func(t): return not friendly_tiles.has(t))

	var w := unit.equipped
	if w.is_empty():
		return _move_toward_nearest(unit, landing)

	# Skip heal-only staves
	if w.get("weapon_type", -1) == Constants.WeaponType.STAFF:
		if "heal" in w.get("weapon_id", "") or "mend" in w.get("weapon_id", ""):
			return _move_toward_nearest(unit, landing)

	var range_vec := unit.attack_range()
	var min_r: int = range_vec.x
	var max_r: int = range_vec.y

	var targets := (player_units + ally_units).filter(func(u): return u.alive)

	var best_move: Vector2i = unit.grid_pos
	var best_target = null
	var best_score := -9999.0

	for tile in landing:
		for target in targets:
			var dist := absi(tile.x - target.grid_pos.x) + absi(tile.y - target.grid_pos.y)
			if dist >= min_r and dist <= max_r:
				var score := _score_attack(unit, target, tile)
				if score > best_score:
					best_score = score
					best_move = tile
					best_target = target

	if best_target:
		unit.grid_pos = best_move
		return {"type": "attack", "unit": unit, "target": best_target, "move_to": best_move}
	else:
		return _move_toward_nearest(unit, landing)


func _score_attack(attacker, defender, from_pos: Vector2i) -> float:
	var td := grid.get_terrain_data(defender.grid_pos)
	var def_bonus: int = td.get("def", 0)
	var dmg := max(0, attacker.attack_power(defender.equipped, defender) - defender.defense() - def_bonus)

	var score: float
	if dmg >= defender.hp:
		score = 200.0 + defender.level * 5.0
	else:
		score = (float(dmg) / max(1, defender.hp)) * 100.0 + defender.level * 2.0

	score -= max(0, defender.defense() + def_bonus - attacker.str_) * 2.0
	return score


func _move_toward_nearest(unit, landing: Array) -> Dictionary:
	var targets := (player_units + ally_units).filter(func(u): return u.alive)
	if targets.is_empty() or landing.is_empty():
		return {}

	var nearest_target = targets[0]
	var best_dist := 9999
	for t in targets:
		var d := absi(unit.grid_pos.x - t.grid_pos.x) + absi(unit.grid_pos.y - t.grid_pos.y)
		if d < best_dist:
			best_dist = d
			nearest_target = t

	var best_tile: Vector2i = unit.grid_pos
	var closest := 9999
	for tile in landing:
		var d := absi(tile.x - nearest_target.grid_pos.x) + absi(tile.y - nearest_target.grid_pos.y)
		if d < closest:
			closest = d
			best_tile = tile

	unit.grid_pos = best_tile
	return {"type": "move", "unit": unit, "move_to": best_tile}
