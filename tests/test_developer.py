"""Тесты для модуля developer_ops и класса Developer."""

from models import Developer
from developer_ops import add_developer, find_developer


def test_add_developer() -> None:
    """Проверить создание разработчика и добавление в коллекцию."""
    developers: list[Developer] = []
    developer = add_developer(developers, "Иван", "Разработчик")
    assert developer.id == 1
    assert developer.name == "Иван"
    assert developer.role == "Разработчик"
    assert len(developers) == 1
    assert developers[0] is developer


def test_find_developer() -> None:
    """Проверить поиск разработчиков по имени или роли."""
    dev1 = Developer(1, "Иван Петров", "Разработчик")
    dev2 = Developer(2, "Пётр Сидоров", "Тестировщик")
    developers = [dev1, dev2]

    result = find_developer(developers, "петров")
    assert len(result) == 1
    assert result[0] is dev1


def test_find_developer_by_role() -> None:
    """Проверить поиск разработчиков по роли."""
    dev1 = Developer(1, "Иван Петров", "Разработчик")
    dev2 = Developer(2, "Пётр Сидоров", "Тестировщик")
    dev3 = Developer(3, "Сергей Иванов", "Разработчик")
    developers = [dev1, dev2, dev3]

    result = find_developer(developers, "разработчик")
    assert len(result) == 2
    assert dev1 in result
    assert dev3 in result
    assert dev2 not in result


def test_developer_str() -> None:
    """Проверить строковое представление разработчика."""
    developer = Developer(1, "Иван Петров", "Разработчик")
    str_repr = str(developer)
    assert "[1]" in str_repr
    assert "Иван Петров" in str_repr
    assert "Разработчик" in str_repr


def test_developer_from_data() -> None:
    """Проверить создание разработчика из словаря данных."""
    data = {"id": 5, "name": "Анна Смирнова", "role": "Аналитик"}
    developer = Developer.from_data(data)
    assert developer.id == 5
    assert developer.name == "Анна Смирнова"
    assert developer.role == "Аналитик"
