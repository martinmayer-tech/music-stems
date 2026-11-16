---
title: "Feature Brief - Add the job queue and worker"
summary: "A SQLite job store and a worker in stem-service that run separation jobs one at a time and load each model once."
status: "approved"
version: "0.1.0"
---
# Feature Brief - Add the job queue and worker

**Feature ID:** 0000008-job-queue-worker

## Business Goal

Each `split()` call loads its models again, and two calls can compete for one GPU. The guide asks for a queue and a model that loads once per worker. This step adds a job store and a worker to `stem-service`, so the HTTP API in step 5 can queue uploads.

## Features

| Feature | User Stories | Priority | Wave |
|---------|-------------|----------|------|
| Job store | As a caller, I add a job and read its status, so that I can follow it from `queued` to `done` or `failed`. | must-have | 1 |
| Durable jobs | As a caller, I restart the service, so that queued jobs still run and a half-run job runs again. | must-have | 1 |
| Worker | As a caller, I queue two jobs, so that they run one after the other and never overlap. | must-have | 1 |
| Model reuse | As a caller, I queue two jobs, so that the second loads no model that the first already loaded. | must-have | 1 |

## Waves

One wave. The feature ships when both observable conditions pass.

## Target Architecture

### Components

| Component | Type | New or Existing | Responsibility |
|-----------|------|-----------------|---------------|
| stem-service | microservice | existing | Holds the job store and the worker. Step 5 adds the HTTP API. |
| stem-core | component-pack | existing | Provides `split()`. The worker calls it. |

### Data Ownership

`stem-service` owns the SQLite table `jobs`. No other component writes it.

### Integration Points

| From | To | Method | Contract |
|------|-----|--------|----------|
| worker | `split()` | Python call | `split(mix, out, full_stems, separator_factory)` |
| worker | job store | Python call | `claim_next()`, `mark_done()`, `mark_failed()` |

## Stack

| Concern | Decision |
|---------|----------|
| Language | Python |
| Runtime | Python 3.12 in CI, 3.13 locally |
| Framework | none. `sqlite3` and `threading` from the standard library |
| Frontend | none |
| Database | SQLite, one file |
| ORM | none |
| Testing | pytest |
| IaC | none |
| Cloud | none |
| Compute | none |
| CI | GitHub Actions |
| Build target | ci-only |

## Scope Boundaries

### In Scope
- A `jobs` table in one SQLite file under `STEMS_DATA_DIR`, and a `JobStore` class.
- A `Worker` class that runs queued jobs one at a time on its own thread, and a helper that starts one worker per device.
- A separator cache that loads each model once per worker.
- Recovery of jobs that a restart interrupted.
- Unit tests with a fake separator.

### Out of Scope
- The HTTP API, uploads, and the web page.
- Caller model choice and ensembles.
- A broker or more than one queue backend.

### Deferred
- The HTTP API waits for step 5. Caller model choice waits for step 7.

## Non-Functional Requirements

| NFR | Target | Measurement |
|-----|--------|-------------|
| Isolation | Two jobs never overlap in run time on one worker | A unit test records start and end times with a fake separator |
| Durability | A committed job survives a restart | A unit test reopens the file and reads the job |
| Start-up cost | Importing the package loads no model library | A unit test checks `sys.modules` |

## Constraints and Assumptions

### Constraints
- Use one SQLite file and one worker thread per device. Add no broker.
- Read `STEMS_DATA_DIR`, default `./data`. Read `STEMS_MODEL_DIR` for models.
- Add no dependency. Unit tests inject a fake separator.

### Assumptions
- An `audio-separator` `Separator` object lets the caller change `output_dir` between runs. A test with a fake separator cannot confirm it.

## Scenario Paths

**Happy path:** A caller adds two jobs. The worker runs the first, then the second. Each job ends as `done` with its output paths.

> The second job loads no model that the first loaded.

**First-run path:** `STEMS_DATA_DIR` holds no file. The store creates the folder, the file, and the table.

> The first job triggers the model download in `audio-separator`.

**Error / sad path:** A job names a file that does not exist, or the separator raises.

> The job ends as `failed` with one error line. The worker goes on to the next job.

**Cross-session continuity:** The service stops while a job is `running` or `queued`.

> On start, a `running` job returns to `queued`. The worker then runs every queued job.

## Acceptance Criteria

- [ ] Two jobs queued together never overlap in run time.
- [ ] The second job loads no model that the first already loaded.
- [ ] A job moves through `queued`, `running`, and `done`, or ends as `failed` with an error.
- [ ] A job survives a restart of the store.
