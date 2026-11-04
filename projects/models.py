"""ORM-модели проектов и версий проекта."""

from django.db import models


class Project(models.Model):
    """Проект, для которого ведётся журнал изменений."""

    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Описание",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self) -> str:
        return self.name


class Version(models.Model):
    """Версия программного проекта."""

    name = models.CharField(max_length=100, verbose_name="Версия")
    release_date = models.DateField(verbose_name="Дата выпуска")
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="versions",
        verbose_name="Проект",
    )

    class Meta:
        ordering = ["-release_date", "pk"]
        verbose_name = "Версия"
        verbose_name_plural = "Версии"

    def __str__(self) -> str:
        return f"{self.project.name} {self.name}"
