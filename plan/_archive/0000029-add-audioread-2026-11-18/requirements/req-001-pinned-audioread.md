---
title: "Requirement: REQ-001 - Pinned audioread"
summary: "The separation extra and the Dockerfile install audioread at one pinned version, and a test keeps the two equal."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-001 - Pinned audioread

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000029-add-audioread
**Source:** US-001, US-002
**Priority:** must-have

## User Story

As a developer, I install the `separation` extra, so that a local `stems split` finds `audioread`.

## Functional Requirements
- The `separation` extra in `pyproject.toml` lists `audioread==3.1.0` after the `audio-separator` pin.
- The `Dockerfile` holds the build argument `AUDIOREAD_VERSION=3.1.0`.
- The `pip install` layer of the `Dockerfile` installs `audioread==${AUDIOREAD_VERSION}`.
- The `audio-separator` pin stays at 0.48.0 in both files.

## Acceptance Criteria
- [ ] AC-1: Pin the library in the extra
  - Given the `pyproject.toml` text
  - When a test reads the `separation` extra
  - Then it holds `audioread==` with an exact version
- [ ] AC-2: Install the library in the image
  - Given the `Dockerfile` text
  - When a test reads the `pip install` layer
  - Then the layer installs `audioread==${AUDIOREAD_VERSION}`
- [ ] AC-3: Keep the two pins equal
  - Given the `Dockerfile` and `pyproject.toml`
  - When a test compares them
  - Then `AUDIOREAD_VERSION` equals the version in the `separation` extra

## Dependencies
- ADR-0009 records the decision.
