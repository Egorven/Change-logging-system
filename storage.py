"""Загрузка, сохранение и экспорт данных приложения."""

import json
from pathlib import Path
from typing import Any

from models import Change, Developer, Project, Version


def _load_raw(filename: str | Path) -> list[dict[str, Any]]:
    """Загрузить сырые данные из JSON-файла."""
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


def _save_raw(filename: str | Path, data: list[dict[str, Any]]) -> None:
    """Сохранить сырые данные в JSON-файл."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


# === Projects ===
def load_projects(filename: str | Path) -> list[Project]:
    """Загрузить проекты из JSON-файла."""
    return [
        Project(p["id"], p["name"], p.get("description", ""))
        for p in _load_raw(filename)
    ]


def save_projects(filename: str | Path, projects: list[Project]) -> None:
    data = [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description} for p in projects
    ]
    _save_raw(filename, data)


# === Developers ===
def load_developers(filename: str | Path) -> list[Developer]:
    """Загрузить разработчиков из JSON-файла."""
    return [Developer.from_data(d) for d in _load_raw(filename)]


def save_developers(filename: str | Path, developers: list[Developer]) -> None:
    """Сохранить разработчиков в JSON-файл."""
    data = [{"id": d.id, "name": d.name, "role": d.role} for d in developers]
    _save_raw(filename, data)


# === Versions ===
def load_versions(
        filename: str | Path,
        projects: list[Project]) -> list[Version]:
    """Загрузить версии из JSON-файла, связывая с проектами."""
    project_map = {p.id: p for p in projects}
    versions = []
    for v in _load_raw(filename):
        project = project_map.get(v.get("project_id"))
        versions.append(Version(
            v["id"],
            v["name"],
            v["release_date"],
            project))
    return versions


def save_versions(filename: str | Path, versions: list[Version]) -> None:
    """Сохранить версии в JSON-файл."""
    data = [
        {
            "id": v.id,
            "name": v.name,
            "release_date": v.release_date,
            "project_id": v.project.id if v.project else None,
        }
        for v in versions
    ]
    _save_raw(filename, data)


# === Changes ===
def load_changes(
    filename: str | Path,
    projects: list[Project],
    versions: list[Version],
    developers: list[Developer],
) -> list[Change]:
    """Загрузить изменения, связывая с объектами."""
    project_map = {p.id: p for p in projects}
    version_map = {v.id: v for v in versions}
    developer_map = {d.id: d for d in developers}
    changes = []
    for c in _load_raw(filename):
        changes.append(
            Change(
                change_id=c["id"],
                change_type=c["type"],
                description=c["description"],
                author=c["author"],
                date=c["date"],
                project=project_map.get(c.get("project_id")),
                version=version_map.get(c.get("version_id")),
                developer=developer_map.get(c.get("developer_id")),
            )
        )
    return changes


def save_changes(filename: str | Path, changes: list[Change]) -> None:
    """Сохранить изменения в JSON-файл."""
    data = [
        {
            "id": c.id,
            "type": c.type,
            "description": c.description,
            "author": c.author,
            "date": c.date,
            "project_id": c.project.id if c.project else None,
            "version_id": c.version.id if c.version else None,
            "developer_id": c.developer.id if c.developer else None,
        }
        for c in changes
    ]
    _save_raw(filename, data)


def to_json(
    project: Project,
    versions: list[Version],
    changes: list[Change],
) -> str:
    """Сформировать JSON-блок проекта, его версий и изменений."""
    data = {
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
        },
        "versions": [
            {"id": v.id, "name": v.name, "release_date": v.release_date}
            for v in versions
        ],
        "changes": [
            {
                "id": c.id,
                "type": c.type,
                "description": c.description,
                "author": c.author,
                "date": c.date,
            }
            for c in changes
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)
