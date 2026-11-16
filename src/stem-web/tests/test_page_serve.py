"""Tests for serving the page and its files (REQ-001)."""

from pathlib import Path

import pytest
import stem_web
from fastapi.testclient import TestClient
from stem_service.api import create_app


@pytest.fixture
def client(tmp_path):
    return TestClient(create_app(tmp_path / "data", run_workers=False))


def test_req_001_static_dir_names_the_page_folder():
    folder = stem_web.static_dir()
    assert isinstance(folder, Path)
    for name in ("index.html", "app.js", "style.css"):
        assert (folder / name).is_file()


def test_req_001_root_returns_the_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "/static/app.js" in response.text
    assert "/static/style.css" in response.text


def test_req_001_assets_are_served_as_they_sit_in_the_repo(client):
    folder = stem_web.static_dir()
    for name in ("app.js", "style.css"):
        response = client.get(f"/static/{name}")
        assert response.status_code == 200
        assert response.content == (folder / name).read_bytes()


@pytest.mark.parametrize(
    "path",
    ["/static/%2e%2e/__init__.py", "/static/..%2f__init__.py", "/static/missing.js"],
)
def test_req_001_refuses_a_path_outside_the_page_folder(client, path):
    response = client.get(path)
    assert response.status_code == 404
    assert b"__version__" not in response.content


def test_req_001_job_routes_still_answer(client):
    assert client.get("/jobs").json() == []
