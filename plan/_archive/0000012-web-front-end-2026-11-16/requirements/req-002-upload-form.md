---
title: "Requirement: REQ-002 - Upload form"
summary: "The page sends a chosen file and the full stems option to POST /jobs."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-002 - Upload form

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000012-web-front-end
**Source:** US-002
**Priority:** must-have

## User Story

As a user, I choose a file and the full stems option and send it, so that the service queues a job.

## Functional Requirements
- The page holds a form with one file input, one `full_stems` checkbox, and one submit button.
- The file input accepts `.wav`, `.flac`, `.mp3`, and `.m4a`.
- On submit, `app.js` posts the file and the `full_stems` value to `POST /jobs` as multipart form data.
- If the API answers with an error, the page shows the `detail` text from the answer. It shows no stem for that upload.

## Acceptance Criteria
- [ ] AC-1: Form fields
  - Given the served page
  - When a test reads `GET /`
  - Then it holds a file input, a `full_stems` checkbox, and a submit button
- [ ] AC-2: Post to the API
  - Given the served script
  - When a test reads `/static/app.js`
  - Then it posts a `FormData` with the file and `full_stems` to `/jobs`
- [ ] AC-3: Show an error
  - Given an upload that the API refuses
  - When the answer is not 2xx
  - Then the script writes the `detail` text to the status line with `textContent`

## Dependencies
- REQ-001 serves the page and the script.
