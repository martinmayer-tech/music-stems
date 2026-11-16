---
title: "Discovery - 0000016-docker-packaging"
summary: "Raw discovery-pass findings: what the orchestrator knew before coaching began."
---
# Discovery - 0000016-docker-packaging

## Header (all modes)

| Field | Value |
|-------|-------|
| Adoption mode detected | `standard-iterative` |
| Detection signal | `docs/about.md` at 0.7.0 and `src/` beside an archive. The chart is the source of truth |
| Git pre-flight | Branch `feat/0000016-docker-packaging`, cut by the driver from `initiative/0000001-stem-separation-service` |
| Skills inbox | empty |
| Track | full |

## Mode Findings

### Standard Iterative

- Current version (`docs/about.md`): `0.7.0`. Step 8 bumps minor to `0.8.0`. The merge queue writes it.
- Prior features (`plan/_archive/`): 0000002 to 0000014, one for each of steps 1 to 7.
- Constraining ADRs: `docs/adr/0001` to `0007`. ADR-0004 sets the pooled worker. ADR-0005 sets the loopback bind and no login.
- Component map: `stem-core` holds `split()` and the `stems` command. `stem-service` holds the job store, the worker, and the API. `stem-web` holds the page files.
- Repo instructions: `agent-permissions.md` and `grep-tests-before-moving-files.md`.
- Pending migrations: 0007 and 0009. No `Migration:` row in the chart, so the step records `Migration pending` and carries on.
- Backlog: entry 0000017 is the step's entry. Entries 0000018 to 0000022 are not for this step.
- Queue: no `plan/.initiative-queue/` folder exists, so no item names step 8.
- Schema: the chart lists no change for step 8.
- Dependencies: the chart lists `python:3.12-slim`, `ffmpeg`, and `audio-separator[gpu]` for step 8.
- Existing seams: `python -m stem_service` reads `STEMS_HOST`, `STEMS_PORT`, `STEMS_DATA_DIR`, `STEMS_MODEL_DIR`, and `STEMS_MAX_UPLOAD_MB`. The default host is `127.0.0.1`. The root `pyproject.toml` has the extras `service` and `separation`. The `separation` extra pins `audio-separator[cpu]==0.48.0`.
- Local toolchain: Docker 29.9.3 with a running daemon. Python 3.13 with a virtual environment outside the repo.
- Baseline: the pack suite runs in a clean clone. Its output goes to `plan/current/baseline-failures.md`.
