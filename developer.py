"""Операции с разработчиками."""

from typing import Any

def add_developer(developers: list[dict[str, Any]], name: str,
                  role: str = "") -> dict[str, Any]:
    """Добавить разработчика и вернуть созданную запись."""
    developer = {
        "id": max((item["id"] for item in developers), default=0) + 1,
        "name": name,
        "role": role,
    }
    developers.append(developer)
    return developer


def find_developer(developers: list[dict[str, Any]],
                   query: str) -> list[dict[str, Any]]:
    """Найти разработчиков по имени или роли."""
    query = query.casefold()
    return [
        item for item in developers
        if query in item["name"].casefold()
        or query in item.get("role", "").casefold()
    ]
