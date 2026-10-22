"""Импорт существующих JSON-данных в SQLite."""

import json
from pathlib import Path
from typing import Any

from db.database import get_connection, initialize_database


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def _read_json(filename: str) -> list[dict[str, Any]]:
    with (DATA_DIR / filename).open(encoding="utf-8") as data_file:
        data = json.load(data_file)
    if not isinstance(data, list):
        raise ValueError(f"Файл {filename} должен содержать список")
    return data


def import_json_data() -> None:
    """Перенести все записи из JSON, заменив данные импортируемых таблиц."""
    projects = _read_json("project.json")
    developers = _read_json("developer.json")
    versions = _read_json("version.json")
    changes = _read_json("changes.json")

    initialize_database()
    with get_connection() as connection:
        connection.execute("DELETE FROM changes")
        connection.execute("DELETE FROM versions")
        connection.execute("DELETE FROM developers")
        connection.execute("DELETE FROM projects")
        connection.executemany(
            "INSERT INTO projects (id, name, description) VALUES (?, ?, ?)",
            [
                (item["id"], item["name"], item.get("description", ""))
                for item in projects
            ],
        )
        connection.executemany(
            "INSERT INTO developers (id, name, role) VALUES (?, ?, ?)",
            [
                (item["id"], item["name"], item.get("role", ""))
                for item in developers
            ],
        )
        connection.executemany(
            """INSERT INTO versions (id, name, release_date, project_id)
               VALUES (?, ?, ?, ?)""",
            [
                (
                    item["id"],
                    item["name"],
                    item["release_date"],
                    item.get("project_id"),
                )
                for item in versions
            ],
        )
        connection.executemany(
            """INSERT INTO changes
               (id, type, description, author, change_date,
                project_id, version_id, developer_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    item["id"],
                    item["type"],
                    item["description"],
                    item["author"],
                    item["date"],
                    item.get("project_id"),
                    item.get("version_id"),
                    item.get("developer_id"),
                )
                for item in changes
            ],
        )
        connection.commit()


if __name__ == "__main__":
    import_json_data()
