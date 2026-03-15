"""
Weapon definitions for Sengoku Tactics
"""
from game.constants import *


class Weapon:
    def __init__(self, weapon_id, name, weapon_type, might, hit, crit, weight,
                 min_range=1, max_range=1, uses=30, description=""):
        self.weapon_id   = weapon_id
        self.name        = name
        self.weapon_type = weapon_type
        self.might       = might    # damage bonus
        self.hit         = hit      # accuracy
        self.crit        = crit     # crit rate
        self.weight      = weight   # reduces speed
        self.min_range   = min_range
        self.max_range   = max_range
        self.uses        = uses
        self.current_uses= uses
        self.description = description

    def is_ranged(self):
        return self.max_range > 1

    def get_triangle_bonus(self, other_weapon):
        """Return +1, 0, or -1 based on weapon triangle."""
        if other_weapon is None:
            return 0
        my_type    = self.weapon_type
        their_type = other_weapon.weapon_type
        advantages = WEAPON_TRIANGLE.get(my_type, {})
        if their_type in advantages:
            return advantages[their_type]
        # Check if we're at disadvantage
        their_advantages = WEAPON_TRIANGLE.get(their_type, {})
        if my_type in their_advantages:
            return -1
        return 0

    def __repr__(self):
        return f"<Weapon {self.name} [{self.weapon_type}] Mt:{self.might} Hit:{self.hit} Crit:{self.crit}>"


# ─── Weapon Instances ────────────────────────────────────────────────────────

WEAPONS = {
    # Katana
    "iron_katana":     Weapon("iron_katana",    "Iron Katana",     WEAPON_KATANA,   5, 85, 0,  5, description="A reliable iron blade."),
    "steel_katana":    Weapon("steel_katana",   "Steel Katana",    WEAPON_KATANA,   8, 80, 0,  8, description="A heavier, stronger blade."),
    "silver_katana":   Weapon("silver_katana",  "Silver Katana",   WEAPON_KATANA,  12, 90, 5,  6, description="A finely crafted blade."),
    "muramasa":        Weapon("muramasa",        "Muramasa",        WEAPON_KATANA,  15, 75,15,  9, description="The cursed blade that thirsts for blood."),
    "masamune":        Weapon("masamune",        "Masamune",        WEAPON_KATANA,  14, 95,10,  5, description="The legendary blade of peace."),

    # Yari (Spear)
    "iron_yari":       Weapon("iron_yari",       "Iron Yari",       WEAPON_YARI,     6, 80, 0,  7, description="A standard ashigaru spear."),
    "steel_yari":      Weapon("steel_yari",      "Steel Yari",      WEAPON_YARI,     9, 75, 0, 10, description="Heavy cavalry-breaking spear."),
    "silver_yari":     Weapon("silver_yari",     "Silver Yari",     WEAPON_YARI,    13, 85, 5,  8, description="A balanced long spear."),
    "jumonji_yari":    Weapon("jumonji_yari",    "Jumonji Yari",    WEAPON_YARI,    11, 80,10,  9, description="Cross-headed spear, hard to deflect."),

    # Naginata
    "iron_naginata":   Weapon("iron_naginata",   "Iron Naginata",   WEAPON_NAGINATA, 7, 80, 0,  8, description="A polearm favored by sohei."),
    "steel_naginata":  Weapon("steel_naginata",  "Steel Naginata",  WEAPON_NAGINATA,10, 75, 0, 11, description="Heavy, armor-crushing swing."),
    "silver_naginata": Weapon("silver_naginata", "Silver Naginata", WEAPON_NAGINATA,14, 85, 5,  9, description="Refined warrior's polearm."),

    # Nodachi
    "iron_nodachi":    Weapon("iron_nodachi",    "Iron Nodachi",    WEAPON_NODACHI,  8, 75, 0, 12, description="A massive two-handed blade."),
    "steel_nodachi":   Weapon("steel_nodachi",   "Steel Nodachi",   WEAPON_NODACHI, 12, 70, 0, 15, description="Powerful but slow."),
    "odenta_mitsu":    Weapon("odenta_mitsu",    "Odenta-Mitsu",    WEAPON_NODACHI, 16, 80,10, 12, description="One of Japan's great swords."),

    # Tanto (Dagger)
    "iron_tanto":      Weapon("iron_tanto",      "Iron Tanto",      WEAPON_TANTO,    4, 90, 5,  2, description="A swift short blade."),
    "steel_tanto":     Weapon("steel_tanto",     "Steel Tanto",     WEAPON_TANTO,    6, 88, 8,  4, description="Poisoned for extra effect."),
    "kunai":           Weapon("kunai",           "Kunai",           WEAPON_TANTO,    3, 95,10,  1, min_range=1, max_range=2, description="Thrown with deadly precision."),

    # Bow
    "iron_bow":        Weapon("iron_bow",        "Iron Bow",        WEAPON_BOW,      5, 80, 0,  5, min_range=2, max_range=2, description="A standard ashigaru bow."),
    "steel_bow":       Weapon("steel_bow",       "Steel Bow",       WEAPON_BOW,      8, 75, 0,  8, min_range=2, max_range=2, description="A powerful war bow."),
    "silver_bow":      Weapon("silver_bow",      "Silver Bow",      WEAPON_BOW,     12, 85, 5,  6, min_range=2, max_range=2, description="Precise and powerful."),
    "yumi":            Weapon("yumi",            "Daikyu",          WEAPON_BOW,      9, 78, 5,  7, min_range=2, max_range=3, description="Long-range asymmetric bow."),
    "tanegashima":     Weapon("tanegashima",     "Tanegashima",     WEAPON_BOW,     14, 65, 0, 10, min_range=2, max_range=3, description="Matchlock rifle from the south seas."),

    # Tetsubo (Club/Mace)
    "iron_tetsubo":    Weapon("iron_tetsubo",    "Iron Tetsubo",    WEAPON_TETSUBO,  9, 75, 0, 13, description="A spiked iron war club."),
    "steel_tetsubo":   Weapon("steel_tetsubo",   "Steel Tetsubo",   WEAPON_TETSUBO, 13, 70, 0, 16, description="Devastates armor."),

    # Staff (Healing / Magic)
    "heal_staff":      Weapon("heal_staff",      "Heal Staff",      WEAPON_STAFF,    0, 100,0,  2, description="Restores 10 HP to an ally.", uses=20),
    "mend_staff":      Weapon("mend_staff",      "Mend Staff",      WEAPON_STAFF,    0, 100,0,  4, description="Restores 20 HP to an ally.", uses=15),
    "ofuda":           Weapon("ofuda",           "Ofuda",           WEAPON_STAFF,    8, 85, 5,  3, description="Paper talismans charged with spiritual power."),
    "shakujo":         Weapon("shakujo",         "Shakujo",         WEAPON_STAFF,   10, 80, 5,  8, description="The ringed staff of a warrior monk."),
}


def get_weapon(weapon_id):
    """Return a fresh copy of a weapon by id."""
    import copy
    w = WEAPONS.get(weapon_id)
    if w is None:
        raise KeyError(f"Unknown weapon id: {weapon_id}")
    return copy.copy(w)
