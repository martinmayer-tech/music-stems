---
title: "Scope - Add the HTTP API"
summary: "Defines explicit boundaries of what is in scope and out of scope."
status: "active"
version: "0.1.0"
---
# Scope - Add the HTTP API

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000010-http-api
**Version:** 0.5.0

## In Scope

- `stem_service/api.py` with `create_app()` and the four routes.
- `stem_service/__main__.py`, which runs the app with uvicorn.
- Upload checks for the extension and the size.
- New settings in `config.py` for the host, the port, the upload limit, and the `uploads` folder.
- The `service` dependency extra, the `httpx` test dependency, and the CI install line.
- Unit tests with a fake separator and the FastAPI test client.
- The OpenAPI spec, the component docs, and the living docs that the code changes.

## Out of Scope

- A login or any other auth.
- The web page and the route that serves it.
- Cancel or delete a job: gap: out of scope.
- Pick a model: gap: out of scope.
- A broker or a second queue backend.

## Deferred

- The web page waits for step 6. It blocks the browser front end.
- Model choice and ensembles wait for step 7. They add a field to the upload route.
