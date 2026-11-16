"""Tests for the options that the worker passes to split() (REQ-003)."""

import time
from pathlib import Path

import pytest
from stem_core.separation import SIX_STEM_MODEL, VOCALS_MODEL
from stem_service.jobs import JobStore
from stem_service.worker import ModelPool, Worker

TIMEOUT = 10


def wait_for_finish(store):
    deadline = time.monotonic() + TIMEOUT
    while time.monotonic() < deadline:
        jobs = store.list()
        if jobs and all(j.status in ("done", "failed") for j in jobs):
            return
        time.sleep(0.01)
    raise AssertionError("the job did not finish")


class Recorder:
    """A separator that writes real files and records each build and load."""

    builds: list[tuple[str, str | None]] = []
    loads: list[str] = []

    def __init__(self, output_dir, output_format, model_file_dir, ensemble_preset=None):
        self.output_dir = output_dir
        self.preset = ensemble_preset
        self.model = None
        Recorder.builds.append((output_dir, ensemble_preset))

    def load_model(self, model_filename):
        Recorder.loads.append(model_filename)
        self.model = model_filename

    def separate(self, path, names=None):
        if self.model == VOCALS_MODEL:
            stems = ["Vocals", "Instrumental"]
        elif self.model == SIX_STEM_MODEL:
            stems = ["Drums", "Bass", "Other", "Vocals", "Guitar", "Piano"]
        else:
            stems = ["Drums", "Bass", "Other", "Vocals"]
        files = []
        for stem in stems:
            target = Path(self.output_dir) / f"{(names or {})[stem]}.wav"
            target.write_text(stem)
            files.append(str(target))
        return files


@pytest.fixture(autouse=True)
def reset():
    Recorder.builds = []
    Recorder.loads = []


@pytest.fixture
def setup(tmp_path):
    store = JobStore(tmp_path / "data" / "jobs.sqlite3")
    mix = tmp_path / "mix.wav"
    mix.write_text("audio")
    return store, tmp_path / "data", mix


def run(store, data_dir):
    worker = Worker(store, data_dir=data_dir, separator_factory=Recorder, poll_interval=0.01)
    worker.start()
    try:
        wait_for_finish(store)
    finally:
        worker.stop()


def test_req_003_the_worker_passes_the_stored_options_to_split(setup):
    store, data_dir, mix = setup
    seen = []

    def fake_split(mix_path, out_dir, full_stems, factory, **options):
        seen.append(options)
        return []

    store.add(mix, True, {"model": "htdemucs_6s.yaml", "single_stem": "guitar"})
    worker = Worker(store, data_dir=data_dir, split_func=fake_split, poll_interval=0.01)
    worker.start()
    try:
        wait_for_finish(store)
    finally:
        worker.stop()
    assert seen == [{"model": "htdemucs_6s.yaml", "single_stem": "guitar"}]


def test_req_003_a_six_stem_job_returns_guitar_and_piano(setup):
    store, data_dir, mix = setup
    job_id = store.add(mix, True, {"model": "htdemucs_6s.yaml"})
    run(store, data_dir)
    job = store.get(job_id)
    assert job.status == "done"
    assert [Path(p).stem for p in job.outputs][-2:] == ["guitar", "piano"]


def test_req_003_a_job_with_an_unlisted_model_fails_before_any_model_loads(setup):
    store, data_dir, mix = setup
    job_id = store.add(mix, True, {"model": "evil.ckpt"})
    run(store, data_dir)
    job = store.get(job_id)
    assert job.status == "failed"
    assert "evil.ckpt" in job.error
    assert Recorder.loads == [] and Recorder.builds == []


def test_req_003_the_pool_keeps_a_preset_separator_apart_from_a_plain_one(tmp_path):
    pool = ModelPool(Recorder)
    plain = pool.acquire(VOCALS_MODEL, str(tmp_path), "WAV", "models")
    preset = pool.acquire(VOCALS_MODEL, str(tmp_path), "WAV", "models", "vocal_clean")
    again = pool.acquire(VOCALS_MODEL, str(tmp_path), "WAV", "models", "vocal_clean")
    assert plain is not preset
    assert preset is again
    assert plain.preset is None and preset.preset == "vocal_clean"
