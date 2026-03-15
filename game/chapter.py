"""
Chapter definitions for Sengoku Tactics
"""
import copy
from game.constants import *
from game.unit import create_unit_roster
from game.map import MAP_BUILDERS


class Chapter:
    def __init__(self, number, title, subtitle, narrative_intro, narrative_victory,
                 narrative_defeat, objective, objective_detail,
                 player_units, enemy_units, ally_units,
                 map_builder, turn_limit=None):
        self.number    = number
        self.title     = title
        self.subtitle  = subtitle
        self.narrative_intro   = narrative_intro
        self.narrative_victory = narrative_victory
        self.narrative_defeat  = narrative_defeat
        self.objective         = objective
        self.objective_detail  = objective_detail
        self.player_unit_defs  = player_units  # list of (unit_id, start_x, start_y)
        self.enemy_unit_defs   = enemy_units   # list of (unit_id, start_x, start_y)
        self.ally_unit_defs    = ally_units    # list of (unit_id, start_x, start_y)
        self.map_builder = map_builder
        self.turn_limit  = turn_limit  # None = unlimited

    def build(self, roster):
        """Instantiate the chapter — returns (game_map, player_units, enemy_units, ally_units)."""
        gmap = self.map_builder()

        def place(unit_defs, faction):
            placed = []
            for (uid, x, y) in unit_defs:
                if uid not in roster:
                    continue
                u = copy.deepcopy(roster[uid])
                u.faction = faction
                u.x = x
                u.y = y
                placed.append(u)
            return placed

        players  = place(self.player_unit_defs,  FACTION_PLAYER)
        enemies  = place(self.enemy_unit_defs,   FACTION_ENEMY)
        allies   = place(self.ally_unit_defs,    FACTION_ALLY)
        return gmap, players, enemies, allies


def _r():
    """Fresh roster for each chapter build."""
    return create_unit_roster()


# ─── Chapter Definitions ──────────────────────────────────────────────────────

