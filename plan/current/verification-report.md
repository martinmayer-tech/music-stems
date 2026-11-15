# Verification report - 0000002-python-scaffold

The agent created a virtual environment in a scratch folder and installed `pytest` and `ruff`. It ran each check from the repo root. It ran the failing-test case in a scratch copy of `HEAD`.

| Criterion | Method | Outcome | Evidence |
|-----------|--------|---------|----------|
| REQ-001 AC-1 | CLI: `pytest` | verified | Exit 0, 6 tests passed, one smoke test for each component |
| REQ-001 AC-2 | CLI: `ruff check .` | verified | Exit 0, all checks passed |
| REQ-002 AC-1 | CLI: `pytest` in a scratch copy with a failing test | verified locally | Exit 1, 1 failed and 6 passed. The pull request check turns red after the first CI run |
| REQ-002 AC-2 | CLI: `pytest` and `ruff check .` in a clean tree | verified locally | Exit 0. The pull request check turns green after the first CI run |
| REQ-003 AC-1 | Side effect: read `product.yml` | verified | Three components, and each `component.yml` exists |
| REQ-003 AC-2 | CLI: `node ravintio-zero/scripts/merge-queue.mjs versions` | verified | Exit 0, `ok: 0.0.0` |

The chart marks the Python job criterion as `CI`. It counts as validated after the first CI run on the step PR.

A lint error in a scratch copy gave `ruff check .` exit 1.
