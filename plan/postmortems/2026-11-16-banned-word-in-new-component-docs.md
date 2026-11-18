---
title: "Postmortem: 2026-11-16 - A banned word reached two stem-web files"
summary: "The wording allowlist suite flagged the word framework in a manifest and a risk doc. The agent found it only in the full suite run."
status: "closed"
---
# Postmortem: 2026-11-16 - A banned word reached two stem-web files

> Path: `plan/postmortems/2026-11-16-banned-word-in-new-component-docs.md`. Written by `ravintio-postmortem`.

**Trigger:** P2 self-correction
**Feature:** 0000012-web-front-end
**Date:** 2026-11-16

## Summary

`src/stem-web/component.yml` and `src/stem-web/docs/risk.md` listed "a framework" as out of scope. The suite `test-0000042-req-010-pack-wording-allowlist.sh` bans that word outside an allowlist. The step found it in the 20-minute full suite run. Both files now say "a UI library".

## Timeline

| Time | Event | Evidence |
|------|-------|----------|
| 2026-11-16T01:36:00Z | The step wrote both files and committed | commit "Document the web front end" |
| 2026-11-16T01:57:34Z | The full suite reported one new failure that named both files | build-log line `Rework: U4-docs` |
| 2026-11-16T01:57:34Z | The step replaced the word and the suite passed | `ravintio-zero/tests/test-0000042-req-010-pack-wording-allowlist.sh` |

First missed chance to catch it: the Test impact scan. It listed the suite for a new tracked file, but nobody ran it before the docs commit.

## 5 whys

1. The full suite failed because two tracked files held a banned word.
2. The author used the common name for the concept.
3. The plan listed the suite under U4-docs, but P2 runs it only in the full run.
4. The full run is the first and only time that the suites run, so a quick suite waits 20 minutes.
5. The Test impact table names suites but the implement skill does not say to run a named suite at the unit's commit.

**Gap:** The implement skill asks for the suites in `## Test impact` before the full suite, but it gives no step for a docs-only unit.

## Actions

| Type | Action | Status | Owner | Lives in | Verified by | Ref |
|------|--------|--------|-------|----------|-------------|-----|
| corrective | Replace the word in both files | done | step 6 | `src/stem-web/component.yml`, `src/stem-web/docs/risk.md` | `test-0000042-req-010-pack-wording-allowlist.sh` | commit "Fix wording and the baseline record" |
| preventive | none, because the pack rule already says to run the named suites first and the step skipped it | none | none | none | none | none |
| detective | none, because the full suite caught it before ship | none | none | none | none | none |
