"""
Weapon definitions for Sengoku Tactics
"""
import copy
from game.constants import *


class Weapon:
    def __init__(self, weapon_id, name, weapon_type, might, hit, crit, weight,
                 min_range=1, max_range=1, uses=30, description="",
                 anti_flying=False, anti_mounted=False, magic_damage=False):
        self.weapon_id    = weapon_id
        self.name         = name
        self.weapon_type  = weapon_type
        self.might        = might
        self.hit          = hit
        self.crit         = crit
        self.weight       = weight
        self.min_range    = min_range
        self.max_range    = max_range
        self.uses         = uses
        self.current_uses = uses
        self.description  = description
        self.anti_flying  = anti_flying    # +5 dmg vs flyers
        self.anti_mounted = anti_mounted   # +5 dmg vs mounted
        self.magic_damage = magic_damage   # uses MAG, ignores DEF

    def is_ranged(self):
        return self.max_range > 1

    def get_triangle_bonus(self, other_weapon):
        if other_weapon is None:
            return 0
        my_type    = self.weapon_type
        their_type = other_weapon.weapon_type
        advantages = WEAPON_TRIANGLE.get(my_type, {})
        if their_type in advantages:
            return advantages[their_type]
        their_advantages = WEAPON_TRIANGLE.get(their_type, {})
        if my_type in their_advantages:
            return -1
        return 0

    def __repr__(self):
        return (f"<Weapon {self.name} [{self.weapon_type}] "
                f"Mt:{self.might} Hit:{self.hit} Crit:{self.crit}>")


