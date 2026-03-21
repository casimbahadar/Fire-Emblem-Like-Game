'''
Boss battle pre-combat dialogs and unit vs unit rivalries.
Samurai Warriors-style: dramatic speeches before important fights.
'''

# ── Boss pre-battle dialogs ───────────────────────────────────────────────────
# Keyed by boss unit_id. Each entry is a list of (speaker_id_or_label, text) tuples.
# speaker_id matches a unit_id for named units, or "narrator" for narration.

BOSS_DIALOGS = {

    "yoshimoto": [
        ("narrator",    "Imagawa Yoshimoto looks up from his tea ceremony, incredulous."),
        ("yoshimoto",   "You DARE interrupt a man of culture? Twenty-five thousand\n"
                        "soldiers guard this camp! You are nothing but a gust of wind!"),
        ("nobunaga",    "Then let this wind be the last thing you hear.\n"
                        "Human life is fifty years — yours ends now."),
        ("yoshimoto",   "...Insolent wretch!"),
    ],

    "shingen": [
        ("narrator",    "The Tiger of Kai surveys the battlefield with cold calculation."),
        ("shingen",     "WIND — FOREST — FIRE — MOUNTAIN. You have read my banner.\n"
                        "Do you understand what those words mean?"),
        ("nobunaga",    "They mean you are about to be defeated by someone\n"
                        "who ignored every rule you ever wrote."),
        ("shingen",     "Ha! Bold words, boy. Show me if they are worth anything.\n"
                        "TAKEDA — CHARGE!"),
    ],

    "kenshin": [
        ("narrator",    "Uesugi Kenshin raises his naginata — the Bishamonten's avatar."),
        ("kenshin",     "I did not come to conquer. I came because justice demanded it.\n"
                        "Every man who falls today falls on your head, Oda Nobunaga."),
        ("nobunaga",    "Justice? You call it justice to march armies across\n"
                        "innocent provinces? I call it something else."),
        ("kenshin",     "BISHAMONTEN GUIDES MY BLADE! WHO DARES STAND AGAINST THE DIVINE?"),
        ("nobunaga",    "I do. And I'm not impressed by gods, either."),
    ],

    "mitsuhide": [
        ("narrator",    "Akechi Mitsuhide faces Nobunaga one last time. His voice is hollow."),
        ("mitsuhide",   "My lord... I am sorry. There is no excuse I can give you.\n"
                        "What I did was unforgivable. I know that."),
        ("nobunaga",    "Is it Mitsuhide? ...I should have seen this coming.\n"
                        "You always tried too hard to be loyal. That was your flaw."),
        ("mitsuhide",   "Then strike me down. I will not resist my punishment."),
        ("nobunaga",    "You already know I won't make it that simple."),
    ],

    "mitsunari": [
        ("narrator",    "Ishida Mitsunari stands firm before his army's rout."),
        ("mitsunari",   "You think this ends here? Hideyoshi-sama's dream\n"
                        "cannot be killed by a battle! I will not bend!"),
        ("hideyoshi",   "Mitsunari... I built the dream. You are trying to\n"
                        "freeze it in amber. That is not what I wanted."),
        ("mitsunari",   "Then what DID you want?! You left no instructions!\n"
                        "Just a child and a castle and twenty rival lords!"),
        ("hideyoshi",   "...I wanted peace. Maybe I was wrong to think I could build it."),
    ],

    "masamune": [
        ("narrator",    "Date Masamune flashes his one-eyed grin across the battlefield."),
        ("masamune",    "Ha! Finally, someone worth fighting! Do you know\n"
                        "who I am? The One-Eyed Dragon of Oshu!"),
        ("nobunaga",    "I know who you are. Born a century too late,\n"
                        "and desperately trying to make up for it."),
        ("masamune",    "TOO LATE?! I'll show you too late! My blade will\n"
                        "carve my name into HISTORY — starting with your skull!"),
    ],

    "ujiyasu": [
        ("narrator",    "The Lion of Sagami plants his feet — he has never lost a castle."),
        ("ujiyasu",     "You think walls and siege craft impress me?\n"
                        "I built these defenses. I KNOW every weakness. And I know yours."),
        ("hideyoshi",   "Then you know I filled your moat with a garden party\n"
                        "and my men haven't broken a sweat. It's over, Ujiyasu."),
        ("ujiyasu",     "...Damn monkey. You fight like no samurai I've ever faced."),
        ("hideyoshi",   "That's because I'm not really a samurai. Never was."),
    ],

    "nagamasa": [
        ("narrator",    "Azai Nagamasa faces Nobunaga. Between them stands the ghost of an alliance."),
        ("nagamasa",    "I know what you think of me. Traitor. Oath-breaker.\n"
                        "But the Asakura were allies of the Azai long before you were."),
        ("nobunaga",    "Honor I can respect. But you picked the losing side."),
        ("nagamasa",    "Perhaps. But I picked the HONORABLE side.\n"
                        "That matters more to me than winning."),
        ("narrator",    "Nearby, Oichi weeps silently."),
    ],

    "yoshihiro": [
        ("narrator",    "Shimazu Yoshihiro — the Demon of Sekigahara — turns to face the enemy alone."),
        ("yoshihiro",   "You want to fight the Shimazu? GOOD.\n"
                        "Come then! All of you! I haven't started yet!"),
        ("ieyasu",      "Yoshihiro... even you cannot win this. The battle is lost."),
        ("yoshihiro",   "LOST? The Shimazu don't LOSE! We just run out of people to kill!\n"
                        "DEMON — CHARGE!"),
    ],

    "sanada_yukimura_late": [
        ("narrator",    "Sanada Yukimura. His eyes burn with the fire of a man\n"
                        "who knows this is his last day — and has made peace with it."),
        ("yukimura",    "IEYASU! I am here! I am SANADA YUKIMURA and I am STILL ALIVE!\n"
                        "Come out and face me! THIS IS MY MOMENT!"),
        ("ieyasu",      "[pale] ...That man... even now he terrifies me."),
        ("yukimura",    "Japan has no more strong men after today.\n"
                        "At least... I can say I was the last one."),
    ],

    "hideyori": [
        ("narrator",    "Toyotomi Hideyori, young lord of Osaka, draws his blade for the first time."),
        ("hideyori",    "My father built this castle! My father unified Japan!\n"
                        "You cannot simply... take it! It belongs to the TOYOTOMI!"),
        ("ieyasu",      "Hideyori... I served your father. I loved him, in my way.\n"
                        "But his era is over. You must understand that."),
        ("hideyori",    "Never! I will never yield Osaka! NEVER!"),
        ("ieyasu",      "[quiet] ...I know. That is why I came."),
    ],

    "motonari": [
        ("narrator",    "Mori Motonari — the Fox of Chugoku — watches with cold eyes."),
        ("motonari",    "You walked into my territory. Every path you took,\n"
                        "every ally you made — I planned for it. Three steps ago\n"
                        "you were already inside my trap."),
        ("hideyoshi",   "Funny thing about traps — the person who built them\n"
                        "always thinks they're smarter than they are."),
        ("motonari",    "...You're not what I expected, little monkey."),
        ("hideyoshi",   "Nobody ever is. That's how I keep winning."),
    ],

    "tatsuoki": [
        ("narrator",    "Saito Tatsuoki — pale, sweating, nothing like his legendary father."),
        ("tatsuoki",    "You attack INABAYAMA? My father's castle?!\n"
                        "Do you know what my father was? Do you know his NAME?"),
        ("nobunaga",    "Saito Dosan. The Viper of Mino. He was brilliant.\n"
                        "He was also my father-in-law. He told me this castle was MINE."),
        ("tatsuoki",    "He said— he would NEVER—"),
        ("nobunaga",    "He wrote it. Before you drove off every retainer he had."),
    ],

    "yoshihisa": [
        ("narrator",    "Shimazu Yoshihisa deploys his famous tsuridono trap formation."),
        ("yoshihisa",   "You are already in the trap. Feigning retreat drew you here.\n"
                        "My flanks will close in thirty seconds. Surrender now\n"
                        "and I will spare your men."),
        ("hideyoshi",   "I know your formation. Kanbei told me about it this morning."),
        ("yoshihisa",   "...That bald schemer."),
        ("kanbei",      "[from somewhere nearby] I prefer 'strategist,' my lord."),
    ],
}

