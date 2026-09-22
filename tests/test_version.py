"""Тесты для модуля version_ops и класса Version."""

from models import Project, Version
from version_ops import add_version, sort_versions


def test_add_version() -> None:
    """Проверить создание версии и добавление в коллекцию."""
    project = Project(1, "Demo", "Описание")
    versions: list[Version] = []
    version = add_version(versions, project, "1.0.0", "2026-09-10")
    assert version.id == 1
    assert version.name == "1.0.0"
    assert version.release_date == "2026-09-10"
    assert version.project is project
    assert len(versions) == 1


def test_sort_versions() -> None:
    """Проверить сортировку версий по дате выпуска."""
    project = Project(1, "Demo", "Описание")
    v1 = Version(1, "1.0.0", "2026-09-10", project)
    v2 = Version(2, "1.1.0", "2026-10-10", project)
    v3 = Version(3, "0.9.0", "2026-08-01", project)
    versions = [v1, v2, v3]

    sorted_versions = sort_versions(versions)
    assert sorted_versions[0].release_date == "2026-08-01"
    assert sorted_versions[1].release_date == "2026-09-10"
    assert sorted_versions[2].release_date == "2026-10-10"


def test_version_str() -> None:
    """Проверить строковое представление версии."""
    project = Project(1, "Demo", "Описание")
    version = Version(1, "1.0.0", "2026-09-10", project)
    str_repr = str(version)
    assert "[1]" in str_repr
    assert "1.0.0" in str_repr
    assert "2026-09-10" in str_repr
    assert "Demo" in str_repr


def test_version_without_project() -> None:
    """Проверить создание версии без связанного проекта."""
    version = Version(1, "1.0.0", "2026-09-10")
    assert version.project is None
    assert version.id == 1
    assert version.name == "1.0.0"
