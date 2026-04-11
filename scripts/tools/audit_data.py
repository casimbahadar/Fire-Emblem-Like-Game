#!/usr/bin/env python3
"""
Data consistency audit for Sengoku Tactics.

Run from the project root:
    python3 scripts/tools/audit_data.py

Validates:
  - chapters.gd: in-bounds positions, no overlaps, balanced brackets
  - chapters.gd → roster.gd: all unit IDs exist
  - roster.gd → weapons.gd: all weapon IDs exist
  - roster.gd → constants.gd: all class constants exist

Exits with code 0 on success, 1 on any failure.
"""

import os
import re
import sys


def main() -> int:
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(root)

    failures = []

    # ── Load source files ────────────────────────────────────────────────
    chapters = open("scripts/data/chapters.gd").read()
    roster = open("scripts/data/roster.gd").read()
    weapons = open("scripts/data/weapons.gd").read()
    constants = open("scripts/core/constants.gd").read()

    # ── 1. chapters.gd data consistency ──────────────────────────────────
    sections = re.split(r'\{\s*"number":\s*(\d+)', chapters)[1:]
    pairs = [(sections[i], sections[i + 1]) for i in range(0, len(sections), 2)]

    for num_str, body in pairs:
        num = int(num_str)
        w_m = re.search(r'"map_width":\s*(\d+)', body)
        h_m = re.search(r'"map_height":\s*(\d+)', body)
        if not w_m or not h_m:
            failures.append(f"Ch{num}: missing map_width/map_height")
            continue
        w, h = int(w_m.group(1)), int(h_m.group(1))

        for field, pat in [
            ("player", r'"player_units":\s*\[(.*?)\],\s*"enemy_units"'),
            ("enemy", r'"enemy_units":\s*\[(.*?)\],\s*"ally_units"'),
        ]:
            m = re.search(pat, body, re.DOTALL)
            if not m:
                continue
            entries = re.findall(r'\["([^"]+)",\s*(\d+),\s*(\d+)\]', m.group(1))
            seen_pos = {}
            for eid, x, y in entries:
                x, y = int(x), int(y)
                if not (0 <= x < w and 0 <= y < h):
                    failures.append(
                        f"Ch{num} {field} {eid} out of bounds ({x},{y}) map {w}x{h}"
                    )
                if (x, y) in seen_pos:
                    failures.append(
                        f"Ch{num} {field} overlap at ({x},{y}): "
                        f"{seen_pos[(x, y)]} & {eid}"
                    )
                seen_pos[(x, y)] = eid

    # ── 2. Bracket balance ───────────────────────────────────────────────
    depth = 0
    for c in chapters:
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
    if depth != 0:
        failures.append(f"chapters.gd brackets unbalanced (depth={depth})")

    # ── 3. chapters → roster unit references ─────────────────────────────
    roster_ids = set(re.findall(r'units\["([^"]+)"\]\s*=', roster))
    referenced_ids = set()
    for m in re.finditer(r'\["([a-z_0-9]+)",\s*\d+,\s*\d+\]', chapters):
        referenced_ids.add(m.group(1))
    missing_units = referenced_ids - roster_ids
    for mu in sorted(missing_units):
        failures.append(f"chapters.gd references missing unit: {mu}")

    # ── 4. roster → weapons references ───────────────────────────────────
    weapon_ids = set(
        re.findall(r'^\s*"([a-z_0-9]+)"\s*:\s*\{', weapons, re.MULTILINE)
    )
    used_weapons = set()
    for m in re.finditer(r"\[([^\[\]]*?)\]\s*,\s*Color", roster):
        used_weapons.update(re.findall(r'"([a-z_0-9]+)"', m.group(1)))
    missing_weapons = used_weapons - weapon_ids
    for mw in sorted(missing_weapons):
        failures.append(f"roster.gd references missing weapon: {mw}")

    # ── 5. roster → constants class references ───────────────────────────
    defined_classes = set(
        re.findall(r"^const\s+(CLASS_[A-Z_]+)\s*:?=\s*\"", constants, re.MULTILINE)
    )
    # CLASS_SYMBOLS is a dict, not a class — exclude it
    referenced_classes = {
        c
        for c in re.findall(r"Constants\.(CLASS_[A-Z_]+)", roster)
        if c != "CLASS_SYMBOLS"
    }
    missing_classes = referenced_classes - defined_classes
    for mc in sorted(missing_classes):
        failures.append(f"roster.gd references missing class: {mc}")

    # ── Report ───────────────────────────────────────────────────────────
    if failures:
        print(f"AUDIT FAILED — {len(failures)} issue(s):")
        for f in failures:
            print(f"  - {f}")
        return 1

    # Summary
    total_enemies = sum(
        len(re.findall(r'\["', line))
        for line in chapters.split("\n")
        if '"enemy_units"' in line
    )
    print(f"AUDIT PASSED")
    print(f"  chapters: 20")
    print(f"  unit IDs referenced: {len(referenced_ids)}")
    print(f"  weapon IDs referenced: {len(used_weapons)}")
    print(f"  enemy placements total: {total_enemies}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