# ── Unit vs unit rival dialogs ─────────────────────────────────────────────────
# Triggered when specific attacker fights specific defender (first encounter only)
RIVAL_DIALOGS = {
    ("nobunaga", "kenshin"): [
        ("nobunaga", "So you finally came south, Dragon."),
        ("kenshin",  "I came for justice, not ambition. Unlike you."),
        ("nobunaga", "Justice and ambition look the same from the battlefield."),
    ],
    ("hideyoshi", "mitsunari"): [
        ("mitsunari","Lord Hideyoshi... why did you never write down the rules?"),
        ("hideyoshi","Because I trusted the people around me to figure it out."),
        ("mitsunari","...That trust was misplaced."),
        ("hideyoshi","Maybe. I still don't regret it."),
    ],
    ("ieyasu", "yukimura"): [
        ("yukimura", "IEYASU! You survived Sekigahara, you survived everything—"),
        ("ieyasu",   "As did you, Yukimura. As did you."),
        ("yukimura", "Then let this be the end. One of us walks away today."),
        ("ieyasu",   "[quietly] I know. I know."),
    ],
    ("oichi", "nagamasa"): [
        ("oichi",    "Nagamasa... please. Stop. There must be another way."),
        ("nagamasa", "Oichi... my heart breaks that it is you asking this.\n"
                     "But I cannot abandon my father's oath. I am sorry."),
        ("oichi",    "Then I am sorry too."),
    ],
    ("kiyomasa", "fukushima"): [
        ("fukushima","That enemy is MINE, Kiyomasa! Stand ASIDE!"),
        ("kiyomasa", "You're too slow! I was already moving when you were still arguing!"),
        ("fukushima","I AM NOT SLOW—"),
        ("kiyomasa", "You're slower than me. That's all that matters."),
    ],
    ("hanzo", "fuma"): [
        ("hanzo",    "Fuma Kotaro. I've waited for this."),
        ("fuma",     "..."),
        ("hanzo",    "You never talk. Somehow that makes you more terrifying."),
        ("fuma",     "..."),
        ("hanzo",    "Right. Shall we?"),
    ],
    ("nobunaga", "mitsuhide"): [
        ("mitsuhide","My lord... there are no words for what I have done."),
        ("nobunaga", "There never are. Yet somehow men always do it anyway."),
        ("mitsuhide","I thought— I believed— I was wrong. That is all I can say."),
        ("nobunaga", "Then say it with your blade."),
    ],
}

