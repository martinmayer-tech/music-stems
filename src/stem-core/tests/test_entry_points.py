"""Tests for the stems console script and python -m stem_core (REQ-001)."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PYPROJECT = (ROOT / "pyproject.toml").read_text(encoding="utf-8")


def test_req_001_pyproject_maps_stems_to_the_cli_main():
    assert re.search(r'\[project\.scripts\][^\[]*stems\s*=\s*"stem_core\.cli:main"', PYPROJECT)


def test_req_001_pyproject_packages_stem_core_from_its_component_folder():
    assert re.search(r'packages\s*=\s*\["stem_core"\]', PYPROJECT)
    assert re.search(r'package-dir\s*=\s*\{\s*""\s*=\s*"src/stem-core"\s*\}', PYPROJECT)
    assert (ROOT / "src" / "stem-core" / "stem_core" / "cli.py").is_file()


def test_req_001_the_separation_extra_stays_pinned():
    assert re.search(r'separation\s*=\s*\[\s*"audio-separator\[cpu\]==[0-9]', PYPROJECT)


def test_req_001_python_dash_m_exits_non_zero_with_one_error_line(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "stem_core", "split", str(tmp_path / "missing.wav")],
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src" / "stem-core")},
        check=False,
    )
    assert result.returncode != 0
    assert result.stdout == ""
    assert len(result.stderr.splitlines()) == 1
