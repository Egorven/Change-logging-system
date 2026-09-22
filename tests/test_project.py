from project import add_project, delete_project


def test_add_project() -> None:
    projects = []
    project = add_project(projects, "Demo", "Описание")
    assert project["id"] == 1
    assert len(projects) == 1


def test_delete_project() -> None:
    projects = [{"id": 1, "name": "Demo"}]
    assert delete_project(projects, 1)
    assert projects == []


def test_delete_project_related_data() -> None:
    projects = [{"id": 1, "name": "Demo"}]
    versions = [
        {"id": 1, "project_id": 1, "name": "1.0.0"},
        {"id": 2, "project_id": 2, "name": "1.0.0"},
    ]
    changes = [
        {"id": 1, "project_id": 1, "version_id": 1},
        {"id": 2, "project_id": 2, "version_id": 2},
    ]
    project_versions = [
        item for item in versions if item["project_id"] == 1
    ]
    version_ids = {item["id"] for item in project_versions}

    assert delete_project(projects, 1)
    versions[:] = [item for item in versions if item["id"] not in version_ids]
    changes[:] = [
        item for item in changes
        if item.get("project_id") != 1
        and item.get("version_id") not in version_ids
    ]

    assert versions == [{"id": 2, "project_id": 2, "name": "1.0.0"}]
    assert changes == [{"id": 2, "project_id": 2, "version_id": 2}]
