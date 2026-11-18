---
title: "ADR 0009: Pin audioread beside the engine"
summary: "The separation extra and the Dockerfile install audioread at one exact version, because the pinned engine imports it and nothing else installs it."
status: "accepted"
component: "stem-core"
version: "0.8.1"
---
# ADR-0009 - Pin audioread beside the engine

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000029-add-audioread
**Component:** stem-core
**File:** `docs/adr/0009-pin-audioread-beside-the-engine.md`
**Date:** 2026-11-18

## Context

A job in the built image ends `failed` with `No module named 'audioread'`. `audio-separator` 0.48.0 imports `audioread`, and `librosa` 1.0.1 no longer installs it. ADR-0002 pins the engine to one exact version. ADR-0008 makes the `Dockerfile` install the engine by name, not through the `separation` extra, so that a build argument can select the GPU extra.

## Decision

The project names `audioread` as a direct dependency at one exact version.

- The `separation` extra in `pyproject.toml` lists `audioread==3.1.0` after the engine pin.
- The `Dockerfile` holds the build argument `AUDIOREAD_VERSION` and installs `audioread==${AUDIOREAD_VERSION}` in the engine's layer.
- A test keeps `AUDIOREAD_VERSION` equal to the version in the extra.
- The human approved the library at the design gate of feature 0000029-add-audioread.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| Move the engine pin to a release that declares `audioread` | No extra pin | A new engine version needs a full rerun of the model checks | The design keeps the engine at 0.48.0 |
| Pin `librosa` below 1.0 | No new direct dependency | It holds back a library the engine chose | The engine's own import is the gap |
| Install `audioread` with no version | One shorter line | A later release can change behaviour unseen | ADR-0002 sets exact pins for the engine path |
| Make the `Dockerfile` install the `separation` extra | One pin in one file | The extra names the CPU build, so the GPU argument stops working | ADR-0008 keeps the build argument |

## Affected Components

| Component | Impact |
|-----------|--------|
| stem-core | The `separation` extra gains `audioread` |
| stem-service | The `Dockerfile` gains a build argument and installs `audioread` |

## Consequences

**Positive:**
- A fresh image separates a track with no manual install.
- A local install of the `separation` extra works on Python 3.13.

**Negative:**
- A second pin now appears in two files.
- The project carries a library that the engine ought to declare.

**Risks:**
- A later engine release declares its own `audioread` range, and the exact pin conflicts with it.

## Related ADRs

- ADR-0002 sets the engine pin.
- ADR-0008 sets the image and its build arguments.

## Supersedes

- None.

## Superseded By

- None.
