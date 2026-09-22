from changes import (
    add_change,
    filter_by_type,
    format_entry,
    get_statistics,
)


def test_add_change_and_format_entry() -> None:
    changes = []
    change = add_change(
        changes, "fixed", "Исправлена ошибка", "Иван", "2026-09-10"
    )
    assert change["id"] == 1
    assert "Исправлено" in format_entry(change)


def test_filter_by_type() -> None:
    changes = [
        {"id": 1, "type": "fixed"},
        {"id": 2, "type": "added"},
    ]
    assert filter_by_type(changes, "fixed") == [changes[0]]


def test_statistics() -> None:
    changes = [
        {"id": 1, "type": "fixed"},
        {"id": 2, "type": "added"},
    ]
    assert get_statistics(changes) == {"fixed": 1, "added": 1}
