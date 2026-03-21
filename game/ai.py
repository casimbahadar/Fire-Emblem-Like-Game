'''
Enemy AI for Sengoku Tactics — aggressive, with flying/mounted awareness.
'''
from game.constants import *
from game.combat import resolve_combat, resolve_heal
from game.weapon import WEAPON_STAFF


class EnemyAI:
    def __init__(self, game_state):
        self.gs = game_state

    def run_enemy_turn(self):
        enemies = [u for u in self.gs.enemy_units if u.alive and not u.has_acted]
        for enemy in enemies:
            self._process_unit(enemy)
            enemy.done()

    def run_ally_turn(self):
        allies = [u for u in self.gs.ally_units if u.alive and not u.has_acted]
        for ally in allies:
            self._process_ally(ally)
            ally.done()

    def _process_unit(self, unit):
        gs   = self.gs
        gmap = gs.game_map

        # Get reachable tiles (respects flying/mounted)
        reachable = gmap.get_movement_range(
            unit.x, unit.y, unit.move, unit.unit_class,
            is_flying=unit.is_flying, is_mounted=unit.is_mounted,
            water_walk=unit.water_walk,
        )
        # Remove tiles occupied by allied faction
        friendly_tiles = {(u.x, u.y) for u in gs.enemy_units
                          if u.alive and u != unit}
        reachable -= friendly_tiles

        w = unit.equipped
        if w is None:
            self._move_toward_nearest(unit, gs.player_units + gs.ally_units, reachable)
            return

        min_r, max_r = unit.attack_range()

        # Check if weapon is a pure healing staff — don't attack with it
        is_heal_only = (w.weapon_type == WEAPON_STAFF and
                        ("heal" in w.weapon_id or "mend" in w.weapon_id))
        if is_heal_only:
            self._move_toward_nearest(unit, gs.player_units + gs.ally_units, reachable)
            return

        best_move   = None
        best_target = None
        best_score  = -9999

        targets = [t for t in gs.player_units + gs.ally_units if t.alive]

        for (mx, my) in reachable:
            for target in targets:
                dist = abs(mx - target.x) + abs(my - target.y)
                if min_r <= dist <= max_r:
                    score = self._score_attack(unit, target, mx, my)
                    if score > best_score:
                        best_score  = score
                        best_move   = (mx, my)
                        best_target = target

        if best_move and best_target:
            if best_move != (unit.x, unit.y):
                unit.x, unit.y = best_move
            terrain_att = gmap.get_terrain(unit.x, unit.y)
            terrain_def = gmap.get_terrain(best_target.x, best_target.y)
            result = resolve_combat(unit, best_target, terrain_att, terrain_def)
            gs.combat_log.append(result)
            if not best_target.alive:
                best_target.alive = False
        else:
            self._move_toward_nearest(unit, targets, reachable)

    def _score_attack(self, attacker, defender, ax, ay):
        gs   = self.gs
        gmap = gs.game_map
        terrain_def = gmap.get_terrain(defender.x, defender.y)
        td  = TERRAIN_DATA[terrain_def]

        atk  = attacker.attack_power(defender.equipped, target=defender)
        def_ = defender.def_ + td["def"]
        dmg  = max(0, atk - def_)

        if dmg >= defender.hp:
            score = 200 + defender.level * 5
        else:
            score = (dmg / max(1, defender.hp)) * 100 + defender.level * 2

        score -= max(0, def_ - attacker.str_) * 2

        if defender.is_lord:
            score += 50
        if attacker.is_flying and defender.equipped:
            # Flyers slightly avoid well-armed defenders
            from game.weapon import WEAPON_BOW
            if defender.equipped.weapon_type == WEAPON_BOW:
                score -= 30

        return score

    def _move_toward_nearest(self, unit, targets, reachable):
        alive_targets = [t for t in targets if t.alive]
        if not alive_targets:
            return
        nearest = min(alive_targets, key=lambda t: abs(unit.x-t.x)+abs(unit.y-t.y))
        best, best_d = None, 9999
        for (mx, my) in reachable:
            d = abs(mx - nearest.x) + abs(my - nearest.y)
            if d < best_d:
                best_d = d
                best   = (mx, my)
        if best and best != (unit.x, unit.y):
            unit.x, unit.y = best

    def _process_ally(self, unit):
        gs   = self.gs
        gmap = gs.game_map
        reachable = gmap.get_movement_range(
            unit.x, unit.y, unit.move, unit.unit_class,
            is_flying=unit.is_flying, is_mounted=unit.is_mounted,
            water_walk=unit.water_walk,
        )
        friendly_tiles = {(u.x, u.y) for u in gs.ally_units
                          if u.alive and u != unit}
        reachable -= friendly_tiles

        w = unit.equipped
        if w and w.weapon_type == WEAPON_STAFF:
            best_target, best_move, worst_hp_pct = None, None, 1.0
            for (mx, my) in reachable:
                for friend in gs.player_units + gs.ally_units:
                    if not friend.alive or friend == unit:
                        continue
                    dist = abs(mx - friend.x) + abs(my - friend.y)
                    if dist <= w.max_range:
                        pct = friend.hp / friend.max_hp
                        if pct < worst_hp_pct:
                            worst_hp_pct = pct
                            best_target  = friend
                            best_move    = (mx, my)
            if best_target and worst_hp_pct < 0.85:
                if best_move and best_move != (unit.x, unit.y):
                    unit.x, unit.y = best_move
                resolve_heal(unit, best_target)
                return

        self._process_unit(unit)
