---
title: "Postmortem: 2026-11-15 - Manifest wording test failed in the full suite"
summary: "A new component manifest carried a banned word and failed a pack test that the plan did not list."
status: "closed"
---
# Postmortem: 2026-11-15 - Manifest wording test failed in the full suite

> Path: `plan/postmortems/2026-11-15-manifest-wording-test.md`. Written by `ravintio-postmortem`.

**Trigger:** P2 self-correction
**Feature:** 0000002-python-scaffold
**Date:** 2026-11-15

## Summary

The full suite failed `test-0000042-req-010-pack-wording-allowlist.sh` after P2 added three manifests. The step removed the optional stack field and the test passed.

## Timeline

| Time | Event | Evidence |
|------|-------|----------|
| 2026-11-15T20:55:42Z | The plan listed the tests to run for the step | `plan/current/execution-plan.md`, section `## Test impact` |
| 2026-11-15T20:57:27Z | The affected tests ran and did not include the wording test | `plan/current/build-log.md`, the `Tests run: test impact` line |
| 2026-11-15T21:36:00Z | The full suite reported one new failure | `plan/current/build-log.md`, the `Tests run: full suite` line |
| 2026-11-15T21:36:31Z | The step removed the field and the test passed | commit `7df74c8` |

First missed chance to catch it: the P1 test impact scan could have listed the wording test.

## 5 whys

1. The full suite failed on three manifests that used a banned word.
2. The manifests copied an optional field from the component template.
3. The template field name is on the wording allowlist test's banned list.
4. The test impact scan has no cause for a new tracked file, so the plan did not list the test.
5. The affected-tests loop ran only listed tests, so the failure surfaced at the full suite.

**Gap:** The test impact scan in the plan skill has no cause for a run that adds a tracked file.

## Actions

| Type | Action | Status | Owner | Lives in | Verified by | Ref |
|------|--------|--------|-------|----------|-------------|-----|
| corrective | Remove the optional stack field from the three manifests | done | step 1 | `src/stem-core/component.yml` | The wording test passes | commit 7df74c8 |
| preventive | Add a tracked-file cause to the test impact scan | filed | pack maintainer | `ravintio-zero/skills/ravintio-plan/SKILL.md` | A test that lists the cause | backlog 0000018 |
| detective | none, because the full suite already caught the failure before P3 | none | none | none | none | none |
