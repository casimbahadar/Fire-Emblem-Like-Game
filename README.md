# Sengoku Tactics: Age of the Warring States

A Fire Emblem-style tactical RPG set in Sengoku-era Japan (1550–1615).
Command historical officers across **20 story chapters** of turn-based grid combat,
following the rise and fall of the three great unifiers — Nobunaga, Hideyoshi, and Ieyasu.

---

## Quick Start

**Requirements:** Python 3.8+ · Pygame 2.x

```bash
pip install pygame
python main.py
```

Runs in a 700 × 680 window. Touch/mouse controls supported alongside keyboard.

---

## Story Overview

The game spans Japan's entire Sengoku period (1560–1615) as a single continuous narrative:

| Arc | Chapters | Storyline |
|-----|----------|-----------|
| The Fool of Owari | 1–3 | Nobunaga's shocking rise — Okehazama, Kawanakajima |
| The Oda Machine | 4–10 | Honnoji betrayal, Hideyoshi's revenge, Nagashino revolution |
| The Western Wars | 11–13 | Mori campaign, Takamatsu flood siege, Yamazaki reckoning |
| The New Order | 14–16 | Shizugatake feud, Komaki patience, Odawara's fall |
| Ieyasu's Gamble | 17–20 | Fushimi last stand, Sekigahara, Osaka Winter & Summer |

---

## Pre-Battle Scenes

Each chapter opens with a **visual-novel style cutscene** before the battle begins.
Named characters exchange 4–7 lines of historically-grounded dialogue that form a
coherent plot arc across the full game.

- Dark ink-wash background with chapter title overlay
- Portrait box (left) shows speaker with faction colour coding
- Gold-framed dialogue box (bottom) with name plate and wrapped text
- Progress dots show position in the scene; line counter top-right
- Advance with **Z / Enter / Space / tap** — skip to chapter intro on last line

---

## Controls

### Keyboard

| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move cursor |
| Z / Enter | Select unit · Confirm · Advance dialogue |
| X / Escape | Cancel / Deselect |
| Space | End player turn (or advance dialogue) |
| A | Attack (unit selected and enemy in range) |
| H | Heal (healer selected, ally in range) |
| W | Wait — end this unit's turn |
| E | Seize castle (lord on seize tile) |
| R | Recruit (lord adjacent to recruitable unit) |
| Tab | View stat sheet for selected unit |
| S | Skip tutorial (on title screen) |

### Touch / Mouse

On-screen buttons appear at the bottom of the screen during player turns:
**Attack · Heal · Wait · Seize · Recruit · Stat**

Tap the map to move the cursor; tap a unit to select it.

---

## Game Modes

**Classic Mode** — Permadeath. Units that fall in battle are gone forever.

**Casual Mode** — Fallen units are revived at full HP at the start of the next chapter.

Mode is selected at game start and affects the entire playthrough.

---

## Combat System

Combat follows the Fire Emblem formula:

1. **Attacker strikes** — Hit rate = Hit% − enemy Avoid (two-RN system)
2. **Defender counters** — if in weapon range and has an equipped weapon
3. **Double attack** — unit with SPD 4+ higher than opponent strikes twice
4. **Critical hit** — triple damage; Crit% = (unit Skill/2) − enemy Luck
5. **EXP gain** — based on level difference; kill bonus; capped at 100/level
6. **Level up** — random stat increases per class growth rates (shown in stat sheet)

The **combat forecast** (visible before confirming) shows Atk, Hit%, and Crit% for both sides.

### Weapon Triangle

```
Yari (Spear)  >  Katana  >  Naginata  >  Yari
Nodachi  >  Naginata
Tanto  >  Bow
Bow       — Ranged; neutral triangle; cannot counter at melee range
Tetsubo   — Heavy bludgeon; neutral triangle
Staff     — Healing / magic; no weapon triangle
```

Advantage: **+Hit, +Damage**. Disadvantage: **−Hit, −Damage**.

---

## Unit Classes

### Core Classes

