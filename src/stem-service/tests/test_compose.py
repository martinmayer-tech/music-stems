"""REQ-002: compose.yaml runs the stack on loopback with two named volumes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _compose() -> str:
    return (ROOT / "compose.yaml").read_text(encoding="utf-8")


def test_req_002_ac_1_publishes_on_loopback_only():
    ports = re.findall(r"^\s*-\s*[\"']?([^\"'\s]+:\d+)[\"']?\s*$", _compose(), re.MULTILINE)
    assert ports
    assert all(port.startswith("127.0.0.1:") for port in ports)
    assert "${STEMS_PORT:-8000}:8000" in _compose()


def test_req_002_ac_2_mounts_both_volumes():
    text = _compose()
    assert re.search(r"^\s*-\s*models:/models\s*$", text, re.MULTILINE)
    assert re.search(r"^\s*-\s*data:/data\s*$", text, re.MULTILINE)
    top = text.split("\nvolumes:\n")[-1]
    assert re.search(r"^\s+models:", top, re.MULTILINE)
    assert re.search(r"^\s+data:", top, re.MULTILINE)


def test_req_002_builds_the_image_and_restarts():
    text = _compose()
    assert "context: ." in text
    assert "STEMS_EXTRA: ${STEMS_EXTRA:-cpu}" in text
    assert "restart: unless-stopped" in text


def test_req_002_ac_3_gpu_override():
    text = (ROOT / "compose.gpu.yaml").read_text(encoding="utf-8")
    assert "STEMS_EXTRA: gpu" in text
    assert "driver: nvidia" in text
    assert "capabilities: [gpu]" in text
