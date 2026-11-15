# Changelog (0000006-command-line-interface, 15 Nov 2026)

**Feature:** Add the command-line interface
**Version:** set by the merge queue at merge
**PR:** 7

## What changed

- Added the `stems` command in `stem_core/cli.py` with the subcommands `split`, `env`, and `models`.
- Added `python -m stem_core` and a `stems` console script.
- Changed `pyproject.toml` to package `stem_core` from `src/stem-core`. It held `packages = []` before.
- Added ADR 0003 and updated the component docs and living docs.

## Why

A user could reach the separation core only from Python code. The guide calls for a scriptable tool.

## Deviations

None.

## Validation results

- `ruff check .` exits 0. `pytest` gives 38 passed and 1 deselected.
- A scratch install ran `stems models`, `stems env`, and `stems split` on a missing file, which exited 1.

## Skipped phases

None.
