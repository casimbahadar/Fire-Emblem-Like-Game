## Main game manager — state machine, input routing, game loop.
## Attached to the root Game node in game.tscn.
extends Node2D

# ── Node references (match game.tscn scene tree) ────────────────────────────
@onready var camera: Camera2D = $Camera2D
@onready var battle_map: Node2D = $BattleMap
@onready var terrain_layer: Node2D = $BattleMap/TerrainLayer
@onready var grid_lines: Node2D = $BattleMap/GridLines
@onready var overlay_layer: Node2D = $BattleMap/OverlayLayer
@onready var unit_layer: Node2D = $BattleMap/UnitLayer
@onready var cursor_layer: Node2D = $BattleMap/CursorLayer
@onready var damage_pop_layer: Node2D = $BattleMap/DamagePopLayer

# UI nodes
@onready var top_bar: PanelContainer = $UI/TopBar
@onready var turn_label: Label = $UI/TopBar/HBox/TurnLabel
@onready var chapter_label: Label = $UI/TopBar/HBox/ChapterLabel
@onready var phase_label: Label = $UI/TopBar/HBox/PhaseLabel
@onready var info_panel: PanelContainer = $UI/InfoPanel
@onready var info_name: Label = $UI/InfoPanel/MarginContainer/VBox/UnitName
@onready var info_class: Label = $UI/InfoPanel/MarginContainer/VBox/UnitClass
@onready var info_hp_bar: ProgressBar = $UI/InfoPanel/MarginContainer/VBox/HPBar
@onready var info_hp_label: Label = $UI/InfoPanel/MarginContainer/VBox/HPLabel
@onready var info_stats_grid: GridContainer = $UI/InfoPanel/MarginContainer/VBox/StatsGrid
@onready var info_terrain: Label = $UI/InfoPanel/MarginContainer/VBox/TerrainLabel
@onready var info_weapon: Label = $UI/InfoPanel/MarginContainer/VBox/WeaponLabel
@onready var message_box: PanelContainer = $UI/MessageBox
@onready var message_label: Label = $UI/MessageBox/MarginContainer/MessageLabel
@onready var action_menu: PanelContainer = $UI/ActionMenu
@onready var action_menu_vbox: VBoxContainer = $UI/ActionMenu/VBox

# Overlay layers
@onready var title_screen_layer: CanvasLayer = $TitleScreen
@onready var combat_anim_layer: CanvasLayer = $CombatAnimLayer
@onready var chapter_intro_layer: CanvasLayer = $ChapterIntroLayer

# ── Game systems ─────────────────────────────────────────────────────────────
var grid: Grid
var turn_manager: TurnManager
var ai: EnemyAI
var title_screen_script: Node = null  # title_screen.gd instance

# ── Unit lists (each entry is a Node2D with meta "unit_data") ────────────────
var player_units: Array = []
var enemy_units: Array = []
var ally_units: Array = []

# ── Interaction state ────────────────────────────────────────────────────────
var selected_unit: Node2D = null
var move_range: Array[Vector2i] = []
var move_range_land: Array[Vector2i] = []
var attack_range: Array[Vector2i] = []

# ── Cursor animation ────────────────────────────────────────────────────────
var _cursor_node: Node2D = null
var _cursor_time: float = 0.0

# ── Touch/drag ──────────────────────────────────────────────────────────────
var _touch_start: Vector2 = Vector2.ZERO
var _is_dragging: bool = false
const DRAG_THRESHOLD := 20.0

# ── Chapter intro state ─────────────────────────────────────────────────────
var _intro_showing: bool = false
var _intro_timer: float = 0.0
const INTRO_DURATION := 4.0

# ── Combat animation state ──────────────────────────────────────────────────
var _combat_animating: bool = false
var _combat_timer: float = 0.0
var _combat_result: Combat.CombatResult = null
var _combat_atk_node: Node2D = null
var _combat_def_node: Node2D = null

# ── Movement animation state ────────────────────────────────────────────────
var _move_animating: bool = false

# ── Phase banner state ──────────────────────────────────────────────────────
var _phase_banner: Label = null
var _phase_banner_showing: bool = false

# ── Danger zone ─────────────────────────────────────────────────────────────
var _danger_zone_visible: bool = false

# ── Stat sheet ──────────────────────────────────────────────────────────────
var _stat_sheet_visible: bool = false
var _stat_sheet_layer: CanvasLayer = null

# ── Move undo tracking ──────────────────────────────────────────────────────
var _pre_move_pos: Vector2i = Vector2i.ZERO

# ── Deploy / Shop screens ───────────────────────────────────────────────────
var _deploy_screen: Control = null
var _shop_screen: Control = null
var _deploy_layer: CanvasLayer = null
var _shop_layer: CanvasLayer = null


func _ready() -> void:
	grid = Grid.new()
	add_child(grid)
	turn_manager = TurnManager.new()

	# Build animated cursor
	_build_cursor()

	# Setup title screen
	_setup_title_screen()

	# Hide game UI initially
	battle_map.visible = false
	info_panel.visible = false
	message_box.visible = false
	action_menu.visible = false
	combat_anim_layer.visible = false
	chapter_intro_layer.visible = false

	# Connect signals
	EventBus.state_changed.connect(_on_state_changed)

	# Start at title
	_enter_title()


func _process(delta: float) -> void:
	# Cursor pulse animation
	_cursor_time += delta
	if _cursor_node:
		var pulse := 0.6 + 0.4 * sin(_cursor_time * 4.0)
		_cursor_node.modulate.a = pulse

	# Chapter intro timer
	if _intro_showing:
		_intro_timer += delta
		if _intro_timer >= INTRO_DURATION:
			_end_chapter_intro()

	# Combat animation timer
	if _combat_animating:
		_combat_timer += delta
		if _combat_timer >= 1.5:
			_finish_combat_anim()

	# Greyed-out units that have acted
	_update_unit_acted_visuals()


# ── Title screen ─────────────────────────────────────────────────────────────

func _setup_title_screen() -> void:
	# The TitleScreen CanvasLayer has the title_screen.gd script attached
	if title_screen_layer.has_signal("start_pressed"):
		title_screen_script = title_screen_layer
		title_screen_layer.start_pressed.connect(_start_new_game)
	else:
		title_screen_script = null


func _enter_title() -> void:
	GameData.change_state(Constants.GameState.TITLE)
	title_screen_layer.visible = true
	battle_map.visible = false
	info_panel.visible = false
	top_bar.visible = false
	if title_screen_script and title_screen_script.has_method("show_screen"):
		title_screen_script.show_screen()


# ── New game ─────────────────────────────────────────────────────────────────

func _start_new_game() -> void:
	title_screen_layer.visible = false
	if title_screen_script and title_screen_script.has_method("hide_screen"):
		title_screen_script.hide_screen()

	battle_map.visible = true
	top_bar.visible = true
	info_panel.visible = true

	# Initialize roster
	var roster_data = Roster.create_roster()
	GameData.roster = roster_data
	GameData.reset_for_new_game()

	_load_chapter(0)


func _continue_game() -> void:
	if not SaveSystem.has_save(0):
		_start_new_game()
		return

	title_screen_layer.visible = false
	if title_screen_script and title_screen_script.has_method("hide_screen"):
		title_screen_script.hide_screen()

	battle_map.visible = true
	top_bar.visible = true
	info_panel.visible = true

	if SaveSystem.load_game(0):
		_load_chapter(GameData.chapter_index)
	else:
		_start_new_game()


# ── Chapter loading ──────────────────────────────────────────────────────────

func _load_chapter(index: int) -> void:
	var ch: Dictionary = Chapters.get_chapter(index)
	GameData.chapter_index = index

	# Show deploy screen if there are enough units and deploy_limit is set
	var deploy_limit: int = ch.get("deploy_limit", 99)
	var available_count := 0
	for uid in GameData.roster:
		var u: UnitData = GameData.roster[uid]
		if u.faction == Constants.Faction.PLAYER and u.alive and uid not in GameData.casualty_list:
			available_count += 1

	if available_count > deploy_limit and deploy_limit < 99:
		_show_deploy_screen(ch)
	else:
		_start_chapter(ch)


func _show_deploy_screen(ch: Dictionary) -> void:
	_deploy_layer = CanvasLayer.new()
	_deploy_layer.layer = 12
	add_child(_deploy_layer)

	var deploy_script = load("res://scripts/ui/deploy_screen.gd")
	_deploy_screen = Control.new()
	_deploy_screen.set_script(deploy_script)
	_deploy_layer.add_child(_deploy_screen)
	_deploy_screen.setup(ch)
	_deploy_screen.deploy_confirmed.connect(_on_deploy_confirmed.bind(ch))


func _on_deploy_confirmed(selected_ids: Array, ch: Dictionary) -> void:
	# Store which units the player chose to deploy
	GameData.set_meta("deployed_units", selected_ids)
	if _deploy_layer:
		_deploy_layer.queue_free()
		_deploy_layer = null
		_deploy_screen = null
	_start_chapter(ch)


