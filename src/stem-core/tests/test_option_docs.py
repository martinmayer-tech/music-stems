"""Tests that the docs name the model options (REQ-001, REQ-002)."""

from pathlib import Path

from stem_core.separation import ENSEMBLE_PRESETS, PASS_TWO_MODELS, SINGLE_STEMS

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = (ROOT / "src" / "stem-core" / "docs" / "interface-contract.md").read_text()


def test_req_001_the_contract_names_the_option_arguments_and_the_check():
    for text in ("model", "ensemble_preset", "single_stem", "validate_options"):
        assert text in CONTRACT


def test_req_002_the_contract_names_the_flags_and_the_model_listing():
    for flag in ("--model", "--ensemble-preset", "--single-stem"):
        assert flag in CONTRACT
    for line in ("pass-2-models", "ensemble-presets", "single-stems"):
        assert line in CONTRACT


def test_req_001_the_contract_lists_every_allowed_model():
    for value in PASS_TWO_MODELS:
        assert value in CONTRACT or value == "htdemucs_ft.yaml"
    assert "htdemucs_6s.yaml" in CONTRACT
    assert len(ENSEMBLE_PRESETS) == 9 and len(SINGLE_STEMS) == 7
    assert "guitar.wav" in CONTRACT
