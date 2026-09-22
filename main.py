"""Точка запуска системы ведения журнала изменений."""

from pathlib import Path

from models import Change, Developer, Project, Version
from changes_ops import (
    add_change,
    filter_by_type,
    get_statistics,
    sort_changes,
)
from developer_ops import add_developer
from project_ops import add_project, delete_project
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
from version_ops import add_version, sort_versions

DATA_DIR = Path(__file__).parent / "data"
PROJECTS_FILE = DATA_DIR / "project.json"
VERSIONS_FILE = DATA_DIR / "version.json"
CHANGES_FILE = DATA_DIR / "changes.json"
DEVELOPERS_FILE = DATA_DIR / "developer.json"
CHANGE_TYPES = {1: "added", 2: "fixed", 3: "removed"}


def show_projects(projects: list[Project]) -> None:
    """Вывести список проектов."""
    if not projects:
        print("Проекты отсутствуют.")
        return
    for project in projects:
        print(project)


def show_versions(versions: list[Version]) -> None:
    """Вывести список версий."""
    if not versions:
        print("Версии отсутствуют.")
        return
    for number, version in enumerate(sort_versions(versions), start=1):
        print(f"{number}. {version}")


def show_changes(changes: list[Change]) -> None:
    """Вывести журнал изменений."""
    if not changes:
        print("Изменения отсутствуют.")
        return
    for change in sort_changes(changes):
        print(change)


def show_developers(developers: list[Developer]) -> None:
    """Вывести список разработчиков."""
    if not developers:
        print("Разработчики отсутствуют.")
        return
    for number, developer in enumerate(developers, start=1):
        print(f"{number}. {developer}")


def save_all(
    projects: list[Project],
    versions: list[Version],
    changes: list[Change],
    developers: list[Developer],
) -> None:
    """Сохранить все коллекции приложения."""
    save_projects(PROJECTS_FILE, projects)
    save_versions(VERSIONS_FILE, versions)
    save_changes(CHANGES_FILE, changes)
    save_developers(DEVELOPERS_FILE, developers)


def find_project_by_id(
        projects: list[Project],
        project_id: int) -> Project | None:
    """Найти проект по идентификатору."""
    return next((p for p in projects if p.id == project_id), None)


def find_developer_by_id(
    developers: list[Developer], developer_id: int
) -> Developer | None:
    """Найти разработчика по идентификатору."""
    return next((d for d in developers if d.id == developer_id), None)


def print_menu() -> None:
    """Вывести главное меню приложения."""
    print("""
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
""")


def main() -> None:
    """Загрузить данные и запустить цикл меню."""
    try:
        projects = load_projects(PROJECTS_FILE)
        developers = load_developers(DEVELOPERS_FILE)
        versions = load_versions(VERSIONS_FILE, projects)
        changes = load_changes(CHANGES_FILE, projects, versions, developers)
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
            project = find_project_by_id(projects, project_id)
            if project is None:
                print("Проект не найден.")
                continue
            version_ids = {v.id for v in versions if v.project is project}
            project_deleted = delete_project(projects, project_id)
            if project_deleted:
                versions[:] = [
                    v for v in versions
                    if v.id not in version_ids
                ]
                changes[:] = [
                    c for c in changes
                    if c.project is not project
                ]
                save_all(projects, versions, changes, developers)
                print("Проект, его версии и изменения удалены.")
        elif choice == 4:
            project_id = input_int("ID проекта: ")
            project = find_project_by_id(projects, project_id)
            if project is None:
                print("Проект не найден.")
                continue
            project_versions = [v for v in versions if v.project is project]
            show_versions(project_versions)
        elif choice == 5:
            project_id = input_int("ID проекта: ")
            project = find_project_by_id(projects, project_id)
            if project is None:
                print("Проект не найден.")
                continue
            version_name = input_text("Название версии: ")
            release_date = input_date("Дата выпуска (ДД.ММ.ГГГГ): ")
            add_version(
                versions,
                project,
                version_name,
                release_date.isoformat()
                )
            save_versions(VERSIONS_FILE, versions)
        elif choice == 6:
            project_id = input_int("ID проекта: ")
            project = find_project_by_id(projects, project_id)
            if project is None:
                print("Проект не найден.")
                continue
            project_changes = [c for c in changes if c.project is project]
            show_changes(project_changes)
        elif choice == 7:
            project_id = input_int("ID проекта: ")
            project = find_project_by_id(projects, project_id)
            if project is None:
                print("Проект не найден.")
                continue
            print("Тип изменения: 1 - добавлено, 2 - исправлено, 3 - удалено")
            type_number = input_int("Выберите тип изменения: ")
            target_type = CHANGE_TYPES.get(type_number)
            if target_type is None:
                print("Неизвестный тип изменения.")
                continue
            project_changes = [c for c in changes if c.project is project]
            show_changes(filter_by_type(project_changes, target_type))
        elif choice == 8:
            project_id = input_int("ID проекта: ")
            project = find_project_by_id(projects, project_id)
            if project is None:
                print("Проект не найден.")
                continue
            print("Тип изменения: 1 - добавлено, 2 - исправлено, 3 - удалено")
            type_number = input_int("Выберите тип изменения: ")
            change_type = CHANGE_TYPES.get(type_number)
            if change_type is None:
                print("Неизвестный тип изменения.")
                continue
            description = input_text("Описание: ")
            developer_id = input_int("ID разработчика: ")
            developer = find_developer_by_id(developers, developer_id)
            if developer is None:
                print("Разработчик не найден.")
                continue
            change_date = input_date("Дата изменения (ДД.ММ.ГГГГ): ")
            add_change(
                changes,
                change_type,
                description,
                developer.name,
                change_date.isoformat(),
                project=project,
                developer=developer,
            )
            save_changes(CHANGES_FILE, changes)
        elif choice == 9:
            project_id = input_int("ID проекта: ")
            project = find_project_by_id(projects, project_id)
            if project is None:
                print("Проект не найден.")
                continue
            project_changes = [c for c in changes if c.project is project]
            print(get_statistics(project_changes))
        elif choice == 10:
            project_id = input_int("ID проекта: ")
            project = find_project_by_id(projects, project_id)
            if project is None:
                print("Проект не найден.")
                continue
            project_versions = [v for v in versions if v.project is project]
            project_changes = [c for c in changes if c.project is project]
            print(to_json(project, project_versions, project_changes))
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
