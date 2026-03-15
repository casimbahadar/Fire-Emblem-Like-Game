"""
Chapter definitions for Sengoku Tactics: Age of the Warring States
20 chapters with Samurai Warriors-inspired narratives, reinforcements, recruits.
"""
import copy
from game.constants import *
from game.unit import create_unit_roster
from game.map import MAP_BUILDERS


class ReinforcementWave:
    def __init__(self, turn, faction, unit_defs, message="Reinforcements arrive!",
                 edge="south"):
        self.turn     = turn
        self.faction  = faction
        self.unit_defs= unit_defs    # list of (unit_id, x, y)
        self.message  = message
        self.edge     = edge
        self.triggered= False


class Chapter:
    def __init__(self, number, title, subtitle,
                 narrative_intro, narrative_victory, narrative_defeat,
                 objective, objective_detail,
                 player_units, enemy_units, ally_units,
                 map_builder, turn_limit=None,
                 reinforcements=None, seize_unit="nobunaga"):
        self.number   = number
        self.title    = title
        self.subtitle = subtitle
        self.narrative_intro   = narrative_intro
        self.narrative_victory = narrative_victory
        self.narrative_defeat  = narrative_defeat
        self.objective         = objective
        self.objective_detail  = objective_detail
        self.player_unit_defs  = player_units
        self.enemy_unit_defs   = enemy_units
        self.ally_unit_defs    = ally_units
        self.map_builder       = map_builder
        self.turn_limit        = turn_limit
        self.reinforcements    = reinforcements or []
        self.seize_unit        = seize_unit   # which lord seizes

    def build(self, roster):
        """Instantiate chapter. Returns (game_map, player_units, enemy_units, ally_units, reinf_waves)."""
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

        players = place(self.player_unit_defs, FACTION_PLAYER)
        enemies = place(self.enemy_unit_defs,  FACTION_ENEMY)
        allies  = place(self.ally_unit_defs,   FACTION_ALLY)

        # Deep copy reinforcements so .triggered flag is fresh each play
        waves = []
        for wave in self.reinforcements:
            w = ReinforcementWave(
                turn=wave.turn,
                faction=wave.faction,
                unit_defs=wave.unit_defs,
                message=wave.message,
                edge=wave.edge
            )
            waves.append(w)

        return gmap, players, enemies, allies, waves


# ─── Chapter Definitions ──────────────────────────────────────────────────────

