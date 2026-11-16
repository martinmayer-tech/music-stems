"""Tests for the model options of the stems command (REQ-002)."""

import subprocess
import sys
from pathlib import Path

from stem_core import cli
from stem_core.separation import ENSEMBLE_PRESETS, PASS_TWO_MODELS, SINGLE_STEMS, split


def make_mix(tmp_path):
    path = tmp_path / "mix.wav"
    path.write_bytes(b"RIFF")
    return path


def test_req_002_the_flags_reach_split_as_keyword_arguments(tmp_path):
    calls = []

    def recording(mix_path, out_dir, full_stems=False, **options):
        calls.append(options)
        return []

    argv = [
        "split",
        str(make_mix(tmp_path)),
        "--model",
        "htdemucs_6s.yaml",
        "--ensemble-preset",
        "vocal_clean",
        "--single-stem",
        "guitar",
    ]
    assert cli.main(argv, split_func=recording) == 0
    assert calls == [
        {"model": "htdemucs_6s.yaml", "ensemble_preset": "vocal_clean", "single_stem": "guitar"}
    ]


def test_req_002_split_gets_no_option_keyword_when_no_flag_is_set(tmp_path):
    calls = []

    def recording(mix_path, out_dir, full_stems=False, **options):
        calls.append(options)
        return []

    cli.main(["split", str(make_mix(tmp_path))], split_func=recording)
    assert calls == [{}]


def test_req_002_a_bad_option_prints_one_error_line_and_exits_one(tmp_path, capsys):
    mix = make_mix(tmp_path)
    code = cli.main(["split", str(mix), "--model", "evil.ckpt"], split_func=split)
    err = capsys.readouterr().err
    assert code == 1
    assert len(err.splitlines()) == 1
    assert err.startswith("stems: error:") and "evil.ckpt" in err


def test_req_002_models_lists_every_allowed_value():
    result = subprocess.run(
        [sys.executable, "-c", "from stem_core import cli; cli.main(['models'])"],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(Path(__file__).resolve().parents[1])},
        check=True,
    )
    for value in (*PASS_TWO_MODELS, *ENSEMBLE_PRESETS, *SINGLE_STEMS):
        assert value in result.stdout
