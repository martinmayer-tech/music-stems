---
title: "Discovery - 0000004-separation-core"
summary: "Raw discovery-pass findings: what the orchestrator knew before coaching began."
---
# Discovery - 0000004-separation-core

## Header (all modes)

| Field | Value |
|-------|-------|
| Adoption mode detected | `standard-iterative` |
| Detection signal | `docs/about.md` at 0.1.0 and `src/` beside an archive. The chart is the source of truth |
| Git pre-flight | Branch `feat/0000004-separation-core`, cut by the driver from `initiative/0000001-stem-separation-service` |
| Skills inbox | empty |
| Track | full |

## Mode Findings

### Standard Iterative

- Current version (`docs/about.md`): `0.1.0`. Step 2 bumps minor to `0.2.0`. The merge queue writes it.
- Prior features (`plan/_archive/`): 0000002-python-scaffold (2026-11-15), the Python layout, tests, and CI.
- Constraining ADRs: `docs/adr/0001-python-tooling.md` (pytest, ruff, Python 3.12 in CI).
- Component map: `stem-core`, `stem-service`, and `stem-web` hold skeletons. `stem-core` owns no data.
- Repo instructions: `agent-permissions.md` and `grep-tests-before-moving-files.md`.
- Pending migrations: 0007 and 0009. No `Migration:` row in the chart, so the step records `Migration pending` and carries on.
- Backlog: entry 0000005 is the step's entry. Entry 0000018 is not for this step.
- Retrospective and postmortem input: step 2 edits the existing manifest only, so the banned optional stack field stays out.
- Toolchain: `pytest`, `ruff`, and a `python` CI job exist. No file installs `audio-separator` yet.
- Newest `audio-separator` on PyPI: 0.48.0.