func _start_chapter(ch: Dictionary) -> void:
	# Setup grid
	grid.setup(ch.get("map_width", 12), ch.get("map_height", 10), ch.get("tiles", []))
	grid.seize_points.clear()
	for sp in ch.get("seize_points", []):
		if sp is Array:
			grid.seize_points.append(Vector2i(sp[0], sp[1]))
		elif sp is Vector2i:
			grid.seize_points.append(sp)

	# Clear old units
	for child in unit_layer.get_children():
		child.queue_free()
	player_units.clear()
	enemy_units.clear()
	ally_units.clear()

	# Get deployed unit IDs (if deploy screen was used)
	var deployed_ids: Array = []
	if GameData.has_meta("deployed_units"):
		deployed_ids = GameData.get_meta("deployed_units")

	# Spawn player units — only deployed ones if deploy screen was used
	for def in ch.get("player_units", []):
		var uid: String = str(def[0]) if def is Array else def.get("id", "")
		if deployed_ids.is_empty() or uid in deployed_ids:
			_spawn_unit(def, Constants.Faction.PLAYER)

	# Spawn enemy and ally units
	for def in ch.get("enemy_units", []):
		_spawn_unit(def, Constants.Faction.ENEMY)
	for def in ch.get("ally_units", []):
		_spawn_unit(def, Constants.Faction.ALLY)

	# Build terrain visuals
	_build_terrain_visuals()
	_build_grid_lines()

	# Setup AI
	ai = EnemyAI.new(grid, player_units, enemy_units, ally_units)

	# Start player turn
	turn_manager.reset()
	GameData.change_state(Constants.GameState.PLAYER_TURN)
	_reset_all_units(Constants.Faction.PLAYER)

	# Center camera on first player unit or map center
	if not player_units.is_empty():
		var first_data: UnitData = player_units[0].get_meta("unit_data")
		GameData.cursor_pos = first_data.grid_pos
	else:
		GameData.cursor_pos = Vector2i(grid.width / 2, grid.height / 2)
	_update_cursor()
	_center_camera_on_cursor()
	_update_top_bar()

	# Show chapter intro
	_show_chapter_intro(ch)
	EventBus.chapter_started.emit(GameData.chapter_index)


# ── Unit spawning ────────────────────────────────────────────────────────────

func _spawn_unit(def, faction: int) -> void:
	# def is ["unit_id", x, y] array or {"id": ..., "x": ..., "y": ...} dict
	var unit_id: String
	var gx: int
	var gy: int

	if def is Array:
		unit_id = str(def[0])
		gx = int(def[1])
		gy = int(def[2])
	elif def is Dictionary:
		unit_id = def.get("id", "")
		gx = def.get("x", 0)
		gy = def.get("y", 0)
	else:
		return

	var unit_data: UnitData
	if GameData.roster.has(unit_id):
		unit_data = GameData.roster[unit_id].duplicate()
	else:
		unit_data = UnitData.new()
		unit_data.unit_id = unit_id
		unit_data.name = unit_id.capitalize().replace("_", " ")

	unit_data.faction = faction
	unit_data.grid_pos = Vector2i(gx, gy)
	unit_data.alive = true
	unit_data.reset_turn()

	# Create visual node
	var unit_node := _create_unit_node(unit_data)
	unit_layer.add_child(unit_node)

	match faction:
		Constants.Faction.PLAYER: player_units.append(unit_node)
		Constants.Faction.ENEMY: enemy_units.append(unit_node)
		Constants.Faction.ALLY: ally_units.append(unit_node)


func _create_unit_node(data: UnitData) -> Node2D:
	var node := Node2D.new()
	node.name = data.unit_id
	node.position = grid.grid_to_pixel(data.grid_pos)
	node.set_meta("unit_data", data)

	var ts := float(Constants.TILE_SIZE)
	var half := ts / 2.0
	var inset := 3.0

	# Badge background (rounded feel via slightly smaller rect)
	var bg := ColorRect.new()
	bg.name = "Badge"
	bg.size = Vector2(ts - inset * 2, ts - inset * 2)
	bg.position = Vector2(-half + inset, -half + inset)
	bg.color = _get_faction_badge_color(data.faction)
	node.add_child(bg)

	# Border highlight (1px outline effect)
	var border := ColorRect.new()
	border.name = "Border"
	border.size = Vector2(ts - inset * 2 + 2, ts - inset * 2 + 2)
	border.position = Vector2(-half + inset - 1, -half + inset - 1)
	border.color = _get_faction_border_color(data.faction)
	border.z_index = -1
	node.add_child(border)

	# Symbol label
	var label := Label.new()
	label.name = "Symbol"
	label.text = Constants.CLASS_SYMBOLS.get(data.unit_class, "★")
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.size = Vector2(ts, ts)
	label.position = Vector2(-half, -half)
	label.add_theme_font_size_override("font_size", 18)
	node.add_child(label)

	# Mini HP bar under unit
	var hp_bg := ColorRect.new()
	hp_bg.name = "HPBarBG"
	hp_bg.size = Vector2(ts - inset * 2, 4)
	hp_bg.position = Vector2(-half + inset, half - inset - 4)
	hp_bg.color = Color(0, 0, 0, 0.7)
	node.add_child(hp_bg)

	var hp_fill := ColorRect.new()
	hp_fill.name = "HPBarFill"
	var hp_ratio := float(data.hp) / max(1, data.max_hp)
	hp_fill.size = Vector2((ts - inset * 2) * hp_ratio, 4)
	hp_fill.position = Vector2(-half + inset, half - inset - 4)
	hp_fill.color = _get_hp_color(data.faction)
	node.add_child(hp_fill)

	return node


func _get_faction_badge_color(faction: int) -> Color:
	match faction:
		Constants.Faction.PLAYER: return Color(0.15, 0.25, 0.55, 0.9)
		Constants.Faction.ENEMY: return Color(0.55, 0.12, 0.12, 0.9)
		Constants.Faction.ALLY: return Color(0.12, 0.45, 0.35, 0.9)
		_: return Color(0.3, 0.3, 0.3, 0.9)


func _get_faction_border_color(faction: int) -> Color:
	match faction:
		Constants.Faction.PLAYER: return Color(0.4, 0.6, 1.0, 0.8)
		Constants.Faction.ENEMY: return Color(1.0, 0.4, 0.4, 0.8)
		Constants.Faction.ALLY: return Color(0.4, 0.9, 0.7, 0.8)
		_: return Color(0.5, 0.5, 0.5, 0.8)


func _get_hp_color(faction: int) -> Color:
	match faction:
		Constants.Faction.PLAYER: return Color(0.24, 0.66, 0.33)
		Constants.Faction.ENEMY: return Color(0.75, 0.22, 0.17)
		Constants.Faction.ALLY: return Color(0.17, 0.62, 0.63)
		_: return Color.WHITE


# ── Terrain & grid visuals ───────────────────────────────────────────────────

func _build_terrain_visuals() -> void:
	for child in terrain_layer.get_children():
		child.queue_free()

	var ts := float(Constants.TILE_SIZE)

	for y in range(grid.height):
		for x in range(grid.width):
			var terrain := grid.get_terrain(Vector2i(x, y))
			var base_color: Color = Constants.TERRAIN_COLORS.get(terrain, Color.GRAY)

			# Slight variation for visual interest
			var noise_val := sin(float(x) * 3.7 + float(y) * 2.3) * 0.04
			var color := Color(
				clampf(base_color.r + noise_val, 0, 1),
				clampf(base_color.g + noise_val * 0.5, 0, 1),
				clampf(base_color.b - noise_val, 0, 1))

			var rect := ColorRect.new()
			rect.size = Vector2(ts, ts)
			rect.position = Vector2(x * ts, y * ts)
			rect.color = color
			terrain_layer.add_child(rect)

			# Special markers for terrain features
			if terrain == Constants.Terrain.FORT or terrain == Constants.Terrain.CASTLE:
				var marker := ColorRect.new()
				marker.size = Vector2(ts * 0.4, ts * 0.4)
				marker.position = Vector2(x * ts + ts * 0.3, y * ts + ts * 0.3)
				marker.color = Color(0.6, 0.5, 0.3, 0.5)
				terrain_layer.add_child(marker)

	# Seize point markers with gold glow
	for sp in grid.seize_points:
		var glow := ColorRect.new()
		glow.size = Vector2(ts, ts)
		glow.position = Vector2(sp.x * ts, sp.y * ts)
		glow.color = Color(0.85, 0.65, 0.13, 0.35)
		terrain_layer.add_child(glow)

		# Inner diamond marker
		var inner := ColorRect.new()
		inner.size = Vector2(ts * 0.5, ts * 0.5)
		inner.position = Vector2(sp.x * ts + ts * 0.25, sp.y * ts + ts * 0.25)
		inner.color = Color(0.85, 0.65, 0.13, 0.6)
		terrain_layer.add_child(inner)


