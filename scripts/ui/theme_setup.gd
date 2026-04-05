extends Node
class_name ThemeSetup
## Autoloaded singleton that creates and applies a dark, feudal-Japan-inspired
## UI theme to every standard Godot control via the root viewport.

# ── Palette ──────────────────────────────────────────────────────────────────
const COLOR_BG_DEEP       := Color("#0a0614")       # very dark indigo
const COLOR_BG_PANEL      := Color("#120e22e6")      # dark panel w/ slight transparency
const COLOR_BORDER_GOLD   := Color("#d4a535")        # gold accent / borders
const COLOR_ACCENT        := Color("#d4a535")        # gold / amber accent
const COLOR_ACCENT_DIM    := Color("#a07828")        # muted gold for pressed states
const COLOR_TEXT           := Color("#f0e8d0")        # cream / ivory
const COLOR_TEXT_DISABLED  := Color("#7a7060")        # dim cream
const COLOR_HOVER_GLOW    := Color("#d4a53540")      # translucent gold glow
const COLOR_BTN_BG        := Color("#1a1430")        # dark button background
const COLOR_BTN_HOVER     := Color("#261e44")        # lighter button hover
const COLOR_BTN_PRESSED   := Color("#0e0a1e")        # darker button pressed
const COLOR_DISABLED_BG   := Color("#0e0b18")        # desaturated background
const COLOR_PROGRESS_BG   := Color("#1a1430")        # bar trough
const COLOR_SCROLL_BG     := Color("#0e0a1e")        # scrollbar trough
const COLOR_SCROLL_GRAB   := Color("#3a2e5a")        # scrollbar grabber

# HP / faction fill colors
const COLOR_HP_PLAYER     := Color("#3ca854")        # green
const COLOR_HP_ENEMY      := Color("#c0392b")        # red
const COLOR_HP_ALLY       := Color("#2b9ea0")        # blue-green / teal

const FONT_SIZE_DEFAULT   := 14
const FONT_SIZE_TITLE     := 22
const FONT_SIZE_SUBTITLE  := 18
const FONT_SIZE_SMALL     := 11

# ── Lifecycle ────────────────────────────────────────────────────────────────

func _ready() -> void:
	var theme := Theme.new()
	_setup_default_font(theme)
	_setup_panel_container(theme)
	_setup_button(theme)
	_setup_label(theme)
	_setup_progress_bar(theme)
	_setup_line_edit(theme)
	_setup_rich_text_label(theme)
	_setup_tab_container(theme)
	_setup_popup_menu(theme)
	_setup_scroll_container(theme)
	_setup_tooltip(theme)
	_setup_h_separator(theme)
	_setup_check_box(theme)
	_setup_option_button(theme)
	_setup_item_list(theme)
	_setup_window(theme)

	# Apply to the entire scene tree via the root viewport.
	get_tree().root.theme = theme

# ── Font ─────────────────────────────────────────────────────────────────────

func _setup_default_font(theme: Theme) -> void:
	theme.set_default_font_size(FONT_SIZE_DEFAULT)
	# Default font colors used across many controls
	theme.set_color("font_color", "Label", COLOR_TEXT)
	theme.set_color("font_color", "Button", COLOR_TEXT)
	theme.set_color("font_color", "RichTextLabel", COLOR_TEXT)
	theme.set_color("font_color", "LineEdit", COLOR_TEXT)
	theme.set_color("font_color", "ItemList", COLOR_TEXT)
	theme.set_color("font_color", "OptionButton", COLOR_TEXT)

# ── PanelContainer ───────────────────────────────────────────────────────────

func _setup_panel_container(theme: Theme) -> void:
	var panel := _make_flat_box(COLOR_BG_PANEL, 4, COLOR_BORDER_GOLD, 1)
	theme.set_stylebox("panel", "PanelContainer", panel)

# ── Button ───────────────────────────────────────────────────────────────────

