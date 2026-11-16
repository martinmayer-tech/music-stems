---
title: "ADR 0008: Docker packaging of the service"
summary: "One image runs the service as a non-root user, two named volumes keep models and jobs, and the compose file publishes on loopback only."
status: "proposed"
component: "stem-service"
version: "0.8.0"
---
# ADR-0008 - Docker packaging of the service

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000016-docker-packaging
**Component:** stem-service
**File:** `docs/adr/0008-docker-packaging-of-the-service.md`
**Date:** 2026-11-16

## Context

Running the service needs a manual Python and FFmpeg install. A container without a volume downloads every model again. ADR-0005 sets a loopback bind with no login, so a container that binds to all interfaces must not widen who can reach it.

## Decision

`stem-service` owns a `Dockerfile` and two compose files at the repo root.

- The image starts from `python:3.12-slim` and installs `ffmpeg`. It installs the `service` extra and `audio-separator[${STEMS_EXTRA}]`, with `cpu` as the default and `gpu` as the alternative.
- The `pip install` layer adds `gcc` and removes it again, because the dependency `diffq` builds from source.
- The build argument `AUDIO_SEPARATOR_VERSION` repeats the pin of `pyproject.toml`, and a test keeps them equal.
- The image sets `STEMS_HOST=0.0.0.0`, `STEMS_DATA_DIR=/data`, and `STEMS_MODEL_DIR=/models`. It runs as a non-root user.
- `compose.yaml` publishes `127.0.0.1:8000` only, and mounts the named volumes `models` and `data`. `compose.gpu.yaml` reserves an NVIDIA device.
- CI builds the CPU image and runs no container. The project publishes no image.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| Bind to `127.0.0.1` in the container | Keeps the default bind | The published port never reaches a loopback bind inside the container | Docker forwards to the container address |
| Bind-mount host folders | The user sees the files | Host permissions block the non-root user | Named volumes inherit the image ownership |
| Publish the image | Users skip the build | Needs a registry and a release flow | The chart says publish no image |

## Affected Components

| Component | Impact |
|-----------|--------|
| stem-service | Gains the `Dockerfile`, the compose files, and their docs |

## Consequences

**Positive:**
- One command starts the service, and a restart keeps models and jobs.
- CI catches a broken Dockerfile.

**Negative:**
- The image is large because the engine pulls PyTorch.
- The pin appears in two files.

**Risks:**
- A user who edits the port line to drop `127.0.0.1` exposes an upload service with no login.

## Related ADRs

- ADR-0002 sets the engine pin.
- ADR-0005 sets the loopback bind and no login.

## Supersedes

- None.

## Superseded By

- None.