func _build_grid_lines() -> void:
	for child in grid_lines.get_children():
		child.queue_free()

	var ts := float(Constants.TILE_SIZE)

	# Vertical lines
	for x in range(grid.width + 1):
		var line := ColorRect.new()
		line.size = Vector2(1, grid.height * ts)
		line.position = Vector2(x * ts, 0)
		line.color = Color(1, 1, 1, 0.08)
		grid_lines.add_child(line)

	# Horizontal lines
	for y in range(grid.height + 1):
		var line := ColorRect.new()
		line.size = Vector2(grid.width * ts, 1)
		line.position = Vector2(0, y * ts)
		line.color = Color(1, 1, 1, 0.08)
		grid_lines.add_child(line)


# ── Cursor ───────────────────────────────────────────────────────────────────

func _build_cursor() -> void:
	_cursor_node = Node2D.new()
	_cursor_node.name = "CursorAnim"
	_cursor_node.z_index = 10

	var ts := float(Constants.TILE_SIZE)
	var corner_len := 10.0
	var thickness := 2.0
	var gold := Color(0.85, 0.65, 0.13, 1.0)

	# Top-left corner
	_add_cursor_line(_cursor_node, Vector2(0, 0), Vector2(corner_len, 0), thickness, gold)
	_add_cursor_line(_cursor_node, Vector2(0, 0), Vector2(0, corner_len), thickness, gold)
	# Top-right corner
	_add_cursor_line(_cursor_node, Vector2(ts, 0), Vector2(ts - corner_len, 0), thickness, gold)
	_add_cursor_line(_cursor_node, Vector2(ts, 0), Vector2(ts, corner_len), thickness, gold)
	# Bottom-left corner
	_add_cursor_line(_cursor_node, Vector2(0, ts), Vector2(corner_len, ts), thickness, gold)
	_add_cursor_line(_cursor_node, Vector2(0, ts), Vector2(0, ts - corner_len), thickness, gold)
	# Bottom-right corner
	_add_cursor_line(_cursor_node, Vector2(ts, ts), Vector2(ts - corner_len, ts), thickness, gold)
	_add_cursor_line(_cursor_node, Vector2(ts, ts), Vector2(ts, ts - corner_len), thickness, gold)

	cursor_layer.add_child(_cursor_node)


func _add_cursor_line(parent: Node2D, from: Vector2, to: Vector2, thickness: float, color: Color) -> void:
	var line := Line2D.new()
	line.add_point(from)
	line.add_point(to)
	line.width = thickness
	line.default_color = color
	parent.add_child(line)


func _update_cursor() -> void:
	if _cursor_node:
		var ts := float(Constants.TILE_SIZE)
		_cursor_node.position = Vector2(
			GameData.cursor_pos.x * ts,
			GameData.cursor_pos.y * ts)

	# Update info panel with what's under cursor
	_update_info_panel(GameData.cursor_pos)


# ── Input handling ───────────────────────────────────────────────────────────

func _unhandled_input(event: InputEvent) -> void:
	# Block input during animations
	if _intro_showing or _combat_animating or _move_animating or _phase_banner_showing:
		if event is InputEventKey and event.pressed:
			if _intro_showing:
				_end_chapter_intro()
			elif _combat_animating:
				_finish_combat_anim()
		return

	# Stat sheet takes priority
	if _stat_sheet_visible:
		if (event is InputEventKey and event.pressed) or \
		   (event is InputEventMouseButton and event.pressed) or \
		   (event is InputEventScreenTouch and not event.pressed):
			_close_stat_sheet()
		return

	# Keyboard input
	if event is InputEventKey and event.pressed:
		match GameData.current_state:
			Constants.GameState.TITLE:
				_handle_title_input(event)
			Constants.GameState.PLAYER_TURN:
				_handle_player_input(event)
			Constants.GameState.VICTORY:
				_handle_victory_input(event)
			Constants.GameState.GAME_OVER:
				_handle_gameover_input(event)

	# Mouse click
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		match GameData.current_state:
			Constants.GameState.TITLE:
				_start_new_game()
			Constants.GameState.PLAYER_TURN:
				_handle_map_click(event.position)
			Constants.GameState.VICTORY:
				_advance_chapter()
			Constants.GameState.GAME_OVER:
				_load_chapter(GameData.chapter_index)

	# Touch input for mobile
	if event is InputEventScreenTouch:
		if event.pressed:
			_touch_start = event.position
			_is_dragging = false
		else:
			if not _is_dragging:
				# Tap — treat as click
				match GameData.current_state:
					Constants.GameState.TITLE:
						_start_new_game()
					Constants.GameState.PLAYER_TURN:
						_handle_map_click(event.position)
					Constants.GameState.VICTORY:
						_advance_chapter()
					Constants.GameState.GAME_OVER:
						_load_chapter(GameData.chapter_index)

	if event is InputEventScreenDrag:
		if event.position.distance_to(_touch_start) > DRAG_THRESHOLD:
			_is_dragging = true
			# Pan camera with touch drag
			camera.position -= event.relative / camera.zoom


func _handle_title_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		_start_new_game()


func _handle_player_input(event: InputEvent) -> void:
	# Action menu is open — handle menu input
	if action_menu.visible:
		_handle_action_menu_input(event)
		return

	# Messages take priority
	if not GameData.message_queue.is_empty():
		if event.is_action_pressed("confirm") or event.is_action_pressed("cancel"):
			GameData.pop_message()
			_update_message_box()
		return

	# Directional movement
	if event.is_action_pressed("move_up"):
		_move_cursor(Vector2i(0, -1))
	elif event.is_action_pressed("move_down"):
		_move_cursor(Vector2i(0, 1))
	elif event.is_action_pressed("move_left"):
		_move_cursor(Vector2i(-1, 0))
	elif event.is_action_pressed("move_right"):
		_move_cursor(Vector2i(1, 0))
	elif event.is_action_pressed("confirm"):
		_handle_confirm()
	elif event.is_action_pressed("cancel"):
		if _danger_zone_visible:
			_hide_danger_zone()
		else:
			_reset_interaction()
	elif event.is_action_pressed("end_turn"):
		_end_player_turn()
	elif event.is_action_pressed("info"):
		_toggle_stat_sheet()
	elif event.is_action_pressed("attack"):
		_toggle_danger_zone()


func _move_cursor(delta: Vector2i) -> void:
	var new_pos := GameData.cursor_pos + delta
	new_pos.x = clampi(new_pos.x, 0, grid.width - 1)
	new_pos.y = clampi(new_pos.y, 0, grid.height - 1)
	GameData.cursor_pos = new_pos
	_update_cursor()
	_center_camera_on_cursor()
	EventBus.cursor_moved.emit(new_pos)


# ── Confirm / select / move ──────────────────────────────────────────────────

func _handle_confirm() -> void:
	var pos := GameData.cursor_pos

	if GameData.cursor_mode == Constants.CursorMode.FREE:
		var unit_node := _unit_at(pos)
		if unit_node:
			var data: UnitData = unit_node.get_meta("unit_data")
			if data.faction == Constants.Faction.PLAYER and data.alive and not data.has_acted:
				_select_unit(unit_node)
			elif data.alive:
				# Show info for non-player units
				_update_info_panel_for_unit(data)

	elif GameData.cursor_mode == Constants.CursorMode.UNIT_SELECTED:
		if pos in move_range_land:
			_move_selected_unit(pos)
		else:
			_reset_interaction()


func _select_unit(unit_node: Node2D) -> void:
	selected_unit = unit_node
	var data: UnitData = unit_node.get_meta("unit_data")
	GameData.cursor_mode = Constants.CursorMode.UNIT_SELECTED
	GameData.selected_unit = unit_node

	# Compute movement range
	if data.has_moved:
		move_range = []
		move_range_land = [data.grid_pos]
	else:
		move_range = grid.get_movement_range(
			data.grid_pos, data.mov, data.unit_class,
			data.is_flying, data.is_mounted, data.water_walk)
		var occupied := {}
		for u in player_units + ally_units:
			var ud: UnitData = u.get_meta("unit_data")
			if ud.alive and ud != data:
				occupied[ud.grid_pos] = true
		for u in enemy_units:
			var ud: UnitData = u.get_meta("unit_data")
			if ud.alive:
				occupied[ud.grid_pos] = true
		move_range_land = move_range.filter(func(t): return not occupied.has(t))
		if not data.grid_pos in move_range_land:
			move_range_land.append(data.grid_pos)

	# Attack range
	var range_vec := data.attack_range()
	attack_range = grid.get_attack_range(move_range_land, range_vec.x, range_vec.y)

	_draw_range_overlay()
	_update_info_panel_for_unit(data)
	EventBus.unit_selected.emit(unit_node)


func _move_selected_unit(pos: Vector2i) -> void:
	if not selected_unit:
		return
	var data: UnitData = selected_unit.get_meta("unit_data")
	_pre_move_pos = data.grid_pos
	var old_pos := data.grid_pos
	data.grid_pos = pos
	data.has_moved = true
	_clear_overlay()

	# Animate movement along path
	_move_animating = true
	var path := _build_move_path(old_pos, pos)
	await _animate_unit_along_path(selected_unit, path)
	_move_animating = false

	_update_unit_hp_bar(selected_unit)
	EventBus.unit_moved.emit(selected_unit, old_pos, pos)

	# Show action menu
	_show_action_menu(data)


