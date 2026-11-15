---
title: "Build Log - 0000004-separation-core"
summary: "Working record of the pipeline run, maintained by the orchestrator."
---
# Build Log - 0000004-separation-core

> Created at discovery (P0). Appended by the orchestrator at each phase boundary. Survives session changes.

## Header

| Field | Value |
|-------|-------|
| Feature ID | `0000004-separation-core` |
| Pipeline start | `2026-11-15T22:01:54Z` |
| Tool | `claude-code` |
| Primary model | `claude-sonnet-5-5` |
| Cheaper model | `claude-haiku-5-5` |
| Run speed | `standard` |

---

## Phase Log

### P0: Discovery

| Field | Value |
|-------|-------|
| Start | `2026-11-15T22:01:54Z` |
| End | `2026-11-15T22:02:44Z` |
| Wall clock | `6` |
| Model tier | primary |
| Skills loaded | ravintio-orchestrator |
| Agents spawned | `0` |
| MCP calls | `0` |
| Parallel task batches | `0` |
| Notes | Step 2 of initiative 0000001 |

- Migration pending: 0007
- Migration pending: 0009
- Run mode: autonomous (2026-11-15T22:01:54Z)
- Run speed: standard (2026-11-15T22:01:54Z)
- Adoption mode: standard-iterative (signal: `docs/about.md` at 0.1.0, `src/` present, step 1 archived)
- Decision applied (initiative chart): Whether the product version tracks the pack version
- Decision applied (initiative chart): Which Python version to target
- Decision applied (initiative chart): A step finds work outside its scope
- Decision applied (initiative chart): Which `audio-separator` version to pin
- Decision applied (initiative chart): Tests need a real model
- Decision applied (initiative chart): `separate()` returns relative paths
- Decision applied (initiative chart): `audio-separator` fails to install on local Python 3.13
- Decision not applicable (initiative chart): Which version step 1 releases: step 1 only
- Queue: no items name step 2
- Bump: minor (chart row), planned version 0.2.0
- Scope Lock (happy path): A developer calls `split` on a WAV mix and gets two absolute paths, or five with `full_stems=True`. [source: draft-accepted (initiative)]
- Scope Lock (first-run path): The model folder holds no models, so `audio-separator` downloads them on first use. [source: draft-accepted (initiative)]
- Scope Lock (error path): A missing mix or a model load failure raises an error and returns no partial list. [source: draft-accepted (initiative)]
- Scope Lock (cross-session continuity): The function keeps no state, and a repeat call rewrites the output files. [source: draft-accepted (initiative)]
- Scope Lock complete. All four scenario paths captured.
- Complete: P0 (2026-11-15T22:02:44Z)

### P1: Plan

| Field | Value |
|-------|-------|
| Start | `2026-11-15T22:02:44Z` |
| End | `2026-11-15T22:03:56Z` |
| Wall clock | `2` |
| Model tier | primary |
| Skills loaded | ravintio-plan |
| Agents spawned | `0` |
| MCP calls | `0` |
| Parallel task batches | `0` |
| Notes | none |

- Complete: P1 (2026-11-15T22:03:56Z)

### P2: Implement

| Field | Value |
|-------|-------|
| Start | `2026-11-15T22:03:56Z` |
| End | `pending` |
| Wall clock | `pending` |
| Model tier | primary |
| Skills loaded | ravintio-implement |
| Agents spawned | `0` |
| MCP calls | `0` |
| Parallel task batches | `0` |
| Notes | none |
- In progress: U1-core (2026-11-15T22:04:09Z)
- RED: U1-core (2026-11-15T22:04:09Z)
- GREEN: U1-core (2026-11-15T22:04:43Z)
- Done: U1-core (content, inline, none, 2026-11-15T22:04:43Z)
- Tests run: REQ-001, REQ-002: src/stem-core/tests/test_separation.py (2026-11-15T22:04:43Z)
- In progress: U2-pin-ci (2026-11-15T22:04:43Z)
