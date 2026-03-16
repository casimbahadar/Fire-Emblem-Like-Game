"""
Map/Grid system for Sengoku Tactics
"""
import heapq
from game.constants import *


class GameMap:
    def __init__(self, width, height, tile_data, name=""):
        self.width  = width
        self.height = height
        self.tiles  = tile_data  # [y][x]
        self.name   = name
        self.seize_points   = []
        self.village_points = []
        self.fort_points    = []
        self.gate_points    = []

    def get_terrain(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return TERRAIN_CLIFF

    def get_terrain_data(self, x, y):
        return TERRAIN_DATA[self.get_terrain(x, y)]

    def is_passable(self, x, y, is_flying=False, water_walk=False):
        t = self.get_terrain(x, y)
        if t == TERRAIN_CLIFF or t == TERRAIN_PEAK:
            return False
        if t in (TERRAIN_SEA, TERRAIN_RIVER):
            return is_flying or water_walk
        return True

    def move_cost(self, x, y, unit_class, is_flying=False, is_mounted=False,
                  water_walk=False):
        t = self.get_terrain(x, y)
        # Impassable for all
        if t in (TERRAIN_CLIFF, TERRAIN_PEAK):
            return 99
        # Water tiles
        if t in (TERRAIN_SEA, TERRAIN_RIVER):
            if is_flying or water_walk:
                return 1
            return 99
        # Flying ignores terrain cost (all passable = 1)
        if is_flying:
            return 1
        td = TERRAIN_DATA[t]
        cost = td["move"]
        # Mounted penalties
        if is_mounted:
            if t in (TERRAIN_MOUNTAIN, TERRAIN_THICKET):
                cost += 3
            if t in (TERRAIN_FOREST,):
                cost += 2
        # Ninja class bonus in rough terrain
        if unit_class == CLASS_NINJA or unit_class == CLASS_KUNOICHI:
            if t in (TERRAIN_MOUNTAIN, TERRAIN_FOREST):
                cost = max(1, cost - 1)
        return max(1, cost)

    def get_movement_range(self, x, y, move_points, unit_class,
                           is_flying=False, is_mounted=False, water_walk=False):
        reachable = {(x, y): 0}
        frontier  = [(x, y, 0)]
        while frontier:
            cx, cy, spent = frontier.pop(0)
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = cx+dx, cy+dy
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                cost = self.move_cost(nx, ny, unit_class, is_flying,
                                      is_mounted, water_walk)
                new_spent = spent + cost
                if new_spent <= move_points:
                    if (nx,ny) not in reachable or reachable[(nx,ny)] > new_spent:
                        reachable[(nx,ny)] = new_spent
                        frontier.append((nx, ny, new_spent))
        return set(reachable.keys())

    def get_attack_range_cells(self, reachable_tiles, min_r, max_r):
        attack_tiles = set()
        for (tx, ty) in reachable_tiles:
            for r in range(min_r, max_r+1):
                for dx in range(-r, r+1):
                    dy_abs = r - abs(dx)
                    for dy in [dy_abs, -dy_abs]:
                        if dy == 0 and dx == 0:
                            continue
                        nx, ny = tx+dx, ty+dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            attack_tiles.add((nx, ny))
        return attack_tiles - reachable_tiles

    def find_path(self, sx, sy, ex, ey, unit_class, occupied,
                  is_flying=False, is_mounted=False, water_walk=False):
        def heuristic(a, b):
            return abs(a[0]-b[0]) + abs(a[1]-b[1])
        open_set = []
        heapq.heappush(open_set, (0, (sx, sy)))
        came_from = {}
        g_score = {(sx,sy): 0}
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
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = cx+dx, cy+dy
                neighbor = (nx, ny)
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if neighbor in occupied and neighbor != (ex, ey):
                    continue
                cost = self.move_cost(nx, ny, unit_class, is_flying,
                                      is_mounted, water_walk)
                if cost >= 99:
                    continue
                tentative = g_score[current] + cost
                if tentative < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor]   = tentative
                    f = tentative + heuristic(neighbor, (ex, ey))
                    heapq.heappush(open_set, (f, neighbor))
        return []


# ─── Terrain shorthand ────────────────────────────────────────────────────────
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
U = TERRAIN_RUINS
E = TERRAIN_DESERT
K = TERRAIN_PEAK
H = TERRAIN_THICKET
G = TERRAIN_GATE


# ─── MAP 1: Owari Plains ─────────────────────────────────────────────────────
def make_chapter1_map():
    tiles = [
        [P, P, P, F, F, M, M, M, F, P, P, P, P, P, P],
        [P, V, P, F, P, M, P, F, F, P, P, P, V, P, P],
        [P, P, D, D, D, D, D, D, D, B, D, D, D, P, P],
        [P, P, P, F, P, P, P, P, P, R, P, F, P, T, P],
        [P, P, P, P, P, F, P, P, P, R, P, P, P, P, P],
        [F, F, P, P, P, P, P, T, P, R, P, P, P, P, F],
        [P, F, P, P, M, M, P, P, P, R, P, P, P, P, P],
        [P, P, P, P, M, P, P, P, P, B, P, P, V, P, C],
        [P, P, V, P, P, P, F, P, P, D, P, F, P, P, C],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, C],
    ]
    gmap = GameMap(15, 10, tiles, name="Owari Plains")
    gmap.seize_points   = [(14, 7)]
    gmap.village_points = [(1,1),(12,1),(2,8),(12,7)]
    gmap.fort_points    = [(13,3),(7,5)]
    return gmap


