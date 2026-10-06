"""View-функции приложения projects."""

from django.http import HttpResponse

from homepage.views import page
from storage import load_projects, load_versions


def find_project_by_id(projects, project_id):
    """Найти проект по идентификатору."""
    for p in projects:
        if p.id == project_id:
            return p
    return None


def projects(request):
    """Список всех проектов."""
    projects_list = load_projects("data/project.json")

    items = ""
    for project in projects_list:
        items += (
            f'<li class="list-group-item d-flex '
            f'justify-content-between">'
            f'<a href="/projects/{project.id}/">{project.name}</a>'
            f"</li>"
        )
    if not items:
        items = '<li class="list-group-item">Проектов пока нет</li>'

    content = f"""
    <h1>Проекты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("ChangeLog — проекты", content))


def project_detail(request, project_id):
    """Страница одного проекта с версиями."""
    projects_list = load_projects("data/project.json")
    project = find_project_by_id(projects_list, project_id)

    if project is None:
        content = """
        <h1 class="text-danger">Проект не найден</h1>
        <a href="/projects/" class="btn btn-outline-secondary">
            ← к списку проектов
        </a>
        """
        return HttpResponse(
            page("Проект не найден", content), status=404,
        )

    versions_list = load_versions("data/version.json", projects_list)
    project_versions = [
        v for v in versions_list
        if v.project and v.project.id == project.id
    ]

    versions_html = ""
    for v in project_versions:
        versions_html += (
            f'<li class="list-group-item">{v.name} — {v.release_date}</li>'
        )
    if not versions_html:
        versions_html = '<li class="list-group-item">Версий пока нет</li>'

    content = f"""
    <div class="card"><div class="card-body">
      <h5 class="card-title">{project.name}</h5>
      <p><strong>ID:</strong> {project.id}</p>
      <p>{project.description}</p>
      <h6 class="mt-3">Версии:</h6>
      <ul class="list-group">{versions_html}</ul>
      <a href="/projects/" class="btn btn-outline-secondary mt-3">
          ← к списку проектов
      </a>
    </div></div>
    """
    return HttpResponse(page(project.name, content))
