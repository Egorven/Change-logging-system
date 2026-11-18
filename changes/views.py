"""View-функции приложения changes."""

from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from changes.forms import ChangeFilterForm, ChangeForm
from changes.models import Change

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
    """Список изменений с проверенной Django-формой фильтрации."""
    filter_form = ChangeFilterForm(request.GET or None)
    changes_query = Change.objects.active().select_related(
        "project", "version", "developer"
    ).annotate(project_name=F("project__name"))
    if filter_form.is_valid():
        data = filter_form.cleaned_data
        if data.get("status") == "all":
            changes_query = Change.objects.select_related(
                "project", "version", "developer"
            ).annotate(project_name=F("project__name"))
        elif data.get("status") == "cancelled":
            changes_query = Change.objects.filter(
                status=Change.CANCELLED
            ).select_related(
                "project", "version", "developer"
            ).annotate(project_name=F("project__name"))
        if data.get("type"):
            changes_query = changes_query.filter(type=data["type"])
        if data.get("q"):
            changes_query = changes_query.filter(
                Q(description__icontains=data["q"])
                | Q(author__icontains=data["q"])
                | Q(developer__name__icontains=data["q"])
            )
        if data.get("project"):
            changes_query = changes_query.filter(project=data["project"])
        if data.get("developer"):
            changes_query = changes_query.filter(developer=data["developer"])
        if data.get("date_from"):
            changes_query = changes_query.filter(date__gte=data["date_from"])
        if data.get("date_to"):
            changes_query = changes_query.filter(date__lte=data["date_to"])
        sort = data.get("sort") or "date"
    else:
        sort = "date"
    sort_fields = {
        "date": "-date",
        "project": "project__name",
        "type": "type",
    }
    changes_query = changes_query.order_by(
        sort_fields[sort], "-pk"
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
    active_changes = Change.objects.active().count()
    context = {
        "changes": page_obj,
        "page_obj": page_obj,
        "badges": BADGES,
        "labels": LABELS,
        "statistics": statistics,
        "total_changes": total_changes,
        "active_changes": active_changes,
        "filter_form": filter_form,
        "selected_type": request.GET.get("type", ""),
        "search_text": request.GET.get("q", ""),
        "selected_project": request.GET.get("project", ""),
        "project_options": filter_form.fields["project"].queryset,
        "developer_options": filter_form.fields["developer"].queryset,
        "selected_developer": request.GET.get("developer", ""),
        "selected_status": request.GET.get("status", "active"),
        "date_from": request.GET.get("date_from", ""),
        "date_to": request.GET.get("date_to", ""),
        "sort": sort,
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


def change_create(request):
    """Создаёт запись изменения по GET/POST с серверной валидацией."""
    form = ChangeForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        change = form.save()
        return redirect("changes:change_detail", change_id=change.pk)
    return render(request, "changes/change_form.html", {
        "form": form, "page_title": "Новое изменение",
    })


def change_edit(request, change_id):
    """Редактирует существующую запись, не открывая служебные поля."""
    change = get_object_or_404(Change, pk=change_id)
    form = ChangeForm(
        request.POST or None, request.FILES or None, instance=change
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("changes:change_detail", change_id=change.pk)
    return render(request, "changes/change_form.html", {
        "form": form, "change": change, "page_title": "Редактирование",
    })


def change_cancel(request, change_id):
    """Отменяет запись только изменяющим POST-запросом."""
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    change = get_object_or_404(Change, pk=change_id)
    if change.status != Change.CANCELLED:
        change.status = Change.CANCELLED
        change.save(update_fields=["status"])
    return redirect("changes:change_detail", change_id=change.pk)
