import json
from pathlib import Path


def load_json(filename: Path) -> list[dict]:
    """Прочитать записи; при ошибке сообщить её вызывающему коду."""
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError(f"В файле {filename.name} ожидается список")
    if not all(isinstance(item, dict) for item in data):
        raise ValueError(f"В файле {filename.name} ожидаются словари")
    return data


def save_json(filename: Path, data: list[dict]) -> None:
    """Сохранить записи; ошибка записи не считается успехом."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")
