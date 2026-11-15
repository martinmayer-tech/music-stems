---
title: "Requirement: REQ-001 - Split from the command line"
summary: "stems split prints one output path per line and exits 0, or prints one error line and exits non-zero."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-001 - Split from the command line

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000006-command-line-interface
**Source:** US-001
**Priority:** must-have

## User Story

As a user, I run `stems split mix.wav --output-dir out`, so that I get one output path per line to use in a script.

## Functional Requirements
- `stems split FILE` calls `split()` and prints each returned absolute path on its own line to standard output.
- `--output-dir DIR` sets the output folder. The default is `./stems-out`.
- The command exits 0 on success.
- A missing input file prints one `stems: error: ...` line to standard error, prints no path, and exits 1.
- A failure inside `split()` prints one error line to standard error and exits 1. The command prints no traceback.
- A `stems` console script and `python -m stem_core` both run the same `main()`.

## Acceptance Criteria
- [ ] AC-1: Paths on success
  - Given an existing mix file and a fake separator
  - When the user runs `stems split mix.wav --output-dir out`
  - Then the command exits 0 and prints 2 absolute paths, one per line
- [ ] AC-2: Missing input
  - Given a mix path that does not exist
  - When the user runs `stems split missing.wav`
  - Then the command exits non-zero, prints one error line, and prints no path
- [ ] AC-3: Entry points
  - Given the `stem_core` package
  - When the user runs `python -m stem_core split missing.wav`
  - Then the process exits non-zero and `pyproject.toml` maps `stems` to `stem_core.cli:main`

## Dependencies
- Step 2: `split()`.
