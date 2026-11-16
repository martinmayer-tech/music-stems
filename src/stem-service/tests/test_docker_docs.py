"""REQ-001 to REQ-003: the docs and the living docs describe the Docker files."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_docker_docs_purpose_names_the_commands():
    text = _read("src/stem-service/docs/purpose.md")
    assert "docker compose up --build" in text
    assert "compose.gpu.yaml" in text
    assert "127.0.0.1" in text


def test_docker_docs_adr_is_indexed():
    assert "ADR-0008" in _read("docs/decisions-index.md")
    assert (ROOT / "docs" / "adr" / "0008-docker-packaging-of-the-service.md").exists()


def test_docker_docs_manifest_names_the_files():
    text = _read("src/stem-service/component.yml")
    assert 'iac: "dockerfile"' in text
    assert "0000016-docker-packaging" in text
