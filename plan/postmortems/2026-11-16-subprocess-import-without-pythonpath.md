---
title: "Postmortem: 2026-11-16 - A subprocess import test ran without PYTHONPATH"
summary: "The first import check ran a child Python with no PYTHONPATH, so it failed on the import. The step passed the package folder in the environment."
status: "closed"
---
# Postmortem: 2026-11-16 - A subprocess import test ran without PYTHONPATH

> Path: `plan/postmortems/2026-11-16-subprocess-import-without-pythonpath.md`. Written by `ravintio-postmortem`.

**Trigger:** P2 self-correction
**Feature:** 0000008-job-queue-worker
**Date:** 2026-11-16

## Summary

The test that checks `audio_separator` stays out of `sys.modules` ran a fresh interpreter with no `PYTHONPATH`. The child could not import `stem_service`, so the test failed on the import and not on its assertion. The step passed the package folder in the child environment and the test passed.

## Timeline

| Time | Event | Evidence |
|------|-------|----------|
| 2026-11-15T23:59:02Z | The first GREEN run failed one test with a non-zero child exit | `src/stem-service/tests/test_jobs.py`, the import check |
| 2026-11-15T23:59:02Z | The step set `PYTHONPATH` in the child environment and the test passed | commit `73c70ce` and `src/stem-service/tests/test_jobs.py` |

First missed chance to catch it: step 3 hit the same failure for `stem-core`. Its postmortem filed no preventive action, so nothing told this step to set `PYTHONPATH`.

## 5 whys

1. The test failed because the child interpreter could not import `stem_service`.
2. The pytest `pythonpath` setting applies to the test process only, and the child does not inherit it.
3. The test author assumed the child sees the same import path as the test.
4. The RED run stopped at a missing module, so the subprocess command never ran before the code existed.
5. The testing standards have no note on how a child process finds the packages under test, and the earlier postmortem filed no preventive action.

**Gap:** `ravintio-zero/standards/testing-standards.md` gives no guidance for subprocess tests that import a package from `src/`.

## Actions

| Type | Action | Status | Owner | Lives in | Verified by | Ref |
|------|--------|--------|-------|----------|-------------|-----|
| corrective | Pass the package folder in the child environment as `PYTHONPATH` | done | step 4 | `src/stem-service/tests/test_jobs.py` | `test_req_004_import_loads_no_model_library` | commit 73c70ce |
| preventive | none, because the step may not edit pack standards and the same gap sits in the postmortem of step 3 | none | none | none | none | none |
| detective | none, because the test failed on its first GREEN run and showed the cause | none | none | none | none | none |
