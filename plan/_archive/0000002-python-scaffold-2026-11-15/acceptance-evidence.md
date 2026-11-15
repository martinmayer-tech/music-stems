# Acceptance evidence - 0000002-python-scaffold

## Checks

- Lint: `ruff check .` exits 0.
- Tests: `pytest` collects 6 tests and all pass.
- Full suite in a clean clone: 0 new failures and 57 inherited failures. Each inherited suite appears in `plan/current/baseline-failures.md`.
- Archetype gates: none installed.
- Self-corrections: 2. One for the gate path form, one for a banned word in the manifests.

## Security

No critical or high findings. One low finding: `pyproject.toml:14` leaves `pytest` and `ruff` unpinned.

## Execution

A scratch copy with a failing test gave `pytest` exit 1. A clean tree gave exit 0. A lint error gave `ruff check .` exit 1. The `python` job itself runs on the step PR. The criterion counts as validated after that first CI run.

## Docs edit pass

`prose-check.mjs check` exits 0 on 21 changed docs in cycle 1. The agent dispatched no review subagent because the script found nothing to fix.
