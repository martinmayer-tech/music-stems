"""Tests for the job store (REQ-001, REQ-002)."""

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest
import stem_service
from stem_service.config import DATA_DIR_VARIABLE, DEFAULT_DATA_DIR, resolve_data_dir
from stem_service.jobs import JobStore


@pytest.fixture
def store(tmp_path):
    return JobStore(tmp_path / "data" / "jobs.sqlite3")


def test_req_001_data_dir_reads_the_variable(monkeypatch):
    monkeypatch.setenv(DATA_DIR_VARIABLE, "/somewhere")
    assert resolve_data_dir() == "/somewhere"


@pytest.mark.parametrize("value", [None, ""])
def test_req_001_data_dir_defaults(monkeypatch, value):
    monkeypatch.delenv(DATA_DIR_VARIABLE, raising=False)
    if value is not None:
        monkeypatch.setenv(DATA_DIR_VARIABLE, value)
    assert resolve_data_dir() == DEFAULT_DATA_DIR


def test_req_001_store_creates_folder_file_and_table(tmp_path):
    path = tmp_path / "new" / "folder" / "jobs.sqlite3"
    JobStore(path)
    assert path.is_file()
    with sqlite3.connect(path) as conn:
        names = [r[0] for r in conn.execute("select name from sqlite_master where type='table'")]
    assert "jobs" in names


def test_req_001_add_then_get_returns_a_queued_job(store):
    job_id = store.add("/in/mix.wav", full_stems=True, options={"a": 1})
    job = store.get(job_id)
    assert job.id == job_id
    assert job.status == "queued"
    assert job.input_path == "/in/mix.wav"
    assert job.full_stems is True
    assert job.options == {"a": 1}
    assert job.created_at
    assert job.started_at is None
    assert job.outputs is None


def test_req_001_get_unknown_id_returns_none(store):
    assert store.get("missing") is None


def test_req_001_list_keeps_creation_order(store):
    ids = [store.add(f"/in/{n}.wav") for n in range(3)]
    assert [j.id for j in store.list()] == ids


def test_req_001_claim_next_takes_the_oldest_queued_job(store):
    first = store.add("/in/a.wav")
    second = store.add("/in/b.wav")
    one = store.claim_next()
    two = store.claim_next()
    assert (one.id, one.status) == (first, "running")
    assert one.started_at
    assert two.id == second
    assert store.claim_next() is None


def test_req_001_mark_done_stores_outputs(store):
    job_id = store.add("/in/a.wav")
    store.claim_next()
    store.mark_done(job_id, ["/out/v.wav", "/out/i.wav"])
    job = store.get(job_id)
    assert job.status == "done"
    assert job.outputs == ["/out/v.wav", "/out/i.wav"]
    assert job.finished_at


def test_req_001_mark_failed_stores_one_error_line(store):
    job_id = store.add("/in/a.wav")
    store.claim_next()
    store.mark_failed(job_id, "boom\nsecond line")
    job = store.get(job_id)
    assert job.status == "failed"
    assert job.error == "boom"
    assert job.finished_at


def test_req_001_rejects_an_unknown_status_in_the_table(store):
    with sqlite3.connect(store.path) as conn, pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "insert into jobs (id, status, input_path, created_at) values ('x', 'bad', 'p', 't')"
        )


def test_req_002_jobs_persist_across_a_new_store(tmp_path):
    path = tmp_path / "jobs.sqlite3"
    first = JobStore(path)
    queued = first.add("/in/a.wav")
    done = first.add("/in/b.wav")
    first.claim_next()
    first.mark_done(queued, ["/out/a.wav"])
    reopened = JobStore(path)
    assert reopened.get(queued).status == "done"
    assert reopened.get(queued).outputs == ["/out/a.wav"]
    assert reopened.get(done).status == "queued"


def test_req_002_recover_requeues_a_running_job(store):
    job_id = store.add("/in/a.wav")
    store.claim_next()
    assert store.recover() == 1
    job = store.get(job_id)
    assert job.status == "queued"
    assert job.started_at is None
    assert store.recover() == 0


def test_req_002_recover_leaves_finished_jobs_alone(store):
    job_id = store.add("/in/a.wav")
    store.claim_next()
    store.mark_failed(job_id, "x")
    assert store.recover() == 0
    assert store.get(job_id).status == "failed"


def test_req_004_import_loads_no_model_library():
    package_root = Path(stem_service.__file__).resolve().parent.parent
    env = {**os.environ, "PYTHONPATH": str(package_root)}
    code = (
        "import sys, stem_service, stem_service.jobs, stem_service.config; "
        "print('audio_separator' in sys.modules)"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True, env=env
    )
    assert result.stdout.strip() == "False"
