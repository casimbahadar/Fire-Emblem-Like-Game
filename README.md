# Sengoku Tactics: Age of the Warring States

A Fire Emblem-style tactical RPG set in Sengoku-era Japan.
Command historical officers across 20 story chapters of turn-based grid combat.

---

## Quick Start

**Requirements:** Python 3.8+ · Pygame 2.x

```bash
pip install pygame
python main.py
```

---

## Story

Japan, 1560. The land is shattered — a hundred warlords tear the realm apart
in endless war. Into this chaos steps a young lord his own men call *the Fool
of Owari*. Against impossible odds he strikes, and the age of Oda Nobunaga begins.

Follow the rise and fall of Japan's three great unifiers across 20 chapters
of war, betrayal, and sacrifice — from the lightning raid at Okehazama to
the final, desperate blaze at Osaka Castle. Alliances will shatter. Generals
will turn on their lords. And in the end, only one clan can claim the realm.

*Every battle has a story. Every story has a cost.*

---

## Game Modes

**Classic** — Permadeath. Units that fall in battle are gone forever.

**Casual** — Fallen units are revived at the start of the next chapter.

---

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move cursor |
| Z / Enter | Select · Confirm · Advance dialogue |
| X / Escape | Cancel / Deselect |
| Space | End player turn |
| A | Attack |
| H | Heal |
| W | Wait |
| E | Seize |
| R | Recruit |
| Tab | Unit stat sheet |

Touch and mouse controls are also fully supported.

---

## Combat

1. **Attacker strikes** — Hit% vs enemy Avoid (two-RN system)
2. **Defender counters** — if in weapon range
3. **Double attack** — SPD 4+ higher than opponent = second strike
4. **Critical hit** — triple damage; Crit% = (Skill / 2) − enemy Luck
5. **EXP & level ups** — kill and survive to grow; stat gains vary by class

The **combat forecast** shows damage, hit%, and crit% before you commit.

### Weapon Triangle

```
Yari  >  Katana  >  Naginata  >  Yari
Nodachi  >  Naginata
Tanto  >  Bow
Staff — healing / magic (no triangle)
```

Advantage grants +Hit +Damage. Disadvantage penalises both.

---

## Unit Classes

### Warriors

| Class | Weapons | Move | Notes |
|-------|---------|------|-------|
| Daimyo | Katana, Nodachi, Yari | 5 | Lord — death ends the game |
| Samurai | Katana, Nodachi | 5 | Balanced all-rounder |
| Ashigaru | Yari, Tetsubo | 4 | Cheap foot soldier |
| Spearman | Yari, Naginata | 4 | Polearm specialist |
| Ronin | Katana, Nodachi | 5 | High STR and SKL, lone wolf |
| Berserker | Tetsubo, Nodachi | 4 | Max power, low accuracy, high crit |
| General | Yari, Tetsubo | 3 | Armoured wall — huge DEF, slow |
| Kusarigama | Chain, Tanto | 5 | Chain-sickle duelist, high SKL |
| Gunner | Gun, Tanto | 4 | Ranged firearm; cannot counter melee |

### Scouts & Rangers

| Class | Weapons | Move | Notes |
|-------|---------|------|-------|
| Archer | Bow | 4 | Ranged — cannot counter at melee |
| Ninja | Tanto, Bow | 6 | Fast, dual-range, ignores rough terrain |
| Kunoichi | Tanto, Bow | 7 | Fastest foot unit; ignores terrain |
| Pirate | Katana, Nodachi | 5 | Can cross rivers and sea tiles |
| Light Cavalry | Tanto, Bow | 9 | Fastest unit in game; scout role |

### Mounted

| Class | Weapons | Move | Notes |
|-------|---------|------|-------|
| Cavalry | Katana, Yari | 7 | Standard mounted warrior |
| Hatamoto | Katana, Nodachi | 7 | Elite samurai on horseback |
| Lance Cavalry | Yari, Naginata | 8 | Anti-infantry charge specialist |
| Mounted Archer | Bow, Katana | 7 | Cavalry with ranged capability |
| Noble Cavalry | Katana, Nodachi, Yari | 8 | Lord-class mount — balanced and fast |
| Great Knight | Katana, Yari, Tetsubo | 6 | Full-plate armoured cavalry; high DEF |
| War Elephant | Tetsubo, Yari | 4 | Massive HP and DEF — extremely slow |
| Thunder Shaman | Staff, Yari | 7 | Lightning magic on horseback |
| Phantom Knight | Katana, Staff | 7 | Cursed cavalry — blade and dark magic |

