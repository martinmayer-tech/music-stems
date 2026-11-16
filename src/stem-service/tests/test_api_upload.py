"""Tests for the upload route (REQ-001)."""

import pytest
from fastapi.testclient import TestClient
from stem_service.api import create_app


@pytest.fixture
def app(tmp_path):
    return create_app(tmp_path / "data", run_workers=False)


@pytest.fixture
def client(app):
    return TestClient(app)


def upload(client, name, content=b"RIFF....WAVE", **fields):
    return client.post("/jobs", files={"file": (name, content, "audio/wav")}, data=fields)


def uploaded_files(tmp_path):
    folder = tmp_path / "data" / "uploads"
    return [p for p in folder.rglob("*") if p.is_file()]


def test_req_001_accepts_a_wav_upload_and_queues_a_job(app, client, tmp_path):
    response = upload(client, "mix.wav", full_stems="true")
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "queued"
    job = app.state.store.get(body["id"])
    assert job is not None
    assert job.full_stems is True
    assert job.input_path.startswith(str(tmp_path / "data" / "uploads"))
    assert uploaded_files(tmp_path)[0].read_bytes() == b"RIFF....WAVE"


@pytest.mark.parametrize("name", ["a.wav", "a.FLAC", "a.Mp3", "a.m4a"])
def test_req_001_accepts_every_listed_extension_in_any_case(client, name):
    assert upload(client, name).status_code == 201


def test_req_001_full_stems_defaults_to_false(app, client):
    job_id = upload(client, "mix.wav").json()["id"]
    assert app.state.store.get(job_id).full_stems is False


def test_req_001_rejects_an_unlisted_extension(app, client, tmp_path):
    response = upload(client, "notes.txt")
    assert response.status_code == 415
    assert app.state.store.list() == []
    assert uploaded_files(tmp_path) == []


def test_req_001_rejects_a_missing_file_field(client):
    assert client.post("/jobs", data={"full_stems": "true"}).status_code == 422


def test_req_001_rejects_an_oversized_upload_and_leaves_nothing(tmp_path):
    app = create_app(tmp_path / "data", run_workers=False, max_upload_bytes=10)
    client = TestClient(app)
    response = upload(client, "mix.wav", content=b"x" * 11)
    assert response.status_code == 413
    assert app.state.store.list() == []
    assert uploaded_files(tmp_path) == []


def test_req_001_accepts_an_upload_at_the_limit(tmp_path):
    app = create_app(tmp_path / "data", run_workers=False, max_upload_bytes=10)
    client = TestClient(app)
    assert upload(client, "mix.wav", content=b"x" * 10).status_code == 201


def test_req_001_keeps_only_the_last_part_of_the_client_file_name(app, client, tmp_path):
    upload(client, "../../evil/..\\sneaky.wav")
    [stored] = uploaded_files(tmp_path)
    assert stored.name == "sneaky.wav"
    assert (tmp_path / "data" / "uploads") in stored.parents


def test_req_001_wakes_the_workers_after_a_valid_upload(app, client):
    class Probe:
        woken = 0

        def wake(self):
            Probe.woken += 1

    app.state.workers = [Probe()]
    upload(client, "mix.wav")
    assert Probe.woken == 1
