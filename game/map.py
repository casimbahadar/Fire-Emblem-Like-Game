"""
Map/Grid system for Sengoku Tactics
"""
from game.constants import *


class GameMap:
    def __init__(self, width, height, tile_data, name=""):
        """
        tile_data: 2D list [row][col] of terrain type strings
        """
        self.width  = width
        self.height = height
        self.tiles  = tile_data   # [y][x]
        self.name   = name

        # Seize/capture points (for objectives)
        self.seize_points = []   # list of (x, y)
        self.village_points = [] # list of (x, y)
        self.fort_points = []    # list of (x, y)

    def get_terrain(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return TERRAIN_CLIFF  # out of bounds = impassable

    def get_terrain_data(self, x, y):
        t = self.get_terrain(x, y)
        return TERRAIN_DATA[t]

    def is_passable(self, x, y, faction=FACTION_PLAYER):
        t = self.get_terrain(x, y)
        td = TERRAIN_DATA[t]
        return td["move"] < 99

    def move_cost(self, x, y, unit_class):
        """Return movement cost to enter this tile."""
        t = self.get_terrain(x, y)
        td = TERRAIN_DATA[t]
        cost = td["move"]

        # Class-specific modifiers
        if unit_class == CLASS_CAVALRY:
            if t in (TERRAIN_MOUNTAIN, TERRAIN_FOREST):
                cost += 2
            if t in (TERRAIN_SEA, TERRAIN_CLIFF):
                cost = 99
        if unit_class == CLASS_NINJA:
            if t == TERRAIN_MOUNTAIN:
                cost -= 1  # ninjas are agile
        if unit_class in (CLASS_MONK, CLASS_SOHEI, CLASS_ONMYOJI):
            if t == TERRAIN_RIVER:
                cost = 3  # spiritual fortitude
        return max(1, cost)

    def get_movement_range(self, x, y, move_points, unit_class):
        """BFS to compute all reachable tiles given move_points."""
        reachable = {(x, y): 0}
        frontier  = [(x, y, 0)]

        while frontier:
            cx, cy, spent = frontier.pop(0)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                cost = self.move_cost(nx, ny, unit_class)
                new_spent = spent + cost
                if new_spent <= move_points:
                    if (nx, ny) not in reachable or reachable[(nx, ny)] > new_spent:
                        reachable[(nx, ny)] = new_spent
                        frontier.append((nx, ny, new_spent))
        return set(reachable.keys())

    def get_attack_range_cells(self, reachable_tiles, min_r, max_r):
        """Return all cells attackable from any reachable tile at given weapon range."""
        attack_tiles = set()
        for (tx, ty) in reachable_tiles:
            for r in range(min_r, max_r + 1):
                for dx in range(-r, r + 1):
                    dy_abs = r - abs(dx)
                    for dy in [dy_abs, -dy_abs]:
                        if dy == 0 and dx == 0:
                            continue
                        nx, ny = tx + dx, ty + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            attack_tiles.add((nx, ny))
        return attack_tiles - reachable_tiles

    def find_path(self, sx, sy, ex, ey, unit_class, occupied):
        """A* pathfinding from (sx,sy) to (ex,ey). Returns list of (x,y) steps."""
        import heapq
        def heuristic(a, b):
            return abs(a[0]-b[0]) + abs(a[1]-b[1])

        open_set = []
        heapq.heappush(open_set, (0, (sx, sy)))
        came_from = {}
        g_score = {(sx, sy): 0}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == (ex, ey):
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            cx, cy = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                neighbor = (nx, ny)
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if neighbor in occupied and neighbor != (ex, ey):
                    continue
                cost = self.move_cost(nx, ny, unit_class)
                if cost >= 99:
                    continue
                tentative = g_score[current] + cost
                if tentative < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor]   = tentative
                    f = tentative + heuristic(neighbor, (ex, ey))
                    heapq.heappush(open_set, (f, neighbor))

        return []  # No path found


# ─── Map Definitions ──────────────────────────────────────────────────────────

P = TERRAIN_PLAIN
F = TERRAIN_FOREST
M = TERRAIN_MOUNTAIN
C = TERRAIN_CASTLE
R = TERRAIN_RIVER
D = TERRAIN_ROAD
T = TERRAIN_FORT
V = TERRAIN_VILLAGE
S = TERRAIN_SEA
L = TERRAIN_CLIFF
B = TERRAIN_BRIDGE


