'''
Unit definitions for Sengoku Tactics
Inspired by Samurai Warriors characters — each unit has a personality archetype,
iconic weapon, and Samurai Warriors-style bio flavor.
'''
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

        # Promotion flags
        self.is_promoted        = unit_class in PROMOTED_CLASSES
        self.promotion_available= False   # Set True when lv10+ reached; promotion is OPTIONAL

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
            # Once lv10+ is reached, mark promotion as available (optional — player chooses via stat screen)
            if (self.level >= PROMOTION_LEVEL and not self.is_promoted
                    and self.unit_class in PROMOTION_CHAINS):
                self.promotion_available = True
        return leveled

    def promote(self, new_class):
        '''Promote this unit to new_class (called from stat sheet). Applies bonuses and updates class data.'''
        if new_class not in PROMOTION_CHAINS.get(self.unit_class, []):
            return False   # invalid promotion choice
        bonuses = PROMOTION_BONUSES.get(new_class, {})
        self.unit_class          = new_class
        self.is_promoted         = True
        self.promotion_available = False
        # Apply stat bonuses
        self.max_hp += bonuses.get("hp",  0); self.hp = min(self.hp + bonuses.get("hp", 0), self.max_hp)
        self.str_   += bonuses.get("str", 0)
        self.mag    += bonuses.get("mag", 0)
        self.skl    += bonuses.get("skl", 0)
        self.spd    += bonuses.get("spd", 0)
        self.lck    += bonuses.get("lck", 0)
        self.def_   += bonuses.get("def", 0)
        self.res    += bonuses.get("res", 0)
        # Reload class data
        cd = CLASS_DATA[new_class]
        self.symbol          = cd["symbol"]
        self.color           = cd["color"]
        self.move            = cd["move"] + bonuses.get("move", 0)
        self.allowed_weapons = cd["weapons"]
        self.is_flying       = cd.get("flying",    False) or new_class in FLYING_CLASSES
        self.is_mounted      = cd.get("mounted",   False) or new_class in MOUNTED_CLASSES
        self.water_walk      = cd.get("water_walk",False) or new_class in WATER_CLASSES
        return True

    def _level_up(self):
        self.level += 1
        g = self.growths
        gains = {}

        def _roll(key, default, lo, hi):
            '''Roll a stat gain. Rate is clamped to [lo, hi].
            Rates above 100 guarantee at least +1 and give a (rate-100)% chance of +2.'''
            rate = max(lo, min(hi, g.get(key, default)))
            if rate <= 100:
                return 1 if random.randint(1, 100) <= rate else 0
            else:
                # Guaranteed +1; extra +1 on (rate-100)% chance
                return 1 + (1 if random.randint(1, 100) <= (rate - 100) else 0)

        # HP: 60–120%
        hp_gain = _roll("hp",  70, 60, 120)
        if hp_gain:
            self.max_hp += hp_gain; self.hp += hp_gain; gains["HP"] = hp_gain
        # All other stats: 20–70%
        if _roll("str", 40, 20, 70): self.str_  += 1; gains["STR"] = 1
        if _roll("mag", 30, 20, 70): self.mag   += 1; gains["MAG"] = 1
        if _roll("skl", 45, 20, 70): self.skl   += 1; gains["SKL"] = 1
        if _roll("spd", 45, 20, 70): self.spd   += 1; gains["SPD"] = 1
        if _roll("lck", 35, 20, 70): self.lck   += 1; gains["LCK"] = 1
        if _roll("def", 35, 20, 70): self.def_  += 1; gains["DEF"] = 1
        if _roll("res", 25, 20, 70): self.res   += 1; gains["RES"] = 1

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

    # ══════════════════════════════════════════════════════════════════════════
    # MULTI-BOSS ENEMY OFFICERS (for historically accurate multi-commander chapters)
    # ══════════════════════════════════════════════════════════════════════════

    units["hidemitsu"] = Unit(
        "hidemitsu", "Akechi Hidemitsu", CLASS_CAVALRY, FACTION_ENEMY, level=7,
        weapon_ids=["steel_yari","steel_katana"],
        portrait_color=(70, 70, 140),
        archetype=ARCHETYPE_LOYAL,
        bio=("Mitsuhide's nephew and most devoted sub-commander. He led the\n"
             "encirclement force at Honnoji and pursued the Oda survivors\n"
             "with ruthless efficiency. Loyal to his uncle to the very end."),
        quote="My uncle's will is absolute. His enemies have no tomorrow.",
        growth_rates={"hp":60,"str":60,"mag":15,"skl":55,"spd":60,"lck":40,"def":55,"res":25}
    )

    units["mitsuyoshi"] = Unit(
        "mitsuyoshi", "Akechi Mitsuyoshi", CLASS_SAMURAI, FACTION_ENEMY, level=7,
        weapon_ids=["steel_katana","iron_nodachi"],
        portrait_color=(90, 90, 160),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("Mitsuhide's son. Inherited his father's precision with a sword\n"
             "but not his patience. He died at Yamazaki trying to cover\n"
             "his father's retreat — cut down before he could reach safety."),
        quote="For the Akechi name — we fight, even if we fall!",
        growth_rates={"hp":55,"str":60,"mag":15,"skl":70,"spd":65,"lck":40,"def":50,"res":25}
    )

    units["muneharu"] = Unit(
        "muneharu", "Shimizu Muneharu", CLASS_GENERAL, FACTION_ENEMY, level=8,
        weapon_ids=["nihongo","steel_tetsubo"],
        portrait_color=(80, 100, 140),
        archetype=ARCHETYPE_LOYAL,
        bio=("The commander of Takamatsu Castle — a man of extraordinary loyalty.\n"
             "When the castle was flooded and all hope lost, he chose to sacrifice\n"
             "himself by ritual suicide so his garrison could live. His courage\n"
             "was acknowledged even by Hideyoshi."),
        quote="My men may live. That is enough. My life is a small price.",
        growth_rates={"hp":70,"str":60,"mag":10,"skl":55,"spd":35,"lck":50,"def":80,"res":30}
    )

    units["miyabe"] = Unit(
        "miyabe", "Miyabe Keijun", CLASS_TACTICIAN, FACTION_ENEMY, level=7,
        weapon_ids=["kanbei_scroll","iron_tanto"],
        portrait_color=(90, 70, 110),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("Mitsuhide's chief military strategist at Honnoji — the planner\n"
             "behind the encirclement. He managed the political aftermath\n"
             "of the coup before Hideyoshi's lightning march changed everything."),
        quote="We planned for every contingency. Every one except Hideyoshi's speed.",
        growth_rates={"hp":40,"str":25,"mag":70,"skl":65,"spd":55,"lck":55,"def":30,"res":65}
    )

    units["katsuyori"] = Unit(
        "katsuyori", "Takeda Katsuyori", CLASS_CAVALRY, FACTION_ENEMY, level=10,
        weapon_ids=["silver_yari","steel_katana"],
        portrait_color=(170, 50, 50),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("Shingen's heir — brave, bold, and tragically reckless.\n"
             "At Nagashino, he ordered his legendary cavalry into the Oda volley\n"
             "fire against all advice. He was not his father. He died for it."),
        quote="Takeda cavalry has never been stopped! CHARGE! CHARGE! CHARGE!",
        is_lord=True,
        growth_rates={"hp":65,"str":70,"mag":20,"skl":60,"spd":65,"lck":40,"def":60,"res":25}
    )

    units["narimasa"] = Unit(
        "narimasa", "Sassa Narimasa", CLASS_BERSERKER, FACTION_ENEMY, level=8,
        weapon_ids=["steel_tetsubo","steel_katana"],
        portrait_color=(170, 80, 50),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("One of Katsuie's most aggressive generals — a berserk warrior\n"
             "who was once banned from Nobunaga's presence for excessive violence\n"
             "even by Nobunaga's standards. That is quite the achievement."),
        quote="Banned from Nobunaga's court for being too violent? I take that as a compliment.",
        growth_rates={"hp":75,"str":70,"mag":5,"skl":45,"spd":50,"lck":30,"def":65,"res":15}
    )

    units["matahachi"] = Unit(
        "matahachi", "Siege Commander Matahachi", CLASS_SPEARMAN, FACTION_ENEMY, level=6,
        weapon_ids=["steel_yari","iron_naginata"],
        portrait_color=(100, 80, 140),
        archetype=ARCHETYPE_LOYAL,
        bio=("A fictional but archetypal siege officer — the man Mitsunari\n"
             "entrusts with holding the critical gates of Osaka Castle.\n"
             "Experienced, cautious, and very hard to dislodge."),
        quote="These walls do not fall while I breathe.",
        growth_rates={"hp":60,"str":55,"mag":10,"skl":55,"spd":45,"lck":40,"def":60,"res":25}
    )

    units["okita_clan"] = Unit(
        "okita_clan", "Ōkita of the Mori", CLASS_WYVERN_KNIGHT, FACTION_ENEMY, level=8,
        weapon_ids=["steel_yari","iron_katana"],
        portrait_color=(50, 110, 70),
        archetype=ARCHETYPE_LOYAL,
        bio=("A Mori flying officer who patrols the sea approaches to Takamatsu\n"
             "Castle. When the castle floods, he flies desperate supply runs\n"
             "low over the water. A devoted and dangerous opponent."),
        quote="The Mori endure. I endure. Fly on!",
        growth_rates={"hp":60,"str":60,"mag":5,"skl":55,"spd":55,"lck":35,"def":60,"res":20}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # NAMED UNITS FOR NEW MAGICAL PROMOTED CLASSES (12)
    # ══════════════════════════════════════════════════════════════════════════

    units["okuni"] = Unit(
        "okuni", "Izumo no Okuni", CLASS_SPIRIT_DANCER, FACTION_PLAYER, level=8,
        weapon_ids=["flying_naginata","heal_staff"],
        portrait_color=(180, 230, 255),
        archetype=ARCHETYPE_FREE,
        bio=("The founder of Kabuki theater — Okuni turned her sacred shrine dances\n"
             "into a new art form that swept Japan. In battle, her movements channel\n"
             "wind kami into blasts that scatter enemy formations."),
        quote="Watch me dance. Then watch your soldiers run.",
        can_recruit=True, recruit_by=["hideyoshi", "any"],
        growth_rates={"hp":35,"str":20,"mag":75,"skl":65,"spd":80,"lck":70,"def":20,"res":70}
    )

    units["tamamo"] = Unit(
        "tamamo", "Tamamo-no-Mae", CLASS_KITSUNE_SAGE, FACTION_ENEMY, level=11,
        weapon_ids=["onmyou_orb","windcutter"],
        portrait_color=(255, 210, 140),
        archetype=ARCHETYPE_MYSTIC,
        bio=("The nine-tailed fox spirit in the guise of a peerless beauty.\n"
             "She has served emperors and shoguns across centuries.\n"
             "Her illusions are indistinguishable from reality."),
        quote="Which of these is real? Are you even certain you are?",
        growth_rates={"hp":30,"str":15,"mag":90,"skl":70,"spd":70,"lck":80,"def":15,"res":80}
    )

    units["tenkai"] = Unit(
        "tenkai", "Tenkai", CLASS_VOID_PROPHET, FACTION_ENEMY, level=10,
        weapon_ids=["onmyou_orb","shakujo"],
        portrait_color=(60, 20, 80),
        archetype=ARCHETYPE_MYSTIC,
        bio=("The Black-Robed Advisor — Ieyasu's mysterious monk counsellor.\n"
             "Rumored to be the reincarnation of Akechi Mitsuhide, Tenkai weaves\n"
             "dark spiritual curses that no warrior can simply cut through."),
        quote="Darkness is not the absence of light. It is the presence of truth.",
        can_recruit=True, recruit_by=["ieyasu", "any"],
        growth_rates={"hp":40,"str":10,"mag":85,"skl":65,"spd":50,"lck":40,"def":25,"res":75}
    )

    units["chigusa"] = Unit(
        "chigusa", "Lady Chigusa", CLASS_SHRINE_ORACLE, FACTION_ALLY, level=8,
        weapon_ids=["amulet_staff","heal_staff"],
        portrait_color=(255, 240, 200),
        archetype=ARCHETYPE_NOBLE,
        bio=("Chief shrine maiden of Atsuta Shrine — the very shrine whose divine favor\n"
             "Nobunaga invoked before Okehazama. Lady Chigusa has tended sacred flame\n"
             "for forty years and seen every warlord bow at her threshold."),
        quote="I do not pray for victory. I pray for you to be worth the gods' attention.",
        growth_rates={"hp":45,"str":15,"mag":75,"skl":65,"spd":55,"lck":75,"def":25,"res":80}
    )

    units["sessai"] = Unit(
        "sessai", "Taigen Sessai", CLASS_CELESTIAL_MONK, FACTION_ENEMY, level=10,
        weapon_ids=["shakujo","iron_naginata"],
        portrait_color=(230, 220, 255),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("The brilliant monk-general of the Imagawa — strategist, diplomat,\n"
             "and healer in one. He guided Yoshimoto's campaigns with serene\n"
             "precision. Even enemies respected his wisdom."),
        quote="I carry the sutras in one hand and a naginata in the other. Both serve the same purpose.",
        can_recruit=True, recruit_by=["nobunaga", "any"],
        growth_rates={"hp":55,"str":40,"mag":70,"skl":65,"spd":55,"lck":60,"def":50,"res":70}
    )

    units["jade_oracle"] = Unit(
        "jade_oracle", "Omiwa the Jade Oracle", CLASS_JADE_SORCERESS, FACTION_ENEMY, level=12,
        weapon_ids=["onmyou_orb","kanbei_scroll"],
        portrait_color=(140, 220, 160),
        archetype=ARCHETYPE_MYSTIC,
        bio=("A reclusive sorceress who channels the spirit of the jade dragon.\n"
             "She answers to no lord and destroys armies that trespass on her mountain.\n"
             "Her magic can shatter castle gates."),
        quote="You came to MY mountain. I did not invite you.",
        growth_rates={"hp":30,"str":10,"mag":95,"skl":75,"spd":55,"lck":45,"def":10,"res":70}
    )

    units["raijin_shaman"] = Unit(
        "raijin_shaman", "Fujibayashi Nagato", CLASS_THUNDER_SHAMAN, FACTION_ENEMY, level=9,
        weapon_ids=["ofuda","steel_yari"],
        portrait_color=(255, 240, 80),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("A warrior-mystic who calls lightning from storm clouds on horseback.\n"
             "He claims Raijin, god of thunder, speaks directly into his ear.\n"
             "The claim is not entirely unconvincing on a battlefield."),
        quote="Thunder first. Lightning second. You third.",
        can_recruit=True, recruit_by=["any"],
        growth_rates={"hp":55,"str":45,"mag":70,"skl":55,"spd":60,"lck":40,"def":50,"res":60}
    )

    units["zogan"] = Unit(
        "zogan", "Zogan the Martyr", CLASS_BLOOD_ASCETIC, FACTION_ENEMY, level=10,
        weapon_ids=["shakujo","kunai"],
        portrait_color=(160, 20, 20),
        archetype=ARCHETYPE_MYSTIC,
        bio=("Fanatical Ikko-Ikki ascetic who has mastered self-mortification to\n"
             "convert agony into spiritual destructive force. He welcomes wounds.\n"
             "The more he bleeds, the more terrible his power becomes."),
        quote="Pain is just karma leaving the body. And taking yours with it.",
        growth_rates={"hp":60,"str":25,"mag":75,"skl":50,"spd":50,"lck":25,"def":35,"res":55}
    )

    units["tsukikage"] = Unit(
        "tsukikage", "Lady Tsukikage", CLASS_MOON_RIDER, FACTION_ALLY, level=8,
        weapon_ids=["flying_naginata","heal_staff"],
        portrait_color=(180, 180, 255),
        archetype=ARCHETYPE_MYSTIC,
        bio=("A celestial guardian who rides a moon-pale steed through the night sky.\n"
             "Her naginata shimmers like moonlight, and her healing songs calm\n"
             "even the most berserk warriors mid-battle."),
        quote="The moon watches every battle. She sent me to even the odds.",
        can_recruit=True, recruit_by=["any"],
        growth_rates={"hp":45,"str":50,"mag":65,"skl":65,"spd":70,"lck":60,"def":40,"res":65}
    )

    units["kagemusha"] = Unit(
        "kagemusha", "Kagemusha of the Dark Pass", CLASS_PHANTOM_KNIGHT, FACTION_ENEMY, level=9,
        weapon_ids=["muramasa","kanbei_scroll"],
        portrait_color=(80, 80, 120),
        archetype=ARCHETYPE_RIVAL,
        bio=("A cursed samurai bound by dark spirit contract who serves whichever\n"
             "warlord currently holds his sealed blade. Neither fully alive nor dead,\n"
             "he fights with a calm that only the beyond-caring possess."),
        quote="I have died before. It was quieter than this.",
        growth_rates={"hp":55,"str":60,"mag":55,"skl":55,"spd":55,"lck":25,"def":55,"res":50}
    )

    units["uzume"] = Unit(
        "uzume", "Ama no Uzume", CLASS_STAR_DANCER, FACTION_ALLY, level=10,
        weapon_ids=["windcutter","heal_staff"],
        portrait_color=(255, 240, 120),
        archetype=ARCHETYPE_MYSTIC,
        bio=("The divine dancer who once lured Amaterasu from the cave,\n"
             "restoring sunlight to the world. Now manifest in the age of war,\n"
             "Uzume soars on starlight, turning the tide with celestial magic."),
        quote="I danced for a sun goddess once. Your army is considerably less impressive.",
        growth_rates={"hp":35,"str":25,"mag":85,"skl":70,"spd":85,"lck":75,"def":20,"res":70}
    )

    units["seimei_heir"] = Unit(
        "seimei_heir", "The Heir of Seimei", CLASS_DEATH_ORACLE, FACTION_ENEMY, level=14,
        weapon_ids=["onmyou_orb","kanbei_scroll"],
        portrait_color=(40, 0, 40),
        archetype=ARCHETYPE_MYSTIC,
        bio=("Descendant of Abe no Seimei, the greatest onmyoji who ever lived.\n"
             "This heir has surpassed even their ancestor — mastering the forbidden\n"
             "arts that can unmake a soul. A late-game boss of terrible power."),
        quote="Seimei saw fate in the stars. I write it.",
        growth_rates={"hp":30,"str":10,"mag":100,"skl":80,"spd":45,"lck":20,"def":10,"res":70}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # NAMED UNITS FOR NEW UNPROMOTED CLASSES (15)
    # ══════════════════════════════════════════════════════════════════════════

    units["koito"] = Unit(
        "koito", "Shirabyoshi Koito", CLASS_SHIRABYOSHI, FACTION_PLAYER, level=5,
        weapon_ids=["kunai"],
        portrait_color=(255, 180, 200),
        archetype=ARCHETYPE_FREE,
        bio=("A wandering sacred dancer who joins the Oda cause after Nobunaga\n"
             "spares her shrine from burning. Her ritual dances channel kami\n"
             "energy into her allies, granting them renewed strength."),
        quote="Dance with me — or watch me dance. Either way, you'll feel better.",
        can_recruit=True, recruit_by=["any"],
        growth_rates={"hp":35,"str":20,"mag":55,"skl":55,"spd":75,"lck":80,"def":15,"res":60}
    )

    units["yuken"] = Unit(
        "yuken", "Yuken the Yamabushi", CLASS_YAMABUSHI, FACTION_ENEMY, level=7,
        weapon_ids=["steel_naginata","ofuda"],
        portrait_color=(120, 80, 40),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("A mountain ascetic warrior who has meditated at Kurama for twenty years.\n"
             "His naginata technique is formidable; his fire-walking rituals have\n"
             "given him an unnerving immunity to ordinary fear."),
        quote="The mountain taught me patience. I spent it all getting here.",
        can_recruit=True, recruit_by=["any"],
        growth_rates={"hp":60,"str":55,"mag":45,"skl":55,"spd":45,"lck":40,"def":55,"res":50}
    )

    units["hana_miko"] = Unit(
        "hana_miko", "Hana the Miko", CLASS_MIKO, FACTION_ALLY, level=5,
        weapon_ids=["heal_staff","iron_bow"],
        portrait_color=(255, 220, 220),
        archetype=ARCHETYPE_NOBLE,
        bio=("A shrine maiden of Ise Jingu, the most sacred shrine in Japan.\n"
             "Her prayers can turn aside arrows, and her spirit-blessed bow\n"
             "strikes truer than most trained archers' shots."),
        quote="The gods do not guarantee victory. They guarantee I will try.",
        growth_rates={"hp":40,"str":25,"mag":65,"skl":60,"spd":55,"lck":70,"def":20,"res":70}
    )

    units["kasai"] = Unit(
        "kasai", "Kasai the Nomad", CLASS_NOMAD, FACTION_ENEMY, level=6,
        weapon_ids=["iron_bow","iron_tanto"],
        portrait_color=(180, 160, 100),
        archetype=ARCHETYPE_FREE,
        bio=("A horse-archer from the northern steppe who rides for whoever pays\n"
             "well. His arrows can split a coin at a hundred yards and he never\n"
             "sleeps on the same patch of ground twice."),
        quote="I don't fight for lords. I fight for the wind at my back.",
        can_recruit=True, recruit_by=["any"],
        growth_rates={"hp":45,"str":50,"mag":10,"skl":70,"spd":70,"lck":55,"def":35,"res":20}
    )

    units["ishida_guard"] = Unit(
        "ishida_guard", "Ishida's Iron Guard", CLASS_FOOT_GUARD, FACTION_ENEMY, level=7,
        weapon_ids=["steel_yari","steel_tetsubo"],
        portrait_color=(160, 160, 140),
        archetype=ARCHETYPE_LOYAL,
        bio=("One of Ishida Mitsunari's elite castle garrison guards.\n"
             "Immovable in defense, they have held fortress gates against forces\n"
             "ten times their number. They do not retreat."),
        quote="This gate does not open. Not for you. Not for anyone.",
        growth_rates={"hp":70,"str":50,"mag":5,"skl":45,"spd":30,"lck":30,"def":75,"res":30}
    )

    units["dohei"] = Unit(
        "dohei", "Dohei the Merchant", CLASS_MERCHANT, FACTION_ALLY, level=4,
        weapon_ids=["iron_tanto","iron_bow"],
        portrait_color=(200, 170, 100),
        archetype=ARCHETYPE_STRATEGIST,
        bio=("A cunning merchant-soldier who profits from every campaign.\n"
             "He carries extra supplies, trades weapons mid-battle, and always\n"
             "knows where the nearest cache of iron is buried."),
        quote="War is terrible. Terrible for most people. Excellent for me.",
        can_recruit=True, recruit_by=["any"],
        growth_rates={"hp":40,"str":35,"mag":25,"skl":55,"spd":55,"lck":65,"def":30,"res":40}
    )

    units["kuro_musha"] = Unit(
        "kuro_musha", "Kuro the Wandering Warrior", CLASS_MUSHA, FACTION_ENEMY, level=6,
        weapon_ids=["steel_katana","iron_yari"],
        portrait_color=(120, 100, 80),
        archetype=ARCHETYPE_FREE,
        bio=("A masterless wandering warrior who fights for whoever has the most\n"
             "interesting battle ahead. No clan owns him. No lord commands him.\n"
             "He fights because it's what he does best."),
        quote="I've fought for a dozen lords. You might be worth a thirteenth.",
        can_recruit=True, recruit_by=["any"],
        growth_rates={"hp":55,"str":60,"mag":10,"skl":60,"spd":55,"lck":50,"def":50,"res":20}
    )

    units["gennosuke"] = Unit(
        "gennosuke", "Gennosuke the Yojimbo", CLASS_YOJIMBO, FACTION_ENEMY, level=7,
        weapon_ids=["steel_katana","steel_nodachi"],
        portrait_color=(80, 80, 60),
        archetype=ARCHETYPE_LOYAL,
        bio=("A legendary bodyguard known across three provinces.\n"
             "He has defended his current lord through seventeen assassination\n"
             "attempts. He charges a great deal. He is worth it."),
        quote="You want past me? That'll cost you more than money.",
        can_recruit=True, recruit_by=["any"],
        growth_rates={"hp":60,"str":60,"mag":10,"skl":65,"spd":55,"lck":45,"def":60,"res":20}
    )

    units["mizuki"] = Unit(
        "mizuki", "Mizuki the Water Witch", CLASS_WATER_WITCH, FACTION_ALLY, level=6,
        weapon_ids=["ofuda","heal_staff"],
        portrait_color=(100, 160, 220),
        archetype=ARCHETYPE_MYSTIC,
        bio=("A water-spirit medium who walks barefoot on river banks and\n"
             "communes with the water kami. Her ice-cold magic flash-freezes\n"
             "enemy formations and heals allies with cool, purifying waters."),
        quote="The river knows everything. It just takes a moment to listen.",
        growth_rates={"hp":38,"str":10,"mag":75,"skl":60,"spd":55,"lck":65,"def":20,"res":75}
    )

    units["kagero_fire"] = Unit(
        "kagero_fire", "Kagero the Fire Acolyte", CLASS_FIRE_ACOLYTE, FACTION_ENEMY, level=6,
        weapon_ids=["ofuda","tanegashima"],
        portrait_color=(220, 100, 40),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("A fire-cult acolyte who combines mystical flame-calling with the\n"
             "Oda's new tanegashima rifles. The result is a walking conflagration\n"
             "that even veteran warriors prefer to avoid."),
        quote="Everything burns eventually. I just help it along.",
        can_recruit=True, recruit_by=["any"],
        growth_rates={"hp":45,"str":20,"mag":70,"skl":55,"spd":50,"lck":40,"def":25,"res":60}
    )

    units["musashibou"] = Unit(
        "musashibou", "Musashibou Benkei", CLASS_BLADE_MONK, FACTION_ENEMY, level=9,
        weapon_ids=["steel_katana","iron_naginata"],
        portrait_color=(160, 100, 60),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("The legendary warrior-monk of Gojo Bridge. He collected 999 swords\n"
             "from defeated samurai; the 1000th led to his downfall and greatest\n"
             "loyalty. A historical legend appearing as an enemy boss."),
        quote="Nine hundred ninety-nine swords I took. You will be one more.",
        growth_rates={"hp":70,"str":65,"mag":35,"skl":65,"spd":50,"lck":45,"def":60,"res":50}
    )

    units["gorozo"] = Unit(
        "gorozo", "Gorozo the Rogue", CLASS_ROGUE, FACTION_PLAYER, level=4,
        weapon_ids=["kunai","iron_chain"],
        portrait_color=(60, 50, 40),
        archetype=ARCHETYPE_FREE,
        bio=("An outlaw-thief who joins the Oda on a dare and never quite leaves.\n"
             "He claims to be able to open any lock and steal anything not nailed\n"
             "down — and some things that are."),
        quote="I'm not a spy. Spies have ideology. I just enjoy this sort of thing.",
        can_recruit=True, recruit_by=["goemon", "any"],
        growth_rates={"hp":40,"str":45,"mag":20,"skl":75,"spd":75,"lck":70,"def":25,"res":30}
    )

    units["kanemitsu"] = Unit(
        "kanemitsu", "Lord Kanemitsu", CLASS_COURT_NOBLE, FACTION_ENEMY, level=7,
        weapon_ids=["kanbei_scroll","iron_katana"],
        portrait_color=(200, 190, 160),
        archetype=ARCHETYPE_NOBLE,
        bio=("A Kyoto court noble who commands through political maneuvering\n"
             "as much as military skill. His network of informants and debts\n"
             "called in makes him dangerous even without drawing a sword."),
        quote="War is simply politics conducted by louder means.",
        can_recruit=True, recruit_by=["nobunaga", "any"],
        growth_rates={"hp":40,"str":35,"mag":60,"skl":55,"spd":50,"lck":65,"def":30,"res":60}
    )

    units["umio"] = Unit(
        "umio", "Umio the Sea Soldier", CLASS_SEA_SOLDIER, FACTION_ENEMY, level=5,
        weapon_ids=["iron_katana","steel_yari"],
        portrait_color=(60, 80, 140),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("A grizzled naval foot soldier who has fought in every sea battle\n"
             "from Kyushu to the Japan Sea. Equally at home on a rocking deck\n"
             "or a rain-soaked beach."),
        quote="Land, sea, river — they're all the same to me. Wet and full of enemies.",
        can_recruit=True, recruit_by=["motochika", "any"],
        growth_rates={"hp":60,"str":55,"mag":5,"skl":50,"spd":50,"lck":45,"def":55,"res":25}
    )

    units["young_takeda"] = Unit(
        "young_takeda", "Young Takeda Retainer", CLASS_KENIN, FACTION_ENEMY, level=3,
        weapon_ids=["iron_katana"],
        portrait_color=(140, 160, 190),
        archetype=ARCHETYPE_LOYAL,
        bio=("A young Takeda clan retainer, barely old enough to hold his sword\n"
             "properly but burning with loyalty to the Tiger of Kai.\n"
             "Raw potential waiting to be forged."),
        quote="I'll prove myself! Lord Shingen will see!",
        can_recruit=True, recruit_by=["any"],
        growth_rates={"hp":55,"str":55,"mag":15,"skl":60,"spd":55,"lck":55,"def":45,"res":25}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # NAMED UNITS FOR NEW PROMOTED CLASSES (4)
    # ══════════════════════════════════════════════════════════════════════════

    units["musashi"] = Unit(
        "musashi", "Miyamoto Musashi", CLASS_SWORD_SAINT, FACTION_ALLY, level=10,
        weapon_ids=["dojikiri","muramasa"],
        portrait_color=(220, 60, 60),
        archetype=ARCHETYPE_HERO,
        bio=("Japan's greatest swordsman — undefeated in over sixty duels.\n"
             "He appears on the battlefield like a legend made flesh,\n"
             "his two-sword style incomprehensible to any opponent."),
        quote="There is nothing outside of yourself that can ever enable you to get better. Everything is within.",
        growth_rates={"hp":55,"str":80,"mag":10,"skl":95,"spd":80,"lck":50,"def":50,"res":20}
    )

    units["matsu"] = Unit(
        "matsu", "Matsu (Lady Maeda)", CLASS_VALKYRIE, FACTION_ALLY, level=8,
        weapon_ids=["physic_staff","silver_bow"],
        portrait_color=(240, 200, 240),
        archetype=ARCHETYPE_NOBLE,
        bio=("Wife of Maeda Toshiie, the legendary Lady Maeda who once faced down\n"
             "Tokugawa's retainers alone in her garden with a naginata. Now she rides\n"
             "into battle as healer and protector of the Maeda cause."),
        quote="My husband charges forward. I make sure there's still someone to come home to.",
        growth_rates={"hp":45,"str":25,"mag":80,"skl":65,"spd":65,"lck":75,"def":35,"res":80}
    )

    units["shimazu_great_gen"] = Unit(
        "shimazu_great_gen", "Shimazu Great General", CLASS_GREAT_GENERAL, FACTION_ENEMY, level=12,
        weapon_ids=["nihongo","oni_tetsubo"],
        portrait_color=(210, 210, 220),
        archetype=ARCHETYPE_LOYAL,
        bio=("The supreme armored commander of the Shimazu western army.\n"
             "His armor has stopped fifteen arrows and three cannon balls.\n"
             "He considers this a slow morning."),
        quote="Come. I have armor for all occasions. Including this one.",
        growth_rates={"hp":80,"str":65,"mag":10,"skl":50,"spd":25,"lck":35,"def":90,"res":40}
    )

    units["imagawa_warlord"] = Unit(
        "imagawa_warlord", "Imagawa Battle-Commander", CLASS_WARLORD, FACTION_ENEMY, level=10,
        weapon_ids=["steel_tetsubo","odenta_mitsu"],
        portrait_color=(220, 50, 30),
        archetype=ARCHETYPE_HOTHEAD,
        bio=("The military strongarm of the Imagawa army — all brute power and\n"
             "battlefield intimidation. Hideyoshi once said this man was the\n"
             "only enemy who ever actually made him run."),
        quote="FORWARD! SMASH EVERYTHING! WORRY LATER!",
        growth_rates={"hp":80,"str":80,"mag":15,"skl":50,"spd":50,"lck":30,"def":70,"res":20}
    )

    # ══════════════════════════════════════════════════════════════════════════
    # PROMOTED GENERIC ENEMY UNITS for Chapters 13-20
    # ══════════════════════════════════════════════════════════════════════════
    # pe_ prefix = promoted enemy, for use in late chapters

    _generic("pe_ron1",  "Elite Ronin",      CLASS_RONIN,         FACTION_ENEMY, 10, ["silver_katana","steel_nodachi"],  (110,20,20))
    _generic("pe_ron2",  "Master Ronin",     CLASS_RONIN,         FACTION_ENEMY, 13, ["dojikiri","muramasa"],            (100,10,10))
    _generic("pe_gen1",  "Iron General",     CLASS_GENERAL,       FACTION_ENEMY, 11, ["silver_yari","steel_tetsubo"],    (130,130,130))
    _generic("pe_gen2",  "Great General",    CLASS_GREAT_GENERAL, FACTION_ENEMY, 12, ["nihongo","oni_tetsubo"],          (205,205,215))
    _generic("pe_hat1",  "Elite Hatamoto",   CLASS_HATAMOTO,      FACTION_ENEMY, 11, ["silver_katana","jumonji_yari"],   (150,90,50))
    _generic("pe_hat2",  "Grand Hatamoto",   CLASS_HATAMOTO,      FACTION_ENEMY, 14, ["dojikiri","silver_yari"],         (140,80,40))
    _generic("pe_gk1",   "Great Knight",     CLASS_GREAT_KNIGHT,  FACTION_ENEMY, 11, ["silver_katana","jumonji_yari"],   (120,120,160))
    _generic("pe_gk2",   "Iron Great Knight",CLASS_GREAT_KNIGHT,  FACTION_ENEMY, 13, ["dojikiri","silver_yari"],         (110,110,150))
    _generic("pe_nc1",   "Lord's Cavalry",   CLASS_NOBLE_CAVALRY, FACTION_ENEMY, 11, ["silver_katana","silver_yari"],    (205,185,70))
    _generic("pe_nc2",   "Grand Cavalry",    CLASS_NOBLE_CAVALRY, FACTION_ENEMY, 13, ["dojikiri","nihongo"],             (195,175,60))
    _generic("pe_fk1",   "Falcon Knight",    CLASS_FALCON_KNIGHT, FACTION_ENEMY, 11, ["silver_naginata","mend_staff"],   (200,180,255))
    _generic("pe_fk2",   "Sky Falcon",       CLASS_FALCON_KNIGHT, FACTION_ENEMY, 13, ["flying_naginata","physic_staff"], (190,170,245))
    _generic("pe_dk1",   "Dragon Knight",    CLASS_DRAGON_KNIGHT, FACTION_ENEMY, 12, ["silver_yari","dojikiri"],         (185,65,20))
    _generic("pe_dk2",   "War Dragon",       CLASS_DRAGON_KNIGHT, FACTION_ENEMY, 15, ["bishamonten","honjo_masamune"],   (175,55,10))
    _generic("pe_sr1",   "Storm Rider",      CLASS_STORM_RIDER,   FACTION_ENEMY, 11, ["windcutter","steel_katana"],      (140,190,255))
    _generic("pe_sr2",   "Sky Assassin",     CLASS_STORM_RIDER,   FACTION_ENEMY, 14, ["windcutter","muramasa"],          (130,180,245))
    _generic("pe_sl1",   "Sky Lancer",       CLASS_SKY_LANCER,    FACTION_ENEMY, 11, ["silver_yari","iron_naginata"],    (160,100,45))
    _generic("pe_sl2",   "Iron Sky Lancer",  CLASS_SKY_LANCER,    FACTION_ENEMY, 13, ["nihongo","flying_naginata"],      (150,90,35))
    _generic("pe_lc1",   "Elite Cavalry",    CLASS_LANCE_CAVALRY, FACTION_ENEMY, 10, ["silver_yari","steel_naginata"],   (195,115,40))
    _generic("pe_lc2",   "Lance Master",     CLASS_LANCE_CAVALRY, FACTION_ENEMY, 12, ["nihongo","silver_naginata"],      (185,105,30))
    _generic("pe_wl1",   "Warlord",          CLASS_WARLORD,       FACTION_ENEMY, 11, ["oni_tetsubo","steel_nodachi"],    (215,45,25))
    _generic("pe_wl2",   "Battle Warlord",   CLASS_WARLORD,       FACTION_ENEMY, 14, ["oni_tetsubo","fuujin_nodachi"],   (205,35,15))
    _generic("pe_gg1",   "Great General",    CLASS_GREAT_GENERAL, FACTION_ENEMY, 13, ["nihongo","oni_tetsubo"],          (200,200,210))
    _generic("pe_tm1",   "Tengu Master",     CLASS_TENGU_MASTER,  FACTION_ENEMY, 10, ["windcutter","onmyou_orb"],        (85,45,145))
    _generic("pe_ea1",   "Eagle Archer",     CLASS_EAGLE_ARCHER,  FACTION_ENEMY, 10, ["silver_bow","yumi_anti_air"],     (160,210,140))
    _generic("pe_sp1",   "Void Prophet",     CLASS_VOID_PROPHET,  FACTION_ENEMY, 10, ["onmyou_orb"],                    (55,15,75))
    _generic("pe_jd1",   "Jade Sorceress",   CLASS_JADE_SORCERESS,FACTION_ENEMY, 11, ["onmyou_orb","kanbei_scroll"],    (130,215,155))
    _generic("pe_ph1",   "Phantom Knight",   CLASS_PHANTOM_KNIGHT,FACTION_ENEMY, 10, ["muramasa","onmyou_orb"],         (75,75,115))
    _generic("pe_we1",   "War Elephant",     CLASS_WAR_ELEPHANT,  FACTION_ENEMY, 11, ["steel_tetsubo","steel_yari"],    (85,65,50))

    # New class generic enemies (unpromoted, for variety in mid-game)
    _generic("e_yam1",  "Yamabushi",         CLASS_YAMABUSHI,     FACTION_ENEMY, 4,  ["iron_naginata","ofuda"],         (110,70,35))
    _generic("e_yam2",  "Elder Yamabushi",   CLASS_YAMABUSHI,     FACTION_ENEMY, 7,  ["steel_naginata","shakujo"],      (100,60,25))
    _generic("e_miko1", "Shrine Maiden",     CLASS_MIKO,          FACTION_ENEMY, 3,  ["heal_staff","iron_bow"],         (255,210,210))
    _generic("e_nom1",  "Nomad Rider",       CLASS_NOMAD,         FACTION_ENEMY, 4,  ["iron_bow","iron_tanto"],         (170,150,90))
    _generic("e_nom2",  "Nomad Scout",       CLASS_NOMAD,         FACTION_ENEMY, 6,  ["steel_bow","iron_tanto"],        (160,140,80))
    _generic("e_fgd1",  "Foot Guard",        CLASS_FOOT_GUARD,    FACTION_ENEMY, 4,  ["iron_yari","iron_tetsubo"],      (150,150,130))
    _generic("e_fgd2",  "Iron Foot Guard",   CLASS_FOOT_GUARD,    FACTION_ENEMY, 7,  ["steel_yari","steel_tetsubo"],    (140,140,120))
    _generic("e_mush1", "Wandering Musha",   CLASS_MUSHA,         FACTION_ENEMY, 4,  ["iron_katana","iron_yari"],       (110,90,70))
    _generic("e_mush2", "Veteran Musha",     CLASS_MUSHA,         FACTION_ENEMY, 7,  ["steel_katana","steel_yari"],     (100,80,60))
    _generic("e_yoji1", "Yojimbo",           CLASS_YOJIMBO,       FACTION_ENEMY, 5,  ["steel_katana"],                  (75,75,55))
    _generic("e_yoji2", "Master Yojimbo",    CLASS_YOJIMBO,       FACTION_ENEMY, 8,  ["steel_katana","steel_nodachi"],  (65,65,45))
    _generic("e_rogue1","Outlaw",            CLASS_ROGUE,         FACTION_ENEMY, 3,  ["iron_tanto","iron_chain"],       (55,45,35))
    _generic("e_rogue2","Bandit Rogue",      CLASS_ROGUE,         FACTION_ENEMY, 5,  ["steel_tanto","iron_chain"],      (45,35,25))
    _generic("e_kenin1","Young Retainer",    CLASS_KENIN,         FACTION_ENEMY, 1,  ["iron_katana"],                   (130,150,180))
    _generic("e_kenin2","Retainer",          CLASS_KENIN,         FACTION_ENEMY, 3,  ["iron_katana"],                   (120,140,170))
    _generic("e_ssol1", "Sea Soldier",       CLASS_SEA_SOLDIER,   FACTION_ENEMY, 4,  ["iron_katana","iron_yari"],       (50,70,130))
    _generic("e_ssol2", "Sea Veteran",       CLASS_SEA_SOLDIER,   FACTION_ENEMY, 6,  ["steel_katana","steel_yari"],     (40,60,120))
    _generic("e_blm1",  "Blade Monk",        CLASS_BLADE_MONK,    FACTION_ENEMY, 4,  ["iron_katana","iron_naginata"],   (150,90,50))
    _generic("e_blm2",  "Sword Monk",        CLASS_BLADE_MONK,    FACTION_ENEMY, 7,  ["steel_katana","steel_naginata"], (140,80,40))

    # Player-side generics for new classes
    _generic("oda_yam1",  "Oda Yamabushi",   CLASS_YAMABUSHI,     FACTION_PLAYER, 3, ["iron_naginata","ofuda"],         (110,70,35))
    _generic("oda_miko1", "Oda Miko",        CLASS_MIKO,          FACTION_PLAYER, 3, ["heal_staff","iron_bow"],         (255,210,210))
    _generic("oda_mush1", "Oda Musha",       CLASS_MUSHA,         FACTION_PLAYER, 3, ["iron_katana","iron_yari"],       (110,90,70))
    _generic("oda_fgd1",  "Oda Foot Guard",  CLASS_FOOT_GUARD,    FACTION_PLAYER, 3, ["iron_yari","iron_tetsubo"],      (150,150,130))
    _generic("oda_blm1",  "Oda Blade Monk",  CLASS_BLADE_MONK,    FACTION_PLAYER, 3, ["iron_katana","iron_naginata"],   (150,90,50))

    return units


# ─────────────────────────────────────────────────────────────────────────────
# Mercenary shop units — weaker than named characters, buyable in prep screen
# ─────────────────────────────────────────────────────────────────────────────

# Mercs have low-but-valid growth rates (floor enforced by _level_up clamping)
_MERC_GROWTH = {"hp": 65, "str": 30, "mag": 20, "skl": 30,
                "spd": 30, "lck": 20, "def": 28, "res": 20}

def create_mercenary(merc_id, chapter_index=0):
    '''
    Create a fresh buyable mercenary scaled to chapter number.
    Mercs are intentionally weaker than named player characters.
    chapter_index 0-19 gives a mild level bump (max +5 levels).
    '''
    level = max(1, 1 + chapter_index // 4)   # lv1 ch1-3, lv2 ch4-7, etc.
    _MERC_DEFS = {
        "merc_ashigaru": ("Hired Ashigaru",   CLASS_ASHIGARU,   ["iron_yari",  "iron_tanto"],     (120, 100, 80)),
        "merc_spearman": ("Hired Spearman",   CLASS_SPEARMAN,   ["iron_yari",  "iron_naginata"],  (120, 110, 90)),
        "merc_archer":   ("Hired Archer",     CLASS_ARCHER,     ["iron_bow",   "iron_tanto"],     (100, 130, 80)),
        "merc_samurai":  ("Hired Samurai",    CLASS_SAMURAI,    ["iron_katana","iron_tanto"],     (110, 90,  60)),
        "merc_cavalry":  ("Hired Cavalry",    CLASS_CAVALRY,    ["iron_yari",  "iron_katana"],    (90,  100, 130)),
        "merc_ninja":    ("Hired Ninja",      CLASS_NINJA,      ["iron_tanto", "iron_chain"],     (60,  60,  80)),
        "merc_monk":     ("Hired Monk",       CLASS_MONK,       ["heal_staff", "iron_tanto"],     (200, 180, 140)),
        "merc_gunner":   ("Hired Gunner",     CLASS_GUNNER,     ["iron_gun",   "iron_tanto"],     (130, 120, 90)),
    }
    if merc_id not in _MERC_DEFS:
        raise KeyError(f"Unknown merc type: {merc_id}")
    name, cls, weapons, color = _MERC_DEFS[merc_id]
    u = Unit(
        merc_id, name, cls, FACTION_PLAYER, level=level,
        weapon_ids=weapons, portrait_color=color,
        bio="A mercenary hired for this campaign. Loyal to gold, not glory.",
        growth_rates=_MERC_GROWTH,
    )
    # Mercs have reduced stats — about 75% of a named unit's combat power
    u.max_hp = max(8, u.max_hp - 4)
    u.hp     = u.max_hp
    u.str_   = max(2, u.str_  - 2)
    u.mag    = max(1, u.mag   - 1)
    u.skl    = max(2, u.skl   - 2)
    u.spd    = max(2, u.spd   - 2)
    u.def_   = max(1, u.def_  - 2)
    u.res    = max(1, u.res   - 1)
    return u
