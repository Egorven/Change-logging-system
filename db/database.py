"""Подключение и базовые операции с SQLite-базой проекта."""

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "changelog.sqlite"


def get_connection() -> sqlite3.Connection:
    """Создать соединение с включённой проверкой внешних ключей."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    """Создать таблицы по SQL-схеме."""
    schema_path = BASE_DIR / "sql" / "schema.sql"
    with schema_path.open(encoding="utf-8") as schema_file:
        schema = schema_file.read()
    with get_connection() as connection:
        connection.executescript(schema)
        connection.commit()
