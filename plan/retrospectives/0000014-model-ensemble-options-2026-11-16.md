---
title: "Retrospective: 2026-11-16 - Add model choice and ensemble options"
summary: "A blameless review of step 7, which added the model options, and the change it files."
status: "open"
---
# Retrospective: 2026-11-16 - Add model choice and ensemble options

> Path: `plan/retrospectives/0000014-model-ensemble-options-2026-11-16.md`. Written by `ravintio-retrospective`.
> Blameless: a cause names a gap in a process, check, standard, or tool. Never name a person or an agent.

**Mode:** run
**Subject:** 0000014-model-ensemble-options
**Date:** 2026-11-16

## Summary

The step added the allowlists, the options in `split()`, the command, the API, the worker, and the page in five phases with two self-corrections. The PR page holds the CI result.

## What helped

- Reading `ensemble_presets.json` from the pinned wheel in P0 gave the real preset names. It also showed that a preset replaces only the default pass 1 model (`plan/_archive/0000014-model-ensemble-options-2026-11-16/discovery.md`).
- One check in `stem-core` served the command, the API, and the worker, so a bad value failed before any model loaded in each path (`src/stem-core/tests/test_options.py`).
- A live service and a browser run observed the 6-stem job, the 422 answer, and the 7 players (`plan/_archive/0000014-model-ensemble-options-2026-11-16/verification-report.md`).

## What slowed the work

- An existing test counted the lines of `stems models`. The plan said all existing tests pass unchanged. P2 found the break (build log, `Deviation:` line).
- The docs unit had no RED line, so the build log check failed at ship. A test of the docs fixed it (build log, second `Deviation:` line).
- The shell guard blocked commands that wrote to a relative path or used a variable with `git add`. The agent rewrote them with absolute and literal paths.

## Keep

- Read the pinned engine package for names and defaults before the design, because tests with fakes cannot show a wrong name.

## Change

- Add a cause to the test impact scan for a run that changes the output of a command or a listing. Backlog entry 0000022 holds this change (`plan/backlog/0000022-test-impact-listing-assertions/entry.md`).

## Actions

| Change | Owner | Lives in | Verified by | Filed as |
|--------|-------|----------|-------------|----------|
| Scan for tests that count output lines | pack maintainer | `ravintio-zero/skills/ravintio-plan/SKILL.md` | The scan lists `test_cli.py` for a run that extends `stems models` | `plan/backlog/0000022-test-impact-listing-assertions/entry.md`, from `plan/retrospectives/0000014-model-ensemble-options-2026-11-16.md` |
