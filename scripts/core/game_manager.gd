## Main game manager — state machine, input routing, game loop.
## Attached to the root Game node.
extends Node2D

# ── Node references ──────────────────────────────────────────────────────────
@onready var camera: Camera2D = $Camera2D
@onready var battle_map: Node2D = $BattleMap
@onready var grid_node: Node2D = $BattleMap/Grid
@onready var terrain_layer: Node2D = $BattleMap/TerrainLayer
@onready var unit_layer: Node2D = $BattleMap/UnitLayer
@onready var overlay_layer: Node2D = $BattleMap/OverlayLayer
@onready var cursor_sprite: Sprite2D = $BattleMap/Cursor
@onready var ui_panel: Panel = $UI/UIPanel
@onready var message_box: PanelContainer = $UI/MessageBox
@onready var message_label: Label = $UI/MessageBox/MessageLabel
@onready var title_screen: CanvasLayer = $TitleScreen
@onready var combat_anim_layer: CanvasLayer = $CombatAnimLayer

# ── Game systems ─────────────────────────────────────────────────────────────
var grid: Grid
var turn_manager: TurnManager
var ai: EnemyAI

# ── Unit lists ───────────────────────────────────────────────────────────────
var player_units: Array = []
var enemy_units: Array = []
var ally_units: Array = []

# ── Interaction state ────────────────────────────────────────────────────────
var selected_unit: Node2D = null
var move_range: Array[Vector2i] = []
var move_range_land: Array[Vector2i] = []
var attack_range: Array[Vector2i] = []
var showing_preview: bool = false
var preview_target = null

# ── Terrain tile sprites (procedural) ────────────────────────────────────────
var _terrain_tiles: Dictionary = {}  # Vector2i → ColorRect


func _ready() -> void:
	grid = Grid.new()
	add_child(grid)
	turn_manager = TurnManager.new()

	# Start at title screen
	_enter_title()

	# Connect signals
	EventBus.state_changed.connect(_on_state_changed)


func _enter_title() -> void:
	GameData.change_state(Constants.GameState.TITLE)
	title_screen.visible = true
	battle_map.visible = false


func _start_new_game() -> void:
	title_screen.visible = false
	battle_map.visible = true

	# Initialize roster
	var roster_data = Roster.create_roster()
	GameData.roster = roster_data
	GameData.reset_for_new_game()

	_load_chapter(0)


func _load_chapter(index: int) -> void:
	var ch: Dictionary = Chapters.get_chapter(index)
	GameData.chapter_index = index

	# Setup grid
	grid.setup(ch.get("map_width", 12), ch.get("map_height", 10), ch.get("tiles", []))
	grid.seize_points.clear()
	for sp in ch.get("seize_points", []):
		grid.seize_points.append(Vector2i(sp[0], sp[1]))

	# Clear old units
	for child in unit_layer.get_children():
		child.queue_free()
	player_units.clear()
	enemy_units.clear()
	ally_units.clear()

	# Spawn units
	for def in ch.get("player_units", []):
		_spawn_unit(def, Constants.Faction.PLAYER)
	for def in ch.get("enemy_units", []):
		_spawn_unit(def, Constants.Faction.ENEMY)
	for def in ch.get("ally_units", []):
		_spawn_unit(def, Constants.Faction.ALLY)

	# Build terrain visuals
	_build_terrain_visuals()

	# Setup AI
	ai = EnemyAI.new(grid, player_units, enemy_units, ally_units)

	# Start player turn
	turn_manager.reset()
	GameData.change_state(Constants.GameState.PLAYER_TURN)
	_reset_all_units(Constants.Faction.PLAYER)

	# Center camera
	GameData.cursor_pos = Vector2i(0, 0)
	_update_cursor()
	EventBus.chapter_started.emit(index)


func _spawn_unit(def: Dictionary, faction: int) -> void:
	var unit_id: String = def.get("id", "")
	var unit_data: UnitData
	if GameData.roster.has(unit_id):
		unit_data = GameData.roster[unit_id].duplicate()
	else:
		unit_data = UnitData.new()
		unit_data.unit_id = unit_id
		unit_data.name = unit_id.capitalize()

	unit_data.faction = faction
	unit_data.grid_pos = Vector2i(def.get("x", 0), def.get("y", 0))
	unit_data.alive = true
	unit_data.reset_turn()

	# Create visual node
	var unit_node := _create_unit_sprite(unit_data)
	unit_layer.add_child(unit_node)

	match faction:
		Constants.Faction.PLAYER: player_units.append(unit_node)
		Constants.Faction.ENEMY: enemy_units.append(unit_node)
		Constants.Faction.ALLY: ally_units.append(unit_node)


