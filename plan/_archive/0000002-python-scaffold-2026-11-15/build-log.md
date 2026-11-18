---
title: "Build Log - 0000002-python-scaffold"
summary: "Working record of the pipeline run, maintained by the orchestrator."
---
# Build Log - 0000002-python-scaffold

> Created at discovery (P0). Appended by the orchestrator at each phase boundary. Survives session changes.

## Header

| Field | Value |
|-------|-------|
| Feature ID | `0000002-python-scaffold` |
| Pipeline start | `2026-11-15T20:53:22Z` |
| Tool | `claude-code` |
| Primary model | `claude-sonnet-5-5` |
| Cheaper model | `claude-haiku-5-5` |
| Run speed | `standard` |

---

## Phase Log

### P0: Discovery

| Field | Value |
|-------|-------|
| Start | `2026-11-15T20:53:22Z` |
| End | `2026-11-15T20:54:37Z` |
| Wall clock | `2` |
| Model tier | primary |
| Skills loaded | ravintio-orchestrator |
| Agents spawned | `0` |
| MCP calls | `0` |
| Parallel task batches | `0` |
| Notes | Step 1 of initiative 0000001 |

- Migration pending: 0007
- Run mode: autonomous (2026-11-15T20:53:22Z)
- Run speed: standard (2026-11-15T20:53:22Z)
- Adoption mode: standard-iterative (signal: `docs/about.md` and `src/` present, no archive)
- Decision applied (initiative chart): Which version step 1 releases
- Decision applied (initiative chart): Whether the product version tracks the pack version
- Decision applied (initiative chart): Which Python version to target
- Decision applied (initiative chart): A step finds work outside its scope
- Queue: no items name step 1
- Scope Lock (happy path): The developer runs ruff and pytest from the repo root and both exit 0. CI does the same. [source: draft-accepted (initiative)]
- Scope Lock (first-run path): A fresh clone creates a virtual environment and installs the dev extras. [source: draft-accepted (initiative)]
- Scope Lock (error path): A failing test or lint error turns the Python check red. [source: draft-accepted (initiative)]
- Scope Lock (cross-session continuity): The step holds no runtime state and resumes from the build log. [source: draft-accepted (initiative)]
- Scope Lock complete. All four scenario paths captured.
- Complete: P0 (2026-11-15T20:54:37Z)

### P1: Plan

| Field | Value |
|-------|-------|
| Start | `2026-11-15T20:54:37Z` |
| End | `2026-11-15T20:55:42Z` |
| Wall clock | `1` |
| Model tier | primary |
| Skills loaded | ravintio-plan |
| Agents spawned | `0` |
| MCP calls | `0` |
| Parallel task batches | `0` |
| Notes | none |

- Complete: P1 (2026-11-15T20:55:42Z)

### P2: Implement

| Field | Value |
|-------|-------|
| Start | `2026-11-15T20:55:42Z` |
| End | `2026-11-15T21:36:31Z` |
| Wall clock | `41` |
| Model tier | primary |
| Skills loaded | ravintio-implement |
| Agents spawned | `0` |
| MCP calls | `0` |
| Parallel task batches | `0` |
| Notes | none |

- Design revised: Component Paths gained `pyproject.toml`, `.gitignore`, and `product.yml`. The files were in scope but missing from the list. [source: draft-accepted (initiative)]
- In progress: U1-config (2026-11-15T20:56:43Z)
- RED: U1-config (2026-11-15T20:56:37Z)
- RED: U2-packages (2026-11-15T20:56:37Z)
- GREEN: U2-packages (2026-11-15T20:56:43Z)
- GREEN: U1-config (2026-11-15T20:56:43Z)
- Done: U1-config (content, inline, none, 2026-11-15T20:56:43Z)
- Done: U2-packages (content, inline, none, 2026-11-15T20:56:43Z)
- Tests run: REQ-001: src/stem-core/tests/test_smoke.py, src/stem-service/tests/test_smoke.py, src/stem-web/tests/test_smoke.py (2026-11-15T20:56:43Z)
- RED: U3-ci (2026-11-15T20:56:56Z)
- GREEN: U3-ci (2026-11-15T20:57:27Z)
- Done: U3-ci (content, inline, none, 2026-11-15T20:57:27Z)
- Tests run: REQ-002: src/stem-core/tests/test_ci_job.py (2026-11-15T20:57:27Z)
- Tests run: test impact: test-0000327-req-002-ci-job.sh, test-0000390-req-003-enforcement-points.sh passed. test-0000317 and test-0000042 show failures that also appear in the P0 baseline run (2026-11-15T20:57:27Z)
- Rework: U4-docs: test-0000042-req-010 failed on a word that the allowlist bans in the manifests, so the step removed the optional stack field (2026-11-15T21:36:31Z)
- Tests run: full suite: 1 new failure, 56 inherited failures (2026-11-15T21:36:31Z)
- Tests run: full suite rerun of test-0000042-req-010-pack-wording-allowlist.sh: 2 passed, 0 failed (2026-11-15T21:36:31Z)
- RED: U4-docs (2026-11-15T21:36:00Z)
- GREEN: U4-docs (2026-11-15T21:36:31Z)
- Done: U4-docs (content, inline, none, 2026-11-15T21:36:31Z)
- Postmortem: plan/postmortems/2026-11-15-manifest-wording-test.md (2026-11-15T21:58:29Z)
- Departure from the concurrency plan: units ran inline in plan order. The units were small.
- Complete: P2 (2026-11-15T21:36:31Z)

### P3: Validate and Accept

| Field | Value |
|-------|-------|
| Start | `2026-11-15T21:36:48Z` |
| End | `2026-11-15T21:57:38Z` |
| Wall clock | `21` |
| Model tier | primary |
| Skills loaded | ravintio-validate-and-accept |
| Agents spawned | `0` |
| MCP calls | `0` |
| Parallel task batches | `0` |
| Notes | none |

- Tests run: full suite: 0 new failures, 57 inherited failures (2026-11-15T21:57:38Z)
- Docs edit pass: prose-check exit 0 on cycle 1, no subagent dispatched (2026-11-15T21:57:38Z)
- Complete: P3 (2026-11-15T21:57:38Z)

### P4: Ship

| Field | Value |
|-------|-------|
| Start | `2026-11-15T21:57:48Z` |
| End | `2026-11-15T21:57:53Z` |
| Wall clock | `1` |
| Model tier | primary |
| Skills loaded | ravintio-ship |
| Agents spawned | `0` |
| MCP calls | `0` |
| Parallel task batches | `0` |
| Notes | none |

- Complete: P4 (2026-11-15T21:57:53Z)

---

## Summary (filled at ship, P4)

| Metric | Value |
|--------|-------|
| Total phases completed | `5` |
| Total wall clock | `67` |
| Total agents spawned | `0` |
| Total MCP calls | `0` |
| Phases using parallelism | `0` |
| Primary tier agent calls | `0` |
| Cheaper tier agent calls | `0` |
| Self-corrections | `2` |
| Phases skipped | `none` |