# ─── MAP 2: Okehazama Forest ──────────────────────────────────────────────────
def make_chapter2_map():
    tiles = [
        [M, M, F, F, F, F, F, F, F, F, F, M, M, M],
        [M, F, F, P, F, F, F, F, P, F, F, F, M, M],
        [M, F, P, P, P, F, F, P, P, P, F, F, F, M],
        [F, F, P, F, P, P, P, P, F, P, P, F, F, F],
        [F, P, P, F, F, P, V, P, F, F, P, P, F, F],
        [P, P, F, F, P, P, D, P, P, F, F, P, P, F],
        [P, P, F, P, P, D, D, D, P, P, F, P, P, P],
        [P, F, F, P, D, D, P, D, D, P, F, F, P, P],
        [F, F, P, D, D, P, P, P, D, D, P, F, F, F],
        [F, P, D, D, P, P, T, P, P, D, D, P, F, F],
        [P, D, D, P, P, F, F, F, P, P, D, D, P, P],
    ]
    gmap = GameMap(14, 11, tiles, name="Okehazama Forest")
    gmap.seize_points   = [(6,4)]
    gmap.village_points = [(6,4)]
    gmap.fort_points    = [(6,9)]
    return gmap


# ─── MAP 3: Kawanakajima ──────────────────────────────────────────────────────
def make_chapter3_map():
    tiles = [
        [C, C, D, P, P, P, P, P, P, P, P, P, M, M, M, M],
        [C, C, D, P, F, P, P, P, P, F, P, P, M, M, M, L],
        [C, D, D, P, P, P, P, P, P, P, P, P, F, M, L, L],
        [P, D, P, P, P, T, P, P, T, P, P, P, P, F, M, M],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, M],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [R, R, R, R, B, R, R, R, B, R, R, R, R, R, R, R],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [F, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F],
        [F, F, P, P, T, P, P, T, P, P, P, P, P, P, F, F],
        [M, F, F, P, P, P, P, P, P, P, P, F, P, P, C, C],
        [M, M, F, F, P, P, P, P, P, F, F, F, F, D, C, C],
    ]
    gmap = GameMap(16, 12, tiles, name="Kawanakajima Battlefield")
    gmap.seize_points = [(1,0),(14,10)]
    gmap.fort_points  = [(5,3),(8,3),(4,9),(7,9)]
    return gmap


# ─── MAP 4: Honnoji Temple ────────────────────────────────────────────────────
def make_chapter4_map():
    # 18 columns x 14 rows
    # Kyoto city grid — Honnoji Temple compound at center-north
    # Streets form a true grid (road tiles); outer districts have residences
    # (village tiles) and merchant buildings (ruins/castle tiles)
    # Temple: walled compound (castle tiles) with moat-ditch (river) on N side
    # Four gates: N outer gate (row 1), W/E wall gates (row 4/5), S inner gate
    # Defensive towers (fort) at compound corners; main hall = seize objective
    # Mitsuhide's troops approach from S, E, W simultaneously
    tiles = [
        #0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17
        [D,  U,  D,  U,  U,  D,  U,  D,  D,  U,  D,  U,  U,  D,  U,  U,  D,  U],  # 0  N city blocks
        [D,  V,  D,  U,  P,  D,  P,  G,  G,  P,  D,  P,  U,  D,  P,  V,  D,  U],  # 1  N outer gate + residences
        [D,  P,  D,  P,  P,  D,  R,  R,  R,  R,  D,  P,  P,  D,  P,  P,  D,  U],  # 2  moat/ditch N of temple
        [D,  U,  D,  U,  C,  C,  C,  T,  T,  C,  C,  C,  U,  D,  U,  U,  D,  U],  # 3  temple outer N wall + towers
        [D,  D,  D,  G,  C,  D,  D,  D,  D,  D,  D,  C,  G,  D,  D,  D,  D,  D],  # 4  W gate — inner road — E gate
        [D,  U,  D,  C,  C,  D,  C,  C,  C,  C,  D,  C,  C,  D,  U,  U,  D,  U],  # 5  temple inner N approach
        [D,  P,  D,  C,  D,  D,  C,  T,  C,  T,  D,  D,  C,  D,  P,  P,  D,  U],  # 6  inner ward — shrine bldgs
        [D,  U,  D,  C,  D,  C,  C,  C,  C,  C,  C,  D,  C,  D,  U,  U,  D,  U],  # 7  main hall corridor
        [D,  P,  D,  C,  D,  C,  T,  C,  C,  C,  T,  C,  C,  D,  P,  P,  D,  U],  # 8  main hall (seize) + flanks
        [D,  U,  D,  C,  D,  C,  C,  C,  C,  C,  C,  D,  C,  D,  U,  U,  D,  U],  # 9  inner ward S
        [D,  D,  D,  G,  C,  D,  D,  D,  D,  D,  D,  C,  G,  D,  D,  D,  D,  D],  # 10 S gate — inner road — E gate
        [D,  P,  D,  U,  C,  C,  C,  T,  T,  C,  C,  C,  U,  D,  P,  P,  D,  U],  # 11 temple outer S wall + towers
        [D,  V,  D,  U,  P,  D,  P,  G,  G,  P,  D,  P,  U,  D,  P,  V,  D,  U],  # 12 S outer gate + residences
        [D,  P,  D,  U,  U,  D,  U,  D,  D,  U,  D,  U,  U,  D,  U,  P,  D,  U],  # 13 S city blocks / entry
    ]
    gmap = GameMap(18, 14, tiles, name="Honnoji Temple — Night of Flames")
    gmap.seize_points   = [(7, 8), (8, 8)]                      # main hall inner sanctum
    gmap.village_points = [(1, 1), (15, 1), (1, 12), (15, 12)]  # residential districts
    gmap.fort_points    = [(7, 3), (9, 3), (6, 6), (9, 6), (6, 8), (9, 8), (7, 11), (9, 11)]
    gmap.gate_points    = [(7, 1), (8, 1), (3, 4), (12, 4), (3, 10), (12, 10), (7, 12), (8, 12)]
    return gmap


