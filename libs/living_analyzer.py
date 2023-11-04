from shapely.geometry import LineString, MultiLineString
from shapely.ops import unary_union

def subtract_elements(base_elements, subtract_elements):
    result = []
    for base in base_elements:
        current_base = base
        for sub in subtract_elements:
            current_base = current_base.difference(sub)
            if current_base.is_empty:
                break

        # 結果が MultiLineString ならば、個々の LineString に分ける
        if isinstance(current_base, MultiLineString):
            for line in current_base.geoms:
                result.append(line)
        elif not current_base.is_empty:
            result.append(current_base)

    return result

def combine_geometries(geoms):
    return unary_union(geoms)

from shapely.geometry import LineString, Polygon

"""互いに近い距離にある平行関係にある壁を両方削除する"""

def remove_closing_walls(walls_ls, meat_width=0.78*255/18):
    horizontal_walls = []
    vertical_walls = []
    horizontal_polygons = []
    vertical_polygons = []
    
    # Step 1: 水平か垂直かを判定してリストを作成
    for wall in walls_ls:
        if is_horizontal(wall):
            horizontal_walls.append(wall)
            horizontal_polygons.append(buffering(wall, meat_width))
        elif is_vertical(wall):
            vertical_walls.append(wall)
            vertical_polygons.append(buffering(wall, meat_width))

    # Step 2: 水平ポリゴンの重なりを検出して削除
    for i, hpoly in enumerate(horizontal_polygons):
        for j, other_hpoly in enumerate(horizontal_polygons):
            if i != j and hpoly.intersects(other_hpoly):  # 自分自身を除外しない
                horizontal_walls[i] = None  # 重なりがある場合はNoneに置き換え
                break  # 一つでも重なりが見つかれば、その壁は処理から除外

    # Step 3: 垂直ポリゴンの重なりを検出して削除
    for i, vpoly in enumerate(vertical_polygons):
        for j, other_vpoly in enumerate(vertical_polygons):
            if i != j and vpoly.intersects(other_vpoly):  # 自分自身を除外しない
                vertical_walls[i] = None  # 重なりがある場合はNoneに置き換え
                break  # 一つでも重なりが見つかれば、その壁は処理から除外
    
    # Step 4: Noneに置き換えられた壁を削除
    filtered_walls_ls = [wall for wall in horizontal_walls + vertical_walls if wall is not None]

    return filtered_walls_ls, horizontal_polygons+vertical_polygons

def is_horizontal(line):
    return line.coords[0][1] == line.coords[1][1]

def is_vertical(line):
    return line.coords[0][0] == line.coords[1][0]

def buffering(linestring, buffer_width, delta=1):
    # linestringの始点と終点の座標を取得
    start_x, start_y = linestring.coords[0]
    end_x, end_y = linestring.coords[1]

    # 垂直か水平かを判断
    if start_x == end_x:  # 垂直な線

        if start_y < end_y:
            start_y += delta
            end_y -= delta
        else:
            start_y -= delta
            end_y += delta
        # X軸に平行な方向にバッファリング
        buffered_coords = [
            (start_x - buffer_width, start_y),
            (start_x + buffer_width, start_y),
            (end_x + buffer_width, end_y),
            (end_x - buffer_width, end_y)
        ]
    elif start_y == end_y:  # 水平な線

        if start_x < end_x:
            start_x += delta
            end_x -= delta
        else:
            start_x -= delta
            end_x += delta
        # Y軸に平行な方向にバッファリング
        buffered_coords = [
            (start_x, start_y - buffer_width),
            (end_x, end_y - buffer_width),
            (end_x, end_y + buffer_width),
            (start_x, start_y + buffer_width)
        ]
    else:
        raise ValueError("LineStringは水平または垂直でなければなりません。")

    # バッファリングされた座標からポリゴンを生成して返す
    return Polygon(buffered_coords)

def calculate_effective_walls(walls, px2m=18/255):
    effective_wall_count = 0
    total_effective_length = 0.0
    effective_walls = []

    for wall in walls:
        try:
            wall.length
        except AttributeError:
            wall = wall[0]
        # 壁の長さを計算
        length = wall.length * px2m
        # 3メートルを超える場合は有効な壁としてカウント
        if length > 3.0:
            effective_wall_count += 1
            total_effective_length += length
            effective_walls.append(wall)

    return effective_wall_count, total_effective_length, effective_walls
