## Grid-based movement and pathfinding for the SRPG tilemap.
## Attach to a Node2D that manages the tactical grid.
class_name Grid
extends Node2D

var width: int = 0
var height: int = 0
var tiles: Array = []   # 2D array of Constants.Terrain values
var seize_points: Array[Vector2i] = []
var fort_points: Array[Vector2i] = []
var village_points: Array[Vector2i] = []


func setup(w: int, h: int, tile_data: Array) -> void:
	width = w
	height = h
	tiles = tile_data


func get_terrain(pos: Vector2i) -> int:
	if pos.x < 0 or pos.x >= width or pos.y < 0 or pos.y >= height:
		return Constants.Terrain.WALL
	return tiles[pos.y][pos.x]


func get_terrain_data(pos: Vector2i) -> Dictionary:
	var t := get_terrain(pos)
	return Constants.TERRAIN_DATA.get(t, Constants.TERRAIN_DATA[Constants.Terrain.PLAIN])


func is_valid(pos: Vector2i) -> bool:
	return pos.x >= 0 and pos.x < width and pos.y >= 0 and pos.y < height


## Get all tiles a unit can move to using BFS with terrain costs.
func get_movement_range(
	origin: Vector2i, move: int, unit_class: String,
	is_flying: bool = false, is_mounted: bool = false,
	water_walk: bool = false
) -> Array[Vector2i]:
	var result: Array[Vector2i] = []
	var visited := {}  # Vector2i → remaining_move
	var queue: Array = [[origin, move]]
	visited[origin] = move

	while not queue.is_empty():
		var current = queue.pop_front()
		var pos: Vector2i = current[0]
		var remaining: int = current[1]
		result.append(pos)

		for dir in [Vector2i.UP, Vector2i.DOWN, Vector2i.LEFT, Vector2i.RIGHT]:
			var next_pos := pos + dir
			if not is_valid(next_pos):
				continue

			var terrain := get_terrain(next_pos)
			var cost: int

			if is_flying:
				cost = 1  # Flying units ignore terrain
			else:
				var td = Constants.TERRAIN_DATA.get(terrain, {})
				cost = td.get("move", 1)
				# Mounted can't enter forests
				if is_mounted and terrain == Constants.Terrain.FOREST:
					continue
				# Water requires water_walk or bridge
				if terrain == Constants.Terrain.RIVER and not water_walk:
					cost = 3
				if terrain == Constants.Terrain.SEA and not water_walk:
					continue

			var new_remaining := remaining - cost
			if new_remaining < 0:
				continue
			if visited.has(next_pos) and visited[next_pos] >= new_remaining:
				continue

			visited[next_pos] = new_remaining
			queue.append([next_pos, new_remaining])

	return result


## Get attack range cells from a set of movement tiles.
func get_attack_range(move_tiles: Array[Vector2i], min_range: int, max_range: int) -> Array[Vector2i]:
	var attack_set := {}
	for tile in move_tiles:
		for dx in range(-max_range, max_range + 1):
			for dy in range(-max_range, max_range + 1):
				var dist := absi(dx) + absi(dy)
				if dist < min_range or dist > max_range:
					continue
				var target := tile + Vector2i(dx, dy)
				if is_valid(target) and not attack_set.has(target):
					attack_set[target] = true
	var result: Array[Vector2i] = []
	for key in attack_set:
		if not key in move_tiles:
			result.append(key)
	return result


## Convert grid position to pixel position (center of tile).
func grid_to_pixel(pos: Vector2i) -> Vector2:
	return Vector2(pos.x * Constants.TILE_SIZE + Constants.TILE_SIZE / 2.0,
	               pos.y * Constants.TILE_SIZE + Constants.TILE_SIZE / 2.0)


## Convert pixel position to grid position.
func pixel_to_grid(pixel: Vector2) -> Vector2i:
	return Vector2i(
		int(pixel.x / Constants.TILE_SIZE),
		int(pixel.y / Constants.TILE_SIZE))
