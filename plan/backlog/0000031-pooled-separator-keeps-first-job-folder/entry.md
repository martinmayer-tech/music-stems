---
title: "Backlog Entry: 0000031 - Pooled separator keeps the first job's folder"
summary: "Every job after the first writes its stems into the first job's folder, so it reports done with no files and overwrites the first job's stems."
status: "open"
priority: "high"
theme: "stem-separation"
---
# Backlog Entry: 0000031 - Pooled separator keeps the first job's folder

**Source feature:** 0000029-add-audioread

**Source phase:** P3

**Deferral source:** discovered mid-flight

**Date filed:** 2026-11-18

---

## Problem

The worker reuses one loaded separator for each model. For a later job, `SeparatorPool.acquire()` in `src/stem-service/stem_service/worker.py` sets `separator.output_dir` to the new job folder. The real `audio-separator` 0.48.0 engine ignores that change and keeps writing to the folder it started with.

The agent ran three jobs in a fresh image on 2026-11-18:

- Job 1, plain: ended `done` with `vocals.wav` and `instrumental.wav` in its own folder.
- Job 2, full stems: pass 1 wrote both stems into the folder of job 1. Pass 2 then failed with `Error opening '/data/jobs/{id}/instrumental.wav': System error.`
- Job 3, plain: ended `done` and listed both stems. Its folder was empty, and `GET /jobs/{id}/stems/vocals.wav` returned 404. Its stems overwrote those of job 1.

So the service gives correct stems for one job per model after each start. `src/stem-service/docs/quirks.md` and the risk list in `component.yml` already name the untested case. The unit tests use fake separators that accept the change.

## Suggested Action

Make a reused separator write to the new job folder. Check where the 0.48.0 engine keeps the folder, which is likely the loaded model instance, and set it there too. If no supported setter exists, write to a fixed work folder and move the stems into the job folder. Add a check that the worker fails a job whose listed stems do not exist.

**Observable condition:** three jobs in a row in one container each end `done`, and each job folder holds its own stems.

## Why Deferred

Feature 0000029 adds `audioread` and changes no worker code. The fix needs its own design, because it changes how the pool and the engine share a folder.