# ─── All Weapons ──────────────────────────────────────────────────────────────
WEAPONS = {
    # ── Katana ───────────────────────────────────────────────────────────────
    "iron_katana":     Weapon("iron_katana",    "Iron Katana",     WEAPON_KATANA,    5, 85,  0,  5,
                              description="A reliable iron blade."),
    "steel_katana":    Weapon("steel_katana",   "Steel Katana",    WEAPON_KATANA,    8, 80,  0,  8,
                              description="A heavier, stronger blade."),
    "silver_katana":   Weapon("silver_katana",  "Silver Katana",   WEAPON_KATANA,   12, 90,  5,  6,
                              description="A finely crafted blade."),
    "muramasa":        Weapon("muramasa",        "Muramasa",        WEAPON_KATANA,   15, 75, 15,  9,
                              description="The cursed blade that thirsts for blood."),
    "masamune":        Weapon("masamune",        "Masamune",        WEAPON_KATANA,   14, 95, 10,  5,
                              description="The legendary blade of peace."),
    "raikiri":         Weapon("raikiri",         "Raikiri",         WEAPON_KATANA,   13, 88, 12,  6,
                              description="'Lightning Cutter' — Naoe Kanetsugu's blade."),
    "dojikiri":        Weapon("dojikiri",        "Dojigiri Yasutsuna", WEAPON_KATANA, 16, 90, 8, 7,
                              description="Greatest of Japan's five great swords."),
    "otenta_mitsu":    Weapon("otenta_mitsu",    "Otenta-Mitsu",    WEAPON_KATANA,   14, 92, 10,  6,
                              description="Revered blade of the Date clan."),
    "heishi_shorin":   Weapon("heishi_shorin",   "Heishi Shorin",   WEAPON_KATANA,   11, 88,  5,  5,
                              description="A blade that cuts illusions as well as flesh."),
    "honjo_masamune":  Weapon("honjo_masamune",  "Honjo Masamune",  WEAPON_KATANA,   17, 95, 15,  5,
                              description="The supreme blade, symbol of the Shogunate."),

    # ── Yari ─────────────────────────────────────────────────────────────────
    "iron_yari":       Weapon("iron_yari",       "Iron Yari",       WEAPON_YARI,      6, 80,  0,  7,
                              description="Standard ashigaru spear."),
    "steel_yari":      Weapon("steel_yari",      "Steel Yari",      WEAPON_YARI,      9, 75,  0, 10,
                              description="Heavy cavalry-breaking spear."),
    "silver_yari":     Weapon("silver_yari",     "Silver Yari",     WEAPON_YARI,     13, 85,  5,  8,
                              description="A balanced long spear."),
    "jumonji_yari":    Weapon("jumonji_yari",    "Jumonji Yari",    WEAPON_YARI,     11, 80, 10,  9,
                              description="Cross-headed spear, hard to deflect.",
                              anti_mounted=True),
    "tonbo_kiri":      Weapon("tonbo_kiri",      "Tonbo-Kiri",      WEAPON_YARI,     16, 88,  8,  8,
                              description="Honda Tadakatsu's legendary dragonfly-cutter.",
                              anti_mounted=True),
    "nihongo":         Weapon("nihongo",         "Nihongo",         WEAPON_YARI,     15, 85,  5,  9,
                              description="One of Japan's three great spears."),

    # ── Naginata ─────────────────────────────────────────────────────────────
    "iron_naginata":   Weapon("iron_naginata",   "Iron Naginata",   WEAPON_NAGINATA,  7, 80,  0,  8,
                              description="Polearm favored by sohei."),
    "steel_naginata":  Weapon("steel_naginata",  "Steel Naginata",  WEAPON_NAGINATA, 10, 75,  0, 11,
                              description="Heavy, armor-crushing swing."),
    "silver_naginata": Weapon("silver_naginata", "Silver Naginata", WEAPON_NAGINATA, 14, 85,  5,  9,
                              description="Refined warrior's polearm."),
    "flying_naginata": Weapon("flying_naginata", "Sky Naginata",    WEAPON_NAGINATA, 12, 82,  8,  7,
                              description="Weighted for aerial strikes.",
                              anti_flying=True),
    "bishamonten":     Weapon("bishamonten",     "Bishamonten Naginata", WEAPON_NAGINATA, 17, 88, 12, 9,
                              description="Kenshin's divine polearm, blessed by the war god."),

    # ── Nodachi ──────────────────────────────────────────────────────────────
    "iron_nodachi":    Weapon("iron_nodachi",    "Iron Nodachi",    WEAPON_NODACHI,   8, 75,  0, 12,
                              description="A massive two-handed blade."),
    "steel_nodachi":   Weapon("steel_nodachi",   "Steel Nodachi",   WEAPON_NODACHI,  12, 70,  0, 15,
                              description="Powerful but slow."),
    "odenta_mitsu":    Weapon("odenta_mitsu",    "Odenta-Mitsu",    WEAPON_NODACHI,  16, 80, 10, 12,
                              description="One of Japan's great swords."),
    "fuujin_nodachi":  Weapon("fuujin_nodachi",  "Fuujin Nodachi",  WEAPON_NODACHI,  14, 78,  8, 10,
                              description="Wind god's slash — strikes like a gale."),

    # ── Tanto / Dagger ───────────────────────────────────────────────────────
    "iron_tanto":      Weapon("iron_tanto",      "Iron Tanto",      WEAPON_TANTO,     4, 90,  5,  2,
                              description="A swift short blade."),
    "steel_tanto":     Weapon("steel_tanto",     "Steel Tanto",     WEAPON_TANTO,     6, 88,  8,  4,
                              description="Poisoned for extra effect."),
    "kunai":           Weapon("kunai",           "Kunai",           WEAPON_TANTO,     3, 95, 10,  1,
                              min_range=1, max_range=2,
                              description="Thrown with deadly precision."),
    "windcutter":      Weapon("windcutter",      "Windcutter",      WEAPON_TANTO,     8, 92, 15,  3,
                              description="Fuma Kotaro's blade — cuts the wind itself."),
    "jitte":           Weapon("jitte",           "Jitte",           WEAPON_TANTO,     5, 94,  5,  2,
                              description="Pronged blade used to disarm opponents."),

    # ── Bow ──────────────────────────────────────────────────────────────────
    "iron_bow":        Weapon("iron_bow",        "Iron Bow",        WEAPON_BOW,       5, 80,  0,  5,
                              min_range=2, max_range=2, description="Standard ashigaru bow."),
    "steel_bow":       Weapon("steel_bow",       "Steel Bow",       WEAPON_BOW,       8, 75,  0,  8,
                              min_range=2, max_range=2, description="A powerful war bow."),
    "silver_bow":      Weapon("silver_bow",      "Silver Bow",      WEAPON_BOW,      12, 85,  5,  6,
                              min_range=2, max_range=2, description="Precise and powerful."),
    "daikyu":          Weapon("daikyu",          "Daikyu",          WEAPON_BOW,       9, 78,  5,  7,
                              min_range=2, max_range=3,
                              description="Asymmetric long bow — extended range.",
                              anti_flying=True),
    "yumi_anti_air":   Weapon("yumi_anti_air",   "Sky-Piercer Bow", WEAPON_BOW,      11, 80, 10,  7,
                              min_range=2, max_range=3,
                              description="Specially balanced to strike flying targets.",
                              anti_flying=True),
    "heavenly_bow":    Weapon("heavenly_bow",    "Heavenly Bow",    WEAPON_BOW,      14, 88, 12,  6,
                              min_range=2, max_range=3, description="A divine archer's weapon.",
                              anti_flying=True),
    "tsuruhime_bow":   Weapon("tsuruhime_bow",   "Lady's Swift Bow",WEAPON_BOW,      10, 92, 12,  4,
                              min_range=2, max_range=2, description="Tsuruhime's personal bow."),

    # ── Tetsubo ───────────────────────────────────────────────────────────────
    "iron_tetsubo":    Weapon("iron_tetsubo",    "Iron Tetsubo",    WEAPON_TETSUBO,   9, 75,  0, 13,
                              description="A spiked iron war club."),
    "steel_tetsubo":   Weapon("steel_tetsubo",   "Steel Tetsubo",   WEAPON_TETSUBO,  13, 70,  0, 16,
                              description="Devastates armor."),
    "oni_tetsubo":     Weapon("oni_tetsubo",     "Oni Tetsubo",     WEAPON_TETSUBO,  17, 68,  5, 18,
                              description="Demon's club — shatters through any defense."),

    # ── Gun (Firearms) ────────────────────────────────────────────────────────
    "tanegashima":     Weapon("tanegashima",     "Tanegashima",     WEAPON_GUN,      14, 65,  0, 10,
                              min_range=2, max_range=3,
                              description="Portuguese matchlock rifle. Slow to reload."),
    "improved_gun":    Weapon("improved_gun",    "Improved Matchlock",WEAPON_GUN,    16, 70,  5, 11,
                              min_range=2, max_range=3,
                              description="Faster reload, greater powder charge."),
    "volley_gun":      Weapon("volley_gun",      "Volley Matchlock", WEAPON_GUN,     12, 80,  3,  8,
                              min_range=2, max_range=2,
                              description="Nagashino formation volleys. +Hit, -Range."),
    "saika_rifle":     Weapon("saika_rifle",     "Saika Rifle",     WEAPON_GUN,      18, 72, 10, 10,
                              min_range=2, max_range=3,
                              description="Magoichi's custom long rifle. Deadly accuracy."),

    # ── Chain (Kusarigama) ────────────────────────────────────────────────────
    "iron_chain":      Weapon("iron_chain",      "Kusarigama",      WEAPON_CHAIN,     7, 82,  8,  6,
                              min_range=1, max_range=2,
                              description="Chain-sickle that can hook from a distance."),
    "silver_chain":    Weapon("silver_chain",    "Silver Kusarigama",WEAPON_CHAIN,   11, 85, 12,  7,
                              min_range=1, max_range=2,
                              description="Precise chain weapon of the Iga schools."),
    "fuma_chain":      Weapon("fuma_chain",      "Fuma Shadow Chain",WEAPON_CHAIN,   14, 88, 18,  6,
                              min_range=1, max_range=2,
                              description="Fuma Kotaro's deadly shadow weapon."),

    # ── Staff (Healing / Magic) ───────────────────────────────────────────────
    "heal_staff":      Weapon("heal_staff",      "Heal Staff",      WEAPON_STAFF,     0, 100, 0,  2,
                              description="Restores 10 HP to an ally.", uses=20),
    "mend_staff":      Weapon("mend_staff",      "Mend Staff",      WEAPON_STAFF,     0, 100, 0,  4,
                              description="Restores 20 HP to an ally.", uses=15),
    "physic_staff":    Weapon("physic_staff",    "Physic Staff",    WEAPON_STAFF,     0, 100, 0,  3,
                              min_range=1, max_range=3,
                              description="Heals at range — target needn't be adjacent.", uses=10),
    "ofuda":           Weapon("ofuda",           "Ofuda",           WEAPON_STAFF,     8, 85,  5,  3,
                              description="Paper talismans charged with spiritual power.",
                              magic_damage=True),
    "shakujo":         Weapon("shakujo",         "Shakujo",         WEAPON_STAFF,    10, 80,  5,  8,
                              description="Ringed staff of a warrior monk."),
    "onmyou_orb":      Weapon("onmyou_orb",      "Onmyou Orb",      WEAPON_STAFF,    13, 88,  8,  4,
                              description="Divination sphere — pierces magical resistance.",
                              magic_damage=True, uses=20),
    "kanbei_scroll":   Weapon("kanbei_scroll",   "Kanbei's Scroll", WEAPON_STAFF,    11, 90, 10,  3,
                              description="War stratagem encoded in spiritual power.",
                              magic_damage=True),
    "amulet_staff":    Weapon("amulet_staff",    "Sacred Amulet",   WEAPON_STAFF,     0, 100, 0,  2,
                              description="Restores 15 HP and grants +5 Def for 1 turn.", uses=12),
}


def get_weapon(weapon_id):
    """Return a fresh copy of a weapon by id."""
    w = WEAPONS.get(weapon_id)
    if w is None:
        raise KeyError(f"Unknown weapon id: {weapon_id}")
    return copy.copy(w)
