"""Tests for the status routes and the stem download (REQ-002, REQ-003)."""

import pytest
from fastapi.testclient import TestClient
from stem_service.api import create_app


@pytest.fixture
def app(tmp_path):
    return create_app(tmp_path / "data", run_workers=False)


@pytest.fixture
def client(app):
    return TestClient(app)


def finished_job(app, tmp_path, names=("vocals.wav", "instrumental.wav")):
    folder = tmp_path / "out"
    folder.mkdir(exist_ok=True)
    paths = []
    for name in names:
        path = folder / name
        path.write_bytes(b"RIFF" + name.encode())
        paths.append(str(path))
    store = app.state.store
    job_id = store.add(tmp_path / "mix.wav")
    store.claim_next()
    store.mark_done(job_id, paths)
    return job_id


def test_req_002_reads_a_queued_job_with_no_server_path(app, client, tmp_path):
    job_id = app.state.store.add(tmp_path / "secret" / "mix.wav", full_stems=True)
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == job_id
    assert body["status"] == "queued"
    assert body["full_stems"] is True
    assert body["stems"] is None
    assert "secret" not in response.text
    assert str(tmp_path) not in response.text


def test_req_002_a_done_job_lists_stem_names_only(app, client, tmp_path):
    job_id = finished_job(app, tmp_path)
    body = client.get(f"/jobs/{job_id}").json()
    assert body["status"] == "done"
    assert body["stems"] == ["vocals.wav", "instrumental.wav"]
    assert str(tmp_path) not in client.get(f"/jobs/{job_id}").text


def test_req_002_a_failed_job_reports_its_error(app, client, tmp_path):
    store = app.state.store
    job_id = store.add(tmp_path / "mix.wav")
    store.claim_next()
    store.mark_failed(job_id, "The model failed.\nTraceback")
    body = client.get(f"/jobs/{job_id}").json()
    assert body["status"] == "failed"
    assert body["error"] == "The model failed."
    assert body["stems"] is None


def test_req_002_lists_jobs_oldest_first(app, client, tmp_path):
    first = app.state.store.add(tmp_path / "a.wav")
    second = app.state.store.add(tmp_path / "b.wav")
    listed = client.get("/jobs").json()
    assert [j["id"] for j in listed] == [first, second]


def test_req_002_an_empty_store_lists_no_jobs(client):
    assert client.get("/jobs").json() == []


def test_req_002_an_unknown_job_gets_404(client):
    assert client.get("/jobs/unknown").status_code == 404


def test_req_003_downloads_a_stem_as_wav(app, client, tmp_path):
    job_id = finished_job(app, tmp_path)
    response = client.get(f"/jobs/{job_id}/stems/vocals.wav")
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"
    assert response.content == b"RIFFvocals.wav"


# The client collapses a plain ".." in the URL, so the test sends it encoded.
@pytest.mark.parametrize("name", ["%2e%2e", "mix.wav", "other.wav", "..%2fmix.wav"])
def test_req_003_refuses_a_name_the_job_does_not_list(app, client, tmp_path, name):
    job_id = finished_job(app, tmp_path)
    (tmp_path / "mix.wav").write_bytes(b"private")
    response = client.get(f"/jobs/{job_id}/stems/{name}")
    assert response.status_code == 404
    assert b"private" not in response.content


def test_req_003_an_unknown_job_gets_404(client):
    assert client.get("/jobs/unknown/stems/vocals.wav").status_code == 404


def test_req_003_a_listed_stem_that_left_the_disk_gets_404(app, client, tmp_path):
    job_id = finished_job(app, tmp_path)
    (tmp_path / "out" / "vocals.wav").unlink()
    assert client.get(f"/jobs/{job_id}/stems/vocals.wav").status_code == 404


def test_req_003_an_unfinished_job_gets_409(app, client, tmp_path):
    job_id = app.state.store.add(tmp_path / "mix.wav")
    assert client.get(f"/jobs/{job_id}/stems/vocals.wav").status_code == 409