# ─── MAP 5: Sekigahara ────────────────────────────────────────────────────────
def make_chapter5_map():
    tiles = [
        [M, M, M, F, F, P, P, P, P, P, P, F, F, M, M, M, M, M],
        [M, M, F, F, P, P, V, P, P, P, V, P, P, F, F, M, M, M],
        [M, F, F, P, P, P, P, P, P, P, P, P, P, P, F, F, M, M],
        [F, F, P, P, P, T, P, P, T, P, P, T, P, P, P, F, F, M],
        [F, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, D, D, D, D, D, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [F, P, P, P, P, T, P, P, T, P, P, T, P, P, P, P, F, F],
        [F, F, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F, M],
        [M, F, F, P, P, P, P, P, P, P, P, P, P, P, F, F, M, M],
        [M, M, F, F, P, V, P, P, P, P, P, V, P, F, F, M, M, M],
    ]
    gmap = GameMap(18, 14, tiles, name="Sekigahara")
    gmap.seize_points   = [(9,6)]
    gmap.village_points = [(6,1),(10,1),(5,13),(11,13)]
    gmap.fort_points    = [(5,3),(8,3),(11,3),(5,10),(8,10),(11,10)]
    return gmap


# ─── MAP 6: Siege of Inabayama Castle ────────────────────────────────────────
def make_chapter6_map():
    tiles = [
        [L, L, M, M, C, C, C, C, C, M, M, L, L, L, L, L],
        [L, M, M, F, C, T, D, T, C, F, M, M, L, L, L, L],
        [L, M, F, F, T, D, D, D, T, F, F, M, L, L, L, L],
        [M, M, F, P, D, D, P, D, D, P, F, M, M, L, L, L],
        [M, F, F, P, P, D, P, D, P, P, F, F, M, L, L, L],
        [M, F, P, P, F, P, P, P, F, P, P, F, M, M, L, L],
        [F, F, P, P, P, P, T, P, P, P, P, F, F, M, L, L],
        [F, P, P, P, P, P, P, P, P, P, P, P, F, F, M, L],
        [P, P, P, P, F, P, P, P, F, P, P, P, P, F, M, M],
        [P, P, D, D, D, D, D, D, D, D, D, D, P, P, P, M],
        [P, P, P, P, P, P, V, P, V, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
    ]
    gmap = GameMap(16, 13, tiles, name="Inabayama Castle Mountain")
    gmap.seize_points   = [(6,0),(7,0)]
    gmap.village_points = [(6,10),(8,10)]
    gmap.fort_points    = [(5,1),(7,1),(7,2),(4,2),(8,2),(6,6)]
    gmap.gate_points    = [(5,1)]
    return gmap


# ─── MAP 7: Battle of Anegawa ─────────────────────────────────────────────────
def make_chapter7_map():
    tiles = [
        [M, M, F, F, P, P, P, P, P, P, P, P, F, F, M, M, M, M],
        [M, F, F, P, P, V, P, P, P, P, V, P, P, F, F, M, M, M],
        [F, F, P, P, P, P, P, P, P, P, P, P, P, P, F, F, M, M],
        [F, P, P, P, T, P, P, P, P, P, P, T, P, P, P, F, F, M],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, R, R, R, R, R, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, B, R, R, R, B, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, R, R, R, R, R, P, P, P, P, P, P, P],
        [F, P, P, P, T, P, P, P, P, P, P, T, P, P, P, F, F, M],
        [F, F, P, P, P, P, P, P, P, P, P, P, P, P, F, F, M, M],
        [M, F, F, P, P, V, P, P, P, P, V, P, P, F, F, M, M, M],
    ]
    gmap = GameMap(18, 12, tiles, name="Anegawa River Crossing")
    gmap.seize_points   = [(2,0),(15,0)]
    gmap.village_points = [(5,1),(10,1),(5,11),(10,11)]
    gmap.fort_points    = [(4,3),(11,3),(4,9),(11,9)]
    return gmap


# ─── MAP 8: Nagashima Island Fortress ────────────────────────────────────────
def make_chapter8_map():
    tiles = [
        [S, S, S, S, S, S, S, S, S, S, S, S, S, S, S, S],
        [S, S, P, P, B, R, R, R, R, R, B, P, P, S, S, S],
        [S, P, V, P, R, P, P, P, P, P, R, P, V, P, S, S],
        [S, P, P, P, B, P, T, P, T, P, B, P, P, P, S, S],
        [S, B, R, R, R, P, P, P, P, P, R, R, R, B, S, S],
        [S, R, P, T, P, P, C, C, P, P, P, T, P, R, S, S],
        [S, R, P, P, P, C, C, C, C, P, P, P, P, R, S, S],
        [S, R, P, T, P, P, C, C, P, P, P, T, P, R, S, S],
        [S, B, R, R, R, P, P, P, P, P, R, R, R, B, S, S],
        [S, P, P, P, B, P, T, P, T, P, B, P, P, P, S, S],
        [S, P, V, P, R, P, P, P, P, P, R, P, V, P, S, S],
        [S, S, P, P, B, R, R, R, R, R, B, P, P, S, S, S],
        [S, S, S, S, S, S, S, S, S, S, S, S, S, S, S, S],
    ]
    gmap = GameMap(16, 13, tiles, name="Nagashima Island Fortress")
    gmap.seize_points   = [(6,6),(7,6)]
    gmap.village_points = [(2,2),(11,2),(2,10),(11,10)]
    gmap.fort_points    = [(6,3),(8,3),(3,5),(11,5),(3,7),(11,7),(6,9),(8,9)]
    return gmap


# ─── MAP 9: Before Nagashino (Takeda approach) ───────────────────────────────
def make_chapter9_map():
    tiles = [
        [M, M, M, F, F, P, P, P, P, P, F, F, M, M, M, M, M, M],
        [M, M, F, F, P, P, V, P, P, V, P, P, F, F, M, M, M, M],
        [M, F, F, P, P, P, P, P, P, P, P, P, P, F, F, M, M, M],
        [F, F, P, P, P, T, P, P, P, P, T, P, P, P, F, F, M, M],
        [F, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F, M],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F],
        [P, P, P, R, R, R, B, R, R, B, R, R, R, P, P, P, P, P],
        [P, P, P, R, C, C, C, C, C, C, C, C, R, P, P, P, P, P],
        [P, P, P, R, C, T, D, D, D, D, T, C, R, P, P, P, P, P],
        [P, P, P, R, C, C, C, C, C, C, C, C, R, P, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [F, P, P, P, P, T, P, P, P, P, T, P, P, P, P, F, F, M],
        [M, F, F, P, P, P, P, P, P, P, P, P, P, F, F, M, M, M],
    ]
    gmap = GameMap(18, 13, tiles, name="Nagashino Castle Area")
    gmap.seize_points   = [(6,7),(7,7),(8,7)]
    gmap.village_points = [(6,1),(9,1)]
    gmap.fort_points    = [(5,3),(10,3),(5,11),(10,11),(5,8),(10,8)]
    return gmap


# ─── MAP 10: Battle of Nagashino ─────────────────────────────────────────────
def make_chapter10_map():
    tiles = [
        [M, M, M, F, F, P, P, P, P, P, P, F, F, M, M, M, M, M, M, M],
        [M, M, F, F, P, P, V, P, P, P, V, P, P, F, F, M, M, M, M, M],
        [M, F, F, P, P, P, P, P, P, P, P, P, P, P, F, F, M, M, M, M],
        [F, F, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F, M, M, M],
        [T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T],  # Palisade!
        [D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D],  # Firing line
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [F, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F],
        [F, F, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F],
        [M, F, F, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F, M],
        [M, M, F, F, P, P, P, P, P, P, P, P, P, P, P, P, F, F, M, M],
        [M, M, M, F, F, P, V, P, P, P, P, V, P, F, F, M, M, M, M, M],
    ]
    gmap = GameMap(20, 13, tiles, name="Nagashino — Volley Line")
    gmap.seize_points   = [(10,0)]
    gmap.village_points = [(6,1),(10,1),(6,12),(11,12)]
    gmap.fort_points    = list((x,4) for x in range(20))  # the whole palisade row
    return gmap


# ─── MAP 11: Chugoku Campaign (vs. Mori) ─────────────────────────────────────
def make_chapter11_map():
    tiles = [
        [S, S, S, S, S, P, P, P, P, P, P, P, M, M, M, M, M, M],
        [S, S, S, P, P, P, V, P, P, V, P, P, F, M, M, M, M, M],
        [S, S, P, P, P, P, P, P, P, P, P, P, F, F, M, M, M, M],
        [S, P, P, V, P, P, P, P, P, P, V, P, P, F, F, M, M, M],
        [S, P, P, P, P, F, F, P, F, F, P, P, P, P, F, F, M, M],
        [P, P, P, P, F, F, P, P, P, F, F, P, P, P, P, F, F, M],
        [P, P, P, P, F, P, T, P, T, P, F, P, P, P, P, P, F, F],
        [P, P, D, D, D, D, D, D, D, D, D, D, D, D, P, P, P, P],
        [P, P, P, P, F, P, T, P, T, P, F, P, P, P, P, P, P, P],
        [P, P, P, P, F, F, P, P, P, F, F, P, P, P, P, F, F, M],
        [S, P, P, P, P, F, F, P, F, F, P, P, P, P, F, F, M, M],
        [S, S, P, P, P, P, P, P, P, P, P, P, F, F, M, M, M, M],
        [S, S, S, P, P, C, C, D, C, C, P, P, F, M, M, M, M, M],
        [S, S, S, S, P, C, C, C, C, C, P, S, S, S, M, M, M, M],
    ]
    gmap = GameMap(18, 14, tiles, name="Chugoku Western Campaign")
    gmap.seize_points   = [(6,12),(7,12),(8,12)]
    gmap.village_points = [(6,1),(9,1),(3,3),(10,3)]
    gmap.fort_points    = [(6,6),(8,6),(6,8),(8,8)]
    return gmap


# ─── MAP 12: Siege of Takamatsu (Flooded) ────────────────────────────────────
def make_chapter12_map():
    tiles = [
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [P, F, P, P, P, P, P, P, P, P, P, P, P, F, P, P],
        [P, P, P, R, R, R, R, R, R, R, R, R, P, P, P, P],
        [P, P, R, R, C, C, C, C, C, C, R, R, R, P, P, P],
        [P, P, R, C, C, T, D, D, T, C, C, R, P, P, P, P],
        [P, P, R, C, D, D, P, P, D, D, C, R, P, P, P, P],
        [P, P, R, C, D, P, C, C, D, P, C, R, P, P, P, P],
        [P, P, R, C, D, D, P, P, D, D, C, R, P, P, P, P],
        [P, P, R, C, C, T, D, D, T, C, C, R, P, P, P, P],
        [P, P, R, R, C, C, C, C, C, C, R, R, R, P, P, P],
        [P, P, P, R, R, R, R, R, R, R, R, R, P, P, P, P],
        [P, F, P, P, P, P, P, P, P, P, P, P, P, F, P, P],
    ]
    gmap = GameMap(16, 12, tiles, name="Takamatsu Castle — Flooded")
    gmap.seize_points   = [(6,6),(7,6)]
    gmap.fort_points    = [(5,4),(8,4),(5,8),(8,8)]
    return gmap


# ─── MAP 13: Battle of Yamazaki ──────────────────────────────────────────────
def make_chapter13_map():
    tiles = [
        [M, M, M, F, P, P, P, P, P, P, P, F, M, M, M, M, M, M],
        [M, M, F, F, P, P, V, P, V, P, P, F, F, M, M, M, M, M],
        [M, F, F, P, P, P, P, P, P, P, P, P, F, F, M, M, M, M],
        [M, F, P, P, P, T, P, P, P, T, P, P, P, F, M, M, M, M],
        [F, P, P, P, P, P, P, P, P, P, P, P, P, P, F, M, M, M],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, M, M],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F],
        [P, P, D, D, D, D, D, D, D, D, D, D, D, D, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, M, M],
        [F, P, P, P, P, T, P, P, T, P, P, P, P, P, F, M, M, M],
        [M, F, F, P, P, P, P, P, P, P, P, P, F, F, M, M, M, M],
        [M, M, F, F, P, P, P, P, P, P, P, F, F, M, M, M, M, M],
    ]
    gmap = GameMap(18, 13, tiles, name="Yamazaki — The Reckoning")
    gmap.seize_points   = [(9,0)]
    gmap.village_points = [(6,1),(8,1)]
    gmap.fort_points    = [(5,3),(9,3),(5,10),(8,10)]
    return gmap