func _build_move_path(from: Vector2i, to: Vector2i) -> Array[Vector2i]:
	# Simple straight-line path stepping one tile at a time
	var path: Array[Vector2i] = [from]
	var current := from
	while current != to:
		var dx := signi(to.x - current.x)
		var dy := signi(to.y - current.y)
		# Prefer horizontal then vertical
		if dx != 0:
			current = Vector2i(current.x + dx, current.y)
		elif dy != 0:
			current = Vector2i(current.x, current.y + dy)
		path.append(current)
	return path


func _animate_unit_along_path(unit_node: Node2D, path: Array[Vector2i]) -> void:
	if path.size() <= 1:
		unit_node.position = grid.grid_to_pixel(path[-1] if not path.is_empty() else Vector2i.ZERO)
		return
	var speed := 0.08  # seconds per tile
	for i in range(1, path.size()):
		var target_pixel := grid.grid_to_pixel(path[i])
		var tween := create_tween()
		tween.tween_property(unit_node, "position", target_pixel, speed)
		await tween.finished


# ── Action menu ──────────────────────────────────────────────────────────────

func _show_action_menu(data: UnitData) -> void:
	# Clear old buttons
	for child in action_menu_vbox.get_children():
		child.queue_free()

	var actions: Array[String] = []

	# Check for attack targets
	var targets := _get_attackable_targets(data)
	if not targets.is_empty():
		actions.append("Attack")

	# Check for heal targets
	if data.equipped.get("weapon_type", -1) == Constants.WeaponType.STAFF:
		var heal_targets := _get_heal_targets(data)
		if not heal_targets.is_empty():
			actions.append("Heal")

	# Talk / Recruit check
	var talk_targets := _get_talk_targets(data)
	if not talk_targets.is_empty():
		actions.append("Talk")

	# Seize check
	if data.grid_pos in grid.seize_points:
		actions.append("Seize")

	# Weapon switch (if unit has multiple weapons)
	if data.weapons.size() > 1:
		actions.append("Weapon")

	actions.append("Wait")

	for action_name in actions:
		var btn := Button.new()
		btn.text = action_name
		btn.pressed.connect(_on_action_selected.bind(action_name))
		action_menu_vbox.add_child(btn)

	action_menu.visible = true


func _handle_action_menu_input(event: InputEvent) -> void:
	if event.is_action_pressed("cancel"):
		_close_action_menu()
		# Undo move — restore to pre-move position
		if selected_unit:
			var data: UnitData = selected_unit.get_meta("unit_data")
			data.grid_pos = _pre_move_pos
			data.has_moved = false
			selected_unit.position = grid.grid_to_pixel(_pre_move_pos)
		_reset_interaction()


func _on_action_selected(action_name: String) -> void:
	action_menu.visible = false
	if not selected_unit:
		return

	var data: UnitData = selected_unit.get_meta("unit_data")

	match action_name:
		"Attack":
			_handle_attack_action()
		"Heal":
			_handle_heal_action()
		"Talk":
			_handle_talk_action()
		"Seize":
			_handle_seize_action()
		"Weapon":
			_handle_weapon_switch()
		"Wait":
			_handle_wait_action()


func _close_action_menu() -> void:
	action_menu.visible = false


# ── Combat actions ───────────────────────────────────────────────────────────

func _handle_attack_action() -> void:
	if not selected_unit:
		return
	var data: UnitData = selected_unit.get_meta("unit_data")
	if data.has_acted:
		return

	var targets := _get_attackable_targets(data)
	if targets.is_empty():
		return

	# Attack first available target
	var target_node: Node2D = targets[0]
	var target_data: UnitData = target_node.get_meta("unit_data")
	_start_combat(data, target_data, selected_unit, target_node)


func _start_combat(atk_data: UnitData, def_data: UnitData, atk_node: Node2D, def_node: Node2D) -> void:
	var terrain_att := grid.get_terrain(atk_data.grid_pos)
	var terrain_def := grid.get_terrain(def_data.grid_pos)
	var result := Combat.resolve(atk_data, def_data, terrain_att, terrain_def)

	# Show combat animation
	_show_combat_anim(atk_data, def_data, result)
	_combat_result = result
	_combat_atk_node = atk_node
	_combat_def_node = def_node


func _show_combat_anim(atk: UnitData, dfn: UnitData, result: Combat.CombatResult) -> void:
	combat_anim_layer.visible = true
	_combat_animating = true
	_combat_timer = 0.0

	# Clear old combat UI
	var bg: ColorRect = combat_anim_layer.get_node("BG")
	for child in bg.get_children():
		child.queue_free()

	var vp_size := get_viewport().get_visible_rect().size

	# Attacker panel (left side)
	var atk_panel := _create_combat_panel(atk, false, Vector2(60, vp_size.y * 0.3))
	bg.add_child(atk_panel)

	# Defender panel (right side)
	var def_panel := _create_combat_panel(dfn, true, Vector2(vp_size.x - 260, vp_size.y * 0.3))
	bg.add_child(def_panel)

	# "VS" label
	var vs := Label.new()
	vs.text = "VS"
	vs.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vs.position = Vector2(vp_size.x / 2 - 30, vp_size.y * 0.4)
	vs.size = Vector2(60, 40)
	vs.add_theme_font_size_override("font_size", 28)
	vs.add_theme_color_override("font_color", Color(0.85, 0.65, 0.13))
	bg.add_child(vs)

	# Show round results
	var results_y := vp_size.y * 0.55
	for i in range(result.rounds.size()):
		var rnd: Combat.RoundResult = result.rounds[i]
		var lbl := Label.new()
		var hit_text := "HIT %d" % rnd.damage if rnd.hit else "MISS"
		if rnd.crit:
			hit_text = "CRIT! %d" % rnd.damage
		var arrow := " → " if not rnd.is_counter else " ← "
		lbl.text = "%s%s%s" % [rnd.attacker_name, arrow, hit_text]
		lbl.position = Vector2(vp_size.x / 2 - 150, results_y + i * 30)
		lbl.size = Vector2(300, 28)
		lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lbl.add_theme_font_size_override("font_size", 16)
		if rnd.crit:
			lbl.add_theme_color_override("font_color", Color(1.0, 0.85, 0.2))
		elif not rnd.hit:
			lbl.add_theme_color_override("font_color", Color(0.6, 0.6, 0.6))
		bg.add_child(lbl)


func _create_combat_panel(data: UnitData, is_right: bool, pos: Vector2) -> PanelContainer:
	var panel := PanelContainer.new()
	panel.position = pos
	panel.size = Vector2(200, 180)

	var vbox := VBoxContainer.new()
	panel.add_child(vbox)

	var name_lbl := Label.new()
	name_lbl.text = data.name
	name_lbl.add_theme_font_size_override("font_size", 18)
	name_lbl.add_theme_color_override("font_color", Color(0.85, 0.65, 0.13))
	name_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vbox.add_child(name_lbl)

	var class_lbl := Label.new()
	class_lbl.text = data.unit_class
	class_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vbox.add_child(class_lbl)

	var hp_lbl := Label.new()
	hp_lbl.text = "HP: %d / %d" % [data.hp, data.max_hp]
	hp_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vbox.add_child(hp_lbl)

	var stat_lbl := Label.new()
	stat_lbl.text = "ATK:%d  DEF:%d  SPD:%d" % [data.attack_power(), data.defense(), data.spd]
	stat_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	stat_lbl.add_theme_font_size_override("font_size", 12)
	vbox.add_child(stat_lbl)

	if not data.equipped.is_empty():
		var wep_lbl := Label.new()
		wep_lbl.text = data.equipped.get("name", "Unarmed")
		wep_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		wep_lbl.add_theme_font_size_override("font_size", 12)
		wep_lbl.add_theme_color_override("font_color", Color(0.7, 0.7, 0.7))
		vbox.add_child(wep_lbl)

	return panel


