"""Класс Change — запись журнала изменений."""

from typing import Optional
from .developer import Developer
from .project import Project
from .version import Version


class Change:
    """Запись журнала изменений."""

    def __init__(
        self,
        change_id: int,
        change_type: str,
        description: str,
        author: str,
        date: str,
        project: Optional[Project] = None,
        version: Optional[Version] = None,
        developer: Optional[Developer] = None,
    ) -> None:
        """Создать запись об изменении."""
        self.id = change_id
        self.type = change_type
        self.description = description
        self.author = author
        self.date = date
        self.project = project
        self.version = version
        self.developer = developer

    def format_entry(self) -> str:
        """Сформировать человекочитаемую запись."""
        labels = {
            "added": "Добавлено",
            "fixed": "Исправлено",
            "removed": "Удалено",
        }
        label = labels.get(self.type, "Изменено")
        return f"[{label}] {self.description} (автор: {self.author})"

    def is_added(self) -> bool:
        """Проверить, является ли изменение добавлением."""
        return self.type == "added"

    def is_fixed(self) -> bool:
        """Проверить, является ли изменение исправлением."""
        return self.type == "fixed"

    def is_removed(self) -> bool:
        """Проверить, является ли изменение удалением."""
        return self.type == "removed"

    def __str__(self) -> str:
        """Строковое представление записи."""
        return f"[{self.id}] {self.date} {self.format_entry()}"
