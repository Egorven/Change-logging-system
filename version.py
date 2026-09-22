"""Операции с версиями проектов."""

from typing import Any


def add_version(versions: list[dict[str, Any]], project_id: int,
                version_name: str, release_date: str) -> dict[str, Any]:
    """Добавить версию проекта и вернуть созданную запись."""
    version = {
        "id": max((item["id"] for item in versions), default=0) + 1,
        "project_id": project_id,
        "name": version_name,
        "release_date": release_date,
    }
    versions.append(version)
    return version


def sort_versions(versions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Вернуть версии, отсортированные по дате выпуска."""
    return sorted(versions, key=lambda item: item["release_date"])
