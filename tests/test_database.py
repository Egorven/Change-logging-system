"""Проверки SQLite-слоя ПР7."""

import sqlite3

import pytest

from db.database import get_connection


def test_corrected_change_date_query_returns_rows() -> None:
    """Исправленный запрос использует действительное имя столбца."""
    with get_connection() as connection:
        rows = connection.execute(
            """SELECT id, change_date
               FROM changes
               WHERE change_date >= ? AND change_date <= ?""",
            ("2026-09-01", "2026-09-30"),
        ).fetchall()

    assert len(rows) == 3


def test_invalid_change_date_column_is_reported() -> None:
    """Ошибка имени поля не маскируется и позволяет диагностировать запрос."""
    with get_connection() as connection:
        with pytest.raises(sqlite3.OperationalError, match="no such column"):
            connection.execute(
                "SELECT id FROM changes WHERE date_created >= ?",
                ("2026-09-01",),
            )
