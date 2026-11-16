---
title: "Backlog Entry: 0000022 - Scan for tests that count output lines"
summary: "The plan test impact scan never names a test that counts the lines of a command listing, so a change that adds lines breaks it unseen."
status: "open"
priority: "low"
theme: "pipeline"
---
# Backlog Entry: 0000022 - Scan for tests that count output lines

**Source feature:** 0000014-model-ensemble-options

**Source phase:** P2

**Deferral source:** discovered mid-flight

**Date filed:** 2026-11-16

---

## Problem

The step added lines to the `stems models` listing. An existing test counted exactly two lines and failed. The test impact scan in P1 greps for ids and file names, so it found no such test. The plan said all existing tests pass unchanged, and P2 found the break.

## Suggested Action

Add a cause to the test impact scan in `ravintio-plan`: the run changes the output of a command or a listing. The scan then greps the test folders for the command name and for `splitlines()` counts.

**Observable condition:** the scan lists `test_cli.py` in the test impact table for a run that extends `stems models`.

## Why Deferred

The step's scope is model options. The scan belongs to the pack. Source retrospective: `plan/retrospectives/0000014-model-ensemble-options-2026-11-16.md`.