| Class | Role | Weapons | Move | Special |
|-------|------|---------|------|---------|
| Daimyo | Lord — death = game over | Katana, Nodachi, Yari | 5 | Can Seize, Recruit |
| Samurai | Balanced warrior | Katana, Nodachi | 5 | — |
| Ashigaru | Foot soldier, numerous | Yari, Tetsubo | 4 | — |
| Spearman | Polearm specialist | Yari, Naginata | 4 | — |
| Cavalry | High movement, powerful charge | Katana, Yari | 7 | Forest/mountain penalty |
| Archer | Ranged attacker | Bow | 4 | Cannot counter at melee |
| Ninja | Fast, dual-range | Tanto, Bow | 6 | Ignores rough terrain |
| Ronin | High STR+SKL, lone warrior | Katana, Nodachi | 5 | — |
| Sohei | Warrior monk — hybrid | Naginata, Staff | 4 | Can heal |
| Monk | Pure healer / mage | Staff | 4 | Healing only |
| Onmyoji | Spiritual mage | Staff | 4 | High MAG |
| Berserker | Maximum power, low accuracy | Tetsubo, Nodachi | 4 | High crit |
| Kunoichi | Female ninja — fastest | Tanto, Bow | 7 | Ignores rough terrain |

### Flying & Mounted Classes

| Class | Weapons | Move | Notes |
|-------|---------|------|-------|
| Tengu Rider | Tanto, Bow | 8 | Flies over all terrain; ignores obstacles |
| War Hawk | Katana, Yari | 8 | Flies; high STR |
| Storm Rider | Bow | 9 | Flies; fastest unit in game |
| Heavy Cavalry | Yari, Tetsubo | 6 | High DEF; terrain-penalised |
| Battle Monk | Naginata, Staff | 5 | Flying; can heal |
| Dragon Rider | Nodachi, Yari | 7 | Flies; best offensive flier |
| Ghost Cavalry | Tanto | 8 | Flies; no terrain cost ever |
| Sea Raider | Katana, Yari | 5 | River/coast movement bonus |
| Ashigaru Cavalry | Yari | 6 | Budget mounted unit |
| Lance Cavalry | Yari, Naginata | 7 | — |
| Mountain Monk | Naginata, Staff | 4 | Mountain specialist |

---

## Terrain

| Terrain | DEF | AVO | Move Cost | Notes |
|---------|-----|-----|-----------|-------|
| Plain | +0 | +0 | 1 | Standard |
| Road | +0 | +0 | 1 | Always fast |
| Forest | +1 | +20 | 2 | Cavalry penalty; Ninja free |
| Village | +1 | +10 | 1 | Can be seized for story |
| Fort | +2 | +20 | 1 | Heals unit at turn start |
| Castle | +3 | +30 | 1 | Seize objective tile |
| Mountain | +2 | +30 | 4 | Heavy cavalry penalty |
| River | +0 | +0 | 5 | Mounted units struggle |
| Bridge | +0 | +0 | 1 | River crossing |
| Sea | — | — | Impassable | Sea Raiders only |

Flying units ignore all terrain movement costs.

---

## Chapters

| # | Subtitle | Objective | Turn Limit |
|---|----------|-----------|------------|
| 1 | Departure from Owari | Seize the castle | — |
| 2 | Storm of Okehazama | Defeat Imagawa Yoshimoto | — |
| 3 | Kawanakajima — Dragon and Tiger | Rout all enemies | — |
| 4 | The Flames of Honnoji | Seize the inner sanctum | — |
| 5 | Sekigahara — The First Reckoning | Defeat the enemy commander | — |
| 6 | Siege of Inabayama | Seize Inabayama Castle | — |
| 7 | The Betrayal at Anegawa | Rout all enemies | — |
| 8 | The Ikko-Ikki at Nagashima | Seize the island fortress | — |
| 9 | Relief of Nagashino Castle | Defend until reinforcements arrive | 12 turns |
| 10 | Nagashino — The Volley Line | Rout all enemies | — |
| 11 | Conquest of the West — Mori Campaign | Seize the western stronghold | — |
| 12 | The Flooded Castle — Takamatsu | Defeat the enemy commander | — |
| 13 | Yamazaki — The Monkey's Revenge | Defeat Akechi Mitsuhide | — |
| 14 | The Battle of Shizugatake | Rout all enemies | — |
| 15 | Komaki-Nagakute — War of Patience | Seize the field headquarters | — |
| 16 | The Fall of Odawara | Seize Odawara Castle | — |
| 17 | Defense of Fushimi | Defend the castle — survive | 15 turns |
| 18 | Sekigahara — The Great Battle | Rout all enemies | — |
| 19 | Osaka — The Winter Siege | Defend Osaka Castle | 18 turns |
| 20 | Osaka Summer — The Final Blaze | Last stand — rout all enemies | — |