func _finish_combat_anim() -> void:
	_combat_animating = false
	combat_anim_layer.visible = false

	if not _combat_result:
		return

	var atk_data: UnitData = _combat_atk_node.get_meta("unit_data") if _combat_atk_node else null
	var def_data: UnitData = _combat_def_node.get_meta("unit_data") if _combat_def_node else null

	# Handle deaths and damage popups
	if def_data and not def_data.alive:
		_combat_def_node.visible = false
		_spawn_damage_popup(def_data.grid_pos, "DEFEATED", Color(1, 0.3, 0.3))
		GameData.push_message("%s was defeated!" % def_data.name)
		EventBus.unit_defeated.emit(_combat_def_node)
	elif def_data and _combat_result.rounds.size() > 0:
		var total_dmg := 0
		for rnd in _combat_result.rounds:
			if rnd.hit and not rnd.is_counter:
				total_dmg += rnd.damage
		if total_dmg > 0:
			_spawn_damage_popup(def_data.grid_pos, str(total_dmg), Color(1, 1, 1))
		_update_unit_hp_bar(_combat_def_node)

	if atk_data and not atk_data.alive:
		_combat_atk_node.visible = false
		_spawn_damage_popup(atk_data.grid_pos, "DEFEATED", Color(1, 0.3, 0.3))
		GameData.push_message("%s was defeated!" % atk_data.name)
		EventBus.unit_defeated.emit(_combat_atk_node)
	elif atk_data:
		var counter_dmg := 0
		for rnd in _combat_result.rounds:
			if rnd.hit and rnd.is_counter:
				counter_dmg += rnd.damage
		if counter_dmg > 0:
			_spawn_damage_popup(atk_data.grid_pos, str(counter_dmg), Color(1, 1, 1))
		_update_unit_hp_bar(_combat_atk_node)

	# Level up messages
	if _combat_result.level_up_att and atk_data:
		GameData.push_message("%s leveled up!" % atk_data.name)
	if _combat_result.level_up_def and def_data:
		GameData.push_message("%s leveled up!" % def_data.name)

	if atk_data:
		atk_data.done()

	_combat_result = null
	_combat_atk_node = null
	_combat_def_node = null
	_reset_interaction()
	_update_message_box()
	_check_victory()
	_check_defeat()


# ── Heal / Wait / Seize actions ──────────────────────────────────────────────

func _handle_heal_action() -> void:
	if not selected_unit:
		return
	var data: UnitData = selected_unit.get_meta("unit_data")
	if data.has_acted or data.equipped.is_empty():
		return
	if data.equipped.get("weapon_type", -1) != Constants.WeaponType.STAFF:
		return

	var heal_targets := _get_heal_targets(data)
	if heal_targets.is_empty():
		return

	var target_node: Node2D = heal_targets[0]
	var ud: UnitData = target_node.get_meta("unit_data")
	var amount := Combat.resolve_heal(data, ud)
	_spawn_damage_popup(ud.grid_pos, "+%d" % amount, Color(0.3, 1.0, 0.4))
	_update_unit_hp_bar(target_node)
	GameData.push_message("%s healed %s for %d HP!" % [data.name, ud.name, amount])
	data.done()
	_reset_interaction()
	_update_message_box()
	EventBus.unit_healed.emit(selected_unit, target_node, amount)


func _handle_wait_action() -> void:
	if not selected_unit:
		return
	var data: UnitData = selected_unit.get_meta("unit_data")
	data.done()
	_reset_interaction()
	EventBus.unit_waited.emit(selected_unit)


func _handle_seize_action() -> void:
	if not selected_unit:
		return
	var data: UnitData = selected_unit.get_meta("unit_data")
	if data.grid_pos in grid.seize_points:
		GameData.push_message("Victory! Point seized!")
		GameData.change_state(Constants.GameState.VICTORY)
		EventBus.seize_point_captured.emit(data.grid_pos)
		EventBus.chapter_victory.emit()
		_update_message_box()


# ── End turn / Enemy AI ──────────────────────────────────────────────────────

func _end_player_turn() -> void:
	for u in player_units:
		var data: UnitData = u.get_meta("unit_data")
		if data.alive:
			data.done()
	_reset_interaction()

	# Check side objectives at end of player turn
	_check_side_objectives()
	_update_message_box()

	GameData.change_state(Constants.GameState.ENEMY_TURN)
	turn_manager.end_player_turn()
	_update_top_bar()

	# Show enemy phase banner then run AI
	_show_phase_banner("Enemy Phase", Color(1.0, 0.4, 0.4))
	await get_tree().create_timer(1.5).timeout
	_run_enemy_turn()


func _run_enemy_turn() -> void:
	# Reset enemy units
	for u in enemy_units:
		var data: UnitData = u.get_meta("unit_data")
		if data.alive:
			data.reset_turn()

	# Update AI references
	ai.player_units = _get_alive_unit_data(player_units)
	ai.enemy_units = _get_alive_unit_data(enemy_units)
	ai.ally_units = _get_alive_unit_data(ally_units)
	var actions := ai.run_turn()

	# Apply AI actions one at a time with visual pacing
	for action in actions:
		var unit_data = action.get("unit", null)
		if not unit_data:
			continue

		var unit_node: Node2D = _find_node_for_data(unit_data, enemy_units)
		if not unit_node:
			continue

		# Animate movement
		var move_to = action.get("move_to", null)
		if move_to and move_to is Vector2i:
			var old_pos := unit_node.position
			var path := _build_move_path(
				grid.pixel_to_grid(old_pos), move_to)
			await _animate_unit_along_path(unit_node, path)

		_update_unit_hp_bar(unit_node)

		if action.get("type", "") == "attack":
			var target = action.get("target", null)
			if target:
				var terrain_att := grid.get_terrain(unit_data.grid_pos)
				var terrain_def := grid.get_terrain(target.grid_pos)
				var result := Combat.resolve(unit_data, target, terrain_att, terrain_def)

				# Show damage on targets
				if not target.alive:
					var target_node := _find_node_for_data(target, player_units + ally_units)
					if target_node:
						target_node.visible = false
						_spawn_damage_popup(target.grid_pos, "DEFEATED", Color(1, 0.3, 0.3))
				else:
					var target_node := _find_node_for_data(target, player_units + ally_units)
					if target_node:
						# Show damage number
						var total_dmg := 0
						for rnd in result.rounds:
							if rnd.hit and not rnd.is_counter:
								total_dmg += rnd.damage
						if total_dmg > 0:
							_spawn_damage_popup(target.grid_pos, str(total_dmg), Color(1, 0.6, 0.6))
						_update_unit_hp_bar(target_node)

				# Show counter damage on attacker
				if not unit_data.alive:
					unit_node.visible = false
					_spawn_damage_popup(unit_data.grid_pos, "DEFEATED", Color(1, 0.3, 0.3))
				else:
					var counter_dmg := 0
					for rnd in result.rounds:
						if rnd.hit and rnd.is_counter:
							counter_dmg += rnd.damage
					if counter_dmg > 0:
						_spawn_damage_popup(unit_data.grid_pos, str(counter_dmg), Color(1, 0.6, 0.6))
					_update_unit_hp_bar(unit_node)

		# Brief pause between each enemy action
		await get_tree().create_timer(0.4).timeout

	_check_defeat()

	# Start next player turn
	for u in player_units:
		var data: UnitData = u.get_meta("unit_data")
		if data.alive:
			data.reset_turn()

	turn_manager.turn_number += 1
	GameData.change_state(Constants.GameState.PLAYER_TURN)
	turn_manager.start_player_turn()
	_update_top_bar()

	# Show player phase banner
	_show_phase_banner("Player Phase", Color(0.4, 0.6, 1.0))


# ── Victory / Defeat / Chapter advance ───────────────────────────────────────

func _check_victory() -> void:
	var enemies_alive := enemy_units.filter(func(u): return u.get_meta("unit_data").alive)
	if enemies_alive.is_empty():
		GameData.push_message("All enemies defeated! Victory!")
		GameData.change_state(Constants.GameState.VICTORY)
		EventBus.chapter_victory.emit()
		_update_message_box()


func _check_defeat() -> void:
	for u in player_units:
		var data: UnitData = u.get_meta("unit_data")
		if data.unit_class == Constants.CLASS_LORD and not data.alive:
			GameData.push_message("%s has fallen! Defeat..." % data.name)
			GameData.change_state(Constants.GameState.GAME_OVER)
			EventBus.chapter_defeat.emit()
			_update_message_box()
			return


func _handle_victory_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		_advance_chapter()


func _advance_chapter() -> void:
	# Award gold for completing chapter
	GameData.gold += Constants.GOLD_PER_CHAPTER

	# Save progress after each chapter
	SaveSystem.save_game(0)

	# Sync surviving unit stats back to roster
	for u in player_units:
		var data: UnitData = u.get_meta("unit_data")
		if data.alive:
			GameData.roster[data.unit_id] = data

	if GameData.chapter_index + 1 < Chapters.chapter_count():
		# Show shop between chapters
		_show_shop_screen()
	else:
		GameData.push_message("Congratulations! You have completed Sengoku Tactics!")
		_update_message_box()
		await get_tree().create_timer(3.0).timeout
		_enter_title()


func _show_shop_screen() -> void:
	_shop_layer = CanvasLayer.new()
	_shop_layer.layer = 12
	add_child(_shop_layer)

	var shop_script = load("res://scripts/ui/shop_screen.gd")
	_shop_screen = Control.new()
	_shop_screen.set_script(shop_script)
	_shop_layer.add_child(_shop_screen)
	_shop_screen.setup()
	_shop_screen.shop_closed.connect(_on_shop_closed)


func _on_shop_closed() -> void:
	if _shop_layer:
		_shop_layer.queue_free()
		_shop_layer = null
		_shop_screen = null
	_load_chapter(GameData.chapter_index + 1)


func _handle_gameover_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		_load_chapter(GameData.chapter_index)


