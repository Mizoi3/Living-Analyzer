#!/usr/bin/env python3

import json
import os
from shapely.geometry import LineString
from lib.utils import create_linestrings
from lib.living_analyzer import subtract_elements, remove_closing_walls, calculate_effective_walls

JSON_DIR = "/path/to/json/directory"  # 実際のJSONファイルがあるディレクトリへのパスに置き換えてね

def process_json_file(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    walls = data['room_polygons_seq']
    adjacency = data['adjacency']
    windows = data['windows']

    # 壁、ドア、窓のLineStringを作成
    walls_ls = create_linestrings(walls)
    doors_ls = [LineString([(entry[3], entry[4]), (entry[3] + entry[5], entry[4] + entry[6])]) for entry in adjacency if entry[2] == 1]
    windows_ls = [LineString([(w[1], w[2]), (w[1] + w[3], w[2] + w[4])]) for w in windows]

    # 処理の実行
    walls_minus_doors_ls = subtract_elements(walls_ls, doors_ls)
    walls_doors_windows_ls = subtract_elements(walls_minus_doors_ls, windows_ls)
    # draw.draw_linestrings(walls_doors_windows_ls)

    true_walls_ls, _ = remove_closing_walls(walls_doors_windows_ls)
    # draw.draw_linestrings(true_walls_ls)

    _, _, effective_walls_ls = calculate_effective_walls(true_walls_ls)
    # draw.draw_linestrings(true_walls_ls, effective_walls_ls)

    return effective_walls_ls

def main():
    for json_file in os.listdir(JSON_DIR):
        if json_file.endswith('.json'):
            effective_walls_ls = process_json_file(os.path.join(JSON_DIR, json_file))
            print(json_file, effective_walls_ls)

if __name__ == "__main__":
    main()
