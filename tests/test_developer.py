from developer import add_developer, find_developer


def test_add_developer() -> None:
    developers = []
    developer = add_developer(developers, "Иван", "Разработчик")
    assert developer["id"] == 1


def test_find_developer() -> None:
    developers = [{"id": 1, "name": "Иван Петров", "role": "Разработчик"}]
    assert find_developer(developers, "петров") == developers
