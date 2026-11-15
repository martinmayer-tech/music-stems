"""Tests for split() with an injected fake separator (REQ-001, REQ-002)."""

from pathlib import Path

import pytest
from stem_core import split
from stem_core.separation import (
    DEFAULT_MODEL_DIR,
    FULL_STEMS_MODEL,
    VOCALS_MODEL,
    resolve_model_dir,
)


class FakeSeparator:
    """Writes real files, returns bare file names like audio-separator does."""

    instances: list["FakeSeparator"] = []

    def __init__(self, output_dir, output_format, model_file_dir):
        self.output_dir = Path(output_dir)
        self.output_format = output_format
        self.model_file_dir = model_file_dir
        self.models: list[str] = []
        self.inputs: list[str] = []
        FakeSeparator.instances.append(self)

    def load_model(self, model_filename):
        self.models.append(model_filename)

    def separate(self, path, names=None):
        self.inputs.append(str(path))
        pass_number = len(self.models)
        if pass_number == 1:
            stems = ["Vocals", "Instrumental"]
        else:
            stems = ["Drums", "Bass", "Other", "Vocals"]
        files = []
        for stem in stems:
            name = (names or {}).get(stem, f"{Path(path).stem}_({stem})")
            (self.output_dir / f"{name}.wav").write_text(f"pass{pass_number}:{stem}")
            files.append(f"{name}.wav")
        return files


@pytest.fixture(autouse=True)
def reset_fake():
    FakeSeparator.instances.clear()


@pytest.fixture
def mix(tmp_path):
    path = tmp_path / "mix.wav"
    path.write_bytes(b"RIFF")
    return path


def test_req_001_split_returns_two_existing_wav_paths(mix, tmp_path):
    result = split(mix, tmp_path / "out", separator_factory=FakeSeparator)
    assert len(result) == 2
    assert all(p.endswith(".wav") and Path(p).exists() for p in result)


def test_req_001_split_returns_absolute_paths(mix, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = split(str(mix), "out", separator_factory=FakeSeparator)
    out = (tmp_path / "out").resolve()
    assert all(Path(p).is_absolute() and Path(p).parent == out for p in result)


def test_req_001_split_runs_pass_one_with_wav_and_the_roformer_model(mix, tmp_path):
    split(mix, tmp_path / "out", separator_factory=FakeSeparator)
    fake = FakeSeparator.instances[0]
    assert fake.models == [VOCALS_MODEL]
    assert fake.output_format == "WAV"


def test_req_001_missing_mix_raises_before_any_model_loads(tmp_path):
    with pytest.raises(FileNotFoundError):
        split(tmp_path / "none.wav", tmp_path / "out", separator_factory=FakeSeparator)
    assert FakeSeparator.instances == []


def test_req_001_model_dir_comes_from_the_environment(mix, tmp_path, monkeypatch):
    monkeypatch.setenv("STEMS_MODEL_DIR", str(tmp_path / "models"))
    split(mix, tmp_path / "out", separator_factory=FakeSeparator)
    assert FakeSeparator.instances[0].model_file_dir == str(tmp_path / "models")


def test_req_001_model_dir_defaults_when_the_variable_is_unset(monkeypatch):
    monkeypatch.delenv("STEMS_MODEL_DIR", raising=False)
    assert resolve_model_dir() == DEFAULT_MODEL_DIR


def test_req_002_full_stems_returns_five_absolute_paths(mix, tmp_path):
    result = split(mix, tmp_path / "out", full_stems=True, separator_factory=FakeSeparator)
    assert len(result) == 5
    assert all(Path(p).is_absolute() and Path(p).exists() for p in result)
    names = [Path(p).name for p in result]
    assert names == ["vocals.wav", "instrumental.wav", "drums.wav", "bass.wav", "other.wav"]


def test_req_002_pass_one_vocals_file_survives_pass_two(mix, tmp_path):
    result = split(mix, tmp_path / "out", full_stems=True, separator_factory=FakeSeparator)
    assert Path(result[0]).read_text() == "pass1:Vocals"


def test_req_002_pass_two_reads_the_pass_one_instrumental(mix, tmp_path):
    result = split(mix, tmp_path / "out", full_stems=True, separator_factory=FakeSeparator)
    fake = FakeSeparator.instances[0]
    assert fake.models == [VOCALS_MODEL, FULL_STEMS_MODEL]
    assert fake.inputs[1] == result[1]


def test_req_002_residual_vocals_file_is_removed(mix, tmp_path):
    split(mix, tmp_path / "out", full_stems=True, separator_factory=FakeSeparator)
    assert not (tmp_path / "out" / "residual_vocals.wav").exists()
