## Full unit roster — auto-generated from Python source.
class_name Roster
extends RefCounted


static func create_roster() -> Dictionary:
	var units := {}

	units["nobunaga"] = _u("nobunaga", "Oda Nobunaga", Constants.CLASS_LORD, Constants.Faction.PLAYER, 10,
		["masamune", "iron_yari"], Color(0.78, 0.31, 0.12),
		"The Demon King of the Sixth Heaven. Brutal visionary who would\nshatter tradition with gunpowder and iron will. He calls himself\na demon, but his brilliance cannot be denied.",
		"The old order crumbles before me. Only the strong survive!",
		true, false, [],
		{"hp":70,"str":65,"mag":35,"skl":60,"spd":55,"lck":50,"def":60,"res":30})

	units["hideyoshi"] = _u("hideyoshi", "Toyotomi Hideyoshi", Constants.CLASS_SAMURAI, Constants.Faction.PLAYER, 7,
		["steel_katana", "iron_tanto"], Color(0.78, 0.63, 0.20),
		"From sandal-bearer to regent — Hideyoshi's rise is Japan's greatest\nrags-to-riches story. Cunning and cheerful, he wins allies with\ncharm as readily as swords.",
		"Every sunrise is a new chance to reach the top!",
		false, false, [],
		{"hp":60,"str":55,"mag":30,"skl":60,"spd":60,"lck":65,"def":45,"res":30})

	units["mitsuhide"] = _u("mitsuhide", "Akechi Mitsuhide", Constants.CLASS_SAMURAI, Constants.Faction.PLAYER, 8,
		["steel_katana", "silver_katana"], Color(0.31, 0.31, 0.63),
		"The Brilliant General of the Oda. Cultured, precise, deeply loyal\nto tradition. He serves Nobunaga faithfully — but his lord's contempt\ngnaws at something deep within him.",
		"I fight with reason, not rage. And that makes me more dangerous.",
		false, false, [],
		{"hp":50,"str":60,"mag":25,"skl":75,"spd":65,"lck":40,"def":55,"res":30})

	units["katsuie"] = _u("katsuie", "Shibata Katsuie", Constants.CLASS_SAMURAI, Constants.Faction.PLAYER, 7,
		["steel_tetsubo", "iron_nodachi"], Color(0.63, 0.24, 0.24),
		"'The Devil Shibata' — no castle has stood against his charge,\nno army has broken his will. Gruff, fearless, and completely\ndevoted to Nobunaga's cause.",
		"Out of my way! I'll smash through anything — man, wall, or mountain!",
		false, false, [],
		{"hp":80,"str":75,"mag":10,"skl":45,"spd":45,"lck":25,"def":70,"res":15})

	units["nagahide"] = _u("nagahide", "Niwa Nagahide", Constants.CLASS_ASHIGARU, Constants.Faction.PLAYER, 6,
		["steel_yari", "iron_naginata"], Color(0.31, 0.55, 0.31),
		"Trusted administrator and general of the Oda. Where others rush\nheadlong into glory, Nagahide ensures the army is fed, supplied,\nand properly positioned.",
		"Victory is built on preparation. Let us be thorough.",
		false, false, [],
		{"hp":60,"str":55,"mag":15,"skl":55,"spd":50,"lck":45,"def":60,"res":30})

	units["ranmaru"] = _u("ranmaru", "Mori Ranmaru", Constants.CLASS_NINJA, Constants.Faction.PLAYER, 5,
		["iron_tanto", "iron_bow"], Color(0.78, 0.51, 0.63),
		"Nobunaga's devoted page. His loyalty transcends all reason —\nwhere Nobunaga walks, Ranmaru is his shadow, his shield,\nand if need be, his final guardian.",
		"Lord Nobunaga's path is my path. I will not falter!",
		false, false, [],
		{"hp":40,"str":50,"mag":25,"skl":80,"spd":75,"lck":60,"def":30,"res":40})

	units["nene"] = _u("nene", "Nene", Constants.CLASS_NINJA, Constants.Faction.PLAYER, 5,
		["kunai", "iron_bow"], Color(0.90, 0.63, 0.78),
		"Wife of Hideyoshi, spy-mistress of the Oda, and everyone's\nsurprisingly competent big sister. Her network of informants\nstretches across all provinces.",
		"You underestimate me because I smile. That's my greatest weapon.",
		false, false, [],
		{"hp":40,"str":45,"mag":40,"skl":75,"spd":80,"lck":70,"def":25,"res":55})

	units["oichi"] = _u("oichi", "Oichi", Constants.CLASS_NOBLE_LADY, Constants.Faction.PLAYER, 5,
		["heal_staff", "iron_bow"], Color(0.86, 0.71, 0.86),
		"Nobunaga's gentle younger sister. Sent to wed Azai Nagamasa as\na political alliance, she carries grace in one hand and quiet\ntragedy in the other.",
		"I pray this war ends before it swallows everyone I love.",
		false, false, [],
		{"hp":40,"str":30,"mag":65,"skl":55,"spd":55,"lck":80,"def":25,"res":70})

	units["toshiie"] = _u("toshiie", "Maeda Toshiie", Constants.CLASS_ASHIGARU, Constants.Faction.PLAYER, 6,
		["jumonji_yari", "iron_katana"], Color(0.24, 0.63, 0.78),
		"'The Tiger of the Maeda' — Toshiie fights with bold, aggressive\nstrokes. His cross-bladed spear is legendary, and his rivalry\nwith Hideyoshi is equally famous.",
		"My spear leads — the rest of the army follows!",
		false, false, [],
		{"hp":65,"str":60,"mag":10,"skl":60,"spd":55,"lck":50,"def":60,"res":25})

	units["no"] = _u("no", "No (Lady Nōhime)", Constants.CLASS_NINJA, Constants.Faction.PLAYER, 6,
		["iron_tanto", "heal_staff"], Color(0.71, 0.39, 0.63),
		"Nobunaga's principal wife. Daughter of the Viper of Mino,\nNo is as sharp as any blade. Rumor says she carries a dagger\neven at the tea ceremony.",
		"Behind this beauty lies a blade. Try me, and find out.",
		false, false, [],
		{"hp":40,"str":45,"mag":55,"skl":70,"spd":75,"lck":75,"def":30,"res":60})

	units["ina"] = _u("ina", "Ina (Komatsuhime)", Constants.CLASS_CAVALRY, Constants.Faction.PLAYER, 5,
		["iron_bow", "iron_katana"], Color(0.63, 0.78, 0.63),
		"Daughter of Honda Tadakatsu. She inherited her father's ferocity\nand her mother's grace — a mounted archer of extraordinary skill\nwho once barred even Sanada Yukimura at the castle gate.",
		"Step back. I never miss.",
		false, false, [],
		{"hp":50,"str":55,"mag":15,"skl":75,"spd":70,"lck":60,"def":50,"res":30})

	units["goemon"] = _u("goemon", "Ishikawa Goemon", Constants.CLASS_NINJA, Constants.Faction.PLAYER, 5,
		["kunai", "iron_tanto"], Color(0.39, 0.31, 0.24),
		"Japan's most famous thief and outlaw-ninja. He steals from the\nrich, gives to the poor, and somehow ends up on Hideyoshi's\nside despite being hunted by half of Japan.",
		"The greater the danger, the greater the fun. Ha ha!",
		false, false, [],
		{"hp":45,"str":55,"mag":20,"skl":80,"spd":80,"lck":70,"def":30,"res":35})

	units["gracia"] = _u("gracia", "Gracia (Tama)", Constants.CLASS_NOBLE_LADY, Constants.Faction.PLAYER, 4,
		["heal_staff", "iron_bow"], Color(0.78, 0.78, 0.94),
		"Daughter of Akechi Mitsuhide. Her gentle nature belies a fierce\nspirit — she converted to Christianity and was given the baptismal\nname Gracia. Even in war, she carries hope.",
		"Even in darkness, a single candle can push back the night.",
		false, false, [],
		{"hp":38,"str":25,"mag":70,"skl":55,"spd":60,"lck":80,"def":20,"res":75})

	units["kanbei"] = _u("kanbei", "Kuroda Kanbei", Constants.CLASS_ONMYOJI, Constants.Faction.PLAYER, 8,
		["kanbei_scroll", "iron_tanto"], Color(0.31, 0.27, 0.43),
		"'The Black Monk' — Hideyoshi's brilliant, one-legged strategist.\nKanbei's plans never fail. His eccentricities are legendary:\nhe laughs at the worst moments and weeps at the strangest victories.",
		"The enemy's plan is written on their face. I have already won.",
		false, false, [],
		{"hp":40,"str":25,"mag":75,"skl":75,"spd":55,"lck":55,"def":30,"res":70})

	units["kiyomasa"] = _u("kiyomasa", "Kato Kiyomasa", Constants.CLASS_ASHIGARU, Constants.Faction.PLAYER, 7,
		["nihongo", "steel_yari"], Color(0.78, 0.39, 0.24),
		"'The Tiger Slayer' — Kiyomasa's reputation was forged in the\nKorean campaign where he allegedly hunted tigers bare-handed.\nHis spear is as long as his stubbornness.",
		"If it moves and isn't on our side, my spear will settle the matter!",
		false, false, [],
		{"hp":70,"str":70,"mag":10,"skl":60,"spd":50,"lck":40,"def":65,"res":20})

	units["fukushima"] = _u("fukushima", "Fukushima Masanori", Constants.CLASS_SAMURAI, Constants.Faction.PLAYER, 6,
		["steel_tetsubo", "steel_katana"], Color(0.71, 0.31, 0.20),
		"Hideyoshi's foster nephew and eternal rival of Kato Kiyomasa.\nTheir argument over who gets to charge first is more dangerous\nthan most enemy armies.",
		"Out of the way, Kiyomasa! This kill is MINE!",
		false, false, [],
		{"hp":75,"str":70,"mag":10,"skl":50,"spd":50,"lck":35,"def":65,"res":15})

	units["ieyasu"] = _u("ieyasu", "Tokugawa Ieyasu", Constants.CLASS_CAVALRY, Constants.Faction.ALLY, 8,
		["steel_katana", "steel_yari"], Color(0.39, 0.47, 0.78),
		"The Tanuki of Mikawa. Patient as a stone, cunning as a fox.\nHe endured Imagawa hostage years, Oda alliance, and personal\ntragedy — all to outlast everyone else.",
		"He who endures longest, laughs last.",
		false, false, [],
		{"hp":65,"str":60,"mag":25,"skl":55,"spd":55,"lck":60,"def":65,"res":40})

	units["tadakatsu"] = _u("tadakatsu", "Honda Tadakatsu", Constants.CLASS_GENERAL, Constants.Faction.ALLY, 9,
		["tonbo_kiri", "iron_tetsubo"], Color(0.63, 0.63, 0.63),
		"Japan's mightiest warrior — Honda Tadakatsu never once received\na serious wound in 57 battles. He is Ieyasu's unmovable wall;\nhis tonbo-kiri spear is feared by every army in Japan.",
		"Come. All of you. I have not yet begun to fight.",
		false, false, [],
		{"hp":80,"str":70,"mag":10,"skl":60,"spd":45,"lck":45,"def":85,"res":25})

	units["naomasa"] = _u("naomasa", "Ii Naomasa", Constants.CLASS_CAVALRY, Constants.Faction.ALLY, 7,
		["steel_yari", "steel_katana"], Color(0.86, 0.20, 0.20),
		"The Red Devil — Ii Naomasa's entire army wears crimson armor\nto strike fear into enemies. He nearly died at Sekigahara but\nfought until the last enemy fled.",
		"Red as blood — my color signals that I am coming for you!",
		false, false, [],
		{"hp":65,"str":65,"mag":15,"skl":60,"spd":65,"lck":45,"def":60,"res":25})

	units["hanzo"] = _u("hanzo", "Hattori Hanzo", Constants.CLASS_NINJA, Constants.Faction.ALLY, 8,
		["steel_tanto", "daikyu"], Color(0.16, 0.16, 0.16),
		"The Demon Ninja — Ieyasu's shadow guardian. Half-legend,\nhalf-warrior monk, entirely terrifying. His steel tanto has\nnever left a survivor to describe his face.",
		"You saw me. That is unusual. Most don't live to say so.",
		false, false, [],
		{"hp":45,"str":65,"mag":30,"skl":85,"spd":80,"lck":55,"def":40,"res":50})

	units["yukimura"] = _u("yukimura", "Sanada Yukimura", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 9,
		["nihongo", "steel_katana"], Color(0.86, 0.12, 0.12),
		"Japan's greatest hero — the 'Crimson Demon of War' whose final\ncharge at Osaka shook the Tokugawa army to its core. Brave,\npassionate, and absolutely brilliant with a spear.",
		"My spear carries the honor of the Sanada! COME!",
		false, true, ["hideyoshi", "any"],
		{"hp":70,"str":70,"mag":15,"skl":70,"spd":65,"lck":55,"def":65,"res":30})

	units["nobuyuki"] = _u("nobuyuki", "Sanada Nobuyuki", Constants.CLASS_SAMURAI, Constants.Faction.ALLY, 7,
		["steel_katana", "iron_yari"], Color(0.71, 0.20, 0.20),
		"Yukimura's older brother — calmer, steadier, and ultimately\non a different side of the war. Their fraternal bond survives\neven the divide at Sekigahara.",
		"Our family is split by war. But the Sanada name remains unbroken.",
		false, false, [],
		{"hp":60,"str":60,"mag":15,"skl":65,"spd":60,"lck":50,"def":60,"res":30})

	units["masayuki"] = _u("masayuki", "Sanada Masayuki", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 10,
		["kanbei_scroll", "iron_tanto"], Color(0.63, 0.16, 0.16),
		"The greatest strategist of the Sanada clan. He held Ueda Castle\nagainst the Tokugawa twice with a fraction of their numbers.\nHis mind is a labyrinth no enemy has ever navigated safely.",
		"You fell into my trap three steps ago. The rest is ceremony.",
		false, true, ["nobunaga", "ieyasu"],
		{"hp":45,"str":30,"mag":80,"skl":75,"spd":60,"lck":65,"def":35,"res":70})

	units["shingen"] = _u("shingen", "Takeda Shingen", Constants.CLASS_LORD, Constants.Faction.ENEMY, 12,
		["odenta_mitsu", "silver_yari"], Color(0.63, 0.12, 0.12),
		"The Tiger of Kai. Master of the cavalry charge, nemesis of Kenshin.\nHis fan — 'Swift as wind, still as forest, fierce as fire,\nimmovable as mountain' — is strategy made poetry.",
		"WIND — FOREST — FIRE — MOUNTAIN! Takeda rides!",
		true, false, [],
		{"hp":80,"str":75,"mag":30,"skl":65,"spd":55,"lck":55,"def":70,"res":35})

	units["kansuke"] = _u("kansuke", "Yamamoto Kansuke", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 9,
		["steel_katana", "iron_yari"], Color(0.39, 0.24, 0.31),
		"Shingen's one-eyed, lame strategist. Rejected by every lord\nbefore Shingen — but Shingen saw genius. At Kawanakajima,\nKansuke charged into the enemy alone, accepting death as\npenance for his miscalculation.",
		"My body is broken. My mind is not. Attack!",
		false, false, [],
		{"hp":50,"str":65,"mag":20,"skl":75,"spd":60,"lck":30,"def":55,"res":25})

	units["masakage"] = _u("masakage", "Yamagata Masakage", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 8,
		["steel_yari", "steel_katana"], Color(0.71, 0.31, 0.24),
		"Red-armored general of the Takeda cavalry. His charging red\nhorsemen have broken formations that no infantry could stop.\nHe died at Nagashino under the Oda volley fire.",
		"Red armor! Red hearts! CHARGE!",
		false, false, [],
		{"hp":65,"str":65,"mag":10,"skl":55,"spd":70,"lck":45,"def":55,"res":20})

	units["nobushige"] = _u("nobushige", "Takeda Nobushige", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 7,
		["steel_katana"], Color(0.78, 0.39, 0.31),
		"Shingen's younger brother. Brave, principled, and devoted.\nHis 'Ninety-Nine Articles' on military strategy became\na cornerstone of samurai philosophy.",
		"Honor is not a reward. It is the road itself.",
		false, false, [],
		{"hp":60,"str":60,"mag":20,"skl":65,"spd":60,"lck":55,"def":55,"res":35})

	units["masanobu"] = _u("masanobu", "Kosaka Masanobu", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 8,
		["silver_yari", "steel_katana"], Color(0.63, 0.39, 0.27),
		"'The Keeper of the Northern Army' — Masanobu is the brilliant\nadministrator behind the Takeda war machine. Without him,\nShingen's armies would not march half as far.",
		"Supply lines are the true sinews of war.",
		false, false, [],
		{"hp":55,"str":55,"mag":30,"skl":65,"spd":60,"lck":55,"def":55,"res":40})

	units["kenshin"] = _u("kenshin", "Uesugi Kenshin", Constants.CLASS_LORD, Constants.Faction.ENEMY, 12,
		["bishamonten", "silver_katana"], Color(0.39, 0.55, 0.86),
		"The Dragon of Echigo. The living avatar of Bishamonten,\ngod of war. He never struck first without cause — but when\nhe struck, no one could stop him. He was Shingen's greatest rival.",
		"Bishamonten guides my blade! Who dares stand against the divine?",
		true, false, [],
		{"hp":75,"str":75,"mag":40,"skl":70,"spd":65,"lck":65,"def":65,"res":50})

	units["kanetsugu"] = _u("kanetsugu", "Naoe Kanetsugu", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 8,
		["raikiri", "iron_naginata"], Color(0.24, 0.39, 0.71),
		"He wears the kanji for 'love' (ai) on his helmet — and means it.\nKanetsugu's devotion to Kenshin's ideals of justice outlives\neven his lord. His blade, Raikiri, cuts like lightning.",
		"Love — that is what I fight for. Does that surprise you?",
		false, true, ["kenshin", "nobunaga", "any"],
		{"hp":55,"str":65,"mag":30,"skl":70,"spd":65,"lck":60,"def":55,"res":40})

	units["kagetsora"] = _u("kagetsora", "Uesugi Kagetsora", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 7,
		["steel_yari"], Color(0.31, 0.47, 0.78),
		"Adopted heir of Kenshin. The Hojo blood in him created endless\ntension with the Uesugi retainers. He fought valiantly against\nboth his destiny and his doubts.",
		"I carry two bloodlines and serve one master. That is enough.",
		false, false, [],
		{"hp":60,"str":60,"mag":15,"skl":60,"spd":60,"lck":50,"def":60,"res":30})

	units["masamune"] = _u("masamune", "Date Masamune", Constants.CLASS_LORD, Constants.Faction.ENEMY, 11,
		["otenta_mitsu", "silver_yari"], Color(0.12, 0.12, 0.31),
		"The One-Eyed Dragon of Oshu. He lost his eye to smallpox and\nremoved it himself. Born too late to rule all Japan — but he\nnever stopped trying. Flamboyant, unpredictable, magnificent.",
		"History will remember this moment — because I made it memorable!",
		true, false, [],
		{"hp":70,"str":70,"mag":35,"skl":70,"spd":65,"lck":60,"def":65,"res":40})

	units["shigezane"] = _u("shigezane", "Date Shigezane", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 8,
		["steel_yari", "steel_katana"], Color(0.24, 0.24, 0.55),
		"Masamune's cousin, closest friend, and steadiest general.\nWhere Masamune burns bright and reckless, Shigezane is\nthe grounding force that keeps the dragon from flying too high.",
		"I'm always pulling him back from the edge. It never gets easier.",
		false, true, ["masamune", "any"],
		{"hp":65,"str":65,"mag":15,"skl":60,"spd":65,"lck":50,"def":60,"res":25})

	units["yoshihisa"] = _u("yoshihisa", "Shimazu Yoshihisa", Constants.CLASS_LORD, Constants.Faction.ENEMY, 10,
		["steel_nodachi", "steel_yari"], Color(0.31, 0.24, 0.55),
		"The Shimazu lord who unified Kyushu. Master of the 'tsuridono'\nencirclement tactic — feign retreat to draw enemies into\na trap of flanking forces. Methodical and merciless.",
		"Retreat is not weakness. It is the first move of a trap.",
		true, false, [],
		{"hp":70,"str":65,"mag":25,"skl":65,"spd":55,"lck":55,"def":65,"res":35})

	units["yoshihiro"] = _u("yoshihiro", "Shimazu Yoshihiro", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 9,
		["fuujin_nodachi", "steel_tetsubo"], Color(0.39, 0.20, 0.63),
		"The Demon of Sekigahara. Trapped on the losing side, Yoshihiro\ncharged directly through the Tokugawa main force to escape —\na move so audacious it became legend.",
		"Demon? Yes. Yours, specifically. NOW DIE!",
		false, false, [],
		{"hp":80,"str":80,"mag":10,"skl":55,"spd":55,"lck":35,"def":70,"res":15})

	units["toyohisa"] = _u("toyohisa", "Shimazu Toyohisa", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 8,
		["steel_katana", "iron_nodachi"], Color(0.47, 0.24, 0.63),
		"Yoshihiro's nephew — young, fierce, and desperately brave.\nHe sacrificed himself covering the Shimazu retreat at Sekigahara,\ndying in a last stand against impossible odds.",
		"Uncle, go! I will hold them here as long as I breathe!",
		false, false, [],
		{"hp":70,"str":70,"mag":10,"skl":65,"spd":60,"lck":45,"def":60,"res":20})

	units["ujiyasu"] = _u("ujiyasu", "Hojo Ujiyasu", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 11,
		["nihongo", "iron_tetsubo"], Color(0.39, 0.39, 0.71),
		"'The Lion of Sagami' — Ujiyasu never lost a castle to siege\nin his lifetime. Master of fortification, night raids,\nand three-front defensive warfare.",
		"A castle is not stone and timber. It is the will of those inside.",
		true, true, ["ieyasu", "any"],
		{"hp":75,"str":65,"mag":25,"skl":65,"spd":45,"lck":55,"def":80,"res":40})

	units["ujimasa"] = _u("ujimasa", "Hojo Ujimasa", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 9,
		["steel_katana", "steel_yari"], Color(0.31, 0.31, 0.63),
		"Ujiyasu's heir — he inherited the castle network but not quite\nhis father's strategic genius. Nevertheless, he defended the\nHojo lands with fierce dignity to the very end.",
		"The Hojo stand. We have always stood. We will not yield now.",
		false, false, [],
		{"hp":65,"str":65,"mag":20,"skl":60,"spd":55,"lck":50,"def":65,"res":30})

	units["fuma"] = _u("fuma", "Fuma Kotaro", Constants.CLASS_NINJA, Constants.Faction.ENEMY, 9,
		["fuma_chain", "windcutter"], Color(0.12, 0.08, 0.20),
		"The shadow-lord of the Fuma ninja. Part man, part myth.\nHe terrorized Uesugi supply lines and fought Hattori Hanzo\nto a terrifying standstill. His face has never been confirmed.",
		"...",
		false, true, ["ranmaru", "goemon", "hanzo"],
		{"hp":50,"str":65,"mag":30,"skl":90,"spd":85,"lck":60,"def":40,"res":50})

	units["motonari"] = _u("motonari", "Mori Motonari", Constants.CLASS_LORD, Constants.Faction.ENEMY, 12,
		["silver_katana", "kanbei_scroll"], Color(0.20, 0.47, 0.31),
		"'The Fox of Chugoku' — Motonari conquered the west through\ndeception, alliance, and brilliant betrayal. His famous lesson:\n'One arrow breaks, three bound together do not.'",
		"I gave you every chance to walk away. Now it is too late.",
		true, false, [],
		{"hp":65,"str":60,"mag":55,"skl":70,"spd":55,"lck":70,"def":55,"res":55})

	units["terumoto"] = _u("terumoto", "Mori Terumoto", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 9,
		["steel_katana", "steel_yari"], Color(0.24, 0.51, 0.35),
		"Grandson of Motonari. He inherited vast domains and mediocre\nmilitary talent — but held the Mori name together through\ntwo generations of war.",
		"My grandfather built this. I will not be the one to lose it.",
		false, false, [],
		{"hp":65,"str":60,"mag":20,"skl":55,"spd":55,"lck":50,"def":60,"res":30})

	units["ekei"] = _u("ekei", "Ankokuji Ekei", Constants.CLASS_MONK, Constants.Faction.ENEMY, 8,
		["ofuda", "heal_staff"], Color(0.39, 0.63, 0.51),
		"The Mori's diplomat-monk. A master negotiator who served as\nenvoy and spy for the western alliance. When diplomacy failed,\nhe opened the sutra of war.",
		"I prayed for peace. You refused it. Let us proceed to the sermon.",
		false, false, [],
		{"hp":40,"str":20,"mag":75,"skl":70,"spd":55,"lck":65,"def":25,"res":75})

	units["magoichi"] = _u("magoichi", "Saika Magoichi", Constants.CLASS_GUNNER, Constants.Faction.ENEMY, 8,
		["saika_rifle", "iron_tanto"], Color(0.35, 0.24, 0.16),
		"Leader of the Saika mercenary gunners. His rifle never misses\na target he truly aims for. He serves whoever pays — and whoever\namuses him. Today, that might be you.",
		"I don't choose sides. I choose interesting employers.",
		false, true, ["nobunaga", "hideyoshi", "any"],
		{"hp":50,"str":60,"mag":25,"skl":80,"spd":55,"lck":60,"def":40,"res":35})

	units["motochika"] = _u("motochika", "Chosokabe Motochika", Constants.CLASS_PIRATE, Constants.Faction.ENEMY, 9,
		["odenta_mitsu", "daikyu"], Color(0.20, 0.27, 0.55),
		"Lord of Shikoku — the 'Demon Child of Tosa'. Unifier of his\nisland province, he fights from land and sea alike. His naval\ntactics are as inventive as his battlefield charges.",
		"The sea and the mountains alike are my castle! Try to take them!",
		true, true, ["hideyoshi", "any"],
		{"hp":65,"str":65,"mag":25,"skl":60,"spd":65,"lck":55,"def":55,"res":35})

	units["ginchiyo"] = _u("ginchiyo", "Tachibana Ginchiyo", Constants.CLASS_PEGASUS, Constants.Faction.ENEMY, 8,
		["flying_naginata", "heal_staff"], Color(0.78, 0.78, 1.00),
		"Lady general of the Tachibana. She inherited her father's lightning\nblade and her mother's grace — a rare and deadly combination.\nShe rides through storms other soldiers flee from.",
		"The lightning doesn't ask permission. Neither do I.",
		false, true, ["oichi", "nene", "any"],
		{"hp":50,"str":60,"mag":40,"skl":75,"spd":80,"lck":65,"def":45,"res":60})

	units["tsuruhime"] = _u("tsuruhime", "Tsuruhime of Iyo", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 7,
		["tsuruhime_bow", "iron_tanto"], Color(0.78, 0.86, 1.00),
		"The holy warrior-priestess of Oyamazumi Shrine. She commanded\nIyo Province's naval forces in person and never lost a sea battle.\nHer arrows are said to be guided by the gods of the sea.",
		"The sea gods have blessed these arrows. Let them find their mark!",
		false, true, ["motochika", "any"],
		{"hp":50,"str":55,"mag":35,"skl":80,"spd":75,"lck":70,"def":45,"res":50})

	units["mitsunari"] = _u("mitsunari", "Ishida Mitsunari", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 10,
		["onmyou_orb", "iron_tanto"], Color(0.31, 0.63, 0.51),
		"Loyal administrator of the Toyotomi — and the man who forced\nSekigahara. Cold, calculating, despised by the warriors around him,\nyet absolutely devoted to Hideyoshi's legacy.",
		"I will preserve what Lord Hideyoshi built, even if I fight alone!",
		true, false, [],
		{"hp":45,"str":30,"mag":80,"skl":75,"spd":60,"lck":65,"def":35,"res":75})

	units["otani"] = _u("otani", "Otani Yoshitsugu", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 9,
		["onmyou_orb", "heal_staff"], Color(0.47, 0.35, 0.59),
		"The Phantom General — Yoshitsugu was disfigured by leprosy,\ncarried to battle in a palanquin. Yet his tactical mind never\ndimmed, and his loyalty to Mitsunari never wavered.",
		"This body is broken. My will is not. Strike!",
		false, false, [],
		{"hp":40,"str":20,"mag":85,"skl":75,"spd":50,"lck":65,"def":25,"res":80})

	units["konishi"] = _u("konishi", "Konishi Yukinaga", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 8,
		["steel_yari", "steel_katana"], Color(0.31, 0.39, 0.24),
		"Christian daimyo and naval commander. He led the first wave of\nthe Korean invasion and always preferred negotiation to battle.\nHe and Kato Kiyomasa famously despised each other.",
		"There is no glory in unnecessary war. But here we are.",
		false, false, [],
		{"hp":60,"str":60,"mag":25,"skl":60,"spd":65,"lck":55,"def":55,"res":40})

	units["tatsuoki"] = _u("tatsuoki", "Saito Tatsuoki", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 7,
		["steel_katana", "iron_yari"], Color(0.31, 0.55, 0.31),
		"Son of the Viper of Mino. He inherited his father Dosan's\ngreat castle but not his genius. Indulgent and weak-willed,\nhe drove his own retainers away before Nobunaga arrived.",
		"You dare attack Inabayama?! I will not flee!",
		true, false, [],
		{"hp":55,"str":55,"mag":20,"skl":55,"spd":55,"lck":45,"def":50,"res":30})

	units["nagamasa"] = _u("nagamasa", "Azai Nagamasa", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 9,
		["steel_katana", "silver_yari"], Color(0.24, 0.55, 0.47),
		"Nobunaga's brother-in-law — and the man who broke alliance\nto honor an older oath. Brave, honorable, and doomed.\nHe chose loyalty to principle over self-interest.",
		"Honor demanded this. I do not regret it, even now.",
		true, true, ["oichi", "nobunaga"],
		{"hp":65,"str":65,"mag":25,"skl":65,"spd":60,"lck":55,"def":65,"res":35})

	units["yoshikage"] = _u("yoshikage", "Asakura Yoshikage", Constants.CLASS_LORD, Constants.Faction.ENEMY, 8,
		["steel_katana", "steel_yari"], Color(0.16, 0.31, 0.47),
		"The Asakura lord — cultured, indecisive, and tragically late\nto every battle that might have saved him. His castle at Ichijodani\nwas a center of art and learning burned in an afternoon.",
		"I should have marched months ago. I know that now.",
		true, false, [],
		{"hp":60,"str":58,"mag":25,"skl":55,"spd":50,"lck":45,"def":58,"res":35})

	units["yoshimoto"] = _u("yoshimoto", "Imagawa Yoshimoto", Constants.CLASS_LORD, Constants.Faction.ENEMY, 10,
		["silver_katana", "silver_yari"], Color(0.63, 0.47, 0.71),
		"The grand Imagawa lord — 25,000 soldiers strong, he marched\non Kyoto and stopped in a gully for tea. When Nobunaga's\nstorm hit, he died before he could rise from his cushion.",
		"How DARE you interrupt my tea ceremony with a war!",
		true, false, [],
		{"hp":65,"str":60,"mag":30,"skl":60,"spd":50,"lck":60,"def":60,"res":40})

	units["hideyori"] = _u("hideyori", "Toyotomi Hideyori", Constants.CLASS_LORD, Constants.Faction.ENEMY, 9,
		["silver_katana", "silver_yari"], Color(0.78, 0.63, 0.31),
		"Son of Hideyoshi. Born to rule all Japan — but the Tokugawa\nclosed in on Osaka Castle. Young, proud, and trapped by\nhis own legacy, he refused to surrender.",
		"My father's dream will not die with me. It will not die!",
		true, false, [],
		{"hp":65,"str":65,"mag":30,"skl":60,"spd":55,"lck":55,"def":60,"res":40})

	units["sanada_yukimura_late"] = _u("sanada_yukimura_late", "Sanada Yukimura (Osaka)", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 14,
		["nihongo", "steel_katana"], Color(0.90, 0.08, 0.08),
		"In his final battle at Osaka, Yukimura's charge shook Ieyasu's\ncamp to its foundations. The old Tokugawa lord turned pale.\nFor one glorious moment, the war hung by a thread.",
		"FOR THE TOYOTOMI! FOR JAPAN! THIS IS MY MOMENT!",
		false, false, [],
		{"hp":75,"str":80,"mag":15,"skl":75,"spd":70,"lck":60,"def":70,"res":30})

	units["oda_ash1"] = _u("oda_ash1", "Oda Ashigaru", Constants.CLASS_ASHIGARU, Constants.Faction.PLAYER, 1,
		["iron_yari"], Color(0.47, 0.47, 0.47),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_ash2"] = _u("oda_ash2", "Oda Ashigaru", Constants.CLASS_ASHIGARU, Constants.Faction.PLAYER, 1,
		["iron_yari"], Color(0.47, 0.47, 0.47),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_ash3"] = _u("oda_ash3", "Oda Ashigaru", Constants.CLASS_ASHIGARU, Constants.Faction.PLAYER, 2,
		["iron_tetsubo"], Color(0.47, 0.47, 0.47),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_arch1"] = _u("oda_arch1", "Oda Archer", Constants.CLASS_ARCHER, Constants.Faction.PLAYER, 2,
		["iron_bow"], Color(0.20, 0.71, 0.20),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_arch2"] = _u("oda_arch2", "Oda Archer", Constants.CLASS_ARCHER, Constants.Faction.PLAYER, 3,
		["steel_bow"], Color(0.20, 0.71, 0.20),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_cav1"] = _u("oda_cav1", "Oda Cavalry", Constants.CLASS_CAVALRY, Constants.Faction.PLAYER, 3,
		["iron_yari", "iron_katana"], Color(0.86, 0.51, 0.12),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_gun1"] = _u("oda_gun1", "Oda Gunner", Constants.CLASS_GUNNER, Constants.Faction.PLAYER, 3,
		["tanegashima", "iron_tanto"], Color(0.31, 0.35, 0.43),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_gun2"] = _u("oda_gun2", "Oda Gunner", Constants.CLASS_GUNNER, Constants.Faction.PLAYER, 4,
		["improved_gun", "iron_tanto"], Color(0.31, 0.35, 0.43),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_monk1"] = _u("oda_monk1", "Oda Monk", Constants.CLASS_MONK, Constants.Faction.PLAYER, 3,
		["heal_staff", "shakujo"], Color(0.90, 0.78, 0.16),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_spear1"] = _u("oda_spear1", "Oda Spearman", Constants.CLASS_ASHIGARU, Constants.Faction.PLAYER, 2,
		["iron_yari"], Color(0.20, 0.78, 0.86),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_ninja1"] = _u("oda_ninja1", "Oda Ninja", Constants.CLASS_NINJA, Constants.Faction.PLAYER, 3,
		["iron_tanto", "kunai"], Color(0.24, 0.24, 0.24),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_sam1"] = _u("oda_sam1", "Oda Samurai", Constants.CLASS_SAMURAI, Constants.Faction.PLAYER, 3,
		["iron_katana"], Color(0.20, 0.39, 0.78),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_sam2"] = _u("oda_sam2", "Oda Samurai", Constants.CLASS_SAMURAI, Constants.Faction.PLAYER, 4,
		["steel_katana"], Color(0.20, 0.39, 0.78),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_hatamoto1"] = _u("oda_hatamoto1", "Oda Hatamoto", Constants.CLASS_CAVALRY, Constants.Faction.PLAYER, 5,
		["steel_katana", "jumonji_yari"], Color(0.71, 0.39, 0.20),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ash1"] = _u("e_ash1", "Ashigaru", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 1,
		["iron_yari"], Color(0.71, 0.24, 0.24),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ash2"] = _u("e_ash2", "Ashigaru", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 1,
		["iron_yari"], Color(0.71, 0.24, 0.24),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ash3"] = _u("e_ash3", "Ashigaru", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 2,
		["iron_tetsubo"], Color(0.71, 0.24, 0.24),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ash4"] = _u("e_ash4", "Ashigaru", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 3,
		["iron_yari"], Color(0.71, 0.24, 0.24),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ash5"] = _u("e_ash5", "Ashigaru", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 3,
		["iron_tetsubo"], Color(0.67, 0.20, 0.20),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_sam1"] = _u("e_sam1", "Samurai", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 3,
		["iron_katana"], Color(0.59, 0.20, 0.20),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_sam2"] = _u("e_sam2", "Samurai", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 4,
		["steel_katana"], Color(0.59, 0.20, 0.20),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_sam3"] = _u("e_sam3", "Samurai", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 5,
		["steel_katana"], Color(0.63, 0.16, 0.16),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_cav1"] = _u("e_cav1", "Cavalry", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 3,
		["iron_yari", "iron_katana"], Color(0.78, 0.31, 0.31),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_cav2"] = _u("e_cav2", "Cavalry", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 5,
		["steel_yari", "steel_katana"], Color(0.78, 0.27, 0.27),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_arch1"] = _u("e_arch1", "Archer", Constants.CLASS_ARCHER, Constants.Faction.ENEMY, 2,
		["iron_bow"], Color(0.71, 0.31, 0.31),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_arch2"] = _u("e_arch2", "Archer", Constants.CLASS_ARCHER, Constants.Faction.ENEMY, 4,
		["steel_bow"], Color(0.67, 0.27, 0.27),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ninja1"] = _u("e_ninja1", "Ninja", Constants.CLASS_NINJA, Constants.Faction.ENEMY, 4,
		["iron_tanto", "kunai"], Color(0.20, 0.16, 0.24),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ninja2"] = _u("e_ninja2", "Ninja", Constants.CLASS_NINJA, Constants.Faction.ENEMY, 6,
		["steel_tanto", "daikyu"], Color(0.20, 0.16, 0.24),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_spear1"] = _u("e_spear1", "Spearman", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 3,
		["iron_yari"], Color(0.63, 0.24, 0.24),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_spear2"] = _u("e_spear2", "Spearman", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 4,
		["steel_yari"], Color(0.63, 0.22, 0.22),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_monk1"] = _u("e_monk1", "Warrior Monk", Constants.CLASS_MONK, Constants.Faction.ENEMY, 3,
		["iron_naginata", "heal_staff"], Color(0.39, 0.55, 0.55),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_monk2"] = _u("e_monk2", "Warrior Monk", Constants.CLASS_MONK, Constants.Faction.ENEMY, 5,
		["steel_naginata", "heal_staff"], Color(0.31, 0.51, 0.51),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_gen1"] = _u("e_gen1", "General", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 5,
		["iron_yari", "iron_tetsubo"], Color(0.55, 0.55, 0.55),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_gen2"] = _u("e_gen2", "General", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 7,
		["steel_yari", "steel_tetsubo"], Color(0.51, 0.51, 0.51),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_gun1"] = _u("e_gun1", "Gunner", Constants.CLASS_GUNNER, Constants.Faction.ENEMY, 3,
		["tanegashima", "iron_tanto"], Color(0.31, 0.35, 0.43),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_gun2"] = _u("e_gun2", "Gunner", Constants.CLASS_GUNNER, Constants.Faction.ENEMY, 5,
		["improved_gun", "iron_tanto"], Color(0.31, 0.35, 0.43),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_hat1"] = _u("e_hat1", "Hatamoto", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 5,
		["steel_katana", "steel_yari"], Color(0.63, 0.39, 0.24),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_pg1"] = _u("e_pg1", "Pegasus Knight", Constants.CLASS_PEGASUS, Constants.Faction.ENEMY, 4,
		["iron_naginata"], Color(0.71, 0.67, 0.86),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_wy1"] = _u("e_wy1", "Wyvern Knight", Constants.CLASS_WYVERN, Constants.Faction.ENEMY, 5,
		["steel_yari"], Color(0.55, 0.27, 0.16),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_wy2"] = _u("e_wy2", "Wyvern Knight", Constants.CLASS_WYVERN, Constants.Faction.ENEMY, 7,
		["silver_yari"], Color(0.51, 0.24, 0.12),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ron1"] = _u("e_ron1", "Ronin", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 5,
		["steel_katana"], Color(0.47, 0.12, 0.12),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ron2"] = _u("e_ron2", "Ronin", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 7,
		["steel_katana", "iron_nodachi"], Color(0.43, 0.08, 0.08),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_pirate1"] = _u("e_pirate1", "Pirate", Constants.CLASS_PIRATE, Constants.Faction.ENEMY, 4,
		["iron_katana", "iron_nodachi"], Color(0.20, 0.24, 0.47),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_pirate2"] = _u("e_pirate2", "Pirate", Constants.CLASS_PIRATE, Constants.Faction.ENEMY, 6,
		["steel_katana", "steel_nodachi"], Color(0.16, 0.20, 0.43),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_mach1"] = _u("e_mach1", "Mounted Archer", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 4,
		["iron_bow", "iron_katana"], Color(0.55, 0.67, 0.47),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_berz1"] = _u("e_berz1", "Berserker", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 5,
		["steel_tetsubo"], Color(0.78, 0.16, 0.16),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_berz2"] = _u("e_berz2", "Berserker", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 7,
		["oni_tetsubo"], Color(0.75, 0.12, 0.12),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ikko1"] = _u("e_ikko1", "Ikko-Ikki", Constants.CLASS_MONK, Constants.Faction.ENEMY, 3,
		["iron_naginata"], Color(0.39, 0.59, 0.55),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ikko2"] = _u("e_ikko2", "Ikko-Ikki", Constants.CLASS_MONK, Constants.Faction.ENEMY, 4,
		["steel_naginata", "heal_staff"], Color(0.35, 0.55, 0.51),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ksama1"] = _u("e_ksama1", "Kusarigama", Constants.CLASS_NINJA, Constants.Faction.ENEMY, 4,
		["iron_chain"], Color(0.27, 0.20, 0.35),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ron3"] = _u("e_ron3", "Rival Ronin", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 6,
		["steel_katana"], Color(0.39, 0.12, 0.12),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_hata2"] = _u("e_hata2", "Elite Hatamoto", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 8,
		["silver_katana", "jumonji_yari"], Color(0.59, 0.35, 0.20),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_fk1"] = _u("e_fk1", "Falcon Knight", Constants.CLASS_PEGASUS, Constants.Faction.ENEMY, 5,
		["iron_naginata", "heal_staff"], Color(0.82, 0.75, 1.00),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_fk2"] = _u("e_fk2", "Falcon Knight", Constants.CLASS_PEGASUS, Constants.Faction.ENEMY, 7,
		["steel_naginata", "mend_staff"], Color(0.78, 0.71, 1.00),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ea1"] = _u("e_ea1", "Eagle Archer", Constants.CLASS_PEGASUS, Constants.Faction.ENEMY, 5,
		["steel_bow"], Color(0.67, 0.86, 0.59),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ea2"] = _u("e_ea2", "Eagle Archer", Constants.CLASS_PEGASUS, Constants.Faction.ENEMY, 7,
		["silver_bow", "yumi_anti_air"], Color(0.63, 0.82, 0.55),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_sr1"] = _u("e_sr1", "Storm Rider", Constants.CLASS_NINJA, Constants.Faction.ENEMY, 5,
		["iron_tanto", "iron_katana"], Color(0.59, 0.78, 1.00),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_sr2"] = _u("e_sr2", "Storm Rider", Constants.CLASS_NINJA, Constants.Faction.ENEMY, 8,
		["steel_tanto", "steel_katana"], Color(0.55, 0.75, 1.00),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_tm1"] = _u("e_tm1", "Tengu Master", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 5,
		["iron_tanto", "ofuda"], Color(0.35, 0.20, 0.59),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_sl1"] = _u("e_sl1", "Sky Lancer", Constants.CLASS_WYVERN, Constants.Faction.ENEMY, 6,
		["steel_yari"], Color(0.67, 0.43, 0.22),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_sl2"] = _u("e_sl2", "Sky Lancer", Constants.CLASS_WYVERN, Constants.Faction.ENEMY, 8,
		["silver_yari", "iron_naginata"], Color(0.63, 0.39, 0.18),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_dk1"] = _u("e_dk1", "Dragon Knight", Constants.CLASS_WYVERN, Constants.Faction.ENEMY, 8,
		["silver_yari", "steel_katana"], Color(0.75, 0.27, 0.10),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_dk2"] = _u("e_dk2", "Dragon Knight", Constants.CLASS_WYVERN, Constants.Faction.ENEMY, 10,
		["dojikiri", "nihongo"], Color(0.71, 0.24, 0.08),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_lc1"] = _u("e_lc1", "Lance Cavalry", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 4,
		["iron_yari"], Color(0.82, 0.51, 0.22),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_lc2"] = _u("e_lc2", "Lance Cavalry", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 6,
		["steel_yari", "iron_naginata"], Color(0.78, 0.47, 0.18),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_we1"] = _u("e_we1", "War Elephant", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 6,
		["iron_tetsubo", "iron_yari"], Color(0.35, 0.27, 0.22),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_we2"] = _u("e_we2", "War Elephant", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 9,
		["steel_tetsubo", "steel_yari"], Color(0.31, 0.24, 0.18),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ltc1"] = _u("e_ltc1", "Light Cavalry", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 3,
		["iron_tanto", "iron_bow"], Color(0.76, 0.76, 0.43),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ltc2"] = _u("e_ltc2", "Light Cavalry", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 5,
		["steel_tanto", "iron_bow"], Color(0.73, 0.73, 0.39),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_gk1"] = _u("e_gk1", "Great Knight", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 5,
		["steel_katana", "iron_yari"], Color(0.51, 0.51, 0.67),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_gk2"] = _u("e_gk2", "Great Knight", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 8,
		["silver_katana", "jumonji_yari"], Color(0.47, 0.47, 0.63),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_nc1"] = _u("e_nc1", "Noble Cavalry", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 6,
		["steel_katana", "silver_yari"], Color(0.82, 0.75, 0.29),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["kobayakawa"] = _u("kobayakawa", "Kobayakawa Hideaki", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 8,
		["silver_katana", "jumonji_yari"], Color(0.39, 0.43, 0.67),
		"The pivotal traitor of Sekigahara. Promised rewards by both sides,\nhe waited atop his hill — until Ieyasu fired a warning shot toward him.\nHe then charged Mitsunari's flank, deciding the battle.",
		"The winning side... is the side that wins. Obviously.",
		false, true, ["ieyasu", "any"],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["matsunaga"] = _u("matsunaga", "Matsunaga Hisahide", Constants.CLASS_NINJA, Constants.Faction.ENEMY, 9,
		["steel_tanto", "steel_katana"], Color(0.24, 0.16, 0.39),
		"The 'Three Great Villainies' lord — burned Todaiji, killed the Shogun,\nbetrayed every alliance he made. When cornered by Nobunaga,\nhe blew himself up with his own precious tea kettle.",
		"Burn everything, own nothing. That is true freedom.",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["naotora"] = _u("naotora", "Ii Naotora", Constants.CLASS_CAVALRY, Constants.Faction.ALLY, 7,
		["steel_yari", "iron_naginata"], Color(0.90, 0.24, 0.24),
		"The Lady Ii — she inherited her clan's famous red armor and held\ntheir domain alone while the men were at war. She is Ii Naomasa's\nadoptive mother and the true iron heart of the red devils.",
		"Red is not the color of death. It is the color of life — and will!",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["tsuruhime_upgraded"] = _u("tsuruhime_upgraded", "Tsuruhime the Sea Falcon", Constants.CLASS_PEGASUS, Constants.Faction.ALLY, 8,
		["tsuruhime_bow", "yumi_anti_air"], Color(0.71, 0.82, 1.00),
		"Promoted to Eagle Archer after mastering the gods' own wind currents.\nHer shots from altitude have the force of a diving hawk.\nShe claims the sea eagles are her messengers from Oyamazumi Shrine.",
		"The gods gave me arrows and wings. Let that be sufficient.",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["yoshitsune"] = _u("yoshitsune", "Minamoto no Yoshitsune", Constants.CLASS_PEGASUS, Constants.Faction.ALLY, 9,
		["silver_naginata", "physic_staff"], Color(0.78, 0.86, 1.00),
		"The legendary hero-general — appearing as a vision to guide the army.\nSwift as thought, agile as the wind, and blessed with divine grace.\nHe fights from the air, healing allies even as he strikes enemies.",
		"I ride where the wind rides. And the wind goes everywhere.",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["shimazu_ash1"] = _u("shimazu_ash1", "Shimazu Soldier", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 4,
		["iron_yari"], Color(0.35, 0.20, 0.55),
		"",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["shimazu_ash2"] = _u("shimazu_ash2", "Shimazu Soldier", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 4,
		["iron_yari"], Color(0.35, 0.20, 0.55),
		"",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["shimazu_archer"] = _u("shimazu_archer", "Shimazu Archer", Constants.CLASS_PEGASUS, Constants.Faction.ENEMY, 5,
		["steel_bow"], Color(0.39, 0.24, 0.59),
		"",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["hidemitsu"] = _u("hidemitsu", "Akechi Hidemitsu", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 7,
		["steel_yari", "steel_katana"], Color(0.27, 0.27, 0.55),
		"Mitsuhide's nephew and most devoted sub-commander. He led the\nencirclement force at Honnoji and pursued the Oda survivors\nwith ruthless efficiency. Loyal to his uncle to the very end.",
		"My uncle's will is absolute. His enemies have no tomorrow.",
		false, false, [],
		{"hp":60,"str":60,"mag":15,"skl":55,"spd":60,"lck":40,"def":55,"res":25})

	units["mitsuyoshi"] = _u("mitsuyoshi", "Akechi Mitsuyoshi", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 7,
		["steel_katana", "iron_nodachi"], Color(0.35, 0.35, 0.63),
		"Mitsuhide's son. Inherited his father's precision with a sword\nbut not his patience. He died at Yamazaki trying to cover\nhis father's retreat — cut down before he could reach safety.",
		"For the Akechi name — we fight, even if we fall!",
		false, false, [],
		{"hp":55,"str":60,"mag":15,"skl":70,"spd":65,"lck":40,"def":50,"res":25})

	units["muneharu"] = _u("muneharu", "Shimizu Muneharu", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 8,
		["nihongo", "steel_tetsubo"], Color(0.31, 0.39, 0.55),
		"The commander of Takamatsu Castle — a man of extraordinary loyalty.\nWhen the castle was flooded and all hope lost, he chose to sacrifice\nhimself by ritual suicide so his garrison could live. His courage\nwas acknowledged even by Hideyoshi.",
		"My men may live. That is enough. My life is a small price.",
		false, false, [],
		{"hp":70,"str":60,"mag":10,"skl":55,"spd":35,"lck":50,"def":80,"res":30})

	units["miyabe"] = _u("miyabe", "Miyabe Keijun", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 7,
		["kanbei_scroll", "iron_tanto"], Color(0.35, 0.27, 0.43),
		"Mitsuhide's chief military strategist at Honnoji — the planner\nbehind the encirclement. He managed the political aftermath\nof the coup before Hideyoshi's lightning march changed everything.",
		"We planned for every contingency. Every one except Hideyoshi's speed.",
		false, false, [],
		{"hp":40,"str":25,"mag":70,"skl":65,"spd":55,"lck":55,"def":30,"res":65})

	units["katsuyori"] = _u("katsuyori", "Takeda Katsuyori", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 10,
		["silver_yari", "steel_katana"], Color(0.67, 0.20, 0.20),
		"Shingen's heir — brave, bold, and tragically reckless.\nAt Nagashino, he ordered his legendary cavalry into the Oda volley\nfire against all advice. He was not his father. He died for it.",
		"Takeda cavalry has never been stopped! CHARGE! CHARGE! CHARGE!",
		true, false, [],
		{"hp":65,"str":70,"mag":20,"skl":60,"spd":65,"lck":40,"def":60,"res":25})

	units["narimasa"] = _u("narimasa", "Sassa Narimasa", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 8,
		["steel_tetsubo", "steel_katana"], Color(0.67, 0.31, 0.20),
		"One of Katsuie's most aggressive generals — a berserk warrior\nwho was once banned from Nobunaga's presence for excessive violence\neven by Nobunaga's standards. That is quite the achievement.",
		"Banned from Nobunaga's court for being too violent? I take that as a compliment.",
		false, false, [],
		{"hp":75,"str":70,"mag":5,"skl":45,"spd":50,"lck":30,"def":65,"res":15})

	units["matahachi"] = _u("matahachi", "Siege Commander Matahachi", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 6,
		["steel_yari", "iron_naginata"], Color(0.39, 0.31, 0.55),
		"A fictional but archetypal siege officer — the man Mitsunari\nentrusts with holding the critical gates of Osaka Castle.\nExperienced, cautious, and very hard to dislodge.",
		"These walls do not fall while I breathe.",
		false, false, [],
		{"hp":60,"str":55,"mag":10,"skl":55,"spd":45,"lck":40,"def":60,"res":25})

	units["okita_clan"] = _u("okita_clan", "Ōkita of the Mori", Constants.CLASS_WYVERN, Constants.Faction.ENEMY, 8,
		["steel_yari", "iron_katana"], Color(0.20, 0.43, 0.27),
		"A Mori flying officer who patrols the sea approaches to Takamatsu\nCastle. When the castle floods, he flies desperate supply runs\nlow over the water. A devoted and dangerous opponent.",
		"The Mori endure. I endure. Fly on!",
		false, false, [],
		{"hp":60,"str":60,"mag":5,"skl":55,"spd":55,"lck":35,"def":60,"res":20})

	units["okuni"] = _u("okuni", "Izumo no Okuni", Constants.CLASS_PEGASUS, Constants.Faction.PLAYER, 8,
		["flying_naginata", "heal_staff"], Color(0.71, 0.90, 1.00),
		"The founder of Kabuki theater — Okuni turned her sacred shrine dances\ninto a new art form that swept Japan. In battle, her movements channel\nwind kami into blasts that scatter enemy formations.",
		"Watch me dance. Then watch your soldiers run.",
		false, true, ["hideyoshi", "any"],
		{"hp":35,"str":20,"mag":75,"skl":65,"spd":80,"lck":70,"def":20,"res":70})

	units["tamamo"] = _u("tamamo", "Tamamo-no-Mae", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 11,
		["onmyou_orb", "windcutter"], Color(1.00, 0.82, 0.55),
		"The nine-tailed fox spirit in the guise of a peerless beauty.\nShe has served emperors and shoguns across centuries.\nHer illusions are indistinguishable from reality.",
		"Which of these is real? Are you even certain you are?",
		false, false, [],
		{"hp":30,"str":15,"mag":90,"skl":70,"spd":70,"lck":80,"def":15,"res":80})

	units["tenkai"] = _u("tenkai", "Tenkai", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 10,
		["onmyou_orb", "shakujo"], Color(0.24, 0.08, 0.31),
		"The Black-Robed Advisor — Ieyasu's mysterious monk counsellor.\nRumored to be the reincarnation of Akechi Mitsuhide, Tenkai weaves\ndark spiritual curses that no warrior can simply cut through.",
		"Darkness is not the absence of light. It is the presence of truth.",
		false, true, ["ieyasu", "any"],
		{"hp":40,"str":10,"mag":85,"skl":65,"spd":50,"lck":40,"def":25,"res":75})

	units["chigusa"] = _u("chigusa", "Lady Chigusa", Constants.CLASS_MONK, Constants.Faction.ALLY, 8,
		["amulet_staff", "heal_staff"], Color(1.00, 0.94, 0.78),
		"Chief shrine maiden of Atsuta Shrine — the very shrine whose divine favor\nNobunaga invoked before Okehazama. Lady Chigusa has tended sacred flame\nfor forty years and seen every warlord bow at her threshold.",
		"I do not pray for victory. I pray for you to be worth the gods' attention.",
		false, false, [],
		{"hp":45,"str":15,"mag":75,"skl":65,"spd":55,"lck":75,"def":25,"res":80})

	units["sessai"] = _u("sessai", "Taigen Sessai", Constants.CLASS_MONK, Constants.Faction.ENEMY, 10,
		["shakujo", "iron_naginata"], Color(0.90, 0.86, 1.00),
		"The brilliant monk-general of the Imagawa — strategist, diplomat,\nand healer in one. He guided Yoshimoto's campaigns with serene\nprecision. Even enemies respected his wisdom.",
		"I carry the sutras in one hand and a naginata in the other. Both serve the same purpose.",
		false, true, ["nobunaga", "any"],
		{"hp":55,"str":40,"mag":70,"skl":65,"spd":55,"lck":60,"def":50,"res":70})

	units["jade_oracle"] = _u("jade_oracle", "Omiwa the Jade Oracle", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 12,
		["onmyou_orb", "kanbei_scroll"], Color(0.55, 0.86, 0.63),
		"A reclusive sorceress who channels the spirit of the jade dragon.\nShe answers to no lord and destroys armies that trespass on her mountain.\nHer magic can shatter castle gates.",
		"You came to MY mountain. I did not invite you.",
		false, false, [],
		{"hp":30,"str":10,"mag":95,"skl":75,"spd":55,"lck":45,"def":10,"res":70})

	units["raijin_shaman"] = _u("raijin_shaman", "Fujibayashi Nagato", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 9,
		["ofuda", "steel_yari"], Color(1.00, 0.94, 0.31),
		"A warrior-mystic who calls lightning from storm clouds on horseback.\nHe claims Raijin, god of thunder, speaks directly into his ear.\nThe claim is not entirely unconvincing on a battlefield.",
		"Thunder first. Lightning second. You third.",
		false, true, ["any"],
		{"hp":55,"str":45,"mag":70,"skl":55,"spd":60,"lck":40,"def":50,"res":60})

	units["zogan"] = _u("zogan", "Zogan the Martyr", Constants.CLASS_MONK, Constants.Faction.ENEMY, 10,
		["shakujo", "kunai"], Color(0.63, 0.08, 0.08),
		"Fanatical Ikko-Ikki ascetic who has mastered self-mortification to\nconvert agony into spiritual destructive force. He welcomes wounds.\nThe more he bleeds, the more terrible his power becomes.",
		"Pain is just karma leaving the body. And taking yours with it.",
		false, false, [],
		{"hp":60,"str":25,"mag":75,"skl":50,"spd":50,"lck":25,"def":35,"res":55})

	units["tsukikage"] = _u("tsukikage", "Lady Tsukikage", Constants.CLASS_PEGASUS, Constants.Faction.ALLY, 8,
		["flying_naginata", "heal_staff"], Color(0.71, 0.71, 1.00),
		"A celestial guardian who rides a moon-pale steed through the night sky.\nHer naginata shimmers like moonlight, and her healing songs calm\neven the most berserk warriors mid-battle.",
		"The moon watches every battle. She sent me to even the odds.",
		false, true, ["any"],
		{"hp":45,"str":50,"mag":65,"skl":65,"spd":70,"lck":60,"def":40,"res":65})

	units["kagemusha"] = _u("kagemusha", "Kagemusha of the Dark Pass", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 9,
		["muramasa", "kanbei_scroll"], Color(0.31, 0.31, 0.47),
		"A cursed samurai bound by dark spirit contract who serves whichever\nwarlord currently holds his sealed blade. Neither fully alive nor dead,\nhe fights with a calm that only the beyond-caring possess.",
		"I have died before. It was quieter than this.",
		false, false, [],
		{"hp":55,"str":60,"mag":55,"skl":55,"spd":55,"lck":25,"def":55,"res":50})

	units["uzume"] = _u("uzume", "Ama no Uzume", Constants.CLASS_PEGASUS, Constants.Faction.ALLY, 10,
		["windcutter", "heal_staff"], Color(1.00, 0.94, 0.47),
		"The divine dancer who once lured Amaterasu from the cave,\nrestoring sunlight to the world. Now manifest in the age of war,\nUzume soars on starlight, turning the tide with celestial magic.",
		"I danced for a sun goddess once. Your army is considerably less impressive.",
		false, false, [],
		{"hp":35,"str":25,"mag":85,"skl":70,"spd":85,"lck":75,"def":20,"res":70})

	units["seimei_heir"] = _u("seimei_heir", "The Heir of Seimei", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 14,
		["onmyou_orb", "kanbei_scroll"], Color(0.16, 0.00, 0.16),
		"Descendant of Abe no Seimei, the greatest onmyoji who ever lived.\nThis heir has surpassed even their ancestor — mastering the forbidden\narts that can unmake a soul. A late-game boss of terrible power.",
		"Seimei saw fate in the stars. I write it.",
		false, false, [],
		{"hp":30,"str":10,"mag":100,"skl":80,"spd":45,"lck":20,"def":10,"res":70})

	units["koito"] = _u("koito", "Shirabyoshi Koito", Constants.CLASS_NINJA, Constants.Faction.PLAYER, 5,
		["kunai"], Color(1.00, 0.71, 0.78),
		"A wandering sacred dancer who joins the Oda cause after Nobunaga\nspares her shrine from burning. Her ritual dances channel kami\nenergy into her allies, granting them renewed strength.",
		"Dance with me — or watch me dance. Either way, you'll feel better.",
		false, true, ["any"],
		{"hp":35,"str":20,"mag":55,"skl":55,"spd":75,"lck":80,"def":15,"res":60})

	units["yuken"] = _u("yuken", "Yuken the Yamabushi", Constants.CLASS_MONK, Constants.Faction.ENEMY, 7,
		["steel_naginata", "ofuda"], Color(0.47, 0.31, 0.16),
		"A mountain ascetic warrior who has meditated at Kurama for twenty years.\nHis naginata technique is formidable; his fire-walking rituals have\ngiven him an unnerving immunity to ordinary fear.",
		"The mountain taught me patience. I spent it all getting here.",
		false, true, ["any"],
		{"hp":60,"str":55,"mag":45,"skl":55,"spd":45,"lck":40,"def":55,"res":50})

	units["hana_miko"] = _u("hana_miko", "Hana the Miko", Constants.CLASS_MONK, Constants.Faction.ALLY, 5,
		["heal_staff", "iron_bow"], Color(1.00, 0.86, 0.86),
		"A shrine maiden of Ise Jingu, the most sacred shrine in Japan.\nHer prayers can turn aside arrows, and her spirit-blessed bow\nstrikes truer than most trained archers' shots.",
		"The gods do not guarantee victory. They guarantee I will try.",
		false, false, [],
		{"hp":40,"str":25,"mag":65,"skl":60,"spd":55,"lck":70,"def":20,"res":70})

	units["kasai"] = _u("kasai", "Kasai the Nomad", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 6,
		["iron_bow", "iron_tanto"], Color(0.71, 0.63, 0.39),
		"A horse-archer from the northern steppe who rides for whoever pays\nwell. His arrows can split a coin at a hundred yards and he never\nsleeps on the same patch of ground twice.",
		"I don't fight for lords. I fight for the wind at my back.",
		false, true, ["any"],
		{"hp":45,"str":50,"mag":10,"skl":70,"spd":70,"lck":55,"def":35,"res":20})

	units["ishida_guard"] = _u("ishida_guard", "Ishida's Iron Guard", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 7,
		["steel_yari", "steel_tetsubo"], Color(0.63, 0.63, 0.55),
		"One of Ishida Mitsunari's elite castle garrison guards.\nImmovable in defense, they have held fortress gates against forces\nten times their number. They do not retreat.",
		"This gate does not open. Not for you. Not for anyone.",
		false, false, [],
		{"hp":70,"str":50,"mag":5,"skl":45,"spd":30,"lck":30,"def":75,"res":30})

	units["dohei"] = _u("dohei", "Dohei the Merchant", Constants.CLASS_ASHIGARU, Constants.Faction.ALLY, 4,
		["iron_tanto", "iron_bow"], Color(0.78, 0.67, 0.39),
		"A cunning merchant-soldier who profits from every campaign.\nHe carries extra supplies, trades weapons mid-battle, and always\nknows where the nearest cache of iron is buried.",
		"War is terrible. Terrible for most people. Excellent for me.",
		false, true, ["any"],
		{"hp":40,"str":35,"mag":25,"skl":55,"spd":55,"lck":65,"def":30,"res":40})

	units["kuro_musha"] = _u("kuro_musha", "Kuro the Wandering Warrior", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 6,
		["steel_katana", "iron_yari"], Color(0.47, 0.39, 0.31),
		"A masterless wandering warrior who fights for whoever has the most\ninteresting battle ahead. No clan owns him. No lord commands him.\nHe fights because it's what he does best.",
		"I've fought for a dozen lords. You might be worth a thirteenth.",
		false, true, ["any"],
		{"hp":55,"str":60,"mag":10,"skl":60,"spd":55,"lck":50,"def":50,"res":20})

	units["gennosuke"] = _u("gennosuke", "Gennosuke the Yojimbo", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 7,
		["steel_katana", "steel_nodachi"], Color(0.31, 0.31, 0.24),
		"A legendary bodyguard known across three provinces.\nHe has defended his current lord through seventeen assassination\nattempts. He charges a great deal. He is worth it.",
		"You want past me? That'll cost you more than money.",
		false, true, ["any"],
		{"hp":60,"str":60,"mag":10,"skl":65,"spd":55,"lck":45,"def":60,"res":20})

	units["mizuki"] = _u("mizuki", "Mizuki the Water Witch", Constants.CLASS_ONMYOJI, Constants.Faction.ALLY, 6,
		["ofuda", "heal_staff"], Color(0.39, 0.63, 0.86),
		"A water-spirit medium who walks barefoot on river banks and\ncommunes with the water kami. Her ice-cold magic flash-freezes\nenemy formations and heals allies with cool, purifying waters.",
		"The river knows everything. It just takes a moment to listen.",
		false, false, [],
		{"hp":38,"str":10,"mag":75,"skl":60,"spd":55,"lck":65,"def":20,"res":75})

	units["kagero_fire"] = _u("kagero_fire", "Kagero the Fire Acolyte", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 6,
		["ofuda", "tanegashima"], Color(0.86, 0.39, 0.16),
		"A fire-cult acolyte who combines mystical flame-calling with the\nOda's new tanegashima rifles. The result is a walking conflagration\nthat even veteran warriors prefer to avoid.",
		"Everything burns eventually. I just help it along.",
		false, true, ["any"],
		{"hp":45,"str":20,"mag":70,"skl":55,"spd":50,"lck":40,"def":25,"res":60})

	units["musashibou"] = _u("musashibou", "Musashibou Benkei", Constants.CLASS_MONK, Constants.Faction.ENEMY, 9,
		["steel_katana", "iron_naginata"], Color(0.63, 0.39, 0.24),
		"The legendary warrior-monk of Gojo Bridge. He collected 999 swords\nfrom defeated samurai; the 1000th led to his downfall and greatest\nloyalty. A historical legend appearing as an enemy boss.",
		"Nine hundred ninety-nine swords I took. You will be one more.",
		false, false, [],
		{"hp":70,"str":65,"mag":35,"skl":65,"spd":50,"lck":45,"def":60,"res":50})

	units["gorozo"] = _u("gorozo", "Gorozo the Rogue", Constants.CLASS_NINJA, Constants.Faction.PLAYER, 4,
		["kunai", "iron_chain"], Color(0.24, 0.20, 0.16),
		"An outlaw-thief who joins the Oda on a dare and never quite leaves.\nHe claims to be able to open any lock and steal anything not nailed\ndown — and some things that are.",
		"I'm not a spy. Spies have ideology. I just enjoy this sort of thing.",
		false, true, ["goemon", "any"],
		{"hp":40,"str":45,"mag":20,"skl":75,"spd":75,"lck":70,"def":25,"res":30})

	units["kanemitsu"] = _u("kanemitsu", "Lord Kanemitsu", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 7,
		["kanbei_scroll", "iron_katana"], Color(0.78, 0.75, 0.63),
		"A Kyoto court noble who commands through political maneuvering\nas much as military skill. His network of informants and debts\ncalled in makes him dangerous even without drawing a sword.",
		"War is simply politics conducted by louder means.",
		false, true, ["nobunaga", "any"],
		{"hp":40,"str":35,"mag":60,"skl":55,"spd":50,"lck":65,"def":30,"res":60})

	units["umio"] = _u("umio", "Umio the Sea Soldier", Constants.CLASS_PIRATE, Constants.Faction.ENEMY, 5,
		["iron_katana", "steel_yari"], Color(0.24, 0.31, 0.55),
		"A grizzled naval foot soldier who has fought in every sea battle\nfrom Kyushu to the Japan Sea. Equally at home on a rocking deck\nor a rain-soaked beach.",
		"Land, sea, river — they're all the same to me. Wet and full of enemies.",
		false, true, ["motochika", "any"],
		{"hp":60,"str":55,"mag":5,"skl":50,"spd":50,"lck":45,"def":55,"res":25})

	units["young_takeda"] = _u("young_takeda", "Young Takeda Retainer", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 3,
		["iron_katana"], Color(0.55, 0.63, 0.75),
		"A young Takeda clan retainer, barely old enough to hold his sword\nproperly but burning with loyalty to the Tiger of Kai.\nRaw potential waiting to be forged.",
		"I'll prove myself! Lord Shingen will see!",
		false, true, ["any"],
		{"hp":55,"str":55,"mag":15,"skl":60,"spd":55,"lck":55,"def":45,"res":25})

	units["musashi"] = _u("musashi", "Miyamoto Musashi", Constants.CLASS_SAMURAI, Constants.Faction.ALLY, 10,
		["dojikiri", "muramasa"], Color(0.86, 0.24, 0.24),
		"Japan's greatest swordsman — undefeated in over sixty duels.\nHe appears on the battlefield like a legend made flesh,\nhis two-sword style incomprehensible to any opponent.",
		"There is nothing outside of yourself that can ever enable you to get better. Everything is within.",
		false, false, [],
		{"hp":55,"str":80,"mag":10,"skl":95,"spd":80,"lck":50,"def":50,"res":20})

	units["matsu"] = _u("matsu", "Matsu (Lady Maeda)", Constants.CLASS_NOBLE_LADY, Constants.Faction.ALLY, 8,
		["physic_staff", "silver_bow"], Color(0.94, 0.78, 0.94),
		"Wife of Maeda Toshiie, the legendary Lady Maeda who once faced down\nTokugawa's retainers alone in her garden with a naginata. Now she rides\ninto battle as healer and protector of the Maeda cause.",
		"My husband charges forward. I make sure there's still someone to come home to.",
		false, false, [],
		{"hp":45,"str":25,"mag":80,"skl":65,"spd":65,"lck":75,"def":35,"res":80})

	units["shimazu_great_gen"] = _u("shimazu_great_gen", "Shimazu Great General", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 12,
		["nihongo", "oni_tetsubo"], Color(0.82, 0.82, 0.86),
		"The supreme armored commander of the Shimazu western army.\nHis armor has stopped fifteen arrows and three cannon balls.\nHe considers this a slow morning.",
		"Come. I have armor for all occasions. Including this one.",
		false, false, [],
		{"hp":80,"str":65,"mag":10,"skl":50,"spd":25,"lck":35,"def":90,"res":40})

	units["imagawa_warlord"] = _u("imagawa_warlord", "Imagawa Battle-Commander", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 10,
		["steel_tetsubo", "odenta_mitsu"], Color(0.86, 0.20, 0.12),
		"The military strongarm of the Imagawa army — all brute power and\nbattlefield intimidation. Hideyoshi once said this man was the\nonly enemy who ever actually made him run.",
		"FORWARD! SMASH EVERYTHING! WORRY LATER!",
		false, false, [],
		{"hp":80,"str":80,"mag":15,"skl":50,"spd":50,"lck":30,"def":70,"res":20})

	units["pe_ron1"] = _u("pe_ron1", "Elite Ronin", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 10,
		["silver_katana", "steel_nodachi"], Color(0.43, 0.08, 0.08),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_ron2"] = _u("pe_ron2", "Master Ronin", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 13,
		["dojikiri", "muramasa"], Color(0.39, 0.04, 0.04),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_gen1"] = _u("pe_gen1", "Iron General", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 11,
		["silver_yari", "steel_tetsubo"], Color(0.51, 0.51, 0.51),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_gen2"] = _u("pe_gen2", "Great General", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 12,
		["nihongo", "oni_tetsubo"], Color(0.80, 0.80, 0.84),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_hat1"] = _u("pe_hat1", "Elite Hatamoto", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 11,
		["silver_katana", "jumonji_yari"], Color(0.59, 0.35, 0.20),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_hat2"] = _u("pe_hat2", "Grand Hatamoto", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 14,
		["dojikiri", "silver_yari"], Color(0.55, 0.31, 0.16),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_gk1"] = _u("pe_gk1", "Great Knight", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 11,
		["silver_katana", "jumonji_yari"], Color(0.47, 0.47, 0.63),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_gk2"] = _u("pe_gk2", "Iron Great Knight", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 13,
		["dojikiri", "silver_yari"], Color(0.43, 0.43, 0.59),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_nc1"] = _u("pe_nc1", "Lord's Cavalry", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 11,
		["silver_katana", "silver_yari"], Color(0.80, 0.73, 0.27),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_nc2"] = _u("pe_nc2", "Grand Cavalry", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 13,
		["dojikiri", "nihongo"], Color(0.76, 0.69, 0.24),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_fk1"] = _u("pe_fk1", "Falcon Knight", Constants.CLASS_PEGASUS, Constants.Faction.ENEMY, 11,
		["silver_naginata", "mend_staff"], Color(0.78, 0.71, 1.00),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_fk2"] = _u("pe_fk2", "Sky Falcon", Constants.CLASS_PEGASUS, Constants.Faction.ENEMY, 13,
		["flying_naginata", "physic_staff"], Color(0.75, 0.67, 0.96),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_dk1"] = _u("pe_dk1", "Dragon Knight", Constants.CLASS_WYVERN, Constants.Faction.ENEMY, 12,
		["silver_yari", "dojikiri"], Color(0.73, 0.25, 0.08),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_dk2"] = _u("pe_dk2", "War Dragon", Constants.CLASS_WYVERN, Constants.Faction.ENEMY, 15,
		["bishamonten", "honjo_masamune"], Color(0.69, 0.22, 0.04),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_sr1"] = _u("pe_sr1", "Storm Rider", Constants.CLASS_NINJA, Constants.Faction.ENEMY, 11,
		["windcutter", "steel_katana"], Color(0.55, 0.75, 1.00),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_sr2"] = _u("pe_sr2", "Sky Assassin", Constants.CLASS_NINJA, Constants.Faction.ENEMY, 14,
		["windcutter", "muramasa"], Color(0.51, 0.71, 0.96),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_sl1"] = _u("pe_sl1", "Sky Lancer", Constants.CLASS_WYVERN, Constants.Faction.ENEMY, 11,
		["silver_yari", "iron_naginata"], Color(0.63, 0.39, 0.18),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_sl2"] = _u("pe_sl2", "Iron Sky Lancer", Constants.CLASS_WYVERN, Constants.Faction.ENEMY, 13,
		["nihongo", "flying_naginata"], Color(0.59, 0.35, 0.14),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_lc1"] = _u("pe_lc1", "Elite Cavalry", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 10,
		["silver_yari", "steel_naginata"], Color(0.76, 0.45, 0.16),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_lc2"] = _u("pe_lc2", "Lance Master", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 12,
		["nihongo", "silver_naginata"], Color(0.73, 0.41, 0.12),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_wl1"] = _u("pe_wl1", "Warlord", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 11,
		["oni_tetsubo", "steel_nodachi"], Color(0.84, 0.18, 0.10),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_wl2"] = _u("pe_wl2", "Battle Warlord", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 14,
		["oni_tetsubo", "fuujin_nodachi"], Color(0.80, 0.14, 0.06),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_gg1"] = _u("pe_gg1", "Great General", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 13,
		["nihongo", "oni_tetsubo"], Color(0.78, 0.78, 0.82),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_tm1"] = _u("pe_tm1", "Tengu Master", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 10,
		["windcutter", "onmyou_orb"], Color(0.33, 0.18, 0.57),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_ea1"] = _u("pe_ea1", "Eagle Archer", Constants.CLASS_PEGASUS, Constants.Faction.ENEMY, 10,
		["silver_bow", "yumi_anti_air"], Color(0.63, 0.82, 0.55),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_sp1"] = _u("pe_sp1", "Void Prophet", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 10,
		["onmyou_orb"], Color(0.22, 0.06, 0.29),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_jd1"] = _u("pe_jd1", "Jade Sorceress", Constants.CLASS_ONMYOJI, Constants.Faction.ENEMY, 11,
		["onmyou_orb", "kanbei_scroll"], Color(0.51, 0.84, 0.61),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_ph1"] = _u("pe_ph1", "Phantom Knight", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 10,
		["muramasa", "onmyou_orb"], Color(0.29, 0.29, 0.45),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["pe_we1"] = _u("pe_we1", "War Elephant", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 11,
		["steel_tetsubo", "steel_yari"], Color(0.33, 0.25, 0.20),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_yam1"] = _u("e_yam1", "Yamabushi", Constants.CLASS_MONK, Constants.Faction.ENEMY, 4,
		["iron_naginata", "ofuda"], Color(0.43, 0.27, 0.14),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_yam2"] = _u("e_yam2", "Elder Yamabushi", Constants.CLASS_MONK, Constants.Faction.ENEMY, 7,
		["steel_naginata", "shakujo"], Color(0.39, 0.24, 0.10),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_miko1"] = _u("e_miko1", "Shrine Maiden", Constants.CLASS_MONK, Constants.Faction.ENEMY, 3,
		["heal_staff", "iron_bow"], Color(1.00, 0.82, 0.82),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_nom1"] = _u("e_nom1", "Nomad Rider", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 4,
		["iron_bow", "iron_tanto"], Color(0.67, 0.59, 0.35),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_nom2"] = _u("e_nom2", "Nomad Scout", Constants.CLASS_CAVALRY, Constants.Faction.ENEMY, 6,
		["steel_bow", "iron_tanto"], Color(0.63, 0.55, 0.31),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_fgd1"] = _u("e_fgd1", "Foot Guard", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 4,
		["iron_yari", "iron_tetsubo"], Color(0.59, 0.59, 0.51),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_fgd2"] = _u("e_fgd2", "Iron Foot Guard", Constants.CLASS_GENERAL, Constants.Faction.ENEMY, 7,
		["steel_yari", "steel_tetsubo"], Color(0.55, 0.55, 0.47),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_mush1"] = _u("e_mush1", "Wandering Musha", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 4,
		["iron_katana", "iron_yari"], Color(0.43, 0.35, 0.27),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_mush2"] = _u("e_mush2", "Veteran Musha", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 7,
		["steel_katana", "steel_yari"], Color(0.39, 0.31, 0.24),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_yoji1"] = _u("e_yoji1", "Yojimbo", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 5,
		["steel_katana"], Color(0.29, 0.29, 0.22),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_yoji2"] = _u("e_yoji2", "Master Yojimbo", Constants.CLASS_SAMURAI, Constants.Faction.ENEMY, 8,
		["steel_katana", "steel_nodachi"], Color(0.25, 0.25, 0.18),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_rogue1"] = _u("e_rogue1", "Outlaw", Constants.CLASS_NINJA, Constants.Faction.ENEMY, 3,
		["iron_tanto", "iron_chain"], Color(0.22, 0.18, 0.14),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_rogue2"] = _u("e_rogue2", "Bandit Rogue", Constants.CLASS_NINJA, Constants.Faction.ENEMY, 5,
		["steel_tanto", "iron_chain"], Color(0.18, 0.14, 0.10),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_kenin1"] = _u("e_kenin1", "Young Retainer", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 1,
		["iron_katana"], Color(0.51, 0.59, 0.71),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_kenin2"] = _u("e_kenin2", "Retainer", Constants.CLASS_ASHIGARU, Constants.Faction.ENEMY, 3,
		["iron_katana"], Color(0.47, 0.55, 0.67),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ssol1"] = _u("e_ssol1", "Sea Soldier", Constants.CLASS_PIRATE, Constants.Faction.ENEMY, 4,
		["iron_katana", "iron_yari"], Color(0.20, 0.27, 0.51),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_ssol2"] = _u("e_ssol2", "Sea Veteran", Constants.CLASS_PIRATE, Constants.Faction.ENEMY, 6,
		["steel_katana", "steel_yari"], Color(0.16, 0.24, 0.47),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_blm1"] = _u("e_blm1", "Blade Monk", Constants.CLASS_MONK, Constants.Faction.ENEMY, 4,
		["iron_katana", "iron_naginata"], Color(0.59, 0.35, 0.20),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["e_blm2"] = _u("e_blm2", "Sword Monk", Constants.CLASS_MONK, Constants.Faction.ENEMY, 7,
		["steel_katana", "steel_naginata"], Color(0.55, 0.31, 0.16),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_yam1"] = _u("oda_yam1", "Oda Yamabushi", Constants.CLASS_MONK, Constants.Faction.PLAYER, 3,
		["iron_naginata", "ofuda"], Color(0.43, 0.27, 0.14),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_miko1"] = _u("oda_miko1", "Oda Miko", Constants.CLASS_MONK, Constants.Faction.PLAYER, 3,
		["heal_staff", "iron_bow"], Color(1.00, 0.82, 0.82),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_mush1"] = _u("oda_mush1", "Oda Musha", Constants.CLASS_SAMURAI, Constants.Faction.PLAYER, 3,
		["iron_katana", "iron_yari"], Color(0.43, 0.35, 0.27),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_fgd1"] = _u("oda_fgd1", "Oda Foot Guard", Constants.CLASS_GENERAL, Constants.Faction.PLAYER, 3,
		["iron_yari", "iron_tetsubo"], Color(0.59, 0.59, 0.51),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	units["oda_blm1"] = _u("oda_blm1", "Oda Blade Monk", Constants.CLASS_MONK, Constants.Faction.PLAYER, 3,
		["iron_katana", "iron_naginata"], Color(0.59, 0.35, 0.20),
		"A soldier of the age.",
		"",
		false, false, [],
		{"hp":50,"str":40,"mag":30,"skl":45,"spd":45,"lck":35,"def":35,"res":25})

	return units


static func _u(id: String, uname: String, cls: String, faction: int, level: int,
		weapon_ids: Array, col: Color, bio: String, quote: String,
		is_boss: bool, can_recruit: bool, recruit_by: Array,
		growths: Dictionary) -> UnitData:
	var u := UnitData.new()
	u.unit_id = id
	u.name = uname
	u.unit_class = cls
	u.faction = faction
	u.level = level
	u.color = col
	u.bio = bio
	u.portrait_quote = quote
	u.is_boss = is_boss
	u.can_recruit = can_recruit
	for rid in recruit_by:
		u.recruit_by.append(rid)
	u.symbol = Constants.CLASS_SYMBOLS.get(cls, "\u2605")
	# Growth rates
	u.growth_hp = growths.get("hp", 50)
	u.growth_str = growths.get("str", 40)
	u.growth_mag = growths.get("mag", 20)
	u.growth_skl = growths.get("skl", 40)
	u.growth_spd = growths.get("spd", 40)
	u.growth_lck = growths.get("lck", 30)
	u.growth_def = growths.get("def", 30)
	u.growth_res = growths.get("res", 20)
	# Load weapons
	for wid in weapon_ids:
		var w := WeaponData.get_weapon(wid)
		if not w.is_empty():
			u.weapons.append(w)
	# Compute base stats from level (simplified)
	var base_hp := 20
	var base_str := 5
	var base_mag := 2
	var base_skl := 5
	var base_spd := 5
	var base_lck := 3
	var base_def := 3
	var base_res := 2
	var base_mov := 5
	# Class-based stat adjustments
	match cls:
		Constants.CLASS_LORD:
			base_hp = 40; base_str = 14; base_mag = 4; base_skl = 12
			base_spd = 10; base_lck = 8; base_def = 12; base_res = 6; base_mov = 6
		Constants.CLASS_SAMURAI:
			base_hp = 32; base_str = 11; base_mag = 2; base_skl = 10
			base_spd = 9; base_lck = 5; base_def = 8; base_res = 3; base_mov = 5
		Constants.CLASS_ASHIGARU:
			base_hp = 28; base_str = 8; base_mag = 0; base_skl = 6
			base_spd = 6; base_lck = 5; base_def = 6; base_res = 2; base_mov = 4
		Constants.CLASS_ARCHER:
			base_hp = 25; base_str = 9; base_mag = 0; base_skl = 12
			base_spd = 8; base_lck = 6; base_def = 5; base_res = 2; base_mov = 5
		Constants.CLASS_CAVALRY:
			base_hp = 30; base_str = 12; base_mag = 0; base_skl = 8
			base_spd = 10; base_lck = 5; base_def = 9; base_res = 2; base_mov = 8
		Constants.CLASS_NINJA:
			base_hp = 22; base_str = 10; base_mag = 3; base_skl = 14
			base_spd = 14; base_lck = 8; base_def = 4; base_res = 5; base_mov = 6
		Constants.CLASS_MONK:
			base_hp = 24; base_str = 5; base_mag = 12; base_skl = 8
			base_spd = 7; base_lck = 9; base_def = 4; base_res = 10; base_mov = 5
		Constants.CLASS_ONMYOJI:
			base_hp = 20; base_str = 3; base_mag = 15; base_skl = 10
			base_spd = 8; base_lck = 10; base_def = 3; base_res = 14; base_mov = 5
		Constants.CLASS_NOBLE_LADY:
			base_hp = 20; base_str = 5; base_mag = 10; base_skl = 10
			base_spd = 11; base_lck = 14; base_def = 3; base_res = 12; base_mov = 5
		Constants.CLASS_GUNNER:
			base_hp = 26; base_str = 11; base_mag = 2; base_skl = 10
			base_spd = 6; base_lck = 5; base_def = 6; base_res = 3; base_mov = 4
		Constants.CLASS_GENERAL:
			base_hp = 46; base_str = 13; base_mag = 0; base_skl = 8
			base_spd = 5; base_lck = 4; base_def = 18; base_res = 6; base_mov = 4
		Constants.CLASS_PEGASUS:
			base_hp = 24; base_str = 10; base_mag = 6; base_skl = 13
			base_spd = 14; base_lck = 9; base_def = 5; base_res = 10; base_mov = 7
		Constants.CLASS_WYVERN:
			base_hp = 34; base_str = 15; base_mag = 0; base_skl = 10
			base_spd = 9; base_lck = 4; base_def = 13; base_res = 4; base_mov = 7
		Constants.CLASS_PIRATE:
			base_hp = 30; base_str = 12; base_mag = 0; base_skl = 8
			base_spd = 10; base_lck = 6; base_def = 7; base_res = 4; base_mov = 5
	var scale := level - 1
	u.max_hp = base_hp + scale * 2
	u.hp = u.max_hp
	u.str_ = base_str + scale
	u.mag = base_mag + scale
	u.skl = base_skl + scale
	u.spd = base_spd + scale
	u.lck = base_lck + scale
	u.def_ = base_def + scale
	u.res = base_res + scale
	u.mov = base_mov
	return u


static func create_mercenary(merc_id: String, _chapter: int = 0) -> UnitData:
	var level := 1 + _chapter / 4
	var defs := {
		"merc_ashigaru": ["Hired Ashigaru", Constants.CLASS_ASHIGARU, ["iron_yari", "iron_tanto"], Color(0.47, 0.39, 0.31)],
		"merc_spearman": ["Hired Spearman", Constants.CLASS_ASHIGARU, ["iron_yari", "iron_naginata"], Color(0.47, 0.43, 0.35)],
		"merc_archer": ["Hired Archer", Constants.CLASS_ARCHER, ["iron_bow", "iron_tanto"], Color(0.39, 0.51, 0.31)],
		"merc_samurai": ["Hired Samurai", Constants.CLASS_SAMURAI, ["iron_katana", "iron_tanto"], Color(0.43, 0.35, 0.24)],
		"merc_cavalry": ["Hired Cavalry", Constants.CLASS_CAVALRY, ["iron_yari", "iron_katana"], Color(0.35, 0.39, 0.51)],
		"merc_ninja": ["Hired Ninja", Constants.CLASS_NINJA, ["iron_tanto", "iron_chain"], Color(0.24, 0.24, 0.31)],
		"merc_monk": ["Hired Monk", Constants.CLASS_MONK, ["heal_staff", "iron_tanto"], Color(0.78, 0.71, 0.55)],
		"merc_gunner": ["Hired Gunner", Constants.CLASS_GUNNER, ["tanegashima", "iron_tanto"], Color(0.51, 0.47, 0.35)],
	}
	if not defs.has(merc_id):
		push_error("Unknown merc: %s" % merc_id)
		return null
	var d: Array = defs[merc_id]
	var u := _u(merc_id, d[0], d[1], Constants.Faction.PLAYER, level,
		d[2], d[3], "A mercenary hired for this campaign.", "",
		false, false, [],
		{"hp":65,"str":30,"mag":20,"skl":30,"spd":30,"lck":20,"def":28,"res":20})
	# Mercs are weaker
	u.max_hp = max(8, u.max_hp - 4)
	u.hp = u.max_hp
	u.str_ = max(2, u.str_ - 2)
	u.mag = max(1, u.mag - 1)
	u.skl = max(2, u.skl - 2)
	u.spd = max(2, u.spd - 2)
	u.def_ = max(1, u.def_ - 2)
	u.res = max(1, u.res - 1)
	return u
