"""ORM-модели разработчиков и записей журнала изменений."""

from django.db import models

from projects.models import Project, Version


class Developer(models.Model):
    """Разработчик, который может быть автором записи журнала."""

    name = models.CharField(max_length=200, verbose_name="Имя")
    role = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Роль",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Разработчик"
        verbose_name_plural = "Разработчики"

    def __str__(self) -> str:
        return self.name


class Change(models.Model):
    """Запись журнала изменений."""

    ADDED = "added"
    FIXED = "fixed"
    REMOVED = "removed"
    TYPE_CHOICES = (
        (ADDED, "Добавлено"),
        (FIXED, "Исправлено"),
        (REMOVED, "Удалено"),
    )

    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Тип",
    )
    description = models.TextField(verbose_name="Описание")
    author = models.CharField(max_length=200, verbose_name="Автор")
    date = models.DateField(
        db_column="change_date",
        verbose_name="Дата изменения",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="changes",
        null=True,
        blank=True,
        verbose_name="Проект",
    )
    version = models.ForeignKey(
        Version,
        on_delete=models.SET_NULL,
        related_name="changes",
        null=True,
        blank=True,
        verbose_name="Версия",
    )
    developer = models.ForeignKey(
        Developer,
        on_delete=models.SET_NULL,
        related_name="changes",
        null=True,
        blank=True,
        verbose_name="Разработчик",
    )

    class Meta:
        ordering = ["-date", "-pk"]
        verbose_name = "Изменение"
        verbose_name_plural = "Изменения"

    def __str__(self) -> str:
        return f"[{self.get_type_display()}] {self.description}"

    def format_entry(self) -> str:
        return (
            f"[{self.get_type_display()}] {self.description} "
            f"(автор: {self.author})"
        )

    def is_added(self) -> bool:
        return self.type == self.ADDED

    def is_fixed(self) -> bool:
        return self.type == self.FIXED

    def is_removed(self) -> bool:
        return self.type == self.REMOVED
