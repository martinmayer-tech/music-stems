"""Tests for the service settings, the entry point, and an upload-to-download run (REQ-004)."""

import time
from pathlib import Path

import pytest
import uvicorn
from fastapi.testclient import TestClient
from stem_service import __main__ as entry
from stem_service.api import create_app
from stem_service.config import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    HOST_VARIABLE,
    MAX_UPLOAD_VARIABLE,
    PORT_VARIABLE,
    resolve_host,
    resolve_max_upload_bytes,
    resolve_port,
)

TIMEOUT = 10


def fake_split(mix_path, out_dir, full_stems, separator_factory):
    """Write real WAV-named files, as split() does, with no model."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    names = ["vocals", "instrumental"]
    if full_stems:
        names += ["drums", "bass", "other"]
    paths = []
    for name in names:
        path = out / f"{name}.wav"
        path.write_bytes(b"RIFF" + name.encode())
        paths.append(str(path))
    return paths


def wait_for_status(client, job_id, wanted):
    deadline = time.monotonic() + TIMEOUT
    while time.monotonic() < deadline:
        body = client.get(f"/jobs/{job_id}").json()
        if body["status"] in wanted:
            return body
        time.sleep(0.01)
    raise AssertionError(f"job {job_id} never reached {wanted}")


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    for name in (HOST_VARIABLE, PORT_VARIABLE, MAX_UPLOAD_VARIABLE):
        monkeypatch.delenv(name, raising=False)


def test_req_004_the_default_address_is_the_loopback_address():
    assert DEFAULT_HOST == "127.0.0.1"
    assert resolve_host() == "127.0.0.1"
    assert resolve_port() == DEFAULT_PORT == 8000


@pytest.mark.parametrize("value", ["", None])
def test_req_004_an_empty_setting_falls_back_to_the_default(monkeypatch, value):
    if value is not None:
        monkeypatch.setenv(HOST_VARIABLE, value)
        monkeypatch.setenv(PORT_VARIABLE, value)
    assert resolve_host() == "127.0.0.1"
    assert resolve_port() == 8000


def test_req_004_a_set_variable_overrides_each_default(monkeypatch):
    monkeypatch.setenv(HOST_VARIABLE, "0.0.0.0")
    monkeypatch.setenv(PORT_VARIABLE, "9100")
    assert resolve_host() == "0.0.0.0"
    assert resolve_port() == 9100


def test_req_004_the_upload_limit_defaults_to_500_megabytes(monkeypatch):
    assert resolve_max_upload_bytes() == 500 * 1024 * 1024
    monkeypatch.setenv(MAX_UPLOAD_VARIABLE, "2")
    assert resolve_max_upload_bytes() == 2 * 1024 * 1024


def test_req_004_the_app_creates_the_data_folder_the_database_and_uploads(tmp_path):
    data = tmp_path / "does" / "not" / "exist"
    create_app(data, run_workers=False)
    assert data.is_dir()
    assert (data / "jobs.sqlite3").is_file()
    assert (data / "uploads").is_dir()


def test_req_004_the_entry_point_runs_uvicorn_on_the_configured_address(monkeypatch, tmp_path):
    monkeypatch.setenv("STEMS_DATA_DIR", str(tmp_path / "data"))
    calls = []
    monkeypatch.setattr(uvicorn, "run", lambda app, **kwargs: calls.append((app, kwargs)))
    entry.main()
    [(app, kwargs)] = calls
    assert kwargs == {"host": "127.0.0.1", "port": 8000}
    assert app.title == "Stem service"


def test_req_004_the_app_adds_no_login(tmp_path):
    client = TestClient(create_app(tmp_path / "data", run_workers=False))
    assert client.get("/jobs").status_code == 200
    assert "WWW-Authenticate" not in client.get("/jobs").headers


@pytest.mark.parametrize("full_stems", [False, True])
def test_req_004_a_job_runs_from_upload_to_download(tmp_path, full_stems):
    app = create_app(
        tmp_path / "data",
        worker_options={"split_func": fake_split, "poll_interval": 0.01},
    )
    with TestClient(app) as client:
        response = client.post(
            "/jobs",
            files={"file": ("mix.wav", b"RIFF....WAVE", "audio/wav")},
            data={"full_stems": str(full_stems).lower()},
        )
        assert response.status_code == 201
        job = wait_for_status(client, response.json()["id"], {"done", "failed"})
        assert job["status"] == "done"
        assert len(job["stems"]) == (5 if full_stems else 2)
        for name in job["stems"]:
            stem = client.get(f"/jobs/{job['id']}/stems/{name}")
            assert stem.status_code == 200
            assert stem.headers["content-type"] == "audio/wav"
            assert stem.content.startswith(b"RIFF")


def test_req_004_a_failed_job_reports_its_error_over_http(tmp_path):
    def broken(*args, **kwargs):
        raise RuntimeError("The model failed.")

    app = create_app(
        tmp_path / "data", worker_options={"split_func": broken, "poll_interval": 0.01}
    )
    with TestClient(app) as client:
        job_id = client.post("/jobs", files={"file": ("mix.wav", b"RIFF", "audio/wav")}).json()[
            "id"
        ]
        job = wait_for_status(client, job_id, {"done", "failed"})
    assert job["status"] == "failed"
    assert job["error"] == "The model failed."


def test_req_004_the_app_stops_its_worker_at_shutdown(tmp_path):
    app = create_app(
        tmp_path / "data", worker_options={"split_func": fake_split, "poll_interval": 0.01}
    )
    with TestClient(app):
        [worker] = app.state.workers
        assert worker.is_running
    assert not worker.is_running
    assert app.state.workers == []
