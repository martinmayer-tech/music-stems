---
title: "Retrospective: 2026-11-15 - Command-line interface"
summary: "A blameless review of step 3 of the stem separation initiative, and the change it files."
status: "open"
---
# Retrospective: 2026-11-15 - Command-line interface

**Mode:** run
**Subject:** 0000006-command-line-interface
**Date:** 2026-11-15

## Summary

The step added the `stems` command with `split`, `env`, and `models`, a console script, and the package install. CI passed on the first run. The two full suite runs took about 50 of the 52 minutes.

## What helped

- The chart's Decisions rows named `argparse` and the Python target, so the step stopped for no question (`plan/_archive/0000006-command-line-interface-2026-11-15/build-log.md`, the `Decision applied` lines).
- Injected `split_func` and probes kept every test free of models and machine facts (`src/stem-core/tests/test_cli.py`).
- A scratch install of the built package showed the console script worked before CI ran (`verification-report.md` in the archive).

## What slowed the work

- Each full pack suite run in a clean clone took 22 to 28 minutes, and 57 inherited failures hide in them (`build-report.md`, section Inherited failures).
- The first subprocess test failed because `python -I` ignores `PYTHONPATH` (`plan/postmortems/2026-11-15-isolated-subprocess-test.md`).

## Keep

- Inject every machine-dependent fact as an argument, so unit tests need no tool and no model.

## Change

- Add a line to the testing standards that `python -I` ignores `PYTHONPATH` in subprocess tests.

## Actions

| Change | Owner | Lives in | Verified by | Filed as |
|--------|-------|----------|-------------|----------|
| Note the `python -I` and `PYTHONPATH` interaction in the testing standards | none, because the standard is a pack file and the step's scope excludes pack changes | none | none | none, because the step's scope excludes pack changes |
