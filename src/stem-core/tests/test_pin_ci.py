"""Checks the pinned separation extra and its CI install (REQ-003)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PYPROJECT = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
WORKFLOW = (ROOT / ".github" / "workflows" / "ravintio.yml").read_text(encoding="utf-8")


def python_job() -> str:
    start = WORKFLOW.index("\n  python:\n")
    rest = WORKFLOW[start + 1 :]
    end = rest.find("\n  # ", 1)
    return rest if end == -1 else rest[:end]


def test_req_003_separation_extra_pins_audio_separator_exactly():
    match = re.search(r'separation\s*=\s*\[\s*"(audio-separator\[cpu\])==([0-9][^"]*)"', PYPROJECT)
    assert match, "the separation extra must pin audio-separator[cpu] with =="


def test_req_003_ci_installs_the_separation_extra():
    job = python_job()
    assert "separation" in job
    assert ".[dev,service,separation]" in job


def test_req_003_pytest_settings_register_the_slow_marker():
    assert "slow:" in PYPROJECT


def test_req_003_default_pytest_run_excludes_the_slow_marker():
    assert 'addopts = "--import-mode=importlib -m \'not slow\'"' in PYPROJECT
