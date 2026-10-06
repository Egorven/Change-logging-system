"""Модуль Version — версия проекта и операции с ней."""

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
        return (
            f"[{self.id}] {self.name} "
            f"({self.release_date}) — {project_name}"
        )


def add_version(
    versions: list[Version],
    project: Project,
    version_name: str,
    release_date: str,
) -> Version:
    """Добавить версию проекта и вернуть созданный объект."""
    version_id = max((v.id for v in versions), default=0) + 1
    version = Version(version_id, version_name, release_date, project)
    versions.append(version)
    return version


def sort_versions(versions: list[Version]) -> list[Version]:
    """Вернуть версии, отсортированные по дате выпуска."""
    return sorted(versions, key=lambda v: v.release_date)
