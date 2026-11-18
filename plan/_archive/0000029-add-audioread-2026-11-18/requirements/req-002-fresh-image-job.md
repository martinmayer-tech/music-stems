---
title: "Requirement: REQ-002 - Fresh image runs a job"
summary: "A job uploaded to a freshly built image ends done with two stems and no manual install."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-002 - Fresh image runs a job

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000029-add-audioread
**Source:** US-001
**Priority:** must-have

## User Story

As a user, I run `docker compose up --build` and upload a track, so that the job ends `done` with no manual install.

## Functional Requirements
- A fresh CPU image imports `audioread` with no command after the build.
- A job uploaded to that image ends `done` and lists `vocals.wav` and `instrumental.wav`.
- The component docs no longer describe the fault or the manual install.

## Acceptance Criteria
- [ ] AC-1: Import the library in the image
  - Given a CPU image built from this branch
  - When the agent runs `python -c "import audioread"` in a container
  - Then the command exits 0
- [ ] AC-2: Finish a job
  - Given a stack from `docker compose up --build` with no manual install
  - When the agent uploads a short audio file and polls the job
  - Then the job ends `done` with `vocals.wav` and `instrumental.wav`

## Dependencies
- REQ-001 adds the library.
- The check runs by hand in P3, because CI runs no separation.
