## Procedural animated title screen for Sengoku Tactics: Age of the Warring States.
## Builds the entire UI in code — no external assets required.
## Attach to a CanvasLayer node in your scene tree.
extends CanvasLayer

signal start_pressed

# ── Palette ──────────────────────────────────────────────────────────────────
const COLOR_GOLD := Color(0.83, 0.65, 0.21)
const COLOR_GOLD_DIM := Color(0.83, 0.65, 0.21, 0.35)
const COLOR_GOLD_GLOW := Color(1.0, 0.85, 0.3, 0.45)
const COLOR_CREAM := Color(0.94, 0.91, 0.82)
const COLOR_DARK_BG := Color(0.04, 0.02, 0.08)
const COLOR_DARK_BG_TOP := Color(0.07, 0.03, 0.14)
const COLOR_DIM_TEXT := Color(0.5, 0.45, 0.4, 0.5)
const COLOR_TRANSPARENT := Color(1, 1, 1, 0)

# ── Node references (created in _ready) ─────────────────────────────────────
var _root: Control
var _title_label: Label
var _title_glow: Label
var _subtitle_label: Label
var _prompt_label: Label
var _version_label: Label
var _line_top: ColorRect
var _line_bottom: ColorRect
var _mon_container: Control
var _fade_overlay: ColorRect

# ── Tween handles ────────────────────────────────────────────────────────────
var _prompt_tween: Tween
var _glow_tween: Tween

# ── State ────────────────────────────────────────────────────────────────────
var _is_active := false


func _ready() -> void:
	layer = 100
	_build_ui()
	_start_animations()
	_is_active = true


# ─────────────────────────────────────────────────────────────────────────────
#  UI CONSTRUCTION
# ─────────────────────────────────────────────────────────────────────────────

func _build_ui() -> void:
	# Root Control — full-screen anchor
	_root = Control.new()
	_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root.mouse_filter = Control.MOUSE_FILTER_STOP
	add_child(_root)

	_build_background()
	_build_mon_crest()
	_build_decorative_lines()
	_build_title()
	_build_subtitle()
	_build_prompt()
	_build_version()
	_build_fade_overlay()


# ── Background gradient (two overlapping rects) ─────────────────────────────

func _build_background() -> void:
	# Bottom layer: solid near-black
	var bg_bottom := ColorRect.new()
	bg_bottom.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg_bottom.color = COLOR_DARK_BG
	_root.add_child(bg_bottom)

	# Top layer: dark indigo, fading from top to transparent at bottom
	var bg_top := ColorRect.new()
	bg_top.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg_top.color = COLOR_DARK_BG_TOP
	_root.add_child(bg_top)

	# Subtle vertical gradient via a panel stylebox with modulate
	# We approximate a gradient by stacking a half-screen rect with transparency
	var bg_gradient := ColorRect.new()
	bg_gradient.set_anchors_preset(Control.PRESET_FULL_RECT)
	bg_gradient.anchor_bottom = 0.5
	bg_gradient.color = Color(0.1, 0.04, 0.2, 0.25)
	_root.add_child(bg_gradient)

	# Atmospheric particles / vignette corners — four dim rects in corners
	for corner_data in [
		{"left": 0.0, "top": 0.0, "right": 0.3, "bottom": 0.3},
		{"left": 0.7, "top": 0.0, "right": 1.0, "bottom": 0.3},
		{"left": 0.0, "top": 0.7, "right": 0.3, "bottom": 1.0},
		{"left": 0.7, "top": 0.7, "right": 1.0, "bottom": 1.0},
	]:
		var vignette := ColorRect.new()
		vignette.anchor_left = corner_data["left"]
		vignette.anchor_top = corner_data["top"]
		vignette.anchor_right = corner_data["right"]
		vignette.anchor_bottom = corner_data["bottom"]
		vignette.offset_left = 0
		vignette.offset_top = 0
		vignette.offset_right = 0
		vignette.offset_bottom = 0
		vignette.color = Color(0, 0, 0, 0.25)
		_root.add_child(vignette)


# ── Mon (family crest) — drawn with simple shapes ───────────────────────────

func _build_mon_crest() -> void:
	_mon_container = Control.new()
	_mon_container.set_anchors_preset(Control.PRESET_CENTER_TOP)
	_mon_container.anchor_top = 0.12
	_mon_container.offset_left = -60
	_mon_container.offset_top = 0
	_mon_container.custom_minimum_size = Vector2(120, 120)
	_mon_container.size = Vector2(120, 120)
	_root.add_child(_mon_container)

	# The mon is drawn in a dedicated Node2D child so we can use _draw().
	var mon_drawing := MonDrawing.new()
	mon_drawing.position = Vector2(60, 60)
	_mon_container.add_child(mon_drawing)


