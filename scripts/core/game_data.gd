## Global game data — persists across scenes. Autoloaded as GameData.
extends Node

# ── Game settings ────────────────────────────────────────────────────────────
var classic_mode: bool = true
var deploy_mode: int = Constants.DeployMode.FORCED

# ── Economy ──────────────────────────────────────────────────────────────────
var gold: int = 0

# ── Chapter progression ─────────────────────────────────────────────────────
var chapter_index: int = 0
var turn_number: int = 1

# ── Unit roster (all unlocked units across the campaign) ─────────────────────
var roster: Dictionary = {}        # unit_id → UnitData resource
var casualty_list: Array = []      # unit_ids lost in classic mode

# ── Current battle state ─────────────────────────────────────────────────────
var current_state: int = Constants.GameState.TITLE
var cursor_pos: Vector2i = Vector2i.ZERO
var cursor_mode: int = Constants.CursorMode.FREE
var selected_unit: Node = null

# ── Tutorial ─────────────────────────────────────────────────────────────────
var tutorial_active: bool = false
var tutorial_stage: int = 0
var in_tutorial: bool = false

# ── Combat log ───────────────────────────────────────────────────────────────
var combat_log: Array = []
var message_queue: Array[String] = []


func change_state(new_state: int) -> void:
	var old := current_state
	current_state = new_state
	EventBus.state_changed.emit(
		Constants.GameState.keys()[new_state],
		Constants.GameState.keys()[old])


func push_message(text: String) -> void:
	message_queue.append(text)
	EventBus.message_displayed.emit(text)


func pop_message() -> String:
	if message_queue.is_empty():
		return ""
	var msg := message_queue[0]
	message_queue.remove_at(0)
	EventBus.message_dismissed.emit()
	return msg


func reset_for_new_game() -> void:
	gold = 0
	chapter_index = 0
	turn_number = 1
	roster.clear()
	casualty_list.clear()
	combat_log.clear()
	message_queue.clear()
	tutorial_active = false
	tutorial_stage = 0
	in_tutorial = false
	cursor_pos = Vector2i.ZERO
	cursor_mode = Constants.CursorMode.FREE
	selected_unit = null