# ─── MAP 14: Battle of Shizugatake ───────────────────────────────────────────
def make_chapter14_map():
    tiles = [
        [L, L, M, C, C, C, D, C, C, C, M, L, L, L, L, L],
        [L, M, M, C, T, D, D, D, T, C, M, M, L, L, L, L],
        [L, M, F, F, D, P, P, P, D, F, F, M, L, L, L, L],
        [M, M, F, P, P, P, T, P, P, P, F, M, M, L, L, L],
        [M, F, P, P, P, P, P, P, P, P, P, F, M, M, L, L],
        [F, P, P, P, P, P, P, P, P, P, P, P, F, M, L, L],
        [P, P, P, P, F, P, P, P, F, P, P, P, P, F, M, L],
        [P, P, P, F, F, P, T, P, F, F, P, P, P, F, M, M],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, M],
        [P, P, D, D, D, D, D, D, D, D, D, D, P, P, P, F],
        [P, P, P, P, P, P, V, P, V, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
    ]
    gmap = GameMap(16, 14, tiles, name="Shizugatake Mountain")
    gmap.seize_points   = [(6,0),(7,0)]
    gmap.village_points = [(6,10),(8,10)]
    gmap.fort_points    = [(4,1),(8,1),(6,3),(6,7)]
    return gmap


