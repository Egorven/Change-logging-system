"""Настройка админ-панели приложения changes."""

from django.contrib import admin

from changes.models import Change, Developer


admin.site.register(Change)
admin.site.register(Developer)
# Register your models here.
