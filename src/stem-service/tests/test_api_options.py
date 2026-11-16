"""Tests for the model options on the upload route (REQ-003)."""

import pytest
from fastapi.testclient import TestClient
from stem_service.api import create_app


@pytest.fixture
def app(tmp_path):
    return create_app(tmp_path / "data", run_workers=False)


@pytest.fixture
def client(app):
    return TestClient(app)


def upload(client, **fields):
    return client.post(
        "/jobs", files={"file": ("mix.wav", b"RIFF....WAVE", "audio/wav")}, data=fields
    )


def test_req_003_a_listed_model_is_stored_in_the_job_options(app, client):
    response = upload(client, model="htdemucs_6s.yaml", full_stems="true")
    assert response.status_code == 201
    job = app.state.store.get(response.json()["id"])
    assert job.options == {"model": "htdemucs_6s.yaml"}


def test_req_003_every_option_is_stored_and_an_empty_value_counts_as_unset(app, client):
    response = upload(client, ensemble_preset="vocal_clean", single_stem="vocals", model="")
    job = app.state.store.get(response.json()["id"])
    assert job.options == {"ensemble_preset": "vocal_clean", "single_stem": "vocals"}


def test_req_003_a_job_with_no_option_stores_an_empty_object(app, client):
    job = app.state.store.get(upload(client).json()["id"])
    assert job.options == {}


@pytest.mark.parametrize(
    "fields, named",
    [
        ({"model": "evil.ckpt"}, "evil.ckpt"),
        ({"ensemble_preset": "nope"}, "nope"),
        ({"single_stem": "kazoo"}, "kazoo"),
        ({"single_stem": "guitar"}, "guitar"),
    ],
)
def test_req_003_a_bad_option_gets_422_and_leaves_no_job_or_file(
    app, client, tmp_path, fields, named
):
    response = upload(client, **fields)
    assert response.status_code == 422
    assert named in response.json()["detail"]
    assert app.state.store.list() == []
    uploads = tmp_path / "data" / "uploads"
    assert [p for p in uploads.rglob("*") if p.is_file()] == []
