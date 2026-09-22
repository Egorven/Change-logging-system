"""Операции с коллекцией версий."""

from models import Version, Project


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
