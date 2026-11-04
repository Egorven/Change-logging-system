"""View-функции приложения projects."""

from django.shortcuts import get_object_or_404, render

from projects.models import Project


def projects(request):
    """Список всех проектов."""
    project_list = Project.objects.order_by("name")
    return render(
        request,
        "projects/project_list.html",
        {"projects": project_list},
    )


def project_detail(request, project_id):
    """Страница одного проекта с версиями."""
    project = get_object_or_404(Project, pk=project_id)
    project_versions = project.versions.order_by("-release_date", "pk")

    return render(
        request,
        "projects/project_detail.html",
        {"project": project, "versions": project_versions},
    )
