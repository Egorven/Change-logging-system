"""View-функции приложения projects."""

from django.shortcuts import render

from db.database import get_connection


def find_project_by_id(projects, project_id):
    """Найти проект по идентификатору."""
    for project in projects:
        if project.id == project_id:
            return project
    return None


def projects(request):
    """Список всех проектов."""
    with get_connection() as connection:
        project_list = connection.execute(
            """SELECT id, name, description
               FROM projects
               ORDER BY name"""
        ).fetchall()
    return render(
        request,
        "projects/project_list.html",
        {"projects": project_list},
    )


def project_detail(request, project_id):
    """Страница одного проекта с версиями."""
    with get_connection() as connection:
        project = connection.execute(
            """SELECT id, name, description
               FROM projects
               WHERE id = ?""",
            (project_id,),
        ).fetchone()
        project_versions = connection.execute(
            """SELECT id, name, release_date, project_id
               FROM versions
               WHERE project_id = ?
               ORDER BY release_date DESC""",
            (project_id,),
        ).fetchall()

    if project is None:
        return render(
            request,
            "projects/project_detail.html",
            {"project": None, "versions": []},
            status=404,
        )

    return render(
        request,
        "projects/project_detail.html",
        {"project": project, "versions": project_versions},
    )
