---
title: "Requirement: REQ-003 - Job progress"
summary: "The page lists jobs and polls until each reaches done or failed."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-003 - Job progress

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000012-web-front-end
**Source:** US-003
**Priority:** must-have

## User Story

As a user, I see my jobs and their status update, so that I know when a job is `done` or `failed`.

## Functional Requirements
- On load, the page reads `GET /jobs` and lists each job with its id, status, and error line.
- If the list is empty, the page shows "No jobs yet."
- The page re-reads `GET /jobs` every two seconds while any job is `queued` or `running`. It stops when none is.
- The script writes server text with `textContent` and never `innerHTML`.

## Acceptance Criteria
- [ ] AC-1: List jobs
  - Given the served page and script
  - When a test reads them
  - Then the script reads `/jobs` and the page holds a job list and the text "No jobs yet."
- [ ] AC-2: Poll until finished
  - Given the served script
  - When a test reads it
  - Then it sets a two-second timer that runs while a job is `queued` or `running`
- [ ] AC-3: Render text safely
  - Given the served script
  - When a test reads it
  - Then it holds no `innerHTML`

## Dependencies
- REQ-001 serves the page and the script.
