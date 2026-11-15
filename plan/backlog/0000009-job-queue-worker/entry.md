---
title: "Backlog Entry: 0000009 - Job queue and worker"
summary: "Job queue and worker for the self-hosted stem separation service."
status: "open"
priority: "high"
theme: "stem-separation"
---
# Backlog Entry: 0000009 - Job queue and worker

**Source feature:** none (human request)

**Source phase:** none (human request)

**Deferral source:** human request

**Date filed:** 2026-11-15

---

## Problem

Each `split()` call loads its models again, and two calls can compete for one GPU. Section 10 of the guide asks for a queue and a model that loads once per worker.

## Suggested Action

Build a `stem-service` component with a job store in SQLite and one worker per device. The worker keeps each loaded model and runs one job at a time. A job moves through `queued`, `running`, `done`, and `failed`. Jobs survive a restart.

**Observable condition:** two jobs queued together never overlap in run time, and the second job loads no model that the first already loaded.

## Why Deferred

The human asked for the solution as one initiative. Initiative 0000001 runs this entry as its own step.