def make_chapter1_map():
    """
    Chapter 1: Departure from Owari
    A plains map with some forest and a river crossing.
    15x10 tiles
    """
    tiles = [
        # 0    1    2    3    4    5    6    7    8    9   10   11   12   13   14
        [  P,   P,   P,   F,   F,   M,   M,   M,   F,   P,   P,   P,   P,   P,   P ],  # 0
        [  P,   V,   P,   F,   P,   M,   P,   F,   F,   P,   P,   P,   V,   P,   P ],  # 1
        [  P,   P,   D,   D,   D,   D,   D,   D,   D,   B,   D,   D,   D,   P,   P ],  # 2
        [  P,   P,   P,   F,   P,   P,   P,   P,   P,   R,   P,   F,   P,   T,   P ],  # 3
        [  P,   P,   P,   P,   P,   F,   P,   P,   P,   R,   P,   P,   P,   P,   P ],  # 4
        [  F,   F,   P,   P,   P,   P,   P,   T,   P,   R,   P,   P,   P,   P,   F ],  # 5
        [  P,   F,   P,   P,   M,   M,   P,   P,   P,   R,   P,   P,   P,   P,   P ],  # 6
        [  P,   P,   P,   P,   M,   P,   P,   P,   P,   B,   P,   P,   V,   P,   C ],  # 7
        [  P,   P,   V,   P,   P,   P,   F,   P,   P,   D,   P,   F,   P,   P,   C ],  # 8
        [  P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   C ],  # 9
    ]
    gmap = GameMap(15, 10, tiles, name="Owari Plains")
    gmap.seize_points = [(14, 7)]
    gmap.village_points = [(1, 1), (12, 1), (2, 8), (12, 7)]
    gmap.fort_points = [(13, 3), (7, 5)]
    return gmap


def make_chapter2_map():
    """
    Chapter 2: The Battle of Okehazama - Ambush in the Forest
    Dense forest with narrow paths. 14x11 tiles.
    """
    tiles = [
        # 0    1    2    3    4    5    6    7    8    9   10   11   12   13
        [  M,   M,   F,   F,   F,   F,   F,   F,   F,   F,   F,   M,   M,   M ],  # 0
        [  M,   F,   F,   P,   F,   F,   F,   F,   P,   F,   F,   F,   M,   M ],  # 1
        [  M,   F,   P,   P,   P,   F,   F,   P,   P,   P,   F,   F,   F,   M ],  # 2
        [  F,   F,   P,   F,   P,   P,   P,   P,   F,   P,   P,   F,   F,   F ],  # 3
        [  F,   P,   P,   F,   F,   P,   V,   P,   F,   F,   P,   P,   F,   F ],  # 4
        [  P,   P,   F,   F,   P,   P,   D,   P,   P,   F,   F,   P,   P,   F ],  # 5
        [  P,   P,   F,   P,   P,   D,   D,   D,   P,   P,   F,   P,   P,   P ],  # 6
        [  P,   F,   F,   P,   D,   D,   P,   D,   D,   P,   F,   F,   P,   P ],  # 7
        [  F,   F,   P,   D,   D,   P,   P,   P,   D,   D,   P,   F,   F,   F ],  # 8
        [  F,   P,   D,   D,   P,   P,   T,   P,   P,   D,   D,   P,   F,   F ],  # 9
        [  P,   D,   D,   P,   P,   F,   F,   F,   P,   P,   D,   D,   P,   P ],  # 10
    ]
    gmap = GameMap(14, 11, tiles, name="Okehazama Forest")
    gmap.seize_points = [(6, 4)]
    gmap.village_points = [(6, 4)]
    gmap.fort_points = [(6, 9)]
    return gmap


def make_chapter3_map():
    """
    Chapter 3: Kawanakajima - The Dragon and the Tiger
    Open battlefield with a river cutting through the center. 16x12 tiles.
    """
    tiles = [
        # 0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
        [  C,   C,   D,   P,   P,   P,   P,   P,   P,   P,   P,   P,   M,   M,   M,   M ],  # 0
        [  C,   C,   D,   P,   F,   P,   P,   P,   P,   F,   P,   P,   M,   M,   M,   L ],  # 1
        [  C,   D,   D,   P,   P,   P,   P,   P,   P,   P,   P,   P,   F,   M,   L,   L ],  # 2
        [  P,   D,   P,   P,   P,   T,   P,   P,   T,   P,   P,   P,   P,   F,   M,   M ],  # 3
        [  P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   F,   M ],  # 4
        [  P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P ],  # 5
        [  R,   R,   R,   R,   B,   R,   R,   R,   B,   R,   R,   R,   R,   R,   R,   R ],  # 6
        [  P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P ],  # 7
        [  F,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   F ],  # 8
        [  F,   F,   P,   P,   T,   P,   P,   T,   P,   P,   P,   P,   P,   P,   F,   F ],  # 9
        [  M,   F,   F,   P,   P,   P,   P,   P,   P,   P,   P,   F,   P,   P,   C,   C ],  # 10
        [  M,   M,   F,   F,   P,   P,   P,   P,   P,   F,   F,   F,   F,   D,   C,   C ],  # 11
    ]
    gmap = GameMap(16, 12, tiles, name="Kawanakajima Battlefield")
    gmap.seize_points = [(1, 0), (14, 10)]
    gmap.fort_points = [(5, 3), (8, 3), (4, 9), (7, 9)]
    return gmap


