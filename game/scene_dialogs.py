'''
Pre-battle scene dialogs for each chapter.
Each entry is a list of (speaker, line) tuples.
Speaker names are used by the renderer to colour portrait boxes and
look up the speaking unit's faction for framing.

Narrative arc:
  Ch 1–5   : Nobunaga's rise — Okehazama, Kawanakajima, Honnoji betrayal,
              Hideyoshi's survival and first reckoning at Sekigahara.
  Ch 6–10  : The Oda machine — Inabayama, Anegawa, Nagashima, Nagashino.
  Ch 11–13 : Western campaign, flood-siege, Yamazaki revenge.
  Ch 14–16 : Shibata feud, Komaki war, Odawara fall — Hideyoshi supreme.
  Ch 17–20 : Ieyasu's gamble, Sekigahara, Osaka sieges, final blaze.

Portrait colours are kept here so the renderer can paint them without
needing the full unit roster.
'''

# Speaker → (R, G, B) portrait background tint
PORTRAIT_COLORS = {
    "nobunaga":   (120,  30,  10),
    "hideyoshi":  ( 80, 120,  20),
    "ieyasu":     ( 20,  60, 120),
    "mitsuhide":  ( 50,  50, 140),
    "katsuie":    (140,  60,  10),
    "toshiie":    (100,  80,  30),
    "ranmaru":    (160, 100,  20),
    "nene":       (160,  60, 120),
    "chacha":     (200, 100, 140),
    "kenshin":    ( 10,  80, 140),
    "shingen":    (140,  10,  10),
    "kansuke":    ( 80,  20,  80),
    "kanetsugu":  ( 30,  90, 140),
    "yoshimoto":  ( 80,  80,   0),
    "yukimura":   (180,  30,  10),
    "masayuki":   (120,  20,  60),
    "tadakatsu":  ( 20,  80, 160),
    "naomasa":    ( 20, 120, 100),
    "motonari":   ( 30, 100,  60),
    "ekei":       ( 60,  40, 100),
    "tsuruhime":  (160,  80, 160),
    "hanbei":     ( 80, 160, 100),
    "kanbei":     ( 40, 100, 140),
    "yoshitsune": (200, 160,  20),
    "ii_naotora": (180,  20,  20),
    "matsunaga":  ( 60,  20,  80),
    "nagahide":   (100,  80,  30),
    "katsuie":    (140,  60,  10),
    "toshiie":    (100,  90,  20),
    "masayuki":   (120,  20,  60),
    "nobushige":  (160,  40,  20),
    "katsuyori":  (140,  20,  20),
    "narrator":   ( 30,  30,  50),
    "unknown":    ( 40,  40,  40),
}

def _pc(name):
    return PORTRAIT_COLORS.get(name, (60, 60, 80))


# ─── Chapter scene dialogs ────────────────────────────────────────────────────
# Each scene is a list of (speaker_key, display_name, line_of_dialogue)
# speaker_key must match PORTRAIT_COLORS keys.

