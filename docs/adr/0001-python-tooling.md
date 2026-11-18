---
title: "ADR 0001: Python tooling and layout"
summary: "Use one root pyproject.toml with pytest and ruff, and one package folder for each component under src/."
status: "accepted"
component: "stem-core"
version: "0.1.0"
---
# ADR-0001 - Python tooling and layout

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000002-python-scaffold
**Component:** stem-core, stem-service, stem-web
**File:** `docs/adr/0001-python-tooling.md`
**Date:** 2026-11-15

## Context

The repo holds no Python code. Eight steps add three components. Each step needs one way to lint and test, and one CI job to run both.

## Decision

Use one `pyproject.toml` at the repo root. Set `requires-python` to `>=3.10`, so local Python 3.13 and CI Python 3.12 both work. List `pytest` and `ruff` in a `dev` extra. Each component lives at `src/{component-id}/` with its package at `src/{component-id}/{package}/` and its tests at `src/{component-id}/tests/`. Package names use underscores, as in `stem_core`. Pytest finds each component through the `pythonpath` setting. CI runs `ruff check .` and then `pytest` in one job named `python`.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| One `pyproject.toml` for each component | Each component installs alone | Three files to keep in step, and three CI runs | The service is one product with one version |
| `tox` or `nox` | Matrix runs across Python versions | A new dependency that the chart does not approve | The chart pins Python 3.12 for CI |
| `flake8` and `black` | Familiar tools | Two tools where `ruff` covers both | `ruff` lints and formats in one tool |

## Affected Components

| Component | Impact |
|-----------|--------|
| stem-core | Gets a package skeleton and a smoke test |
| stem-service | Gets a package skeleton and a smoke test |
| stem-web | Gets a package skeleton and a smoke test |

## Consequences

**Positive:**
- Later steps add code and tests with no new tooling work.
- One CI job covers every component.

**Negative:**
- The three components share one dependency set until a step splits it.

**Risks:**
- A `ruff` run over the whole repo can read pack files. The config excludes `ravintio-zero` and `plan`.

## Related ADRs

- None.

## Supersedes

- None.

## Superseded By

- None.
