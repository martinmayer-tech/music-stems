---
title: "Postmortem: 2026-11-15 - A subprocess test ignored PYTHONPATH"
summary: "The first subprocess test ran Python in isolated mode, which ignores PYTHONPATH, so the import failed. The step removed the flag."
status: "closed"
---
# Postmortem: 2026-11-15 - A subprocess test ignored PYTHONPATH

> Path: `plan/postmortems/2026-11-15-isolated-subprocess-test.md`. Written by `ravintio-postmortem`.

**Trigger:** P2 self-correction
**Feature:** 0000006-command-line-interface
**Date:** 2026-11-15

## Summary

The test that checks `audio_separator` stays out of `sys.modules` ran a fresh interpreter with `-I`. Isolated mode ignores `PYTHONPATH`, so the child process could not import `stem_core`. The step removed the flag and the test passed.

## Timeline

| Time | Event | Evidence |
|------|-------|----------|
| 2026-11-15T22:56:55Z | The new CLI tests ran RED because `stem_core.cli` did not exist | `plan/current/build-log.md`, the `RED: U1-cli` line |
| 2026-11-15T22:57:03Z | The first GREEN run failed one test with a non-zero child exit | `src/stem-core/tests/test_cli.py`, `test_req_004_env_and_models_import_no_model_library` |
| 2026-11-15T22:57:03Z | The step removed `-I` from the child command and the test passed | commit `69aa6ea` and `src/stem-core/tests/test_cli.py` |

First missed chance to catch it: the RED run failed on a missing module, so it never reached the subprocess command.

## 5 whys

1. The test failed because the child interpreter could not import `stem_core`.
2. The child ran with `-I`, which ignores `PYTHONPATH`.
3. The test author added `-I` for a clean interpreter and did not check how it treats the environment.
4. The RED run stopped at the missing module, so the command never ran before the code existed.
5. The testing standards have no note on how isolated mode and `PYTHONPATH` interact.

**Gap:** `ravintio-zero/standards/testing-standards.md` gives no guidance for subprocess tests that need a clean interpreter.

## Actions

| Type | Action | Status | Owner | Lives in | Verified by | Ref |
|------|--------|--------|-------|----------|-------------|-----|
| corrective | Run the child process without `-I` and pass only `PYTHONPATH` in its environment | done | step 3 | `src/stem-core/tests/test_cli.py` | `test_req_004_env_and_models_import_no_model_library` | commit 69aa6ea |
| preventive | none, because the cost is one failed local run and the pack cannot cover every interpreter flag | none | none | none | none | none |
| detective | none, because the test failed on its first GREEN run and showed the cause | none | none | none | none | none |
