"""Настройка административной панели журнала изменений."""

from django.contrib import admin
from django.db.models import Count

from changes.models import Change, Developer


class DeveloperChangeInline(admin.TabularInline):
    model = Change
    extra = 0
    fields = ("type", "description", "date", "project", "version")
    can_delete = False


@admin.register(Change)
class ChangeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "author",
        "date",
        "project",
        "version",
        "developer",
    )
    list_display_links = ("id",)
    search_fields = (
        "description",
        "author",
        "project__name",
        "developer__name",
    )
    list_filter = ("type", "date", "project", "developer")
    ordering = ("-date", "-pk")
    list_per_page = 20
    list_select_related = ("project", "version", "developer")


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "role", "change_count")
    list_display_links = ("name",)
    search_fields = ("name", "role")
    ordering = ("name",)
    list_per_page = 20
    inlines = (DeveloperChangeInline,)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            admin_change_count=Count("changes"),
        )

    @admin.display(description="Записей изменений",
                   ordering="admin_change_count")
    def change_count(self, obj):
        return obj.admin_change_count
