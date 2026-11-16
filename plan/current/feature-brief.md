---
title: "Feature Brief - Add the Docker image and compose file"
summary: "A Dockerfile and a compose file run the service with one command. Two volumes keep the models and the jobs across restarts, and a build argument selects the GPU extra."
status: "approved"
version: "0.1.0"
---
# Feature Brief - Add the Docker image and compose file

**Feature ID:** 0000016-docker-packaging

## Business Goal

Running the service needs a manual Python and FFmpeg install. A container without a volume downloads every model again. This step packages the service so that `docker compose up` serves the page and keeps models and jobs across restarts.

## Features

| Feature | User Stories | Priority | Wave |
|---------|-------------|----------|------|
| Docker image | As a user, I build one image with Python 3.12 and FFmpeg, so that I install nothing by hand. | must-have | 1 |
| Compose file | As a user, I run `docker compose up`, so that the page opens on a local port and a restart keeps the models and the jobs. | must-have | 1 |
| CI image build | As a maintainer, I want CI to build the CPU image, so that a broken Dockerfile fails a pull request. | must-have | 1 |

## Waves

One wave. The feature ships when the observable condition passes.

## Target Architecture

### Components

| Component | Type | New or Existing | Responsibility |
|-----------|------|-----------------|---------------|
| stem-service | microservice | existing | Owns the `Dockerfile`, the `.dockerignore`, the compose files, and their docs. It still runs `python -m stem_service`. |

### Data Ownership

`stem-service` keeps ownership of the `jobs` table. The data volume holds its SQLite file and the job output. The model volume holds the downloaded models. The step adds no field.

### Integration Points

| From | To | Method | Contract |
|------|-----|--------|----------|
| Host | Container | Published port | `127.0.0.1:8000` on the host maps to port 8000 in the container |
| Container | Volumes | Mount | `/data` for `STEMS_DATA_DIR` and `/models` for `STEMS_MODEL_DIR` |

## Stack

| Concern | Decision |
|---------|----------|
| Language | Python, Dockerfile, YAML |
| Runtime | Python 3.12 in the image and in CI, 3.13 locally |
| Framework | FastAPI behind uvicorn, as in step 5 |
| Frontend | none |
| Database | SQLite, no schema change |
| ORM | none |
| Testing | pytest reads the Dockerfile and compose file as text. `docker build` runs in CI |
| IaC | dockerfile |
| Cloud | none |
| Compute | docker |
| CI | GitHub Actions |
| Build target | docker |

## Scope Boundaries

### In Scope
- A `Dockerfile` on `python:3.12-slim` that installs FFmpeg and the service.
- A build argument that selects the `cpu` or `gpu` extra of `audio-separator`.
- A `compose.yaml` with one named volume for models and one for job data.
- A `compose.gpu.yaml` override that reserves an NVIDIA device.
- A `.dockerignore` file.
- A CI job that builds the CPU image on a pull request.
- Tests, component docs, living docs, and an ADR.

### Out of Scope
- Publishing the image to a registry.
- Running a separation in CI.
- A login or a reverse proxy.
- A multi-container setup.

### Deferred
- Nothing deferred.

## Non-Functional Requirements

| NFR | Target | Measurement |
|-----|--------|-------------|
| Loopback publish | The compose file publishes the port on `127.0.0.1` only | A test reads the port line |
| Persistence | A restart keeps the models and the finished jobs | A local run restarts the stack and lists the job |

## Constraints and Assumptions

### Constraints
- Add no login. The container binds to all interfaces, and the compose file limits the host side to `127.0.0.1`.
- The image pins `audio-separator` to the version in `pyproject.toml`.
- CI builds the CPU image only and runs no separation in it.
- Publish no image.

### Assumptions
- The GPU image needs the NVIDIA container toolkit on the host. CI never checks it.

## Scenario Paths

**Happy path:** A user runs `docker compose up --build`. The page opens on `http://127.0.0.1:8000`, and an upload ends `done`.

> The first job downloads its models into the model volume.

**First-run path:** A user starts the stack with no volume. Docker creates both volumes, and the service starts with an empty job list.

> The first split takes longer, because each model downloads once.

**Error / sad path:** A user builds the GPU image on a host with no NVIDIA toolkit. The build still works, and the service fails at the first job with the engine's error.

> The docs name the toolkit as a prerequisite.

**Cross-session continuity:** A user runs `docker compose down` and then `up`. The job list and the models remain.

> `docker compose down -v` removes the volumes on purpose.

## Acceptance Criteria

- [ ] `docker build` of the CPU image succeeds.
- [ ] `docker compose up` serves the page on a local port.
- [ ] A restart keeps the downloaded models and the finished jobs.
- [ ] A build argument selects the GPU extra.
