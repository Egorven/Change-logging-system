"""Точка запуска системы ведения журнала изменений."""

from pathlib import Path
from typing import Any

from changes import (
    add_change,
    filter_by_type,
    format_entry,
    get_statistics,
    sort_changes,
)
from developer import add_developer
from project import add_project, delete_project
from storage import (
    load_changes,
    load_developers,
    load_projects,
    load_versions,
    save_changes,
    save_developers,
    save_projects,
    save_versions,
    to_json,
)
from utils import input_date, input_int, input_text
from version import add_version, sort_versions


DATA_DIR = Path(__file__).parent / "data"
PROJECTS_FILE = DATA_DIR / "project.json"
VERSIONS_FILE = DATA_DIR / "version.json"
CHANGES_FILE = DATA_DIR / "changes.json"
DEVELOPERS_FILE = DATA_DIR / "developer.json"
CHANGE_TYPES = {1: "added", 2: "fixed", 3: "removed"}


def show_projects(projects: list[dict[str, Any]]) -> None:
    """Вывести список проектов."""
    if not projects:
        print("Проекты отсутствуют.")
        return
    for item in projects:
        print(f"{item['id']}. {item['name']} — {item.get('description', '')}")


def show_versions(versions: list[dict[str, Any]]) -> None:
    """Вывести список версий."""
    if not versions:
        print("Версии отсутствуют.")
        return
    for number, item in enumerate(sort_versions(versions), start=1):
        print(
            f"{number}. {item['name']} "
            f"(дата: {item['release_date']})"
        )


def show_changes(changes: list[dict[str, Any]]) -> None:
    """Вывести журнал изменений."""
    if not changes:
        print("Изменения отсутствуют.")
        return
    for item in sort_changes(changes):
        print(f"{item['id']}. {item['date']} {format_entry(item)}")


def show_developers(developers: list[dict[str, Any]]) -> None:
    """Вывести список разработчиков."""
    if not developers:
        print("Разработчики отсутствуют.")
        return
    for number, item in enumerate(developers, start=1):
        print(f"{number}. {item['name']} — {item.get('role', '')}")


def save_all(
    projects: list[dict[str, Any]],
    versions: list[dict[str, Any]],
    changes: list[dict[str, Any]],
    developers: list[dict[str, Any]],
) -> None:
    """Сохранить все коллекции приложения."""
    save_projects(PROJECTS_FILE, projects)
    save_versions(VERSIONS_FILE, versions)
    save_changes(CHANGES_FILE, changes)
    save_developers(DEVELOPERS_FILE, developers)


def print_menu() -> None:
    """Вывести главное меню приложения."""
    print(
        """
=== Система ведения журнала изменений ===
1. Показать проекты
2. Добавить проект
3. Удалить проект
4. Показать версии
5. Добавить версию
6. Показать изменения
7. Фильтровать изменения по типу
8. Добавить изменение
9. Показать статистику изменений
10. Экспортировать данные проекта в JSON
11. Добавить разработчика
12. Показать список разработчиков
0. Выход
"""
    )