# ─── MAP 15: Komaki-Nagakute ──────────────────────────────────────────────────
def make_chapter15_map():
    tiles = [
        [M, M, F, F, P, P, P, P, P, P, P, P, F, F, M, M, M, M, M, M],
        [M, F, F, P, P, V, P, P, P, P, V, P, P, F, F, M, M, M, M, M],
        [F, F, P, P, P, P, P, P, P, P, P, P, P, P, F, F, M, M, M, M],
        [F, P, P, P, T, P, P, P, P, P, P, T, P, P, P, F, F, M, M, M],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F, M, M],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F, M],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F],
        [D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D, D],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, F, F, M],
        [F, P, P, P, T, P, P, P, P, P, P, T, P, P, P, P, F, F, M, M],
        [F, F, P, P, P, P, P, P, P, P, P, P, P, P, F, F, M, M, M, M],
        [M, F, F, P, P, V, P, P, P, P, V, P, P, F, F, M, M, M, M, M],
    ]
    gmap = GameMap(20, 13, tiles, name="Komaki-Nagakute Plains")
    gmap.seize_points   = [(10,6)]
    gmap.village_points = [(5,1),(10,1),(5,12),(10,12)]
    gmap.fort_points    = [(4,3),(11,3),(4,10),(11,10)]
    return gmap


# ─── MAP 16: Siege of Odawara Castle ─────────────────────────────────────────
def make_chapter16_map():
    # 20 columns x 18 rows
    # Odawara sits on a peninsula: sea (S) on east cols 14-19, mountains/peaks
    # on west cols 0-2, narrow land corridor approaching from south (rows 14-17)
    # THREE concentric rings:
    #   Outermost wall: row 12 / cols 3-13, gate at col 8 (S approach)
    #   Outer moat: row 11 (river tiles) bridged at cols 5 and 10
    #   Middle wall: row 8 / cols 3-13, gates at cols 6 and 10
    #   Inner moat: row 6 (river) bridged at col 8
    #   Inner keep: rows 1-4 / cols 4-12 — main tower at row 2
    # Town between outer and middle walls (rows 9-10)
    # Tokugawa/Hideyoshi siege position: forts at south rows 15-16
    tiles = [
        #0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        [M,  K,  K,  M,  C,  C,  C,  C,  C,  C,  C,  C,  M,  S,  S,  S,  S,  S,  S,  S],  # 0  keep pinnacle + sea N
        [M,  M,  K,  C,  C,  T,  D,  D,  C,  D,  D,  T,  C,  S,  S,  S,  S,  S,  S,  S],  # 1  inner keep top — towers
        [M,  M,  F,  C,  D,  P,  P,  C,  C,  C,  P,  P,  C,  S,  S,  S,  S,  S,  S,  S],  # 2  keep interior (seize)
        [M,  M,  F,  C,  D,  P,  T,  C,  C,  C,  T,  P,  C,  S,  S,  S,  S,  S,  S,  S],  # 3  inner ward — shrine
        [M,  F,  P,  C,  C,  C,  C,  C,  G,  C,  C,  C,  C,  S,  S,  S,  S,  S,  S,  S],  # 4  inner N wall + gate
        [M,  F,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  S,  S,  S,  S,  S,  S,  S],  # 5  inner bailey yard
        [M,  F,  P,  R,  R,  R,  R,  R,  B,  R,  R,  R,  R,  S,  S,  S,  S,  S,  S,  S],  # 6  inner moat (river) + bridge
        [M,  F,  P,  C,  C,  C,  C,  G,  D,  G,  C,  C,  C,  S,  S,  S,  S,  S,  S,  S],  # 7  middle wall N + twin gates
        [M,  P,  P,  C,  V,  D,  D,  P,  D,  P,  D,  D,  C,  S,  S,  S,  S,  S,  S,  S],  # 8  town N row — market
        [M,  P,  P,  C,  D,  V,  U,  P,  P,  P,  U,  V,  C,  S,  S,  S,  S,  S,  S,  S],  # 9  town center — ruins/shops
        [M,  P,  P,  C,  V,  D,  D,  P,  D,  P,  D,  D,  C,  S,  S,  S,  S,  S,  S,  S],  # 10 town S row — market
        [M,  F,  P,  C,  C,  C,  C,  G,  D,  G,  C,  C,  C,  S,  S,  S,  S,  S,  S,  S],  # 11 middle wall S + twin gates
        [M,  F,  P,  R,  R,  B,  R,  R,  R,  R,  B,  R,  R,  S,  S,  S,  S,  S,  S,  S],  # 12 outer moat + two bridges
        [M,  F,  P,  P,  C,  C,  C,  C,  C,  C,  C,  C,  P,  S,  S,  S,  S,  S,  S,  S],  # 13 outer wall
        [M,  M,  F,  P,  C,  G,  D,  D,  D,  D,  G,  C,  P,  P,  P,  S,  S,  S,  S,  S],  # 14 outer S wall + main gates
        [M,  M,  M,  F,  P,  P,  D,  T,  P,  T,  D,  P,  F,  P,  P,  P,  S,  S,  S,  S],  # 15 siege approach — Hideyoshi forts
        [M,  M,  M,  M,  F,  P,  D,  P,  P,  P,  D,  P,  P,  F,  P,  P,  P,  P,  S,  S],  # 16 southern forest road
        [M,  M,  M,  M,  M,  F,  F,  D,  F,  F,  D,  F,  F,  M,  P,  P,  P,  P,  S,  S],  # 17 S forest / entry
    ]
    gmap = GameMap(20, 18, tiles, name="Odawara Castle — The Grand Siege")
    gmap.seize_points   = [(7, 2), (8, 2), (9, 2)]          # inner keep / main tower
    gmap.gate_points    = [(8, 4), (7, 7), (9, 7), (7, 11), (9, 11), (5, 14), (10, 14)]
    gmap.fort_points    = [(5, 1), (11, 1), (6, 3), (10, 3), (7, 15), (9, 15)]
    gmap.village_points = [(4, 8), (12, 8), (5, 9), (11, 9), (4, 10), (12, 10)]
    return gmap