func _handle_map_click(screen_pos: Vector2) -> void:
	# Convert screen position to world position
	var world_pos := get_global_mouse_position()
	var grid_pos := grid.pixel_to_grid(world_pos)
	if grid.is_valid(grid_pos):
		GameData.cursor_pos = grid_pos
		_update_cursor()

		if action_menu.visible:
			return  # Don't process map clicks while menu is open

		_handle_confirm()


# ── Helpers ──────────────────────────────────────────────────────────────────

func _reset_interaction() -> void:
	selected_unit = null
	GameData.cursor_mode = Constants.CursorMode.FREE
	GameData.selected_unit = null
	move_range.clear()
	move_range_land.clear()
	attack_range.clear()
	_clear_overlay()
	action_menu.visible = false
	EventBus.unit_deselected.emit()


func _unit_at(pos: Vector2i) -> Node2D:
	for u in player_units + enemy_units + ally_units:
		var data: UnitData = u.get_meta("unit_data")
		if data.alive and data.grid_pos == pos:
			return u
	return null


func _get_attackable_targets(data: UnitData) -> Array:
	if data.equipped.is_empty():
		return []
	var range_vec := data.attack_range()
	var targets: Array = []
	for u in enemy_units:
		var ud: UnitData = u.get_meta("unit_data")
		if not ud.alive:
			continue
		var dist := absi(data.grid_pos.x - ud.grid_pos.x) + absi(data.grid_pos.y - ud.grid_pos.y)
		if dist >= range_vec.x and dist <= range_vec.y:
			targets.append(u)
	return targets


func _get_heal_targets(data: UnitData) -> Array:
	var targets: Array = []
	for dir in [Vector2i.UP, Vector2i.DOWN, Vector2i.LEFT, Vector2i.RIGHT]:
		var adj := data.grid_pos + dir
		var unit_node := _unit_at(adj)
		if unit_node:
			var ud: UnitData = unit_node.get_meta("unit_data")
			if ud.faction == data.faction and ud.alive and ud.hp < ud.max_hp:
				targets.append(unit_node)
	return targets


func _reset_all_units(faction: int) -> void:
	var list: Array
	match faction:
		Constants.Faction.PLAYER: list = player_units
		Constants.Faction.ENEMY: list = enemy_units
		Constants.Faction.ALLY: list = ally_units
		_: return
	for u in list:
		var data: UnitData = u.get_meta("unit_data")
		if data.alive:
			data.reset_turn()


func _get_alive_unit_data(unit_list: Array) -> Array:
	var result: Array = []
	for u in unit_list:
		var data: UnitData = u.get_meta("unit_data")
		if data.alive:
			result.append(data)
	return result


func _find_node_for_data(data, unit_list: Array) -> Node2D:
	for u in unit_list:
		if u.get_meta("unit_data") == data:
			return u
	return null


func _center_camera_on_cursor() -> void:
	var target := grid.grid_to_pixel(GameData.cursor_pos)
	camera.position = target


# ── Overlay drawing ──────────────────────────────────────────────────────────

func _draw_range_overlay() -> void:
	_clear_overlay()
	var ts := float(Constants.TILE_SIZE)

	for pos in move_range_land:
		var rect := ColorRect.new()
		rect.size = Vector2(ts, ts)
		rect.position = Vector2(pos.x * ts, pos.y * ts)
		rect.color = Color(0.2, 0.5, 1.0, 0.3)
		overlay_layer.add_child(rect)

	for pos in attack_range:
		if pos in move_range_land:
			continue
		var rect := ColorRect.new()
		rect.size = Vector2(ts, ts)
		rect.position = Vector2(pos.x * ts, pos.y * ts)
		rect.color = Color(1.0, 0.2, 0.2, 0.25)
		overlay_layer.add_child(rect)


func _clear_overlay() -> void:
	for child in overlay_layer.get_children():
		child.queue_free()


# ── UI updates ───────────────────────────────────────────────────────────────

func _update_top_bar() -> void:
	turn_label.text = "Turn %d" % turn_manager.turn_number
	chapter_label.text = "Ch.%d" % (GameData.chapter_index + 1)
	match GameData.current_state:
		Constants.GameState.PLAYER_TURN:
			phase_label.text = "Player Phase"
			phase_label.add_theme_color_override("font_color", Color(0.4, 0.6, 1.0))
		Constants.GameState.ENEMY_TURN:
			phase_label.text = "Enemy Phase"
			phase_label.add_theme_color_override("font_color", Color(1.0, 0.4, 0.4))
		Constants.GameState.ALLY_TURN:
			phase_label.text = "Ally Phase"
			phase_label.add_theme_color_override("font_color", Color(0.4, 0.9, 0.6))
		_:
			phase_label.text = ""


func _update_info_panel(pos: Vector2i) -> void:
	var unit_node := _unit_at(pos)
	if unit_node:
		var data: UnitData = unit_node.get_meta("unit_data")
		_update_info_panel_for_unit(data)
	else:
		# Show terrain info only
		var terrain := grid.get_terrain(pos)
		var tname: String = Constants.TERRAIN_NAMES.get(terrain, "???")
		var tdata: Dictionary = Constants.TERRAIN_DATA.get(terrain, {})
		info_name.text = ""
		info_class.text = ""
		info_hp_bar.visible = false
		info_hp_label.text = ""
		info_terrain.text = "%s  DEF+%d  AVO+%d" % [tname, tdata.get("def", 0), tdata.get("avo", 0)]
		info_weapon.text = ""
		# Clear stats grid
		for child in info_stats_grid.get_children():
			child.queue_free()


func _update_info_panel_for_unit(data: UnitData) -> void:
	info_name.text = data.name
	info_class.text = "%s Lv.%d" % [data.unit_class, data.level]

	info_hp_bar.visible = true
	info_hp_bar.max_value = data.max_hp
	info_hp_bar.value = data.hp
	info_hp_label.text = "HP: %d / %d" % [data.hp, data.max_hp]

	# Terrain under unit
	var terrain := grid.get_terrain(data.grid_pos)
	var tname: String = Constants.TERRAIN_NAMES.get(terrain, "???")
	var tdata: Dictionary = Constants.TERRAIN_DATA.get(terrain, {})
	info_terrain.text = "%s  DEF+%d  AVO+%d" % [tname, tdata.get("def", 0), tdata.get("avo", 0)]

	# Equipped weapon
	if not data.equipped.is_empty():
		info_weapon.text = data.equipped.get("name", "Unarmed")
	else:
		info_weapon.text = "Unarmed"

	# Stats grid
	for child in info_stats_grid.get_children():
		child.queue_free()

	var stats := [
		["STR", data.str_], ["MAG", data.mag],
		["SKL", data.skl], ["SPD", data.spd],
		["DEF", data.def_], ["RES", data.res],
		["LCK", data.lck], ["MOV", data.mov],
	]
	for s in stats:
		var lbl := Label.new()
		lbl.text = "%s: %d" % [s[0], s[1]]
		lbl.add_theme_font_size_override("font_size", 11)
		info_stats_grid.add_child(lbl)


func _update_message_box() -> void:
	if GameData.message_queue.is_empty():
		message_box.visible = false
	else:
		message_box.visible = true
		message_label.text = GameData.message_queue[0]


# ── Damage popups ────────────────────────────────────────────────────────────

func _spawn_damage_popup(pos: Vector2i, text: String, color: Color) -> void:
	var ts := float(Constants.TILE_SIZE)
	var lbl := Label.new()
	lbl.text = text
	lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	lbl.position = Vector2(pos.x * ts, pos.y * ts - 10)
	lbl.size = Vector2(ts, 30)
	lbl.add_theme_font_size_override("font_size", 16)
	lbl.add_theme_color_override("font_color", color)
	lbl.z_index = 20
	damage_pop_layer.add_child(lbl)

	# Animate: float up and fade out
	var tween := create_tween()
	tween.tween_property(lbl, "position:y", lbl.position.y - 40, 1.0)
	tween.parallel().tween_property(lbl, "modulate:a", 0.0, 1.0).set_delay(0.3)
	tween.tween_callback(lbl.queue_free)


# ── Unit visual updates ─────────────────────────────────────────────────────

func _update_unit_hp_bar(unit_node: Node2D) -> void:
	if not unit_node or not unit_node.has_meta("unit_data"):
		return
	var data: UnitData = unit_node.get_meta("unit_data")
	var hp_fill: ColorRect = unit_node.get_node_or_null("HPBarFill")
	if hp_fill:
		var ts := float(Constants.TILE_SIZE)
		var inset := 3.0
		var hp_ratio := float(data.hp) / max(1, data.max_hp)
		hp_fill.size.x = (ts - inset * 2) * hp_ratio


func _update_unit_acted_visuals() -> void:
	for u in player_units:
		if not is_instance_valid(u):
			continue
		var data: UnitData = u.get_meta("unit_data")
		if data.alive and data.has_acted:
			u.modulate = Color(0.5, 0.5, 0.5, 1.0)
		elif data.alive:
			u.modulate = Color.WHITE