func _create_unit_sprite(data: UnitData) -> Node2D:
	var node := Node2D.new()
	node.name = data.unit_id
	node.position = grid.grid_to_pixel(data.grid_pos)
	node.set_meta("unit_data", data)

	# Background circle
	var bg := ColorRect.new()
	bg.size = Vector2(Constants.TILE_SIZE - 4, Constants.TILE_SIZE - 4)
	bg.position = Vector2(-Constants.TILE_SIZE / 2.0 + 2, -Constants.TILE_SIZE / 2.0 + 2)
	match data.faction:
		Constants.Faction.PLAYER: bg.color = Constants.COLOR_PLAYER
		Constants.Faction.ENEMY: bg.color = Constants.COLOR_ENEMY
		Constants.Faction.ALLY: bg.color = Constants.COLOR_ALLY
	node.add_child(bg)

	# Symbol label
	var label := Label.new()
	label.text = data.symbol
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	label.size = Vector2(Constants.TILE_SIZE, Constants.TILE_SIZE)
	label.position = Vector2(-Constants.TILE_SIZE / 2.0, -Constants.TILE_SIZE / 2.0)
	node.add_child(label)

	return node


func _build_terrain_visuals() -> void:
	# Clear old terrain
	for child in terrain_layer.get_children():
		child.queue_free()
	_terrain_tiles.clear()

	for y in range(grid.height):
		for x in range(grid.width):
			var terrain := grid.get_terrain(Vector2i(x, y))
			var color: Color = Constants.TERRAIN_COLORS.get(terrain, Color.GRAY)
			var rect := ColorRect.new()
			rect.size = Vector2(Constants.TILE_SIZE, Constants.TILE_SIZE)
			rect.position = Vector2(x * Constants.TILE_SIZE, y * Constants.TILE_SIZE)
			rect.color = color
			terrain_layer.add_child(rect)
			_terrain_tiles[Vector2i(x, y)] = rect

	# Seize point markers
	for sp in grid.seize_points:
		var marker := ColorRect.new()
		marker.size = Vector2(Constants.TILE_SIZE, Constants.TILE_SIZE)
		marker.position = Vector2(sp.x * Constants.TILE_SIZE, sp.y * Constants.TILE_SIZE)
		marker.color = Color(Constants.COLOR_GOLD, 0.4)
		terrain_layer.add_child(marker)


func _update_cursor() -> void:
	cursor_sprite.visible = true
	cursor_sprite.position = grid.grid_to_pixel(GameData.cursor_pos)
	# Draw cursor as outline (using modulate for now)
	if not cursor_sprite.texture:
		var img := Image.create(Constants.TILE_SIZE, Constants.TILE_SIZE, false, Image.FORMAT_RGBA8)
		img.fill(Color(1, 1, 1, 0))
		# Draw border
		for i in range(Constants.TILE_SIZE):
			img.set_pixel(i, 0, Color.WHITE)
			img.set_pixel(i, Constants.TILE_SIZE - 1, Color.WHITE)
			img.set_pixel(0, i, Color.WHITE)
			img.set_pixel(Constants.TILE_SIZE - 1, i, Color.WHITE)
			if i > 0 and i < Constants.TILE_SIZE - 1:
				img.set_pixel(1, i, Color.WHITE)
				img.set_pixel(Constants.TILE_SIZE - 2, i, Color(1, 1, 1, 0.3))
		cursor_sprite.texture = ImageTexture.create_from_image(img)
	cursor_sprite.position = Vector2(
		GameData.cursor_pos.x * Constants.TILE_SIZE,
		GameData.cursor_pos.y * Constants.TILE_SIZE) + Vector2(Constants.TILE_SIZE / 2.0, Constants.TILE_SIZE / 2.0)


# ── Input handling ───────────────────────────────────────────────────────────

func _unhandled_input(event: InputEvent) -> void:
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

	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		match GameData.current_state:
			Constants.GameState.TITLE:
				_start_new_game()
			Constants.GameState.PLAYER_TURN:
				_handle_map_click(event.position)


func _handle_title_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		_start_new_game()


func _handle_player_input(event: InputEvent) -> void:
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

	# Confirm / Select
	elif event.is_action_pressed("confirm"):
		_handle_confirm()

	# Cancel
	elif event.is_action_pressed("cancel"):
		_reset_interaction()

	# Attack
	elif event.is_action_pressed("attack"):
		_handle_attack_action()

	# Wait
	elif event.is_action_pressed("wait_action"):
		_handle_wait_action()

	# Heal
	elif event.is_action_pressed("heal"):
		_handle_heal_action()

	# End turn
	elif event.is_action_pressed("end_turn"):
		_end_player_turn()

	# Seize
	elif event.is_action_pressed("seize"):
		_handle_seize_action()


