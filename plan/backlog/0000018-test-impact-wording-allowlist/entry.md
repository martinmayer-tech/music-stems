---
title: "Backlog Entry: 0000018 - Add the wording allowlist test to the test impact scan"
summary: "The plan skill's test impact scan misses the wording allowlist test that fails on a new tracked file."
status: "open"
priority: "medium"
theme: "pipeline"
---
# Backlog Entry: 0000018 - Add the wording allowlist test to the test impact scan

**Source feature:** 0000002-python-scaffold

**Source phase:** P2

**Deferral source:** discovered mid-flight

**Date filed:** 2026-11-15

---

## Problem

`ravintio-zero/tests/test-0000042-req-010-pack-wording-allowlist.sh` searches every tracked file for a banned word. A new `component.yml` copied from `ravintio-zero/templates/component.template.yml` carries the optional stack field that holds the word. The test failed in the full suite and not in the affected tests. The `## Test impact` scan in `ravintio-zero/skills/ravintio-plan/SKILL.md` has no cause that lists this test.

## Suggested Action

Add a cause to the scan: the run adds a tracked file. List `test-0000042-req-010-pack-wording-allowlist.sh` for it. Also consider removing the field from the component template.

## Why Deferred

The change edits a pack skill, which lies outside the scope of the Python scaffold step.

## Source retrospective

`plan/retrospectives/0000002-python-scaffold-2026-11-15.md`. The postmortem is `plan/postmortems/2026-11-15-manifest-wording-test.md`.
