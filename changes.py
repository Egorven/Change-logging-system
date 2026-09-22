"""Операции с записями журнала изменений."""

from collections import Counter
from typing import Any


def add_change(changes: list[dict[str, Any]], change_type: str,
               description: str, author: str, change_date: str,
               project_id: int | None = None,
               version_id: int | None = None,
               developer_id: int | None = None) -> dict[str, Any]:
    """Добавить запись об изменении и вернуть ее."""
    change = {
        "id": max((item["id"] for item in changes), default=0) + 1,
        "type": change_type,
        "description": description,
        "author": author,
        "date": change_date,
    }
    if project_id is not None:
        change["project_id"] = project_id
    if version_id is not None:
        change["version_id"] = version_id
    if developer_id is not None:
        change["developer_id"] = developer_id
    changes.append(change)
    return change


def format_entry(change: dict[str, Any]) -> str:
    """Сформировать человекочитаемую запись об изменении."""
    labels = {
        "added": "Добавлено",
        "fixed": "Исправлено",
        "removed": "Удалено",
    }
    label = labels.get(change["type"], "Изменено")
    return (
        f"[{label}] {change['description']} "
        f"(автор: {change['author']})"
    )


def filter_by_type(changes: list[dict[str, Any]],
                   target_type: str) -> list[dict[str, Any]]:
    """Отфильтровать изменения по категории."""
    return [item for item in changes if item["type"] == target_type]


def sort_changes(changes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Вернуть изменения, отсортированные от новых к старым."""
    return sorted(changes, key=lambda item: item["date"], reverse=True)


def get_statistics(changes: list[dict[str, Any]]) -> dict[str, int]:
    """Подсчитать количество изменений каждого типа."""
    return dict(Counter(item["type"] for item in changes))
