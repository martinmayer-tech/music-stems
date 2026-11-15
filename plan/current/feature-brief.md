---
title: "Feature Brief - Scaffold the Python project and its CI"
summary: "The Python project layout, test and lint tooling, and a CI job for the stem separation service."
status: "approved"
version: "0.1.0"
---
# Feature Brief - Scaffold the Python project and its CI

**Feature ID:** 0000002-python-scaffold

## Business Goal

The repo holds no application code, no Python project, and no version file. CI runs the pack checks only, so nothing lints or tests Python code. This step gives later steps a project layout, a test runner, a linter, and a CI job to build on.

## Features

| Feature | User Stories | Priority | Wave |
|---------|-------------|----------|------|
| Python project layout | As a developer, I run `pytest` and `ruff` from the repo root, so that every later step has one way to test and lint. | must-have | 1 |
| Python CI job | As a maintainer, I see a red check on a pull request with a failing test and a green check on one with passing tests, so that I trust each merge. | must-have | 1 |
| Product version record | As a maintainer, I read the product version from `docs/about.md` and `product.yml`, so that the merge queue can set it. | must-have | 1 |

## Waves

One wave.

## Target Architecture

### Components

| Component | Type | New or Existing | Responsibility |
|-----------|------|-----------------|----------------|
| `stem-core` | component-pack | new | Holds the separation function and the `stems` command in later steps |
| `stem-service` | microservice | new | Holds the job store, the worker, and the HTTP API in later steps |
| `stem-web` | microfrontend | new | Holds the web page in later steps |

### Data Ownership

None. Step 4 adds the first data store.

### Integration Points

None.

## Stack

| Concern | Decision |
|---------|----------|
| Language | Python 3.12 in CI, `requires-python >=3.10` |
| Framework | none |
| Database | none |
| Testing | pytest |
| Lint | ruff |
| CI | GitHub Actions |
| Build target | ci-only |

## Scope Boundaries

### In Scope
- One `pyproject.toml` at the repo root with `pytest` and `ruff` settings.
- A package skeleton and one smoke test for each of the three components.
- A Python CI job for pull requests to `initiative/**` and `main`.
- `docs/about.md` and `product.yml` at version `0.1.0`, with the three components listed.

### Out of Scope
- Any separation, CLI, queue, API, or web code.
- Docker files.

### Deferred
- `audio-separator` install. Step 2 adds it.

## Non-Functional Requirements

| NFR | Target | Measurement |
|-----|--------|-------------|
| CI check | A failing test gives a red Python check and a passing run gives a green one | Exact pass or fail on a pull request |

## Constraints and Assumptions

### Constraints
- Local runs use Python 3.13. CI uses Python 3.12.
- The product version never tracks the pack version.

### Assumptions
- `pytest` and `ruff` install from PyPI in CI.

## Scenario Paths

**Happy path:** A developer installs the dev tools, runs `ruff check .` and `pytest`, and both exit 0. CI does the same on a pull request.

> Same.

**First-run path:** A fresh clone has no virtual environment. The developer creates one and installs the dev extras from `pyproject.toml`.

> Same.

**Error / sad path:** A failing test or a lint error makes the CI job exit non-zero and the check turns red.

> Same.

**Cross-session continuity:** The step holds no runtime state. A restart resumes from the build log.

> Same.

## Acceptance Criteria

- [ ] A pull request with a failing unit test gets a red Python check.
- [ ] A pull request with passing tests and clean lint gets a green Python check.
- [ ] `ruff check .` and `pytest` exit 0 from the repo root.
- [ ] `product.yml` lists the three components, each with a valid `component.yml`.
- [ ] The merge queue sets version `0.1.0` in `docs/about.md` and `product.yml` at merge.
