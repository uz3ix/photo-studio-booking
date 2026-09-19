"""Проверки JSON на временных файлах pytest."""

import json

import pytest

from module.storage import load_json, save_json


def test_load_json(tmp_path):
    path = tmp_path / "studios.json"
    path.write_text('[{"name": "Свет"}]', encoding="utf-8")
    assert load_json(path) == [{"name": "Свет"}]


def test_load_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_json(tmp_path / "missing.json")


@pytest.mark.parametrize("content", ["{broken", "{}", "[1]"])
def test_load_invalid_data(tmp_path, content):
    path = tmp_path / "invalid.json"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError):
        load_json(path)
    assert path.read_text(encoding="utf-8") == content


def test_save_json(tmp_path):
    path = tmp_path / "studios.json"
    path.write_text("old content", encoding="utf-8")
    data = [{"id": 1, "name": "Свет"}]
    save_json(path, data)
    assert json.loads(path.read_text(encoding="utf-8")) == data


def test_save_failure(tmp_path):
    with pytest.raises(OSError):
        save_json(tmp_path / "missing" / "data.json", [])
