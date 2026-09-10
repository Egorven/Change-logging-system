import json
from datetime import date

# Данные
project = "ChangeLog Tracker"
version = "1.0.0"
changes = [
    {"type": "fixed", "description": "Исправлена ошибка при сохранении", "author": "Иван Петров", "date": "2026-09-10"},
    {"type": "added", "description": "Добавлен экспорт в JSON", "author": "Мария Ивановна", "date": "2026-09-09"},
    {"type": "fixed", "description": "Исправлен баг в авторизации", "author": "Иван Петров", "date": "2026-09-08"},
]

# Функция 1. Форматирование записи об изменении
def format_entry(change):
    labels = {"added": "Добавлено", "fixed": "Исправлено", "removed": "Удалено"}
    label = labels.get(change["type"], "Изменено")
    return f"[{label}] {change['description']} (автор: {change['author']})"

# Функция 2. Фильтрация изменений по категории
def filter_by_type(changes, target_type):
    return [c for c in changes if c["type"] == target_type]

# Функция 3. Экспорт в JSON
def to_json(project, version, changes):
    data = {
        "project": project,
        "version": version,
        "changes": changes
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


print("Фильтрация по категории 'fixed'")
fixed_changes = filter_by_type(changes, "fixed")
for c in fixed_changes:
    print(" -", format_entry(c))

print("\nЭкспорт в JSON ")
print(to_json(project, version, changes))