"""Операции с коллекцией проектов."""

from models import Project


def add_project(projects:
                list[Project],
                name: str,
                description: str = "") -> Project:
    """Добавить проект и вернуть созданный объект."""
    project_id = max((p.id for p in projects), default=0) + 1
    project = Project(
        project_id,
        name,
        description)
    projects.append(project)
    return project


def delete_project(projects: list[Project], project_id: int) -> bool:
    """Удалить проект по идентификатору."""
    for project in projects:
        if project.id == project_id:
            projects.remove(project)
            return True
    return False