# ── Decorative horizontal lines ─────────────────────────────────────────────

func _build_decorative_lines() -> void:
	# Top line — above title
	_line_top = _create_h_line(0.40)
	_root.add_child(_line_top)

	# Bottom line — below subtitle
	_line_bottom = _create_h_line(0.58)
	_root.add_child(_line_bottom)


func _create_h_line(vertical_anchor: float) -> ColorRect:
	var line := ColorRect.new()
	line.anchor_left = 0.2
	line.anchor_right = 0.8
	line.anchor_top = vertical_anchor
	line.anchor_bottom = vertical_anchor
	line.offset_top = 0
	line.offset_bottom = 2
	line.offset_left = 0
	line.offset_right = 0
	line.color = COLOR_GOLD_DIM

	# Diamond accents at each end — small squares rotated 45 degrees
	for side in [-1, 1]:
		var diamond := ColorRect.new()
		diamond.custom_minimum_size = Vector2(8, 8)
		diamond.size = Vector2(8, 8)
		diamond.color = COLOR_GOLD
		diamond.pivot_offset = Vector2(4, 4)
		diamond.rotation = PI / 4.0
		if side == -1:
			diamond.position = Vector2(-6, -3)
		else:
			diamond.anchor_left = 1.0
			diamond.anchor_right = 1.0
			diamond.offset_left = -2
			diamond.offset_top = -3
		line.add_child(diamond)

	return line


# ── Title ────────────────────────────────────────────────────────────────────

func _build_title() -> void:
	# Glow layer (slightly larger, blurred via modulate alpha pulsing)
	_title_glow = Label.new()
	_title_glow.text = "SENGOKU TACTICS"
	_title_glow.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_title_glow.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_title_glow.set_anchors_preset(Control.PRESET_CENTER)
	_title_glow.anchor_top = 0.42
	_title_glow.anchor_bottom = 0.52
	_title_glow.anchor_left = 0.0
	_title_glow.anchor_right = 1.0
	_title_glow.offset_top = 0
	_title_glow.offset_bottom = 0
	_title_glow.add_theme_font_size_override("font_size", 56)
	_title_glow.add_theme_color_override("font_color", COLOR_GOLD_GLOW)
	_root.add_child(_title_glow)

	# Main title label
	_title_label = Label.new()
	_title_label.text = "SENGOKU TACTICS"
	_title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_title_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_title_label.set_anchors_preset(Control.PRESET_CENTER)
	_title_label.anchor_top = 0.42
	_title_label.anchor_bottom = 0.52
	_title_label.anchor_left = 0.0
	_title_label.anchor_right = 1.0
	_title_label.offset_top = 0
	_title_label.offset_bottom = 0
	_title_label.add_theme_font_size_override("font_size", 54)
	_title_label.add_theme_color_override("font_color", COLOR_GOLD)

	# Shadow
	_title_label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.7))
	_title_label.add_theme_constant_override("shadow_offset_x", 3)
	_title_label.add_theme_constant_override("shadow_offset_y", 3)

	_root.add_child(_title_label)


# ── Subtitle ─────────────────────────────────────────────────────────────────

func _build_subtitle() -> void:
	_subtitle_label = Label.new()
	_subtitle_label.text = "Age of the Warring States"
	_subtitle_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_subtitle_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_subtitle_label.set_anchors_preset(Control.PRESET_CENTER)
	_subtitle_label.anchor_top = 0.52
	_subtitle_label.anchor_bottom = 0.58
	_subtitle_label.anchor_left = 0.0
	_subtitle_label.anchor_right = 1.0
	_subtitle_label.offset_top = 0
	_subtitle_label.offset_bottom = 0
	_subtitle_label.add_theme_font_size_override("font_size", 22)
	_subtitle_label.add_theme_color_override("font_color", COLOR_CREAM)
	_subtitle_label.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.5))
	_subtitle_label.add_theme_constant_override("shadow_offset_x", 1)
	_subtitle_label.add_theme_constant_override("shadow_offset_y", 1)
	_root.add_child(_subtitle_label)


# ── Prompt ───────────────────────────────────────────────────────────────────

func _build_prompt() -> void:
	_prompt_label = Label.new()
	_prompt_label.text = "— Press ENTER or Tap to Begin —"
	_prompt_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_prompt_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_prompt_label.set_anchors_preset(Control.PRESET_CENTER)
	_prompt_label.anchor_top = 0.75
	_prompt_label.anchor_bottom = 0.80
	_prompt_label.anchor_left = 0.0
	_prompt_label.anchor_right = 1.0
	_prompt_label.offset_top = 0
	_prompt_label.offset_bottom = 0
	_prompt_label.add_theme_font_size_override("font_size", 18)
	_prompt_label.add_theme_color_override("font_color", COLOR_CREAM)
	_prompt_label.modulate.a = 0.0  # start invisible — tween fades in
	_root.add_child(_prompt_label)


