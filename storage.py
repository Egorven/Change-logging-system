"""Загрузка, сохранение и экспорт данных приложения."""

import json
from pathlib import Path
from typing import Any


def _load(filename: str | Path) -> list[dict[str, Any]]:
    """Загрузить список словарей из JSON-файла."""
    path = Path(filename)
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return []
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"Некорректный JSON в файле {path}") from error
    if not isinstance(data, list):
        raise ValueError(f"Файл {path} должен содержать список")
    return data


def _save(filename: str | Path, data: list[dict[str, Any]]) -> None:
    """Сохранить список словарей в JSON-файл."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def to_json(project: dict[str, Any], versions: list[dict[str, Any]],
            changes: list[dict[str, Any]]) -> str:
    """Сформировать JSON-блок проекта, его версий и изменений."""
    data = {
        "project": project,
        "versions": versions,
        "changes": changes,
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def load_projects(filename: str | Path) -> list[dict[str, Any]]:
    """Загрузить проекты из JSON-файла."""
    return _load(filename)


def save_projects(filename: str | Path,
                  projects: list[dict[str, Any]]) -> None:
    """Сохранить проекты в JSON-файл."""
    _save(filename, projects)


def load_versions(filename: str | Path) -> list[dict[str, Any]]:
    """Загрузить версии из JSON-файла."""
    return _load(filename)


def save_versions(filename: str | Path,
                  versions: list[dict[str, Any]]) -> None:
    """Сохранить версии в JSON-файл."""
    _save(filename, versions)


def load_changes(filename: str | Path) -> list[dict[str, Any]]:
    """Загрузить изменения из JSON-файла."""
    return _load(filename)


def save_changes(filename: str | Path,
                 changes: list[dict[str, Any]]) -> None:
    """Сохранить изменения в JSON-файл."""
    _save(filename, changes)


def load_developers(filename: str | Path) -> list[dict[str, Any]]:
    """Загрузить разработчиков из JSON-файла."""
    return _load(filename)


def save_developers(filename: str | Path,
                    developers: list[dict[str, Any]]) -> None:
    """Сохранить разработчиков в JSON-файл."""
    _save(filename, developers)
