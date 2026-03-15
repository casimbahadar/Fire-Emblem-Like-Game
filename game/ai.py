"""
Enemy AI for Sengoku Tactics
Simple aggressive/defensive AI similar to Fire Emblem GBA.
"""
import random
from game.constants import *
from game.combat import resolve_combat


class EnemyAI:
    def __init__(self, game_state):
        self.gs = game_state  # reference to GameState

    def run_enemy_turn(self):
        """Process all enemy unit actions."""
        enemies = [u for u in self.gs.enemy_units if u.alive and not u.has_acted]
        for enemy in enemies:
            self._process_unit(enemy)
            enemy.done()

    def run_ally_turn(self):
        """Process all ally unit actions (heal/attack as appropriate)."""
        allies = [u for u in self.gs.ally_units if u.alive and not u.has_acted]
        for ally in allies:
            self._process_ally(ally)
            ally.done()

    def _process_unit(self, unit):
        """Determine best action for one enemy unit."""
        gs = self.gs
        gmap = gs.game_map

        occupied = {(u.x, u.y) for u in gs.all_units() if u.alive and u != unit}

        # Compute reachable tiles
        reachable = gmap.get_movement_range(unit.x, unit.y, unit.move, unit.unit_class)
        reachable -= {(u.x, u.y) for u in gs.all_units() if u.alive and u.faction == unit.faction and u != unit}

        # Find best attack target
        best_move  = None
        best_target = None
        best_score = -999

        w = unit.equipped
        if w is None:
            # Can't attack; just move toward nearest player
            self._move_toward_nearest(unit, gs.player_units, reachable, gmap)
            return

        min_r, max_r = unit.attack_range()

        for (mx, my) in reachable:
            for target in gs.player_units + gs.ally_units:
                if not target.alive:
                    continue
                dist = abs(mx - target.x) + abs(my - target.y)
                if min_r <= dist <= max_r:
                    score = self._score_attack(unit, target, mx, my, gmap)
                    if score > best_score:
                        best_score = score
                        best_move  = (mx, my)
                        best_target = target

        if best_move and best_target:
            # Move to best_move
            if best_move != (unit.x, unit.y):
                unit.x, unit.y = best_move
            # Attack
            terrain_att = gmap.get_terrain(unit.x, unit.y)
            terrain_def = gmap.get_terrain(best_target.x, best_target.y)
            result = resolve_combat(unit, best_target, terrain_att, terrain_def)
            gs.combat_log.append(result)
            if best_target.hp <= 0:
                best_target.alive = False
        else:
            # No attack possible; move toward nearest enemy
            targets = gs.player_units + gs.ally_units
            self._move_toward_nearest(unit, targets, reachable, gmap)

    def _score_attack(self, attacker, defender, ax, ay, gmap):
        """Score how good an attack would be (higher = better)."""
        terrain_att = gmap.get_terrain(ax, ay)
        terrain_def = gmap.get_terrain(defender.x, defender.y)

        # Estimate damage
        atk = attacker.attack_power(defender.equipped)
        def_ = defender.def_ + TERRAIN_DATA[terrain_def]["def"]
        dmg = max(0, atk - def_)

        # Bonus for killing blow
        if dmg >= defender.hp:
            score = 200 + defender.level * 5
        else:
            hp_pct_dmg = (dmg / max(1, defender.hp)) * 100
            score = hp_pct_dmg + defender.level * 2

        # Penalty for attacking high-def targets
        score -= max(0, def_ - attacker.str_) * 2

        # Bonus for targeting lords (player win condition)
        if defender.is_lord:
            score += 50

        return score

    def _move_toward_nearest(self, unit, targets, reachable, gmap):
        """Move toward the nearest target."""
        alive_targets = [t for t in targets if t.alive]
        if not alive_targets:
            return

        # Pick closest
        def dist_to(t):
            return abs(unit.x - t.x) + abs(unit.y - t.y)
        nearest = min(alive_targets, key=dist_to)

        # Move to reachable tile closest to target
        best = None
        best_d = 9999
        for (mx, my) in reachable:
            d = abs(mx - nearest.x) + abs(my - nearest.y)
            if d < best_d:
                best_d = d
                best = (mx, my)

        if best and best != (unit.x, unit.y):
            unit.x, unit.y = best

    def _process_ally(self, unit):
        """Allies prefer to heal low-HP friends, otherwise attack."""
        gs = self.gs
        gmap = gs.game_map
        reachable = gmap.get_movement_range(unit.x, unit.y, unit.move, unit.unit_class)
        reachable -= {(u.x, u.y) for u in gs.all_units() if u.alive and u.faction == unit.faction and u != unit}

        w = unit.equipped
        if w and w.weapon_type == WEAPON_STAFF:
            # Healer: find most injured ally
            from game.combat import resolve_heal
            best_target = None
            worst_hp_pct = 1.0
            for (mx, my) in reachable:
                for friend in gs.player_units + gs.ally_units:
                    if not friend.alive or friend == unit:
                        continue
                    dist = abs(mx - friend.x) + abs(my - friend.y)
                    if dist == 1:
                        pct = friend.hp / friend.max_hp
                        if pct < worst_hp_pct:
                            worst_hp_pct = pct
                            best_target = friend
                            best_move = (mx, my)
            if best_target and worst_hp_pct < 0.85:
                unit.x, unit.y = best_move
                resolve_heal(unit, best_target)
                return

        # Otherwise attack
        self._process_unit(unit)