# ── Version ──────────────────────────────────────────────────────────────────

func _build_version() -> void:
	_version_label = Label.new()
	_version_label.text = "v1.0"
	_version_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_version_label.vertical_alignment = VERTICAL_ALIGNMENT_BOTTOM
	_version_label.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	_version_label.offset_left = -80
	_version_label.offset_top = -30
	_version_label.offset_right = -16
	_version_label.offset_bottom = -10
	_version_label.add_theme_font_size_override("font_size", 13)
	_version_label.add_theme_color_override("font_color", COLOR_DIM_TEXT)
	_root.add_child(_version_label)


# ── Fade overlay (for show/hide transitions) ─────────────────────────────────

func _build_fade_overlay() -> void:
	_fade_overlay = ColorRect.new()
	_fade_overlay.set_anchors_preset(Control.PRESET_FULL_RECT)
	_fade_overlay.color = Color(0, 0, 0, 0)
	_fade_overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_root.add_child(_fade_overlay)


# ─────────────────────────────────────────────────────────────────────────────
#  ANIMATIONS
# ─────────────────────────────────────────────────────────────────────────────

func _start_animations() -> void:
	_animate_entrance()
	_animate_prompt_pulse()
	_animate_title_glow()


func _animate_entrance() -> void:
	# Fade the whole root in from black
	_root.modulate = Color(1, 1, 1, 0)
	var tween := create_tween()
	tween.tween_property(_root, "modulate:a", 1.0, 1.5).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)

	# Mon slides down
	var mon_start_y := _mon_container.offset_top - 30.0
	_mon_container.offset_top = mon_start_y
	tween.parallel().tween_property(_mon_container, "offset_top", mon_start_y + 30.0, 1.8)\
		.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)

	# Decorative lines expand from center
	_line_top.anchor_left = 0.48
	_line_top.anchor_right = 0.52
	_line_bottom.anchor_left = 0.48
	_line_bottom.anchor_right = 0.52

	var line_tween := create_tween()
	line_tween.set_parallel(true)
	line_tween.tween_property(_line_top, "anchor_left", 0.2, 1.2)\
		.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC).set_delay(0.6)
	line_tween.tween_property(_line_top, "anchor_right", 0.8, 1.2)\
		.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC).set_delay(0.6)
	line_tween.tween_property(_line_bottom, "anchor_left", 0.2, 1.2)\
		.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC).set_delay(0.7)
	line_tween.tween_property(_line_bottom, "anchor_right", 0.8, 1.2)\
		.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC).set_delay(0.7)

	# Prompt fades in after everything else
	var prompt_tween := create_tween()
	prompt_tween.tween_property(_prompt_label, "modulate:a", 1.0, 1.0)\
		.set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_SINE).set_delay(2.0)


func _animate_prompt_pulse() -> void:
	# Continuous fade-in / fade-out loop for the prompt text
	if _prompt_tween and _prompt_tween.is_valid():
		_prompt_tween.kill()

	_prompt_tween = create_tween().set_loops()
	_prompt_tween.tween_property(_prompt_label, "modulate:a", 0.25, 1.4)\
		.set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE).set_delay(2.5)
	_prompt_tween.tween_property(_prompt_label, "modulate:a", 1.0, 1.4)\
		.set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)


func _animate_title_glow() -> void:
	# Subtle pulsing glow behind the title
	if _glow_tween and _glow_tween.is_valid():
		_glow_tween.kill()

	_glow_tween = create_tween().set_loops()
	_glow_tween.tween_property(_title_glow, "modulate:a", 0.3, 2.0)\
		.set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)
	_glow_tween.tween_property(_title_glow, "modulate:a", 0.8, 2.0)\
		.set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)


# ─────────────────────────────────────────────────────────────────────────────
#  INPUT
# ─────────────────────────────────────────────────────────────────────────────

func _unhandled_input(event: InputEvent) -> void:
	if not _is_active:
		return

	var triggered := false

	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_ENTER or event.keycode == KEY_KP_ENTER or event.keycode == KEY_SPACE:
			triggered = true

	if event is InputEventScreenTouch and event.pressed:
		triggered = true

	# Also handle regular mouse click as "tap"
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		triggered = true

	if triggered:
		_on_start()
		get_viewport().set_input_as_handled()


