---
title: "Requirement: REQ-001 - Upload"
summary: "A caller uploads an audio file and the service queues a job for it."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-001 - Upload

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000010-http-api
**Source:** US-001
**Priority:** must-have

## User Story

As a caller, I upload an audio file, so that the service queues a job for it.

## Functional Requirements
- `POST /jobs` takes one multipart file field named `file` and an optional form field `full_stems`, which defaults to false.
- The route accepts the extensions `.wav`, `.flac`, `.mp3`, and `.m4a`, in any letter case. Any other extension gets status 415.
- The route copies the upload to `{data_dir}/uploads/{random id}/{file name}`. It keeps only the last part of the client's file name.
- The route stops at the limit from `STEMS_MAX_UPLOAD_MB`, default 500. A larger upload gets status 413, and the route deletes the partial file.
- A rejected upload creates no job.
- A valid upload adds a job to the store, wakes the workers, and returns status 201 with the job as JSON.

## Acceptance Criteria
- [ ] AC-1: Accept a WAV file
  - Given an app with no running worker
  - When the caller posts a WAV file with `full_stems` set to true
  - Then the answer is 201 with a job id and the status `queued`
  - And the store holds that job with `full_stems` set and an input file under `uploads`
- [ ] AC-2: Reject an unlisted extension
  - Given an app
  - When the caller posts a file named `notes.txt`
  - Then the answer is 415 and the store holds no job
- [ ] AC-3: Reject an oversized upload
  - Given an app with an upload limit of 10 bytes
  - When the caller posts a file of 11 bytes
  - Then the answer is 413, the store holds no job, and no file remains under `uploads`

## Dependencies
- None.
