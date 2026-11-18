"""Smoke test for the stem_service package (REQ-001)."""

import stem_service


def test_req_001_stem_service_smoke():
    assert stem_service.__version__
