'''
Combat Animation State Machine for Sengoku Tactics.
Drives the full-screen battle cutscene that plays when combat is confirmed.
'''


class CombatAnimState:
    '''Tracks the frame-by-frame state of a battle animation.'''

    # Phase durations (in frames at 60 FPS)
    STRIKE_FRAMES = 30    # unit lunges toward target
    RESULT_FRAMES = 40    # damage number / MISS popup
    HP_DRAIN_FRAMES = 25  # HP bar drains to new value
    PAUSE_FRAMES  = 15    # brief pause between rounds
    DONE_WAIT     = -1    # wait for player input

    def __init__(self, attacker, defender, result):
        self.attacker = attacker
        self.defender = defender
        self.result   = result
        self.rounds   = result.rounds

        # HP tracking (animated drain)
        self.att_max_hp = attacker.max_hp
        self.def_max_hp = defender.max_hp
        # Start from pre-combat HP (reconstruct from damage dealt)
        self.att_hp_start = attacker.hp
        self.def_hp_start = defender.hp
        # Walk backwards through rounds to find pre-combat HP
        for rnd in reversed(self.rounds):
            if rnd.is_counter and rnd.hit:
                self.att_hp_start += rnd.damage
            elif not rnd.is_counter and rnd.hit:
                self.def_hp_start += rnd.damage
        self.att_hp_display = float(self.att_hp_start)
        self.def_hp_display = float(self.def_hp_start)

        # Target HP for current drain animation
        self._att_hp_target = float(self.att_hp_start)
        self._def_hp_target = float(self.def_hp_start)

        # Animation state
        self.round_idx   = 0
        self.phase       = "strike"   # strike → result → hp_drain → pause → next
        self.phase_timer = 0
        self.finished    = False

    @property
    def current_round(self):
        if self.round_idx < len(self.rounds):
            return self.rounds[self.round_idx]
        return None

    def update(self):
        '''Advance one frame. Call every game tick.'''
        if self.finished:
            return

        self.phase_timer += 1

        if self.phase == "strike":
            if self.phase_timer >= self.STRIKE_FRAMES:
                self.phase = "result"
                self.phase_timer = 0
                # Set HP drain target based on this round's damage
                rnd = self.current_round
                if rnd and rnd.hit:
                    if rnd.is_counter:
                        self._att_hp_target = max(0,
                            self._att_hp_target - rnd.damage)
                    else:
                        self._def_hp_target = max(0,
                            self._def_hp_target - rnd.damage)

        elif self.phase == "result":
            if self.phase_timer >= self.RESULT_FRAMES:
                self.phase = "hp_drain"
                self.phase_timer = 0

        elif self.phase == "hp_drain":
            # Smoothly drain HP bars
            t = min(1.0, self.phase_timer / self.HP_DRAIN_FRAMES)
            # Lerp toward target
            prev_att = self.att_hp_display
            prev_def = self.def_hp_display
            if self._att_hp_target < self.att_hp_display:
                self.att_hp_display = max(self._att_hp_target,
                    self.att_hp_display - (self.att_max_hp / self.HP_DRAIN_FRAMES))
            if self._def_hp_target < self.def_hp_display:
                self.def_hp_display = max(self._def_hp_target,
                    self.def_hp_display - (self.def_max_hp / self.HP_DRAIN_FRAMES))

            if self.phase_timer >= self.HP_DRAIN_FRAMES:
                # Snap to target
                self.att_hp_display = self._att_hp_target
                self.def_hp_display = self._def_hp_target
                self.phase = "pause"
                self.phase_timer = 0

        elif self.phase == "pause":
            if self.phase_timer >= self.PAUSE_FRAMES:
                # Move to next round or finish
                self.round_idx += 1
                if self.round_idx < len(self.rounds):
                    self.phase = "strike"
                    self.phase_timer = 0
                else:
                    self.phase = "done"
                    self.phase_timer = 0

        elif self.phase == "done":
            # Wait for player input (dismiss)
            pass

    def dismiss(self):
        '''Player pressed confirm — end the animation.'''
        if self.phase == "done":
            self.finished = True
        else:
            # Skip to end immediately
            self.att_hp_display = self.attacker.hp
            self.def_hp_display = self.defender.hp
            self.round_idx = len(self.rounds) - 1
            self.phase = "done"
            self.phase_timer = 0
