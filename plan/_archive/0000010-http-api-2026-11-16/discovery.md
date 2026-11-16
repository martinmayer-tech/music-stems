---
title: "Discovery - 0000010-http-api"
summary: "Raw discovery-pass findings: what the orchestrator knew before coaching began."
---
# Discovery - 0000010-http-api

## Header (all modes)

| Field | Value |
|-------|-------|
| Adoption mode detected | `standard-iterative` |
| Detection signal | `docs/about.md` at 0.4.0 and `src/` beside an archive. The chart is the source of truth |
| Git pre-flight | Branch `feat/0000010-http-api`, cut by the driver from `initiative/0000001-stem-separation-service` |
| Skills inbox | empty |
| Track | full |

## Mode Findings

### Standard Iterative

- Current version (`docs/about.md`): `0.4.0`. Step 5 bumps minor to `0.5.0`. The merge queue writes it.
- Prior features (`plan/_archive/`): 0000002-python-scaffold, 0000004-separation-core, 0000006-command-line-interface, and 0000008-job-queue-worker.
- Constraining ADRs: `docs/adr/0001-python-tooling.md`, `0002-separator-injection-and-pin.md`, `0003-stems-command-and-packaging.md`, and `0004-sqlite-job-store-and-pooled-worker.md`.
- Component map: `stem-service` holds `config.py`, `jobs.py`, and `worker.py`. It owns the `jobs` table. `stem-web` is a skeleton.
- Repo instructions: `agent-permissions.md` and `grep-tests-before-moving-files.md`.
- Pending migrations: 0007 and 0009. No `Migration:` row in the chart, so the step records `Migration pending` and carries on.
- Backlog: entry 0000011 is the step's entry. Entries 0000018 and 0000019 are not for this step.
- Queue: `plan/.initiative-queue/` holds no item that names step 5.
- Schema: the chart lists no change for step 5. The API reads and writes the existing `jobs` table through `JobStore`.
- Dependencies: the chart approves `fastapi`, `uvicorn`, `python-multipart`, and `httpx` for step 5.
- Existing API: `JobStore.add(input_path, full_stems, options)`, `get`, `list`, `claim_next`, `mark_done`, `mark_failed`, and `recover`. `Worker` has `wake()`. `start_workers(store, devices)` starts the workers. `config.py` holds `resolve_data_dir()`, `database_path()`, and `job_output_dir()`.
- Local toolchain: Python 3.13. The step installs the four approved libraries in a virtual environment outside the repo.
- Baseline: the pack suite runs in a clean clone. Its output goes to `plan/current/baseline-failures.md`.
