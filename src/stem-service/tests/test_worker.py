"""Tests for the worker and the model pool (REQ-002, REQ-003, REQ-004)."""

import threading
import time
from pathlib import Path

import pytest
from stem_core.separation import FULL_STEMS_MODEL, VOCALS_MODEL
from stem_service.jobs import JobStore
from stem_service.worker import ModelPool, Worker, start_workers

TIMEOUT = 10


def wait_for(condition, timeout=TIMEOUT):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if condition():
            return True
        time.sleep(0.01)
    return False


def all_finished(store):
    jobs = store.list()
    return bool(jobs) and all(j.status in ("done", "failed") for j in jobs)


class CountingFake:
    """A separator that writes real files and counts model loads for the whole test."""

    loads: list[str] = []
    created: list["CountingFake"] = []

    def __init__(self, output_dir, output_format, model_file_dir):
        self.output_dir = output_dir
        self.model = None
        CountingFake.created.append(self)

    def load_model(self, model_filename):
        CountingFake.loads.append(model_filename)
        self.model = model_filename

    def separate(self, path, names=None):
        stems = (
            ["Vocals", "Instrumental"]
            if self.model == VOCALS_MODEL
            else [
                "Drums",
                "Bass",
                "Other",
                "Vocals",
            ]
        )
        files = []
        for stem in stems:
            name = (names or {})[stem]
            target = Path(self.output_dir) / f"{name}.wav"
            target.write_text(stem)
            files.append(str(target))
        return files


@pytest.fixture(autouse=True)
def reset_fake():
    CountingFake.loads = []
    CountingFake.created = []


@pytest.fixture
def setup(tmp_path):
    store = JobStore(tmp_path / "data" / "jobs.sqlite3")
    mix = tmp_path / "mix.wav"
    mix.write_text("audio")
    return store, tmp_path / "data", mix


def test_req_003_jobs_run_in_turn_and_never_overlap(setup):
    store, data_dir, mix = setup
    intervals = []
    lock = threading.Lock()

    def slow_split(mix_path, out_dir, full_stems, factory):
        start = time.monotonic()
        time.sleep(0.05)
        with lock:
            intervals.append((start, time.monotonic()))
        return [str(Path(out_dir) / "vocals.wav")]

    first = store.add(mix)
    second = store.add(mix)
    worker = Worker(store, data_dir=data_dir, split_func=slow_split, poll_interval=0.01)
    worker.start()
    try:
        assert wait_for(lambda: all_finished(store))
    finally:
        worker.stop()
    intervals.sort()
    assert len(intervals) == 2
    assert intervals[0][1] <= intervals[1][0]
    assert store.get(first).status == "done"
    assert store.get(second).status == "done"
    assert store.get(first).outputs


def test_req_003_a_failed_job_does_not_stop_the_worker(setup):
    store, data_dir, mix = setup

    def flaky_split(mix_path, out_dir, full_stems, factory):
        if "bad" in str(mix_path):
            raise RuntimeError("model failed\nwith detail")
        return ["/out/a.wav"]

    bad = store.add("bad.wav")
    good = store.add(mix)
    worker = Worker(store, data_dir=data_dir, split_func=flaky_split, poll_interval=0.01)
    worker.start()
    try:
        assert wait_for(lambda: all_finished(store))
    finally:
        worker.stop()
    assert store.get(bad).status == "failed"
    assert store.get(bad).error == "model failed"
    assert store.get(good).status == "done"


def test_req_003_a_missing_input_fails_the_job_with_one_line(setup):
    store, data_dir, _ = setup
    job_id = store.add("/nowhere/missing.wav")
    worker = Worker(store, data_dir=data_dir, separator_factory=CountingFake, poll_interval=0.01)
    worker.start()
    try:
        assert wait_for(lambda: all_finished(store))
    finally:
        worker.stop()
    job = store.get(job_id)
    assert job.status == "failed"
    assert "missing.wav" in job.error
    assert "\n" not in job.error


