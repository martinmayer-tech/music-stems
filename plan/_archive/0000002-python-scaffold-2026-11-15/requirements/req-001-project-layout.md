---
title: "Requirement: REQ-001 - Python project layout"
summary: "One pyproject.toml, three component packages, and one smoke test for each."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-001 - Python project layout

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000002-python-scaffold
**Source:** US-001
**Priority:** must-have

## User Story

As a developer, I run `pytest` and `ruff` from the repo root, so that every later step has one way to test and lint.

## Functional Requirements
- One `pyproject.toml` at the repo root sets `requires-python` to `>=3.10`.
- The `dev` extra lists `pytest` and `ruff`.
- Each of `stem-core`, `stem-service`, and `stem-web` holds a package with a `__version__` value and one smoke test.
- The pytest settings find the three component test folders from the repo root.

## Acceptance Criteria
- [ ] AC-1: Tests pass
  - Given a virtual environment with the dev extra installed
  - When the developer runs `pytest` from the repo root
  - Then the run exits 0 and collects one test for each component
- [ ] AC-2: Lint passes
  - Given the same environment
  - When the developer runs `ruff check .` from the repo root
  - Then the run exits 0

## Dependencies
- None.
