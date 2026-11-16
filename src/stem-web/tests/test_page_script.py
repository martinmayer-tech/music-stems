"""Tests for the page markup and the script text (REQ-002, REQ-003, REQ-004)."""

import re

import pytest
from fastapi.testclient import TestClient
from stem_service.api import create_app


@pytest.fixture
def client(tmp_path):
    return TestClient(create_app(tmp_path / "data", run_workers=False))


@pytest.fixture
def page(client):
    return client.get("/").text


@pytest.fixture
def script(client):
    return client.get("/static/app.js").text


def test_req_002_page_holds_the_form_fields(page):
    assert re.search(r'<input[^>]*type="file"[^>]*name="file"', page)
    assert re.search(r'<input[^>]*type="checkbox"[^>]*name="full_stems"', page)
    assert re.search(r'<button[^>]*type="submit"', page)
    for extension in (".wav", ".flac", ".mp3", ".m4a"):
        assert extension in page


def test_req_002_script_posts_form_data_to_the_jobs_route(script):
    assert "new FormData" in script
    assert 'fetch("/jobs", { method: "POST"' in script
    assert "full_stems" in script


def test_req_002_script_shows_the_error_detail_with_text_content(script):
    assert ".detail" in script
    assert re.search(r"status\.textContent\s*=", script)


def test_req_003_page_holds_the_job_list_and_the_empty_text(page, script):
    assert 'id="jobs"' in page
    assert "No jobs yet." in script + page


def test_req_003_script_reads_the_job_list_and_polls_every_two_seconds(script):
    assert 'fetch("/jobs")' in script
    assert "POLL_MS = 2000" in script
    assert "setTimeout(refresh, POLL_MS)" in script
    assert '"queued"' in script
    assert '"running"' in script


def test_req_003_script_never_uses_inner_html(script):
    assert "innerHTML" not in script
    assert "outerHTML" not in script
    assert "insertAdjacentHTML" not in script
    assert "document.write" not in script
