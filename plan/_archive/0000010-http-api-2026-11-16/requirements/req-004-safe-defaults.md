---
title: "Requirement: REQ-004 - Safe defaults and entry point"
summary: "The service starts on 127.0.0.1, creates its folders, runs a worker, and completes a job from upload to download."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-004 - Safe defaults and entry point

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000010-http-api
**Source:** US-004
**Priority:** must-have

## User Story

As an operator, I start the service, so that it binds to `127.0.0.1` and rejects unlisted or oversized uploads.

## Functional Requirements
- `resolve_host()` returns `STEMS_HOST`, or `127.0.0.1` when the variable is unset or empty.
- `resolve_port()` returns `STEMS_PORT` as an integer, or 8000 when the variable is unset or empty.
- `python -m stem_service` runs the app with uvicorn on that host and port.
- `create_app()` builds the app. At start-up it creates the data folder, the database, and the `uploads` folder. It then starts one worker, and it stops the worker at shutdown.
- The app adds no login.

## Acceptance Criteria
- [ ] AC-1: Default address
  - Given no `STEMS_HOST` and no `STEMS_PORT`
  - When the operator reads `resolve_host()` and `resolve_port()`
  - Then they return `127.0.0.1` and 8000, and a set variable overrides each
- [ ] AC-2: First run
  - Given a data folder that does not exist
  - When the app starts
  - Then the folder, the database file, and the `uploads` folder exist
- [ ] AC-3: Upload to download
  - Given a running app with a fake separator
  - When the caller uploads a file, polls the job until `done`, and downloads each stem
  - Then every stem arrives as a WAV file

## Dependencies
- REQ-001, REQ-002, and REQ-003 supply the routes.
