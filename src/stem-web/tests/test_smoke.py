"""Smoke test for the stem_web package (REQ-001)."""

import stem_web


def test_req_001_stem_web_smoke():
    assert stem_web.__version__
