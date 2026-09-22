"""Класс Developer — разработчик."""

from typing import Any


class Developer:
    """Разработчик — автор изменений."""

    def __init__(self, developer_id: int, name: str, role: str = "") -> None:
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
