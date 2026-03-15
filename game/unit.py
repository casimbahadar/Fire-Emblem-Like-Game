"""
Unit definitions for Sengoku Tactics
Inspired by Samurai Warriors characters — each unit has a personality archetype,
iconic weapon, and Samurai Warriors-style bio flavor.
"""
import random
import copy
from game.constants import *
from game.weapon import get_weapon


class Unit:
    def __init__(self, unit_id, name, unit_class, faction, level=1,
                 weapon_ids=None, portrait_color=None, bio="",
                 is_lord=False, archetype=ARCHETYPE_HERO,
                 can_recruit=False, recruit_by=None,
                 growth_rates=None, quote=""):
        self.unit_id   = unit_id
        self.name      = name
        self.unit_class= unit_class
        self.faction   = faction
        self.level     = level
        self.is_lord   = is_lord
        self.bio       = bio
        self.archetype = archetype
        self.quote     = quote  # Samurai Warriors-style battle quote

        # Recruit flags
        self.can_recruit  = can_recruit   # Can this unit be recruited?
        self.recruit_by   = recruit_by or ["any"]  # list of unit_ids or ["any"]
        self.recruited    = False

        # Load class data
        cd = CLASS_DATA[unit_class]
        self.symbol      = cd["symbol"]
        self.color       = portrait_color or cd["color"]
        self.move        = cd["move"]
        self.allowed_weapons = cd["weapons"]
        self.is_flying   = cd.get("flying", False)
        self.is_mounted  = cd.get("mounted", False) or unit_class in MOUNTED_CLASSES
        self.water_walk  = cd.get("water_walk", False) or unit_class in WATER_CLASSES

        # Growth rates (for level up)
        default_growths = {"hp": 50, "str": 40, "mag": 30, "skl": 45,
                           "spd": 45, "lck": 35, "def": 35, "res": 25}
        self.growths = growth_rates or default_growths

        # Compute base stats with level scaling
        scale = level - 1
        self.max_hp = cd["hp"]  + scale * 2
        self.str_   = cd["str"] + scale * 1
        self.mag    = cd["mag"] + scale * 1
        self.skl    = cd["skl"] + scale * 1
        self.spd    = cd["spd"] + scale * 1
        self.lck    = cd["lck"] + scale * 1
        self.def_   = cd["def"] + scale * 1
        self.res    = cd["res"] + scale * 1
        self.hp     = self.max_hp
        self.exp    = 0

        # Weapon inventory
        self.weapons = []
        if weapon_ids:
            for wid in weapon_ids:
                try:
                    self.weapons.append(get_weapon(wid))
                except KeyError:
                    pass
        self.equipped_weapon_index = 0

        # Map position
        self.x = 0
        self.y = 0

        # State flags
        self.has_moved = False
        self.has_acted = False
        self.alive     = True

        # Terrain bonus cache
        self._terrain_def = 0
        self._terrain_avo = 0

    # ── Equipment ─────────────────────────────────────────────────────────────

    @property
    def equipped(self):
        if not self.weapons:
            return None
        return self.weapons[self.equipped_weapon_index]

    def equip(self, index):
        if 0 <= index < len(self.weapons):
            self.equipped_weapon_index = index

    def can_use_weapon(self, weapon):
        return weapon.weapon_type in self.allowed_weapons

    # ── Combat Stats ──────────────────────────────────────────────────────────

    def attack_power(self, enemy_weapon=None, target=None):
        w = self.equipped
        if w is None:
            return self.str_
        if w.magic_damage:
            base = self.mag + w.might
        elif w.weapon_type == WEAPON_STAFF and "heal" in w.weapon_id:
            base = self.mag + 10
        else:
            base = self.str_ + w.might
        tri = w.get_triangle_bonus(enemy_weapon) if enemy_weapon else 0
        bonus = tri * 1
        # Anti-type bonuses
        if target:
            if w.anti_flying and target.is_flying:
                bonus += 5
            if w.anti_mounted and target.is_mounted:
                bonus += 5
        return base + bonus

    def hit_rate(self, enemy_weapon=None):
        w = self.equipped
        if w is None:
            return 0
        weapon_hit = w.hit + self.skl * 2 + self.lck // 2
        tri = w.get_triangle_bonus(enemy_weapon) if enemy_weapon else 0
        return min(100, weapon_hit + tri * 15)

    def avoid(self):
        w = self.equipped
        weight_pen = 0
        if w and not w.magic_damage:
            overage = w.weight - self.str_ // 2
            if overage > 0:
                weight_pen = overage
        effective_spd = max(0, self.spd - weight_pen)
        return effective_spd * 2 + self.lck + self._terrain_avo

    def crit_rate(self, enemy_weapon=None):
        w = self.equipped
        if w is None:
            return 0
        return max(0, w.crit + self.skl // 2 - self.level // 4)

    def crit_avoid(self):
        return self.lck

    def defense(self):
        w = self.equipped
        if w and w.magic_damage:
            return self.res + self._terrain_def
        return self.def_ + self._terrain_def

    def attack_range(self):
        w = self.equipped
        if w is None:
            return (1, 1)
        return (w.min_range, w.max_range)

    def set_terrain_bonuses(self, def_bonus, avo_bonus):
        # Flying units ignore terrain bonuses (but also get no bonuses)
        if self.is_flying:
            self._terrain_def = 0
            self._terrain_avo = 0
        else:
            self._terrain_def = def_bonus
            self._terrain_avo = avo_bonus

    # ── Turn Management ───────────────────────────────────────────────────────

    def reset_turn(self):
        self.has_moved = False
        self.has_acted = False

    def done(self):
        self.has_moved = True
        self.has_acted = True

    # ── EXP & Level Up ────────────────────────────────────────────────────────

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
        g = self.growths
        gains = {}
        if random.randint(1,100) <= g.get("hp",  50): self.max_hp += 1; self.hp += 1; gains["HP"] = 1
        if random.randint(1,100) <= g.get("str", 40): self.str_  += 1; gains["STR"] = 1
        if random.randint(1,100) <= g.get("mag", 30): self.mag   += 1; gains["MAG"] = 1
        if random.randint(1,100) <= g.get("skl", 45): self.skl   += 1; gains["SKL"] = 1
        if random.randint(1,100) <= g.get("spd", 45): self.spd   += 1; gains["SPD"] = 1
        if random.randint(1,100) <= g.get("lck", 35): self.lck   += 1; gains["LCK"] = 1
        if random.randint(1,100) <= g.get("def", 35): self.def_  += 1; gains["DEF"] = 1
        if random.randint(1,100) <= g.get("res", 25): self.res   += 1; gains["RES"] = 1
        self._last_level_gains = gains
        return gains

    # ── Health ────────────────────────────────────────────────────────────────

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.alive = False

    def __repr__(self):
        return f"<Unit {self.name} [{self.unit_class}] Lv{self.level} HP:{self.hp}/{self.max_hp}>"


# ─────────────────────────────────────────────────────────────────────────────
# Full Sengoku Roster — Samurai Warriors inspired characterizations
# ─────────────────────────────────────────────────────────────────────────────

def create_unit_roster():
    units = {}

    # ══════════════════════════════════════════════════════════════════════════
    # ODA CLAN — PLAYER UNITS
    # ══════════════════════════════════════════════════════════════════════════

    units["nobunaga"] = Unit(
        "nobunaga", "Oda Nobunaga", CLASS_DAIMYO, FACTION_PLAYER, level=10,
        weapon_ids=["masamune", "iron_yari"],
        portrait_color=(200, 80, 30),
        archetype=ARCHETYPE_AMBITIOUS,
        bio=("The Demon King of the Sixth Heaven. Brutal visionary who would\n"
             "shatter tradition with gunpowder and iron will. He calls himself\n"
             "a demon, but his brilliance cannot be denied."),
        quote="The old order crumbles before me. Only the strong survive!",
        is_lord=True,
        growth_rates={"hp":70,"str":65,"mag":35,"skl":60,"spd":55,"lck":50,"def":60,"res":30}
    )
    units["hideyoshi"] = Unit(
        "hideyoshi", "Toyotomi Hideyoshi", CLASS_SAMURAI, FACTION_PLAYER, level=7,
        weapon_ids=["steel_katana", "iron_tanto"],
        portrait_color=(200, 160, 50),
        archetype=ARCHETYPE_FREE,
        bio=("From sandal-bearer to regent — Hideyoshi's rise is Japan's greatest\n"
             "rags-to-riches story. Cunning and cheerful, he wins allies with\n"
             "charm as readily as swords."),
        quote="Every sunrise is a new chance to reach the top!",
        growth_rates={"hp":60,"str":55,"mag":30,"skl":60,"spd":60,"lck":65,"def":45,"res":30}
    )
    units["mitsuhide"] = Unit(
        "mitsuhide", "Akechi Mitsuhide", CLASS_RONIN, FACTION_PLAYER, level=8,
        weapon_ids=["steel_katana", "silver_katana"],
        portrait_color=(80, 80, 160),
        archetype=ARCHETYPE_NOBLE,
        bio=("The Brilliant General of the Oda. Cultured, precise, deeply loyal\n"
             "to tradition. He serves Nobunaga faithfully — but his lord's contempt\n"
             "gnaws at something deep within him."),
        quote="I fight with reason, not rage. And that makes me more dangerous.",
        growth_rates={"hp":50,"str":60,"mag":25,"skl":75,"spd":65,"lck":40,"def":55,"res":30}
    )
    units["katsuie"] = Unit(
        "katsuie", "Shibata Katsuie", CLASS_BERSERKER, FACTION_PLAYER, level=7,
        weapon_ids=["steel_tetsubo", "iron_nodachi"],
        portrait_color=(160, 60, 60),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("'The Devil Shibata' — no castle has stood against his charge,\n"
             "no army has broken his will. Gruff, fearless, and completely\n"
             "devoted to Nobunaga's cause."),
        quote="Out of my way! I'll smash through anything — man, wall, or mountain!",
        growth_rates={"hp":80,"str":75,"mag":10,"skl":45,"spd":45,"lck":25,"def":70,"res":15}
    )
    units["nagahide"] = Unit(
        "nagahide", "Niwa Nagahide", CLASS_SPEARMAN, FACTION_PLAYER, level=6,
        weapon_ids=["steel_yari", "iron_naginata"],
        portrait_color=(80, 140, 80),
        archetype=ARCHETYPE_LOYAL,
        bio=("Trusted administrator and general of the Oda. Where others rush\n"
             "headlong into glory, Nagahide ensures the army is fed, supplied,\n"
             "and properly positioned."),
        quote="Victory is built on preparation. Let us be thorough.",
        growth_rates={"hp":60,"str":55,"mag":15,"skl":55,"spd":50,"lck":45,"def":60,"res":30}
    )
    units["ranmaru"] = Unit(
        "ranmaru", "Mori Ranmaru", CLASS_NINJA, FACTION_PLAYER, level=5,
        weapon_ids=["iron_tanto", "iron_bow"],
        portrait_color=(200, 130, 160),
        archetype=ARCHETYPE_LOYAL,
        bio=("Nobunaga's devoted page. His loyalty transcends all reason —\n"
             "where Nobunaga walks, Ranmaru is his shadow, his shield,\n"
             "and if need be, his final guardian."),
        quote="Lord Nobunaga's path is my path. I will not falter!",
        growth_rates={"hp":40,"str":50,"mag":25,"skl":80,"spd":75,"lck":60,"def":30,"res":40}
    )
    units["nene"] = Unit(
        "nene", "Nene", CLASS_KUNOICHI, FACTION_PLAYER, level=5,
        weapon_ids=["kunai", "iron_bow"],
        portrait_color=(230, 160, 200),
        archetype=ARCHETYPE_FREE,
        bio=("Wife of Hideyoshi, spy-mistress of the Oda, and everyone's\n"
             "surprisingly competent big sister. Her network of informants\n"
             "stretches across all provinces."),
        quote="You underestimate me because I smile. That's my greatest weapon.",
        growth_rates={"hp":40,"str":45,"mag":40,"skl":75,"spd":80,"lck":70,"def":25,"res":55}
    )
    units["oichi"] = Unit(
        "oichi", "Oichi", CLASS_NOBLE_LADY, FACTION_PLAYER, level=5,
        weapon_ids=["heal_staff", "iron_bow"],
        portrait_color=(220, 180, 220),
        archetype=ARCHETYPE_NOBLE,
        bio=("Nobunaga's gentle younger sister. Sent to wed Azai Nagamasa as\n"
             "a political alliance, she carries grace in one hand and quiet\n"
             "tragedy in the other."),
        quote="I pray this war ends before it swallows everyone I love.",
        growth_rates={"hp":40,"str":30,"mag":65,"skl":55,"spd":55,"lck":80,"def":25,"res":70}
    )
    units["toshiie"] = Unit(
        "toshiie", "Maeda Toshiie", CLASS_SPEARMAN, FACTION_PLAYER, level=6,
        weapon_ids=["jumonji_yari", "iron_katana"],
        portrait_color=(60, 160, 200),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("'The Tiger of the Maeda' — Toshiie fights with bold, aggressive\n"
             "strokes. His cross-bladed spear is legendary, and his rivalry\n"
             "with Hideyoshi is equally famous."),
        quote="My spear leads — the rest of the army follows!",
        growth_rates={"hp":65,"str":60,"mag":10,"skl":60,"spd":55,"lck":50,"def":60,"res":25}
    )
    units["no"] = Unit(
        "no", "No (Lady Nōhime)", CLASS_KUNOICHI, FACTION_PLAYER, level=6,
        weapon_ids=["iron_tanto", "heal_staff"],
        portrait_color=(180, 100, 160),
        archetype=ARCHETYPE_MYSTIC,
        bio=("Nobunaga's principal wife. Daughter of the Viper of Mino,\n"
             "No is as sharp as any blade. Rumor says she carries a dagger\n"
             "even at the tea ceremony."),
        quote="Behind this beauty lies a blade. Try me, and find out.",
        growth_rates={"hp":40,"str":45,"mag":55,"skl":70,"spd":75,"lck":75,"def":30,"res":60}
    )
    units["ina"] = Unit(
        "ina", "Ina (Komatsuhime)", CLASS_MOUNTED_ARCHER, FACTION_PLAYER, level=5,
        weapon_ids=["iron_bow", "iron_katana"],
        portrait_color=(160, 200, 160),
        archetype=ARCHETYPE_HERO,
        bio=("Daughter of Honda Tadakatsu. She inherited her father's ferocity\n"
             "and her mother's grace — a mounted archer of extraordinary skill\n"
             "who once barred even Sanada Yukimura at the castle gate."),
        quote="Step back. I never miss.",
        growth_rates={"hp":50,"str":55,"mag":15,"skl":75,"spd":70,"lck":60,"def":50,"res":30}
    )
    units["goemon"] = Unit(
        "goemon", "Ishikawa Goemon", CLASS_NINJA, FACTION_PLAYER, level=5,
        weapon_ids=["kunai", "iron_tanto"],
        portrait_color=(100, 80, 60),
        archetype=ARCHETYPE_FREE,
        bio=("Japan's most famous thief and outlaw-ninja. He steals from the\n"
             "rich, gives to the poor, and somehow ends up on Hideyoshi's\n"
             "side despite being hunted by half of Japan."),
        quote="The greater the danger, the greater the fun. Ha ha!",
        growth_rates={"hp":45,"str":55,"mag":20,"skl":80,"spd":80,"lck":70,"def":30,"res":35}
    )
    units["gracia"] = Unit(
        "gracia", "Gracia (Tama)", CLASS_NOBLE_LADY, FACTION_PLAYER, level=4,
        weapon_ids=["heal_staff", "iron_bow"],
        portrait_color=(200, 200, 240),
        archetype=ARCHETYPE_MYSTIC,
        bio=("Daughter of Akechi Mitsuhide. Her gentle nature belies a fierce\n"
             "spirit — she converted to Christianity and was given the baptismal\n"
             "name Gracia. Even in war, she carries hope."),
        quote="Even in darkness, a single candle can push back the night.",
        growth_rates={"hp":38,"str":25,"mag":70,"skl":55,"spd":60,"lck":80,"def":20,"res":75}
    )
    units["kanbei"] = Unit(
        "kanbei", "Kuroda Kanbei", CLASS_TACTICIAN, FACTION_PLAYER, level=8,
        weapon_ids=["kanbei_scroll", "iron_tanto"],
        portrait_color=(80, 70, 110),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("'The Black Monk' — Hideyoshi's brilliant, one-legged strategist.\n"
             "Kanbei's plans never fail. His eccentricities are legendary:\n"
             "he laughs at the worst moments and weeps at the strangest victories."),
        quote="The enemy's plan is written on their face. I have already won.",
        growth_rates={"hp":40,"str":25,"mag":75,"skl":75,"spd":55,"lck":55,"def":30,"res":70}
    )
    units["kiyomasa"] = Unit(
        "kiyomasa", "Kato Kiyomasa", CLASS_SPEARMAN, FACTION_PLAYER, level=7,
        weapon_ids=["nihongo", "steel_yari"],
        portrait_color=(200, 100, 60),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("'The Tiger Slayer' — Kiyomasa's reputation was forged in the\n"
             "Korean campaign where he allegedly hunted tigers bare-handed.\n"
             "His spear is as long as his stubbornness."),
        quote="If it moves and isn't on our side, my spear will settle the matter!",
        growth_rates={"hp":70,"str":70,"mag":10,"skl":60,"spd":50,"lck":40,"def":65,"res":20}
    )
    units["fukushima"] = Unit(
        "fukushima", "Fukushima Masanori", CLASS_BERSERKER, FACTION_PLAYER, level=6,
        weapon_ids=["steel_tetsubo", "steel_katana"],
        portrait_color=(180, 80, 50),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("Hideyoshi's foster nephew and eternal rival of Kato Kiyomasa.\n"
             "Their argument over who gets to charge first is more dangerous\n"
             "than most enemy armies."),
        quote="Out of the way, Kiyomasa! This kill is MINE!",
        growth_rates={"hp":75,"str":70,"mag":10,"skl":50,"spd":50,"lck":35,"def":65,"res":15}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # TOKUGAWA CLAN — ALLY / PLAYER UNITS
    # ══════════════════════════════════════════════════════════════════════════

    units["ieyasu"] = Unit(
        "ieyasu", "Tokugawa Ieyasu", CLASS_CAVALRY, FACTION_ALLY, level=8,
        weapon_ids=["steel_katana", "steel_yari"],
        portrait_color=(100, 120, 200),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("The Tanuki of Mikawa. Patient as a stone, cunning as a fox.\n"
             "He endured Imagawa hostage years, Oda alliance, and personal\n"
             "tragedy — all to outlast everyone else."),
        quote="He who endures longest, laughs last.",
        growth_rates={"hp":65,"str":60,"mag":25,"skl":55,"spd":55,"lck":60,"def":65,"res":40}
    )
    units["tadakatsu"] = Unit(
        "tadakatsu", "Honda Tadakatsu", CLASS_GENERAL, FACTION_ALLY, level=9,
        weapon_ids=["tonbo_kiri", "iron_tetsubo"],
        portrait_color=(160, 160, 160),
        archetype=ARCHETYPE_LOYAL,
        bio=("Japan's mightiest warrior — Honda Tadakatsu never once received\n"
             "a serious wound in 57 battles. He is Ieyasu's unmovable wall;\n"
             "his tonbo-kiri spear is feared by every army in Japan."),
        quote="Come. All of you. I have not yet begun to fight.",
        growth_rates={"hp":80,"str":70,"mag":10,"skl":60,"spd":45,"lck":45,"def":85,"res":25}
    )
    units["naomasa"] = Unit(
        "naomasa", "Ii Naomasa", CLASS_CAVALRY, FACTION_ALLY, level=7,
        weapon_ids=["steel_yari", "steel_katana"],
        portrait_color=(220, 50, 50),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("The Red Devil — Ii Naomasa's entire army wears crimson armor\n"
             "to strike fear into enemies. He nearly died at Sekigahara but\n"
             "fought until the last enemy fled."),
        quote="Red as blood — my color signals that I am coming for you!",
        growth_rates={"hp":65,"str":65,"mag":15,"skl":60,"spd":65,"lck":45,"def":60,"res":25}
    )
    units["hanzo"] = Unit(
        "hanzo", "Hattori Hanzo", CLASS_NINJA, FACTION_ALLY, level=8,
        weapon_ids=["steel_tanto", "daikyu"],
        portrait_color=(40, 40, 40),
        archetype=ARCHETYPE_MYSTIC,
        bio=("The Demon Ninja — Ieyasu's shadow guardian. Half-legend,\n"
             "half-warrior monk, entirely terrifying. His steel tanto has\n"
             "never left a survivor to describe his face."),
        quote="You saw me. That is unusual. Most don't live to say so.",
        growth_rates={"hp":45,"str":65,"mag":30,"skl":85,"spd":80,"lck":55,"def":40,"res":50}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # SANADA CLAN — RECRUITABLE
    # ══════════════════════════════════════════════════════════════════════════

    units["yukimura"] = Unit(
        "yukimura", "Sanada Yukimura", CLASS_SPEARMAN, FACTION_ENEMY, level=9,
        weapon_ids=["nihongo", "steel_katana"],
        portrait_color=(220, 30, 30),
        archetype=ARCHETYPE_HERO,
        bio=("Japan's greatest hero — the 'Crimson Demon of War' whose final\n"
             "charge at Osaka shook the Tokugawa army to its core. Brave,\n"
             "passionate, and absolutely brilliant with a spear."),
        quote="My spear carries the honor of the Sanada! COME!",
        can_recruit=True, recruit_by=["hideyoshi", "any"],
        growth_rates={"hp":70,"str":70,"mag":15,"skl":70,"spd":65,"lck":55,"def":65,"res":30}
    )
    units["nobuyuki"] = Unit(
        "nobuyuki", "Sanada Nobuyuki", CLASS_SAMURAI, FACTION_ALLY, level=7,
        weapon_ids=["steel_katana", "iron_yari"],
        portrait_color=(180, 50, 50),
        archetype=ARCHETYPE_LOYAL,
        bio=("Yukimura's older brother — calmer, steadier, and ultimately\n"
             "on a different side of the war. Their fraternal bond survives\n"
             "even the divide at Sekigahara."),
        quote="Our family is split by war. But the Sanada name remains unbroken.",
        growth_rates={"hp":60,"str":60,"mag":15,"skl":65,"spd":60,"lck":50,"def":60,"res":30}
    )
    units["masayuki"] = Unit(
        "masayuki", "Sanada Masayuki", CLASS_TACTICIAN, FACTION_ENEMY, level=10,
        weapon_ids=["kanbei_scroll", "iron_tanto"],
        portrait_color=(160, 40, 40),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("The greatest strategist of the Sanada clan. He held Ueda Castle\n"
             "against the Tokugawa twice with a fraction of their numbers.\n"
             "His mind is a labyrinth no enemy has ever navigated safely."),
        quote="You fell into my trap three steps ago. The rest is ceremony.",
        can_recruit=True, recruit_by=["nobunaga", "ieyasu"],
        growth_rates={"hp":45,"str":30,"mag":80,"skl":75,"spd":60,"lck":65,"def":35,"res":70}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # TAKEDA CLAN — ENEMY
    # ══════════════════════════════════════════════════════════════════════════

    units["shingen"] = Unit(
        "shingen", "Takeda Shingen", CLASS_DAIMYO, FACTION_ENEMY, level=12,
        weapon_ids=["odenta_mitsu", "silver_yari"],
        portrait_color=(160, 30, 30),
        archetype=ARCHETYPE_RIVAL,
        bio=("The Tiger of Kai. Master of the cavalry charge, nemesis of Kenshin.\n"
             "His fan — 'Swift as wind, still as forest, fierce as fire,\n"
             "immovable as mountain' — is strategy made poetry."),
        quote="WIND — FOREST — FIRE — MOUNTAIN! Takeda rides!",
        is_lord=True,
        growth_rates={"hp":80,"str":75,"mag":30,"skl":65,"spd":55,"lck":55,"def":70,"res":35}
    )
    units["kansuke"] = Unit(
        "kansuke", "Yamamoto Kansuke", CLASS_RONIN, FACTION_ENEMY, level=9,
        weapon_ids=["steel_katana", "iron_yari"],
        portrait_color=(100, 60, 80),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("Shingen's one-eyed, lame strategist. Rejected by every lord\n"
             "before Shingen — but Shingen saw genius. At Kawanakajima,\n"
             "Kansuke charged into the enemy alone, accepting death as\n"
             "penance for his miscalculation."),
        quote="My body is broken. My mind is not. Attack!",
        growth_rates={"hp":50,"str":65,"mag":20,"skl":75,"spd":60,"lck":30,"def":55,"res":25}
    )
    units["masakage"] = Unit(
        "masakage", "Yamagata Masakage", CLASS_CAVALRY, FACTION_ENEMY, level=8,
        weapon_ids=["steel_yari", "steel_katana"],
        portrait_color=(180, 80, 60),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("Red-armored general of the Takeda cavalry. His charging red\n"
             "horsemen have broken formations that no infantry could stop.\n"
             "He died at Nagashino under the Oda volley fire."),
        quote="Red armor! Red hearts! CHARGE!",
        growth_rates={"hp":65,"str":65,"mag":10,"skl":55,"spd":70,"lck":45,"def":55,"res":20}
    )
    units["nobushige"] = Unit(
        "nobushige", "Takeda Nobushige", CLASS_SAMURAI, FACTION_ENEMY, level=7,
        weapon_ids=["steel_katana"],
        portrait_color=(200, 100, 80),
        archetype=ARCHETYPE_NOBLE,
        bio=("Shingen's younger brother. Brave, principled, and devoted.\n"
             "His 'Ninety-Nine Articles' on military strategy became\n"
             "a cornerstone of samurai philosophy."),
        quote="Honor is not a reward. It is the road itself.",
        growth_rates={"hp":60,"str":60,"mag":20,"skl":65,"spd":60,"lck":55,"def":55,"res":35}
    )
    units["masanobu"] = Unit(
        "masanobu", "Kosaka Masanobu", CLASS_CAVALRY, FACTION_ENEMY, level=8,
        weapon_ids=["silver_yari", "steel_katana"],
        portrait_color=(160, 100, 70),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("'The Keeper of the Northern Army' — Masanobu is the brilliant\n"
             "administrator behind the Takeda war machine. Without him,\n"
             "Shingen's armies would not march half as far."),
        quote="Supply lines are the true sinews of war.",
        growth_rates={"hp":55,"str":55,"mag":30,"skl":65,"spd":60,"lck":55,"def":55,"res":40}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # UESUGI CLAN — ENEMY
    # ══════════════════════════════════════════════════════════════════════════

    units["kenshin"] = Unit(
        "kenshin", "Uesugi Kenshin", CLASS_DAIMYO, FACTION_ENEMY, level=12,
        weapon_ids=["bishamonten", "silver_katana"],
        portrait_color=(100, 140, 220),
        archetype=ARCHETYPE_RIVAL,
        bio=("The Dragon of Echigo. The living avatar of Bishamonten,\n"
             "god of war. He never struck first without cause — but when\n"
             "he struck, no one could stop him. He was Shingen's greatest rival."),
        quote="Bishamonten guides my blade! Who dares stand against the divine?",
        is_lord=True,
        growth_rates={"hp":75,"str":75,"mag":40,"skl":70,"spd":65,"lck":65,"def":65,"res":50}
    )
    units["kanetsugu"] = Unit(
        "kanetsugu", "Naoe Kanetsugu", CLASS_SAMURAI, FACTION_ENEMY, level=8,
        weapon_ids=["raikiri", "iron_naginata"],
        portrait_color=(60, 100, 180),
        archetype=ARCHETYPE_NOBLE,
        bio=("He wears the kanji for 'love' (ai) on his helmet — and means it.\n"
             "Kanetsugu's devotion to Kenshin's ideals of justice outlives\n"
             "even his lord. His blade, Raikiri, cuts like lightning."),
        quote="Love — that is what I fight for. Does that surprise you?",
        can_recruit=True, recruit_by=["kenshin", "nobunaga", "any"],
        growth_rates={"hp":55,"str":65,"mag":30,"skl":70,"spd":65,"lck":60,"def":55,"res":40}
    )
    units["kagetsora"] = Unit(
        "kagetsora", "Uesugi Kagetsora", CLASS_SPEARMAN, FACTION_ENEMY, level=7,
        weapon_ids=["steel_yari"],
        portrait_color=(80, 120, 200),
        archetype=ARCHETYPE_NOBLE,
        bio=("Adopted heir of Kenshin. The Hojo blood in him created endless\n"
             "tension with the Uesugi retainers. He fought valiantly against\n"
             "both his destiny and his doubts."),
        quote="I carry two bloodlines and serve one master. That is enough.",
        growth_rates={"hp":60,"str":60,"mag":15,"skl":60,"spd":60,"lck":50,"def":60,"res":30}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # DATE CLAN — ENEMY
    # ══════════════════════════════════════════════════════════════════════════

    units["masamune"] = Unit(
        "masamune", "Date Masamune", CLASS_DAIMYO, FACTION_ENEMY, level=11,
        weapon_ids=["otenta_mitsu", "silver_yari"],
        portrait_color=(30, 30, 80),
        archetype=ARCHETYPE_AMBITIOUS,
        bio=("The One-Eyed Dragon of Oshu. He lost his eye to smallpox and\n"
             "removed it himself. Born too late to rule all Japan — but he\n"
             "never stopped trying. Flamboyant, unpredictable, magnificent."),
        quote="History will remember this moment — because I made it memorable!",
        is_lord=True,
        growth_rates={"hp":70,"str":70,"mag":35,"skl":70,"spd":65,"lck":60,"def":65,"res":40}
    )
    units["shigezane"] = Unit(
        "shigezane", "Date Shigezane", CLASS_CAVALRY, FACTION_ENEMY, level=8,
        weapon_ids=["steel_yari", "steel_katana"],
        portrait_color=(60, 60, 140),
        archetype=ARCHETYPE_LOYAL,
        bio=("Masamune's cousin, closest friend, and steadiest general.\n"
             "Where Masamune burns bright and reckless, Shigezane is\n"
             "the grounding force that keeps the dragon from flying too high."),
        quote="I'm always pulling him back from the edge. It never gets easier.",
        can_recruit=True, recruit_by=["masamune", "any"],
        growth_rates={"hp":65,"str":65,"mag":15,"skl":60,"spd":65,"lck":50,"def":60,"res":25}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # SHIMAZU CLAN — ENEMY
    # ══════════════════════════════════════════════════════════════════════════

    units["yoshihisa"] = Unit(
        "yoshihisa", "Shimazu Yoshihisa", CLASS_DAIMYO, FACTION_ENEMY, level=10,
        weapon_ids=["steel_nodachi", "steel_yari"],
        portrait_color=(80, 60, 140),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("The Shimazu lord who unified Kyushu. Master of the 'tsuridono'\n"
             "encirclement tactic — feign retreat to draw enemies into\n"
             "a trap of flanking forces. Methodical and merciless."),
        quote="Retreat is not weakness. It is the first move of a trap.",
        is_lord=True,
        growth_rates={"hp":70,"str":65,"mag":25,"skl":65,"spd":55,"lck":55,"def":65,"res":35}
    )
    units["yoshihiro"] = Unit(
        "yoshihiro", "Shimazu Yoshihiro", CLASS_BERSERKER, FACTION_ENEMY, level=9,
        weapon_ids=["fuujin_nodachi", "steel_tetsubo"],
        portrait_color=(100, 50, 160),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("The Demon of Sekigahara. Trapped on the losing side, Yoshihiro\n"
             "charged directly through the Tokugawa main force to escape —\n"
             "a move so audacious it became legend."),
        quote="Demon? Yes. Yours, specifically. NOW DIE!",
        growth_rates={"hp":80,"str":80,"mag":10,"skl":55,"spd":55,"lck":35,"def":70,"res":15}
    )
    units["toyohisa"] = Unit(
        "toyohisa", "Shimazu Toyohisa", CLASS_SAMURAI, FACTION_ENEMY, level=8,
        weapon_ids=["steel_katana", "iron_nodachi"],
        portrait_color=(120, 60, 160),
        archetype=ARCHETYPE_HERO,
        bio=("Yoshihiro's nephew — young, fierce, and desperately brave.\n"
             "He sacrificed himself covering the Shimazu retreat at Sekigahara,\n"
             "dying in a last stand against impossible odds."),
        quote="Uncle, go! I will hold them here as long as I breathe!",
        growth_rates={"hp":70,"str":70,"mag":10,"skl":65,"spd":60,"lck":45,"def":60,"res":20}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # HOJO CLAN — ENEMY (SOME RECRUITABLE)
    # ══════════════════════════════════════════════════════════════════════════

    units["ujiyasu"] = Unit(
        "ujiyasu", "Hojo Ujiyasu", CLASS_GENERAL, FACTION_ENEMY, level=11,
        weapon_ids=["nihongo", "iron_tetsubo"],
        portrait_color=(100, 100, 180),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("'The Lion of Sagami' — Ujiyasu never lost a castle to siege\n"
             "in his lifetime. Master of fortification, night raids,\n"
             "and three-front defensive warfare."),
        quote="A castle is not stone and timber. It is the will of those inside.",
        is_lord=True,
        can_recruit=True, recruit_by=["ieyasu", "any"],
        growth_rates={"hp":75,"str":65,"mag":25,"skl":65,"spd":45,"lck":55,"def":80,"res":40}
    )
    units["ujimasa"] = Unit(
        "ujimasa", "Hojo Ujimasa", CLASS_SAMURAI, FACTION_ENEMY, level=9,
        weapon_ids=["steel_katana", "steel_yari"],
        portrait_color=(80, 80, 160),
        archetype=ARCHETYPE_NOBLE,
        bio=("Ujiyasu's heir — he inherited the castle network but not quite\n"
             "his father's strategic genius. Nevertheless, he defended the\n"
             "Hojo lands with fierce dignity to the very end."),
        quote="The Hojo stand. We have always stood. We will not yield now.",
        growth_rates={"hp":65,"str":65,"mag":20,"skl":60,"spd":55,"lck":50,"def":65,"res":30}
    )
    units["fuma"] = Unit(
        "fuma", "Fuma Kotaro", CLASS_KUSARIGAMA, FACTION_ENEMY, level=9,
        weapon_ids=["fuma_chain", "windcutter"],
        portrait_color=(30, 20, 50),
        archetype=ARCHETYPE_MYSTIC,
        bio=("The shadow-lord of the Fuma ninja. Part man, part myth.\n"
             "He terrorized Uesugi supply lines and fought Hattori Hanzo\n"
             "to a terrifying standstill. His face has never been confirmed."),
        quote="..." ,
        can_recruit=True, recruit_by=["ranmaru", "goemon", "hanzo"],
        growth_rates={"hp":50,"str":65,"mag":30,"skl":90,"spd":85,"lck":60,"def":40,"res":50}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # MORI CLAN — ENEMY
    # ══════════════════════════════════════════════════════════════════════════

    units["motonari"] = Unit(
        "motonari", "Mori Motonari", CLASS_DAIMYO, FACTION_ENEMY, level=12,
        weapon_ids=["silver_katana", "kanbei_scroll"],
        portrait_color=(50, 120, 80),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("'The Fox of Chugoku' — Motonari conquered the west through\n"
             "deception, alliance, and brilliant betrayal. His famous lesson:\n"
             "'One arrow breaks, three bound together do not.'"),
        quote="I gave you every chance to walk away. Now it is too late.",
        is_lord=True,
        growth_rates={"hp":65,"str":60,"mag":55,"skl":70,"spd":55,"lck":70,"def":55,"res":55}
    )
    units["terumoto"] = Unit(
        "terumoto", "Mori Terumoto", CLASS_SAMURAI, FACTION_ENEMY, level=9,
        weapon_ids=["steel_katana", "steel_yari"],
        portrait_color=(60, 130, 90),
        archetype=ARCHETYPE_NOBLE,
        bio=("Grandson of Motonari. He inherited vast domains and mediocre\n"
             "military talent — but held the Mori name together through\n"
             "two generations of war."),
        quote="My grandfather built this. I will not be the one to lose it.",
        growth_rates={"hp":65,"str":60,"mag":20,"skl":55,"spd":55,"lck":50,"def":60,"res":30}
    )
    units["ekei"] = Unit(
        "ekei", "Ankokuji Ekei", CLASS_MONK, FACTION_ENEMY, level=8,
        weapon_ids=["ofuda", "heal_staff"],
        portrait_color=(100, 160, 130),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("The Mori's diplomat-monk. A master negotiator who served as\n"
             "envoy and spy for the western alliance. When diplomacy failed,\n"
             "he opened the sutra of war."),
        quote="I prayed for peace. You refused it. Let us proceed to the sermon.",
        growth_rates={"hp":40,"str":20,"mag":75,"skl":70,"spd":55,"lck":65,"def":25,"res":75}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # SAIKA MERCENARIES — RECRUITABLE
    # ══════════════════════════════════════════════════════════════════════════

    units["magoichi"] = Unit(
        "magoichi", "Saika Magoichi", CLASS_GUNNER, FACTION_ENEMY, level=8,
        weapon_ids=["saika_rifle", "iron_tanto"],
        portrait_color=(90, 60, 40),
        archetype=ARCHETYPE_FREE,
        bio=("Leader of the Saika mercenary gunners. His rifle never misses\n"
             "a target he truly aims for. He serves whoever pays — and whoever\n"
             "amuses him. Today, that might be you."),
        quote="I don't choose sides. I choose interesting employers.",
        can_recruit=True, recruit_by=["nobunaga", "hideyoshi", "any"],
        growth_rates={"hp":50,"str":60,"mag":25,"skl":80,"spd":55,"lck":60,"def":40,"res":35}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # CHOSOKABE CLAN — ENEMY (RECRUITABLE)
    # ══════════════════════════════════════════════════════════════════════════

    units["motochika"] = Unit(
        "motochika", "Chosokabe Motochika", CLASS_PIRATE, FACTION_ENEMY, level=9,
        weapon_ids=["odenta_mitsu", "daikyu"],
        portrait_color=(50, 70, 140),
        archetype=ARCHETYPE_FREE,
        bio=("Lord of Shikoku — the 'Demon Child of Tosa'. Unifier of his\n"
             "island province, he fights from land and sea alike. His naval\n"
             "tactics are as inventive as his battlefield charges."),
        quote="The sea and the mountains alike are my castle! Try to take them!",
        is_lord=True,
        can_recruit=True, recruit_by=["hideyoshi", "any"],
        growth_rates={"hp":65,"str":65,"mag":25,"skl":60,"spd":65,"lck":55,"def":55,"res":35}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # TACHIBANA CLAN — RECRUITABLE
    # ══════════════════════════════════════════════════════════════════════════

    units["ginchiyo"] = Unit(
        "ginchiyo", "Tachibana Ginchiyo", CLASS_PEGASUS_KNIGHT, FACTION_ENEMY, level=8,
        weapon_ids=["flying_naginata", "heal_staff"],
        portrait_color=(200, 200, 255),
        archetype=ARCHETYPE_HERO,
        bio=("Lady general of the Tachibana. She inherited her father's lightning\n"
             "blade and her mother's grace — a rare and deadly combination.\n"
             "She rides through storms other soldiers flee from."),
        quote="The lightning doesn't ask permission. Neither do I.",
        can_recruit=True, recruit_by=["oichi", "nene", "any"],
        growth_rates={"hp":50,"str":60,"mag":40,"skl":75,"spd":80,"lck":65,"def":45,"res":60}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # TSURUHIME — RECRUITABLE NAVAL ARCHER
    # ══════════════════════════════════════════════════════════════════════════

    units["tsuruhime"] = Unit(
        "tsuruhime", "Tsuruhime of Iyo", CLASS_MOUNTED_ARCHER, FACTION_ENEMY, level=7,
        weapon_ids=["tsuruhime_bow", "iron_tanto"],
        portrait_color=(200, 220, 255),
        archetype=ARCHETYPE_HERO,
        bio=("The holy warrior-priestess of Oyamazumi Shrine. She commanded\n"
             "Iyo Province's naval forces in person and never lost a sea battle.\n"
             "Her arrows are said to be guided by the gods of the sea."),
        quote="The sea gods have blessed these arrows. Let them find their mark!",
        can_recruit=True, recruit_by=["motochika", "any"],
        growth_rates={"hp":50,"str":55,"mag":35,"skl":80,"spd":75,"lck":70,"def":45,"res":50}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # WESTERN COALITION — ISHIDA / LATE CAMPAIGN ENEMIES
    # ══════════════════════════════════════════════════════════════════════════

    units["mitsunari"] = Unit(
        "mitsunari", "Ishida Mitsunari", CLASS_TACTICIAN, FACTION_ENEMY, level=10,
        weapon_ids=["onmyou_orb", "iron_tanto"],
        portrait_color=(80, 160, 130),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("Loyal administrator of the Toyotomi — and the man who forced\n"
             "Sekigahara. Cold, calculating, despised by the warriors around him,\n"
             "yet absolutely devoted to Hideyoshi's legacy."),
        quote="I will preserve what Lord Hideyoshi built, even if I fight alone!",
        is_lord=True,
        growth_rates={"hp":45,"str":30,"mag":80,"skl":75,"spd":60,"lck":65,"def":35,"res":75}
    )
    units["otani"] = Unit(
        "otani", "Otani Yoshitsugu", CLASS_ONMYOJI, FACTION_ENEMY, level=9,
        weapon_ids=["onmyou_orb", "heal_staff"],
        portrait_color=(120, 90, 150),
        archetype=ARCHETYPE_LOYAL,
        bio=("The Phantom General — Yoshitsugu was disfigured by leprosy,\n"
             "carried to battle in a palanquin. Yet his tactical mind never\n"
             "dimmed, and his loyalty to Mitsunari never wavered."),
        quote="This body is broken. My will is not. Strike!",
        growth_rates={"hp":40,"str":20,"mag":85,"skl":75,"spd":50,"lck":65,"def":25,"res":80}
    )
    units["konishi"] = Unit(
        "konishi", "Konishi Yukinaga", CLASS_CAVALRY, FACTION_ENEMY, level=8,
        weapon_ids=["steel_yari", "steel_katana"],
        portrait_color=(80, 100, 60),
        archetype=ARCHETYPE_NOBLE,
        bio=("Christian daimyo and naval commander. He led the first wave of\n"
             "the Korean invasion and always preferred negotiation to battle.\n"
             "He and Kato Kiyomasa famously despised each other."),
        quote="There is no glory in unnecessary war. But here we are.",
        growth_rates={"hp":60,"str":60,"mag":25,"skl":60,"spd":65,"lck":55,"def":55,"res":40}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # SAITO CLAN — EARLY ENEMY
    # ══════════════════════════════════════════════════════════════════════════

    units["tatsuoki"] = Unit(
        "tatsuoki", "Saito Tatsuoki", CLASS_SAMURAI, FACTION_ENEMY, level=7,
        weapon_ids=["steel_katana", "iron_yari"],
        portrait_color=(80, 140, 80),
        archetype=ARCHETYPE_AMBITIOUS,
        bio=("Son of the Viper of Mino. He inherited his father Dosan's\n"
             "great castle but not his genius. Indulgent and weak-willed,\n"
             "he drove his own retainers away before Nobunaga arrived."),
        quote="You dare attack Inabayama?! I will not flee!",
        is_lord=True,
        growth_rates={"hp":55,"str":55,"mag":20,"skl":55,"spd":55,"lck":45,"def":50,"res":30}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # AZAI / ASAKURA — ENEMY
    # ══════════════════════════════════════════════════════════════════════════

    units["nagamasa"] = Unit(
        "nagamasa", "Azai Nagamasa", CLASS_CAVALRY, FACTION_ENEMY, level=9,
        weapon_ids=["steel_katana", "silver_yari"],
        portrait_color=(60, 140, 120),
        archetype=ARCHETYPE_NOBLE,
        bio=("Nobunaga's brother-in-law — and the man who broke alliance\n"
             "to honor an older oath. Brave, honorable, and doomed.\n"
             "He chose loyalty to principle over self-interest."),
        quote="Honor demanded this. I do not regret it, even now.",
        is_lord=True,
        can_recruit=True, recruit_by=["oichi", "nobunaga"],
        growth_rates={"hp":65,"str":65,"mag":25,"skl":65,"spd":60,"lck":55,"def":65,"res":35}
    )
    units["yoshikage"] = Unit(
        "yoshikage", "Asakura Yoshikage", CLASS_DAIMYO, FACTION_ENEMY, level=8,
        weapon_ids=["steel_katana", "steel_yari"],
        portrait_color=(40, 80, 120),
        archetype=ARCHETYPE_NOBLE,
        bio=("The Asakura lord — cultured, indecisive, and tragically late\n"
             "to every battle that might have saved him. His castle at Ichijodani\n"
             "was a center of art and learning burned in an afternoon."),
        quote="I should have marched months ago. I know that now.",
        is_lord=True,
        growth_rates={"hp":60,"str":58,"mag":25,"skl":55,"spd":50,"lck":45,"def":58,"res":35}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # IMAGAWA CLAN — EARLY ENEMY
    # ══════════════════════════════════════════════════════════════════════════

    units["yoshimoto"] = Unit(
        "yoshimoto", "Imagawa Yoshimoto", CLASS_DAIMYO, FACTION_ENEMY, level=10,
        weapon_ids=["silver_katana", "silver_yari"],
        portrait_color=(160, 120, 180),
        archetype=ARCHETYPE_NOBLE,
        bio=("The grand Imagawa lord — 25,000 soldiers strong, he marched\n"
             "on Kyoto and stopped in a gully for tea. When Nobunaga's\n"
             "storm hit, he died before he could rise from his cushion."),
        quote="How DARE you interrupt my tea ceremony with a war!",
        is_lord=True,
        growth_rates={"hp":65,"str":60,"mag":30,"skl":60,"spd":50,"lck":60,"def":60,"res":40}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # TOYOTOMI — LATE GAME ENEMIES
    # ══════════════════════════════════════════════════════════════════════════

    units["hideyori"] = Unit(
        "hideyori", "Toyotomi Hideyori", CLASS_DAIMYO, FACTION_ENEMY, level=9,
        weapon_ids=["silver_katana", "silver_yari"],
        portrait_color=(200, 160, 80),
        archetype=ARCHETYPE_NOBLE,
        bio=("Son of Hideyoshi. Born to rule all Japan — but the Tokugawa\n"
             "closed in on Osaka Castle. Young, proud, and trapped by\n"
             "his own legacy, he refused to surrender."),
        quote="My father's dream will not die with me. It will not die!",
        is_lord=True,
        growth_rates={"hp":65,"str":65,"mag":30,"skl":60,"spd":55,"lck":55,"def":60,"res":40}
    )
    units["sanada_yukimura_late"] = Unit(
        "sanada_yukimura_late", "Sanada Yukimura (Osaka)", CLASS_SPEARMAN,
        FACTION_ENEMY, level=14,
        weapon_ids=["nihongo", "steel_katana"],
        portrait_color=(230, 20, 20),
        archetype=ARCHETYPE_HERO,
        bio=("In his final battle at Osaka, Yukimura's charge shook Ieyasu's\n"
             "camp to its foundations. The old Tokugawa lord turned pale.\n"
             "For one glorious moment, the war hung by a thread."),
        quote="FOR THE TOYOTOMI! FOR JAPAN! THIS IS MY MOMENT!",
        is_lord=False,
        growth_rates={"hp":75,"str":80,"mag":15,"skl":75,"spd":70,"lck":60,"def":70,"res":30}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # GENERIC UNITS (player/enemy/ally filler)
    # ══════════════════════════════════════════════════════════════════════════

    def _generic(uid, name, cls, faction, lv, wids, col, bio="A soldier of the age."):
        units[uid] = Unit(uid, name, cls, faction, level=lv,
                          weapon_ids=wids, portrait_color=col, bio=bio)

    # Player generics
    _generic("oda_ash1",   "Oda Ashigaru",    CLASS_ASHIGARU,     FACTION_PLAYER, 1,  ["iron_yari"],     GREY)
    _generic("oda_ash2",   "Oda Ashigaru",    CLASS_ASHIGARU,     FACTION_PLAYER, 1,  ["iron_yari"],     GREY)
    _generic("oda_ash3",   "Oda Ashigaru",    CLASS_ASHIGARU,     FACTION_PLAYER, 2,  ["iron_tetsubo"],  GREY)
    _generic("oda_arch1",  "Oda Archer",      CLASS_ARCHER,       FACTION_PLAYER, 2,  ["iron_bow"],      GREEN)
    _generic("oda_arch2",  "Oda Archer",      CLASS_ARCHER,       FACTION_PLAYER, 3,  ["steel_bow"],     GREEN)
    _generic("oda_cav1",   "Oda Cavalry",     CLASS_CAVALRY,      FACTION_PLAYER, 3,  ["iron_yari","iron_katana"], ORANGE)
    _generic("oda_gun1",   "Oda Gunner",      CLASS_GUNNER,       FACTION_PLAYER, 3,  ["tanegashima","iron_tanto"], SLATE)
    _generic("oda_gun2",   "Oda Gunner",      CLASS_GUNNER,       FACTION_PLAYER, 4,  ["improved_gun","iron_tanto"], SLATE)
    _generic("oda_monk1",  "Oda Monk",        CLASS_MONK,         FACTION_PLAYER, 3,  ["heal_staff","shakujo"], YELLOW)
    _generic("oda_spear1", "Oda Spearman",    CLASS_SPEARMAN,     FACTION_PLAYER, 2,  ["iron_yari"],     CYAN)
    _generic("oda_ninja1", "Oda Ninja",       CLASS_NINJA,        FACTION_PLAYER, 3,  ["iron_tanto","kunai"], DARK_GREY)
    _generic("oda_sam1",   "Oda Samurai",     CLASS_SAMURAI,      FACTION_PLAYER, 3,  ["iron_katana"],   BLUE)
    _generic("oda_sam2",   "Oda Samurai",     CLASS_SAMURAI,      FACTION_PLAYER, 4,  ["steel_katana"],  BLUE)
    _generic("oda_hatamoto1", "Oda Hatamoto", CLASS_HATAMOTO,     FACTION_PLAYER, 5,  ["steel_katana","jumonji_yari"], COPPER)

    # Enemy generics
    _generic("e_ash1",   "Ashigaru",       CLASS_ASHIGARU,    FACTION_ENEMY, 1,  ["iron_yari"],      (180,60,60))
    _generic("e_ash2",   "Ashigaru",       CLASS_ASHIGARU,    FACTION_ENEMY, 1,  ["iron_yari"],      (180,60,60))
    _generic("e_ash3",   "Ashigaru",       CLASS_ASHIGARU,    FACTION_ENEMY, 2,  ["iron_tetsubo"],   (180,60,60))
    _generic("e_ash4",   "Ashigaru",       CLASS_ASHIGARU,    FACTION_ENEMY, 3,  ["iron_yari"],      (180,60,60))
    _generic("e_ash5",   "Ashigaru",       CLASS_ASHIGARU,    FACTION_ENEMY, 3,  ["iron_tetsubo"],   (170,50,50))
    _generic("e_sam1",   "Samurai",        CLASS_SAMURAI,     FACTION_ENEMY, 3,  ["iron_katana"],    (150,50,50))
    _generic("e_sam2",   "Samurai",        CLASS_SAMURAI,     FACTION_ENEMY, 4,  ["steel_katana"],   (150,50,50))
    _generic("e_sam3",   "Samurai",        CLASS_SAMURAI,     FACTION_ENEMY, 5,  ["steel_katana"],   (160,40,40))
    _generic("e_cav1",   "Cavalry",        CLASS_CAVALRY,     FACTION_ENEMY, 3,  ["iron_yari","iron_katana"],    (200,80,80))
    _generic("e_cav2",   "Cavalry",        CLASS_CAVALRY,     FACTION_ENEMY, 5,  ["steel_yari","steel_katana"],  (200,70,70))
    _generic("e_arch1",  "Archer",         CLASS_ARCHER,      FACTION_ENEMY, 2,  ["iron_bow"],       (180,80,80))
    _generic("e_arch2",  "Archer",         CLASS_ARCHER,      FACTION_ENEMY, 4,  ["steel_bow"],      (170,70,70))
    _generic("e_ninja1", "Ninja",          CLASS_NINJA,       FACTION_ENEMY, 4,  ["iron_tanto","kunai"],       (50,40,60))
    _generic("e_ninja2", "Ninja",          CLASS_NINJA,       FACTION_ENEMY, 6,  ["steel_tanto","daikyu"],     (50,40,60))
    _generic("e_spear1", "Spearman",       CLASS_SPEARMAN,    FACTION_ENEMY, 3,  ["iron_yari"],      (160,60,60))
    _generic("e_spear2", "Spearman",       CLASS_SPEARMAN,    FACTION_ENEMY, 4,  ["steel_yari"],     (160,55,55))
    _generic("e_monk1",  "Warrior Monk",   CLASS_SOHEI,       FACTION_ENEMY, 3,  ["iron_naginata","heal_staff"],(100,140,140))
    _generic("e_monk2",  "Warrior Monk",   CLASS_SOHEI,       FACTION_ENEMY, 5,  ["steel_naginata","heal_staff"],(80,130,130))
    _generic("e_gen1",   "General",        CLASS_GENERAL,     FACTION_ENEMY, 5,  ["iron_yari","iron_tetsubo"], (140,140,140))
    _generic("e_gen2",   "General",        CLASS_GENERAL,     FACTION_ENEMY, 7,  ["steel_yari","steel_tetsubo"],(130,130,130))
    _generic("e_gun1",   "Gunner",         CLASS_GUNNER,      FACTION_ENEMY, 3,  ["tanegashima","iron_tanto"],  SLATE)
    _generic("e_gun2",   "Gunner",         CLASS_GUNNER,      FACTION_ENEMY, 5,  ["improved_gun","iron_tanto"], SLATE)
    _generic("e_hat1",   "Hatamoto",       CLASS_HATAMOTO,    FACTION_ENEMY, 5,  ["steel_katana","steel_yari"], (160,100,60))
    _generic("e_pg1",    "Pegasus Knight", CLASS_PEGASUS_KNIGHT, FACTION_ENEMY, 4, ["iron_naginata"], (180,170,220))
    _generic("e_wy1",    "Wyvern Knight",  CLASS_WYVERN_KNIGHT,  FACTION_ENEMY, 5, ["steel_yari"],   (140,70,40))
    _generic("e_wy2",    "Wyvern Knight",  CLASS_WYVERN_KNIGHT,  FACTION_ENEMY, 7, ["silver_yari"],  (130,60,30))
    _generic("e_ron1",   "Ronin",          CLASS_RONIN,       FACTION_ENEMY, 5,  ["steel_katana"],   (120,30,30))
    _generic("e_ron2",   "Ronin",          CLASS_RONIN,       FACTION_ENEMY, 7,  ["steel_katana","iron_nodachi"],(110,20,20))
    _generic("e_pirate1","Pirate",         CLASS_PIRATE,      FACTION_ENEMY, 4,  ["iron_katana","iron_nodachi"],(50,60,120))
    _generic("e_pirate2","Pirate",         CLASS_PIRATE,      FACTION_ENEMY, 6,  ["steel_katana","steel_nodachi"],(40,50,110))
    _generic("e_mach1",  "Mounted Archer", CLASS_MOUNTED_ARCHER,FACTION_ENEMY,4,  ["iron_bow","iron_katana"],   SAGE)
    _generic("e_berz1",  "Berserker",      CLASS_BERSERKER,   FACTION_ENEMY, 5,  ["steel_tetsubo"],  (200,40,40))
    _generic("e_berz2",  "Berserker",      CLASS_BERSERKER,   FACTION_ENEMY, 7,  ["oni_tetsubo"],    (190,30,30))
    _generic("e_ikko1",  "Ikko-Ikki",      CLASS_SOHEI,       FACTION_ENEMY, 3,  ["iron_naginata"],  (100,150,140))
    _generic("e_ikko2",  "Ikko-Ikki",      CLASS_SOHEI,       FACTION_ENEMY, 4,  ["steel_naginata","heal_staff"],(90,140,130))
    _generic("e_ksama1", "Kusarigama",     CLASS_KUSARIGAMA,  FACTION_ENEMY, 4,  ["iron_chain"],     (70,50,90))
    _generic("e_ron3",   "Rival Ronin",    CLASS_RONIN,       FACTION_ENEMY, 6,  ["steel_katana"],   (100,30,30))
    _generic("e_hata2",  "Elite Hatamoto", CLASS_HATAMOTO,    FACTION_ENEMY, 8,  ["silver_katana","jumonji_yari"],(150,90,50))

    # ── New flying generics ────────────────────────────────────────────────────
    _generic("e_fk1",  "Falcon Knight",  CLASS_FALCON_KNIGHT, FACTION_ENEMY, 5,  ["iron_naginata","heal_staff"],  (210,190,255))
    _generic("e_fk2",  "Falcon Knight",  CLASS_FALCON_KNIGHT, FACTION_ENEMY, 7,  ["steel_naginata","mend_staff"], (200,180,255))
    _generic("e_ea1",  "Eagle Archer",   CLASS_EAGLE_ARCHER,  FACTION_ENEMY, 5,  ["steel_bow"],                   (170,220,150))
    _generic("e_ea2",  "Eagle Archer",   CLASS_EAGLE_ARCHER,  FACTION_ENEMY, 7,  ["silver_bow","yumi_anti_air"],  (160,210,140))
    _generic("e_sr1",  "Storm Rider",    CLASS_STORM_RIDER,   FACTION_ENEMY, 5,  ["iron_tanto","iron_katana"],    (150,200,255))
    _generic("e_sr2",  "Storm Rider",    CLASS_STORM_RIDER,   FACTION_ENEMY, 8,  ["steel_tanto","steel_katana"],  (140,190,255))
    _generic("e_tm1",  "Tengu Master",   CLASS_TENGU_MASTER,  FACTION_ENEMY, 5,  ["iron_tanto","ofuda"],          (90,50,150))
    _generic("e_sl1",  "Sky Lancer",     CLASS_SKY_LANCER,    FACTION_ENEMY, 6,  ["steel_yari"],                  (170,110,55))
    _generic("e_sl2",  "Sky Lancer",     CLASS_SKY_LANCER,    FACTION_ENEMY, 8,  ["silver_yari","iron_naginata"], (160,100,45))
    _generic("e_dk1",  "Dragon Knight",  CLASS_DRAGON_KNIGHT, FACTION_ENEMY, 8,  ["silver_yari","steel_katana"],  (190,70,25))
    _generic("e_dk2",  "Dragon Knight",  CLASS_DRAGON_KNIGHT, FACTION_ENEMY,10,  ["dojikiri","nihongo"],          (180,60,20))

    # ── New mounted generics ───────────────────────────────────────────────────
    _generic("e_lc1",  "Lance Cavalry",  CLASS_LANCE_CAVALRY, FACTION_ENEMY, 4,  ["iron_yari"],                   (210,130,55))
    _generic("e_lc2",  "Lance Cavalry",  CLASS_LANCE_CAVALRY, FACTION_ENEMY, 6,  ["steel_yari","iron_naginata"],  (200,120,45))
    _generic("e_we1",  "War Elephant",   CLASS_WAR_ELEPHANT,  FACTION_ENEMY, 6,  ["iron_tetsubo","iron_yari"],    (90,70,55))
    _generic("e_we2",  "War Elephant",   CLASS_WAR_ELEPHANT,  FACTION_ENEMY, 9,  ["steel_tetsubo","steel_yari"],  (80,60,45))
    _generic("e_ltc1", "Light Cavalry",  CLASS_LIGHT_CAVALRY, FACTION_ENEMY, 3,  ["iron_tanto","iron_bow"],       (195,195,110))
    _generic("e_ltc2", "Light Cavalry",  CLASS_LIGHT_CAVALRY, FACTION_ENEMY, 5,  ["steel_tanto","iron_bow"],      (185,185,100))
    _generic("e_gk1",  "Great Knight",   CLASS_GREAT_KNIGHT,  FACTION_ENEMY, 5,  ["steel_katana","iron_yari"],    (130,130,170))
    _generic("e_gk2",  "Great Knight",   CLASS_GREAT_KNIGHT,  FACTION_ENEMY, 8,  ["silver_katana","jumonji_yari"],(120,120,160))
    _generic("e_nc1",  "Noble Cavalry",  CLASS_NOBLE_CAVALRY, FACTION_ENEMY, 6,  ["steel_katana","silver_yari"],  (210,190,75))

    # ── Named units using new classes ──────────────────────────────────────────
    units["kobayakawa"] = Unit(
        "kobayakawa", "Kobayakawa Hideaki", CLASS_GREAT_KNIGHT, FACTION_ENEMY, level=8,
        weapon_ids=["silver_katana","jumonji_yari"],
        portrait_color=(100,110,170),
        archetype=ARCHETYPE_AMBITIOUS,
        bio=("The pivotal traitor of Sekigahara. Promised rewards by both sides,\n"
             "he waited atop his hill — until Ieyasu fired a warning shot toward him.\n"
             "He then charged Mitsunari's flank, deciding the battle."),
        quote="The winning side... is the side that wins. Obviously.",
        can_recruit=True, recruit_by=["ieyasu","any"],
    )
    units["matsunaga"] = Unit(
        "matsunaga", "Matsunaga Hisahide", CLASS_STORM_RIDER, FACTION_ENEMY, level=9,
        weapon_ids=["steel_tanto","steel_katana"],
        portrait_color=(60,40,100),
        archetype=ARCHETYPE_MYSTIC,
        bio=("The 'Three Great Villainies' lord — burned Todaiji, killed the Shogun,\n"
             "betrayed every alliance he made. When cornered by Nobunaga,\n"
             "he blew himself up with his own precious tea kettle."),
        quote="Burn everything, own nothing. That is true freedom.",
    )
    units["naotora"] = Unit(
        "naotora", "Ii Naotora", CLASS_NOBLE_CAVALRY, FACTION_ALLY, level=7,
        weapon_ids=["steel_yari","iron_naginata"],
        portrait_color=(230,60,60),
        archetype=ARCHETYPE_HERO,
        bio=("The Lady Ii — she inherited her clan's famous red armor and held\n"
             "their domain alone while the men were at war. She is Ii Naomasa's\n"
             "adoptive mother and the true iron heart of the red devils."),
        quote="Red is not the color of death. It is the color of life — and will!",
    )
    units["tsuruhime_upgraded"] = Unit(
        "tsuruhime_upgraded", "Tsuruhime the Sea Falcon", CLASS_EAGLE_ARCHER, FACTION_ALLY, level=8,
        weapon_ids=["tsuruhime_bow","yumi_anti_air"],
        portrait_color=(180,210,255),
        archetype=ARCHETYPE_HERO,
        bio=("Promoted to Eagle Archer after mastering the gods' own wind currents.\n"
             "Her shots from altitude have the force of a diving hawk.\n"
             "She claims the sea eagles are her messengers from Oyamazumi Shrine."),
        quote="The gods gave me arrows and wings. Let that be sufficient.",
    )
    units["yoshitsune"] = Unit(
        "yoshitsune", "Minamoto no Yoshitsune", CLASS_FALCON_KNIGHT, FACTION_ALLY, level=9,
        weapon_ids=["silver_naginata","physic_staff"],
        portrait_color=(200,220,255),
        archetype=ARCHETYPE_HERO,
        bio=("The legendary hero-general — appearing as a vision to guide the army.\n"
             "Swift as thought, agile as the wind, and blessed with divine grace.\n"
             "He fights from the air, healing allies even as he strikes enemies."),
        quote="I ride where the wind rides. And the wind goes everywhere.",
    )

    # ── Shimazu generic variants using new classes ─────────────────────────────
    def _named(uid, name, cls, faction, lv, wids, col, bio=""):
        units[uid] = Unit(uid, name, cls, faction, level=lv,
                          weapon_ids=wids, portrait_color=col, bio=bio)

    _named("shimazu_ash1", "Shimazu Soldier", CLASS_LANCE_CAVALRY, FACTION_ENEMY,
           4, ["iron_yari"], (90,50,140))
    _named("shimazu_ash2", "Shimazu Soldier", CLASS_LANCE_CAVALRY, FACTION_ENEMY,
           4, ["iron_yari"], (90,50,140))
    _named("shimazu_archer","Shimazu Archer", CLASS_EAGLE_ARCHER, FACTION_ENEMY,
           5, ["steel_bow"], (100,60,150))

    return units