# ── Chapter intro screen ────────────────────────────────────────────────────

func _show_chapter_intro(ch: Dictionary) -> void:
	_intro_showing = true
	_intro_timer = 0.0
	chapter_intro_layer.visible = true

	# Use the existing BG node from the scene tree
	var bg: ColorRect = chapter_intro_layer.get_node("BG")
	# Clear old dynamic content from BG
	for child in bg.get_children():
		child.queue_free()

	var vp_size := get_viewport().get_visible_rect().size
	bg.color = Color(0.04, 0.02, 0.08, 0.95)

	# Gold decorative line top
	var line_top := ColorRect.new()
	line_top.size = Vector2(vp_size.x * 0.6, 2)
	line_top.position = Vector2(vp_size.x * 0.2, vp_size.y * 0.25)
	line_top.color = Color(0.85, 0.65, 0.13, 0.8)
	bg.add_child(line_top)

	# Chapter number
	var ch_num := Label.new()
	ch_num.text = "Chapter %d" % ch.get("number", GameData.chapter_index + 1)
	ch_num.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	ch_num.size = Vector2(vp_size.x, 40)
	ch_num.position = Vector2(0, vp_size.y * 0.28)
	ch_num.add_theme_font_size_override("font_size", 20)
	ch_num.add_theme_color_override("font_color", Color(0.85, 0.65, 0.13))
	bg.add_child(ch_num)

	# Chapter title
	var title := Label.new()
	title.text = ch.get("title", "Unknown")
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.size = Vector2(vp_size.x, 50)
	title.position = Vector2(0, vp_size.y * 0.35)
	title.add_theme_font_size_override("font_size", 32)
	title.add_theme_color_override("font_color", Color(0.94, 0.91, 0.82))
	bg.add_child(title)

	# Subtitle
	if ch.has("subtitle"):
		var sub := Label.new()
		sub.text = ch.get("subtitle", "")
		sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		sub.size = Vector2(vp_size.x, 30)
		sub.position = Vector2(0, vp_size.y * 0.42)
		sub.add_theme_font_size_override("font_size", 16)
		sub.add_theme_color_override("font_color", Color(0.7, 0.65, 0.55))
		bg.add_child(sub)

	# Gold decorative line bottom
	var line_bot := ColorRect.new()
	line_bot.size = Vector2(vp_size.x * 0.6, 2)
	line_bot.position = Vector2(vp_size.x * 0.2, vp_size.y * 0.48)
	line_bot.color = Color(0.85, 0.65, 0.13, 0.8)
	bg.add_child(line_bot)

	# Narrative intro text
	if ch.has("narrative_intro"):
		var narr := Label.new()
		narr.text = ch.get("narrative_intro", "")
		narr.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		narr.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		narr.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		narr.size = Vector2(vp_size.x * 0.7, vp_size.y * 0.3)
		narr.position = Vector2(vp_size.x * 0.15, vp_size.y * 0.55)
		narr.add_theme_font_size_override("font_size", 14)
		narr.add_theme_color_override("font_color", Color(0.8, 0.77, 0.68))
		bg.add_child(narr)

	# "Press any key" hint
	var hint := Label.new()
	hint.text = "Press any key to continue..."
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.size = Vector2(vp_size.x, 30)
	hint.position = Vector2(0, vp_size.y * 0.9)
	hint.add_theme_font_size_override("font_size", 12)
	hint.add_theme_color_override("font_color", Color(0.5, 0.48, 0.4))
	bg.add_child(hint)

	# Fade in with tween
	chapter_intro_layer.modulate = Color(1, 1, 1, 0)
	var tween := create_tween()
	tween.tween_property(chapter_intro_layer, "modulate:a", 1.0, 0.5)


func _end_chapter_intro() -> void:
	_intro_showing = false
	var tween := create_tween()
	tween.tween_property(chapter_intro_layer, "modulate:a", 0.0, 0.3)
	tween.tween_callback(func(): chapter_intro_layer.visible = false)


# ── Phase banner ─────────────────────────────────────────────────────────────

func _show_phase_banner(text: String, color: Color) -> void:
	_phase_banner_showing = true
	if _phase_banner:
		_phase_banner.queue_free()

	var vp_size := get_viewport().get_visible_rect().size

	_phase_banner = Label.new()
	_phase_banner.text = text
	_phase_banner.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_phase_banner.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_phase_banner.size = Vector2(vp_size.x, 60)
	_phase_banner.position = Vector2(-vp_size.x, vp_size.y * 0.4)
	_phase_banner.add_theme_font_size_override("font_size", 30)
	_phase_banner.add_theme_color_override("font_color", color)
	_phase_banner.z_index = 100

	# Dark backing strip
	var bg := ColorRect.new()
	bg.size = Vector2(vp_size.x, 60)
	bg.color = Color(0, 0, 0, 0.7)
	_phase_banner.add_child(bg)
	bg.z_index = -1

	# Gold borders on top/bottom of banner
	var line_t := ColorRect.new()
	line_t.size = Vector2(vp_size.x, 2)
	line_t.color = Color(0.85, 0.65, 0.13, 0.8)
	_phase_banner.add_child(line_t)
	var line_b := ColorRect.new()
	line_b.size = Vector2(vp_size.x, 2)
	line_b.position = Vector2(0, 58)
	line_b.color = Color(0.85, 0.65, 0.13, 0.8)
	_phase_banner.add_child(line_b)

	add_child(_phase_banner)

	# Slide in from left, pause, slide out right
	var tween := create_tween()
	tween.tween_property(_phase_banner, "position:x", 0.0, 0.3).set_ease(Tween.EASE_OUT)
	tween.tween_interval(0.8)
	tween.tween_property(_phase_banner, "position:x", vp_size.x, 0.3).set_ease(Tween.EASE_IN)
	tween.tween_callback(func():
		_phase_banner_showing = false
		if _phase_banner:
			_phase_banner.queue_free()
			_phase_banner = null
	)


# ── Danger zone overlay ─────────────────────────────────────────────────────

func _toggle_danger_zone() -> void:
	if _danger_zone_visible:
		_hide_danger_zone()
	else:
		_show_danger_zone()


func _show_danger_zone() -> void:
	if GameData.cursor_mode != Constants.CursorMode.FREE:
		return
	_danger_zone_visible = true
	_clear_overlay()
	var ts := float(Constants.TILE_SIZE)
	var danger_tiles := {}

	for u in enemy_units:
		var data: UnitData = u.get_meta("unit_data")
		if not data.alive:
			continue
		var e_move := grid.get_movement_range(
			data.grid_pos, data.mov, data.unit_class,
			data.is_flying, data.is_mounted, data.water_walk)
		var range_vec := data.attack_range()
		var e_attack := grid.get_attack_range(e_move, range_vec.x, range_vec.y)
		for tile in e_move + e_attack:
			danger_tiles[tile] = true

	for tile in danger_tiles:
		var rect := ColorRect.new()
		rect.size = Vector2(ts, ts)
		rect.position = Vector2(tile.x * ts, tile.y * ts)
		rect.color = Color(1.0, 0.1, 0.1, 0.2)
		overlay_layer.add_child(rect)


func _hide_danger_zone() -> void:
	_danger_zone_visible = false
	_clear_overlay()


# ── Weapon switching ─────────────────────────────────────────────────────────

func _handle_weapon_switch() -> void:
	if not selected_unit:
		return
	var data: UnitData = selected_unit.get_meta("unit_data")
	if data.weapons.size() <= 1:
		return

	# Cycle to next weapon
	data.equipped_weapon_index = (data.equipped_weapon_index + 1) % data.weapons.size()
	var wep_name: String = data.equipped.get("name", "Unarmed")
	GameData.push_message("%s equipped %s" % [data.name, wep_name])
	_update_info_panel_for_unit(data)
	_update_message_box()

	# Re-show the action menu (don't consume the action)
	_show_action_menu(data)


# ── Recruitment / Talk ───────────────────────────────────────────────────────

func _get_talk_targets(data: UnitData) -> Array:
	var targets: Array = []
	for dir in [Vector2i.UP, Vector2i.DOWN, Vector2i.LEFT, Vector2i.RIGHT]:
		var adj := data.grid_pos + dir
		var unit_node := _unit_at(adj)
		if unit_node:
			var ud: UnitData = unit_node.get_meta("unit_data")
			if ud.alive and ud.can_recruit and data.unit_id in ud.recruit_by:
				targets.append(unit_node)
	return targets


