---
title: "Feature Brief - Add the HTTP API"
summary: "A FastAPI service in stem-service that accepts an upload, queues a job, reports status, and serves each stem as a WAV file."
status: "approved"
version: "0.1.0"
---
# Feature Brief - Add the HTTP API

**Feature ID:** 0000010-http-api

## Business Goal

No process outside Python can submit a job or fetch stems. The web page in step 6 needs an API to call. This step adds an HTTP API to `stem-service` that sits on the job store and the worker from step 4.

## Features

| Feature | User Stories | Priority | Wave |
|---------|-------------|----------|------|
| Upload | As a caller, I upload an audio file, so that the service queues a job for it. | must-have | 1 |
| Job status | As a caller, I read one job or the list of jobs, so that I can follow a job to `done` or `failed`. | must-have | 1 |
| Stem download | As a caller, I download each stem of a finished job, so that I get a WAV file. | must-have | 1 |
| Safe defaults | As an operator, I start the service, so that it binds to `127.0.0.1` and rejects unlisted or oversized uploads. | must-have | 1 |

## Waves

One wave. The feature ships when the observable condition passes.

## Target Architecture

### Components

| Component | Type | New or Existing | Responsibility |
|-----------|------|-----------------|---------------|
| stem-service | microservice | existing | Adds `stem_service/api.py`, which serves the HTTP API on the job store and the worker. |
| stem-core | component-pack | existing | Provides `split()`. The worker calls it. |

### Data Ownership

`stem-service` owns the SQLite table `jobs` and the data folder. The API writes uploads under `STEMS_DATA_DIR/uploads` and reads stems from `STEMS_DATA_DIR/jobs`. No other component writes them.

### Integration Points

| From | To | Method | Contract |
|------|-----|--------|----------|
| HTTP client | API | HTTP | `POST /jobs`, `GET /jobs`, `GET /jobs/{id}`, `GET /jobs/{id}/stems/{name}` |
| API | job store | Python call | `add()`, `get()`, `list()` |
| API | worker | Python call | `start_workers()`, `Worker.wake()`, `Worker.stop()` |

## Stack

| Concern | Decision |
|---------|----------|
| Language | Python |
| Runtime | Python 3.12 in CI, 3.13 locally |
| Framework | FastAPI, served by uvicorn |
| Frontend | none |
| Database | SQLite, one file |
| ORM | none |
| Testing | pytest with the FastAPI test client from httpx |
| IaC | none |
| Cloud | none |
| Compute | none |
| CI | GitHub Actions |
| Build target | ci-only |

## Scope Boundaries

### In Scope
- `POST /jobs`: accept one multipart upload and a `full_stems` flag, and queue a job.
- `GET /jobs` and `GET /jobs/{id}`: report job status.
- `GET /jobs/{id}/stems/{name}`: serve one stem as a WAV file.
- Upload validation: allowed extensions WAV, FLAC, MP3, and M4A, and a size limit from `STEMS_MAX_UPLOAD_MB` (default 500).
- A `python -m stem_service` entry point that binds to `127.0.0.1` and starts the worker.
- Unit tests with a fake separator and the test client.

### Out of Scope
- A login or any other auth.
- The web page, caller model choice, ensembles, cancel, and delete.
- A broker or more than one queue backend.

### Deferred
- The web page waits for step 6. Caller model choice waits for step 7.

## Non-Functional Requirements

| NFR | Target | Measurement |
|-----|--------|-------------|
| Exposure | The service binds to `127.0.0.1` unless the operator sets `STEMS_HOST` | A unit test reads the default host |
| Upload limit | An upload above `STEMS_MAX_UPLOAD_MB` gets status 413 and leaves no job | A test with a limit of 1 byte |
| Path safety | A stem request outside the job's output list gets status 404 | A test requests `../` names |

## Constraints and Assumptions

### Constraints
- Add no login. Bind to `127.0.0.1` by default.
- Accept WAV, FLAC, MP3, and M4A up to the limit from `STEMS_MAX_UPLOAD_MB`.
- The libraries are `fastapi`, `uvicorn`, `python-multipart`, and `httpx`. Add no other dependency.
- Unit tests inject a fake separator.

### Assumptions
- The service trusts a caller on the same host, because it has no login and binds to the loopback address.

## Scenario Paths

**Happy path:** A client uploads a WAV file, polls the job until `done`, and downloads each stem as a WAV file.

> The upload returns status 201 with a job id.

**First-run path:** `STEMS_DATA_DIR` holds no file. The app creates the folder, the database, and the `uploads` folder.

> The first job triggers the model download in `audio-separator`.

**Error / sad path:** A client uploads a `.txt` file, an oversized file, or asks for an unknown job or stem.

> The API answers 415, 413, or 404. It creates no job for a rejected upload.

**Cross-session continuity:** The service restarts while a job is `queued` or `running`.

> The worker requeues a `running` job. A client then reads the same job id and gets its result.

## Acceptance Criteria

- [ ] An upload returns a job id, and the job reaches `done`.
- [ ] Each stem of a `done` job downloads as a WAV file.
- [ ] An unlisted extension, an oversized upload, an unknown job, and an unknown stem each get a 4xx answer.
- [ ] The default host is `127.0.0.1`.
