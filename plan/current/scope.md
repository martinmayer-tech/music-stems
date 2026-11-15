---
title: "Scope - Scaffold the Python project and its CI"
summary: "Defines explicit boundaries of what is in scope and out of scope."
status: "active"
version: "0.1.0"
---
# Scope - Scaffold the Python project and its CI

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000002-python-scaffold
**Version:** 0.1.0

## In Scope

- A root `pyproject.toml` with `pytest` and `ruff` settings and a `dev` extra.
- Package skeletons and one smoke test for `stem-core`, `stem-service`, and `stem-web`.
- A `component.yml` and a `docs/README.md` for each component.
- A `python` job in `.github/workflows/ravintio.yml`.
- The three components listed in `product.yml`.
- Ignore rules for Python build and cache folders.

## Out of Scope

- Separation, CLI, queue, API, and web code.
- Docker files.
- Publishing a package.

## Deferred

- The `audio-separator` install waits for step 2, which pins the version.
