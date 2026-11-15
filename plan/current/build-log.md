---
title: "Build Log - 0000006-command-line-interface"
summary: "Working record of the pipeline run, maintained by the orchestrator."
---
# Build Log - 0000006-command-line-interface

> Created at discovery (P0). Appended by the orchestrator at each phase boundary. Survives session changes.

## Header

| Field | Value |
|-------|-------|
| Feature ID | `0000006-command-line-interface` |
| Pipeline start | `2026-11-15T22:54:00Z` |
| Tool | `claude-code` |
| Primary model | `claude-sonnet-5-5` |
| Cheaper model | `claude-haiku-5-5` |
| Run speed | `standard` |

---

## Phase Log

### P0: Discovery

| Field | Value |
|-------|-------|
| Start | `2026-11-15T22:54:00Z` |
| End | `{{timestamp, filled when the phase completes}}` |
| Wall clock | `{{whole minutes from Start to End}}` |
| Model tier | primary |
| Skills loaded | ravintio-orchestrator |
| Agents spawned | `0` |
| MCP calls | `0` |
| Parallel task batches | `0` |
| Notes | Step 3 of initiative 0000001 |

- Migration pending: 0007
- Migration pending: 0009
- Run mode: autonomous (2026-11-15T22:54:00Z)
- Run speed: standard (2026-11-15T22:54:00Z)
- Adoption mode: standard-iterative (signal: `docs/about.md` at 0.2.0, `src/` present, steps 1 and 2 archived)
- Decision applied (initiative chart): Whether the product version tracks the pack version
- Decision applied (initiative chart): Which Python version to target
- Decision applied (initiative chart): A step finds work outside its scope
- Decision applied (initiative chart): Tests need a real model
- Decision applied (initiative chart): Which CLI library to use
- Queue: no items name step 3
- Bump: minor (chart row), planned version 0.3.0
- Scope Lock (happy path): A user runs `stems split mix.wav --output-dir out` and gets one absolute path per line and exit 0. [source: draft-accepted (initiative)]
- Scope Lock (first-run path): The model folder holds no models, so `audio-separator` downloads them on first use. [source: draft-accepted (initiative)]
- Scope Lock (error path): A missing input file or a model failure prints one error line, prints no path, and exits non-zero. [source: draft-accepted (initiative)]
- Scope Lock (cross-session continuity): The command keeps no state, and a repeat run rewrites the output files. [source: draft-accepted (initiative)]
- Scope Lock complete. All four scenario paths captured.

---

## Summary (filled at ship, P4)

| Metric | Value |
|--------|-------|
| Total phases completed | `{{count}}` |
| Total wall clock | `{{minutes from pipeline start to the P4 End}}` |
| Total agents spawned | `{{count}}` |
| Total MCP calls | `{{count}}` |
| Phases using parallelism | `{{count}}` |
| Primary tier agent calls | `{{count}}` |
| Cheaper tier agent calls | `{{count}}` |
| Self-corrections | `{{count}}` |
| Phases skipped | `{{list or "none"}}` |
