"""
Unit definitions for Sengoku Tactics
"""
import math
from game.constants import *
from game.weapon import get_weapon


class Unit:
    def __init__(self, unit_id, name, unit_class, faction, level=1,
                 weapon_ids=None, portrait_color=None, bio="", is_lord=False):
        self.unit_id   = unit_id
        self.name      = name
        self.unit_class= unit_class
        self.faction   = faction
        self.level     = level
        self.is_lord   = is_lord  # lord death = game over
        self.bio       = bio

        # Load class data
        cd = CLASS_DATA[unit_class]
        self.symbol    = cd["symbol"]
        self.color     = portrait_color or cd["color"]
        self.move      = cd["move"]
        self.allowed_weapons = cd["weapons"]

        # Compute stats with level scaling
        self.max_hp  = cd["hp"]  + (level - 1) * 2
        self.str_    = cd["str"] + (level - 1) * 1
        self.mag     = cd["mag"] + (level - 1) * 1
        self.skl     = cd["skl"] + (level - 1) * 1
        self.spd     = cd["spd"] + (level - 1) * 1
        self.lck     = cd["lck"] + (level - 1) * 1
        self.def_    = cd["def"] + (level - 1) * 1
        self.res     = cd["res"] + (level - 1) * 1

        self.hp      = self.max_hp
        self.exp     = 0

        # Weapons inventory (list of Weapon objects)
        self.weapons  = []
        if weapon_ids:
            for wid in weapon_ids:
                self.weapons.append(get_weapon(wid))
        self.equipped_weapon_index = 0

        # Position on map
        self.x = 0
        self.y = 0

        # State flags
        self.has_moved    = False
        self.has_acted    = False
        self.alive        = True

    # ── Equipment ────────────────────────────────────────────────────────────

    @property
    def equipped(self):
        if not self.weapons:
            return None
        return self.weapons[self.equipped_weapon_index]

    def equip(self, index):
        if 0 <= index < len(self.weapons):
            self.equipped_weapon_index = index

    # ── Combat Stats ─────────────────────────────────────────────────────────

    def attack_power(self, enemy_weapon=None):
        w = self.equipped
        if w is None:
            return self.str_
        if w.weapon_type == WEAPON_STAFF:
            base = self.mag + w.might
        else:
            base = self.str_ + w.might
        tri = w.get_triangle_bonus(enemy_weapon) if enemy_weapon else 0
        return base + tri * 1  # +1 or -1 bonus

    def hit_rate(self, enemy_weapon=None):
        w = self.equipped
        if w is None:
            return 0
        weapon_hit = w.hit + self.skl * 2 + self.lck // 2
        tri = w.get_triangle_bonus(enemy_weapon) if enemy_weapon else 0
        return min(100, weapon_hit + tri * 15)

    def avoid(self):
        terrain_avo = getattr(self, '_terrain_avo', 0)
        w = self.equipped
        weight_pen = 0
        if w and w.weight > self.str_ // 2:
            weight_pen = w.weight - self.str_ // 2
        effective_spd = max(0, self.spd - weight_pen)
        return effective_spd * 2 + self.lck + terrain_avo

    def crit_rate(self, enemy_weapon=None):
        w = self.equipped
        if w is None:
            return 0
        return max(0, w.crit + self.skl // 2 - (self.level // 4))

    def crit_avoid(self):
        return self.lck

    def defense(self):
        terrain_def = getattr(self, '_terrain_def', 0)
        w = self.equipped
        if w and w.weapon_type == WEAPON_STAFF:
            return self.res + terrain_def
        return self.def_ + terrain_def

    def attack_range(self):
        w = self.equipped
        if w is None:
            return (1, 1)
        return (w.min_range, w.max_range)

    def set_terrain_bonuses(self, def_bonus, avo_bonus):
        self._terrain_def = def_bonus
        self._terrain_avo = avo_bonus

    # ── Turn Management ───────────────────────────────────────────────────────

    def reset_turn(self):
        self.has_moved = False
        self.has_acted = False

    def done(self):
        self.has_moved = True
        self.has_acted = True

    # ── Experience ────────────────────────────────────────────────────────────

    def gain_exp(self, amount):
        self.exp += amount
        leveled = False
        while self.exp >= 100:
            self.exp -= 100
            self._level_up()
            leveled = True
        return leveled

    def _level_up(self):
        self.level += 1
        cd = CLASS_DATA[self.unit_class]
        # Stat increases (simplified — fixed growth)
        growths = {
            "hp":  50, "str": 40, "mag": 30, "skl": 45,
            "spd": 45, "lck": 35, "def": 35, "res": 25
        }
        import random
        if random.randint(1, 100) <= growths["hp"]:  self.max_hp += 1; self.hp += 1
        if random.randint(1, 100) <= growths["str"]: self.str_  += 1
        if random.randint(1, 100) <= growths["mag"]: self.mag   += 1
        if random.randint(1, 100) <= growths["skl"]: self.skl   += 1
        if random.randint(1, 100) <= growths["spd"]: self.spd   += 1
        if random.randint(1, 100) <= growths["lck"]: self.lck   += 1
        if random.randint(1, 100) <= growths["def"]: self.def_  += 1
        if random.randint(1, 100) <= growths["res"]: self.res   += 1

    # ── Healing ───────────────────────────────────────────────────────────────

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.alive = False

    def __repr__(self):
        return f"<Unit {self.name} [{self.unit_class}] Lv{self.level} HP:{self.hp}/{self.max_hp}>"


# ─── Sengoku Historical Officers ─────────────────────────────────────────────

def create_unit_roster():
    """Return a dict of unit_id -> Unit for all defined officers."""
    units = {}

    # ── Oda Clan (Player) ────────────────────────────────────────────────────
    units["nobunaga"] = Unit(
        "nobunaga", "Oda Nobunaga", CLASS_DAIMYO, FACTION_PLAYER, level=10,
        weapon_ids=["masamune", "iron_yari"],
        portrait_color=(200, 80, 30),
        bio="The Demon King of the Sixth Heaven. Unifier of Japan by fire and iron.",
        is_lord=True
    )
    units["hideyoshi"] = Unit(
        "hideyoshi", "Toyotomi Hideyoshi", CLASS_SAMURAI, FACTION_PLAYER, level=7,
        weapon_ids=["steel_katana", "iron_tanto"],
        portrait_color=(200, 160, 50),
        bio="From sandal-bearer to regent. Wit sharper than any blade."
    )
    units["mitsuhide"] = Unit(
        "mitsuhide", "Akechi Mitsuhide", CLASS_RONIN, FACTION_PLAYER, level=8,
        weapon_ids=["steel_katana", "silver_katana"],
        portrait_color=(80, 80, 160),
        bio="The Brilliant General. His loyalty has yet to be tested."
    )
    units["katsuie"] = Unit(
        "katsuie", "Shibata Katsuie", CLASS_BERSERKER, FACTION_PLAYER, level=7,
        weapon_ids=["steel_tetsubo", "iron_nodachi"],
        portrait_color=(160, 60, 60),
        bio="The Devil Shibata. Unmatched in brute strength."
    )
    units["nagahide"] = Unit(
        "nagahide", "Niwa Nagahide", CLASS_SPEARMAN, FACTION_PLAYER, level=6,
        weapon_ids=["steel_yari", "iron_naginata"],
        portrait_color=(80, 140, 80),
        bio="One of Nobunaga's trusted administrators and generals."
    )
    units["ranmaru"] = Unit(
        "ranmaru", "Mori Ranmaru", CLASS_NINJA, FACTION_PLAYER, level=5,
        weapon_ids=["iron_tanto", "iron_bow"],
        portrait_color=(200, 130, 160),
        bio="Nobunaga's devoted page. Quick as the wind."
    )
    units["nene"] = Unit(
        "nene", "Nene", CLASS_KUNOICHI, FACTION_PLAYER, level=5,
        weapon_ids=["kunai", "iron_bow"],
        portrait_color=(230, 160, 200),
        bio="Wife of Hideyoshi. Her network of informants is unrivaled."
    )
    units["ieyasu_ally"] = Unit(
        "ieyasu_ally", "Tokugawa Ieyasu", CLASS_CAVALRY, FACTION_ALLY, level=8,
        weapon_ids=["steel_katana", "steel_yari"],
        portrait_color=(100, 120, 200),
        bio="The Tanuki of Mikawa. Patient, calculating, enduring."
    )

    # ── Takeda Clan (Enemy) ──────────────────────────────────────────────────
    units["shingen"] = Unit(
        "shingen", "Takeda Shingen", CLASS_DAIMYO, FACTION_ENEMY, level=12,
        weapon_ids=["odenta_mitsu", "silver_yari"],
        portrait_color=(160, 30, 30),
        bio="The Tiger of Kai. His cavalry crushes all opposition.",
        is_lord=True
    )
    units["kansuke"] = Unit(
        "kansuke", "Yamamoto Kansuke", CLASS_RONIN, FACTION_ENEMY, level=9,
        weapon_ids=["steel_katana", "iron_yari"],
        portrait_color=(100, 60, 80),
        bio="Shingen's one-eyed strategist. Crippled yet undefeated."
    )
    units["masakage"] = Unit(
        "masakage", "Yamagata Masakage", CLASS_CAVALRY, FACTION_ENEMY, level=8,
        weapon_ids=["steel_yari", "steel_katana"],
        portrait_color=(180, 80, 60),
        bio="One of Shingen's 24 generals. Feared red-armored cavalry."
    )
    units["nobushige"] = Unit(
        "nobushige", "Takeda Nobushige", CLASS_SAMURAI, FACTION_ENEMY, level=7,
        weapon_ids=["steel_katana"],
        portrait_color=(200, 100, 80),
        bio="Shingen's younger brother. Noble and brave."
    )

    # ── Uesugi Clan (Enemy / Rival) ───────────────────────────────────────────
    units["kenshin"] = Unit(
        "kenshin", "Uesugi Kenshin", CLASS_DAIMYO, FACTION_ENEMY, level=12,
        weapon_ids=["silver_katana", "silver_naginata"],
        portrait_color=(100, 140, 220),
        bio="The Dragon of Echigo. Avatar of the war god Bishamonten.",
        is_lord=True
    )
    units["kanetsugu"] = Unit(
        "kanetsugu", "Naoe Kanetsugu", CLASS_SAMURAI, FACTION_ENEMY, level=8,
        weapon_ids=["steel_katana", "iron_naginata"],
        portrait_color=(60, 100, 180),
        bio="Devoted retainer. Wears 'ai' (love) on his helmet."
    )
    units["kagetsora"] = Unit(
        "kagetsora", "Uesugi Kagetsora", CLASS_SPEARMAN, FACTION_ENEMY, level=7,
        weapon_ids=["steel_yari"],
        portrait_color=(80, 120, 200),
        bio="Adopted heir of Kenshin. Caught between two clans."
    )

    # ── Date Clan (Enemy) ─────────────────────────────────────────────────────
    units["masamune"] = Unit(
        "masamune", "Date Masamune", CLASS_DAIMYO, FACTION_ENEMY, level=11,
        weapon_ids=["silver_katana", "silver_yari"],
        portrait_color=(30, 30, 80),
        bio="The One-Eyed Dragon of Oshu. Ambition without bounds.",
        is_lord=True
    )
    units["shigezane"] = Unit(
        "shigezane", "Date Shigezane", CLASS_CAVALRY, FACTION_ENEMY, level=8,
        weapon_ids=["steel_yari", "steel_katana"],
        portrait_color=(60, 60, 140),
        bio="Masamune's cousin and closest friend."
    )

    # ── Shimazu Clan (Enemy) ──────────────────────────────────────────────────
    units["yoshihisa"] = Unit(
        "yoshihisa", "Shimazu Yoshihisa", CLASS_DAIMYO, FACTION_ENEMY, level=10,
        weapon_ids=["steel_nodachi", "steel_yari"],
        portrait_color=(80, 60, 140),
        bio="Leader of the Shimazu. Master of the tsuridono ambush tactic.",
        is_lord=True
    )
    units["yoshihiro"] = Unit(
        "yoshihiro", "Shimazu Yoshihiro", CLASS_BERSERKER, FACTION_ENEMY, level=9,
        weapon_ids=["odenta_mitsu", "steel_tetsubo"],
        portrait_color=(100, 50, 160),
        bio="Demon of Sekigahara. Even wounded he broke through enemy lines."
    )

    # ── Generic units ─────────────────────────────────────────────────────────
    units["ashigaru_e1"] = Unit(
        "ashigaru_e1", "Oda Ashigaru", CLASS_ASHIGARU, FACTION_PLAYER, level=1,
        weapon_ids=["iron_yari"], portrait_color=GREY, bio="A loyal foot soldier."
    )
    units["ashigaru_e2"] = Unit(
        "ashigaru_e2", "Oda Ashigaru", CLASS_ASHIGARU, FACTION_PLAYER, level=1,
        weapon_ids=["iron_yari"], portrait_color=GREY, bio="A loyal foot soldier."
    )
    units["archer_p1"] = Unit(
        "archer_p1", "Oda Archer", CLASS_ARCHER, FACTION_PLAYER, level=2,
        weapon_ids=["iron_bow"], portrait_color=GREEN, bio="Trained bowman."
    )
    units["enemy_ash1"] = Unit(
        "enemy_ash1", "Takeda Ashigaru", CLASS_ASHIGARU, FACTION_ENEMY, level=1,
        weapon_ids=["iron_yari"], portrait_color=(180, 60, 60), bio="Enemy foot soldier."
    )
    units["enemy_ash2"] = Unit(
        "enemy_ash2", "Takeda Ashigaru", CLASS_ASHIGARU, FACTION_ENEMY, level=1,
        weapon_ids=["iron_yari"], portrait_color=(180, 60, 60), bio="Enemy foot soldier."
    )
    units["enemy_ash3"] = Unit(
        "enemy_ash3", "Takeda Ashigaru", CLASS_ASHIGARU, FACTION_ENEMY, level=2,
        weapon_ids=["iron_tetsubo"], portrait_color=(180, 60, 60), bio="Enemy foot soldier."
    )
    units["enemy_cav1"] = Unit(
        "enemy_cav1", "Takeda Cavalryman", CLASS_CAVALRY, FACTION_ENEMY, level=3,
        weapon_ids=["iron_yari", "iron_katana"], portrait_color=(200, 80, 80), bio="Mounted Takeda warrior."
    )
    units["enemy_arch1"] = Unit(
        "enemy_arch1", "Takeda Archer", CLASS_ARCHER, FACTION_ENEMY, level=2,
        weapon_ids=["iron_bow"], portrait_color=(180, 80, 80), bio="Enemy bowman."
    )
    units["enemy_ninja1"] = Unit(
        "enemy_ninja1", "Fuma Shinobi", CLASS_NINJA, FACTION_ENEMY, level=4,
        weapon_ids=["kunai", "iron_tanto"], portrait_color=(40, 40, 40), bio="A shadow warrior."
    )
    units["monk_p1"] = Unit(
        "monk_p1", "Ikko-Ikki Monk", CLASS_SOHEI, FACTION_ENEMY, level=3,
        weapon_ids=["iron_naginata", "heal_staff"], portrait_color=TEAL, bio="A warrior monk of the True Pure Land."
    )
    units["enemy_samurai1"] = Unit(
        "enemy_samurai1", "Uesugi Samurai", CLASS_SAMURAI, FACTION_ENEMY, level=4,
        weapon_ids=["steel_katana"], portrait_color=(80, 100, 200), bio="Veteran of Echigo."
    )
    units["enemy_samurai2"] = Unit(
        "enemy_samurai2", "Uesugi Samurai", CLASS_SAMURAI, FACTION_ENEMY, level=3,
        weapon_ids=["iron_katana"], portrait_color=(80, 100, 200), bio="Veteran of Echigo."
    )
    units["enemy_spear1"] = Unit(
        "enemy_spear1", "Date Spearman", CLASS_SPEARMAN, FACTION_ENEMY, level=3,
        weapon_ids=["iron_yari"], portrait_color=(60, 60, 120), bio="Date foot soldier."
    )
    units["enemy_spear2"] = Unit(
        "enemy_spear2", "Date Spearman", CLASS_SPEARMAN, FACTION_ENEMY, level=2,
        weapon_ids=["iron_naginata"], portrait_color=(60, 60, 120), bio="Date foot soldier."
    )
    units["healer_p1"] = Unit(
        "healer_p1", "Oda Onmyoji", CLASS_ONMYOJI, FACTION_PLAYER, level=4,
        weapon_ids=["heal_staff", "ofuda"], portrait_color=PURPLE, bio="A court mage of the Oda."
    )
    units["enemy_date_cav1"] = Unit(
        "enemy_date_cav1", "Date Cavalryman", CLASS_CAVALRY, FACTION_ENEMY, level=4,
        weapon_ids=["steel_yari", "iron_katana"], portrait_color=(50, 50, 130), bio="Date cavalry."
    )
    units["shimazu_ash1"] = Unit(
        "shimazu_ash1", "Shimazu Ashigaru", CLASS_ASHIGARU, FACTION_ENEMY, level=3,
        weapon_ids=["iron_yari"], portrait_color=(100, 60, 160), bio="Shimazu foot soldier."
    )
    units["shimazu_ash2"] = Unit(
        "shimazu_ash2", "Shimazu Ashigaru", CLASS_ASHIGARU, FACTION_ENEMY, level=3,
        weapon_ids=["iron_tetsubo"], portrait_color=(100, 60, 160), bio="Shimazu foot soldier."
    )
    units["shimazu_archer1"] = Unit(
        "shimazu_archer1", "Shimazu Archer", CLASS_ARCHER, FACTION_ENEMY, level=3,
        weapon_ids=["iron_bow"], portrait_color=(120, 70, 180), bio="Expert Shimazu bowman."
    )

    return units