CHAPTERS = [
    Chapter(
        number=1,
        title="Chapter 1",
        subtitle="Departure from Owari",
        narrative_intro=(
            "Year 1560. The Imagawa clan marches 25,000 strong toward Kyoto,\n"
            "threatening to crush the young Oda clan in their path.\n"
            "Nobunaga refuses to wait — with barely 2,000 men, he charges\n"
            "into the storm. The age of the warring states has begun.\n\n"
            "Objective: Seize the enemy stronghold."
        ),
        narrative_victory=(
            "The Imagawa vanguard crumbles before Nobunaga's ferocity.\n"
            "Word spreads through all the provinces: Oda Nobunaga cannot be stopped.\n"
            "The road to unification has opened."
        ),
        narrative_defeat=(
            "The outnumbered Oda forces were overwhelmed.\n"
            "Nobunaga's ambition ends here, on the fields of Owari.\n"
            "History will not remember him."
        ),
        objective=OBJ_SEIZE,
        objective_detail="Seize the castle at the east (14, 7) with Nobunaga.",
        player_units=[
            ("nobunaga",    1, 8),
            ("hideyoshi",   1, 7),
            ("ranmaru",     0, 6),
            ("ashigaru_e1", 2, 9),
            ("ashigaru_e2", 0, 9),
            ("archer_p1",   1, 9),
        ],
        enemy_units=[
            ("enemy_ash1",  12, 2),
            ("enemy_ash2",  13, 4),
            ("enemy_ash3",  12, 5),
            ("enemy_cav1",  11, 3),
            ("enemy_arch1", 14, 5),
            ("kansuke",     13, 6),   # boss
        ],
        ally_units=[],
        map_builder=MAP_BUILDERS[1],
    ),

    Chapter(
        number=2,
        title="Chapter 2",
        subtitle="The Storm of Okehazama",
        narrative_intro=(
            "Imagawa Yoshimoto rests his vast army in the forest gully of Okehazama.\n"
            "A sudden summer storm darkens the sky — thunder, rain, lightning.\n"
            "Nobunaga sees his chance. Through the blinding tempest, a small\n"
            "strike force charges into the heart of the enemy camp.\n\n"
            "Objective: Defeat the enemy commander to rout the army."
        ),
        narrative_victory=(
            "Imagawa Yoshimoto falls in the chaos of the storm.\n"
            "His great army dissolves like mist. The miracle of Okehazama\n"
            "will be spoken of for generations."
        ),
        narrative_defeat=(
            "The ambush was repelled. Imagawa's forces regroup and\n"
            "crush the Oda. The dream of unification dies in the rain."
        ),
        objective=OBJ_DEFEAT_BOSS,
        objective_detail="Defeat the enemy commander in the forest.",
        player_units=[
            ("nobunaga",    1, 10),
            ("mitsuhide",   2, 10),
            ("hideyoshi",   1, 9),
            ("ranmaru",     0, 9),
            ("nene",        3, 10),
            ("archer_p1",   2, 9),
        ],
        enemy_units=[
            ("enemy_ash1",   5, 6),
            ("enemy_ash2",   7, 5),
            ("enemy_ash3",   3, 5),
            ("enemy_ninja1", 8, 3),
            ("enemy_arch1",  4, 4),
            ("enemy_cav1",   9, 6),
            ("monk_p1",      10, 4),
            ("shingen",      6, 4),   # boss (using Shingen as stand-in for Yoshimoto)
        ],
        ally_units=[],
        map_builder=MAP_BUILDERS[2],
    ),

    Chapter(
        number=3,
        title="Chapter 3",
        subtitle="Kawanakajima — Dragon Meets Tiger",
        narrative_intro=(
            "1561. On the plain of Kawanakajima, the two greatest generals\n"
            "of the age meet for the fourth time: Takeda Shingen, the Tiger of Kai,\n"
            "and Uesugi Kenshin, the Dragon of Echigo.\n"
            "The Oda must choose a side — or exploit the chaos.\n\n"
            "Objective: Rout all enemy forces."
        ),
        narrative_victory=(
            "The field is yours. Both clans regroup, nursing their wounds.\n"
            "Nobunaga has turned the famous rivalry to his advantage."
        ),
        narrative_defeat=(
            "Caught between the Dragon and the Tiger,\n"
            "the Oda forces are destroyed."
        ),
        objective=OBJ_ROUT_ENEMY,
        objective_detail="Defeat all enemy units.",
        player_units=[
            ("nobunaga",    1, 5),
            ("hideyoshi",   0, 5),
            ("katsuie",     1, 6),
            ("nagahide",    0, 6),
            ("mitsuhide",   2, 5),
            ("healer_p1",   1, 7),
            ("archer_p1",   2, 6),
            ("ashigaru_e1", 0, 7),
            ("ieyasu_ally", 2, 7),  # ally on player's side
        ],
        enemy_units=[
            # Uesugi forces (north side)
            ("kenshin",        2, 0),
            ("kanetsugu",      3, 1),
            ("kagetsora",      4, 1),
            ("enemy_samurai1", 1, 1),
            ("enemy_samurai2", 5, 1),
            # Takeda forces (south side)
            ("shingen",        13, 11),
            ("kansuke",        12, 10),
            ("masakage",       14, 10),
            ("enemy_cav1",     13, 10),
            ("enemy_ash1",     12, 11),
            ("enemy_ash2",     14, 11),
        ],
        ally_units=[],
        map_builder=MAP_BUILDERS[3],
    ),

    Chapter(
        number=4,
        title="Chapter 4",
        subtitle="The Flames of Honnoji",
        narrative_intro=(
            "Year 1582. Akechi Mitsuhide, trusted general of Nobunaga,\n"
            "has turned his 13,000 soldiers against his lord.\n"
            "As dawn breaks, Honnoji temple is surrounded.\n"
            "Nobunaga, with only a handful of pages, prepares his last stand.\n\n"
            "Survive and reach the inner sanctum. The truth of betrayal awaits."
        ),
        narrative_victory=(
            "Against all odds, Nobunaga escapes the ring of fire.\n"
            "The traitor Mitsuhide has failed. But this is not over —\n"
            "Hideyoshi is already marching to answer the crime."
        ),
        narrative_defeat=(
            "The flames of Honnoji consume everything.\n"
            "Nobunaga performs his final act. The age of Oda ends here.\n"
            "'The life of man is fifty years...'"
        ),
        objective=OBJ_SEIZE,
        objective_detail="Reach the inner sanctum (7, 6) with Nobunaga to survive.",
        player_units=[
            ("nobunaga",    7,  11),
            ("ranmaru",     6,  11),
            ("nagahide",    8,  11),
            ("ashigaru_e1", 6,  10),
            ("ashigaru_e2", 8,  10),
            ("healer_p1",   7,  10),
        ],
        enemy_units=[
            # Akechi forces — the betrayers
            ("mitsuhide",       7,  0),   # boss (Mitsuhide as enemy this chapter)
            ("enemy_samurai1",  5,  2),
            ("enemy_samurai2",  9,  2),
            ("enemy_spear1",    4,  4),
            ("enemy_spear2",   10,  4),
            ("enemy_ninja1",    6,  5),
            ("enemy_ash1",      3,  6),
            ("enemy_ash2",     11,  6),
            ("enemy_arch1",     5,  8),
            ("enemy_cav1",      9,  8),
            ("enemy_ash3",      4,  9),
            ("enemy_date_cav1",10,  9),
        ],
        ally_units=[],
        map_builder=MAP_BUILDERS[4],
    ),

    Chapter(
        number=5,
        title="Chapter 5",
        subtitle="Sekigahara — The Final Reckoning",
        narrative_intro=(
            "Year 1600. The land trembles beneath the weight of two great\n"
            "coalitions. Toyotomi loyalists under Ishida Mitsunari face\n"
            "Tokugawa Ieyasu's eastern army. The fate of Japan hangs\n"
            "on this single day, this single field.\n\n"
            "Seize the center of the battlefield to claim victory."
        ),
        narrative_victory=(
            "The Tokugawa banner rises over Sekigahara.\n"
            "The age of warring states draws to a close.\n"
            "Two hundred and fifty years of peace — the Pax Tokugawa — begins.\n\n"
            "But the price was paid in blood."
        ),
        narrative_defeat=(
            "The eastern army falters. Ieyasu's dream dies here.\n"
            "The warring states continue without end..."
        ),
        objective=OBJ_SEIZE,
        objective_detail="Seize the center of Sekigahara (9, 6) to end the battle.",
        player_units=[
            ("hideyoshi",    1, 13),   # standing in as eastern commander
            ("katsuie",      0, 12),
            ("nagahide",     2, 12),
            ("nene",         1, 12),
            ("archer_p1",    3, 13),
            ("ashigaru_e1",  0, 13),
            ("ashigaru_e2",  2, 13),
            ("healer_p1",    1, 11),
            ("ieyasu_ally",  3, 12),
        ],
        enemy_units=[
            # Western coalition
            ("yoshihisa",       9,  1),   # boss
            ("yoshihiro",       8,  2),
            ("shimazu_ash1",    7,  2),
            ("shimazu_ash2",   10,  2),
            ("shimazu_archer1", 9,  3),
            ("masamune",       16,  7),   # Date clan flanking
            ("shigezane",      15,  7),
            ("enemy_date_cav1",16,  8),
            ("enemy_spear1",   15,  8),
            ("kenshin",         9,  0),   # Uesugi on western side
            ("enemy_samurai1",  8,  1),
            ("enemy_samurai2", 10,  1),
            ("enemy_arch1",     7,  3),
        ],
        ally_units=[],
        map_builder=MAP_BUILDERS[5],
    ),
]
