'''
Prologue dialogue for Sengoku Tactics: Age of the Warring States.
A multi-slide historical intro explaining Japan's Sengoku era that runs
once when the player starts a new game, just before the tutorial or Chapter 1.

Each slide: (speaker_key, display_name, text)
speaker_key controls portrait colour (uses PORTRAIT_COLORS from scene_dialogs).
Use speaker_key "" for a narrator/omniscient voice.
'''

PROLOGUE_SLIDES = [
    # ── Slide 1: The Land ─────────────────────────────────────────────────────
    ("narrator", "Narrator",
     "Japan. An island nation cradled between mountains and sea.\n"
     "For centuries its people cultivated rice, poetry, and war\n"
     "with equal devotion. Then the old order shattered."),

    # ── Slide 2: The Shogunate's Collapse ────────────────────────────────────
    ("narrator", "Narrator",
     "The Ashikaga Shogunate — once the supreme military government —\n"
     "collapsed into civil war after the Onin War of 1467.\n"
     "For over a century, Japan had no true ruler. Only warlords."),

    # ── Slide 3: The Sengoku Jidai ────────────────────────────────────────────
    ("narrator", "Narrator",
     "This age was called the SENGOKU JIDAI — the Age of the\n"
     "Country at War. Every province bled. Every clan raised banners.\n"
     "To be born samurai was to be born into unending conflict."),

    # ── Slide 4: The Great Powers ─────────────────────────────────────────────
    ("narrator", "Narrator",
     "From this chaos, powerful lords emerged:\n"
     "Takeda Shingen — 'The Tiger of Kai' — commanded the most\n"
     "feared cavalry in Japan. He had never lost a battle."),

    ("narrator", "Narrator",
     "Uesugi Kenshin — 'The Dragon of Echigo' — fought for honour\n"
     "above profit. He sent salt to his enemies when they were embargoed.\n"
     "He and Shingen clashed five times at Kawanakajima. Neither won."),

    ("narrator", "Narrator",
     "Mori Motonari — master of strategy, lord of eight provinces —\n"
     "united western Japan through brilliance and patience.\n"
     "He told his sons: a single arrow breaks — three together, never."),

    ("narrator", "Narrator",
     "The Imagawa clan marched 25,000 strong toward the capital,\n"
     "holding the richest domains in central Japan.\n"
     "Between them and Kyoto stood one small, 'mad' lord."),

    # ── Slide 5: Nobunaga Enters ──────────────────────────────────────────────
    ("nobunaga", "Oda Nobunaga",
     "Oda Nobunaga — called the Demon King, called the Fool of Owari.\n"
     "He was 26 years old. His army numbered two thousand.\n"
     "He danced. He laughed. He was not afraid."),

    ("narrator", "Narrator",
     "Nobunaga was different from every lord before him.\n"
     "He despised tradition when tradition was inefficient.\n"
     "He embraced guns, trade, and commoners when lords scorned all three."),

    # ── Slide 6: The Key Figures ──────────────────────────────────────────────
    ("hideyoshi", "Toyotomi Hideyoshi",
     "By his side: Toyotomi Hideyoshi — born a peasant's son,\n"
     "risen to sandal-bearer, now the sharpest mind in the army.\n"
     "He would one day rule all Japan. For now, he served."),

    ("mitsuhide", "Akechi Mitsuhide",
     "And Akechi Mitsuhide — cultured, brilliant, deeply loyal.\n"
     "A man who loved order and tradition. Who served Nobunaga faithfully\n"
     "for years. Who harbored one thing: wounded pride."),

    # ── Slide 7: The Samurai Code ─────────────────────────────────────────────
    ("narrator", "Narrator",
     "In this world, the samurai code — BUSHIDO — shaped every decision.\n"
     "Loyalty unto death. Honor above survival.\n"
     "A samurai who surrendered shamed his entire clan."),

    ("narrator", "Narrator",
     "But Nobunaga cared little for ceremony.\n"
     "He trained ashigaru — foot soldiers, peasants — to hold rifles\n"
     "and stand firm against cavalry. This was heresy. It was also genius."),

    # ── Slide 8: What is at Stake ─────────────────────────────────────────────
    ("narrator", "Narrator",
     "To control Japan, a lord needed to hold Kyoto — the capital —\n"
     "and install a Shogun loyal to their cause.\n"
     "The Imagawa were marching there now. Someone had to stop them."),

    # ── Slide 9: The Promise ──────────────────────────────────────────────────
    ("nobunaga", "Oda Nobunaga",
     "'Human life is fifty years. Compared to the span of heaven\n"
     "and earth, it is like a dream or an illusion.\n"
     "Is there anything that lasts forever?'"),

    ("nobunaga", "Oda Nobunaga",
     "He danced the ancient war-song Atsumori\n"
     "— then rode out into the storm.\n"
     "The age of Oda Nobunaga had begun."),

    # ── Slide 10: Transition to Game ─────────────────────────────────────────
    ("narrator", "Narrator",
     "You now take command. Guide Nobunaga's forces through 20 chapters\n"
     "of the Sengoku era — from the miracle of Okehazama\n"
     "to the final fire of Osaka Castle."),

    ("narrator", "Narrator",
     "Build your army. Choose your officers carefully.\n"
     "Train them, promote them, and forge alliances.\n"
     "The destiny of Japan rests on your decisions."),
]

# Portrait colours for prologue speakers (used by renderer)
PROLOGUE_PORTRAIT_COLORS = {
    "narrator":  (30, 30, 55),
    "nobunaga":  (160, 50, 20),
    "hideyoshi": (170, 130, 30),
    "mitsuhide": (60, 60, 130),
}