func _move_cursor(delta: Vector2i) -> void:
	var new_pos := GameData.cursor_pos + delta
	new_pos.x = clampi(new_pos.x, 0, grid.width - 1)
	new_pos.y = clampi(new_pos.y, 0, grid.height - 1)
	GameData.cursor_pos = new_pos
	_update_cursor()
	_center_camera_on_cursor()
	EventBus.cursor_moved.emit(new_pos)


func _handle_confirm() -> void:
	var pos := GameData.cursor_pos

	if GameData.cursor_mode == Constants.CursorMode.FREE:
		# Try to select a unit
		var unit_node := _unit_at(pos)
		if unit_node:
			var data: UnitData = unit_node.get_meta("unit_data")
			if data.faction == Constants.Faction.PLAYER and data.alive and not data.has_acted:
				_select_unit(unit_node)
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

	# Compute ranges
	if data.has_moved:
		move_range = []
		move_range_land = [data.grid_pos]
	else:
		move_range = grid.get_movement_range(
			data.grid_pos, data.mov, data.unit_class,
			data.is_flying, data.is_mounted, data.water_walk)
		# Remove tiles occupied by other units
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
	EventBus.unit_selected.emit(unit_node)


func _move_selected_unit(pos: Vector2i) -> void:
	if not selected_unit:
		return
	var data: UnitData = selected_unit.get_meta("unit_data")
	data.grid_pos = pos
	data.has_moved = true
	selected_unit.position = grid.grid_to_pixel(pos)
	_clear_overlay()
	EventBus.unit_moved.emit(selected_unit, data.grid_pos, pos)


func _handle_attack_action() -> void:
	if not selected_unit:
		return
	var data: UnitData = selected_unit.get_meta("unit_data")
	if data.has_acted:
		return

	var targets := _get_attackable_targets(data)
	if targets.is_empty():
		return

	# Open combat with first target
	var target_node: Node2D = targets[0]
	var target_data: UnitData = target_node.get_meta("unit_data")
	_execute_combat(data, target_data, selected_unit, target_node)


func _execute_combat(atk_data: UnitData, def_data: UnitData, atk_node: Node2D, def_node: Node2D) -> void:
	var terrain_att := grid.get_terrain(atk_data.grid_pos)
	var terrain_def := grid.get_terrain(def_data.grid_pos)
	var result := Combat.resolve(atk_data, def_data, terrain_att, terrain_def)

	# Update visuals
	if not def_data.alive:
		def_node.visible = false
		GameData.push_message("%s was defeated!" % def_data.name)
		EventBus.unit_defeated.emit(def_node)
	if not atk_data.alive:
		atk_node.visible = false
		GameData.push_message("%s was defeated!" % atk_data.name)
		EventBus.unit_defeated.emit(atk_node)

	atk_data.done()
	_reset_interaction()
	_update_message_box()
	_check_victory()
	_check_defeat()

	EventBus.combat_finished.emit({
		"attacker": atk_data.name, "defender": def_data.name,
		"rounds": result.rounds.size(),
		"attacker_died": result.attacker_died,
		"defender_died": result.defender_died,
	})


func _handle_wait_action() -> void:
	if not selected_unit:
		return
	var data: UnitData = selected_unit.get_meta("unit_data")
	data.done()
	_reset_interaction()
	EventBus.unit_waited.emit(selected_unit)


func _handle_heal_action() -> void:
	if not selected_unit:
		return
	var data: UnitData = selected_unit.get_meta("unit_data")
	if data.has_acted or data.equipped.is_empty():
		return
	if data.equipped.get("weapon_type", -1) != Constants.WeaponType.STAFF:
		return

	# Find adjacent allies that need healing
	for dir in [Vector2i.UP, Vector2i.DOWN, Vector2i.LEFT, Vector2i.RIGHT]:
		var adj := data.grid_pos + dir
		var unit_node := _unit_at(adj)
		if unit_node:
			var ud: UnitData = unit_node.get_meta("unit_data")
			if ud.faction == data.faction and ud.alive and ud.hp < ud.max_hp:
				var amount := Combat.resolve_heal(data, ud)
				GameData.push_message("%s healed %s for %d HP!" % [data.name, ud.name, amount])
				data.done()
				_reset_interaction()
				_update_message_box()
				EventBus.unit_healed.emit(selected_unit, unit_node, amount)
				return


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


func _end_player_turn() -> void:
	# Mark remaining units as done
	for u in player_units:
		var data: UnitData = u.get_meta("unit_data")
		if data.alive:
			data.done()
	_reset_interaction()

	# Enemy turn
	GameData.change_state(Constants.GameState.ENEMY_TURN)
	turn_manager.end_player_turn()
	_run_enemy_turn()


