---
title: "Build Log - 0000014-model-ensemble-options"
summary: "Working record of the pipeline run, maintained by the orchestrator."
---
# Build Log - 0000014-model-ensemble-options

> Created at discovery (P0). Appended by the orchestrator at each phase boundary. Survives session changes.

## Header

| Field | Value |
|-------|-------|
| Feature ID | `0000014-model-ensemble-options` |
| Pipeline start | `2026-11-16T02:10:45Z` |
| Tool | `claude-code` |
| Primary model | `claude-sonnet-5-5` |
| Cheaper model | `claude-haiku-5-5` |
| Run speed | `standard` |

---

## Phase Log

### P0: Discovery

| Field | Value |
|-------|-------|
| Start | `2026-11-16T02:10:45Z` |
| End | `2026-11-16T02:22:18Z` |
| Wall clock | `11` |
| Model tier | primary |
| Skills loaded | ravintio-orchestrator |
| Agents spawned | `0` |
| MCP calls | `0` |
| Parallel task batches | `0` |
| Notes | Step 7 of initiative 0000001 |

- Migration pending: 0007
- Migration pending: 0009
- Run mode: autonomous (2026-11-16T02:10:45Z)
- Run speed: standard (2026-11-16T02:10:45Z)
- Adoption mode: standard-iterative (signal: `docs/about.md` at 0.6.0, `src/` present, steps 1 to 6 archived)
- Decision applied (initiative chart): Whether the product version tracks the pack version
- Decision applied (initiative chart): Which Python version to target
- Decision applied (initiative chart): A step finds work outside its scope
- Decision applied (initiative chart): Tests need a real model
- Decision applied (initiative chart): Which models a caller may pick
- Queue: no items name step 7
- Bump: minor (chart row), planned version 0.7.0
- Dependencies: none for step 7
- Schema: step 7 row is `none`. The `jobs.options` column already exists.
- Scope Lock (happy path): A user sends a mix with `htdemucs_6s.yaml` and full stems. The job ends `done` and lists guitar and piano stems. [source: draft-accepted (initiative)]
- Scope Lock (first-run path): A user sends no option and the job runs the two default models. [source: draft-accepted (initiative)]
- Scope Lock (error path): A caller names an unlisted model, preset, or stem. The caller gets a clear error before any model loads. [source: draft-accepted (initiative)]
- Scope Lock (cross-session continuity): A queued job keeps its options in `jobs.options` across a restart. [source: draft-accepted (initiative)]
- Scope Lock complete. All four scenario paths captured.
- Baseline: the clean-clone run is still going. The agent records it before P3 starts.
- Complete: P0 (2026-11-16T02:22:18Z)
