---
title: "Postmortem: 2026-11-15 - The real separator differed from the fake"
summary: "The real separator listed stems in another order and returned a silent vocals stem for a pure tone. The fake separator hid both."
status: "closed"
---
# Postmortem: 2026-11-15 - The real separator differed from the fake

> Path: `plan/postmortems/2026-11-15-real-separator-differences.md`. Written by `ravintio-postmortem`.

**Trigger:** P2 self-correction
**Feature:** 0000004-separation-core
**Date:** 2026-11-15

## Summary

Unit tests with a fake separator passed. The first real-model run found two differences. The real separator listed the instrumental before the vocals, and the vocals stem of a pure tone held no sound. The step sorted the stems and narrowed the sound check.

## Timeline

| Time | Event | Evidence |
|------|-------|----------|
| 2026-11-15T22:04:00Z | Unit tests passed with the fake separator | `plan/current/build-log.md`, the `Tests run: REQ-001, REQ-002` line |
| 2026-11-15T22:06:00Z | The real run failed the sound check on the vocals stem | `src/stem-core/tests/test_real_model.py` |
| 2026-11-15T22:08:00Z | A direct call with `full_stems=True` returned the instrumental first | `plan/current/verification-report.md` |
| 2026-11-15T22:08:23Z | The step sorted the stems and narrowed the test | commit `5261c07` and `src/stem-core/stem_core/separation.py` |

First missed chance to catch it: the fake separator returned the stems in the order that the code expected.

## 5 whys

1. The fake and the real separator returned different orders.
2. The guide does not state an order, so the fake used the order that the code expected.
3. Nothing in the plan required a real run before P2 ended.
4. The `slow` test came late, because the chart keeps it out of CI.
5. The execution plan has no step that runs the real model once while the code takes shape.

**Gap:** The plan skill has no cause that asks for one real-library run when tests inject a fake.

## Actions

| Type | Action | Status | Owner | Lives in | Verified by | Ref |
|------|--------|--------|-------|----------|-------------|-----|
| corrective | Sort the pass 1 stems by name and check sound in the instrumental only | done | step 2 | `src/stem-core/stem_core/separation.py` | `test_req_001_result_order_does_not_depend_on_the_separator_order` | commit 5261c07 |
| preventive | none, because the `slow` test now runs the real model and stays in the repo | none | none | none | none | none |
| detective | none, because the real run happened before P3 and caught both differences | none | none | none | none | none |