def make_chapter4_map():
    """
    Chapter 4: The Fall of Honnoji - Siege and Betrayal
    A castle complex under attack. 16x12 tiles.
    """
    tiles = [
        # 0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15
        [  P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P ],  # 0
        [  P,   F,   P,   P,   C,   C,   C,   C,   C,   C,   C,   C,   P,   P,   F,   P ],  # 1
        [  P,   P,   P,   C,   C,   T,   D,   D,   D,   T,   C,   C,   C,   P,   P,   P ],  # 2
        [  P,   P,   P,   C,   D,   D,   P,   P,   P,   D,   D,   C,   P,   P,   P,   P ],  # 3
        [  P,   P,   C,   C,   D,   P,   P,   C,   P,   P,   D,   C,   C,   P,   P,   P ],  # 4
        [  P,   P,   C,   D,   P,   P,   C,   C,   C,   P,   P,   D,   C,   P,   P,   P ],  # 5
        [  P,   P,   C,   D,   P,   C,   C,   C,   C,   C,   P,   D,   C,   P,   P,   P ],  # 6
        [  P,   P,   C,   D,   P,   P,   C,   C,   C,   P,   P,   D,   C,   P,   P,   P ],  # 7
        [  P,   P,   C,   C,   D,   P,   P,   P,   P,   P,   D,   C,   C,   P,   P,   P ],  # 8
        [  P,   P,   P,   C,   D,   D,   P,   P,   P,   D,   D,   C,   P,   P,   P,   P ],  # 9
        [  P,   F,   P,   C,   C,   T,   D,   D,   D,   T,   C,   C,   C,   P,   F,   P ],  # 10
        [  P,   P,   P,   P,   C,   C,   C,   C,   C,   C,   C,   C,   P,   P,   P,   P ],  # 11
    ]
    gmap = GameMap(16, 12, tiles, name="Honnoji Temple")
    gmap.seize_points = [(7, 6)]  # The inner sanctum
    gmap.fort_points = [(5, 2), (9, 2), (5, 10), (9, 10)]
    return gmap


def make_chapter5_map():
    """
    Chapter 5: Battle of Sekigahara - The Final Clash
    Large open battlefield with mountains flanking. 18x14 tiles.
    """
    tiles = [
        # 0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17
        [  M,   M,   M,   F,   F,   P,   P,   P,   P,   P,   P,   F,   F,   M,   M,   M,   M,   M ],  # 0
        [  M,   M,   F,   F,   P,   P,   V,   P,   P,   P,   V,   P,   P,   F,   F,   M,   M,   M ],  # 1
        [  M,   F,   F,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   F,   F,   M,   M ],  # 2
        [  F,   F,   P,   P,   P,   T,   P,   P,   T,   P,   P,   T,   P,   P,   P,   F,   F,   M ],  # 3
        [  F,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   F,   F ],  # 4
        [  P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P ],  # 5
        [  P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P ],  # 6
        [  P,   P,   P,   P,   P,   P,   D,   D,   D,   D,   D,   P,   P,   P,   P,   P,   P,   P ],  # 7
        [  P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P ],  # 8
        [  P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P ],  # 9
        [  F,   P,   P,   P,   P,   T,   P,   P,   T,   P,   P,   T,   P,   P,   P,   P,   F,   F ],  # 10
        [  F,   F,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   F,   F,   M ],  # 11
        [  M,   F,   F,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   P,   F,   F,   M,   M ],  # 12
        [  M,   M,   F,   F,   P,   V,   P,   P,   P,   P,   P,   V,   P,   F,   F,   M,   M,   M ],  # 13
    ]
    gmap = GameMap(18, 14, tiles, name="Sekigahara")
    gmap.seize_points = [(9, 6)]
    gmap.village_points = [(6, 1), (10, 1), (5, 13), (11, 13)]
    gmap.fort_points = [(5, 3), (8, 3), (11, 3), (5, 10), (8, 10), (11, 10)]
    return gmap


MAP_BUILDERS = {
    1: make_chapter1_map,
    2: make_chapter2_map,
    3: make_chapter3_map,
    4: make_chapter4_map,
    5: make_chapter5_map,
}