func _run_enemy_turn() -> void:
	# Reset enemy units
	for u in enemy_units:
		var data: UnitData = u.get_meta("unit_data")
		if data.alive:
			data.reset_turn()

	# AI actions
	ai.player_units = player_units.filter(func(u): return u.get_meta("unit_data").alive)
	ai.enemy_units = enemy_units.filter(func(u): return u.get_meta("unit_data").alive)
	var actions := ai.run_turn()

	# Apply AI movement visually
	for action in actions:
		var unit_node: Node2D = action.get("unit_node", null)
		if not unit_node:
			# Find the node for this unit
			var unit_data = action.get("unit", null)
			if unit_data:
				for u in enemy_units:
					if u.get_meta("unit_data") == unit_data:
						unit_node = u
						break
		if unit_node:
			var data: UnitData = unit_node.get_meta("unit_data")
			unit_node.position = grid.grid_to_pixel(data.grid_pos)

		if action.get("type", "") == "attack":
			var target = action.get("target", null)
			if target:
				var atk_data: UnitData = action.get("unit")
				var terrain_att := grid.get_terrain(atk_data.grid_pos)
				var terrain_def := grid.get_terrain(target.grid_pos)
				var result := Combat.resolve(atk_data, target, terrain_att, terrain_def)
				# Update target visibility
				if not target.alive:
					for u in player_units + ally_units:
						if u.get_meta("unit_data") == target:
							u.visible = false

	_check_defeat()

	# Reset player units for new turn
	for u in player_units:
		var data: UnitData = u.get_meta("unit_data")
		if data.alive:
			data.reset_turn()

	turn_manager.turn_number += 1
	GameData.change_state(Constants.GameState.PLAYER_TURN)
	turn_manager.start_player_turn()


# ── Helpers ──────────────────────────────────────────────────────────────────

func _reset_interaction() -> void:
	selected_unit = null
	GameData.cursor_mode = Constants.CursorMode.FREE
	GameData.selected_unit = null
	move_range.clear()
	move_range_land.clear()
	attack_range.clear()
	showing_preview = false
	preview_target = null
	_clear_overlay()
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


func _check_victory() -> void:
	var enemies_alive := enemy_units.filter(func(u): return u.get_meta("unit_data").alive)
	if enemies_alive.is_empty():
		GameData.push_message("All enemies defeated! Victory!")
		GameData.change_state(Constants.GameState.VICTORY)
		EventBus.chapter_victory.emit()
		_update_message_box()


func _check_defeat() -> void:
	# Check if lord is dead
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
		if GameData.chapter_index + 1 < Chapters.chapter_count():
			_load_chapter(GameData.chapter_index + 1)
		else:
			_enter_title()


func _handle_gameover_input(event: InputEvent) -> void:
	if event.is_action_pressed("confirm"):
		_load_chapter(GameData.chapter_index)  # Restart chapter


func _handle_map_click(screen_pos: Vector2) -> void:
	var world_pos := get_global_mouse_position()
	var grid_pos := grid.pixel_to_grid(world_pos)
	if grid.is_valid(grid_pos):
		GameData.cursor_pos = grid_pos
		_update_cursor()
		_handle_confirm()


func _center_camera_on_cursor() -> void:
	var target := grid.grid_to_pixel(GameData.cursor_pos)
	camera.position = target


# ── Overlay drawing ──────────────────────────────────────────────────────────

func _draw_range_overlay() -> void:
	_clear_overlay()
	for pos in move_range_land:
		var rect := ColorRect.new()
		rect.size = Vector2(Constants.TILE_SIZE, Constants.TILE_SIZE)
		rect.position = Vector2(pos.x * Constants.TILE_SIZE, pos.y * Constants.TILE_SIZE)
		rect.color = Constants.COLOR_MOVE_RANGE
		overlay_layer.add_child(rect)

	for pos in attack_range:
		var rect := ColorRect.new()
		rect.size = Vector2(Constants.TILE_SIZE, Constants.TILE_SIZE)
		rect.position = Vector2(pos.x * Constants.TILE_SIZE, pos.y * Constants.TILE_SIZE)
		rect.color = Constants.COLOR_ATTACK_RANGE
		overlay_layer.add_child(rect)


func _clear_overlay() -> void:
	for child in overlay_layer.get_children():
		child.queue_free()


func _update_message_box() -> void:
	if GameData.message_queue.is_empty():
		message_box.visible = false
	else:
		message_box.visible = true
		message_label.text = GameData.message_queue[0]


func _on_state_changed(new_state: String, _old_state: String) -> void:
	# Handle state transition visuals
	match new_state:
		"TITLE":
			title_screen.visible = true
			battle_map.visible = false
		"PLAYER_TURN", "ENEMY_TURN", "ALLY_TURN":
			title_screen.visible = false
			battle_map.visible = true
		"VICTORY":
			GameData.push_message("Chapter Complete!")
			_update_message_box()
		"GAME_OVER":
			GameData.push_message("Game Over... Press Z to retry.")
			_update_message_box()
