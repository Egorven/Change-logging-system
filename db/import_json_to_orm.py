"""Перенос исходных JSON-данных в таблицы Django ORM."""

import json
import os
import sys
from datetime import date
from pathlib import Path
from typing import Any

import django
from django.db import transaction
from django.utils.text import slugify

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "changelog.settings")
django.setup()

from changes.models import Change, Developer  # noqa: E402
from projects.models import Project, Version  # noqa: E402


def read_json(filename: str) -> list[dict[str, Any]]:
    with (DATA_DIR / filename).open(encoding="utf-8") as data_file:
        data = json.load(data_file)
    if not isinstance(data, list):
        raise ValueError(f"Файл {filename} должен содержать список")
    return data


def main() -> None:
    projects = read_json("project.json")
    developers = read_json("developer.json")
    versions = read_json("version.json")
    changes = read_json("changes.json")

    with transaction.atomic():
        for item in projects:
            Project.objects.update_or_create(
                pk=item["id"],
                defaults={
                    "name": item["name"],
                    "description": item.get("description", ""),
                    "slug": (
                        f"{slugify(item['name']) or 'project'}-{item['id']}"
                    ),
                },
            )
        for item in developers:
            Developer.objects.update_or_create(
                pk=item["id"],
                defaults={
                    "name": item["name"],
                    "role": item.get("role", ""),
                },
            )
        for item in versions:
            Version.objects.update_or_create(
                pk=item["id"],
                defaults={
                    "name": item["name"],
                    "release_date": date.fromisoformat(item["release_date"]),
                    "project_id": item["project_id"],
                },
            )
        for item in changes:
            Change.objects.update_or_create(
                pk=item["id"],
                defaults={
                    "type": item["type"],
                    "description": item["description"],
                    "author": item["author"],
                    "date": date.fromisoformat(item["date"]),
                    "project_id": item.get("project_id"),
                    "version_id": item.get("version_id"),
                    "developer_id": item.get("developer_id"),
                    "status": item.get("status", Change.ACTIVE),
                },
            )

    print("Перенос данных в Django ORM завершён.")
    print(f"Проектов: {Project.objects.count()}")
    print(f"Разработчиков: {Developer.objects.count()}")
    print(f"Версий: {Version.objects.count()}")
    print(f"Изменений: {Change.objects.count()}")


if __name__ == "__main__":
    main()
