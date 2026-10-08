"""View-функции приложения projects."""

from django.shortcuts import render

from storage import load_projects, load_versions


def find_project_by_id(projects, project_id):
    """Найти проект по идентификатору."""
    for project in projects:
        if project.id == project_id:
            return project
    return None


def projects(request):
    """Список всех проектов."""
    project_list = load_projects("data/project.json")
    return render(
        request,
        "projects/project_list.html",
        {"projects": project_list},
    )


def project_detail(request, project_id):
    """Страница одного проекта с версиями."""
    projects_list = load_projects("data/project.json")
    project = find_project_by_id(projects_list, project_id)

    if project is None:
        return render(
            request,
            "projects/project_detail.html",
            {"project": None, "versions": []},
            status=404,
        )

    versions_list = load_versions("data/version.json", projects_list)
    project_versions = [
        version for version in versions_list
        if version.project and version.project.id == project.id
    ]
    return render(
        request,
        "projects/project_detail.html",
        {"project": project, "versions": project_versions},
    )
