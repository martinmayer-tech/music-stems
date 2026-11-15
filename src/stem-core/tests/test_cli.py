"""Tests for the stems command with an injected fake separator and probes (REQ-001 to REQ-004)."""

import functools
import subprocess
import sys
from pathlib import Path

import pytest
from stem_core import cli
from stem_core.separation import FULL_STEMS_MODEL, VOCALS_MODEL, split


class FakeSeparator:
    """Writes real files and returns bare file names, like audio-separator."""

    def __init__(self, output_dir, output_format, model_file_dir):
        self.output_dir = Path(output_dir)
        self.models: list[str] = []

    def load_model(self, model_filename):
        self.models.append(model_filename)

    def separate(self, path, names=None):
        stems = (
            ["Vocals", "Instrumental"]
            if len(self.models) == 1
            else [
                "Drums",
                "Bass",
                "Other",
                "Vocals",
            ]
        )
        files = []
        for stem in stems:
            name = (names or {}).get(stem, f"{Path(path).stem}_({stem})")
            (self.output_dir / f"{name}.wav").write_text(stem)
            files.append(f"{name}.wav")
        return files


FAKE_SPLIT = functools.partial(split, separator_factory=FakeSeparator)


@pytest.fixture
def mix(tmp_path):
    path = tmp_path / "mix.wav"
    path.write_bytes(b"RIFF")
    return path


def test_req_001_split_prints_one_absolute_path_per_line_and_exits_zero(mix, tmp_path, capsys):
    out = tmp_path / "out"
    code = cli.main(["split", str(mix), "--output-dir", str(out)], split_func=FAKE_SPLIT)
    captured = capsys.readouterr()
    lines = captured.out.splitlines()
    assert code == 0
    assert len(lines) == 2
    assert all(Path(line).is_absolute() and Path(line).exists() for line in lines)
    assert captured.err == ""


def test_req_001_split_defaults_the_output_folder_to_stems_out(mix, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    code = cli.main(["split", str(mix)], split_func=FAKE_SPLIT)
    lines = capsys.readouterr().out.splitlines()
    assert code == 0
    assert all(Path(line).parent == (tmp_path / "stems-out").resolve() for line in lines)


def test_req_001_missing_input_prints_one_error_line_and_no_path(tmp_path, capsys):
    code = cli.main(["split", str(tmp_path / "missing.wav")], split_func=FAKE_SPLIT)
    captured = capsys.readouterr()
    assert code != 0
    assert captured.out == ""
    assert len(captured.err.splitlines()) == 1
    assert captured.err.startswith("stems: error:")


def test_req_001_a_split_failure_prints_one_error_line_and_no_traceback(mix, capsys):
    def failing(*args, **kwargs):
        raise RuntimeError("pass 1 wrote no vocals file")

    code = cli.main(["split", str(mix)], split_func=failing)
    captured = capsys.readouterr()
    assert code == 1
    assert captured.out == ""
    assert captured.err.splitlines() == ["stems: error: pass 1 wrote no vocals file"]


def test_req_001_a_missing_engine_names_the_separation_extra(mix, capsys):
    def no_engine(*args, **kwargs):
        raise ModuleNotFoundError("No module named 'audio_separator'")

    code = cli.main(["split", str(mix)], split_func=no_engine)
    err = capsys.readouterr().err
    assert code == 1
    assert len(err.splitlines()) == 1
    assert "separation" in err


def test_req_002_full_stems_flag_prints_five_paths(mix, tmp_path, capsys):
    code = cli.main(
        ["split", str(mix), "--output-dir", str(tmp_path / "o"), "--full-stems"],
        split_func=FAKE_SPLIT,
    )
    lines = capsys.readouterr().out.splitlines()
    assert code == 0
    stems = [Path(line).stem for line in lines]
    assert stems == ["vocals", "instrumental", "drums", "bass", "other"]


def test_req_002_without_the_flag_the_command_passes_full_stems_false(mix, capsys):
    calls = []

    def recording(mix_path, out_dir, full_stems=False):
        calls.append(full_stems)
        return []

    cli.main(["split", str(mix)], split_func=recording)
    cli.main(["split", str(mix), "--full-stems"], split_func=recording)
    assert calls == [False, True]


def test_req_003_env_prints_three_lines_from_the_probes(capsys):
    probes = cli.Probes(
        python=lambda: "3.12.1",
        ffmpeg=lambda: "ffmpeg version 7.0",
        device=lambda: "mps",
    )
    code = cli.main(["env"], probes=probes)
    assert code == 0
    assert capsys.readouterr().out.splitlines() == [
        "python: 3.12.1",
        "ffmpeg: ffmpeg version 7.0",
        "device: mps",
    ]


def test_req_003_env_reports_missing_tools_and_exits_zero(capsys):
    probes = cli.Probes(python=lambda: "3.13.0", ffmpeg=lambda: None, device=lambda: "cpu")
    code = cli.main(["env"], probes=probes)
    lines = capsys.readouterr().out.splitlines()
    assert code == 0
    assert "ffmpeg: not found" in lines
    assert "device: cpu" in lines


def test_req_003_the_device_probe_falls_back_to_cpu_when_torch_is_absent(monkeypatch):
    monkeypatch.setitem(sys.modules, "torch", None)
    assert cli.probe_device() == "cpu"


def test_req_003_the_ffmpeg_probe_returns_none_when_the_binary_is_absent(monkeypatch):
    monkeypatch.setattr(cli.shutil, "which", lambda name: None)
    assert cli.probe_ffmpeg() is None


def test_req_004_models_lists_both_models_and_exits_zero(capsys):
    code = cli.main(["models"])
    out = capsys.readouterr().out
    assert code == 0
    assert VOCALS_MODEL in out
    assert FULL_STEMS_MODEL in out
    assert len(out.splitlines()) == 2


def test_req_004_env_and_models_import_no_model_library():
    script = (
        "import sys\n"
        "from stem_core import cli\n"
        "cli.main(['models'])\n"
        "cli.main(['env'], probes=cli.Probes(lambda: 'x', lambda: None, lambda: 'cpu'))\n"
        "print('audio_separator' in sys.modules)\n"
    )
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(root)},
        check=True,
    )
    assert result.stdout.splitlines()[-1] == "False"
