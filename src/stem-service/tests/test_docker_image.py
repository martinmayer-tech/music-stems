"""REQ-001: the Dockerfile builds one image with Python 3.12, FFmpeg, and the service."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _dockerfile() -> str:
    return (ROOT / "Dockerfile").read_text(encoding="utf-8")


def test_req_001_ac_1_base_image_and_ffmpeg():
    text = _dockerfile()
    assert re.search(r"^FROM python:3\.12-slim\b", text, re.MULTILINE)
    assert re.search(r"apt-get install\b[^\n]*\bffmpeg\b", text.replace("\\\n", " "))


def test_req_001_ac_2_extra_is_a_build_argument():
    text = _dockerfile()
    assert re.search(r"^ARG STEMS_EXTRA=cpu\s*$", text, re.MULTILINE)
    assert "audio-separator[${STEMS_EXTRA}]" in text


def test_req_001_ac_3_pin_matches_pyproject():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    pinned = re.search(r"audio-separator\[cpu\]==([0-9][^\"]*)\"", pyproject)
    argument = re.search(r"^ARG AUDIO_SEPARATOR_VERSION=(\S+)\s*$", _dockerfile(), re.MULTILINE)
    assert pinned and argument
    assert argument.group(1) == pinned.group(1)


def test_req_001_runtime_settings():
    text = _dockerfile()
    assert "STEMS_HOST=0.0.0.0" in text
    assert "STEMS_DATA_DIR=/data" in text
    assert "STEMS_MODEL_DIR=/models" in text
    assert "EXPOSE 8000" in text
    assert re.search(r"^USER \S+", text, re.MULTILINE)
    assert re.search(r"^HEALTHCHECK\b", text, re.MULTILINE)
    assert 'CMD ["python", "-m", "stem_service"]' in text


def test_req_001_dockerignore_keeps_noise_out():
    names = (ROOT / ".dockerignore").read_text(encoding="utf-8").split()
    for name in (".git", "plan", "data"):
        assert name in names


def test_req_001_compiler_builds_and_leaves_in_one_layer():
    text = _dockerfile().replace("\\\n", " ")
    layer = next(line for line in text.splitlines() if "pip install" in line)
    assert "apt-get install -y --no-install-recommends gcc libc6-dev" in layer
    assert "apt-get purge -y --auto-remove gcc libc6-dev" in layer


def test_req_001_ac_2_layer_installs_audioread():
    text = _dockerfile().replace("\\\n", " ")
    layer = next(line for line in text.splitlines() if "pip install" in line)
    assert '"audioread==${AUDIOREAD_VERSION}"' in layer


def test_req_001_ac_3_audioread_pin_matches_pyproject():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    pinned = re.search(r'"audioread==([0-9][^"]*)"', pyproject)
    argument = re.search(r"^ARG AUDIOREAD_VERSION=(\S+)\s*$", _dockerfile(), re.MULTILINE)
    assert pinned and argument
    assert argument.group(1) == pinned.group(1)
