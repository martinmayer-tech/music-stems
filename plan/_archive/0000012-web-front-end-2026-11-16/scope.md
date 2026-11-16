---
title: "Scope - Add the web front end"
summary: "Defines explicit boundaries of what is in scope and out of scope."
status: "active"
version: "0.1.0"
---
# Scope - Add the web front end

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000012-web-front-end
**Version:** 0.6.0

## In Scope

- `stem_web/static/index.html`, `app.js`, and `style.css`, with no build step.
- `stem_web.static_dir()`.
- `GET /` and the `/static` mount in `create_app()`.
- An upload form with the `full_stems` option.
- A job list that polls while a job is `queued` or `running`.
- One player and one download link for each stem of a `done` job.
- Tests over HTTP, and a `node` test of `stemLinks`.
- The OpenAPI spec for the two new routes, the component docs, and the living docs that the code changes.

## Out of Scope

- A build step, a framework, or browser automation.
- Cancel or delete a job: gap: out of scope.
- Pick a model: gap: out of scope.
- A login: gap: out of scope.

## Deferred

- Model choice waits for step 7. It blocks a model field on the upload form.
