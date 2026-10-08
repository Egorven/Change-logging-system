"""View-функции приложения changes."""

from django.shortcuts import render

from storage import (
    load_changes,
    load_developers,
    load_projects,
    load_versions,
)

BADGES = {
    "added": "bg-success",
    "fixed": "bg-warning",
    "removed": "bg-danger",
}
LABELS = {
    "added": "Добавлено",
    "fixed": "Исправлено",
    "removed": "Удалено",
}


def _load_all():
    """Загрузить все изменения со связанными объектами."""
    projects = load_projects("data/project.json")
    developers = load_developers("data/developer.json")
    versions = load_versions("data/version.json", projects)
    return load_changes(
        "data/changes.json", projects, versions, developers,
    )


def changes(request):
    """Список всех изменений."""
    changes_list = _load_all()
    context = {
        "changes": changes_list,
        "badges": BADGES,
        "labels": LABELS,
    }
    return render(request, "changes/change_list.html", context)


def change_detail(request, change_id):
    """Страница одного изменения."""
    changes_list = _load_all()
    change = next((
        item for item in changes_list if item.id == change_id), None
        )

    if change is None:
        return render(
            request,
            "changes/change_detail.html",
            {"change": None},
            status=404,
        )

    author = change.developer.name if change.developer else change.author
    context = {
        "change": change,
        "author": author,
        "project_name": change.project.name if change.project else "—",
        "version_name": change.version.name if change.version else "—",
        "badge": BADGES.get(change.type, "bg-secondary"),
        "label": LABELS.get(change.type, "Изменено"),
    }
    return render(request, "changes/change_detail.html", context)
