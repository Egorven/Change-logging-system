"""Настройка административной панели проектов."""

from django.contrib import admin
from django.db.models import Count

from changes.models import Change
from projects.models import Project, Version


class VersionInline(admin.TabularInline):
    model = Version
    extra = 0
    fields = ("name", "release_date")


class ChangeInline(admin.TabularInline):
    model = Change
    extra = 0
    fields = ("type", "author", "date", "developer")
    can_delete = False


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "version_count", "name_length")
    list_display_links = ("name",)
    search_fields = ("name", "description")
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id", "slug", "name_length")
    inlines = (VersionInline, ChangeInline)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            admin_version_count=Count("versions"),
        )

    @admin.display(description="Версий", ordering="admin_version_count")
    def version_count(self, obj):
        return obj.admin_version_count


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "project", "release_date")
    search_fields = ("name", "project__name")
    list_filter = ("release_date", "project")
    ordering = ("-release_date", "pk")
    list_per_page = 20
    list_select_related = ("project",)


"""Настройка админ-панели приложения changes."""
