"""Настройка админ-панели приложения projects."""

from django.contrib import admin

from projects.models import Project, Version


admin.site.register(Project)
admin.site.register(Version)
"""Настройка админ-панели приложения changes."""
