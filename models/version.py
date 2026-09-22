"""Класс Version — версия проекта."""

from typing import Optional
from .project import Project


class Version:
    """Версия проекта."""

    def __init__(
        self,
        version_id: int,
        name: str,
        release_date: str,
        project: Optional[Project] = None,
    ) -> None:
        """Создать объект версии."""
        self.id = version_id
        self.name = name
        self.release_date = release_date
        self.project = project

    def __str__(self) -> str:
        """Строковое представление версии."""
        project_name = self.project.name if self.project else "—"
        return (f"[{self.id}] {self.name} "
                f"({self.release_date}) — {project_name}")
