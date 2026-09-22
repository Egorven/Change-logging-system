"""Тесты для модуля change_ops и класса Change."""

from models import Change
from changes_ops import (
    add_change,
    filter_by_type,
    get_statistics,
    sort_changes,
)


def test_add_change_and_format_entry() -> None:
    """Проверить создание изменения и форматирование записи."""
    changes: list[Change] = []
    change = add_change(
        changes,
        "fixed",
        "Исправлена ошибка",
        "Иван",
        "2026-09-10",
    )
    assert change.id == 1
    assert change.type == "fixed"
    assert change.description == "Исправлена ошибка"
    assert change.author == "Иван"
    assert change.date == "2026-09-10"
    assert "Исправлено" in change.format_entry()


def test_filter_by_type() -> None:
    """Проверить фильтрацию изменений по типу."""
    change1 = Change(1, "fixed", "Исправление", "Иван", "2026-09-10")
    change2 = Change(2, "added", "Добавление", "Пётр", "2026-09-11")
    changes = [change1, change2]

    filtered = filter_by_type(changes, "fixed")
    assert len(filtered) == 1
    assert filtered[0] is change1
    assert filtered[0].type == "fixed"


def test_statistics() -> None:
    """Проверить подсчёт статистики по типам изменений."""
    change1 = Change(1, "fixed", "Исправление", "Иван", "2026-09-10")
    change2 = Change(2, "added", "Добавление", "Пётр", "2026-09-11")
    change3 = Change(3, "fixed", "Ещё исправление", "Сергей", "2026-09-12")
    changes = [change1, change2, change3]

    stats = get_statistics(changes)
    assert stats == {"fixed": 2, "added": 1}


def test_change_methods() -> None:
    """Проверить методы проверки типа изменения."""
    change_added = Change(1, "added", "Добавление", "Иван", "2026-09-10")
    change_fixed = Change(2, "fixed", "Исправление", "Пётр", "2026-09-11")
    change_removed = Change(3, "removed", "Удаление", "Сергей", "2026-09-12")

    assert change_added.is_added()
    assert not change_added.is_fixed()
    assert not change_added.is_removed()

    assert not change_fixed.is_added()
    assert change_fixed.is_fixed()
    assert not change_fixed.is_removed()

    assert not change_removed.is_added()
    assert not change_removed.is_fixed()
    assert change_removed.is_removed()


def test_change_str() -> None:
    """Проверить строковое представление изменения."""
    change = Change(1, "fixed", "Исправлена ошибка", "Иван", "2026-09-10")
    str_repr = str(change)
    assert "[1]" in str_repr
    assert "2026-09-10" in str_repr
    assert "Исправлено" in str_repr
    assert "Исправлена ошибка" in str_repr
    assert "Иван" in str_repr


def test_sort_changes() -> None:
    """Проверить сортировку изменений по дате."""
    change1 = Change(1, "fixed", "Старое", "Иван", "2026-09-10")
    change2 = Change(2, "added", "Среднее", "Пётр", "2026-09-15")
    change3 = Change(3, "removed", "Новое", "Сергей", "2026-09-20")
    changes = [change1, change2, change3]

    sorted_changes = sort_changes(changes)
    assert sorted_changes[0].date == "2026-09-20"
    assert sorted_changes[1].date == "2026-09-15"
    assert sorted_changes[2].date == "2026-09-10"
