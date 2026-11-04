"""Общие данные для шаблонов проекта."""

from projects.models import Project


def project_context(request):
    """Передать в шаблоны название сайта и количество проектов."""
    return {
        "site_name": "ChangeLog",
        "projects_count": Project.objects.count(),
    }
