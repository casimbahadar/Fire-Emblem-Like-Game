"""
Game state management for Sengoku Tactics
"""
from game.constants import *
from game.chapter import CHAPTERS
from game.unit import create_unit_roster
from game.ai import EnemyAI
from game.combat import resolve_combat, resolve_heal


class GameState:
    def __init__(self):
        self.roster        = create_unit_roster()
        self.chapter_index = 0
        self.current_chapter = None
        self.game_map      = None
        self.player_units  = []
        self.enemy_units   = []
        self.ally_units    = []

        self.turn          = 1
        self.phase         = FACTION_PLAYER
        self.state         = STATE_TITLE

        self.selected_unit  = None
        self.cursor_x       = 0
        self.cursor_y       = 0
        self.move_range     = set()
        self.attack_range   = set()
        self.cursor_mode    = CURSOR_FREE

        self.combat_log     = []   # list of CombatResult (for display)
        self.last_combat    = None
        self.message_queue  = []   # list of str for the message box
        self.turn_count     = 0

        self.victory        = False
        self.defeat         = False

        self.ai_controller  = None

        # Survivors carry between chapters
        self._survivors     = {}

    # ── Chapter Loading ───────────────────────────────────────────────────────

    def load_chapter(self, index):
        self.chapter_index = index
        self.current_chapter = CHAPTERS[index]
        gmap, players, enemies, allies = self.current_chapter.build(self.roster)

        self.game_map     = gmap
        self.player_units = players
        self.enemy_units  = enemies
        self.ally_units   = allies

        self.turn       = 1
        self.phase      = FACTION_PLAYER
        self.victory    = False
        self.defeat     = False
        self.combat_log = []
        self.message_queue = []
        self.selected_unit = None
        self.cursor_mode = CURSOR_FREE
        self.move_range  = set()
        self.attack_range = set()

        for u in self.all_units():
            u.reset_turn()

        self.ai_controller = EnemyAI(self)
        self.state = STATE_CHAPTER_INTRO

    def next_chapter(self):
        if self.chapter_index + 1 < len(CHAPTERS):
            self.chapter_index += 1
            self.load_chapter(self.chapter_index)
        else:
            self.state = STATE_VICTORY

    # ── Unit Access ───────────────────────────────────────────────────────────

    def all_units(self):
        return self.player_units + self.enemy_units + self.ally_units

    def unit_at(self, x, y):
        for u in self.all_units():
            if u.alive and u.x == x and u.y == y:
                return u
        return None

    def occupied(self):
        return {(u.x, u.y) for u in self.all_units() if u.alive}

    # ── Phase Management ─────────────────────────────────────────────────────

    def start_player_turn(self):
        self.phase = FACTION_PLAYER
        self.state = STATE_PLAYER_TURN
        for u in self.player_units:
            if u.alive:
                u.reset_turn()
        for u in self.ally_units:
            if u.alive:
                u.reset_turn()
        self.push_message(f"Turn {self.turn} — Player Phase")

    def end_player_turn(self):
        self.selected_unit = None
        self.move_range    = set()
        self.attack_range  = set()
        self.cursor_mode   = CURSOR_FREE
        self.state = STATE_ENEMY_TURN
        self.phase = FACTION_ENEMY

    def run_enemy_turn(self):
        for u in self.enemy_units:
            if u.alive:
                u.reset_turn()
        self.ai_controller.run_enemy_turn()
        self.check_defeat()
        if not self.defeat:
            self.run_ally_turn()

    def run_ally_turn(self):
        for u in self.ally_units:
            if u.alive:
                u.reset_turn()
        self.ai_controller.run_ally_turn()
        self.turn += 1
        self.start_player_turn()

    # ── Selection & Movement ─────────────────────────────────────────────────

    def select_unit(self, x, y):
        u = self.unit_at(x, y)
        if u and u.faction == FACTION_PLAYER and u.alive and not u.has_acted:
            self.selected_unit = u
            self.cursor_mode   = CURSOR_UNIT_SEL
            self._compute_ranges(u)
            return True
        return False

    def _compute_ranges(self, unit):
        gmap = self.game_map
        occupied_others = {(u.x, u.y) for u in self.all_units()
                           if u.alive and u != unit and u.faction != FACTION_PLAYER}
        # Movement range
        self.move_range = gmap.get_movement_range(
            unit.x, unit.y, unit.move, unit.unit_class
        )
        # Remove tiles occupied by enemies (can't land on them)
        enemy_tiles = {(u.x, u.y) for u in self.enemy_units + self.ally_units
                       if u.alive and u.faction != FACTION_PLAYER}
        # Allow passing through allies but not stopping
        friendly_tiles = {(u.x, u.y) for u in self.player_units + self.ally_units
                          if u.alive and u != unit}
        move_land = self.move_range - enemy_tiles - friendly_tiles
        move_land.add((unit.x, unit.y))  # always can stay
        self.move_range_land = move_land

        # Attack range from any reachable landing tile
        if unit.equipped:
            mn, mx = unit.attack_range()
            self.attack_range = gmap.get_attack_range_cells(move_land, mn, mx)
        else:
            self.attack_range = set()

    def move_unit(self, unit, tx, ty):
        if (tx, ty) in self.move_range_land:
            unit.x = tx
            unit.y = ty
            unit.has_moved = True
            self._compute_ranges(unit)
            return True
        return False

    def get_attackable_targets(self, unit):
        """Return list of units attackable from current position."""
        if unit.equipped is None:
            return []
        mn, mx = unit.attack_range()
        targets = []
        for t in self.enemy_units + self.ally_units:
            if not t.alive:
                continue
            if t.faction == FACTION_PLAYER:
                continue
            dist = abs(unit.x - t.x) + abs(unit.y - t.y)
            if mn <= dist <= mx:
                targets.append(t)
        return targets

    def get_healable_targets(self, unit):
        """Return list of allies that can be healed."""
        w = unit.equipped
        if w is None or "heal" not in w.weapon_id and "mend" not in w.weapon_id:
            return []
        targets = []
        for t in self.player_units + self.ally_units:
            if not t.alive or t == unit:
                continue
            dist = abs(unit.x - t.x) + abs(unit.y - t.y)
            if dist == 1 and t.hp < t.max_hp:
                targets.append(t)
        return targets

    def attack(self, attacker, defender):
        terrain_att = self.game_map.get_terrain(attacker.x, attacker.y)
        terrain_def = self.game_map.get_terrain(defender.x, defender.y)
        result = resolve_combat(attacker, defender, terrain_att, terrain_def)
        self.last_combat = result
        self.combat_log.append(result)

        if not defender.alive:
            self.push_message(f"{defender.name} was defeated!")
        if not attacker.alive:
            self.push_message(f"{attacker.name} was defeated!")

        attacker.done()
        self.check_victory()
        self.check_defeat()
        return result

    def heal_action(self, healer, target):
        amount = resolve_heal(healer, target)
        healer.done()
        self.push_message(f"{healer.name} healed {target.name} for {amount} HP.")
        return amount

    # ── Win/Lose Conditions ───────────────────────────────────────────────────

    def check_victory(self):
        ch = self.current_chapter
        if ch.objective == OBJ_ROUT_ENEMY:
            if all(not u.alive for u in self.enemy_units):
                self._trigger_victory()
        elif ch.objective == OBJ_SEIZE:
            seize_pts = self.game_map.seize_points
            for u in self.player_units:
                if u.alive and u.is_lord and (u.x, u.y) in seize_pts:
                    self._trigger_victory()
        elif ch.objective == OBJ_DEFEAT_BOSS:
            # Boss is the first enemy unit with is_lord flag
            bosses = [u for u in self.enemy_units if u.is_lord]
            if bosses and all(not b.alive for b in bosses):
                self._trigger_victory()

    def check_defeat(self):
        lords = [u for u in self.player_units if u.is_lord]
        if lords and all(not u.alive for u in lords):
            self._trigger_defeat()
        # Also check turn limit
        ch = self.current_chapter
        if ch.turn_limit and self.turn > ch.turn_limit:
            self._trigger_defeat()

    def _trigger_victory(self):
        if not self.victory:
            self.victory = True
            self.state   = STATE_VICTORY
            self.push_message("Victory!")

    def _trigger_defeat(self):
        if not self.defeat:
            self.defeat = True
            self.state  = STATE_GAME_OVER
            self.push_message("Defeat...")

    # ── Messages ──────────────────────────────────────────────────────────────

    def push_message(self, msg):
        self.message_queue.append(msg)

    def pop_message(self):
        if self.message_queue:
            return self.message_queue.pop(0)
        return None
