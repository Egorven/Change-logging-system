-- Запросы ПР7 для ChangeLog Tracker.

-- 1. Список проектов.
SELECT id, name, description
FROM projects
ORDER BY name;

-- 2. Последние версии.
SELECT id, name, release_date, project_id
FROM versions
ORDER BY release_date DESC
LIMIT 10;

-- 3. Поиск изменений заданного типа.
SELECT id, type, description, author, change_date
FROM changes
WHERE type = ?;

-- 4. Поиск изменений по фрагменту описания.
SELECT id, type, description, author, change_date
FROM changes
WHERE description LIKE ?;

-- 5. Изменения с проектом, версией и разработчиком.
SELECT c.id, c.type, c.description, c.change_date,
       p.name AS project_name, v.name AS version_name,
       COALESCE(d.name, c.author) AS developer_name
FROM changes AS c
JOIN projects AS p ON p.id = c.project_id
LEFT JOIN versions AS v ON v.id = c.version_id
LEFT JOIN developers AS d ON d.id = c.developer_id
ORDER BY c.change_date DESC;

-- 6. Версии с проектами.
SELECT v.name AS version_name, v.release_date, p.name AS project_name
FROM versions AS v
JOIN projects AS p ON p.id = v.project_id
ORDER BY v.release_date DESC;

-- 7. Общее число изменений.
SELECT COUNT(*) AS changes_count
FROM changes;

-- 8. Самая ранняя и самая поздняя дата изменения.
SELECT MIN(change_date) AS first_change, MAX(change_date) AS last_change
FROM changes;

-- 9. Количество изменений по типам.
SELECT type, COUNT(*) AS changes_count
FROM changes
GROUP BY type
ORDER BY changes_count DESC;

-- 10. Проекты с заданным минимальным количеством изменений.
SELECT p.name AS project_name, COUNT(c.id) AS changes_count
FROM projects AS p
LEFT JOIN changes AS c ON c.project_id = p.id
GROUP BY p.id, p.name
HAVING COUNT(c.id) >= ?;

-- 11. Поиск изменений по тексту, типу и диапазону дат.
SELECT c.id, c.type, c.description, c.author, c.change_date,
       p.name AS project_name
FROM changes AS c
LEFT JOIN projects AS p ON p.id = c.project_id
WHERE (c.description LIKE ? OR c.author LIKE ?)
  AND c.type = ?
  AND c.change_date BETWEEN ? AND ?
ORDER BY c.change_date DESC;

-- 12. Проекты с изменениями заданного типа за период.
SELECT p.name AS project_name, COUNT(c.id) AS changes_count
FROM projects AS p
JOIN changes AS c ON c.project_id = p.id
WHERE c.type = ?
  AND c.change_date >= ?
  AND c.change_date <= ?
GROUP BY p.id, p.name
HAVING COUNT(c.id) > ?;