CHAPTER_SCENES = [

    # ── Chapter 1 · Departure from Owari ─────────────────────────────────────
    [
        ("narrator",   "Narrator",
         "Year 1560. The Imagawa clan marches 25,000 soldiers toward Kyoto."),
        ("narrator",   "Narrator",
         "Their path leads through Owari — domain of Oda Nobunaga, a lord\n"
         "his own retainers call 'The Fool of Owari.'"),
        ("hideyoshi",  "Hideyoshi",
         "My lord... scouts report forty battalions. Our walls hold two thousand,\n"
         "if we count the cooks and stable boys."),
        ("nobunaga",   "Nobunaga",
         "Human life is fifty years — compared to the span of heaven, it is\n"
         "nothing but a fleeting dream. I refuse to hide behind walls!"),
        ("ranmaru",    "Ranmaru",
         "Then... we charge, my lord? Into forty thousand?"),
        ("nobunaga",   "Nobunaga",
         "We charge. Destiny does not wait for the timid. ALL MEN — MOVE OUT!"),
    ],

    # ── Chapter 2 · Storm of Okehazama ───────────────────────────────────────
    [
        ("narrator",   "Narrator",
         "The Imagawa vanguard camps in the forest gully of Okehazama.\n"
         "Yoshimoto takes tea, certain of his conquest. A summer storm builds."),
        ("mitsuhide",  "Mitsuhide",
         "My lord, the storm will mask our approach. Two thousand men against\n"
         "the Imagawa's ten-fold strength... this is either genius or madness."),
        ("nobunaga",   "Nobunaga",
         "History remembers neither cowards nor the cautious, Mitsuhide.\n"
         "It remembers those who act."),
        ("yoshimoto",  "Yoshimoto",
         "[unaware, in his camp]  Another cup of tea. We march on Kyoto\n"
         "at dawn. Nobunaga is a nuisance — nothing more."),
        ("hideyoshi",  "Hideyoshi",
         "The thunder — it's deafening! They won't hear us until we're\n"
         "inside the camp. My lord, this is actually going to work!"),
        ("nobunaga",   "Nobunaga",
         "Of course it will. CHARGE — and do not stop until Yoshimoto's\n"
         "head rests at my feet!"),
    ],

    # ── Chapter 3 · Kawanakajima — Dragon and Tiger ──────────────────────────
    [
        ("narrator",   "Narrator",
         "1561. The plain of Kawanakajima. The Dragon of Echigo — Uesugi\n"
         "Kenshin — descends from the north for the fourth time."),
        ("narrator",   "Narrator",
         "From the south comes the Tiger of Kai — Takeda Shingen.\n"
         "Between them, a third force watches in silence."),
        ("kenshin",    "Kenshin",
         "Shingen. I have sworn to the god Bishamonten that I will not rest\n"
         "while your ambition devours the realm."),
        ("shingen",    "Shingen",
         "Pretty words for a man who has never taken a single castle\n"
         "from me. Come then, monk. Let us settle this."),
        ("nobunaga",   "Nobunaga",
         "[observing from a ridge]  Let them exhaust each other.\n"
         "Then the Oda will inherit what remains."),
        ("mitsuhide",  "Mitsuhide",
         "And if they unite against us instead, my lord?"),
        ("nobunaga",   "Nobunaga",
         "Then we fight both. I was born for this age, Mitsuhide.\n"
         "Now — hold our position and wait for my signal."),
    ],

    # ── Chapter 4 · The Flames of Honnoji ────────────────────────────────────
    [
        ("narrator",   "Narrator",
         "June 1582. Nobunaga rests at Honnoji temple in Kyoto,\n"
         "almost alone — his unification of Japan nearly complete."),
        ("mitsuhide",  "Mitsuhide",
         "[outside the burning temple]  Forgive me, my lord. What I do now\n"
         "I do for the realm — not for ambition."),
        ("nobunaga",   "Nobunaga",
         "[inside, hearing the commotion]  ...Mitsuhide? So. The fox bares\n"
         "its teeth at last. Very well. This is fine."),
        ("ranmaru",    "Ranmaru",
         "My lord — we are surrounded! Please, escape through the—"),
        ("nobunaga",   "Nobunaga",
         "No. A man lives fifty years. I have lived mine fully.\n"
         "Ranmaru — protect yourself. That is an order."),
        ("mitsuhide",  "Mitsuhide",
         "[grimly]  Nobunaga... even now you face death without flinching.\n"
         "This deed will haunt me. But it must be done."),
    ],

    # ── Chapter 5 · Sekigahara — The First Reckoning ─────────────────────────
    [
        ("narrator",   "Narrator",
         "Nobunaga is gone. His greatest general — Hideyoshi — races\n"
         "back from the west. He reaches Yamazaki first."),
        ("hideyoshi",  "Hideyoshi",
         "Mitsuhide waited thirteen years for his chance at the throne.\n"
         "He held it for thirteen days."),
        ("nene",       "Nene",
         "Hideyoshi... you grieve too. I see it. Nobunaga was cruel\n"
         "and magnificent and impossible — and he was yours to serve."),
        ("hideyoshi",  "Hideyoshi",
         "I grieve later. Right now I avenge him.\n"
         "Every Shimazu blade between us and Mitsuhide — cut it down."),
        ("mitsuhide",  "Mitsuhide",
         "[rallying what forces remain]  Hideyoshi moves impossibly fast.\n"
         "I underestimated the Monkey. I will not survive this day."),
        ("hideyoshi",  "Hideyoshi",
         "To all men! The Oda lives through us! FORWARD!"),
    ],

    # ── Chapter 6 · Siege of Inabayama ───────────────────────────────────────
    [
        ("narrator",   "Narrator",
         "Years earlier — 1567. Inabayama Castle, stronghold of the Saito\n"
         "clan, perches atop Mount Kinka like an eagle's nest."),
        ("hanbei",     "Hanbei",
         "I have studied Inabayama's walls for three months, Lord Nobunaga.\n"
         "There is a path — steep, treacherous, and completely unguarded."),
        ("nobunaga",   "Nobunaga",
         "Of course there is. That is why I hired you, Hanbei.\n"
         "Show Hideyoshi. He enjoys climbing things."),
        ("hideyoshi",  "Hideyoshi",
         "...I enjoy climbing things?"),
        ("hanbei",     "Hanbei",
         "Once Inabayama falls, the road to central Japan opens.\n"
         "Lord Nobunaga, this is the first true step toward Tenka Fubu."),
        ("nobunaga",   "Nobunaga",
         "Rule all under heaven by force. Yes. Begin."),
    ],

    # ── Chapter 7 · The Betrayal at Anegawa ──────────────────────────────────
    [
        ("narrator",   "Narrator",
         "1570. The Asai and Asakura clans — once Nobunaga's allies —\n"
         "reveal their true colours and march to destroy him."),
        ("nagahide",   "Nagahide",
         "Lord Nobunaga — the Asai have broken the alliance!\n"
         "Nagamasa himself leads their vanguard across the Ane River!"),
        ("nobunaga",   "Nobunaga",
         "My sister's husband turns his blade on me. Ha.\n"
         "A man's family is his greatest blindspot. Noted."),
        ("ieyasu",     "Ieyasu",
         "My forces will hold the Tokugawa flank. The river crossing\n"
         "is treacherous — we must not let them encircle us."),
        ("katsuie",    "Katsuie",
         "I'll take the Shibata heavy infantry straight into their centre.\n"
         "Give me the order, my lord — I'll break them in one charge!"),
        ("nobunaga",   "Nobunaga",
         "Then do it, Katsuie. Ieyasu — keep the Asakura off our flank.\n"
         "Today we remind them why the Oda does not forgive betrayal."),
    ],

    # ── Chapter 8 · The Ikko-Ikki at Nagashima ───────────────────────────────
    [
        ("narrator",   "Narrator",
         "The Ikko-Ikki — warrior monks and peasant faithful — have turned\n"
         "the island fortress of Nagashima into an impregnable thorn\n"
         "in the side of Oda expansion."),
        ("ekei",       "Ankokuji Ekei",
         "The Pure Land faithful will not bend to a demon lord.\n"
         "These walls have held three Oda assaults already."),
        ("nobunaga",   "Nobunaga",
         "The Buddha does not protect forts. I do not negotiate\n"
         "with those who shoot at my messengers."),
        ("mitsuhide",  "Mitsuhide",
         "My lord — the monks fight with fearless conviction.\n"
         "They believe dying in battle earns paradise."),
        ("nobunaga",   "Nobunaga",
         "Then we are doing them a favour. Burn the outer palisades.\n"
         "Every boat on the river is mine. They will not resupply."),
        ("ranmaru",    "Ranmaru",
         "Understood, my lord. The island will be ours before the\n"
         "autumn rains. I swear it on my honour."),
    ],

    # ── Chapter 9 · Relief of Nagashino Castle ────────────────────────────────
    [
        ("narrator",   "Narrator",
         "1575. Takeda Katsuyori — son of the great Shingen — lays siege\n"
         "to Nagashino Castle. Inside: five hundred starving men."),
        ("narrator",   "Narrator",
         "A lone messenger, Torii Suneemon, swims the Takigawa River\n"
         "and runs thirty miles to reach Nobunaga. He will die for it."),
        ("ieyasu",     "Ieyasu",
         "Nagashino cannot hold another week, my lord.\n"
         "Katsuyori has thirty thousand cavalry. We have twelve."),
        ("nobunaga",   "Nobunaga",
         "Numbers are not the question. Position is the question.\n"
         "I need that river line and three thousand arquebusiers."),
        ("katsuie",    "Katsuie",
         "The Takeda cavalry are the finest in Japan. They will simply\n"
         "ride through your musketeers before they can reload."),
        ("nobunaga",   "Nobunaga",
         "Not if the musketeers fire in rotating volleys.\n"
         "Three lines. One fires — steps back — the next fires.\n"
         "We will not give the horses a moment to close. Trust the plan."),
    ],

    # ── Chapter 10 · Nagashino — The Volley Line ─────────────────────────────
    [
        ("narrator",   "Narrator",
         "21 May, 1575. Behind a palisade wall on the Shidarahara plain,\n"
         "three thousand matchlock arquebuses are loaded and waiting."),
        ("yukimura",   "Sanada Yukimura",
         "Father — the Oda line is strange. They have built a fence.\n"
         "A fence against the Takeda cavalry? It is an insult."),
        ("masayuki",   "Sanada Masayuki",
         "It is a trap. Do not let Katsuyori charge. We must—"),
        ("narrator",   "Narrator",
         "But Katsuyori is already riding. The thunder of hooves\n"
         "shakes the earth. The Takeda cavalry — undefeated for decades."),
        ("nobunaga",   "Nobunaga",
         "...FIRE!"),
        ("narrator",   "Narrator",
         "The volley line speaks. Again. Again. The age of cavalry\n"
         "supremacy ends in smoke and gunpowder at Nagashino."),
    ],

    # ── Chapter 11 · Conquest of the West — Mori Campaign ────────────────────
    [
        ("narrator",   "Narrator",
         "With eastern rivals weakened, Nobunaga turns west.\n"
         "The Mori clan — masters of the Inland Sea — stand in his path."),
        ("motonari",   "Mori Terumoto",
         "My grandfather Motonari carved this domain from nothing.\n"
         "I will not surrender a single province to the Fool of Owari."),
        ("kanbei",     "Kuroda Kanbei",
         "Lord Hideyoshi — the Mori fleet controls the supply lines\n"
         "to Miki Castle. Our besieging force will starve before they do."),
        ("hideyoshi",  "Hideyoshi",
         "Then we build our own fleet. And we win the sea battle\n"
         "before we win the land battle."),
        ("ekei",       "Ankokuji Ekei",
         "[as Mori envoy]  The Mori have ruled the west for sixty years.\n"
         "What makes you think this time will be different, Monkey?"),
        ("hideyoshi",  "Hideyoshi",
         "Because this time, I have guns bigger than your pride.\n"
         "Tell Terumoto — surrender or starve. His choice."),
    ],

    # ── Chapter 12 · The Flooded Castle — Takamatsu ──────────────────────────
    [
        ("narrator",   "Narrator",
         "Takamatsu Castle sits in a bowl of plains, surrounded by rivers.\n"
         "Kanbei studies the terrain for one day, then smiles."),
        ("kanbei",     "Kuroda Kanbei",
         "My lord Hideyoshi — we do not need to storm Takamatsu.\n"
         "We need only to drown it."),
        ("hideyoshi",  "Hideyoshi",
         "...Drown it?"),
        ("kanbei",     "Kuroda Kanbei",
         "Three weeks of earthwork dikes. Redirect the river.\n"
         "The castle becomes an island. Their rice rots in the flood.\n"
         "They surrender — or we leave them to the fish."),
        ("motonari",   "Mori Terumoto",
         "[inside Takamatsu]  The water rises daily. Shimizu Muneharu\n"
         "refuses to surrender. He says he will give his life for us."),
        ("hideyoshi",  "Hideyoshi",
         "Then hold the dikes. This war ends in water, not fire."),
    ],

    # ── Chapter 13 · Yamazaki — The Monkey's Revenge ─────────────────────────
    [
        ("narrator",   "Narrator",
         "June 2nd, 1582. Honnoji burns. Nobunaga is gone.\n"
         "The news reaches Hideyoshi at Takamatsu in hours."),
        ("hideyoshi",  "Hideyoshi",
         "..."),
        ("kanbei",     "Kuroda Kanbei",
         "My lord. This is the moment. Make peace with the Mori today —\n"
         "any terms they ask. And race back east. The realm is leaderless."),
        ("hideyoshi",  "Hideyoshi",
         "You want me to weep later. I understand.\n"
         "[straightens]  Call the commanders. We march before dawn."),
        ("mitsuhide",  "Mitsuhide",
         "[at Yamazaki]  Hideyoshi... he covered two hundred li in eight days.\n"
         "I have thirteen days. I had thirteen days..."),
        ("hideyoshi",  "Hideyoshi",
         "For Nobunaga — for the realm — and yes, for myself.\n"
         "Mitsuhide! You will answer for Honnoji on this hill!"),
    ],

    # ── Chapter 14 · The Battle of Shizugatake ────────────────────────────────
    [
        ("narrator",   "Narrator",
         "1583. The Oda succession is contested. Katsuie backs young\n"
         "Nobutaka against Hideyoshi's chosen heir, Samboshi."),
        ("katsuie",    "Shibata Katsuie",
         "I served Nobunaga for thirty years. I will not bow to his\n"
         "sandal-bearer. Hideyoshi is NOT the Oda successor!"),
        ("hideyoshi",  "Hideyoshi",
         "Katsuie — you are a great warrior. But great warriors do\n"
         "not always make great leaders. Step aside."),
        ("katsuie",    "Shibata Katsuie",
         "I have never stepped aside from anything in my life.\n"
         "Come then, Monkey! Let steel decide it!"),
        ("toshiie",    "Maeda Toshiie",
         "[torn]  Katsuie is my lord. Hideyoshi is my friend.\n"
         "Today I may be forced to choose between them..."),
        ("hideyoshi",  "Hideyoshi",
         "Toshiie — I do not ask you to betray Katsuie.\n"
         "I ask you only to remember what Nobunaga would have wanted."),
    ],

    # ── Chapter 15 · Komaki-Nagakute — War of Patience ───────────────────────
    [
        ("narrator",   "Narrator",
         "1584. Ieyasu and Nobukatsu challenge Hideyoshi's supremacy.\n"
         "Two great tacticians face each other at Komaki — and wait."),
        ("ieyasu",     "Tokugawa Ieyasu",
         "Hideyoshi rushes everything. His strength is speed and numbers.\n"
         "Take both away from him and the Monkey has no tricks left."),
        ("tadakatsu",  "Honda Tadakatsu",
         "My lord, the Toyotomi flank moves south — they are trying\n"
         "to outmanoeuvre us toward Nagakute."),
        ("ieyasu",     "Tokugawa Ieyasu",
         "Then Nagakute is where we meet them. I want Naomasa's\n"
         "Red Devils on the left — and nobody charges until I say."),
        ("hideyoshi",  "Hideyoshi",
         "Ieyasu. You always were the most cautious man in Japan.\n"
         "But patience has a limit. Push the flanks — now!"),
        ("ieyasu",     "Tokugawa Ieyasu",
         "This battle will not be won in a day.\n"
         "I can wait. I have always been good at waiting."),
    ],

    # ── Chapter 16 · The Fall of Odawara ─────────────────────────────────────
    [
        ("narrator",   "Narrator",
         "1590. Hideyoshi's last great campaign — the siege of Odawara,\n"
         "impregnable fortress of the Hojo clan. He brings 200,000 men."),
        ("hideyoshi",  "Hideyoshi",
         "The Hojo believe their walls are eternal. They held off the\n"
         "Takeda. They held off Uesugi Kenshin. They will not hold me."),
        ("nene",       "Nene",
         "You plan to simply... wait them out?"),
        ("hideyoshi",  "Hideyoshi",
         "I plan to build a castle overnight on the hill overlooking them,\n"
         "throw a party inside it loud enough for them to hear,\n"
         "and let despair do the fighting for me."),
        ("nene",       "Nene",
         "That is the most absurd strategy I have ever heard.\n"
         "...It will absolutely work, won't it."),
        ("hideyoshi",  "Hideyoshi",
         "Odawara falls. Japan is unified. And then...\n"
         "[pause]  Then I will make a terrible mistake in Korea.\n"
         "But that is a problem for tomorrow."),
    ],

    # ── Chapter 17 · Defense of Fushimi ──────────────────────────────────────
    [
        ("narrator",   "Narrator",
         "1598. Toyotomi Hideyoshi is dying. He whispers to Ieyasu:\n"
         "'I leave my son Hideyori in your hands. Please. Care for him.'"),
        ("narrator",   "Narrator",
         "Ieyasu bows. He will not keep this promise.\n"
         "The realm holds its breath."),
        ("ieyasu",     "Tokugawa Ieyasu",
         "Fushimi Castle. The symbol of Toyotomi power.\n"
         "Mitsunari's loyalists will come for it. We must be ready."),
        ("tadakatsu",  "Honda Tadakatsu",
         "My lord — our garrison is eight hundred against their thousands.\n"
         "Fushimi cannot hold indefinitely."),
        ("ieyasu",     "Tokugawa Ieyasu",
         "It does not need to hold indefinitely. It needs to hold long\n"
         "enough to force the western lords to show their allegiances."),
        ("ii_naotora", "Ii Naotora",
         "Then the Red Devils of Ii will hold this wall until the\n"
         "last stone. Give the order, Lord Ieyasu. We do not retreat."),
    ],

    # ── Chapter 18 · Sekigahara — The Great Battle ───────────────────────────
    [
        ("narrator",   "Narrator",
         "October 21st, 1600. Sekigahara. 160,000 soldiers face each other\n"
         "across the valley in autumn mist. The fate of Japan hangs here."),
        ("ieyasu",     "Tokugawa Ieyasu",
         "Every clan in Japan has chosen a side.\n"
         "The western lords — Mitsunari's coalition — outnumber us.\n"
         "But numbers are not the whole story."),
        ("tadakatsu",  "Honda Tadakatsu",
         "Kobayakawa Hideaki holds the southern ridge.\n"
         "He pledged to the west — but his loyalty is... uncertain."),
        ("ieyasu",     "Tokugawa Ieyasu",
         "I sent him a letter. He will betray Mitsunari when the moment\n"
         "comes. I am certain of it."),
        ("yukimura",   "Sanada Yukimura",
         "[in the western camp]  The Tokugawa cannot be allowed to win\n"
         "this day. For Lord Hideyori — for the Toyotomi — charge!"),
        ("ieyasu",     "Tokugawa Ieyasu",
         "The mist lifts. The battle begins.\n"
         "Today, I fulfil what I have waited forty years for.\n"
         "...ADVANCE!"),
    ],

    # ── Chapter 19 · Osaka — The Winter Siege ────────────────────────────────
    [
        ("narrator",   "Narrator",
         "1614. Toyotomi Hideyori — Hideyoshi's son — shelters in Osaka\n"
         "Castle with 100,000 ronin who have nowhere else to go."),
        ("chacha",     "Lady Chacha",
         "They come for my son. Ieyasu smiled at Hideyoshi's deathbed\n"
         "and made his promise — and has been breaking it ever since."),
        ("yukimura",   "Sanada Yukimura",
         "Lady Chacha. I am Sanada Yukimura. My family has fought the\n"
         "Tokugawa for thirty years. I will defend Hideyori — or die here."),
        ("ieyasu",     "Tokugawa Ieyasu",
         "The castle is impregnable from outside. Very well.\n"
         "We fill the moat. We negotiate a false peace. And we wait."),
        ("yukimura",   "Sanada Yukimura",
         "They are filling the outer moats! This is treachery!\n"
         "The peace terms were a lie from the beginning!"),
        ("chacha",     "Lady Chacha",
         "Yukimura — can Osaka hold without the outer walls?"),
        ("yukimura",   "Sanada Yukimura",
         "It must. Ready the garrison. We fight in the spring."),
    ],

    # ── Chapter 20 · Osaka Summer — The Final Blaze ──────────────────────────
    [
        ("narrator",   "Narrator",
         "Summer, 1615. The Tokugawa return. The outer moats are filled.\n"
         "Osaka stands alone, beautiful and doomed."),
        ("yukimura",   "Sanada Yukimura",
         "We cannot win this war. I have known it since winter.\n"
         "But a samurai does not choose when to die — only how."),
        ("chacha",     "Lady Chacha",
         "Yukimura... take Hideyori and flee. There may still be—"),
        ("yukimura",   "Sanada Yukimura",
         "Hideyori will not run. And neither will I.\n"
         "If this is the Toyotomi's last day — it will be a day\n"
         "Japan remembers for a thousand years."),
        ("ieyasu",     "Tokugawa Ieyasu",
         "[commanding the encircling army]  End this. The age of\n"
         "warring states ends today. Japan will know peace — my peace."),
        ("yukimura",   "Sanada Yukimura",
         "THEN COME AND TAKE IT!\n"
         "FOR OSAKA! FOR TOYOTOMI! FOR THE DREAM THAT REFUSES TO DIE!"),
    ],
]
