---
title: "Feature Brief - Add audioread to the image and the separation extra"
summary: "A pinned audioread in the separation extra and the Dockerfile lets a job in a fresh image end done."
status: "approved"
version: "0.1.0"
---
# Feature Brief - Add audioread to the image and the separation extra

**Feature ID:** 0000029-add-audioread

## Business Goal

A job in the built image ends `failed` with `No module named 'audioread'`. `audio-separator` 0.48.0 imports `audioread`, and `librosa` 1.0.1 no longer installs it. This run pins `audioread` so that a fresh image separates a track with no manual install.

The run folds in backlog entry 0000023, filed by feature 0000016-docker-packaging.

## Features

| Feature | User Stories | Priority | Wave |
|---------|-------------|----------|------|
| Pinned `audioread` | As a user, I run `docker compose up --build` and upload a track, so that the job ends `done` with no manual install. | must-have | 1 |
| Local install | As a developer, I install the `separation` extra, so that a local `stems split` finds `audioread`. | must-have | 1 |

## Waves

One wave. The feature ships when the acceptance criteria pass.

## Target Architecture

### Components

| Component | Type | New or Existing | Responsibility |
|-----------|------|-----------------|---------------|
| stem-core | component-pack | existing | Owns the `separation` extra in the root `pyproject.toml` and its dependency doc. |
| stem-service | microservice | existing | Owns the `Dockerfile`, its tests, and its dependency doc. |

### Data Ownership

No change.

### Integration Points

No change.

## Stack

| Concern | Decision |
|---------|----------|
| Language | Python, Dockerfile |
| Runtime | Python 3.12 in the image and in CI, 3.13 locally |
| Framework | FastAPI behind uvicorn, unchanged |
| Frontend | none |
| Database | SQLite, no schema change |
| ORM | none |
| Testing | pytest reads `pyproject.toml` and the `Dockerfile` as text. One real job runs by hand |
| IaC | dockerfile |
| Cloud | none |
| Compute | docker |
| CI | GitHub Actions |
| Build target | local |

## Scope Boundaries

### In Scope
- `audioread==3.1.0` in the `separation` extra.
- An `AUDIOREAD_VERSION` build argument in the `Dockerfile`, and its install.
- A test that compares the two pins.
- The dependency docs of `stem-core` and `stem-service`.
- One real job through a fresh image, run by hand.
- The removal of backlog entry 0000023.

### Out of Scope
- A newer `audio-separator`.
- A separation run in CI.
- A run of the GPU image.
- The pack gaps in backlog entries 0000018 to 0000030.

### Deferred
- Nothing deferred.

## Non-Functional Requirements

| NFR | Target | Measurement |
|-----|--------|-------------|
| Pin parity | The `Dockerfile` and `pyproject.toml` name one `audioread` version | A test compares the two |

## Constraints and Assumptions

### Constraints
- Keep the `audio-separator` pin at 0.48.0.
- Change no model, no API, and no page.

### Assumptions
- `audioread` 3.1.0 works with `audio-separator` 0.48.0 on Python 3.12.

## Scenario Paths

**Happy path:** A user runs `docker compose up --build` and uploads a track. The job ends `done` with `vocals.wav` and `instrumental.wav`.

> The first job downloads its models into the model volume.

**First-run path:** A user builds the image for the first time. The build installs `audioread` with the engine.

> No extra command follows the build.

**Error / sad path:** The engine misses another module. The job ends `failed` and the API reports the engine's error line.

> The run reports the module and files it.

**Cross-session continuity:** A user rebuilds the image. The rebuilt image still holds `audioread`.

> The models and the jobs stay in their volumes.

## Acceptance Criteria

- [ ] The `separation` extra in `pyproject.toml` pins `audioread` with `==`.
- [ ] The `Dockerfile` installs `audioread` at the same version, and a test compares the two pins.
- [ ] A job uploaded to a fresh image from `docker compose up --build` ends `done` with `vocals.wav` and `instrumental.wav`.
