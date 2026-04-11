# Portraits

This directory holds optional character portrait images for Sengoku Tactics.
**The game runs perfectly fine with zero images here** — when no portrait is
found, the stat sheet falls back to a procedural class symbol.

## How the loader works

`game_manager.gd::_try_load_portrait()` looks for a portrait in this order:

1. An explicit `portrait_path` set on the unit's roster entry
2. `res://assets/portraits/<unit_id>.png`
3. `res://assets/portraits/<unit_id>.jpg`
4. `res://assets/portraits/classes/<class_lower_with_underscores>.png`
   (e.g. `mounted_archer.png`, `noble_lady.png`)

So the easiest way to add art is to drop files named after the unit IDs from
`scripts/data/roster.gd` (e.g. `nobunaga.png`, `hideyoshi.png`) into this
directory. To cover a whole class at once, use the `classes/` subfolder.

Recommended portrait dimensions: **square (e.g. 512×512 or 768×768)**.
The stat sheet uses a square portrait area on the right side and applies
`STRETCH_KEEP_ASPECT_COVERED`, so non-square images will be cropped.

## Licensing — IMPORTANT

**No images are bundled with this repo.** You must add your own and verify
the license of each file you use. The author of this repo cannot guarantee
the license status of any image you download from the internet. **Always
check the license on the original source page**, not just a reposted image.

Below are reputable sources known to host genuinely free game art with
clear licenses. Read each individual asset's license before using it.

### CC0 / Public Domain (no attribution required, commercial OK)

| Source | What it has |
|---|---|
| [OpenGameArt — CC0 Portraits collection](https://opengameart.org/content/cc0-portraits) | Curated CC0 portrait art |
| [OpenGameArt — DENZI's public domain art](https://opengameart.org/content/denzis-public-domain-art) | Long-running PD pixel art collection |
| [OpenGameArt — CC0 tag](https://opengameart.org/taxonomy/term/4) | Everything tagged CC0 |
| [Kenney.nl](https://kenney.nl/) | Stylized CC0 game packs |

### CC-BY / CC-BY-SA (free, but attribution required)

CC-BY just needs you to credit the artist somewhere in your game.
CC-BY-SA additionally requires that any modified version you distribute
also be released under CC-BY-SA — be aware of this if you edit assets.

| Source | What it has |
|---|---|
| [OpenGameArt — Samurai tag](https://opengameart.org/art-tags/samurai) | Samurai-themed art (mixed licenses, check each) |
| [LPC (Liberated Pixel Cup)](https://opengameart.org/content/liberated-pixel-cup-lpc-base-assets-sprites-map-tiles) | CC-BY-SA 3.0 / GPL 3.0 character bases |
| [LPC Anime Portraits](https://lpc.opengameart.org/content/anime-portrait-for-lpc-characters) | Anime-style portraits matching LPC sprites |
| [Reiner's Tilesets](https://www.reinerstilesets.de/) | Free game art (check site terms) |

### itch.io free packs (license varies per pack)

| Source | What it has |
|---|---|
| [itch.io — free portrait assets](https://itch.io/game-assets/free/tag-portraits) | Mixed pixel + illustrated portraits |
| [itch.io — free CC0 RPG assets](https://itch.io/game-assets/new-and-popular/free/genre-rpg/tag-cc0) | Filtered to CC0 only |
| [itch.io — free anime assets](https://itch.io/game-assets/free/tag-anime) | Anime-style art |

### AI generation

If you generate portraits yourself with Stable Diffusion, Midjourney, or
similar tools, the licensing depends on the specific tool's terms of
service and your jurisdiction's stance on AI-generated work. In most
hobby/personal contexts this is fine. **For commercial release, consult
the actual license.**

## Recording attributions

If you use any CC-BY or CC-BY-SA art, create a file `CREDITS.md` in this
folder listing each piece, the artist, the source URL, and the license.
This is required by those licenses and is good practice anyway.

Example entry:

```
- nobunaga.png — "Samurai Warlord" by ExampleArtist
  Source: https://opengameart.org/content/example
  License: CC-BY 3.0
```
