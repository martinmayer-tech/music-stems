---
title: "Backlog Entry: 0000019 - Add a subprocess import note to the testing standards"
summary: "The testing standards say nothing about how a child process finds the packages under test, and two steps hit the same failure."
status: "open"
priority: "medium"
theme: "pipeline"
---
# Backlog Entry: 0000019 - Add a subprocess import note to the testing standards

**Source feature:** 0000008-job-queue-worker

**Source phase:** P2

**Deferral source:** discovered mid-flight

**Date filed:** 2026-11-16

---

## Problem

A test that starts a child Python to check `sys.modules` fails when the child cannot import the package under test. The pytest `pythonpath` setting applies to the test process only. Step 3 hit this with `python -I`, and step 4 hit it with no `PYTHONPATH`. `ravintio-zero/standards/testing-standards.md` has no note on either case.

## Suggested Action

Add a short note to `ravintio-zero/standards/testing-standards.md`. A subprocess test passes the package folder in the child's `PYTHONPATH` and avoids `-I`.

## Why Deferred

The change edits a pack standard, which lies outside the scope of the job queue step.

## Source retrospective

`plan/retrospectives/0000008-job-queue-worker-2026-11-16.md`. The postmortem is `plan/postmortems/2026-11-16-subprocess-import-without-pythonpath.md`.
