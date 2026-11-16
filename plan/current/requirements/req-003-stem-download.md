---
title: "Requirement: REQ-003 - Stem download"
summary: "A caller downloads each stem of a finished job as a WAV file."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-003 - Stem download

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000010-http-api
**Source:** US-003
**Priority:** must-have

## User Story

As a caller, I download each stem of a finished job, so that I get a WAV file.

## Functional Requirements
- `GET /jobs/{id}/stems/{name}` returns the file with the media type `audio/wav` when `name` matches the file name of one of the job's outputs.
- The route reads no path from the request. It looks `name` up in the job's stored outputs.
- An unknown job, or a name that is not in the outputs, gets status 404. A name such as `..` gets 404.
- A job that is not `done` gets status 409.

## Acceptance Criteria
- [ ] AC-1: Download a stem
  - Given a `done` job whose output is `vocals.wav`
  - When the caller reads `GET /jobs/{id}/stems/vocals.wav`
  - Then the answer is 200 with the type `audio/wav` and the bytes of the file
- [ ] AC-2: Refuse an unlisted name
  - Given a `done` job and a file outside its outputs
  - When the caller asks for a name that the job does not list, including `..`
  - Then the answer is 404 and no other file leaves the server
- [ ] AC-3: Refuse an unfinished job
  - Given a `queued` job
  - When the caller asks for any stem
  - Then the answer is 409

## Dependencies
- REQ-002 reports the `stems` names that this route serves.