def test_req_003_worker_picks_up_a_job_added_while_idle(setup):
    store, data_dir, mix = setup
    worker = Worker(store, data_dir=data_dir, separator_factory=CountingFake, poll_interval=0.01)
    worker.start()
    try:
        time.sleep(0.05)
        job_id = store.add(mix)
        worker.wake()
        assert wait_for(lambda: store.get(job_id).status == "done")
    finally:
        worker.stop()


def test_req_003_start_workers_starts_one_worker_for_each_device(setup):
    store, data_dir, _ = setup
    workers = start_workers(store, ["cuda:0", "cuda:1"], data_dir=data_dir, poll_interval=0.01)
    try:
        assert [w.name for w in workers] == ["cuda:0", "cuda:1"]
        assert all(w.is_running for w in workers)
    finally:
        for w in workers:
            w.stop()
    assert not any(w.is_running for w in workers)


def test_req_003_two_workers_never_run_one_job_twice(setup):
    store, data_dir, mix = setup
    runs = []
    lock = threading.Lock()

    def counting_split(mix_path, out_dir, full_stems, factory):
        with lock:
            runs.append(Path(out_dir).name)
        time.sleep(0.01)
        return ["/out/a.wav"]

    ids = [store.add(mix) for _ in range(6)]
    workers = start_workers(
        store, ["a", "b"], data_dir=data_dir, split_func=counting_split, poll_interval=0.01
    )
    try:
        assert wait_for(lambda: all_finished(store))
    finally:
        for w in workers:
            w.stop()
    assert sorted(runs) == sorted(ids)


def test_req_002_worker_start_runs_a_job_that_a_restart_interrupted(setup):
    store, data_dir, mix = setup
    job_id = store.add(mix)
    store.claim_next()
    assert store.get(job_id).status == "running"
    worker = Worker(store, data_dir=data_dir, separator_factory=CountingFake, poll_interval=0.01)
    worker.start()
    try:
        assert wait_for(lambda: store.get(job_id).status == "done")
    finally:
        worker.stop()


def test_req_004_second_job_loads_no_model_the_first_loaded(setup):
    store, data_dir, mix = setup
    first = store.add(mix)
    second = store.add(mix)
    worker = Worker(store, data_dir=data_dir, separator_factory=CountingFake, poll_interval=0.01)
    worker.start()
    try:
        assert wait_for(lambda: all_finished(store))
    finally:
        worker.stop()
    assert CountingFake.loads == [VOCALS_MODEL]
    assert store.get(first).status == "done"
    assert store.get(second).status == "done"


def test_req_004_each_job_writes_to_its_own_folder(setup):
    store, data_dir, mix = setup
    first = store.add(mix)
    second = store.add(mix)
    worker = Worker(store, data_dir=data_dir, separator_factory=CountingFake, poll_interval=0.01)
    worker.start()
    try:
        assert wait_for(lambda: all_finished(store))
    finally:
        worker.stop()
    for job_id in (first, second):
        outputs = store.get(job_id).outputs
        assert len(outputs) == 2
        assert all(Path(p).parent.name == job_id for p in outputs)
        assert all(Path(p).is_file() for p in outputs)


def test_req_004_two_passes_keep_both_models_loaded(setup):
    store, data_dir, mix = setup
    for _ in range(2):
        store.add(mix, full_stems=True)
    worker = Worker(store, data_dir=data_dir, separator_factory=CountingFake, poll_interval=0.01)
    worker.start()
    try:
        assert wait_for(lambda: all_finished(store))
    finally:
        worker.stop()
    assert sorted(CountingFake.loads) == sorted([VOCALS_MODEL, FULL_STEMS_MODEL])
    assert all(len(j.outputs) == 5 for j in store.list())


def test_req_004_pool_builds_one_separator_for_each_model():
    pool = ModelPool(CountingFake)
    one = pool.factory("/out/1", "WAV", "/models")
    one.load_model(model_filename=VOCALS_MODEL)
    two = pool.factory("/out/2", "WAV", "/models")
    two.load_model(model_filename=VOCALS_MODEL)
    assert CountingFake.loads == [VOCALS_MODEL]
    assert len(CountingFake.created) == 1
    assert CountingFake.created[0].output_dir == "/out/2"
