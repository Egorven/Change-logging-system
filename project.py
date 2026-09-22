"""Операции с проектами."""

from typing import Any


def add_project(projects: list[dict[str, Any]], name: str,
                description: str = "") -> dict[str, Any]:
    """Добавить проект и вернуть созданную запись."""
    project = {
        "id": max((item["id"] for item in projects), default=0) + 1,
        "name": name,
        "description": description,
    }
    projects.append(project)
    return project


def delete_project(projects: list[dict[str, Any]], project_id: int) -> bool:
    """Удалить проект по идентификатору."""
    for item in projects:
        if item["id"] == project_id:
            projects.remove(item)
            return True
    return False