func _handle_talk_action() -> void:
	if not selected_unit:
		return
	var data: UnitData = selected_unit.get_meta("unit_data")
	var talk_targets := _get_talk_targets(data)
	if talk_targets.is_empty():
		return

	var target_node: Node2D = talk_targets[0]
	var target_data: UnitData = target_node.get_meta("unit_data")

	# Recruit the unit
	target_data.faction = Constants.Faction.PLAYER
	target_data.can_recruit = false
	target_data.reset_turn()

	# Move from enemy/ally list to player list
	enemy_units.erase(target_node)
	ally_units.erase(target_node)
	player_units.append(target_node)

	# Update visuals
	var badge: ColorRect = target_node.get_node_or_null("Badge")
	if badge:
		badge.color = _get_faction_badge_color(Constants.Faction.PLAYER)
	var border: ColorRect = target_node.get_node_or_null("Border")
	if border:
		border.color = _get_faction_border_color(Constants.Faction.PLAYER)
	var hp_fill: ColorRect = target_node.get_node_or_null("HPBarFill")
	if hp_fill:
		hp_fill.color = _get_hp_color(Constants.Faction.PLAYER)

	# Add to roster for persistence
	GameData.roster[target_data.unit_id] = target_data

	GameData.push_message("%s has joined your army!" % target_data.name)
	if not target_data.portrait_quote.is_empty():
		GameData.push_message('"%s"' % target_data.portrait_quote)

	data.done()
	_reset_interaction()
	_update_message_box()
	EventBus.unit_recruited.emit(selected_unit, target_node)


# ── Side objectives ──────────────────────────────────────────────────────────

func _check_side_objectives() -> void:
	var ch: Dictionary = Chapters.get_chapter(GameData.chapter_index)
	var side_objs: Array = ch.get("side_objectives", [])
	for obj in side_objs:
		if obj.get("completed", false):
			continue
		var obj_type: String = obj.get("type", "")
		match obj_type:
			"defeat":
				var target_id: String = obj.get("target", "")
				var found := false
				for u in enemy_units + ally_units:
					var ud: UnitData = u.get_meta("unit_data")
					if ud.unit_id == target_id and ud.alive:
						found = true
						break
				if not found:
					obj["completed"] = true
					var reward: int = obj.get("reward_gold", 0)
					GameData.gold += reward
					var desc: String = obj.get("description", "Side objective complete!")
					GameData.push_message("%s (+%d gold)" % [desc, reward])
			"visit":
				var target_pos = obj.get("target", [0, 0])
				var tpos := Vector2i(target_pos[0], target_pos[1]) if target_pos is Array else target_pos
				for u in player_units:
					var ud: UnitData = u.get_meta("unit_data")
					if ud.alive and ud.grid_pos == tpos:
						obj["completed"] = true
						var reward: int = obj.get("reward_gold", 0)
						GameData.gold += reward
						var desc: String = obj.get("description", "Side objective complete!")
						GameData.push_message("%s (+%d gold)" % [desc, reward])
						break
			"survive":
				var turns: int = obj.get("turns", 0)
				if turn_manager.turn_number >= turns:
					obj["completed"] = true
					var reward: int = obj.get("reward_gold", 0)
					GameData.gold += reward
					var desc: String = obj.get("description", "Side objective complete!")
					GameData.push_message("%s (+%d gold)" % [desc, reward])


# ── Stat sheet ───────────────────────────────────────────────────────────────

func _toggle_stat_sheet() -> void:
	if _stat_sheet_visible:
		_close_stat_sheet()
	else:
		_open_stat_sheet()


func _open_stat_sheet() -> void:
	# Show detailed info for unit under cursor, or selected unit
	var unit_node := _unit_at(GameData.cursor_pos)
	if not unit_node:
		return
	var data: UnitData = unit_node.get_meta("unit_data")

	_stat_sheet_visible = true
	if _stat_sheet_layer:
		_stat_sheet_layer.queue_free()

	_stat_sheet_layer = CanvasLayer.new()
	_stat_sheet_layer.layer = 15
	add_child(_stat_sheet_layer)

	var vp_size := get_viewport().get_visible_rect().size

	# Dark overlay
	var overlay := ColorRect.new()
	overlay.size = vp_size
	overlay.color = Color(0, 0, 0, 0.75)
	_stat_sheet_layer.add_child(overlay)

	# Main panel
	var panel := PanelContainer.new()
	panel.size = Vector2(min(500, vp_size.x - 40), min(500, vp_size.y - 80))
	panel.position = Vector2((vp_size.x - panel.size.x) / 2, (vp_size.y - panel.size.y) / 2)
	_stat_sheet_layer.add_child(panel)

	var margin := MarginContainer.new()
	margin.set_anchors_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 20)
	margin.add_theme_constant_override("margin_right", 20)
	margin.add_theme_constant_override("margin_top", 16)
	margin.add_theme_constant_override("margin_bottom", 16)
	panel.add_child(margin)

	var vbox := VBoxContainer.new()
	vbox.add_theme_constant_override("separation", 6)
	margin.add_child(vbox)

	# Name + class header
	var header := Label.new()
	header.text = "%s  —  %s Lv.%d" % [data.name, data.unit_class, data.level]
	header.add_theme_font_size_override("font_size", 22)
	header.add_theme_color_override("font_color", Color(0.85, 0.65, 0.13))
	header.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vbox.add_child(header)

	# Symbol
	var sym := Label.new()
	sym.text = Constants.CLASS_SYMBOLS.get(data.unit_class, "★")
	sym.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	sym.add_theme_font_size_override("font_size", 36)
	vbox.add_child(sym)

	# HP bar
	var hp_line := Label.new()
	hp_line.text = "HP: %d / %d" % [data.hp, data.max_hp]
	hp_line.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hp_line.add_theme_font_size_override("font_size", 16)
	vbox.add_child(hp_line)

	# Stats grid (2 columns)
	var sgrid := GridContainer.new()
	sgrid.columns = 4
	sgrid.add_theme_constant_override("h_separation", 20)
	sgrid.add_theme_constant_override("v_separation", 4)
	vbox.add_child(sgrid)

	var stats := [
		["STR", data.str_], ["MAG", data.mag],
		["SKL", data.skl], ["SPD", data.spd],
		["DEF", data.def_], ["RES", data.res],
		["LCK", data.lck], ["MOV", data.mov],
	]
	for s in stats:
		var lbl := Label.new()
		lbl.text = "%s" % s[0]
		lbl.add_theme_font_size_override("font_size", 14)
		lbl.add_theme_color_override("font_color", Color(0.7, 0.65, 0.55))
		sgrid.add_child(lbl)
		var val := Label.new()
		val.text = "%d" % s[1]
		val.add_theme_font_size_override("font_size", 14)
		sgrid.add_child(val)

	# Separator
	var sep := HSeparator.new()
	vbox.add_child(sep)

	# Weapons list
	var wep_header := Label.new()
	wep_header.text = "Weapons"
	wep_header.add_theme_font_size_override("font_size", 16)
	wep_header.add_theme_color_override("font_color", Color(0.85, 0.65, 0.13))
	vbox.add_child(wep_header)

	for i in range(data.weapons.size()):
		var w: Dictionary = data.weapons[i]
		var equipped_mark := " [E]" if i == data.equipped_weapon_index else ""
		var wlbl := Label.new()
		wlbl.text = "%s%s  Mt:%d  Hit:%d  Rng:%d-%d" % [
			w.get("name", "???"), equipped_mark,
			w.get("might", 0), w.get("hit", 0),
			w.get("min_range", 1), w.get("max_range", 1)]
		wlbl.add_theme_font_size_override("font_size", 13)
		vbox.add_child(wlbl)

	if data.weapons.is_empty():
		var no_wep := Label.new()
		no_wep.text = "Unarmed"
		no_wep.add_theme_font_size_override("font_size", 13)
		no_wep.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
		vbox.add_child(no_wep)

	# Bio
	if not data.bio.is_empty():
		var sep2 := HSeparator.new()
		vbox.add_child(sep2)
		var bio_lbl := Label.new()
		bio_lbl.text = data.bio
		bio_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		bio_lbl.add_theme_font_size_override("font_size", 12)
		bio_lbl.add_theme_color_override("font_color", Color(0.7, 0.67, 0.6))
		vbox.add_child(bio_lbl)

	# Close hint
	var hint := Label.new()
	hint.text = "Press any key to close"
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.add_theme_font_size_override("font_size", 11)
	hint.add_theme_color_override("font_color", Color(0.4, 0.38, 0.35))
	vbox.add_child(hint)

	EventBus.stat_sheet_opened.emit(unit_node)


func _close_stat_sheet() -> void:
	_stat_sheet_visible = false
	if _stat_sheet_layer:
		_stat_sheet_layer.queue_free()
		_stat_sheet_layer = null
	EventBus.stat_sheet_closed.emit()


# ── State change handler ─────────────────────────────────────────────────────

func _on_state_changed(new_state: String, _old_state: String) -> void:
	match new_state:
		"TITLE":
			title_screen_layer.visible = true
			battle_map.visible = false
			top_bar.visible = false
			info_panel.visible = false
		"PLAYER_TURN", "ENEMY_TURN", "ALLY_TURN":
			title_screen_layer.visible = false
			battle_map.visible = true
			top_bar.visible = true
			info_panel.visible = true
			_update_top_bar()
		"VICTORY":
			GameData.push_message("Chapter Complete! Press Z or tap to continue.")
			_update_message_box()
		"GAME_OVER":
			GameData.push_message("Game Over... Press Z or tap to retry.")
			_update_message_box()
