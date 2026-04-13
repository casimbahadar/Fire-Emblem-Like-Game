## Turn manager — handles phase cycling: Player → Enemy → Ally → next turn.
class_name TurnManager
extends RefCounted

var turn_number: int = 1
var current_faction: int = Constants.Faction.PLAYER

signal phase_started(faction: int, turn: int)
signal phase_ended(faction: int)


func start_player_turn() -> void:
	current_faction = Constants.Faction.PLAYER
	phase_started.emit(Constants.Faction.PLAYER, turn_number)
	EventBus.turn_started.emit(Constants.Faction.PLAYER, turn_number)


func end_player_turn() -> void:
	phase_ended.emit(Constants.Faction.PLAYER)
	EventBus.turn_ended.emit(Constants.Faction.PLAYER)
	current_faction = Constants.Faction.ENEMY


func start_enemy_turn() -> void:
	current_faction = Constants.Faction.ENEMY
	phase_started.emit(Constants.Faction.ENEMY, turn_number)
	EventBus.phase_changed.emit(Constants.Faction.ENEMY)


func end_enemy_turn() -> void:
	phase_ended.emit(Constants.Faction.ENEMY)
	current_faction = Constants.Faction.ALLY


func start_ally_turn() -> void:
	current_faction = Constants.Faction.ALLY
	phase_started.emit(Constants.Faction.ALLY, turn_number)
	EventBus.phase_changed.emit(Constants.Faction.ALLY)


func end_ally_turn() -> void:
	phase_ended.emit(Constants.Faction.ALLY)
	turn_number += 1
	start_player_turn()


func reset() -> void:
	turn_number = 1
	current_faction = Constants.Faction.PLAYER
