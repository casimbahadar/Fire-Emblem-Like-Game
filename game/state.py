'''
Game state management for Sengoku Tactics
Includes: recruit mechanic, reinforcement waves, flying/mounted movement
'''
import copy
from game.constants import *
from game.chapter import CHAPTERS
from game.unit import create_unit_roster, create_mercenary
from game.ai import EnemyAI
from game.combat import resolve_combat, resolve_heal
from game.dialogs import get_pre_combat_dialog, reset_dialog_flags
from game.tutorial import TutorialManager


class GameState:
    def __init__(self):
        self.roster         = create_unit_roster()
        self.chapter_index  = 0
        self.current_chapter= None
        self.game_map       = None
        self.player_units   = []
        self.enemy_units    = []
        self.ally_units     = []
        self.reinforce_waves= []

        self.turn        = 1
        self.phase       = FACTION_PLAYER
        self.state       = STATE_TITLE

        # ── Economy ───────────────────────────────────────────────────────────
        self.gold = STARTING_GOLD

        # ── Deployment mode ───────────────────────────────────────────────────
        # DEPLOY_FORCED: chapter-defined required units; DEPLOY_FREE: player picks any
        self.deploy_mode = DEPLOY_FORCED

        # ── Persistent roster for free-deploy (all unlocked named units) ──────
        # Accumulated across chapters — new characters added here on unlock
        self.free_roster: list = []

        # ── Prep-screen state ─────────────────────────────────────────────────
        self.prep_available_units: list = []
        self.prep_selected_units: list  = []
        self.prep_mercs: list           = []
        self.prep_tab       = PREP_TAB_DEPLOY
        self.prep_cursor    = 0
        self.prep_max_mercs = 3

        # ── Side objectives ───────────────────────────────────────────────────
        # Current chapter active side objectives (reset each chapter)
        self.active_side_objectives: list = []
        # Persistent set of completed side objective IDs (carried across chapters)
        self.completed_obj_ids: set = set()

        self.selected_unit   = None
        self.cursor_x        = 0
        self.cursor_y        = 0
        self.move_range      = set()
        self.move_range_land = set()
        self.attack_range    = set()
        self.cursor_mode     = CURSOR_FREE

        self.combat_log  = []
        self.last_combat = None
        self.message_queue = []
        self.level_up_queue= []   # list of (unit, gains_dict)

        self.victory = False
        self.defeat  = False

        self.ai_controller = None

        # Stat sheet target
        self.stat_sheet_unit = None

        # Defend-mode turn tracker
        self._defend_turns_survived = 0

        # Boss dialog reset
        reset_dialog_flags()

        # Persistent roster across chapters (survivors carry forward)
        self._chapter_survivors = {}

        # Game mode: True = Classic (permadeath), False = Casual (revive next chapter)
        self.classic_mode = True

        # Casual mode: units killed this chapter are tracked for revival next chapter
        self._casual_dead = []

        # Tutorial
        self.tutorial = TutorialManager()

        # Pre-battle scene dialog state
        self.scene_dialog     = []   # list of (speaker_key, display_name, line)
        self.scene_dialog_idx = 0    # current line being shown

        # Boss dialog state
        self.pending_dialog       = None   # list of (speaker, text) or None
        self.pending_dialog_idx   = 0
        self.pending_dialog_atk   = None   # attacker unit after dialog
        self.pending_dialog_def   = None   # defender unit after dialog

    # ── Chapter Loading ───────────────────────────────────────────────────────

    def load_chapter(self, index):
        self.chapter_index   = index
        self.current_chapter = CHAPTERS[index]
        ch = self.current_chapter

        # Build the full chapter data (map + all unit placements)
        gmap, players, enemies, allies, waves, side_objs = ch.build(self.roster)

        # Casual mode: revive player units that died last chapter at full HP
        if not self.classic_mode and self._casual_dead:
            alive_ids = {u.unit_id for u in players}
            for dead_u in self._casual_dead:
                if dead_u.unit_id not in alive_ids:
                    dead_u.hp = dead_u.max_hp
                    dead_u.alive = True
                    dead_u.faction = FACTION_PLAYER
                    dead_u.x, dead_u.y = 0, 0
                    players.append(dead_u)
            self._casual_dead = []

        self.game_map       = gmap
        self.enemy_units    = enemies
        self.ally_units     = allies
        self.reinforce_waves= waves

        # ── Side objectives (filter by chain prerequisites) ───────────────────
        self.active_side_objectives = [
            so for so in side_objs
            if all(r in self.completed_obj_ids for r in so.requires)
        ]

        # ── Prep screen initialisation ────────────────────────────────────────
        limit = ch.deploy_limit

        if self.deploy_mode == DEPLOY_FREE and self.free_roster:
            # Free mode: player picks from their accumulated roster
            import copy as _cp
            avail = []
            seen = set()
            for u in self.free_roster:
                if u.unit_id not in seen and u.alive:
                    avail.append(_cp.deepcopy(u))
                    seen.add(u.unit_id)
            # Also include any new chapter-specific characters
            for u in players:
                if u.unit_id not in seen:
                    avail.append(u)
                    seen.add(u.unit_id)
            self.prep_available_units = avail
            # Required forced units (lord etc.) auto-selected first
            forced_ids = set(ch.forced_units or [])
            forced = [u for u in avail if u.unit_id in forced_ids]
            others = [u for u in avail if u.unit_id not in forced_ids]
            self.prep_selected_units = (forced + others)[:limit]
        else:
            # Forced mode: chapter decides available pool
            self.prep_available_units = players
            self.prep_selected_units  = list(players[:limit])

        self.prep_mercs     = []
        self.prep_tab       = PREP_TAB_DEPLOY
        self.prep_cursor    = 0
        self.prep_max_mercs = max(1, limit - len(self.prep_available_units))

        # Keep player_units empty until prep is confirmed
        self.player_units = []

        self.turn    = 1
        self.phase   = FACTION_PLAYER
        self.victory = False
        self.defeat  = False
        self.combat_log      = []
        self.message_queue   = []
        self.level_up_queue  = []
        self.selected_unit   = None
        self.cursor_mode     = CURSOR_FREE
        self.move_range      = set()
        self.move_range_land = set()
        self.attack_range    = set()
        self.stat_sheet_unit = None
        self._defend_turns_survived = 0

        # ── Flow: scene → prep → chapter intro ───────────────────────────────
        if ch.scene_dialog:
            self.scene_dialog     = ch.scene_dialog
            self.scene_dialog_idx = 0
            self.state = STATE_SCENE
        else:
            self.scene_dialog     = []
            self.scene_dialog_idx = 0
            self.state = STATE_PREP

        self.cursor_x = 0
        self.cursor_y = 0

    def confirm_prep_and_start(self):
        '''
        Called when the player hits 'Battle!' on the prep screen.
        Deploys selected named units + purchased mercs onto the map
        using the chapter's player_unit_defs placement data.
        '''
        ch = self.current_chapter
        import copy as _copy

        # Build id→position map from chapter's original unit defs
        pos_map = {uid: (x, y) for uid, x, y in ch.player_unit_defs}

        deployed = []
        for u in self.prep_selected_units:
            if u.unit_id in pos_map:
                u.x, u.y = pos_map[u.unit_id]
            else:
                # Shouldn't happen, but just in case
                u.x, u.y = 0, 0
            deployed.append(u)

        # Place mercs at the first few spawn positions not taken by named units
        taken_positions = {(u.x, u.y) for u in deployed}
        # Use last positions in player_unit_defs as fallback merc spawn points
        fallback = [(x, y) for _, x, y in ch.player_unit_defs
                    if (x, y) not in taken_positions]
        for i, merc in enumerate(self.prep_mercs):
            if i < len(fallback):
                merc.x, merc.y = fallback[i]
            else:
                merc.x, merc.y = 0, 0
            deployed.append(merc)

        self.player_units = deployed

        # Update free roster with any new named characters from this chapter
        existing_ids = {u.unit_id for u in self.free_roster}
        import copy as _cp
        for u in deployed:
            if not getattr(u, '_is_merc', False) and u.unit_id not in existing_ids:
                self.free_roster.append(_cp.deepcopy(u))
                existing_ids.add(u.unit_id)

        for u in self.all_units():
            u.reset_turn()

        self.ai_controller = EnemyAI(self)
        self.state = STATE_CHAPTER_INTRO

        lords = [u for u in self.player_units if u.is_lord and u.alive]
        if lords:
            self.cursor_x = lords[0].x
            self.cursor_y = lords[0].y

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
        for u in self.player_units + self.ally_units:
            if u.alive:
                u.reset_turn()
        self.check_reinforcements()
        ch = self.current_chapter
        if ch.objective == OBJ_DEFEND:
            self._defend_turns_survived += 1
            needed = ch.turn_limit or 10
            self.push_message(
                f"Turn {self.turn} — {self._defend_turns_survived}/{needed} turns survived.")
        else:
            self.push_message(f"Turn {self.turn} — Player Phase")

    def end_player_turn(self):
        self.selected_unit   = None
        self.move_range      = set()
        self.move_range_land = set()
        self.attack_range    = set()
        self.cursor_mode     = CURSOR_FREE
        self.state = STATE_ENEMY_TURN
        self.phase = FACTION_ENEMY

    def run_enemy_turn(self):
        for u in self.enemy_units:
            if u.alive:
                u.reset_turn()
        self.ai_controller.run_enemy_turn()
        self.check_defeat()
        if not self.defeat:
            self._run_ally_phase()

    def _run_ally_phase(self):
        for u in self.ally_units:
            if u.alive:
                u.reset_turn()
        self.ai_controller.run_ally_turn()
        self.turn += 1
        self.start_player_turn()
        self.check_victory()

    # ── Reinforcements ────────────────────────────────────────────────────────

    def check_reinforcements(self):
        for wave in self.reinforce_waves:
            if wave.triggered:
                continue
            if self.turn == wave.turn:
                new_units = []
                for (uid, x, y) in wave.unit_defs:
                    if uid not in self.roster:
                        continue
                    u = copy.deepcopy(self.roster[uid])
                    u.faction = wave.faction
                    u.x = x
                    u.y = y
                    u.reset_turn()
                    # Make sure spawn tile is not occupied
                    if self.unit_at(x, y) is not None:
                        # Nudge to adjacent free tile
                        placed = False
                        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(1,1),(-1,-1),(1,-1),(-1,1)]:
                            nx, ny = x+dx, y+dy
                            if (0 <= nx < self.game_map.width and
                                0 <= ny < self.game_map.height and
                                self.unit_at(nx, ny) is None):
                                u.x, u.y = nx, ny
                                placed = True
                                break
                        if not placed:
                            continue
                    new_units.append(u)

                if wave.faction == FACTION_ENEMY:
                    self.enemy_units.extend(new_units)
                elif wave.faction == FACTION_ALLY:
                    self.ally_units.extend(new_units)
                else:
                    self.player_units.extend(new_units)

                wave.triggered = True
                self.push_message(wave.message)

    # ── Selection & Movement ─────────────────────────────────────────────────

    def select_unit(self, x, y):
        u = self.unit_at(x, y)
        if (u and u.faction == FACTION_PLAYER and
                u.alive and not u.has_acted):
            self.selected_unit = u
            self.cursor_mode   = CURSOR_UNIT_SEL
            self._compute_ranges(u)
            return True
        return False

    def _compute_ranges(self, unit):
        gmap = self.game_map
        self.move_range = gmap.get_movement_range(
            unit.x, unit.y, unit.move, unit.unit_class,
            is_flying=unit.is_flying,
            is_mounted=unit.is_mounted,
            water_walk=unit.water_walk,
        )
        # Landing squares: can't land on enemy or friendly-occupied
        enemy_tiles   = {(u.x, u.y) for u in self.enemy_units if u.alive}
        friendly_tiles= {(u.x, u.y) for u in self.player_units + self.ally_units
                         if u.alive and u != unit}
        self.move_range_land = (self.move_range - enemy_tiles - friendly_tiles)
        self.move_range_land.add((unit.x, unit.y))

        if unit.equipped:
            mn, mx = unit.attack_range()
            self.attack_range = gmap.get_attack_range_cells(self.move_range_land, mn, mx)
        else:
            self.attack_range = set()

    def move_unit(self, unit, tx, ty):
        if (tx, ty) in self.move_range_land:
            unit.x = tx
            unit.y = ty
            unit.has_moved = True
            self._compute_ranges(unit)
            if unit.faction == FACTION_PLAYER:
                self.check_side_objectives("visit_tile", tile=(tx, ty))
            return True
        return False

    def get_attackable_targets(self, unit):
        if unit.equipped is None:
            return []
        mn, mx = unit.attack_range()
        targets = []
        for t in self.enemy_units:
            if not t.alive:
                continue
            dist = abs(unit.x - t.x) + abs(unit.y - t.y)
            if mn <= dist <= mx:
                targets.append(t)
        return targets

    def get_healable_targets(self, unit):
        w = unit.equipped
        if w is None:
            return []
        is_heal = ("heal" in w.weapon_id or "mend" in w.weapon_id or
                   "physic" in w.weapon_id or "amulet" in w.weapon_id)
        if not is_heal:
            return []
        targets = []
        max_r = w.max_range
        for t in self.player_units + self.ally_units:
            if not t.alive or t == unit:
                continue
            dist = abs(unit.x - t.x) + abs(unit.y - t.y)
            if dist <= max_r and t.hp < t.max_hp:
                targets.append(t)
        return targets

    def get_recruitable_adjacent(self, recruiter):
        '''Return list of adjacent enemy units that recruiter can talk to.'''
        targets = []
        for t in self.enemy_units + self.ally_units:
            if not t.alive or not t.can_recruit or t.recruited:
                continue
            dist = abs(recruiter.x - t.x) + abs(recruiter.y - t.y)
            if dist == 1:
                if ("any" in t.recruit_by or
                        recruiter.unit_id in t.recruit_by):
                    targets.append(t)
        return targets

    # ── Actions ───────────────────────────────────────────────────────────────

    def check_and_trigger_dialog(self, attacker, defender):
        '''Check for pre-combat dialog. Returns True if dialog was triggered.'''
        lines = get_pre_combat_dialog(attacker, defender)
        if lines:
            self.pending_dialog     = lines
            self.pending_dialog_idx = 0
            self.pending_dialog_atk = attacker
            self.pending_dialog_def = defender
            return True
        return False

    def advance_dialog(self):
        '''Advance dialog by one line. Returns True if dialog is complete.'''
        if self.pending_dialog is None:
            return True
        self.pending_dialog_idx += 1
        if self.pending_dialog_idx >= len(self.pending_dialog):
            self.pending_dialog = None
            return True
        return False

    def attack(self, attacker, defender):
        terrain_att = self.game_map.get_terrain(attacker.x, attacker.y)
        terrain_def = self.game_map.get_terrain(defender.x, defender.y)
        result = resolve_combat(attacker, defender, terrain_att, terrain_def)
        self.last_combat = result
        self.combat_log.append(result)

        if not defender.alive:
            self.push_message(f"{defender.name} was defeated!")
            if not self.classic_mode and defender.faction == FACTION_PLAYER:
                self._casual_dead.append(defender)
            if defender.faction == FACTION_ENEMY:
                self.check_side_objectives("kill_unit", unit_id=defender.unit_id)
        if not attacker.alive:
            self.push_message(f"{attacker.name} was defeated!")
            if not self.classic_mode and attacker.faction == FACTION_PLAYER:
                self._casual_dead.append(attacker)

        if result.level_up_att and not attacker.alive is False:
            gains = getattr(attacker, '_last_level_gains', {})
            self.level_up_queue.append((attacker, gains))
            self.push_message(f"{attacker.name} reached Level {attacker.level}!")
        if result.level_up_def and defender.alive:
            gains = getattr(defender, '_last_level_gains', {})
            self.level_up_queue.append((defender, gains))

        attacker.done()
        self.check_victory()
        self.check_defeat()
        return result

    def heal_action(self, healer, target):
        amount = resolve_heal(healer, target)
        healer.done()
        self.push_message(f"{healer.name} healed {target.name} for {amount} HP.")
        return amount

    def recruit_unit(self, recruiter, target):
        '''Recruit a target unit into the player army.'''
        if not target.can_recruit:
            return False
        if "any" not in target.recruit_by and recruiter.unit_id not in target.recruit_by:
            return False

        # Remove from enemy/ally list
        if target in self.enemy_units:
            self.enemy_units.remove(target)
        elif target in self.ally_units:
            self.ally_units.remove(target)

        target.faction   = FACTION_PLAYER
        target.recruited = True
        target.reset_turn()
        self.player_units.append(target)
        # Add to free roster for future chapter availability
        if target.unit_id not in {u.unit_id for u in self.free_roster}:
            import copy as _cp
            self.free_roster.append(_cp.deepcopy(target))
        self.push_message(f"{target.name} has joined your cause!")
        self.check_side_objectives("recruit_unit", unit_id=target.unit_id)
        recruiter.done()
        return True

    # ── Victory / Defeat ─────────────────────────────────────────────────────

    def check_victory(self):
        ch = self.current_chapter
        if self.victory or ch is None:
            return
        if ch.objective == OBJ_ROUT_ENEMY:
            if all(not u.alive for u in self.enemy_units):
                self._trigger_victory()
        elif ch.objective == OBJ_SEIZE:
            pts = self.game_map.seize_points
            for u in self.player_units:
                if not u.alive:
                    continue
                # Any lord can seize, or match seize_unit if specified
                seize_ok = (u.is_lord or
                            u.unit_id == ch.seize_unit or
                            ch.seize_unit == "any")
                if seize_ok and (u.x, u.y) in pts:
                    self._trigger_victory()
        elif ch.objective == OBJ_DEFEAT_BOSS:
            bosses = [u for u in self.enemy_units if u.is_lord]
            if bosses and all(not b.alive for b in bosses):
                self._trigger_victory()
        elif ch.objective == OBJ_DEFEND:
            needed = ch.turn_limit or 10
            if self._defend_turns_survived >= needed:
                self._trigger_victory()

    def check_defeat(self):
        if self.defeat:
            return
        lords = [u for u in self.player_units if u.is_lord]
        if lords and all(not u.alive for u in lords):
            self._trigger_defeat()

    # ── Side Objectives ───────────────────────────────────────────────────────

    def check_side_objectives(self, event_type, **kwargs):
        '''
        Call after relevant game events. event_type is one of:
          "kill_unit", "visit_tile", "recruit_unit", "chapter_end"
        kwargs carry event-specific data.
        '''
        for so in self.active_side_objectives:
            if so.completed or so.failed:
                continue
            triggered = False
            if so.obj_type == "kill_unit" and event_type == "kill_unit":
                triggered = (kwargs.get("unit_id") == so.target)
            elif so.obj_type == "visit_tile" and event_type == "visit_tile":
                triggered = (kwargs.get("tile") == so.target)
            elif so.obj_type == "recruit_unit" and event_type == "recruit_unit":
                triggered = (kwargs.get("unit_id") == so.target)
            elif so.obj_type == "clear_turns" and event_type == "chapter_end":
                triggered = (self.turn <= int(so.target))
            elif so.obj_type == "no_casualties" and event_type == "chapter_end":
                triggered = not any(
                    not u.alive for u in self.player_units
                    if not getattr(u, '_is_merc', False)
                )
            elif so.obj_type == "protect_unit" and event_type == "chapter_end":
                target_alive = any(
                    u.alive for u in self.player_units + self.ally_units
                    if u.unit_id == so.target
                )
                triggered = target_alive

            if triggered:
                so.completed = True
                self.completed_obj_ids.add(so.obj_id)
                self.gold += so.gold_reward
                msg = f"Side Objective: {so.description}"
                if so.gold_reward:
                    msg += f"  (+{so.gold_reward} ryo)"
                self.push_message(msg)
                # Unlock a special character if this obj specifies one
                if so.unlock_unit and so.unlock_unit in self.roster:
                    import copy as _cp
                    new_u = _cp.deepcopy(self.roster[so.unlock_unit])
                    new_u.faction = FACTION_PLAYER
                    if new_u.unit_id not in {u.unit_id for u in self.free_roster}:
                        self.free_roster.append(new_u)
                    self.push_message(
                        f"{new_u.name} will be available from the next chapter!")

    def _trigger_victory(self):
        if not self.victory:
            self.victory = True
            self.state   = STATE_VICTORY
            self.gold   += GOLD_PER_CHAPTER
            # Check end-of-chapter side objectives
            self.check_side_objectives("chapter_end")
            self.push_message(f"Victory!  (+{GOLD_PER_CHAPTER} gold)")

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
