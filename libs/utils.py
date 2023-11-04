# 座標のリストを受け取り、連続する点を結んでLineStringオブジェクトのリストを作成
def create_linestrings(coord_pairs):
    linestrings = []
    for i in range(len(coord_pairs)):
        start_point = coord_pairs[i]
        # リストの最後の点を最初の点に繋ぐために % を使う
        end_point = coord_pairs[(i + 1) % len(coord_pairs)]
        linestrings.append(LineString([start_point, end_point]))
    return linestrings
