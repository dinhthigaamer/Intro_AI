from pathlib import Path

current_file = Path(__file__).resolve()
current_dir = current_file.parent

MAP_DIR = current_dir.parent.parent / "map_data"
