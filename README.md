# RPLAN Living Analyzer

## living_analyzer.py
座標リストで与えられるリビングから、ドアや窓を削除し、家具配置に有効な壁のみを抽出できる

## Usage
```
python feature_extraction_with_json_dir.py
```

出力先を変えたいときは、ファイル内のグローバル変数を変える
```python
JSON_DIR = "../json_parser/rich_json"
RES_DIR = "./res"
```

## Option
1. 廊下の判定の閾値を変更したいときは、`libs.living_analyzer.py`の`remove_closing_walls(walls_ls, meat_width=0.78)`関数の`meat_width`を変更する（デフォルトでは78cm）
1. 家具配置に有効な壁長さの閾値を変えたいときは、`libs.living_analyzer.py`の`calculate_effective_walls(walls, effective_length=3.0)`関数の`effective_length`を変更する（デフォルトでは3.0m）
