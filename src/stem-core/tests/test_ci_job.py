"""Checks the `python` job in the CI workflow (REQ-002)."""

from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[3] / ".github" / "workflows" / "ravintio.yml"


def python_job() -> str:
    text = WORKFLOW.read_text(encoding="utf-8")
    start = text.index("\n  python:\n")
    rest = text[start + 1 :]
    end = rest.find("\n  # ", 1)
    return rest if end == -1 else rest[:end]


def test_req_002_python_job_runs_lint_then_tests():
    job = python_job()
    assert "ruff check ." in job
    assert "pytest" in job
    assert job.index("ruff check .") < job.index("pytest")


def test_req_002_python_job_uses_python_312_and_read_access():
    job = python_job()
    assert 'python-version: "3.12"' in job
    assert "contents: read" in job


def test_req_002_python_job_skips_closed_pull_requests():
    job = python_job()
    assert "github.event.action != 'closed'" in job
