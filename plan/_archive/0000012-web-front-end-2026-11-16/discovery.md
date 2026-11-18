---
title: "Discovery - 0000012-web-front-end"
summary: "Raw discovery-pass findings: what the orchestrator knew before coaching began."
---
# Discovery - 0000012-web-front-end

## Header (all modes)

| Field | Value |
|-------|-------|
| Adoption mode detected | `standard-iterative` |
| Detection signal | `docs/about.md` at 0.5.0 and `src/` beside an archive. The chart is the source of truth |
| Git pre-flight | Branch `feat/0000012-web-front-end`, cut by the driver from `initiative/0000001-stem-separation-service` |
| Skills inbox | empty |
| Track | full |

## Mode Findings

### Standard Iterative

- Current version (`docs/about.md`): `0.5.0`. Step 6 bumps minor to `0.6.0`. The merge queue writes it.
- Prior features (`plan/_archive/`): 0000002-python-scaffold, 0000004-separation-core, 0000006-command-line-interface, 0000008-job-queue-worker, and 0000010-http-api.
- Constraining ADRs: `docs/adr/0001` to `0005`. ADR-0005 sets the loopback bind and no login.
- Component map: `stem-service` holds `api.py` with four routes. `stem-web` is a skeleton with `__version__` and a smoke test.
- Repo instructions: `agent-permissions.md` and `grep-tests-before-moving-files.md`.
- Pending migrations: 0007 and 0009. No `Migration:` row in the chart, so the step records `Migration pending` and carries on.
- Backlog: entry 0000013 is the step's entry. Entries 0000015 and 0000017 belong to steps 7 and 8. Entries 0000018 to 0000020 are not for this step.
- Queue: `plan/.initiative-queue/` holds no item that names step 6.
- Schema: the chart lists no change for step 6. The page reads the API and owns no data.
- Dependencies: the chart lists none for step 6. The page uses plain HTML, CSS, and JavaScript with no build.
- Existing API: `POST /jobs` (multipart `file`, form `full_stems`), `GET /jobs`, `GET /jobs/{id}`, and `GET /jobs/{id}/stems/{name}`. A job answer holds `id`, `status`, `full_stems`, `stems`, `error`, and three timestamps.
- Test rule: tests check the served files and the API calls over HTTP. The step adds no browser automation.
- Local toolchain: Python 3.13 with a virtual environment outside the repo. Node runs the pack scripts.
- Baseline: the pack suite runs in a clean clone. Its output goes to `plan/current/baseline-failures.md`.
