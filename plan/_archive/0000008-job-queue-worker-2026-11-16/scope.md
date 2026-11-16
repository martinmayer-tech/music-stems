---
title: "Scope - Add the job queue and worker"
summary: "Defines explicit boundaries of what is in scope and out of scope."
status: "active"
version: "0.1.0"
---
# Scope - Add the job queue and worker

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000008-job-queue-worker
**Version:** 0.4.0

## In Scope

- `stem_service/config.py`, `jobs.py`, and `worker.py`.
- The SQLite table `jobs` and the `JobStore` class.
- The `Worker` class, `start_workers`, and the `PooledSeparator` model cache.
- Restart recovery.
- Unit tests with a fake separator.
- The data contract, component docs, and the living docs that the code changes.

## Out of Scope

- The HTTP API, uploads, and the web page.
- Cancel a job: gap: out of scope.
- Call the queue over HTTP: gap: out of scope.
- A broker or a second queue backend.
- Model choice by the caller and ensembles.

## Deferred

- The HTTP API waits for step 5. It blocks upload and download.
- Model choice and ensembles wait for step 7. They fill the `options` column.
