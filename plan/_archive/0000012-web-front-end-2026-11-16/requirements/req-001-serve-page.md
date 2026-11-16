---
title: "Requirement: REQ-001 - Serve the page"
summary: "The API serves the page at its root and its files under /static."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-001 - Serve the page

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000012-web-front-end
**Source:** US-001
**Priority:** must-have

## User Story

As a user, I open the service root in a browser, so that I get the page with no build step.

## Functional Requirements
- `GET /` returns `index.html` with the type `text/html`.
- `GET /static/{file}` returns `app.js` and `style.css` from the page folder. The `/static` mount serves no other folder.
- `stem_web.static_dir()` returns the page folder as a path. The app reads the folder from it.
- A path such as `/static/../` serves no file outside the page folder.

## Acceptance Criteria
- [ ] AC-1: Load the page
  - Given a running app
  - When a browser reads `GET /`
  - Then the answer is 200 with the type `text/html` and the page links `/static/app.js` and `/static/style.css`
- [ ] AC-2: Load the assets
  - Given a running app
  - When a browser reads `/static/app.js` and `/static/style.css`
  - Then each answer is 200 with the file bytes
- [ ] AC-3: Refuse a path outside the folder
  - Given a running app
  - When a client asks for a `..` path under `/static`
  - Then the answer is 404 and no file outside the page folder leaves the server

## Dependencies
- None.