Reinforcement waves arrive mid-chapter in most maps. Watch the turn counter.

---

## Roster — Historical Officers

### Oda / Toyotomi (Player)

| Name | Class | Role |
|------|-------|------|
| Oda Nobunaga | Daimyo | Lord — death = game over |
| Toyotomi Hideyoshi | Samurai | Primary fighter; becomes lord in later chapters |
| Akechi Mitsuhide | Ronin | High skill; antagonist in Ch 4 |
| Shibata Katsuie | Berserker | Highest raw power on roster |
| Niwa Nagahide | Spearman | Reliable mid-game veteran |
| Mori Ranmaru | Ninja | Nobunaga's devoted page; fastest Oda unit |
| Nene | Kunoichi | Hideyoshi's wife; spy and fighter |
| Maeda Toshiie | Cavalry | High movement; joins mid-game |
| Kuroda Kanbei | Ronin | Hideyoshi's brilliant strategist |
| Takenaka Hanbei | Monk | Fragile but high magic; joins early |
| Sanada Yukimura | Samurai | Heroic final chapters fighter |
| Sanada Masayuki | Samurai | Yukimura's cunning father |

### Tokugawa (Ally → Later Player)

| Name | Class |
|------|-------|
| Tokugawa Ieyasu | Cavalry |
| Honda Tadakatsu | Berserker |
| Ii Naomasa | Heavy Cavalry |
| Ii Naotora | Lance Cavalry |

### Enemy Bosses (Notable)

| Name | Chapter | Notes |
|------|---------|-------|
| Imagawa Yoshimoto | Ch 2 | Defeat to win Okehazama |
| Uesugi Kenshin | Ch 3 | Dragon of Echigo — Daimyo |
| Takeda Shingen | Ch 3 | Tiger of Kai — Daimyo |
| Takeda Katsuyori | Ch 10 | Commands legendary cavalry |
| Mori Terumoto | Ch 11–12 | Western clan lord |
| Ankokuji Ekei | Ch 8, 11 | Mori envoy; monk class |
| Yamamoto Kansuke | Ch 1, 3 | Shingen's brilliant eye |

---

## Recruit System

Certain enemy or neutral units can be recruited mid-battle:
- Move your **lord** (Nobunaga / Hideyoshi / Ieyasu) adjacent to a recruitable unit
- Press **R** or tap the **Recruit** button
- The unit joins your roster permanently for remaining chapters

Recruited units retain their current stats and level.

---

## Reinforcements

Most chapters feature enemy reinforcement waves that arrive at set turns from
the map edge. A warning banner is shown at the top of the screen when a wave
is imminent. The chapter intro screen also notes the first reinforcement turn.

---

## Tutorial

A guided tutorial chapter runs before Chapter 1, teaching:
- Cursor movement and unit selection
- Movement range and attack range display
- Attack and heal actions
- The weapon triangle
- Turn ending

Press **S** on the title screen (after selecting mode) to skip the tutorial.

---

## Tech Notes

Built with **Python + Pygame 2**. No external assets — all graphics are rendered
procedurally (coloured rectangles, text, anti-aliased primitives).

```
game/
  constants.py     — All game constants, state names, terrain/faction IDs
  unit.py          — Unit class, stat calculations, EXP/level-up, full roster
  map.py           — Map builder for all 20 chapter maps + terrain logic
  chapter.py       — Chapter definitions (objectives, unit placement, waves)
  scene_dialogs.py — Pre-battle VN dialogue for all 20 chapters
  state.py         — GameState — the single source of truth for all game data
  renderer.py      — All drawing code (map, units, UI panels, scene, menus)
  ai.py            — Enemy AI (threat scoring, attack/heal/move logic)
  dialogs.py       — Boss pre-combat dialogue system
  combat.py        — Combat resolution (hit/crit/damage/EXP)
  touch.py         — Touch/mouse button overlay
  tutorial.py      — Step-by-step guided tutorial manager
```