# ─── MAP 17: Defense of Fushimi Castle ───────────────────────────────────────
def make_chapter17_map():
    tiles = [
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
        [P, F, P, P, P, P, P, P, P, P, P, P, P, P, F, P, P, P],
        [P, P, P, P, C, C, C, C, C, C, C, C, P, P, P, P, P, P],
        [P, P, P, C, C, T, D, D, D, D, T, C, C, P, P, P, P, P],
        [P, P, C, C, T, P, P, P, P, P, P, T, C, C, P, P, P, P],
        [P, P, C, D, P, P, C, C, C, C, P, P, D, C, P, P, P, P],
        [P, P, C, D, P, C, C, T, D, T, C, C, P, C, P, P, P, P],
        [P, P, C, D, P, C, D, D, C, D, D, C, P, C, P, P, P, P],
        [P, P, C, D, P, C, C, T, D, T, C, C, P, C, P, P, P, P],
        [P, P, C, D, P, P, C, C, C, C, P, P, D, C, P, P, P, P],
        [P, P, C, C, T, P, P, P, P, P, P, T, C, C, P, P, P, P],
        [P, P, P, C, C, T, D, D, D, D, T, C, C, P, P, P, P, P],
        [P, F, P, P, C, C, C, C, C, C, C, C, P, P, F, P, P, P],
        [P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P, P],
    ]
    gmap = GameMap(18, 14, tiles, name="Fushimi Castle Defense")
    gmap.seize_points   = [(7,7),(8,7)]
    gmap.fort_points    = [(5,3),(10,3),(4,4),(11,4),(7,6),(9,6),(7,8),(9,8),(4,10),(11,10)]
    return gmap