### Support & Magic

| Class | Weapons | Move | Notes |
|-------|---------|------|-------|
| Monk | Staff | 4 | Healer |
| Sohei | Naginata, Staff | 4 | Warrior monk — fight and heal |
| Onmyoji | Staff | 4 | Spiritual mage; high MAG |
| Tactician | Staff, Tanto | 5 | Magic support and buffing |
| Noble Lady | Staff, Bow | 5 | Support specialist; high LCK |
| Celestial Monk | Staff, Naginata | 5 | Promoted Monk — strongest healer |
| Shrine Oracle | Staff | 5 | Sacred healer; can grant damage-absorbing barriers |
| Jade Sorceress | Staff | 4 | Highest foot-unit MAG — very fragile |
| Void Prophet | Staff | 4 | Dark curse weaver; AoE debuffer |
| Blood Ascetic | Staff, Tanto | 4 | Converts own HP into devastating blasts |
| Death Oracle | Staff | 4 | Forbidden death arts — supreme MAG, glass cannon |

### Flying

| Class | Weapons | Move | Notes |
|-------|---------|------|-------|
| Pegasus Knight | Naginata, Staff | 7 | Classic magical flyer — can heal |
| Falcon Knight | Naginata, Staff | 8 | Promoted Pegasus; fastest healer |
| Wyvern Knight | Katana, Yari | 7 | Heavy flying combatant |
| Dragon Knight | Yari, Nodachi, Katana | 6 | Mounts a war-dragon — supreme flying power |
| Sky Lancer | Yari, Naginata | 6 | Armoured flying spearman |
| Eagle Archer | Bow | 7 | Aerial bow specialist; deadly vs flyers |
| Storm Rider | Tanto, Katana | 8 | Fastest aerial duelist |
| Tengu Master | Tanto, Staff | 7 | Ninja-monk of the mountain peaks |
| Spirit Dancer | Staff, Naginata | 8 | Airborne spirit medium; offensive wind magic |
| Kitsune Sage | Staff, Tanto | 7 | Fox-spirit illusionist; highest flying MAG |
| Moon Rider | Naginata, Staff | 8 | Celestial steed rider — magic and blade balanced |
| Star Dancer | Staff, Tanto | 9 | Fastest magical unit; pure celestial caster |

---

## Terrain

| Terrain | DEF | AVO | Notes |
|---------|-----|-----|-------|
| Plain | +0 | +0 | Standard |
| Road | +0 | +0 | Always fast |
| Forest | +1 | +20 | Cavalry penalty; Ninja/Kunoichi free |
| Village | +1 | +10 | — |
| Fort | +2 | +20 | Heals unit at turn start |
| Castle | +3 | +30 | Seize objective |
| Mountain | +2 | +30 | Heavy penalty for mounted units |
| River | +0 | +0 | High movement cost; Pirates unaffected |

Flying units ignore all terrain movement costs and penalties.

---

## Your Officers

A selection of the commanders you will lead into battle:

**Oda Nobunaga** — Daimyo. The Fool of Owari. Reckless, visionary, utterly fearless.
His death means game over.

**Toyotomi Hideyoshi** — Samurai. Rose from peasant sandal-bearer to Japan's greatest general.
Cunning, resourceful, impossible to dislike.

**Akechi Mitsuhide** — Ronin. Cold intellect behind a polite face. A man with a plan of his own.

**Shibata Katsuie** — Berserker. Thirty years of loyal service and an axe that has never stopped swinging.

**Mori Ranmaru** — Ninja. Nobunaga's devoted page. Faster than anyone, loyal beyond reason.

**Nene** — Kunoichi. Hideyoshi's wife and the most dangerous spy on the field.

**Takenaka Hanbei** — Monk. A genius strategist with a body too frail for the battles he wins.

*Many more officers join, defect, and surprise you as the story unfolds.*

---

## Other Features

- **Pre-battle scenes** — Each chapter opens with a visual-novel style cutscene.
  Named characters exchange dialogue that forms a continuous story across all 20 chapters.
- **Reinforcements** — Enemy waves arrive mid-battle at set turns. Plan ahead.
- **Recruit system** — Bring your lord adjacent to certain enemies to turn them to your cause.
- **Tutorial** — A guided first chapter teaches all mechanics before the war begins.
