## Deployment / Prep screen — lets player choose which units to deploy before battle.
## Created dynamically by game_manager and added to a CanvasLayer.
extends Control

signal deploy_confirmed(selected_units: Array)
signal deploy_canceled

var _chapter_data: Dictionary = {}
var _available_units: Array = []  # Array of UnitData
var _selected_ids: Array[String] = []
var _forced_ids: Array[String] = []
var _deploy_limit: int = 8
var _scroll_offset: int = 0
var _cursor_index: int = 0

var _unit_buttons: Array = []
var _vbox: VBoxContainer
var _info_label: Label
var _confirm_btn: Button


func setup(chapter_data: Dictionary) -> void:
	_chapter_data = chapter_data
	_deploy_limit = chapter_data.get("deploy_limit", 8)
	_forced_ids = []
	for uid in chapter_data.get("forced_units", []):
		_forced_ids.append(str(uid))

	# Gather available player units from roster
	_available_units.clear()
	_selected_ids.clear()

	# Forced units are always selected
	for uid in _forced_ids:
		_selected_ids.append(uid)

	# Add all alive player units from roster
	for uid in GameData.roster:
		var u: UnitData = GameData.roster[uid]
		if u.faction == Constants.Faction.PLAYER and u.alive:
			if uid not in GameData.casualty_list:
				_available_units.append(u)

	_build_ui()


func _build_ui() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)

	# Dark background
	var bg := ColorRect.new()
	bg.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg.color = Color(0.04, 0.02, 0.08, 0.95)
	add_child(bg)

	var margin := MarginContainer.new()
	margin.set_anchors_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 40)
	margin.add_theme_constant_override("margin_right", 40)
	margin.add_theme_constant_override("margin_top", 30)
	margin.add_theme_constant_override("margin_bottom", 30)
	add_child(margin)

	var outer_vbox := VBoxContainer.new()
	outer_vbox.add_theme_constant_override("separation", 10)
	margin.add_child(outer_vbox)

	# Title
	var title := Label.new()
	title.text = "Deploy Units"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 26)
	title.add_theme_color_override("font_color", Color(0.85, 0.65, 0.13))
	outer_vbox.add_child(title)

	# Info line
	_info_label = Label.new()
	_update_info_label()
	_info_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_info_label.add_theme_font_size_override("font_size", 14)
	outer_vbox.add_child(_info_label)

	# Gold line
	var line := ColorRect.new()
	line.custom_minimum_size = Vector2(0, 2)
	line.color = Color(0.85, 0.65, 0.13, 0.5)
	outer_vbox.add_child(line)

	# Scrollable unit list
	var scroll := ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	outer_vbox.add_child(scroll)

	_vbox = VBoxContainer.new()
	_vbox.add_theme_constant_override("separation", 4)
	_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(_vbox)

	_rebuild_unit_list()

	# Bottom buttons
	var btn_hbox := HBoxContainer.new()
	btn_hbox.alignment = BoxContainer.ALIGNMENT_CENTER
	btn_hbox.add_theme_constant_override("separation", 20)
	outer_vbox.add_child(btn_hbox)

	_confirm_btn = Button.new()
	_confirm_btn.text = "Deploy"
	_confirm_btn.pressed.connect(_on_confirm)
	_confirm_btn.custom_minimum_size = Vector2(120, 36)
	btn_hbox.add_child(_confirm_btn)

	var cancel_btn := Button.new()
	cancel_btn.text = "Auto-Fill"
	cancel_btn.pressed.connect(_on_auto_fill)
	cancel_btn.custom_minimum_size = Vector2(120, 36)
	btn_hbox.add_child(cancel_btn)


func _rebuild_unit_list() -> void:
	_unit_buttons.clear()
	for child in _vbox.get_children():
		child.queue_free()

	for u in _available_units:
		var is_forced := u.unit_id in _forced_ids
		var is_selected := u.unit_id in _selected_ids

		var btn := Button.new()
		var mark := "[F] " if is_forced else ("[X] " if is_selected else "[ ] ")
		btn.text = "%s%s  %s Lv.%d  HP:%d/%d" % [
			mark, u.name, u.unit_class, u.level, u.hp, u.max_hp]
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		if is_forced:
			btn.disabled = true
		else:
			btn.pressed.connect(_on_unit_toggled.bind(u.unit_id))
		_vbox.add_child(btn)
		_unit_buttons.append(btn)


func _on_unit_toggled(unit_id: String) -> void:
	if unit_id in _forced_ids:
		return
	if unit_id in _selected_ids:
		_selected_ids.erase(unit_id)
	else:
		if _selected_ids.size() >= _deploy_limit:
			return  # At limit
		_selected_ids.append(unit_id)

	_update_info_label()
	_rebuild_unit_list()


func _on_confirm() -> void:
	deploy_confirmed.emit(_selected_ids.duplicate())


func _on_auto_fill() -> void:
	# Auto-select up to deploy limit, prioritizing highest level
	_selected_ids.clear()
	for uid in _forced_ids:
		_selected_ids.append(uid)

	var sorted_units := _available_units.duplicate()
	sorted_units.sort_custom(func(a, b): return a.level > b.level)

	for u in sorted_units:
		if _selected_ids.size() >= _deploy_limit:
			break
		if u.unit_id not in _selected_ids:
			_selected_ids.append(u.unit_id)

	_update_info_label()
	_rebuild_unit_list()


func _update_info_label() -> void:
	if _info_label:
		_info_label.text = "Selected: %d / %d  (Forced: %d)" % [
			_selected_ids.size(), _deploy_limit, _forced_ids.size()]


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed:
		if event.is_action_pressed("cancel"):
			# Can't cancel deploy, auto-fill instead
			_on_auto_fill()
			_on_confirm()
