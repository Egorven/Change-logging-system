from version import add_version, sort_versions


def test_add_version() -> None:
    versions = []
    version = add_version(versions, 1, "1.0.0", "2026-09-10")
    assert version["id"] == 1
    assert version["project_id"] == 1


def test_sort_versions() -> None:
    versions = [
        {
            "id": 1, "project_id": 1,
            "name": "1.0.0", "release_date": "2026-09-10",
        },
        {
            "id": 2, "project_id": 1,
            "name": "1.1.0", "release_date": "2026-10-10",
        },
    ]
    assert sort_versions(versions) == versions
