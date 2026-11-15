# Architecture overview

> Living document. Reflects current system state.

Last updated: 0000004-separation-core

## System summary

Music Stems is a self-hosted service that splits a mix into stems. The repo holds a Python project with three components and a CI job that lints and tests them. `stem-core` holds the two-pass `split()` function.

## Components

| Component | Type | Purpose | Status |
|-----------|------|---------|--------|
| stem-core | component-pack | The two-pass separation function and the `stems` command | active (`split()` built, command planned) |
| stem-service | microservice | The job store, the worker, and the HTTP API | planned |
| stem-web | microfrontend | The web page that the API serves | planned |

## Communication patterns

```mermaid
flowchart LR
    A[stem-web] -->|HTTP| B[stem-service]
    B -->|import| C[stem-core]
```

## Data ownership

No component owns data yet.

## External dependencies

| Dependency | Type | Components that use it |
|-----------|------|----------------------|
| pytest | PyPI, development | stem-core, stem-service, stem-web |
| ruff | PyPI, development | stem-core, stem-service, stem-web |
| audio-separator[cpu]==0.48.0 | PyPI, runtime, `separation` extra | stem-core |

## Key architectural decisions

- ADR-0001: One root `pyproject.toml` with `pytest` and `ruff` serves all components.
- ADR-0002: `split()` takes an injectable separator factory, imports `audio_separator` late, and installs it from a pinned `separation` extra.
