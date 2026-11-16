# Architecture overview

> Living document. Reflects current system state.

Last updated: 0000010-http-api

## System summary

Music Stems is a self-hosted service that splits a mix into stems. The repo holds a Python project with three components and a CI job that lints and tests them. `stem-core` holds the two-pass `split()` function and the `stems` command. `stem-service` holds the job store, the worker, and the HTTP API.

## Components

| Component | Type | Purpose | Status |
|-----------|------|---------|--------|
| stem-core | component-pack | The two-pass separation function and the `stems` command | active (`split()` and the `stems` command built) |
| stem-service | microservice | The job store, the worker, and the HTTP API | active (job store, worker, and HTTP API built) |
| stem-web | microfrontend | The web page that the API serves | planned |

## Communication patterns

```mermaid
flowchart LR
    A[stem-web] -->|HTTP| B[stem-service]
    B -->|import| C[stem-core]
    B --- D[(jobs.sqlite3)]
```

## Data ownership

| Data | Owner | Where |
|------|-------|-------|
| `jobs` table | stem-service | `STEMS_DATA_DIR/jobs.sqlite3` |
| Uploaded files | stem-service | `STEMS_DATA_DIR/uploads` |

## External dependencies

| Dependency | Type | Components that use it |
|-----------|------|----------------------|
| pytest | PyPI, development | stem-core, stem-service, stem-web |
| ruff | PyPI, development | stem-core, stem-service, stem-web |
| audio-separator[cpu]==0.48.0 | PyPI, runtime, `separation` extra | stem-core |
| fastapi, uvicorn, python-multipart | PyPI, runtime, `service` extra | stem-service |
| httpx | PyPI, development | stem-service |

## Key architectural decisions

- ADR-0001: One root `pyproject.toml` with `pytest` and `ruff` serves all components.
- ADR-0002: `split()` takes an injectable separator factory, imports `audio_separator` late, and installs it from a pinned `separation` extra.
- ADR-0003: The `stems` command uses `argparse` with injectable probes, and a console script installs it from the packaged `stem_core`.
- ADR-0004: `stem-service` owns a SQLite `jobs` table. One worker thread for each device runs jobs through a pool that loads each model once.
- ADR-0005: `stem-service` serves a FastAPI app on `127.0.0.1` with no login. A stem request resolves only against a job's stored outputs.
