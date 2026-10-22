-- ChangeLog Tracker: структура базы данных ПР7
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS developers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS versions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    release_date TEXT NOT NULL,
    project_id INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS changes (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL CHECK (type IN ('added', 'fixed', 'removed')),
    description TEXT NOT NULL,
    author TEXT NOT NULL,
    change_date TEXT NOT NULL,
    project_id INTEGER,
    version_id INTEGER,
    developer_id INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (version_id) REFERENCES versions(id) ON DELETE SET NULL,
    FOREIGN KEY (developer_id) REFERENCES developers(id) ON DELETE SET NULL
);
