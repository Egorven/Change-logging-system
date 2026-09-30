"""Модуль Project — проект и операции с ним."""


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


def add_project(
    projects: list[Project],
    name: str,
    description: str = "",
) -> Project:
    """Добавить проект и вернуть созданный объект."""
    project_id = max((p.id for p in projects), default=0) + 1
    project = Project(project_id, name, description)
    projects.append(project)
    return project


def delete_project(projects: list[Project], project_id: int) -> bool:
    """Удалить проект по идентификатору."""
    for project in projects:
        if project.id == project_id:
            projects.remove(project)
            return True
    return False
