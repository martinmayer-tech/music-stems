---
title: "Requirement: REQ-002 - Compose file"
summary: "compose.yaml runs the service on 127.0.0.1 with one volume for models and one for job data, and compose.gpu.yaml reserves an NVIDIA device."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-002 - Compose file

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000016-docker-packaging
**Source:** US-002
**Priority:** must-have

## User Story

As a user, I run `docker compose up`, so that the page opens on a local port and a restart keeps the models and the jobs.

## Functional Requirements
- `compose.yaml` builds the `Dockerfile` and passes `STEMS_EXTRA`, which defaults to `cpu`.
- It publishes `127.0.0.1:${STEMS_PORT:-8000}` to port 8000 in the container.
- It mounts the named volume `models` at `/models` and the named volume `data` at `/data`.
- It sets `restart: unless-stopped`.
- `compose.gpu.yaml` reserves one NVIDIA GPU and sets `STEMS_EXTRA` to `gpu`.

## Acceptance Criteria
- [ ] AC-1: Publish on loopback only
  - Given the `compose.yaml` text
  - When a test reads the port line
  - Then the host side starts with `127.0.0.1`
- [ ] AC-2: Mount both volumes
  - Given the `compose.yaml` text
  - When a test reads it
  - Then `models` mounts at `/models` and `data` mounts at `/data`, and the file declares both as named volumes
- [ ] AC-3: Select the GPU
  - Given the `compose.gpu.yaml` text
  - When a test reads it
  - Then it sets `STEMS_EXTRA` to `gpu` and reserves an `nvidia` device

## Dependencies
- REQ-001 holds the image.
