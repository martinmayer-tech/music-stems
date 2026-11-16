---
title: "ADR 0004: SQLite job store and a worker with a model pool"
summary: "stem-service owns a SQLite jobs table, and one worker thread for each device runs jobs through a pool that loads each model once."
status: "accepted"
component: "stem-service"
version: "0.4.0"
---
# ADR-0004 - SQLite job store and a worker with a model pool

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000008-job-queue-worker
**Component:** stem-service
**File:** `docs/adr/0004-sqlite-job-store-and-pooled-worker.md`
**Date:** 2026-11-15

## Context

Each `split()` call builds a separator and loads its models again. Two calls can also compete for one GPU. The service needs a queue that survives a restart, and a worker that keeps models in memory. The initiative chart fixes the backend: one SQLite file and one worker thread per device, with no broker. The chart also approves the `jobs` table.

## Decision

`stem-service` owns the SQLite table `jobs`. `JobStore` in `stem_service/jobs.py` is the only code that reads or writes it. The store opens one connection per call with `sqlite3`, uses parameterised SQL, and commits before each call returns. `claim_next()` runs inside `BEGIN IMMEDIATE`, so two workers never claim one job.

`Worker` in `stem_service/worker.py` runs one thread. It claims a job, calls `split()`, and marks the job `done` or `failed`. `start_workers(store, devices)` starts one worker for each device name.

The worker passes `split()` a separator factory that returns a `PooledSeparator`. The pool builds one separator for each model through the base factory, loads the model once, and reuses it. Before each use the pool sets the separator's `output_dir` to the job's folder.

`STEMS_DATA_DIR` (default `./data`) holds `jobs.sqlite3` and the folder `jobs/{id}` for each job's output.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| A broker such as Redis or Celery | Scales to many hosts | A new service and dependency | The chart says add no broker |
| An in-memory queue | No file | Jobs vanish on a restart | The entry needs jobs that survive a restart |
| A new `Separator` for each job | No pool code | Each job reloads its models | The entry needs models that load once |

## Affected Components

| Component | Impact |
|-----------|--------|
| stem-service | Gains `config.py`, `jobs.py`, and `worker.py`, and owns the `jobs` table |
| stem-core | None. The worker calls `split()` as it is |

## Consequences

**Positive:**
- Jobs survive a restart, and a job that a restart interrupted runs again.
- A model loads once for each worker, so the second job starts faster.
- The step adds no dependency.

**Negative:**
- SQLite serialises writes, so one file suits one host only.
- The pool holds a loaded model in memory until the worker stops.

**Risks:**
- A real `Separator` may ignore a changed `output_dir`. A later real run shows it.

## Related ADRs

- ADR-0002 sets the injected separator factory that the pool wraps.

## Supersedes

- None.

## Superseded By

- None.
