---
title: "Requirement: REQ-001 - Docker image"
summary: "A Dockerfile builds one image with Python 3.12, FFmpeg, and the service, and a build argument selects the CPU or GPU extra."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-001 - Docker image

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000016-docker-packaging
**Source:** US-001
**Priority:** must-have

## User Story

As a user, I build one image with Python 3.12 and FFmpeg, so that I install nothing by hand.

## Functional Requirements
- The `Dockerfile` starts from `python:3.12-slim` and installs the Debian package `ffmpeg`.
- The build argument `STEMS_EXTRA` selects the `audio-separator` extra. It defaults to `cpu`, and `gpu` selects the GPU extra.
- The build argument `AUDIO_SEPARATOR_VERSION` holds the pin, and it equals the pin in `pyproject.toml`.
- The image sets `STEMS_HOST=0.0.0.0`, `STEMS_DATA_DIR=/data`, and `STEMS_MODEL_DIR=/models`. It exposes port 8000.
- The image runs `python -m stem_service` as a non-root user that owns `/data` and `/models`.
- The image has a healthcheck that reads `GET /`.
- A `.dockerignore` file keeps `.git`, `plan`, `data`, and caches out of the build context.

## Acceptance Criteria
- [ ] AC-1: Name the base and FFmpeg
  - Given the `Dockerfile` text
  - When a test reads it
  - Then it starts from `python:3.12-slim` and installs `ffmpeg`
- [ ] AC-2: Select the extra
  - Given the `Dockerfile` text
  - When a test reads it
  - Then `STEMS_EXTRA` defaults to `cpu` and `audio-separator[${STEMS_EXTRA}]` appears
- [ ] AC-3: Keep the pin in line
  - Given the `Dockerfile` and `pyproject.toml`
  - When a test compares them
  - Then `AUDIO_SEPARATOR_VERSION` equals the version in the `separation` extra

## Dependencies
- ADR-0008 records the decision.
