# Sengoku Tactics: Age of the Warring States

A Fire Emblem-style tactical RPG set in Sengoku-era Japan (1550–1600).
Command historical officers across five chapters of tactical grid combat.

## Requirements

- Python 3.8+
- Pygame 2.x

```bash
pip install pygame
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Move cursor |
| Z / Enter | Select unit / Confirm action |
| X / Escape | Cancel / Deselect |
| Space | End player turn |
| A | Attack (with selected unit) |
| H | Heal (with healer selected) |
| W | Wait (end unit's turn) |
| E | Seize (lord on castle tile) |

## Game Features

### Weapon Triangle
Similar to Fire Emblem's classic system:

```
Yari (Spear) > Katana > Naginata > Yari
Nodachi > Naginata
Tanto > Bow
Bow: Neutral (attacks from range)
Tetsubo: Neutral (heavy bludgeon)
Staff: Healing / Magic
```

Weapon advantage grants +Hit and +Damage. Disadvantage penalizes both.

### Unit Classes

| Class | Description | Weapons |
|-------|-------------|---------|
| Daimyo | Warlord leader — high all-around stats | Katana, Nodachi, Yari |
| Samurai | Balanced warrior | Katana, Nodachi |
| Ashigaru | Foot soldier, cheap but numerous | Yari, Tetsubo |
| Cavalry | High movement, strong charge | Katana, Yari |
| Archer | Ranged attacker, can't counter melee | Bow |
| Ninja | Fast, high skill, dual-range | Tanto, Bow |
| Ronin | High strength and skill, loner | Katana, Nodachi |
| Spearman | Polearm specialist | Yari, Naginata |
| Sohei | Warrior monk — magic + combat | Naginata, Staff |
| Monk | Pure healer / mage | Staff |
| Onmyoji | Spiritual mage, high magic | Staff |
| Berserker | Maximum power, low accuracy | Tetsubo, Nodachi |
| Kunoichi | Female ninja — fastest unit | Tanto, Bow |

### Terrain Types

| Terrain | Def | Avo | Move Cost |
|---------|-----|-----|-----------|
| Plain | +0 | +0 | 1 |
| Road | +0 | +0 | 1 |
| Forest | +1 | +20 | 2 |
| Village | +1 | +10 | 1 |
| Fort | +2 | +20 | 1 |
| Castle | +3 | +30 | 1 |
| Mountain | +2 | +30 | 4 |
| River | +0 | +0 | 5 |
| Bridge | +0 | +0 | 1 |

Cavalry units are penalized in forests and mountains. Ninja move freely over rough terrain.

### Historical Officers

**Player/Oda Clan**
- **Oda Nobunaga** — Lord unit (Daimyo). Death = game over.
- **Toyotomi Hideyoshi** — Samurai. Strong and resourceful.
- **Akechi Mitsuhide** — Ronin. High skill but watch for betrayal...
- **Shibata Katsuie** — Berserker. Raw power unmatched.
- **Niwa Nagahide** — Spearman. Reliable veteran.
- **Mori Ranmaru** — Ninja. Nobunaga's devoted page.
- **Nene** — Kunoichi. Hideyoshi's wife, master spy.

**Allied**
- **Tokugawa Ieyasu** — Cavalry. Patient, powerful. Joins as ally.

**Oda Rivals (Enemy)**
- **Takeda Shingen** — Tiger of Kai. Daimyo. Boss of Chapter 3.
- **Uesugi Kenshin** — Dragon of Echigo. Daimyo. Boss of Chapter 3.
- **Date Masamune** — One-Eyed Dragon. Daimyo. Chapter 5.
- **Shimazu Yoshihisa** — Southern warlord. Boss of Chapter 5.
- Yamamoto Kansuke, Yamagata Masakage, Naoe Kanetsugu, and more.

## Chapters

| # | Title | Map | Objective |
|---|-------|-----|-----------|
| 1 | Departure from Owari | Owari Plains (15×10) | Seize the castle |
| 2 | The Storm of Okehazama | Okehazama Forest (14×11) | Defeat the commander |
| 3 | Kawanakajima | Kawanakajima Battlefield (16×12) | Rout all enemies |
| 4 | The Flames of Honnoji | Honnoji Temple (16×12) | Reach the inner sanctum |
| 5 | Sekigahara | Sekigahara (18×14) | Seize the center |

## Combat System

Combat follows Fire Emblem rules:
1. **Attacker strikes** — hit/miss determined by (Hit Rate − Avoid), using the two-RN system
2. **Defender counters** — if in range and has a usable weapon
3. **Double attack** — unit with SPD 4+ higher than opponent attacks again
4. **Critical hits** — triple damage (Crit% − enemy Luck)
5. **EXP gain** — based on enemy level difference; bonus for kills
6. **Level ups** — random stat increases based on class growth rates

The **combat forecast** (shown before confirming an attack) displays damage, hit%, and crit% for both sides.
