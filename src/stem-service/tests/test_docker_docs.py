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


def test_req_001_audioread_adr_is_indexed():
    assert "ADR-0009" in _read("docs/decisions-index.md")
    assert (ROOT / "docs" / "adr" / "0009-pin-audioread-beside-the-engine.md").exists()


def test_req_001_docs_name_the_audioread_pin():
    assert "AUDIOREAD_VERSION" in _read("src/stem-service/docs/dependencies.md")
    assert "audioread==3.1.0" in _read("src/stem-core/docs/dependencies.md")
    assert "audioread==3.1.0" in _read("docs/architecture-overview.md")


def test_req_002_docs_drop_the_audioread_fault():
    for path in (
        "src/stem-service/docs/quirks.md",
        "src/stem-service/component.yml",
        "src/stem-core/docs/quirks.md",
    ):
        assert "0000023" not in _read(path)
        assert "No module named" not in _read(path)
        assert "also needs `audioread`" not in _read(path)
