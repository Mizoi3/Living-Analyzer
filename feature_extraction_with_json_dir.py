#!/usr/bin/env python3

import json
import os
import sys
import csv

from shapely.geometry import LineString, Polygon, mapping

from libs.utils import create_linestrings
from libs.living_analyzer import subtract_elements, remove_closing_walls, calculate_effective_walls
import libs.drawing_functions as draw
sys.path.append('../')
import config

JSON_DIR = "../json_parser/rich_json"  # 実際のJSONファイルがあるディレクトリへのパスに置き換えてね
RES_DIR = "./res"

def main():
    for json_file in os.listdir(JSON_DIR):
        if json_file.endswith('.json'):
            json_file_path = os.path.join(JSON_DIR, json_file)
            line_pairs = process_json_file(json_file_path)
            formatted_linestrings = [
                [list(line.coords[0]), list(line.coords[1])] for line in line_pairs
            ]
            write_linestrings_to_csv(json_file, formatted_linestrings, RES_DIR)

def process_json_file(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    polygons = data['room_polygon_seq']
    types = [config.category[type_] for type_ in data['types']]
    livings = [polygon for i, polygon in enumerate(polygons) if types[i] == 'Living Room']

    if len(livings) > 1:
        max_area = 0
        walls = None
        for living in livings:
            polygon = Polygon(living)
            area = polygon.area
            if area > max_area:
                max_area = area
                walls = living

    else:
        walls = livings[0]

    adjacency = data['room_adjacency_seq']
    windows = data['windows']

    # 壁、ドア、窓のLineStringを作成
    walls_ls = create_linestrings(walls)
    doors_ls = [LineString([(entry[3], entry[4]), (entry[3] + entry[5], entry[4] + entry[6])]) for entry in adjacency if entry[2] == 1]
    windows_ls = [LineString([(w[1], w[2]), (w[1] + w[3], w[2] + w[4])]) for w in windows]

    # 処理の実行
    walls_minus_doors_ls = subtract_elements(walls_ls, doors_ls)
    walls_doors_windows_ls = subtract_elements(walls_minus_doors_ls, windows_ls)

    true_walls_ls, _ = remove_closing_walls(walls_doors_windows_ls)

    _, _, effective_walls_ls = calculate_effective_walls(true_walls_ls)
    # draw.linestrings(true_walls_ls, effective_walls_ls)

    return effective_walls_ls

def write_linestrings_to_csv(json_filename, line_pairs, res_dir):
    # 結果をCSVファイルに書き込む
    csv_filename = os.path.join(res_dir, 'effective_walls.csv')
    
    # フォルダが存在しない場合は作成する
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    # CSVファイルが既に存在するかをチェックし、ヘッダを追加するかを決める
    file_exists = os.path.isfile(csv_filename)

    with open(csv_filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['File Name', 'LineStrings'])  # ヘッダーの書き込み
        
        # LineStringsを書き込む
        writer.writerow([json_filename, line_pairs])

if __name__ == "__main__":
    main()
