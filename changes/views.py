"""View-функции приложения changes."""

from django.shortcuts import render

from db.database import get_connection

BADGES = {
    "added": "bg-success",
    "fixed": "bg-warning",
    "removed": "bg-danger",
}
LABELS = {
    "added": "Добавлено",
    "fixed": "Исправлено",
    "removed": "Удалено",
}


def changes(request):
    """Список изменений с фильтрацией по параметрам пользователя."""
    change_type = request.GET.get("type", "")
    search_text = request.GET.get("q", "").strip()
    project_id = request.GET.get("project", "").strip()
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()
    conditions = []
    parameters = []
    if change_type in LABELS:
        conditions.append("c.type = ?")
        parameters.append(change_type)
    if search_text:
        conditions.append(
            "(c.description LIKE ? OR c.author LIKE ?)"
        )
        search_pattern = f"%{search_text}%"
        parameters.extend((search_pattern, search_pattern))
    if project_id.isdigit():
        conditions.append("c.project_id = ?")
        parameters.append(int(project_id))
    if date_from:
        conditions.append("c.change_date >= ?")
        parameters.append(date_from)
    if date_to:
        conditions.append("c.change_date <= ?")
        parameters.append(date_to)
    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    with get_connection() as connection:
        changes_list = connection.execute(
            f"""SELECT c.id, c.type, c.description, c.author,
                       c.change_date AS date, p.name AS project_name
                FROM changes AS c
                LEFT JOIN projects AS p ON p.id = c.project_id
                {where_clause}
                ORDER BY c.change_date DESC""",
            parameters,
        ).fetchall()
        statistics_rows = connection.execute(
            """SELECT type, COUNT(*) AS count
               FROM changes
               GROUP BY type
               ORDER BY type"""
        ).fetchall()
        project_options = connection.execute(
            "SELECT id, name FROM projects ORDER BY name"
        ).fetchall()
    statistics = [
        {"label": LABELS.get(row["type"], "Изменено"), "count": row["count"]}
        for row in statistics_rows
    ]
    context = {
        "changes": changes_list,
        "badges": BADGES,
        "labels": LABELS,
        "statistics": statistics,
        "selected_type": change_type,
        "search_text": search_text,
        "selected_project": project_id,
        "project_options": project_options,
        "date_from": date_from,
        "date_to": date_to,
    }
    return render(request, "changes/change_list.html", context)


def change_detail(request, change_id):
    """Страница одного изменения."""
    with get_connection() as connection:
        change = connection.execute(
            """SELECT c.id, c.type, c.description, c.author,
                      c.change_date AS date,
                      COALESCE(d.name, c.author) AS developer_name,
                      p.name AS project_name,
                      v.name AS version_name
               FROM changes AS c
               LEFT JOIN developers AS d ON d.id = c.developer_id
               LEFT JOIN projects AS p ON p.id = c.project_id
               LEFT JOIN versions AS v ON v.id = c.version_id
               WHERE c.id = ?""",
            (change_id,),
        ).fetchone()

    if change is None:
        return render(
            request,
            "changes/change_detail.html",
            {"change": None},
            status=404,
        )

    context = {
        "change": change,
        "author": change["developer_name"],
        "project_name": change["project_name"] or "—",
        "version_name": change["version_name"] or "—",
        "badge": BADGES.get(change["type"], "bg-secondary"),
        "label": LABELS.get(change["type"], "Изменено"),
    }
    return render(request, "changes/change_detail.html", context)
