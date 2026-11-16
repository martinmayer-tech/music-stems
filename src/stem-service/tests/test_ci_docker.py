"""REQ-003: the CI workflow builds the CPU image and publishes nothing."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _job() -> str:
    text = (ROOT / ".github" / "workflows" / "ravintio.yml").read_text(encoding="utf-8")
    match = re.search(r"^  docker:\n(.*?)(?=^  \S|\Z)", text, re.MULTILINE | re.DOTALL)
    assert match, "the workflow has no docker job"
    return match.group(1)


def test_req_003_ac_1_builds_the_cpu_image():
    job = _job()
    assert "github.event_name == 'pull_request'" in job
    assert re.search(r"docker build\b[^\n]*--build-arg STEMS_EXTRA=cpu", job)
    assert "contents: read" in job
    assert "persist-credentials: false" in job


def test_req_003_ac_2_pushes_and_runs_nothing():
    job = _job()
    assert "docker push" not in job
    assert "docker run" not in job
    assert "packages: write" not in job
