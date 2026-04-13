## Between-chapter shop — hire mercenaries and manage gold.
## Created dynamically by game_manager after chapter victory.
extends Control

signal shop_closed

var _gold_label: Label
var _item_vbox: VBoxContainer
var _message_label: Label


func setup() -> void:
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
	margin.add_theme_constant_override("margin_left", 60)
	margin.add_theme_constant_override("margin_right", 60)
	margin.add_theme_constant_override("margin_top", 40)
	margin.add_theme_constant_override("margin_bottom", 40)
	add_child(margin)

	var outer_vbox := VBoxContainer.new()
	outer_vbox.add_theme_constant_override("separation", 12)
	margin.add_child(outer_vbox)

	# Title
	var title := Label.new()
	title.text = "Mercenary Camp"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.add_theme_font_size_override("font_size", 26)
	title.add_theme_color_override("font_color", Color(0.85, 0.65, 0.13))
	outer_vbox.add_child(title)

	# Gold display
	_gold_label = Label.new()
	_update_gold_display()
	_gold_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_gold_label.add_theme_font_size_override("font_size", 18)
	_gold_label.add_theme_color_override("font_color", Color(0.85, 0.65, 0.13))
	outer_vbox.add_child(_gold_label)

	# Gold line
	var line := ColorRect.new()
	line.custom_minimum_size = Vector2(0, 2)
	line.color = Color(0.85, 0.65, 0.13, 0.5)
	outer_vbox.add_child(line)

	# Mercenary list
	var scroll := ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	outer_vbox.add_child(scroll)

	_item_vbox = VBoxContainer.new()
	_item_vbox.add_theme_constant_override("separation", 6)
	_item_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(_item_vbox)

	_rebuild_shop_list()

	# Message label
	_message_label = Label.new()
	_message_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_message_label.add_theme_font_size_override("font_size", 14)
	_message_label.add_theme_color_override("font_color", Color(0.7, 0.65, 0.55))
	outer_vbox.add_child(_message_label)

	# Close button
	var close_btn := Button.new()
	close_btn.text = "Continue to Next Chapter"
	close_btn.pressed.connect(func(): shop_closed.emit())
	close_btn.custom_minimum_size = Vector2(240, 40)
	close_btn.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	outer_vbox.add_child(close_btn)


func _rebuild_shop_list() -> void:
	for child in _item_vbox.get_children():
		child.queue_free()

	for merc_id in Constants.SHOP_PRICES:
		var price: int = Constants.SHOP_PRICES[merc_id]
		var display_name := merc_id.replace("merc_", "").capitalize()

		var hbox := HBoxContainer.new()
		hbox.add_theme_constant_override("separation", 16)
		_item_vbox.add_child(hbox)

		var name_lbl := Label.new()
		name_lbl.text = display_name
		name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		name_lbl.add_theme_font_size_override("font_size", 16)
		hbox.add_child(name_lbl)

		var price_lbl := Label.new()
		price_lbl.text = "%d gold" % price
		price_lbl.add_theme_font_size_override("font_size", 14)
		price_lbl.add_theme_color_override("font_color",
			Color(0.85, 0.65, 0.13) if GameData.gold >= price else Color(0.5, 0.4, 0.4))
		hbox.add_child(price_lbl)

		var buy_btn := Button.new()
		buy_btn.text = "Hire"
		buy_btn.disabled = GameData.gold < price
		buy_btn.pressed.connect(_on_buy.bind(merc_id, price))
		buy_btn.custom_minimum_size = Vector2(80, 30)
		hbox.add_child(buy_btn)


func _on_buy(merc_id: String, price: int) -> void:
	if GameData.gold < price:
		_message_label.text = "Not enough gold!"
		return

	GameData.gold -= price
	var merc: UnitData = Roster.create_mercenary(merc_id, GameData.chapter_index)
	if merc:
		# Generate unique ID
		var uid := "%s_%d" % [merc_id, randi() % 10000]
		merc.unit_id = uid
		merc.faction = Constants.Faction.PLAYER
		merc.alive = true
		GameData.roster[uid] = merc
		_message_label.text = "Hired %s!" % merc.name
	else:
		_message_label.text = "Hired a mercenary!"

	_update_gold_display()
	_rebuild_shop_list()


func _update_gold_display() -> void:
	if _gold_label:
		_gold_label.text = "Gold: %d" % GameData.gold


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed:
		if event.is_action_pressed("cancel"):
			shop_closed.emit()
