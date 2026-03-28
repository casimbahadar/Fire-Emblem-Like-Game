## Global signal bus for decoupled communication between systems.
## Autoloaded as EventBus.
extends Node

# ── State transitions ────────────────────────────────────────────────────────
signal state_changed(new_state: String, old_state: String)

# ── Cursor & selection ───────────────────────────────────────────────────────
signal cursor_moved(grid_pos: Vector2i)
signal unit_selected(unit: Node)
signal unit_deselected()

# ── Unit actions ─────────────────────────────────────────────────────────────
signal unit_moved(unit: Node, from_pos: Vector2i, to_pos: Vector2i)
signal unit_attacked(attacker: Node, defender: Node)
signal unit_healed(healer: Node, target: Node, amount: int)
signal unit_waited(unit: Node)
signal unit_recruited(recruiter: Node, target: Node)
signal unit_defeated(unit: Node)

# ── Combat ───────────────────────────────────────────────────────────────────
signal combat_started(attacker: Node, defender: Node)
signal combat_finished(result: Dictionary)
signal combat_anim_finished()

# ── Turn management ──────────────────────────────────────────────────────────
signal turn_started(faction: int, turn_number: int)
signal turn_ended(faction: int)
signal phase_changed(faction: int)

# ── Chapter / game flow ──────────────────────────────────────────────────────
signal chapter_started(chapter_index: int)
signal chapter_victory()
signal chapter_defeat()
signal seize_point_captured(pos: Vector2i)

# ── Tutorial ─────────────────────────────────────────────────────────────────
signal tutorial_event(event_type: String)
signal tutorial_stage_advanced(stage_index: int)
signal tutorial_completed()
signal tutorial_skipped()

# ── UI ───────────────────────────────────────────────────────────────────────
signal message_displayed(text: String)
signal message_dismissed()
signal stat_sheet_opened(unit: Node)
signal stat_sheet_closed()
