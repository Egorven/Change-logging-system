"""Операции с коллекцией разработчиков."""

from models import Developer


def add_developer(
    developers: list[Developer],
    name: str,
    role: str = "",
) -> Developer:
    """Добавить разработчика и вернуть созданный объект."""
    developer_id = max((d.id for d in developers), default=0) + 1
    developer = Developer(developer_id, name, role)
    developers.append(developer)
    return developer


def find_developer(developers: list[Developer], query: str) -> list[Developer]:
    """Найти разработчиков по имени или роли."""
    query = query.casefold()
    return [
        dev
        for dev in developers
        if query in dev.name.casefold() or query in dev.role.casefold()
    ]