func _setup_button(theme: Theme) -> void:
	# Normal
	var normal := _make_flat_box(COLOR_BTN_BG, 4, COLOR_BORDER_GOLD, 1)
	theme.set_stylebox("normal", "Button", normal)

	# Hover – slightly lighter with an outer gold glow
	var hover := _make_flat_box(COLOR_BTN_HOVER, 4, COLOR_BORDER_GOLD, 1)
	hover.shadow_color = COLOR_HOVER_GLOW
	hover.shadow_size = 4
	theme.set_stylebox("hover", "Button", hover)

	# Pressed – sunken feel
	var pressed := _make_flat_box(COLOR_BTN_PRESSED, 4, COLOR_ACCENT_DIM, 1)
	pressed.content_margin_top = 2
	theme.set_stylebox("pressed", "Button", pressed)

	# Disabled
	var disabled := _make_flat_box(COLOR_DISABLED_BG, 4, Color("#3a3040"), 1)
	theme.set_stylebox("disabled", "Button", disabled)

	# Focus
	var focus := _make_flat_box(Color.TRANSPARENT, 4, COLOR_ACCENT, 2)
	theme.set_stylebox("focus", "Button", focus)

	# Colors
	theme.set_color("font_color", "Button", COLOR_ACCENT)
	theme.set_color("font_hover_color", "Button", COLOR_TEXT)
	theme.set_color("font_pressed_color", "Button", COLOR_ACCENT_DIM)
	theme.set_color("font_disabled_color", "Button", COLOR_TEXT_DISABLED)
	theme.set_font_size("font_size", "Button", FONT_SIZE_DEFAULT)

# ── Label ────────────────────────────────────────────────────────────────────

func _setup_label(theme: Theme) -> void:
	# Labels get a transparent background so they sit cleanly on panels.
	var label_bg := StyleBoxFlat.new()
	label_bg.bg_color = Color.TRANSPARENT
	label_bg.set_content_margin_all(0)
	theme.set_stylebox("normal", "Label", label_bg)
	theme.set_color("font_color", "Label", COLOR_TEXT)
	theme.set_color("font_shadow_color", "Label", Color(0, 0, 0, 0.5))
	theme.set_font_size("font_size", "Label", FONT_SIZE_DEFAULT)

# ── ProgressBar ──────────────────────────────────────────────────────────────

func _setup_progress_bar(theme: Theme) -> void:
	# Background (trough)
	var bg := _make_flat_box(COLOR_PROGRESS_BG, 3, COLOR_BORDER_GOLD, 1)
	bg.set_content_margin_all(0)
	theme.set_stylebox("background", "ProgressBar", bg)

	# Fill – defaults to player green; call create_hp_bar_style() for factions.
	var fill := _make_flat_box(COLOR_HP_PLAYER, 3)
	fill.set_content_margin_all(0)
	theme.set_stylebox("fill", "ProgressBar", fill)

	theme.set_color("font_color", "ProgressBar", COLOR_TEXT)
	theme.set_font_size("font_size", "ProgressBar", FONT_SIZE_SMALL)

# ── LineEdit ─────────────────────────────────────────────────────────────────

func _setup_line_edit(theme: Theme) -> void:
	var normal := _make_flat_box(COLOR_BTN_BG, 3, COLOR_BORDER_GOLD, 1)
	theme.set_stylebox("normal", "LineEdit", normal)

	var focus := _make_flat_box(COLOR_BTN_BG, 3, COLOR_ACCENT, 2)
	theme.set_stylebox("focus", "LineEdit", focus)

	theme.set_color("font_color", "LineEdit", COLOR_TEXT)
	theme.set_color("caret_color", "LineEdit", COLOR_ACCENT)
	theme.set_color("font_placeholder_color", "LineEdit", COLOR_TEXT_DISABLED)
	theme.set_color("selection_color", "LineEdit", Color(COLOR_ACCENT, 0.3))

# ── RichTextLabel ────────────────────────────────────────────────────────────

func _setup_rich_text_label(theme: Theme) -> void:
	var bg := StyleBoxFlat.new()
	bg.bg_color = Color.TRANSPARENT
	bg.set_content_margin_all(0)
	theme.set_stylebox("normal", "RichTextLabel", bg)
	theme.set_color("default_color", "RichTextLabel", COLOR_TEXT)
	theme.set_font_size("normal_font_size", "RichTextLabel", FONT_SIZE_DEFAULT)

# ── TabContainer ─────────────────────────────────────────────────────────────

func _setup_tab_container(theme: Theme) -> void:
	var panel := _make_flat_box(COLOR_BG_PANEL, 4, COLOR_BORDER_GOLD, 1)
	theme.set_stylebox("panel", "TabContainer", panel)

	var tab_selected := _make_flat_box(COLOR_BTN_HOVER, 3, COLOR_ACCENT, 1)
	theme.set_stylebox("tab_selected", "TabContainer", tab_selected)

	var tab_unselected := _make_flat_box(COLOR_BTN_BG, 3, Color("#3a3040"), 1)
	theme.set_stylebox("tab_unselected", "TabContainer", tab_unselected)

	var tab_hovered := _make_flat_box(COLOR_BTN_HOVER, 3, COLOR_ACCENT_DIM, 1)
	theme.set_stylebox("tab_hovered", "TabContainer", tab_hovered)

	theme.set_color("font_selected_color", "TabContainer", COLOR_ACCENT)
	theme.set_color("font_unselected_color", "TabContainer", COLOR_TEXT_DISABLED)
	theme.set_color("font_hovered_color", "TabContainer", COLOR_TEXT)

