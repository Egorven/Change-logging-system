"""ORM-модели проектов и версий проекта."""

from django.db import models
from django.db.models.functions import Length
from django.urls import reverse
from django.utils.text import slugify


class Project(models.Model):
    """Проект, для которого ведётся журнал изменений."""

    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Описание",
    )
    slug = models.SlugField(
        max_length=220,
        blank=True,
        editable=False,
        unique=True,
        verbose_name="URL-идентификатор",
    )
    name_length = models.GeneratedField(
        expression=Length("name"),
        output_field=models.PositiveIntegerField(),
        db_persist=True,
        verbose_name="Длина названия",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "project"
            self.slug = f"{base_slug}-{self.pk}" if self.pk else base_slug
            if not self.pk:
                super().save(*args, **kwargs)
                self.slug = f"{base_slug}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse(
            "projects:project_detail",
            kwargs={"slug": self.slug},
        )


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
