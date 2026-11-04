"""View-функции приложения changes."""

from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, render

from changes.models import Change
from projects.models import Project

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


def changes(request):
    """Список изменений с фильтрацией по параметрам пользователя."""
    change_type = request.GET.get("type", "").strip()
    search_text = request.GET.get("q", "").strip()
    project_id = request.GET.get("project", "").strip()
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()
    sort = request.GET.get("sort", "date")
    error = None
    changes_query = Change.objects.select_related(
        "project", "version", "developer"
    ).annotate(project_name=F("project__name"))
    if change_type in LABELS:
        changes_query = changes_query.filter(type=change_type)
    if search_text:
        changes_query = changes_query.filter(
            Q(description__icontains=search_text)
            | Q(author__icontains=search_text)
            | Q(developer__name__icontains=search_text)
        )
    if project_id.isdigit():
        changes_query = changes_query.filter(project_id=int(project_id))
    if date_from:
        try:
            changes_query = changes_query.filter(
                date__gte=datetime.strptime(date_from, "%Y-%m-%d").date()
            )
        except ValueError:
            error = "Укажите корректную начальную дату."
    if date_to:
        try:
            changes_query = changes_query.filter(
                date__lte=datetime.strptime(date_to, "%Y-%m-%d").date()
            )
        except ValueError:
            error = "Укажите корректную конечную дату."
    sort_fields = {
        "date": "-date",
        "project": "project__name",
        "type": "type",
    }
    changes_query = changes_query.order_by(
        sort_fields.get(sort, "-date"), "-pk"
    )
    page_obj = Paginator(changes_query, 5).get_page(
        request.GET.get("page")
    )
    statistics = [
        {
            "label": LABELS.get(item["type"], "Изменено"),
            "count": item["count"],
        }
        for item in Change.objects.values("type")
        .annotate(count=Count("id"))
        .order_by("type")
    ]
    total_changes = Change.objects.aggregate(total=Count("id"))["total"]
    active_changes = Change.objects.exclude(
        type=Change.REMOVED,
    ).count()
    context = {
        "changes": page_obj,
        "page_obj": page_obj,
        "badges": BADGES,
        "labels": LABELS,
        "statistics": statistics,
        "total_changes": total_changes,
        "active_changes": active_changes,
        "selected_type": change_type,
        "search_text": search_text,
        "selected_project": project_id,
        "project_options": Project.objects.order_by("name"),
        "date_from": date_from,
        "date_to": date_to,
        "sort": sort if sort in sort_fields else "date",
        "error": error,
    }
    return render(request, "changes/change_list.html", context)


def change_detail(request, change_id):
    """Страница одного изменения."""
    change = get_object_or_404(
        Change.objects.select_related("project", "version", "developer"),
        pk=change_id,
    )

    context = {
        "change": change,
        "author": change.developer.name if change.developer else change.author,
        "project_name": change.project.name if change.project else "—",
        "version_name": change.version.name if change.version else "—",
        "badge": BADGES.get(change.type, "bg-secondary"),
        "label": LABELS.get(change.type, "Изменено"),
    }
    return render(request, "changes/change_detail.html", context)
