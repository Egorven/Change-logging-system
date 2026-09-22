"""Класс Project — проект."""


class Project:
    """Проект — основная сущность системы."""

    def __init__(
        self,
        project_id: int,
        name: str,
        description: str = "",
    ) -> None:
        """Создать объект проекта."""
        self.id = project_id
        self.name = name
        self.description = description

    def __str__(self) -> str:
        """Строковое представление проекта."""
        desc = f" — {self.description}" if self.description else ""
        return f"[{self.id}] {self.name}{desc}"
