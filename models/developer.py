"""Модуль Developer — разработчик и операции с ним."""
from typing import Any


class Developer:
    """Разработчик — автор изменений."""

    def __init__(
        self,
        developer_id: int,
        name: str,
        role: str = "",
    ) -> None:
        """Создать объект разработчика."""
        self.id = developer_id
        self.name = name
        self.role = role

    def __str__(self) -> str:
        """Строковое представление разработчика."""
        role = f" ({self.role})" if self.role else ""
        return f"[{self.id}] {self.name}{role}"

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Developer":
        """Создать разработчика из словаря данных."""
        return cls(
            developer_id=data["id"],
            name=data["name"],
            role=data.get("role", ""),
        )


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


def find_developer(
    developers: list[Developer],
    query: str,
) -> list[Developer]:
    """Найти разработчиков по имени или роли."""
    query = query.casefold()
    return [
        dev for dev in developers
        if query in dev.name.casefold()
        or query in dev.role.casefold()
    ]
