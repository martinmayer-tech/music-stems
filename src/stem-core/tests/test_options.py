"""Tests for the model options of split() (REQ-001)."""

from pathlib import Path

import pytest
from stem_core import split
from stem_core.separation import (
    ENSEMBLE_PRESETS,
    FULL_STEMS_MODEL,
    PASS_TWO_MODELS,
    SINGLE_STEMS,
    SIX_STEM_MODEL,
    VOCALS_MODEL,
    validate_options,
)

SIX_STEMS = ["Drums", "Bass", "Other", "Vocals", "Guitar", "Piano"]
FOUR_STEMS = ["Drums", "Bass", "Other", "Vocals"]


class FakeSeparator:
    """Writes real files. Records the preset, the models, and every load."""

    instances: list["FakeSeparator"] = []

    def __init__(self, output_dir, output_format, model_file_dir, ensemble_preset=None):
        self.output_dir = Path(output_dir)
        self.ensemble_preset = ensemble_preset
        self.models: list[str] = []
        FakeSeparator.instances.append(self)

    def load_model(self, model_filename):
        self.models.append(model_filename)

    def separate(self, path, names=None):
        if self.models[-1] == VOCALS_MODEL:
            stems = ["Vocals", "Instrumental"]
        elif self.models[-1] == SIX_STEM_MODEL:
            stems = SIX_STEMS
        else:
            stems = FOUR_STEMS
        files = []
        for stem in stems:
            name = (names or {}).get(stem, f"{Path(path).stem}_({stem})")
            (self.output_dir / f"{name}.wav").write_text(stem)
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


def stems_of(paths):
    return [Path(p).stem for p in paths]


def test_req_001_allowlists_hold_the_listed_values():
    assert PASS_TWO_MODELS == ("htdemucs_ft.yaml", "htdemucs_6s.yaml", "htdemucs.yaml")
    assert len(ENSEMBLE_PRESETS) == 9
    assert "vocal_balanced" in ENSEMBLE_PRESETS
    assert SINGLE_STEMS == ("vocals", "instrumental", "drums", "bass", "other", "guitar", "piano")


def test_req_001_the_six_stem_model_returns_guitar_and_piano(mix, tmp_path):
    result = split(
        mix, tmp_path / "out", True, FakeSeparator, model="htdemucs_6s.yaml"
    )
    assert stems_of(result) == [
        "vocals", "instrumental", "drums", "bass", "other", "guitar", "piano"
    ]
    assert all(Path(p).exists() for p in result)
    assert FakeSeparator.instances[0].models == [VOCALS_MODEL, "htdemucs_6s.yaml"]


def test_req_001_the_default_pass_two_model_stays_htdemucs_ft(mix, tmp_path):
    split(mix, tmp_path / "out", True, FakeSeparator)
    assert FakeSeparator.instances[0].models == [VOCALS_MODEL, FULL_STEMS_MODEL]


@pytest.mark.parametrize(
    "options",
    [
        {"model": "evil.ckpt"},
        {"ensemble_preset": "nope"},
        {"single_stem": "kazoo"},
        {"single_stem": "guitar"},
        {"single_stem": "piano", "model": "htdemucs.yaml"},
    ],
)
def test_req_001_a_bad_option_raises_before_any_separator_exists(mix, tmp_path, options):
    with pytest.raises(ValueError):
        split(mix, tmp_path / "out", True, FakeSeparator, **options)
    assert FakeSeparator.instances == []


def test_req_001_the_error_names_the_option_the_value_and_the_allowed_values():
    with pytest.raises(ValueError) as caught:
        validate_options(model="evil.ckpt")
    text = str(caught.value)
    assert "model" in text and "evil.ckpt" in text
    assert all(name in text for name in PASS_TWO_MODELS)
    assert "\n" not in text


def test_req_001_every_listed_value_validates():
    for model in PASS_TWO_MODELS:
        validate_options(model=model)
    for preset in ENSEMBLE_PRESETS:
        validate_options(ensemble_preset=preset)
    for stem in SINGLE_STEMS:
        validate_options(single_stem=stem, model=SIX_STEM_MODEL)


def test_req_001_a_preset_goes_to_pass_one_and_pass_two_gets_none(mix, tmp_path):
    split(
        mix, tmp_path / "out", True, FakeSeparator, ensemble_preset="vocal_balanced"
    )
    first, second = FakeSeparator.instances
    assert first.ensemble_preset == "vocal_balanced"
    assert first.models == [VOCALS_MODEL]
    assert second.ensemble_preset is None
    assert second.models == [FULL_STEMS_MODEL]


def test_req_001_no_preset_keeps_one_separator_and_the_three_argument_call(mix, tmp_path):
    calls = []

    def factory(output_dir, output_format, model_dir):
        calls.append((output_dir, output_format, model_dir))
        return FakeSeparator(output_dir, output_format, model_dir)

    split(mix, tmp_path / "out", True, factory)
    assert len(calls) == 1


def test_req_001_a_pass_one_single_stem_keeps_one_file_and_skips_pass_two(mix, tmp_path):
    result = split(mix, tmp_path / "out", True, FakeSeparator, single_stem="vocals")
    assert stems_of(result) == ["vocals"]
    assert FakeSeparator.instances[0].models == [VOCALS_MODEL]
    assert sorted(p.name for p in (tmp_path / "out").iterdir()) == ["vocals.wav"]


def test_req_001_a_pass_two_single_stem_implies_pass_two_and_keeps_one_file(mix, tmp_path):
    result = split(mix, tmp_path / "out", False, FakeSeparator, single_stem="drums")
    assert stems_of(result) == ["drums"]
    assert FakeSeparator.instances[0].models == [VOCALS_MODEL, FULL_STEMS_MODEL]
    assert sorted(p.name for p in (tmp_path / "out").iterdir()) == ["drums.wav"]


def test_req_001_a_six_stem_single_stem_returns_the_guitar_file(mix, tmp_path):
    result = split(
        mix, tmp_path / "out", False, FakeSeparator, model="htdemucs_6s.yaml", single_stem="guitar"
    )
    assert stems_of(result) == ["guitar"]
