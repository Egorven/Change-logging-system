"""Операции с коллекцией записей журнала изменений."""

from collections import Counter
from models import Change, Project, Version, Developer


def add_change(
    changes: list[Change],
    change_type: str,
    description: str,
    author: str,
    change_date: str,
    project: Project | None = None,
    version: Version | None = None,
    developer: Developer | None = None,
) -> Change:
    """Добавить запись об изменении и вернуть её."""
    change_id = max((c.id for c in changes), default=0) + 1
    change = Change(
        change_id,
        change_type,
        description,
        author,
        change_date,
        project,
        version,
        developer,
    )
    changes.append(change)
    return change


def filter_by_type(changes: list[Change], target_type: str) -> list[Change]:
    """Отфильтровать изменения по категории."""
    return [c for c in changes if c.type == target_type]


def sort_changes(changes: list[Change]) -> list[Change]:
    """Вернуть изменения, отсортированные от новых к старым."""
    return sorted(changes, key=lambda c: c.date, reverse=True)


def get_statistics(changes: list[Change]) -> dict[str, int]:
    """Подсчитать количество изменений каждого типа."""
    return dict(Counter(c.type for c in changes))
