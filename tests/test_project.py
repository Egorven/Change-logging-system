"""Тесты для модуля project_ops и класса Project."""

from models import Change, Project, Version
from project_ops import add_project, delete_project


def test_add_project() -> None:
    """Проверить создание проекта и добавление в коллекцию."""
    projects: list[Project] = []
    project = add_project(projects, "Demo", "Описание")
    assert project.id == 1
    assert project.name == "Demo"
    assert project.description == "Описание"
    assert len(projects) == 1
    assert projects[0] is project


def test_delete_project() -> None:
    """Проверить удаление проекта по идентификатору."""
    project = Project(1, "Demo", "Описание")
    projects = [project]
    assert delete_project(projects, 1)
    assert len(projects) == 0


def test_delete_project_not_found() -> None:
    """Проверить удаление несуществующего проекта."""
    projects: list[Project] = []
    assert not delete_project(projects, 999)


def test_delete_project_related_data() -> None:
    """Проверить каскадное удаление связанных версий и изменений."""
    project1 = Project(1, "Demo", "Описание")
    project2 = Project(2, "Other", "Другой")

    projects = [project1, project2]
    versions = [
        Version(1, "1.0.0", "2026-09-10", project1),
        Version(2, "1.0.0", "2026-09-10", project2),
    ]
    changes = [
        Change(
            1,
            "fixed",
            "Исправление",
            "Иван",
            "2026-09-10",
            project=project1,
            version=versions[0],
        ),
        Change(
            2,
            "added",
            "Добавление",
            "Пётр",
            "2026-09-11",
            project=project2,
            version=versions[1],
        ),
    ]

    # Собираем ID версий удаляемого проекта
    version_ids = {v.id for v in versions if v.project is project1}

    assert delete_project(projects, 1)

    # Каскадное удаление версий
    versions[:] = [v for v in versions if v.id not in version_ids]
    # Каскадное удаление изменений
    changes[:] = [c for c in changes if c.project is not project1]

    assert len(versions) == 1
    assert versions[0] is versions[0]  # версия project2 осталась
    assert versions[0].project is project2

    assert len(changes) == 1
    assert changes[0].project is project2


def test_project_str() -> None:
    """Проверить строковое представление проекта."""
    project = Project(1, "Demo", "Описание")
    str_repr = str(project)
    assert "[1]" in str_repr
    assert "Demo" in str_repr
    assert "Описание" in str_repr


def test_project_str_without_description() -> None:
    """Проверить строковое представление проекта без описания."""
    project = Project(1, "Demo", "")
    str_repr = str(project)
    assert "[1]" in str_repr
    assert "Demo" in str_repr
