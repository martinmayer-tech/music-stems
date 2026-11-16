---
title: "Requirement: REQ-004 - Stem results"
summary: "A finished job shows one player and one download link per stem."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-004 - Stem results

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000012-web-front-end
**Source:** US-004
**Priority:** must-have

## User Story

As a user, I play each stem of a finished job and download it, so that I can use the stems.

## Functional Requirements
- `stemLinks(jobId, stems)` in `app.js` returns one object per stem name. Each holds `name` and `url`.
- The `url` is `/jobs/{id}/stems/{name}` with `jobId` and `name` encoded by `encodeURIComponent`.
- The page renders one `audio` player and one download link for each entry of a `done` job.
- A `queued`, `running`, or `failed` job shows no player and no link.

## Acceptance Criteria
- [ ] AC-1: One link per stem
  - Given a job id and the stem names `vocals.wav` and `instrumental.wav`
  - When `node` runs `stemLinks`
  - Then it returns two entries with the URLs `/jobs/{id}/stems/vocals.wav` and `/jobs/{id}/stems/instrumental.wav`
- [ ] AC-2: Encode names
  - Given a stem name with a space and a `#`
  - When `node` runs `stemLinks`
  - Then the URL holds `%20` and `%23`
- [ ] AC-3: Render only for a done job
  - Given the served script
  - When a test reads it
  - Then it creates an `audio` element and a download link only in the `done` branch

## Dependencies
- REQ-003 lists the jobs that this requirement renders.