# Track which dialogs have already fired this session (reset per chapter)
_fired_boss_dialogs  = set()
_fired_rival_dialogs = set()


def reset_dialog_flags():
    _fired_boss_dialogs.clear()
    _fired_rival_dialogs.clear()


def get_pre_combat_dialog(attacker, defender):
    '''Return a list of dialog lines, or None if no dialog fires.'''
    lines = None

    # Check rival dialog (specific pair, fires once)
    key = (attacker.unit_id, defender.unit_id)
    rkey = (defender.unit_id, attacker.unit_id)
    if key in RIVAL_DIALOGS and key not in _fired_rival_dialogs:
        lines = RIVAL_DIALOGS[key]
        _fired_rival_dialogs.add(key)
    elif rkey in RIVAL_DIALOGS and rkey not in _fired_rival_dialogs:
        lines = RIVAL_DIALOGS[rkey]
        _fired_rival_dialogs.add(rkey)

    # Check boss dialog (defender is boss/lord, fires once)
    if lines is None and (defender.is_lord or getattr(defender, 'is_boss', False)):
        bid = defender.unit_id
        if bid in BOSS_DIALOGS and bid not in _fired_boss_dialogs:
            lines = BOSS_DIALOGS[bid]
            _fired_boss_dialogs.add(bid)

    return lines