def main() -> None:
    """Загрузить данные и запустить цикл меню."""
    try:
        projects = load_projects(PROJECTS_FILE)
        versions = load_versions(VERSIONS_FILE)
        changes = load_changes(CHANGES_FILE)
        developers = load_developers(DEVELOPERS_FILE)
    except ValueError as error:
        print(f"Ошибка загрузки данных: {error}")
        return

    while True:
        print_menu()
        choice = input_int("Выберите действие: ")

        if choice == 0:
            save_all(projects, versions, changes, developers)
            print("Данные сохранены.")
            return
        if choice == 1:
            show_projects(projects)
        elif choice == 2:
            name = input_text("Название проекта: ")
            description = input_text("Описание проекта: ")
            add_project(projects, name, description)
            save_projects(PROJECTS_FILE, projects)
        elif choice == 3:
            project_id = input_int("ID проекта: ")
            project_versions = [
                item for item in versions
                if item["project_id"] == project_id
            ]
            version_ids = {item["id"] for item in project_versions}
            project_deleted = delete_project(projects, project_id)
            if project_deleted:
                versions[:] = [
                    item for item in versions
                    if item["id"] not in version_ids
                ]
                changes[:] = [
                    item for item in changes
                    if item.get("project_id") != project_id
                    and item.get("version_id") not in version_ids
                ]
                save_all(projects, versions, changes, developers)
                print("Проект, его версии и изменения удалены.")
            else:
                print("Проект не найден.")
        elif choice == 4:
            project_id = input_int("ID проекта: ")
            if not any(item["id"] == project_id for item in projects):
                print("Проект не найден.")
                continue
            project_versions = [
                item for item in versions
                if item["project_id"] == project_id
            ]
            show_versions(project_versions)
        elif choice == 5:
            project_id = input_int("ID проекта: ")
            if not any(item["id"] == project_id for item in projects):
                print("Проект не найден.")
                continue
            version_name = input_text("Название версии: ")
            release_date = input_date("Дата выпуска (ДД.ММ.ГГГГ): ")
            add_version(
                versions, project_id, version_name, release_date.isoformat()
            )
            save_versions(VERSIONS_FILE, versions)
        elif choice == 6:
            project_id = input_int("ID проекта: ")
            if not any(item["id"] == project_id for item in projects):
                print("Проект не найден.")
                continue
            project_changes = [
                item for item in changes
                if item.get("project_id") == project_id
            ]
            show_changes(project_changes)
        elif choice == 7:
            project_id = input_int("ID проекта: ")
            if not any(item["id"] == project_id for item in projects):
                print("Проект не найден.")
                continue
            print(
                "Тип изменения: 1 - добавлено, "
                "2 - исправлено, 3 - удалено"
            )
            type_number = input_int("Выберите тип изменения: ")
            target_type = CHANGE_TYPES.get(type_number)
            if target_type is None:
                print("Неизвестный тип изменения.")
                continue
            project_changes = [
                item for item in changes
                if item.get("project_id") == project_id
            ]
            show_changes(filter_by_type(project_changes, target_type))
        elif choice == 8:
            project_id = input_int("ID проекта: ")
            if not any(item["id"] == project_id for item in projects):
                print("Проект не найден.")
                continue
            print(
                "Тип изменения: 1 - добавлено, "
                "2 - исправлено, 3 - удалено"
            )
            type_number = input_int("Выберите тип изменения: ")
            change_type = CHANGE_TYPES.get(type_number)
            if change_type is None:
                print("Неизвестный тип изменения.")
                continue
            description = input_text("Описание: ")
            developer_id = input_int("ID разработчика: ")
            developer = next(
                (
                    item for item in developers
                    if item["id"] == developer_id
                ),
                None,
            )
            if developer is None:
                print("Разработчик не найден.")
                continue
            change_date = input_date("Дата изменения (ДД.ММ.ГГГГ): ")
            add_change(
                changes,
                change_type,
                description,
                developer["name"],
                change_date.isoformat(),
                project_id=project_id,
                developer_id=developer_id,
            )
            save_changes(CHANGES_FILE, changes)
        elif choice == 9:
            project_id = input_int("ID проекта: ")
            if not any(item["id"] == project_id for item in projects):
                print("Проект не найден.")
                continue
            project_changes = [
                item for item in changes
                if item.get("project_id") == project_id
            ]
            print(get_statistics(project_changes))
        elif choice == 10:
            project_id = input_int("ID проекта: ")
            project = next(
                (item for item in projects if item["id"] == project_id),
                None,
            )
            if project is None:
                print("Проект не найден.")
                continue
            project_versions = [
                item for item in versions
                if item["project_id"] == project_id
            ]
            project_changes = [
                item for item in changes
                if item.get("project_id") == project_id
            ]
            print(
                to_json(
                    project,
                    project_versions,
                    project_changes,
                )
            )
        elif choice == 11:
            name = input_text("Имя разработчика: ")
            role = input_text("Роль: ")
            add_developer(developers, name, role)
            save_developers(DEVELOPERS_FILE, developers)
        elif choice == 12:
            show_developers(developers)
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
