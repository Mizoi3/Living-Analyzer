from shapely.geometry import LineString, Point
import numpy as np
import matplotlib.pyplot as plt

import lib.utils as utils
import lib.drawing_functions as draw
import lib.living_analyzer as living

# ポリゴンの頂点
walls = [[165.0, 87.0], [165.0, 28.0], [148.0, 28.0], [148.0, 87.0],
        [125.0, 87.0], [125.0, 128.5], [108.0, 128.5], [108.0, 159.5],
        [128.0, 159.5], [128.0, 207.0], [185.0, 207.0], [185.0, 87.0]]

# pxとmの対応関係
px_to_m = 18 / 255

# 壁と障害物（ドア、窓）のデータ
adjacency = [
    [0, 1, 2, None, None, None, None], [0, 2, 2, None, None, None, None],
    [0, 5, 2, None, None, None, None], [1, 2, 2, None, None, None, None],
    [1, 3, 2, None, None, None, None], [2, 3, 2, None, None, None, None],
    [2, 4, 2, None, None, None, None], [2, 5, 2, None, None, None, None],
    [3, 4, 2, None, None, None, None], [0, 2, 1, 114.0, 159.0, 12, 0],
    [1, 2, 1, 108.0, 134.0, 0, 12], [2, 3, 1, 125.0, 93.0, 0, 12],
    [2, 4, 1, 148.0, 59.0, 0, 12], [2, 5, 1, 156.0, 207.0, 42, 0]
]

windows = [
    [0, 72, 181, 0, 18, 0], [1, 72, 139, 0, 10, 0], [2, 165, 61, 0, 18, 2],
    [2, 185, 135, 0, 24, 2], [3, 84, 87, 18, 0, 1], [4, 115, 61, 0, 18, 0],
    [5, 133, 229, 45, 0, 3], [5, 185, 209, 0, 17, 2]
]

# 壁のLineStringを作成
walls_ls = utils.create_linestrings(walls)

# ドアのLineStringを作成
doors_ls = [LineString([(entry[3], entry[4]), (entry[3] + entry[5], entry[4] + entry[6])]) for entry in adjacency if entry[2] == 1]

# 窓のLineStringを作成
windows_ls = [LineString([(w[1], w[2]), (w[1] + w[3], w[2] + w[4])]) for w in windows]

# Step1: 引き算により、ドアと窓を削除
walls_minus_doors_ls = living.subtract_elements(walls_ls, doors_ls)
walls_doors_windows_ls = living.subtract_elements(walls_minus_doors_ls, windows_ls)
draw.draw_linestrings(walls_doors_windows_ls)

# Step2: 廊下判定の壁を削除
true_walls_ls, p = living.remove_closing_walls(walls_doors_windows_ls)
draw.draw_linestrings(true_walls_ls)

# Step3: 3m以上の長さの壁を抽出
_, _, effective_walls_ls = living.calculate_effective_walls(true_walls_ls)
draw.draw_linestrings(true_walls_ls, effective_walls_ls)