# ─── MAP 18: Full Battle of Sekigahara ───────────────────────────────────────
def make_chapter18_map():
    # 24 columns x 16 rows
    # Twin mountain ranges: N ridge rows 0-1, S ridge rows 14-15
    # Valley floor rows 4-11; slopes rows 2-3 (N) and 12-13 (S)
    # Western Army (Ishida) deploys cols 0-6; Eastern Army (Tokugawa) cols 17-23
    # Nakasendo road runs the full width at row 7 (battle's central axis)
    # Two rivers run N-S: left river at col 7 (rows 2-6), right at col 16 (rows 2-6)
    # Bridges over left river: row 5 col 7; over right river: row 5 col 16
    # Kobayakawa's hill: SE quadrant cols 18-22 rows 10-13 — fort tiles on crest
    # Western pre-battle camp: NW col 1-2 rows 2-3 (fort tiles)
    # Eastern pre-battle camp: NE col 20-22 rows 2-3 (fort tiles)
    # Villages as mid-valley objective points; forests break line of sight
    tiles = [
        #0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23
        [M,  M,  M,  M,  M,  M,  F,  F,  F,  M,  M,  F,  F,  F,  M,  M,  M,  M,  M,  M,  M,  K,  K,  M],  # 0  N ridge
        [M,  M,  M,  F,  F,  F,  P,  P,  P,  P,  P,  P,  P,  F,  F,  F,  M,  M,  M,  M,  K,  K,  M,  M],  # 1  N upper slopes
        [M,  M,  F,  F,  T,  T,  P,  R,  P,  P,  P,  P,  R,  P,  T,  T,  F,  F,  M,  T,  T,  M,  M,  M],  # 2  W camp/E camp + twin rivers N
        [M,  F,  F,  P,  P,  P,  P,  R,  P,  V,  P,  P,  R,  P,  P,  P,  P,  F,  P,  P,  P,  F,  M,  M],  # 3  lower N slopes + villages
        [F,  F,  P,  P,  P,  P,  P,  B,  P,  P,  P,  P,  B,  P,  P,  P,  P,  P,  P,  P,  P,  P,  F,  M],  # 4  bridges over both rivers
        [F,  P,  P,  P,  P,  V,  P,  P,  F,  P,  P,  F,  P,  P,  V,  P,  P,  P,  P,  P,  P,  P,  P,  F],  # 5  open valley + forest patches
        [P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 6  open valley
        [D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D,  D],  # 7  Nakasendo road — full width
        [P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 8  open valley
        [F,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  F],  # 9  open valley — forest flanks
        [F,  P,  P,  P,  P,  V,  P,  P,  F,  P,  P,  F,  P,  P,  V,  P,  P,  P,  F,  F,  T,  T,  P,  P],  # 10 valley villages + Kobayakawa base
        [F,  F,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  F,  M,  T,  T,  T,  F,  M],  # 11 S valley + Kobayakawa hill mid
        [M,  F,  F,  P,  P,  P,  P,  P,  B,  P,  P,  P,  P,  P,  P,  P,  F,  F,  M,  F,  T,  T,  M,  M],  # 12 S valley bridge + Kobayakawa crest
        [M,  M,  F,  F,  P,  P,  V,  P,  R,  R,  P,  V,  P,  P,  P,  F,  F,  M,  M,  M,  F,  M,  M,  M],  # 13 S river + lower S slopes
        [M,  M,  M,  F,  F,  F,  P,  F,  F,  F,  F,  F,  F,  F,  F,  F,  M,  M,  M,  M,  M,  M,  M,  M],  # 14 S upper slopes
        [M,  M,  M,  M,  M,  M,  F,  F,  F,  M,  M,  F,  F,  F,  M,  M,  M,  M,  M,  M,  M,  M,  M,  M],  # 15 S ridge
    ]
    gmap = GameMap(24, 16, tiles, name="Sekigahara — The Decisive Battle")
    gmap.seize_points   = [(11, 7), (12, 7)]             # Nakasendo center / battle pivot
    gmap.village_points = [(9, 3), (5, 5), (14, 5), (5, 10), (14, 10), (6, 13), (11, 13)]
    gmap.fort_points    = [(4, 2), (5, 2), (13, 2), (14, 2), (19, 2), (20, 2),
                           (20, 10), (21, 10), (19, 11), (20, 11), (21, 11), (20, 12), (21, 12)]
    return gmap


# ─── MAP 19: Siege of Osaka Castle (Winter) ──────────────────────────────────
def make_chapter19_map():
    # 22 columns x 20 rows
    # Osaka Castle — the largest and most heavily moated fortress in Japan
    # THREE concentric moat rings (river tiles) around the central keep
    #   Outer moat: rows 3/16, cols 3-18 (bridged N col 10, S col 10)
    #   Middle moat: rows 6/13, cols 5-16 (bridged N col 10, S col 10)
    #   Inner moat:  rows 8/11, cols 7-14 (bridged at col 10)
    #   Keep (innermost): rows 9-10, cols 8-13
    # Outer wall (castle tiles) just inside outer moat, with gates
    # Tokugawa siege positions: fort tiles surrounding outer moat
    # Sanada Maru: protruding defensive outwork at S face (rows 14-16, cols 8-13)
    # Sea/river flanks: west col 0-1 (river), east col 20-21 (sea)
    tiles = [
        #0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21
        [P,  P,  T,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  T,  P,  P,  P],  # 0  Tokugawa N siege line
        [P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 1  N approach
        [P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 2  N approach
        [P,  P,  P,  R,  R,  R,  R,  R,  R,  R,  B,  R,  R,  R,  R,  R,  R,  R,  R,  P,  P,  P],  # 3  outer moat N
        [P,  P,  P,  R,  C,  C,  C,  C,  C,  G,  D,  G,  C,  C,  C,  C,  C,  C,  R,  P,  P,  P],  # 4  outer wall N + gates
        [P,  P,  P,  R,  C,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  C,  R,  P,  P,  P],  # 5  outer bailey
        [P,  P,  P,  R,  C,  P,  R,  R,  R,  R,  B,  R,  R,  R,  R,  R,  P,  C,  R,  P,  P,  P],  # 6  middle moat N
        [P,  P,  P,  R,  C,  P,  R,  C,  C,  G,  D,  G,  C,  C,  R,  P,  P,  C,  R,  P,  P,  P],  # 7  middle wall N + gates
        [P,  P,  P,  R,  C,  P,  R,  C,  R,  R,  B,  R,  R,  C,  R,  P,  P,  C,  R,  P,  P,  P],  # 8  inner moat N
        [P,  P,  P,  R,  C,  P,  R,  C,  C,  T,  C,  T,  C,  C,  R,  P,  P,  C,  R,  P,  P,  P],  # 9  keep N face — towers
        [P,  P,  P,  R,  C,  P,  R,  C,  D,  D,  C,  D,  D,  C,  R,  P,  P,  C,  R,  P,  P,  P],  # 10 keep — main hall (seize)
        [P,  P,  P,  R,  C,  P,  R,  C,  C,  T,  C,  T,  C,  C,  R,  P,  P,  C,  R,  P,  P,  P],  # 11 keep S face — towers
        [P,  P,  P,  R,  C,  P,  R,  C,  R,  R,  B,  R,  R,  C,  R,  P,  P,  C,  R,  P,  P,  P],  # 12 inner moat S
        [P,  P,  P,  R,  C,  P,  R,  C,  C,  G,  D,  G,  C,  C,  R,  P,  P,  C,  R,  P,  P,  P],  # 13 middle wall S + gates
        [P,  P,  P,  R,  C,  P,  R,  R,  T,  T,  T,  T,  T,  R,  R,  R,  P,  C,  R,  P,  P,  P],  # 14 Sanada Maru — N face (fort)
        [P,  P,  P,  R,  C,  P,  T,  T,  T,  D,  D,  D,  T,  T,  T,  P,  P,  C,  R,  P,  P,  P],  # 15 Sanada Maru — body
        [P,  P,  P,  R,  C,  C,  C,  G,  D,  D,  D,  D,  G,  C,  C,  C,  C,  C,  R,  P,  P,  P],  # 16 outer wall S + Sanada exit gate
        [P,  P,  P,  R,  R,  R,  R,  R,  R,  R,  B,  R,  R,  R,  R,  R,  R,  R,  R,  P,  P,  P],  # 17 outer moat S
        [P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 18 S approach
        [P,  P,  T,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  T,  P,  P,  P],  # 19 Tokugawa S siege line
    ]
    gmap = GameMap(22, 20, tiles, name="Osaka Castle — Winter Siege")
    gmap.seize_points   = [(9, 10), (10, 10), (11, 10)]          # main keep hall
    gmap.gate_points    = [(9, 4), (11, 4), (9, 7), (11, 7), (9, 13), (11, 13), (7, 16), (12, 16)]
    gmap.fort_points    = [(9, 9), (11, 9), (9, 11), (11, 11),   # keep towers
                           (7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (12, 14), (13, 14),  # Sanada Maru N
                           (6, 15), (7, 15), (12, 15), (13, 15),  # Sanada Maru flanks
                           (2, 0), (18, 0), (2, 19), (18, 19)]    # Tokugawa siege camps
    gmap.village_points = []
    return gmap


# ─── MAP 20: Osaka Summer Campaign (Final) ───────────────────────────────────
def make_chapter20_map():
    # 24 columns x 18 rows
    # Osaka Castle is burning — NW quadrant is castle ruins (ruins+castle mix)
    # The open Namba/Tennoji plains spread south and east of the castle
    # Toyotomi loyalists break out in multiple columns heading SE
    # Tokugawa blocking forces hold the SE corner (fort tiles)
    # Villages scattered (civilian protection objectives)
    # Escape route: SE corner (seize = reach col 20-23, row 15-17)
    # River cuts through mid-map adding chokepoints
    # Castle: cols 0-8, rows 0-8 (partially burned, partially intact)
    # Burning sections (ruins): cols 2-7, rows 2-7 inner
    # Castle walls still standing: outer ring (castle tiles)
    # Plains: cols 8-23, rows 4-17
    # SE fort complex (Tokugawa final line): cols 18-22, rows 12-16
    tiles = [
        #0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23
        [C,  C,  C,  C,  C,  C,  C,  C,  C,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 0  castle N wall (intact)
        [C,  C,  U,  U,  U,  U,  U,  C,  C,  P,  V,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 1  burning outer ward
        [C,  U,  U,  U,  U,  U,  U,  U,  C,  P,  P,  P,  P,  V,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 2  burning inner ward
        [C,  U,  U,  C,  T,  C,  U,  U,  C,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 3  keep — one tower still stands
        [C,  U,  U,  C,  D,  C,  U,  U,  G,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 4  last gate (seize inner)
        [C,  U,  U,  U,  U,  U,  U,  U,  C,  F,  F,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 5  burning ward + forest cover
        [C,  C,  U,  U,  U,  U,  U,  C,  C,  P,  F,  F,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 6  S castle outer wall
        [C,  C,  C,  C,  C,  C,  C,  C,  G,  P,  P,  F,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 7  S wall + breakout gate
        [P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 8  open plains begin
        [P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  V,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 9  plains + village
        [R,  R,  R,  R,  R,  R,  B,  R,  R,  R,  R,  R,  R,  B,  R,  R,  R,  R,  R,  R,  R,  R,  P,  P],  # 10 river crossing (two bridges)
        [P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P],  # 11 plains S of river
        [P,  P,  P,  P,  P,  P,  P,  P,  P,  V,  P,  P,  P,  P,  P,  P,  P,  P,  T,  T,  P,  P,  P,  P],  # 12 plains + village + Tokugawa fort
        [P,  P,  P,  P,  P,  P,  P,  F,  F,  P,  P,  P,  P,  P,  P,  P,  P,  P,  T,  T,  T,  P,  P,  P],  # 13 forest + Tokugawa line
        [P,  P,  P,  P,  P,  F,  F,  F,  P,  P,  P,  P,  V,  P,  P,  P,  P,  P,  P,  T,  T,  T,  P,  P],  # 14 forest flank + village + SE fort
        [P,  P,  P,  P,  P,  P,  F,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  T,  T,  P,  P],  # 15 S plains + SE fort line
        [P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  D,  D,  D],  # 16 escape road — SE corner
        [P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  P,  D,  D,  D],  # 17 escape road — SE corner
    ]
    gmap = GameMap(24, 18, tiles, name="Osaka — The Burning Summer")
    gmap.seize_points   = [(4, 4), (21, 16), (22, 16), (23, 16)]  # last keep OR escape route
    gmap.fort_points    = [(4, 3),                                  # last standing tower
                           (18, 12), (19, 12),                     # Tokugawa fort N line
                           (18, 13), (19, 13), (20, 13),
                           (19, 14), (20, 14), (21, 14),
                           (20, 15), (21, 15)]
    gmap.village_points = [(10, 1), (13, 2), (11, 9), (9, 12), (12, 14)]
    gmap.gate_points    = [(8, 4), (8, 7)]
    return gmap


# ─── Registry ─────────────────────────────────────────────────────────────────
MAP_BUILDERS = {
    1:  make_chapter1_map,
    2:  make_chapter2_map,
    3:  make_chapter3_map,
    4:  make_chapter4_map,
    5:  make_chapter5_map,
    6:  make_chapter6_map,
    7:  make_chapter7_map,
    8:  make_chapter8_map,
    9:  make_chapter9_map,
    10: make_chapter10_map,
    11: make_chapter11_map,
    12: make_chapter12_map,
    13: make_chapter13_map,
    14: make_chapter14_map,
    15: make_chapter15_map,
    16: make_chapter16_map,
    17: make_chapter17_map,
    18: make_chapter18_map,
    19: make_chapter19_map,
    20: make_chapter20_map,
}
