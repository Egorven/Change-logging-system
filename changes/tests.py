from datetime import date, timedelta
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.test import TestCase
from django.urls import reverse

from changes.forms import ChangeFilterForm, ChangeForm
from changes.models import Change, Developer
from projects.models import Project, Version


class ChangeFormTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Тестовый проект")
        self.other_project = Project.objects.create(name="Другой проект")
        self.version = Version.objects.create(
            name="1.0", release_date=date(2026, 1, 1), project=self.project
        )
        self.other_version = Version.objects.create(
            name="2.0", release_date=date(2026, 1, 1),
            project=self.other_project,
        )
        self.developer = Developer.objects.create(name="Иван")
        self.data = {
            "type": Change.ADDED,
            "description": "Новая функция",
            "author": "Иван",
            "date": "2026-01-02",
            "project": self.project.pk,
            "version": self.version.pk,
            "developer": self.developer.pk,
        }

    def test_filter_form_rejects_bad_range_and_bad_values(self):
        form = ChangeFilterForm({
            "date_from": "2026-02-02", "date_to": "2026-01-01",
            "project": "not-a-number", "sort": "unsafe",
        })
        self.assertFalse(form.is_valid())

    def test_create_change(self):
        response = self.client.post(
            reverse("changes:change_create"), self.data
        )
        change = Change.objects.get()
        self.assertRedirects(response, reverse(
            "changes:change_detail", args=[change.pk]
        ))

    def test_future_date_and_foreign_version_are_rejected(self):
        data = {**self.data, "date": date.today() + timedelta(days=1)}
        data["version"] = self.other_version.pk
        form = ChangeForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)
        self.assertIn("version", form.errors)

    def test_cancelled_change_does_not_block_new_change(self):
        existing = Change.objects.create(
            type=Change.ADDED, description="Первая", author="Иван",
            date=date(2026, 1, 2), project=self.project,
            version=self.version, developer=self.developer,
        )
        self.assertFalse(ChangeForm(self.data).is_valid())
        existing.status = Change.CANCELLED
        existing.save(update_fields=["status"])
        self.assertTrue(ChangeForm(self.data).is_valid())
        self.assertFalse(
            Change.objects.active().filter(pk=existing.pk).exists()
        )

    def test_edit_excludes_current_change_from_availability_check(self):
        change = Change.objects.create(
            type=Change.ADDED, description="Первая", author="Иван",
            date=date(2026, 1, 2), project=self.project,
            version=self.version, developer=self.developer,
        )
        form = ChangeForm(self.data, instance=change)
        self.assertTrue(form.is_valid(), form.errors)

    def test_cancel_is_post_only_and_changes_status(self):
        change = Change.objects.create(
            type=Change.ADDED, description="Первая", author="Иван",
            date=date(2026, 1, 2), project=self.project,
            version=self.version,
        )
        url = reverse("changes:change_cancel", args=[change.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        self.client.post(url)
        change.refresh_from_db()
        self.assertEqual(change.status, Change.CANCELLED)

    def test_missing_change_returns_404(self):
        self.assertEqual(self.client.get(reverse(
            "changes:change_edit", args=[999999]
        )).status_code, 404)

    def test_csrf_is_required_for_cancel(self):
        change = Change.objects.create(
            type=Change.ADDED, description="Первая", author="Иван",
            date=date(2026, 1, 2), project=self.project,
        )
        csrf_client = self.client_class(enforce_csrf_checks=True)
        response = csrf_client.post(reverse(
            "changes:change_cancel", args=[change.pk]
        ))
        self.assertEqual(response.status_code, 403)

    def test_default_list_hides_cancelled_and_can_show_it(self):
        change = Change.objects.create(
            type=Change.ADDED, description="Отменённая запись",
            author="Иван", date=date(2026, 1, 2),
            project=self.project, status=Change.CANCELLED,
        )
        response = self.client.get(reverse("changes:changes"))
        self.assertNotContains(response, change.description)
        response = self.client.get(
            reverse("changes:changes"), {"status": "cancelled"}
        )
        self.assertContains(response, change.description)

    def test_filter_by_developer_and_pagination_keep_query(self):
        for day in range(1, 7):
            Change.objects.create(
                type=Change.ADDED, description=f"Запись {day}",
                author="Иван", date=date(2026, 2, day),
                project=self.project, developer=self.developer,
            )
        response = self.client.get(reverse("changes:changes"), {
            "developer": self.developer.pk,
            "sort": "project",
            "status": "active",
        })
        self.assertEqual(response.context["page_obj"].paginator.count, 6)
        self.assertContains(response, "developer=")
        self.assertContains(response, "sort=project")

    def test_file_upload_and_image_display(self):
        image = SimpleUploadedFile(
            "screen.png", b"fake-png-content", content_type="image/png"
        )
        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    reverse("changes:change_create"),
                    {**self.data, "attachment": image},
                )
                change = Change.objects.get()
                self.assertRedirects(response, reverse(
                    "changes:change_detail", args=[change.pk]
                ))
                detail = self.client.get(response.url)
                self.assertContains(detail, change.attachment.url)
                self.assertContains(detail, "<img", html=False)
