"""Функции безопасного ввода пользователя."""

from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить целое число и повторить ввод при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ."""
    while True:
        value = input(prompt)
        try:
            return datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            print("Введите дату в формате ДД.ММ.ГГГГ.")


def input_text(prompt: str) -> str:
    """Запросить непустой текст."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Поле не может быть пустым.")
