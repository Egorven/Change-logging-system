"""Пользовательские формы журнала изменений."""

from datetime import date
from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError

from changes.models import Change, Developer
from projects.models import Project


class ChangeFilterForm(forms.Form):
    """Проверяет GET-параметры фильтрации журнала."""

    SORT_CHOICES = (
        ("date", "Дате"),
        ("project", "Проекту"),
        ("type", "Типу"),
    )

    q = forms.CharField(
        required=False,
        label="Поиск",
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "Описание или автор"}),
    )
    type = forms.ChoiceField(
        required=False,
        label="Тип",
        choices=(("", "Все типы"), *Change.TYPE_CHOICES),
    )
    project = forms.ModelChoiceField(
        required=False,
        label="Проект",
        queryset=Project.objects.order_by("name"),
        empty_label="Все проекты",
    )
    developer = forms.ModelChoiceField(
        required=False,
        label="Разработчик",
        queryset=Developer.objects.order_by("name"),
        empty_label="Все разработчики",
    )
    status = forms.ChoiceField(
        required=False,
        label="Статус",
        choices=(
            ("active", "Только активные"),
            ("all", "Все записи"),
            ("cancelled", "Только отменённые"),
        ),
        initial="active",
    )
    date_from = forms.DateField(
        required=False,
        label="Дата от",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    date_to = forms.DateField(
        required=False,
        label="Дата до",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    sort = forms.ChoiceField(
        required=False,
        label="Сортировать по",
        choices=SORT_CHOICES,
        initial="date",
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")
        if date_from and date_to and date_from > date_to:
            raise ValidationError(
                "Начальная дата не может быть позже конечной."
            )
        return cleaned_data


class ChangeForm(forms.ModelForm):
    """Создание и редактирование доступных пользователю полей изменения."""

    class Meta:
        model = Change
        fields = (
            "type",
            "description",
            "author",
            "date",
            "project",
            "version",
            "developer",
            "attachment",
        )
        labels = {
            "attachment": "Изображение или файл",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_date(self):
        change_date = self.cleaned_data["date"]
        if change_date > date.today():
            raise ValidationError("Дата изменения не может быть в будущем.")
        return change_date

    def clean_attachment(self):
        attachment = self.cleaned_data.get("attachment")
        if not attachment:
            return attachment
        if attachment.size > 5 * 1024 * 1024:
            raise ValidationError("Размер файла не должен превышать 5 МБ.")
        allowed = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf"}
        if Path(attachment.name).suffix.lower() not in allowed:
            raise ValidationError(
                "Разрешены изображения JPG, PNG, GIF, WEBP и файлы PDF."
            )
        return attachment

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get("project")
        version = cleaned_data.get("version")
        change_date = cleaned_data.get("date")

        if project and version and version.project_id != project.pk:
            self.add_error(
                "version", "Выбранная версия не относится к проекту."
            )

        if project and change_date:
            occupied = Change.objects.active().filter(
                project=project,
                version=version,
                date=change_date,
            )
            if self.instance.pk:
                occupied = occupied.exclude(pk=self.instance.pk)
            if occupied.exists():
                raise ValidationError(
                    "Для этого проекта, версии и даты уже есть "
                    "активная запись."
                )
        return cleaned_data