CHAPTERS = [

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=1, title="Chapter 1",
        subtitle="Departure from Owari",
        narrative_intro=(
            "Year 1560. The Imagawa clan marches 25,000 strong toward Kyoto.\n"
            "In their path: the tiny Oda domain and its reckless young lord.\n"
            "Where other men cower, Nobunaga dances and shouts war songs.\n\n"
            "NOBUNAGA: 'Human life is fifty years! Compared to the universe —\n"
            "it is nothing but a dream!' CHARGE!"
        ),
        narrative_victory=(
            "The Imagawa vanguard crumbles. Nobunaga laughs on the battlefield\n"
            "while Hideyoshi argues with Ranmaru about who landed the best blow.\n"
            "The age of Oda Nobunaga has begun."
        ),
        narrative_defeat=(
            "Overwhelmed on the Owari plains. Nobunaga dies with a war song\n"
            "on his lips. History will not remember this name."
        ),
        objective=OBJ_SEIZE, objective_detail="Seize the castle (14,7) with Nobunaga.",
        player_units=[
            ("nobunaga", 1,8), ("hideyoshi",1,7), ("ranmaru",0,6),
            ("oda_ash1", 2,9), ("oda_ash2", 0,9), ("oda_arch1",1,9),
        ],
        enemy_units=[
            ("e_ash1",12,2), ("e_ash2",13,4), ("e_ash3",12,5),
            ("e_cav1",11,3), ("e_arch1",14,5), ("kansuke",13,6),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[1],
        reinforcements=[
            ReinforcementWave(4, FACTION_ENEMY,
                [("e_ash4",14,9),("e_sam1",13,9)],
                "Enemy reinforcements arrive from the south!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=2, title="Chapter 2",
        subtitle="Storm of Okehazama",
        narrative_intro=(
            "Imagawa Yoshimoto rests in the forest gully, supremely confident.\n"
            "A summer storm blackens the sky. Lightning. Thunder. Rain.\n\n"
            "NOBUNAGA: 'The heavens are with us! TO OKEHAZAMA!'\n"
            "HIDEYOSHI: 'Wait — how many of them are there again?'\n"
            "NOBUNAGA: 'It doesn't matter. We move NOW!'"
        ),
        narrative_victory=(
            "Yoshimoto's head rolls in the mud. His 25,000 dissolve like smoke.\n"
            "The Miracle of Okehazama will be told for centuries.\n"
            "HIDEYOSHI: 'I can't believe we did that.' NOBUNAGA: 'I can.'"
        ),
        narrative_defeat=(
            "The thunder drowns out Nobunaga's final defiant shout.\n"
            "Yoshimoto orders tea. The Oda are finished."
        ),
        objective=OBJ_DEFEAT_BOSS,
        objective_detail="Defeat Imagawa Yoshimoto in the forest.",
        player_units=[
            ("nobunaga",1,10), ("mitsuhide",2,10), ("hideyoshi",1,9),
            ("ranmaru",0,9),   ("nene",3,10),      ("oda_arch1",2,9),
        ],
        enemy_units=[
            ("e_ash1",5,6), ("e_ash2",7,5), ("e_ash3",3,5),
            ("e_ninja1",8,3), ("e_arch1",4,4), ("e_cav1",9,6),
            ("e_monk1",10,4), ("yoshimoto",6,4),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[2],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_sam1",12,5),("e_cav1",11,4)],
                "Imagawa reinforcements rush to protect their lord!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=3, title="Chapter 3",
        subtitle="Kawanakajima — Dragon and Tiger",
        narrative_intro=(
            "1561. The plain of Kawanakajima. For the fourth time, the Dragon\n"
            "and Tiger clash. Kenshin descends from the north; Shingen rises\n"
            "from the south. Their battle is the storm — and the Oda stand\n"
            "at its eye.\n\n"
            "NOBUNAGA: 'Let them weaken each other. Then... we strike both!'"
        ),
        narrative_victory=(
            "Both great clans retreat, bleeding. Nobunaga controls the field.\n"
            "KENSHIN: 'This is not finished, Oda.'\n"
            "NOBUNAGA: 'No. But you are.'  [smiles]"
        ),
        narrative_defeat=(
            "Caught between Dragon and Tiger. The Oda are crushed, and two\n"
            "great enemies begin the real war."
        ),
        objective=OBJ_ROUT_ENEMY, objective_detail="Defeat all enemy units.",
        player_units=[
            ("nobunaga",1,5), ("hideyoshi",0,5), ("katsuie",1,6),
            ("nagahide",0,6), ("mitsuhide",2,5), ("oda_monk1",1,7),
            ("oda_arch1",2,6), ("oda_ash1",0,7),
        ],
        enemy_units=[
            ("kenshin",2,0), ("kanetsugu",3,1), ("kagetsora",4,1),
            ("e_sam1",1,1), ("e_sam2",5,1),
            ("shingen",13,11), ("kansuke",12,10), ("masakage",14,10),
            ("e_cav1",13,10), ("e_ash1",12,11), ("e_ash2",14,11),
        ],
        ally_units=[("ieyasu",2,7)],
        map_builder=MAP_BUILDERS[3],
        reinforcements=[
            ReinforcementWave(4, FACTION_ENEMY,
                [("nobushige",0,1),("masanobu",15,10)],
                "Both clans send fresh troops!"),
            ReinforcementWave(6, FACTION_ALLY,
                [("tadakatsu",3,7),("naomasa",4,7)],
                "Tokugawa reinforcements arrive to support!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=4, title="Chapter 4",
        subtitle="The Flames of Honnoji",
        narrative_intro=(
            "Year 1582. Honnoji Temple, Kyoto. Midnight.\n"
            "RANMARU: 'My lord! The temple is surrounded!'\n"
            "NOBUNAGA: '...Is it Mitsuhide?'\n"
            "RANMARU: 'Yes, my lord.'\n"
            "NOBUNAGA: [a long pause] 'Then there is nothing to be done.\n"
            "But I will not die easily.'"
        ),
        narrative_victory=(
            "Nobunaga escapes the ring of fire by sheer force of will.\n"
            "Ranmaru falls. The temple burns. Mitsuhide watches the smoke\n"
            "rise from a hilltop, his victory hollow.\n"
            "HIDEYOSHI receives word. He is already marching."
        ),
        narrative_defeat=(
            "The flames consume the Demon King. Nobunaga composes himself,\n"
            "dances his final verse of 'Atsumori', and performs the last\n"
            "act of a great man. The age of Oda ends at dawn."
        ),
        objective=OBJ_SEIZE,
        objective_detail="Reach the inner sanctum (7,6) with Nobunaga to survive.",
        player_units=[
            ("nobunaga",7,11), ("ranmaru",6,11), ("nagahide",8,11),
            ("oda_ash1",6,10), ("oda_ash2",8,10), ("oda_monk1",7,10),
        ],
        enemy_units=[
            ("mitsuhide",7,0), ("e_sam1",5,2), ("e_sam2",9,2),
            ("e_spear1",4,4), ("e_spear2",10,4), ("e_ninja1",6,5),
            ("e_ash1",3,6), ("e_ash2",11,6), ("e_arch1",5,8),
            ("e_cav1",9,8), ("e_ash3",4,9), ("e_hat1",10,9),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[4],
        reinforcements=[
            ReinforcementWave(2, FACTION_ENEMY,
                [("e_ron1",2,4),("e_ron2",12,4)],
                "Mitsuhide sends elite ronin to finish the job!"),
            ReinforcementWave(4, FACTION_ENEMY,
                [("e_ninja2",4,8),("e_ninja2",10,8)],
                "Shadow assassins close in from all directions!"),
        ],
        seize_unit="nobunaga"
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=5, title="Chapter 5",
        subtitle="Sekigahara — The First Reckoning",
        narrative_intro=(
            "Year 1600. The western coalition faces the Tokugawa east.\n"
            "Hideyoshi's dream hangs in the balance.\n\n"
            "HIDEYOSHI: 'If this is the last battle, let it be worthy\n"
            "of the age we built!'\n"
            "IEYASU: 'It won't be the last. But it will end the era.'"
        ),
        narrative_victory=(
            "The Tokugawa banner rises over Sekigahara. The age of warring\n"
            "states draws to its first close. Two hundred and fifty years\n"
            "of Tokugawa peace... at the cost of a field of blood."
        ),
        narrative_defeat=(
            "The eastern army breaks. Ieyasu flees. The war continues —\n"
            "without end, without resolution."
        ),
        objective=OBJ_SEIZE,
        objective_detail="Seize the center of Sekigahara (9,6) with any lord unit.",
        player_units=[
            ("hideyoshi",1,13), ("katsuie",0,12), ("nagahide",2,12),
            ("nene",1,12), ("oda_arch1",3,13), ("oda_ash1",0,13),
            ("oda_ash2",2,13), ("oda_monk1",1,11), ("ieyasu",3,12),
        ],
        enemy_units=[
            ("yoshihisa",9,1), ("yoshihiro",8,2),
            ("shimazu_ash1",7,2), ("shimazu_ash2",10,2),
            ("shimazu_archer",9,3),
            ("masamune",16,7), ("shigezane",15,7),
            ("e_cav1",16,8), ("e_spear1",15,8),
            ("kenshin",9,0), ("e_sam1",8,1), ("e_sam2",10,1),
            ("e_arch1",7,3),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[5],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("otani",5,2),("mitsunari",4,1)],
                "The western leaders ride out personally!"),
            ReinforcementWave(5, FACTION_ALLY,
                [("tadakatsu",3,11),("naomasa",2,11),("hanzo",4,11)],
                "The Tokugawa vanguard arrives at last!"),
        ],
        seize_unit="hideyoshi"
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=6, title="Chapter 6",
        subtitle="Siege of Inabayama",
        narrative_intro=(
            "The Saito castle of Inabayama crowns a steep mountain.\n"
            "Nobunaga's father-in-law Saito Dosan once held it — his\n"
            "worthless son Tatsuoki drove his own generals away.\n\n"
            "HIDEYOSHI: 'Lord Nobunaga, I found a way up through the mountain\n"
            "behind the castle. A secret path!'\n"
            "NOBUNAGA: '...How did you find that?'\n"
            "HIDEYOSHI: [huge grin] 'It's what I do, my lord.'"
        ),
        narrative_victory=(
            "Inabayama falls. Nobunaga renames it Gifu — 'Province of Zhou,'\n"
            "after the ancient kingdom whose lord unified China.\n"
            "The message is clear. ALL of Japan will follow."
        ),
        narrative_defeat=(
            "The mountain path was a trap. Tatsuoki's remaining generals\n"
            "hold the heights and the Oda forces are repulsed."
        ),
        objective=OBJ_SEIZE,
        objective_detail="Seize Inabayama Castle at the mountain peak (6-7, 0).",
        player_units=[
            ("nobunaga",6,12), ("hideyoshi",7,12), ("katsuie",5,12),
            ("mitsuhide",8,12), ("oda_ash1",6,11), ("oda_ash2",7,11),
            ("oda_spear1",5,11), ("oda_arch1",8,11),
        ],
        enemy_units=[
            ("tatsuoki",6,0), ("e_sam1",5,2), ("e_sam2",8,2),
            ("e_ash1",5,4), ("e_ash2",8,4), ("e_arch1",4,5),
            ("e_arch2",9,5), ("e_spear1",6,6), ("e_gen1",7,6),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[6],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_sam2",4,2),("e_ash3",9,3)],
                "Saito reinforcements rush to defend the mountain passes!"),
            ReinforcementWave(5, FACTION_ENEMY,
                [("e_ron1",3,4),("e_ninja1",10,5)],
                "Saito retainers emerge from hidden mountain paths!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=7, title="Chapter 7",
        subtitle="The Betrayal at Anegawa",
        narrative_intro=(
            "Azai Nagamasa — Nobunaga's own brother-in-law — has broken\n"
            "alliance to honor an oath to the Asakura. His wife Oichi\n"
            "sent a silent warning: a bag of beans, tied at both ends.\n"
            "Surrounded on both sides.\n\n"
            "OICHI: 'Brother... forgive me.'\n"
            "NOBUNAGA: 'There is nothing to forgive. This is war.'"
        ),
        narrative_victory=(
            "The Azai-Asakura coalition breaks at the riverbank.\n"
            "Nagamasa retreats to Odani Castle. Oichi weeps.\n"
            "Nobunaga rides past the dead in silence."
        ),
        narrative_defeat=(
            "Caught in the double pincer, the Oda forces are crushed\n"
            "between two rivers and two armies. The alliance fails."
        ),
        objective=OBJ_ROUT_ENEMY,
        objective_detail="Defeat all enemy forces. Recruit Azai Nagamasa with Oichi.",
        player_units=[
            ("nobunaga",2,5), ("hideyoshi",1,5), ("katsuie",3,5),
            ("oichi",2,6), ("toshiie",1,6), ("oda_cav1",0,5),
            ("oda_arch1",3,6), ("oda_ash1",0,6), ("ieyasu",1,7),
        ],
        enemy_units=[
            ("nagamasa",4,2), ("e_sam1",3,1), ("e_sam2",5,1),
            ("e_ash1",2,2), ("e_cav1",6,2),
            ("yoshikage",13,9), ("e_sam3",12,10), ("e_ash2",14,9),
            ("e_ash3",13,10), ("e_spear1",12,9), ("e_arch1",14,10),
        ],
        ally_units=[("tadakatsu",2,7),("naomasa",3,7)],
        map_builder=MAP_BUILDERS[7],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_cav2",2,0),("e_spear2",15,11)],
                "Both clans send in their elite cavalry reserves!"),
            ReinforcementWave(5, FACTION_ENEMY,
                [("e_hat1",4,0),("e_hat1",13,11)],
                "Hatamoto units join the battle on both flanks!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=8, title="Chapter 8",
        subtitle="The Ikko-Ikki at Nagashima",
        narrative_intro=(
            "The Ikko-Ikki — warrior monks of the True Pure Land sect —\n"
            "hold a network of island fortresses in the Nagashima delta.\n"
            "Three times Nobunaga has tried to destroy them. Three times\n"
            "they have repelled him.\n\n"
            "NOBUNAGA: 'This time, we bring FIRE.'\n"
            "KANBEI: [appearing from nowhere] 'A tactician's greeting:\n"
            "I offer my service, Lord Nobunaga. I believe I can help.'"
        ),
        narrative_victory=(
            "The Nagashima fortress complex falls. The Ikko-Ikki are\n"
            "shattered at last. Kanbei's strategic brilliance proved\n"
            "decisive — and he is now firmly Nobunaga's mastermind.\n"
            "Also: Sanada Yukimura was found wandering these islands.\n"
            "He seems... interested in joining."
        ),
        narrative_defeat=(
            "The island network holds. The Ikko-Ikki drive off the Oda\n"
            "for the fourth time. Their bells ring in triumph."
        ),
        objective=OBJ_ROUT_ENEMY,
        objective_detail="Clear the island fortress. Recruit Kanbei by reaching him.",
        player_units=[
            ("nobunaga",7,12), ("hideyoshi",6,12), ("katsuie",8,12),
            ("nagahide",5,12), ("nene",9,12), ("oda_ash1",6,11),
            ("oda_ash2",8,11), ("oda_arch1",7,11), ("oda_gun1",5,11),
        ],
        enemy_units=[
            ("e_ikko1",6,6), ("e_ikko2",7,5), ("e_ikko1",8,6),
            ("e_ikko2",5,5), ("e_monk1",6,4), ("e_monk2",8,4),
            ("e_ash1",4,5), ("e_ash2",10,5),
            ("e_sam1",6,3), ("e_sam2",8,3),
            ("yukimura",2,6),   # recruitable!
            ("kanbei",12,6),    # appears as neutral-enemy, recruitable
        ],
        ally_units=[], map_builder=MAP_BUILDERS[8],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_ikko1",4,7),("e_ikko2",10,7),("e_monk1",7,9)],
                "Ikko-Ikki warrior monks surge from the inner temple!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=9, title="Chapter 9",
        subtitle="Relief of Nagashino Castle",
        narrative_intro=(
            "The Takeda cavalry besieges Nagashino Castle, pinning a small\n"
            "garrison inside. A brave samurai named Torii Suneemon swam the\n"
            "river to call for help — and was crucified when caught.\n\n"
            "KANBEI: 'The castle must hold three more days. Nagashino is\n"
            "the key to everything.'\n"
            "NOBUNAGA: 'Then we make it hold.'"
        ),
        narrative_victory=(
            "The castle holds. Oda reinforcements pour through the breach.\n"
            "The Takeda cavalry is denied its charge. The stage is set\n"
            "for the battle that will change war in Japan forever."
        ),
        narrative_defeat=(
            "Nagashino falls. The Takeda now have an open road westward.\n"
            "Kanbei's strategy collapses without this fortress anchor."
        ),
        objective=OBJ_DEFEND,
        objective_detail="Hold Nagashino Castle for 8 turns.",
        player_units=[
            ("nobunaga",6,8), ("hideyoshi",7,8), ("kanbei",5,8),
            ("katsuie",8,8), ("oda_gun1",6,7), ("oda_gun2",8,7),
            ("oda_arch1",5,7), ("oda_arch2",9,7), ("oda_ash1",6,9),
        ],
        enemy_units=[
            ("shingen",9,1), ("masakage",8,1), ("masanobu",10,1),
            ("e_cav1",7,2), ("e_cav2",11,2), ("e_ash1",6,2),
            ("e_ash2",12,2), ("e_arch1",7,3), ("e_arch2",11,3),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[9],
        turn_limit=None,  # Players must survive 8 turns (checked in state)
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("nobushige",5,0),("e_cav1",13,2)],
                "Takeda second wave — the cavalry of Kai charges again!"),
            ReinforcementWave(5, FACTION_ENEMY,
                [("kansuke",8,0),("e_sam1",6,1),("e_sam2",10,1)],
                "Yamamoto Kansuke leads the elite troops personally!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=10, title="Chapter 10",
        subtitle="Nagashino — The Volley Line",
        narrative_intro=(
            "NOBUNAGA smiles at the long wooden palisade stretching across\n"
            "the plain. Three thousand matchlock riflemen stand in rotating\n"
            "lines, ready to fire in volleys — never stopping.\n\n"
            "KATSUIE: 'This is cowardly! Fighting with guns!'\n"
            "KANBEI: 'This is the future.'\n"
            "MASAKAGE [Takeda cavalry]: 'TAKEDA CHARGES! NOTHING STOPS US!'\n"
            "KANBEI: '...We'll see.'"
        ),
        narrative_victory=(
            "The Takeda cavalry charge breaks against the volley fire.\n"
            "Masakage falls. Shingen's famous cavalry — the greatest in Japan\n"
            "— is shattered in an afternoon.\n"
            "MAGOICHI: 'Told you guns were the future.'\n"
            "He joins the Oda. He has found his interesting employer."
        ),
        narrative_defeat=(
            "The palisade is overrun. Takeda cavalry crashes through.\n"
            "The volley line breaks. Nobunaga's gamble fails."
        ),
        objective=OBJ_DEFEAT_BOSS,
        objective_detail="Defeat Takeda Shingen. Saika Magoichi may be recruited.",
        player_units=[
            ("nobunaga",10,5), ("kanbei",9,5), ("katsuie",11,5),
            ("toshiie",12,5), ("oda_gun1",8,5), ("oda_gun2",12,5),
            ("oda_gun1",10,5), ("oda_arch1",9,6), ("oda_arch2",11,6),
            ("oda_ash1",8,6),  ("oda_ash2",12,6),
        ],
        enemy_units=[
            ("shingen",10,12), ("masakage",8,11), ("masanobu",12,11),
            ("kansuke",9,12), ("e_cav1",7,11), ("e_cav2",11,11),
            ("e_cav1",6,10), ("e_cav2",13,10), ("e_ash1",9,10),
            ("e_ash2",11,10), ("magoichi",3,10),  # recruitable!
        ],
        ally_units=[("ieyasu",10,6),("tadakatsu",9,6),("naomasa",11,6)],
        map_builder=MAP_BUILDERS[10],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("nobushige",5,12),("e_hat1",14,10)],
                "Takeda elite units commit to the charge — hold the palisade!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=11, title="Chapter 11",
        subtitle="Conquest of the West — Mori Campaign",
        narrative_intro=(
            "Hideyoshi has been given the western campaign against the\n"
            "mighty Mori clan — lords of eight provinces. The Fox of Chugoku\n"
            "Mori Motonari has been dead two years, but his grandson\n"
            "Terumoto holds on with diplomatic brilliance.\n\n"
            "HIDEYOSHI: 'I'll win this with kindness and patience!'\n"
            "KATSUIE: '...Please just win it.'"
        ),
        narrative_victory=(
            "The Mori's western fortresses fall one by one.\n"
            "Chosokabe Motochika, Lord of Shikoku, emerges from the\n"
            "coastal fog. He switches sides — he smells a winner.\n"
            "MOTOCHIKA: 'The sea laughs at walls. I laugh at walls.\n"
            "We shall get along.'"
        ),
        narrative_defeat=(
            "The Mori western network holds. Hideyoshi is repulsed\n"
            "from Chugoku. The Mori domain stands."
        ),
        objective=OBJ_SEIZE,
        objective_detail="Seize Mori's western fortress (6-8, 12). Recruit Motochika.",
        player_units=[
            ("hideyoshi",7,13), ("kanbei",6,13), ("kiyomasa",8,13),
            ("fukushima",5,13), ("nene",9,13), ("oda_ash1",6,12),
            ("oda_ash2",8,12), ("oda_cav1",5,12), ("oda_arch1",9,12),
            ("oda_gun1",7,12),
        ],
        enemy_units=[
            ("motonari",7,0), ("terumoto",8,1), ("ekei",6,1),
            ("e_sam1",5,2), ("e_sam2",9,2), ("e_ash1",4,3),
            ("e_ash2",10,3), ("e_arch1",5,5), ("e_arch2",9,5),
            ("e_spear1",6,4), ("e_spear2",8,4),
            ("motochika",3,13),  # recruitable!
        ],
        ally_units=[], map_builder=MAP_BUILDERS[11],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_pirate1",1,4),("e_pirate2",2,5)],
                "Mori naval pirates attack from the coast!"),
            ReinforcementWave(5, FACTION_ENEMY,
                [("e_gen1",7,2),("e_hat1",6,2)],
                "Mori elite guards defend the fortress gates!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=12, title="Chapter 12",
        subtitle="The Flooded Castle — Takamatsu",
        narrative_intro=(
            "Shimizu Muneharu holds Takamatsu Castle for the Mori.\n"
            "Kanbei's solution: dam the river and flood the castle.\n"
            "Slowly, the water rises around the walls.\n\n"
            "KANBEI: 'A siege won by water. Not a drop of blood spilled.'\n"
            "KATSUIE: '...That is disgusting.'\n"
            "KANBEI: 'That is strategy.'"
        ),
        narrative_victory=(
            "Takamatsu Castle surrenders. But a messenger arrives:\n"
            "HONNOJI. Nobunaga is dead. Mitsuhide has struck.\n"
            "HIDEYOSHI: 'Pack everything. We march now. DOUBLE TIME!'\n"
            "KANBEI: [quietly] 'And suddenly the whole world is open.'"
        ),
        narrative_defeat=(
            "The castle holds. The Mori fleet breaks the dam.\n"
            "And in the chaos, the news from Honnoji is lost."
        ),
        objective=OBJ_SEIZE,
        objective_detail="Seize the inner keep (6-7, 6) of Takamatsu Castle.",
        player_units=[
            ("hideyoshi",7,11), ("kanbei",6,11), ("kiyomasa",8,11),
            ("fukushima",5,11), ("motochika",4,11), ("oda_ash1",6,10),
            ("oda_arch1",8,10), ("oda_gun1",7,10), ("oda_gun2",5,10),
            ("tsuruhime",9,11),
        ],
        enemy_units=[
            ("e_gen1",7,6), ("e_sam1",5,6), ("e_sam2",9,6),
            ("e_ash1",6,5), ("e_ash2",8,5), ("e_spear1",6,7),
            ("e_spear2",8,7), ("e_arch1",5,8), ("e_arch2",9,8),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[12],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_pirate1",2,10),("e_pirate2",13,10)],
                "Mori naval reinforcements arrive by water!"),
            ReinforcementWave(5, FACTION_ENEMY,
                [("ekei",7,4),("e_monk2",6,4),("e_monk2",8,4)],
                "The Mori send warrior monks to the inner keep!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=13, title="Chapter 13",
        subtitle="Yamazaki — The Monkey's Revenge",
        narrative_intro=(
            "Thirteen days after Honnoji. Hideyoshi's army has covered\n"
            "200 miles in twelve days — the fastest march in Japanese history.\n\n"
            "MITSUHIDE: 'Impossible. He cannot be here yet.'\n"
            "HIDEYOSHI: [arriving on the horizon with his entire army]\n"
            "MITSUHIDE: '...Oh.'"
        ),
        narrative_victory=(
            "Mitsuhide falls at Yamazaki. His 'Three Days' as lord of Japan\n"
            "end in humiliation. They say a bandit ended him in a bamboo grove.\n"
            "HIDEYOSHI: 'The avenger of Honnoji. That is what history will say.'\n"
            "KANBEI: [quieter] 'Is that all you want history to say?'"
        ),
        narrative_defeat=(
            "The speed wasn't enough. Mitsuhide holds Yamazaki and\n"
            "secures his position. The Oda retainers splinter."
        ),
        objective=OBJ_DEFEAT_BOSS,
        objective_detail="Defeat Akechi Mitsuhide at Yamazaki.",
        player_units=[
            ("hideyoshi",9,12), ("kanbei",8,12), ("kiyomasa",10,12),
            ("fukushima",7,12), ("toshiie",11,12), ("nene",9,11),
            ("oda_cav1",8,11), ("oda_cav1",10,11), ("oda_arch1",7,11),
            ("oda_gun1",11,11), ("motochika",6,12),
        ],
        enemy_units=[
            ("mitsuhide",9,0), ("e_sam1",7,1), ("e_sam2",11,1),
            ("e_ash1",6,2), ("e_ash2",12,2), ("e_spear1",8,2),
            ("e_spear2",10,2), ("e_arch1",7,4), ("e_arch2",11,4),
            ("e_cav1",8,5), ("e_cav2",10,5), ("e_ron1",5,3),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[13],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_hat1",6,0),("e_hat1",12,0)],
                "Mitsuhide's elite hatamoto form a last defensive line!"),
            ReinforcementWave(4, FACTION_ALLY,
                [("nobunaga",9,12),("ranmaru",8,12)],   # Ghost of Nobunaga?? No — survivors!
                "Additional Oda loyalists join Hideyoshi's pursuit!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=14, title="Chapter 14",
        subtitle="The Battle of Shizugatake",
        narrative_intro=(
            "After Yamazaki, the Oda clan's succession war heats up.\n"
            "Shibata Katsuie supports a rival heir — and now his army\n"
            "faces Hideyoshi on the slopes of Shizugatake.\n\n"
            "KATSUIE [enemy this chapter]: 'I served Lord Nobunaga all my life.\n"
            "Who is this monkey to lead in his place?!'\n"
            "HIDEYOSHI: 'A monkey who wins.'"
        ),
        narrative_victory=(
            "Katsuie retreats to Kitanosho Castle. The succession is\n"
            "settled in Hideyoshi's favor. The Seven Spears of Shizugatake —\n"
            "Kiyomasa, Fukushima, and five others — are born as heroes.\n"
            "KATSUIE: 'I would rather die in the castle than bend to Hideyoshi.'"
        ),
        narrative_defeat=(
            "Katsuie's mountain fortress holds. Hideyoshi's ambitions stall.\n"
            "The Oda succession remains contested."
        ),
        objective=OBJ_DEFEAT_BOSS,
        objective_detail="Defeat Shibata Katsuie on the mountain.",
        player_units=[
            ("hideyoshi",8,13), ("kanbei",7,13), ("kiyomasa",9,13),
            ("fukushima",6,13), ("toshiie",10,13), ("nene",8,12),
            ("oda_cav1",7,12), ("oda_arch1",9,12), ("oda_gun1",6,12),
            ("oda_gun2",10,12), ("motochika",5,13),
        ],
        enemy_units=[
            # Katsuie is ENEMY this chapter — internal conflict
            ("katsuie",6,0), ("e_gen1",5,1), ("e_gen1",7,1),
            ("e_sam1",4,2), ("e_sam2",8,2), ("e_hat1",5,2),
            ("e_ash1",4,4), ("e_ash2",8,4), ("e_spear1",6,4),
            ("e_arch1",4,6), ("e_arch2",8,6), ("e_cav1",6,7),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[14],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_hat1",3,3),("e_hat1",9,3)],
                "Katsuie's veteran hatamoto descend from the peak!"),
            ReinforcementWave(5, FACTION_ALLY,
                [("ieyasu",8,13),("naomasa",7,13)],
                "Tokugawa forces arrive to support Hideyoshi's flank!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=15, title="Chapter 15",
        subtitle="Komaki-Nagakute — War of Patience",
        narrative_intro=(
            "Tokugawa Ieyasu resists Hideyoshi's authority.\n"
            "The two great survivors of the age face off on the plains\n"
            "of Komaki. Neither will fully commit to battle.\n\n"
            "KANBEI: 'This is a chess match, not a battle.'\n"
            "IEYASU [across the field]: 'He is right. Let us play carefully.'\n"
            "Both sides wait. And wait. Then Hideyoshi moves."
        ),
        narrative_victory=(
            "The campaign resolves not by decisive battle but by negotiation.\n"
            "Hideyoshi sends Ieyasu his own mother as a hostage — and receives\n"
            "Ieyasu's submission in return. Genius — or madness?\n"
            "IEYASU: 'I will bend this time. But I am watching. Always watching.'"
        ),
        narrative_defeat=(
            "The battle of patience is lost. Hideyoshi over-extends\n"
            "and Tokugawa strikes the exposed flank decisively."
        ),
        objective=OBJ_SEIZE,
        objective_detail="Seize the central position (10,6) and hold.",
        player_units=[
            ("hideyoshi",5,12), ("kanbei",4,12), ("kiyomasa",6,12),
            ("fukushima",3,12), ("toshiie",7,12), ("nene",5,11),
            ("oda_cav1",4,11), ("oda_arch1",6,11), ("oda_gun1",3,11),
            ("oda_gun2",7,11), ("magoichi",8,12),
        ],
        enemy_units=[
            ("ieyasu",14,0), ("tadakatsu",13,0), ("naomasa",15,0),
            ("hanzo",12,1), ("e_cav1",13,2), ("e_cav2",15,2),
            ("e_ash1",12,3), ("e_ash2",16,3), ("e_arch1",13,4),
            ("e_gen1",14,2),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[15],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_hat1",13,1),("e_hat1",15,1),("naomasa",14,0)],
                "Tokugawa sends their elite hatamoto forward!"),
            ReinforcementWave(5, FACTION_ALLY,
                [("motochika",4,12),("tsuruhime",8,12)],
                "Shikoku allies arrive to bolster the Toyotomi line!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=16, title="Chapter 16",
        subtitle="The Fall of Odawara",
        narrative_intro=(
            "The Hojo clan — masters of the impregnable Odawara Castle —\n"
            "have never been taken by siege. Hideyoshi brings 200,000 men.\n"
            "He builds a SECOND TOWN outside the walls for the army to\n"
            "live in comfortably. Then he waits. The Hojo watch in horror.\n\n"
            "UJIYASU: 'What manner of war is this?!'\n"
            "FUMA KOTARO: '...This one is over, my lord.'"
        ),
        narrative_victory=(
            "Odawara Castle surrenders. The Hojo domain ends.\n"
            "Fuma Kotaro — the shadow himself — steps from the darkness\n"
            "and bows to the Oda standard. Even the demon serves the winner.\n"
            "Japan. Is. Unified."
        ),
        narrative_defeat=(
            "Odawara holds. Hideyoshi's long siege fails and his army\n"
            "must retreat in disgrace."
        ),
        objective=OBJ_SEIZE,
        objective_detail="Breach Odawara — seize the inner keep (8-9, 8).",
        player_units=[
            ("hideyoshi",10,15), ("kanbei",9,15), ("kiyomasa",11,15),
            ("fukushima",8,15), ("toshiie",12,15), ("magoichi",7,15),
            ("oda_gun1",9,14), ("oda_gun2",11,14), ("oda_arch1",8,14),
            ("oda_cav1",12,14), ("motochika",6,15),
        ],
        enemy_units=[
            ("ujiyasu",9,8), ("ujimasa",8,7), ("fuma",7,9),  # fuma recruitable!
            ("e_gen1",8,5), ("e_gen1",10,5), ("e_gen2",9,5),
            ("e_sam1",7,6), ("e_sam2",11,6), ("e_hat1",8,6),
            ("e_hat1",10,6), ("e_ash1",7,7), ("e_ash2",11,7),
            ("e_arch1",6,8), ("e_arch2",12,8), ("e_ksama1",5,9),
        ],
        ally_units=[("ieyasu",10,15),("tadakatsu",9,15),("naomasa",11,15)],
        map_builder=MAP_BUILDERS[16],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_gen2",7,4),("e_gen2",11,4),("e_hat1",9,4)],
                "Castle defenders reinforce the inner walls!"),
            ReinforcementWave(5, FACTION_ENEMY,
                [("e_wy1",5,3),("e_wy2",13,3)],
                "Wyvern knight scouts attack from above the walls!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=17, title="Chapter 17",
        subtitle="Defense of Fushimi",
        narrative_intro=(
            "1600. Tokugawa Ieyasu marches east to deal with Uesugi\n"
            "Kagekatsu. In his absence, Ishida Mitsunari strikes.\n"
            "Fushimi Castle — garrisoned by 1,800 men against 40,000.\n\n"
            "TORII MOTOTADA: 'We hold as long as we breathe. That is our duty.\n"
            "Ieyasu-sama must be given time to return.'\n"
            "KANBEI: 'Then let us make it count.'"
        ),
        narrative_victory=(
            "Fushimi holds longer than anyone thought possible.\n"
            "Ieyasu has the time he needs. The western coalition's\n"
            "surprise attack fails to be truly decisive.\n"
            "The road to Sekigahara opens."
        ),
        narrative_defeat=(
            "Fushimi falls too quickly. Mitsunari's coalition\n"
            "has time to fully consolidate. Ieyasu is boxed in."
        ),
        objective=OBJ_DEFEND,
        objective_detail="Hold Fushimi Castle for 10 turns. Prevent the keep from falling.",
        player_units=[
            ("ieyasu",8,7), ("tadakatsu",7,7), ("naomasa",9,7),
            ("hanzo",8,8), ("kanbei",7,8), ("oda_gun1",7,6),
            ("oda_gun2",9,6), ("oda_arch1",6,7), ("oda_arch2",10,7),
            ("oda_ash1",7,9), ("oda_ash2",9,9),
        ],
        enemy_units=[
            ("mitsunari",9,0), ("otani",8,0), ("konishi",10,0),
            ("e_sam1",7,1), ("e_sam2",11,1), ("e_ash1",6,1),
            ("e_ash2",12,1), ("e_spear1",8,1), ("e_spear2",10,1),
            ("e_arch1",7,2), ("e_arch2",11,2), ("e_gen1",9,1),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[17],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_cav1",5,0),("e_cav2",13,0),("e_hat1",9,0)],
                "Mitsunari sends in cavalry to overwhelm the gates!"),
            ReinforcementWave(5, FACTION_ENEMY,
                [("e_wy1",4,1),("e_wy2",14,1)],
                "Wyvern knights assault the walls from above!"),
            ReinforcementWave(7, FACTION_ENEMY,
                [("e_gen2",8,0),("e_gen2",10,0)],
                "Heavy general units move to breach the final gate!"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=18, title="Chapter 18",
        subtitle="Sekigahara — The Great Battle",
        narrative_intro=(
            "October 21, 1600. 80,000 face 120,000 on a foggy morning.\n"
            "IEYASU: 'The fog will lift by noon. When it does, strike.'\n"
            "MITSUNARI: 'Kobayakawa! You are with us — signal your men!'\n"
            "KOBAYAKAWA: [no response]\n"
            "IEYASU: [fires a warning shot toward Kobayakawa's hill]\n"
            "KOBAYAKAWA: [changes sides]\n"
            "MITSUNARI: '...Traitor!'"
        ),
        narrative_victory=(
            "The western coalition collapses in betrayal and rout.\n"
            "The battle is decided in six hours. Ieyasu stands over\n"
            "the greatest battlefield in Japanese history.\n"
            "He will become Shogun. Two hundred and fifty years\n"
            "of Tokugawa peace are born in this blood."
        ),
        narrative_defeat=(
            "Kobayakawa holds. Mitsunari's coordination succeeds.\n"
            "The Tokugawa east is shattered. The Toyotomi legacy lives."
        ),
        objective=OBJ_SEIZE,
        objective_detail="Seize the center of Sekigahara (10-11, 7) with Ieyasu.",
        player_units=[
            ("ieyasu",5,14), ("tadakatsu",4,14), ("naomasa",6,14),
            ("hanzo",5,13), ("kanbei",6,13), ("ina",7,14),
            ("oda_cav1",4,13), ("oda_arch1",6,12), ("oda_gun1",7,13),
            ("oda_gun2",5,12), ("toshiie",8,14),
        ],
        enemy_units=[
            ("mitsunari",11,0), ("otani",9,0), ("konishi",13,0),
            ("e_sam1",10,1), ("e_sam2",12,1), ("e_ash1",9,2),
            ("e_ash2",13,2), ("e_cav1",8,1), ("e_cav2",14,1),
            ("e_gen1",11,2), ("e_arch1",10,3), ("e_arch2",12,3),
            ("yoshihiro",16,7), ("toyohisa",17,8), ("e_berz1",15,8),
            ("masamune",19,7), ("shigezane",18,8),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[18],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_hat1",10,0),("e_hat1",12,0),("e_wy1",8,0)],
                "Western coalition elites advance under Mitsunari's command!"),
            ReinforcementWave(4, FACTION_ALLY,
                [("yukimura",5,14),("nobuyuki",6,14)],  # Sanada split — Yukimura can appear
                "Sanada troops have decided their allegiance! They join Ieyasu!"),
            ReinforcementWave(6, FACTION_ENEMY,
                [("e_berz2",15,7),("e_wy2",17,6)],
                "Shimazu Yoshihiro makes his legendary last charge!"),
        ],
        seize_unit="ieyasu"
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=19, title="Chapter 19",
        subtitle="Osaka — The Winter Siege",
        narrative_intro=(
            "1614. The young Toyotomi Hideyori holds Osaka Castle —\n"
            "the mightiest fortress in Japan — with 100,000 ronin who\n"
            "have nowhere else to go. Ieyasu, now Shogun, must finish\n"
            "what Sekigahara started.\n\n"
            "YUKIMURA [now firmly defending Osaka]: 'This is my moment.\n"
            "Everything I am — everything I've trained for — is for this.'\n"
            "IEYASU: [looking at the walls] 'Fill the outer moat with dirt.'"
        ),
        narrative_victory=(
            "A truce is negotiated. The outer moat is filled. Osaka\n"
            "Castle stands — diminished, vulnerable. Ieyasu knows\n"
            "the summer campaign will finish it. One more battle remains."
        ),
        narrative_defeat=(
            "The Toyotomi defenders hold every approach. The winter\n"
            "siege fails. Hideyori's cause lives another season."
        ),
        objective=OBJ_SEIZE,
        objective_detail="Breach the outer defenses. Seize the outer gate (8-9, 8).",
        player_units=[
            ("ieyasu",10,15), ("tadakatsu",9,15), ("naomasa",8,15),
            ("ina",11,15), ("kanbei",10,14), ("hanzo",9,14),
            ("oda_gun1",8,14), ("oda_gun2",11,14), ("oda_arch1",9,13),
            ("oda_cav1",11,13), ("toshiie",7,15),
        ],
        enemy_units=[
            ("hideyori",9,8), ("sanada_yukimura_late",8,9),
            ("otani",10,9), ("konishi",7,9),
            ("e_sam1",7,7), ("e_sam2",11,7), ("e_gen1",8,7),
            ("e_gen2",10,7), ("e_ash1",7,8), ("e_ash2",11,8),
            ("e_arch1",6,9), ("e_arch2",12,9), ("e_spear1",8,10),
            ("e_spear2",10,10), ("e_wy1",6,6), ("e_wy2",12,6),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[19],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_ron1",8,6),("e_ron2",10,6),("e_ron3",9,5)],
                "Ronin defenders rush from the inner castle walls!"),
            ReinforcementWave(5, FACTION_ENEMY,
                [("e_berz1",7,8),("e_berz2",11,8)],
                "Desperate defenders charge with suicidal ferocity!"),
            ReinforcementWave(7, FACTION_ALLY,
                [("yukimura",10,15),("nobuyuki",9,15)],
                "Wait — this is wrong. The Sanada are here... but whose side?"),
        ]
    ),

    # ═══════════════════════════════════════════════════════════════════════════
    Chapter(
        number=20, title="Chapter 20",
        subtitle="Osaka Summer — The Final Blaze",
        narrative_intro=(
            "1615. The outer moat filled, the castle stripped of defenses,\n"
            "Ieyasu strikes in summer. Osaka burns.\n"
            "But in the chaos, Sanada Yukimura makes his GREATEST charge —\n"
            "breaking through to Ieyasu's headquarters, forcing the old\n"
            "Shogun to flee. For one moment, history almost changed.\n\n"
            "YUKIMURA: 'IEYASU! SHOW YOURSELF! I AM SANADA YUKIMURA!\n"
            "I AM STILL ALIVE! THIS IS MY MOMENT!'"
        ),
        narrative_victory=(
            "Osaka Castle falls. Hideyori is gone. The Toyotomi line ends.\n"
            "Yukimura falls on the field, smiling. He said: 'There are no\n"
            "more strong men in Japan.' An enemy samurai wept to hear it.\n\n"
            "IEYASU: 'It is done. The world... is at peace.'\n"
            "Tokugawa Japan begins. Two hundred and fifty years of order.\n"
            "But was it worth the price?"
        ),
        narrative_defeat=(
            "Yukimura's charge breaks through. Ieyasu flees. Osaka holds.\n"
            "The Toyotomi survive. History is changed — for better or worse,\n"
            "Japan will never know Tokugawa peace."
        ),
        objective=OBJ_SEIZE,
        objective_detail="Seize the castle keep (8-9, 10). Survive Yukimura's charge.",
        player_units=[
            ("ieyasu",11,17), ("tadakatsu",10,17), ("naomasa",12,17),
            ("ina",9,17), ("hanzo",11,16), ("kanbei",10,16),
            ("oda_gun1",9,16), ("oda_gun2",12,16), ("oda_arch1",10,15),
            ("oda_cav1",12,15), ("toshiie",8,17), ("magoichi",13,17),
        ],
        enemy_units=[
            ("hideyori",9,10), ("sanada_yukimura_late",9,11),
            ("e_sam1",7,9), ("e_sam2",11,9), ("e_gen2",8,9),
            ("e_gen2",10,9), ("e_ash1",7,10), ("e_ash2",11,10),
            ("e_spear1",8,12), ("e_spear2",10,12), ("e_ron1",6,11),
            ("e_ron2",12,11), ("e_ron3",9,13), ("e_berz1",8,13),
            ("e_berz2",10,13), ("e_wy1",6,8), ("e_wy2",12,8),
            ("e_ninja1",5,10), ("e_ninja2",13,10),
        ],
        ally_units=[], map_builder=MAP_BUILDERS[20],
        reinforcements=[
            ReinforcementWave(3, FACTION_ENEMY,
                [("e_hat1",8,8),("e_hat1",10,8),("e_hat1",9,7)],
                "The final Toyotomi warriors converge on the keep!"),
            ReinforcementWave(4, FACTION_ENEMY,
                [("e_berz2",7,9),("e_berz2",11,9)],
                "Berserker ronin — with nothing left to lose — charge!"),
            ReinforcementWave(6, FACTION_ALLY,
                [("yukimura",10,17),("nobuyuki",9,17)],
                "Former enemies rally to end the war at last."),
        ],
        seize_unit="ieyasu"
    ),
]
