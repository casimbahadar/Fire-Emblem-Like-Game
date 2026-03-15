"""
Combat resolution for Sengoku Tactics
Two-RN hit system, doubles, crits, weapon triangle, anti-type bonuses.
"""
import random
from game.constants import *
from game.weapon import WEAPON_STAFF


class CombatResult:
    def __init__(self):
        self.attacker_name = ""
        self.defender_name = ""
        self.rounds        = []
        self.attacker_died = False
        self.defender_died = False
        self.exp_attacker  = 0
        self.exp_defender  = 0
        self.level_up_att  = False
        self.level_up_def  = False


class RoundResult:
    def __init__(self, attacker, damage, hit, crit, is_counter=False):
        self.attacker   = attacker
        self.damage     = damage
        self.hit        = hit
        self.crit       = crit
        self.is_counter = is_counter


def resolve_combat(attacker, defender, terrain_attacker=None, terrain_defender=None):
    result = CombatResult()
    result.attacker_name = attacker.name
    result.defender_name = defender.name

    _apply_terrain(attacker, terrain_attacker)
    _apply_terrain(defender, terrain_defender)

    can_counter = _can_counter(attacker, defender)

    # First strike
    rnd = _strike(attacker, defender)
    result.rounds.append(rnd)
    if rnd.hit:
        defender.take_damage(rnd.damage)

    # Counter
    if defender.alive and can_counter:
        rnd2 = _strike(defender, attacker, is_counter=True)
        result.rounds.append(rnd2)
        if rnd2.hit:
            attacker.take_damage(rnd2.damage)

    # Double attacks
    if attacker.alive and defender.alive:
        att_spd = _effective_spd(attacker)
        def_spd = _effective_spd(defender)
        if att_spd - def_spd >= 4:
            rnd3 = _strike(attacker, defender)
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

    # EXP
    ld  = defender.level - attacker.level
    exp = max(1, 20 + ld * 2) + (40 if result.defender_died else 0)
    result.exp_attacker = exp

    if can_counter:
        ld2 = attacker.level - defender.level
        exp2= max(1, 15 + ld2) + (40 if result.attacker_died else 0)
        result.exp_defender = exp2

    if not result.attacker_died:
        w = attacker.equipped
        if not (w and w.weapon_type == WEAPON_STAFF and "heal" in w.weapon_id):
            result.level_up_att = attacker.gain_exp(result.exp_attacker)

    if not result.defender_died and can_counter:
        result.level_up_def = defender.gain_exp(result.exp_defender)

    return result


def resolve_heal(healer, target):
    w = healer.equipped
    if w is None or w.weapon_type != WEAPON_STAFF:
        return 0
    if "mend" in w.weapon_id:
        amount = healer.mag + 20
    elif "physic" in w.weapon_id or "amulet" in w.weapon_id:
        amount = healer.mag + 15
    else:
        amount = healer.mag + 10
    target.heal(amount)
    healer.gain_exp(max(10, 20 - abs(healer.level - target.level)))
    return amount


def _apply_terrain(unit, terrain):
    if terrain and terrain in TERRAIN_DATA:
        td = TERRAIN_DATA[terrain]
        unit.set_terrain_bonuses(td["def"], td["avo"])
    else:
        unit.set_terrain_bonuses(0, 0)


def _effective_spd(unit):
    w = unit.equipped
    if w is None:
        return unit.spd
    pen = max(0, w.weight - unit.str_ // 2)
    return max(0, unit.spd - pen)


def _can_counter(attacker, defender):
    w = defender.equipped
    if w is None:
        return False
    # Pure heal staves can't counter
    if w.weapon_type == WEAPON_STAFF:
        wid = getattr(w, 'weapon_id', '')
        if "heal" in wid or "mend" in wid or "physic" in wid or "amulet" in wid:
            return False
    return True


def _strike(attacker, defender, is_counter=False):
    att_w = attacker.equipped
    def_w = defender.equipped

    hit_rate   = attacker.hit_rate(def_w)
    avoid_rate = defender.avoid()
    actual_hit = max(0, min(100, hit_rate - avoid_rate))

    # Two-RN system (skews distribution toward centre — fewer extreme results)
    r1, r2 = random.randint(0, 99), random.randint(0, 99)
    did_hit = (r1 + r2) // 2 < actual_hit

    crit_rate  = max(0, attacker.crit_rate(def_w) - defender.crit_avoid())
    did_crit   = random.randint(0, 99) < crit_rate

    atk    = attacker.attack_power(def_w, target=defender)
    def_   = defender.defense()
    damage = max(0, atk - def_)
    if did_crit:
        damage *= 3  # Fire Emblem-style triple damage on crit

    if not did_hit:
        damage = 0

    return RoundResult(
        attacker=attacker.name,
        damage=damage,
        hit=did_hit,
        crit=did_crit,
        is_counter=is_counter
    )