# ── PopupMenu ────────────────────────────────────────────────────────────────

func _setup_popup_menu(theme: Theme) -> void:
	var panel := _make_flat_box(COLOR_BG_PANEL, 4, COLOR_BORDER_GOLD, 1)
	theme.set_stylebox("panel", "PopupMenu", panel)

	var hover := _make_flat_box(COLOR_BTN_HOVER, 2, Color.TRANSPARENT, 0)
	theme.set_stylebox("hover", "PopupMenu", hover)

	theme.set_color("font_color", "PopupMenu", COLOR_TEXT)
	theme.set_color("font_hover_color", "PopupMenu", COLOR_ACCENT)
	theme.set_color("font_disabled_color", "PopupMenu", COLOR_TEXT_DISABLED)

# ── ScrollContainer / ScrollBar ──────────────────────────────────────────────

func _setup_scroll_container(theme: Theme) -> void:
	# VScrollBar
	var scroll_bg := _make_flat_box(COLOR_SCROLL_BG, 3)
	theme.set_stylebox("scroll", "VScrollBar", scroll_bg)

	var grabber := _make_flat_box(COLOR_SCROLL_GRAB, 3)
	theme.set_stylebox("grabber", "VScrollBar", grabber)

	var grabber_highlight := _make_flat_box(COLOR_ACCENT_DIM, 3)
	theme.set_stylebox("grabber_highlight", "VScrollBar", grabber_highlight)

	var grabber_pressed := _make_flat_box(COLOR_ACCENT, 3)
	theme.set_stylebox("grabber_pressed", "VScrollBar", grabber_pressed)

	# HScrollBar
	theme.set_stylebox("scroll", "HScrollBar", scroll_bg.duplicate())
	theme.set_stylebox("grabber", "HScrollBar", grabber.duplicate())
	theme.set_stylebox("grabber_highlight", "HScrollBar", grabber_highlight.duplicate())
	theme.set_stylebox("grabber_pressed", "HScrollBar", grabber_pressed.duplicate())

# ── Tooltip ──────────────────────────────────────────────────────────────────

func _setup_tooltip(theme: Theme) -> void:
	var panel := _make_flat_box(Color("#0e0a1eee"), 4, COLOR_BORDER_GOLD, 1)
	panel.set_content_margin_all(8)
	theme.set_stylebox("panel", "TooltipPanel", panel)
	theme.set_color("font_color", "TooltipLabel", COLOR_TEXT)
	theme.set_font_size("font_size", "TooltipLabel", FONT_SIZE_SMALL)

# ── HSeparator ───────────────────────────────────────────────────────────────

func _setup_h_separator(theme: Theme) -> void:
	var sep := StyleBoxFlat.new()
	sep.bg_color = COLOR_BORDER_GOLD
	sep.set_content_margin_all(0)
	sep.content_margin_top = 0
	sep.content_margin_bottom = 0
	theme.set_stylebox("separator", "HSeparator", sep)
	theme.set_constant("separation", "HSeparator", 6)

# ── CheckBox ─────────────────────────────────────────────────────────────────

func _setup_check_box(theme: Theme) -> void:
	theme.set_color("font_color", "CheckBox", COLOR_TEXT)
	theme.set_color("font_hover_color", "CheckBox", COLOR_ACCENT)
	theme.set_color("font_pressed_color", "CheckBox", COLOR_ACCENT_DIM)

	var normal := _make_flat_box(COLOR_BTN_BG, 3, COLOR_BORDER_GOLD, 1)
	theme.set_stylebox("normal", "CheckBox", normal)
	var hover := _make_flat_box(COLOR_BTN_HOVER, 3, COLOR_BORDER_GOLD, 1)
	theme.set_stylebox("hover", "CheckBox", hover)

# ── OptionButton ─────────────────────────────────────────────────────────────

func _setup_option_button(theme: Theme) -> void:
	var normal := _make_flat_box(COLOR_BTN_BG, 4, COLOR_BORDER_GOLD, 1)
	theme.set_stylebox("normal", "OptionButton", normal)

	var hover := _make_flat_box(COLOR_BTN_HOVER, 4, COLOR_BORDER_GOLD, 1)
	hover.shadow_color = COLOR_HOVER_GLOW
	hover.shadow_size = 4
	theme.set_stylebox("hover", "OptionButton", hover)

	var pressed := _make_flat_box(COLOR_BTN_PRESSED, 4, COLOR_ACCENT_DIM, 1)
	theme.set_stylebox("pressed", "OptionButton", pressed)

	var disabled := _make_flat_box(COLOR_DISABLED_BG, 4, Color("#3a3040"), 1)
	theme.set_stylebox("disabled", "OptionButton", disabled)

	theme.set_color("font_color", "OptionButton", COLOR_ACCENT)
	theme.set_color("font_hover_color", "OptionButton", COLOR_TEXT)

