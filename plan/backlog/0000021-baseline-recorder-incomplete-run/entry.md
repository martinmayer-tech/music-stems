---
title: "Backlog Entry: 0000021 - Refuse an unfinished run in the baseline recorder"
summary: "baseline-failures.mjs record accepts output from a suite run that has not ended and stores too few failures."
status: "open"
priority: "medium"
theme: "pipeline"
---
# Backlog Entry: 0000021 - Refuse an unfinished run in the baseline recorder

**Source feature:** 0000012-web-front-end

**Source phase:** P0

**Deferral source:** discovered mid-flight

**Date filed:** 2026-11-16

---

## Problem

`node ravintio-zero/scripts/baseline-failures.mjs record` read the output of a clean-clone run that was still going. It stored 0 failures and exited 0. The finished run held 59. P3 would have reported 59 inherited failures as new.

## Suggested Action

Make `record` exit non-zero when the output has no final summary line, such as `One or more tests failed.` or the all-passed line. Add a test with a truncated output file.

**Observable condition:** `record` on a truncated output file exits non-zero and writes no baseline file.

## Why Deferred

The step's scope is the web page. The recorder belongs to the pack. Source retrospective: `plan/retrospectives/0000012-web-front-end-2026-11-16.md`.
