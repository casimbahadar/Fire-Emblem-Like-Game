"""
Combat resolution system for Sengoku Tactics
"""
import random
from game.constants import *
from game.weapon import WEAPON_STAFF


class CombatResult:
    def __init__(self):
        self.attacker_name  = ""
        self.defender_name  = ""
        self.rounds         = []   # list of RoundResult
        self.attacker_died  = False
        self.defender_died  = False
        self.exp_attacker   = 0
        self.exp_defender   = 0
        self.level_up_att   = False
        self.level_up_def   = False


class RoundResult:
    def __init__(self, attacker, damage, hit, crit, is_counter=False):
        self.attacker   = attacker  # unit name
        self.damage     = damage
        self.hit        = hit       # bool: did it hit
        self.crit       = crit      # bool: was it a crit
        self.is_counter = is_counter


def resolve_combat(attacker, defender, terrain_attacker=None, terrain_defender=None):
    """
    Full Fire Emblem-style combat resolution.
    Returns a CombatResult with all rounds played and final state.
    """
    result = CombatResult()
    result.attacker_name = attacker.name
    result.defender_name = defender.name

    # Apply terrain bonuses
    if terrain_attacker:
        td = TERRAIN_DATA[terrain_attacker]
        attacker.set_terrain_bonuses(td["def"], td["avo"])
    else:
        attacker.set_terrain_bonuses(0, 0)

    if terrain_defender:
        td = TERRAIN_DATA[terrain_defender]
        defender.set_terrain_bonuses(td["def"], td["avo"])
    else:
        defender.set_terrain_bonuses(0, 0)

    att_weapon = attacker.equipped
    def_weapon = defender.equipped

    # Check if defender can counter-attack
    can_counter = _can_counter(attacker, defender)

    # Attacker strikes first
    rnd = _strike(attacker, defender, is_counter=False)
    result.rounds.append(rnd)
    if rnd.hit:
        defender.take_damage(rnd.damage)

    # Defender counter-attacks (if alive and in range)
    if defender.alive and can_counter:
        rnd2 = _strike(defender, attacker, is_counter=True)
        result.rounds.append(rnd2)
        if rnd2.hit:
            attacker.take_damage(rnd2.damage)

    # Double attack: attacker's spd - defender's spd >= 4 → attacker strikes again
    if attacker.alive and defender.alive:
        att_spd = _effective_speed(attacker)
        def_spd = _effective_speed(defender)
        if att_spd - def_spd >= 4:
            rnd3 = _strike(attacker, defender, is_counter=False)
            result.rounds.append(rnd3)
            if rnd3.hit:
                defender.take_damage(rnd3.damage)
        elif def_spd - att_spd >= 4 and can_counter and defender.alive:
            rnd3 = _strike(defender, attacker, is_counter=True)
            result.rounds.append(rnd3)
            if rnd3.hit:
                attacker.take_damage(rnd3.damage)

    result.attacker_died = not attacker.alive
    result.defender_died = not defender.alive

    # EXP calculation
    level_diff = defender.level - attacker.level
    base_exp = max(1, 20 + level_diff * 2)
    kill_bonus = 40 if result.defender_died else 0
    result.exp_attacker = base_exp + kill_bonus

    if can_counter:
        base_def_exp = max(1, 15 + (attacker.level - defender.level))
        kill_bonus_def = 40 if result.attacker_died else 0
        result.exp_defender = base_def_exp + kill_bonus_def

    # Award EXP
    if not result.attacker_died:
        att_w = attacker.equipped
        if att_w and att_w.weapon_type == WEAPON_STAFF:
            pass  # Healers get exp from heal action
        else:
            result.level_up_att = attacker.gain_exp(result.exp_attacker)

    if not result.defender_died and can_counter:
        result.level_up_def = defender.gain_exp(result.exp_defender)

    return result


def resolve_heal(healer, target):
    """Healer uses staff on target. Returns heal amount."""
    w = healer.equipped
    if w is None or w.weapon_type != WEAPON_STAFF:
        return 0
    heal_amount = healer.mag + 10  # base heal
    if w.weapon_id == "mend_staff":
        heal_amount = healer.mag + 20
    target.heal(heal_amount)
    exp = max(10, 20 - abs(healer.level - target.level))
    healer.gain_exp(exp)
    return heal_amount


def _effective_speed(unit):
    w = unit.equipped
    if w is None:
        return unit.spd
    weight_pen = max(0, w.weight - unit.str_ // 2)
    return max(0, unit.spd - weight_pen)


def _can_counter(attacker, defender):
    """Check if defender can counter-attack from their position."""
    if defender.equipped is None:
        return False
    if defender.equipped.weapon_type == WEAPON_STAFF and defender.equipped.weapon_id.endswith("staff"):
        # Heal staff can't counter
        return "heal" not in defender.equipped.weapon_id and "mend" not in defender.equipped.weapon_id
    # Check range — since combat is resolved abstractly here, we assume adjacency
    # The map will verify range before initiating combat
    return True


def _strike(attacker, defender, is_counter=False):
    att_weapon = attacker.equipped
    def_weapon = defender.equipped

    # Hit calculation
    hit_rate    = attacker.hit_rate(def_weapon)
    dodge_rate  = defender.avoid()
    actual_hit  = max(0, min(100, hit_rate - dodge_rate))
    # Two RN system (average two random numbers — skews distribution)
    roll1 = random.randint(0, 99)
    roll2 = random.randint(0, 99)
    avg_roll = (roll1 + roll2) // 2
    did_hit = avg_roll < actual_hit

    # Crit calculation
    crit_rate   = attacker.crit_rate(def_weapon)
    crit_avoid  = defender.crit_avoid()
    actual_crit = max(0, crit_rate - crit_avoid)
    did_crit    = random.randint(0, 99) < actual_crit

    # Damage
    atk   = attacker.attack_power(def_weapon)
    def_  = defender.defense()
    damage = max(0, atk - def_)
    if did_crit:
        damage = damage * 3  # crits triple damage like FE

    if not did_hit:
        damage = 0

    return RoundResult(
        attacker=attacker.name,
        damage=damage,
        hit=did_hit,
        crit=did_crit,
        is_counter=is_counter
    )
