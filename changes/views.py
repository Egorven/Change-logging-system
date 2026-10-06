"""View-функции приложения changes."""

from django.http import HttpResponse

from homepage.views import page
from storage import (
    load_changes, load_developers, load_projects, load_versions,
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

    items = ""
    for change in changes_list:
        badge = BADGES.get(change.type, "bg-secondary")
        label = LABELS.get(change.type, "Изменено")
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between align-items-center">'
            f'<a href="/changes/{change.id}/">{change.description}</a>'
            f'<span class="badge {badge}">{label}</span>'
            f"</li>"
        )
    if not items:
        items = '<li class="list-group-item">Изменений пока нет</li>'

    content = f"""
    <h1>Журнал изменений</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("ChangeLog — изменения", content))


def change_detail(request, change_id):
    """Страница одного изменения."""
    changes_list = _load_all()
    change = next((c for c in changes_list if c.id == change_id), None)

    if change is None:
        content = """
        <h1 class="text-danger">Изменение не найдено</h1>
        <a href="/changes/" class="btn btn-outline-secondary">
            ← к списку изменений
        </a>
        """
        return HttpResponse(
            page("Изменение не найдено", content), status=404,
        )

    badge = BADGES.get(change.type, "bg-secondary")
    label = LABELS.get(change.type, "Изменено")
    project_name = change.project.name if change.project else "—"
    version_name = change.version.name if change.version else "—"
    author = change.developer.name if change.developer else change.author

    content = f"""
    <div class="card"><div class="card-body">
      <h5 class="card-title">{change.description}</h5>
      <p><strong>Тип:</strong>
         <span class="badge {badge}">{label}</span></p>
      <p><strong>Дата:</strong> {change.date}</p>
      <p><strong>Автор:</strong> {author}</p>
      <p><strong>Проект:</strong> {project_name}</p>
      <p><strong>Версия:</strong> {version_name}</p>
      <a href="/changes/" class="btn btn-outline-secondary">
          ← к списку изменений
      </a>
    </div></div>
    """
    return HttpResponse(page(f"Изменение №{change.id}", content))