func _on_start() -> void:
	_is_active = false

	# Kill looping tweens
	if _prompt_tween and _prompt_tween.is_valid():
		_prompt_tween.kill()
	if _glow_tween and _glow_tween.is_valid():
		_glow_tween.kill()

	# Brief flash and fade-out
	_prompt_label.modulate.a = 1.0
	var tween := create_tween()
	tween.tween_property(_prompt_label, "modulate:a", 0.0, 0.15)
	tween.tween_property(_prompt_label, "modulate:a", 1.0, 0.15)
	tween.tween_property(_prompt_label, "modulate:a", 0.0, 0.15)
	tween.tween_callback(start_pressed.emit)


# ─────────────────────────────────────────────────────────────────────────────
#  PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

## Fade the title screen in with a smooth transition.
func show_screen() -> void:
	visible = true
	_fade_overlay.color.a = 1.0
	_root.modulate.a = 0.0

	var tween := create_tween()
	tween.set_parallel(true)
	tween.tween_property(_root, "modulate:a", 1.0, 0.8)\
		.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
	tween.tween_property(_fade_overlay, "color:a", 0.0, 0.8)\
		.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
	await tween.finished

	_is_active = true
	_animate_prompt_pulse()
	_animate_title_glow()


## Fade the title screen out with a smooth transition.
func hide_screen() -> void:
	_is_active = false

	if _prompt_tween and _prompt_tween.is_valid():
		_prompt_tween.kill()
	if _glow_tween and _glow_tween.is_valid():
		_glow_tween.kill()

	var tween := create_tween()
	tween.tween_property(_fade_overlay, "color:a", 1.0, 0.6)\
		.set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_CUBIC)
	tween.parallel().tween_property(_root, "modulate:a", 0.0, 0.6)\
		.set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_CUBIC)
	await tween.finished

	visible = false


# ─────────────────────────────────────────────────────────────────────────────
#  MON CREST — inner class drawn with _draw()
# ─────────────────────────────────────────────────────────────────────────────

class MonDrawing extends Node2D:
	## Draws a stylised clan mon (family crest) using simple shapes.
	## The design is an outer ring with an inner hexagonal star / geometric
	## pattern reminiscent of traditional Japanese kamon.

	const MON_GOLD := Color(0.83, 0.65, 0.21)
	const MON_GOLD_FAINT := Color(0.83, 0.65, 0.21, 0.3)
	const MON_RADIUS := 48.0
	const MON_INNER_RADIUS := 36.0
	const MON_LINE_WIDTH := 2.0

	func _draw() -> void:
		# ── Outer circle ──
		draw_arc(Vector2.ZERO, MON_RADIUS, 0, TAU, 64, MON_GOLD, MON_LINE_WIDTH, true)
		# Second ring, slightly smaller
		draw_arc(Vector2.ZERO, MON_RADIUS - 4.0, 0, TAU, 64, MON_GOLD_FAINT, 1.0, true)

		# ── Inner geometric star (six-pointed) ──
		var points_outer: PackedVector2Array = []
		var points_inner: PackedVector2Array = []
		var num_points := 6

		for i in num_points:
			var angle_outer := -PI / 2.0 + TAU * i / num_points
			var angle_inner := -PI / 2.0 + TAU * (i + 0.5) / num_points
			points_outer.append(Vector2(cos(angle_outer), sin(angle_outer)) * MON_INNER_RADIUS)
			points_inner.append(Vector2(cos(angle_inner), sin(angle_inner)) * (MON_INNER_RADIUS * 0.45))

		# Draw two overlapping triangles to form the star
		for offset in [0, 1]:
			var tri: PackedVector2Array = []
			for i in 3:
				tri.append(points_outer[i * 2 + offset])
			# Filled triangle — faint
			draw_colored_polygon(tri, MON_GOLD_FAINT)
			# Triangle outline
			for i in 3:
				draw_line(tri[i], tri[(i + 1) % 3], MON_GOLD, MON_LINE_WIDTH, true)

		# ── Central circle ──
		draw_arc(Vector2.ZERO, 8.0, 0, TAU, 32, MON_GOLD, MON_LINE_WIDTH, true)
		draw_circle(Vector2.ZERO, 4.0, MON_GOLD)

		# ── Spokes from center to each outer point ──
		for i in num_points:
			var angle := -PI / 2.0 + TAU * i / num_points
			var end_point := Vector2(cos(angle), sin(angle)) * MON_INNER_RADIUS
			draw_line(Vector2.ZERO, end_point, MON_GOLD_FAINT, 1.0, true)

		# ── Small accent dots between star points on the outer ring ──
		for i in num_points:
			var angle := -PI / 2.0 + TAU * (i + 0.5) / num_points
			var dot_pos := Vector2(cos(angle), sin(angle)) * (MON_RADIUS - 2.0)
			draw_circle(dot_pos, 2.0, MON_GOLD)
