---
title: "Backlog Entry: 0000003 - Python scaffold and CI"
summary: "Python scaffold and CI for the self-hosted stem separation service."
status: "open"
priority: "high"
theme: "stem-separation"
---
# Backlog Entry: 0000003 - Python scaffold and CI

**Source feature:** none (human request)

**Source phase:** none (human request)

**Deferral source:** human request

**Date filed:** 2026-11-15

---

## Problem

The repo holds no application code, no Python project, and no version file. CI runs the pack checks only, so nothing lints or tests Python code.

## Suggested Action

Create the Python project layout under `src/` with one `pyproject.toml`, `pytest`, and `ruff`. Add a CI job that runs lint and unit tests on pull requests to `initiative/**` and `main`. Create `docs/about.md` and `product.yml` at version `0.1.0`.

**Observable condition:** a pull request with a failing unit test gets a red Python check, and one with passing tests gets a green check.

## Why Deferred

The human asked for the solution as one initiative. Initiative 0000001 runs this entry as its own step.
