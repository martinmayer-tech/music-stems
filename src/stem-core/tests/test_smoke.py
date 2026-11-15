"""Smoke test for the stem_core package (REQ-001)."""

import stem_core


def test_req_001_stem_core_smoke():
    assert stem_core.__version__
