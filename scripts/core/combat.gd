## Combat resolution system — Two-RN hit, doubles, crits, weapon triangle.
class_name Combat
extends RefCounted


class RoundResult:
	var attacker_name: String
	var damage: int
	var hit: bool
	var crit: bool
	var is_counter: bool

	func _init(a_name: String, dmg: int, did_hit: bool, did_crit: bool, counter: bool = false):
		attacker_name = a_name
		damage = dmg
		hit = did_hit
		crit = did_crit
		is_counter = counter


class CombatResult:
	var attacker_name: String
	var defender_name: String
	var rounds: Array = []  # Array of RoundResult
	var attacker_died: bool = false
	var defender_died: bool = false
	var exp_attacker: int = 0
	var exp_defender: int = 0
	var level_up_att: bool = false
	var level_up_def: bool = false


## Resolve full combat between attacker and defender.
## terrain_att/def are terrain type ints for positional bonuses.
static func resolve(
	attacker: UnitData, defender: UnitData,
	terrain_att: int = Constants.Terrain.PLAIN,
	terrain_def: int = Constants.Terrain.PLAIN
) -> CombatResult:
	var result := CombatResult.new()
	result.attacker_name = attacker.name
	result.defender_name = defender.name

	var td_att := Constants.TERRAIN_DATA.get(terrain_att, {})
	var td_def := Constants.TERRAIN_DATA.get(terrain_def, {})

	var can_counter := _can_counter(attacker, defender)

	# ── First strike ─────────────────────────────────────────────────────
	var rnd := _strike(attacker, defender, td_att, td_def)
	result.rounds.append(rnd)
	if rnd.hit:
		defender.take_damage(rnd.damage)

	# ── Counter ──────────────────────────────────────────────────────────
	if defender.alive and can_counter:
		var rnd2 := _strike(defender, attacker, td_def, td_att, true)
		result.rounds.append(rnd2)
		if rnd2.hit:
			attacker.take_damage(rnd2.damage)

	# ── Double attacks (speed difference >= 4) ───────────────────────────
	if attacker.alive and defender.alive:
		var att_spd := attacker.spd - attacker.equipped.get("weight", 0)
		var def_spd := defender.spd - defender.equipped.get("weight", 0)
		if att_spd - def_spd >= 4:
			var rnd3 := _strike(attacker, defender, td_att, td_def)
			result.rounds.append(rnd3)
			if rnd3.hit:
				defender.take_damage(rnd3.damage)
		elif def_spd - att_spd >= 4 and can_counter and defender.alive:
			var rnd3 := _strike(defender, attacker, td_def, td_att, true)
			result.rounds.append(rnd3)
			if rnd3.hit:
				attacker.take_damage(rnd3.damage)

	# ── Results ──────────────────────────────────────────────────────────
	result.attacker_died = not attacker.alive
	result.defender_died = not defender.alive

	# ── EXP ──────────────────────────────────────────────────────────────
	var ld := defender.level - attacker.level
	result.exp_attacker = max(1, 20 + ld * 2) + (40 if result.defender_died else 0)

	if can_counter:
		var ld2 := attacker.level - defender.level
		result.exp_defender = max(1, 15 + ld2) + (40 if result.attacker_died else 0)

	# ── Apply EXP ────────────────────────────────────────────────────────
	if not result.attacker_died:
		result.level_up_att = attacker.gain_exp(result.exp_attacker)
	if not result.defender_died and can_counter:
		result.level_up_def = defender.gain_exp(result.exp_defender)

	return result


static func _strike(
	atk: UnitData, dfn: UnitData,
	td_atk: Dictionary, td_def: Dictionary,
	is_counter: bool = false
) -> RoundResult:
	var def_bonus: int = td_def.get("def", 0)
	var avo_bonus: int = td_def.get("avo", 0)

	var damage := max(0, atk.attack_power(dfn.equipped, dfn) - dfn.defense() - def_bonus)
	var hit_chance := clampi(atk.hit_rate(dfn.equipped) - dfn.avoid() - avo_bonus, 0, 100)
	var crit_chance := clampi(atk.crit_rate(dfn.equipped) - dfn.crit_avoid(), 0, 100)

	# Two-RN hit system (average of two random rolls — like Fire Emblem)
	var roll := (randf() * 100 + randf() * 100) / 2.0
	var did_hit := roll < hit_chance

	var did_crit := false
	if did_hit and randf() * 100 < crit_chance:
		did_crit = true
		damage *= 3

	if not did_hit:
		damage = 0

	return RoundResult.new(atk.name, damage, did_hit, did_crit, is_counter)


static func _can_counter(attacker: UnitData, defender: UnitData) -> bool:
	var def_w := defender.equipped
	if def_w.is_empty():
		return false
	# Staves can't counter
	if def_w.get("weapon_type", -1) == Constants.WeaponType.STAFF:
		return false
	# Check range: defender must be able to reach attacker's distance
	var dist := absi(attacker.grid_pos.x - defender.grid_pos.x) + absi(attacker.grid_pos.y - defender.grid_pos.y)
	var mn: int = def_w.get("min_range", 1)
	var mx: int = def_w.get("max_range", 1)
	return dist >= mn and dist <= mx


## Resolve healing action.
static func resolve_heal(healer: UnitData, target: UnitData) -> int:
	var w := healer.equipped
	if w.is_empty() or w.get("weapon_type", -1) != Constants.WeaponType.STAFF:
		return 0
	var amount: int
	if "mend" in w.get("weapon_id", ""):
		amount = healer.mag + 20
	elif "physic" in w.get("weapon_id", ""):
		amount = healer.mag + 10
	else:
		amount = healer.mag + 15
	target.heal(amount)
	return amount
