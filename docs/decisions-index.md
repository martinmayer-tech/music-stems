# Decisions index

> Living document. Index of all ADRs across all features. Update it in place.

Last updated: 0000014-model-ensemble-options

## All architecture decision records

| ADR | Title | Feature | Status | Summary |
|-----|-------|---------|--------|---------|
| [ADR-0001](adr/0001-python-tooling.md) | Python tooling and layout | 0000002-python-scaffold | active | One root `pyproject.toml` with `pytest` and `ruff`, and one package folder for each component |
| [ADR-0002](adr/0002-separator-injection-and-pin.md) | Separator injection, lazy import, and a pinned extra | 0000004-separation-core | active | `split()` builds its separator through a factory, and the library installs from a pinned extra |
| [ADR-0003](adr/0003-stems-command-and-packaging.md) | The stems command and the stem_core package install | 0000006-command-line-interface | active | The command uses `argparse` with injectable probes, and a console script installs the packaged `stem_core` |
| [ADR-0004](adr/0004-sqlite-job-store-and-pooled-worker.md) | SQLite job store and a worker with a model pool | 0000008-job-queue-worker | active | `stem-service` owns the `jobs` table, and one worker for each device loads each model once |
| [ADR-0005](adr/0005-fastapi-api-on-loopback-with-no-login.md) | FastAPI HTTP API on the loopback address with no login | 0000010-http-api | active | `stem-service` serves four routes on `127.0.0.1`, adds no login, and serves stems only from a job's outputs |
| [ADR-0006](adr/0006-plain-web-page-served-by-the-api.md) | Plain web page served by the API | 0000012-web-front-end | active | `stem-web` holds a build-free page and `stem-service` serves it at `/` |
| [ADR-0007](adr/0007-allowlisted-model-options-in-stem-core.md) | Allowlisted model options in stem-core | 0000014-model-ensemble-options | active | `stem-core` holds the allowlists and checks each option before any model loads |

## Status definitions

| Status | Meaning |
|--------|---------|
| active | Decision stands, and implementation follows it |
| superseded | A later ADR replaced it |
| amended | The core decision stands, but conditions or scope changed |
