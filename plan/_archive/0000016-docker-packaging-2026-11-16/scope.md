---
title: "Scope - Add the Docker image and compose file"
summary: "Defines explicit boundaries of what is in scope and out of scope."
status: "active"
version: "0.1.0"
---
# Scope - Add the Docker image and compose file

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000016-docker-packaging
**Version:** 0.8.0

## In Scope

- The `Dockerfile`, the `.dockerignore` file, and the build arguments `STEMS_EXTRA` and `AUDIO_SEPARATOR_VERSION`.
- `compose.yaml` with a loopback port and two named volumes, and `compose.gpu.yaml` with an NVIDIA reservation.
- A `docker` job in the CI workflow that builds the CPU image.
- Tests that read the files as text, the component docs, the living docs, and ADR-0008.

## Out of Scope

- Publish the image to a registry: gap: out of scope.
- Run a separation in CI: gap: out of scope.
- A login, a reverse proxy, and a multi-container setup.

## Deferred

- Nothing deferred.