# ── ItemList ─────────────────────────────────────────────────────────────────

func _setup_item_list(theme: Theme) -> void:
	var panel := _make_flat_box(COLOR_BG_PANEL, 4, COLOR_BORDER_GOLD, 1)
	theme.set_stylebox("panel", "ItemList", panel)

	var selected := _make_flat_box(Color(COLOR_ACCENT, 0.25), 2)
	theme.set_stylebox("selected", "ItemList", selected)
	theme.set_stylebox("selected_focus", "ItemList", selected.duplicate())

	var cursor := _make_flat_box(Color.TRANSPARENT, 2, COLOR_ACCENT, 1)
	theme.set_stylebox("cursor_unfocused", "ItemList", cursor)
	theme.set_stylebox("cursor", "ItemList", cursor.duplicate())

	theme.set_color("font_color", "ItemList", COLOR_TEXT)
	theme.set_color("font_selected_color", "ItemList", COLOR_ACCENT)

# ── Window ───────────────────────────────────────────────────────────────────

func _setup_window(theme: Theme) -> void:
	var embedded := _make_flat_box(COLOR_BG_DEEP, 6, COLOR_BORDER_GOLD, 2)
	embedded.set_content_margin_all(4)
	theme.set_stylebox("embedded_border", "Window", embedded)
	theme.set_color("title_color", "Window", COLOR_ACCENT)
	theme.set_font_size("title_size", "Window", FONT_SIZE_SUBTITLE)

# ── Static helpers ───────────────────────────────────────────────────────────

## Returns a StyleBoxFlat suitable for the fill portion of an HP ProgressBar,
## tinted according to the unit's faction.
##   0 = PLAYER  (green)
##   1 = ENEMY   (red)
##   2 = ALLY    (blue-green)
static func create_hp_bar_style(faction: int) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.corner_radius_top_left = 3
	style.corner_radius_top_right = 3
	style.corner_radius_bottom_left = 3
	style.corner_radius_bottom_right = 3
	style.set_content_margin_all(0)

	match faction:
		Constants.Faction.PLAYER:  # 0
			style.bg_color = COLOR_HP_PLAYER
		Constants.Faction.ENEMY:   # 1
			style.bg_color = COLOR_HP_ENEMY
		Constants.Faction.ALLY:    # 2
			style.bg_color = COLOR_HP_ALLY
		_:
			style.bg_color = Color.GRAY

	return style


## Returns the primary UI colour associated with a faction, matching the
## constants already established in Constants.gd but in our theme palette.
static func get_faction_color(faction: int) -> Color:
	match faction:
		Constants.Faction.PLAYER:
			return Color(0.3, 0.5, 0.9)   # soft blue
		Constants.Faction.ENEMY:
			return Color(0.9, 0.3, 0.3)   # crimson
		Constants.Faction.ALLY:
			return Color(0.3, 0.8, 0.4)   # verdant green
		_:
			return Color.WHITE


## Returns a richer, more saturated colour used for unit badge circle
## backgrounds, providing clear at-a-glance faction identification.
static func get_unit_badge_color(faction: int) -> Color:
	match faction:
		Constants.Faction.PLAYER:
			return Color(0.15, 0.30, 0.65) # deep royal blue
		Constants.Faction.ENEMY:
			return Color(0.65, 0.15, 0.15) # dark crimson
		Constants.Faction.ALLY:
			return Color(0.15, 0.55, 0.25) # forest green
		_:
			return Color(0.4, 0.4, 0.4)    # neutral grey

# ── Internal ─────────────────────────────────────────────────────────────────

## Convenience factory for StyleBoxFlat with common settings.
static func _make_flat_box(
		bg_color: Color,
		corner_radius: int,
		border_color: Color = Color.TRANSPARENT,
		border_width: int = 0
) -> StyleBoxFlat:
	var box := StyleBoxFlat.new()
	box.bg_color = bg_color
	box.corner_radius_top_left = corner_radius
	box.corner_radius_top_right = corner_radius
	box.corner_radius_bottom_left = corner_radius
	box.corner_radius_bottom_right = corner_radius

	if border_width > 0:
		box.border_width_top = border_width
		box.border_width_bottom = border_width
		box.border_width_left = border_width
		box.border_width_right = border_width
		box.border_color = border_color

	box.set_content_margin_all(6)
	return box
