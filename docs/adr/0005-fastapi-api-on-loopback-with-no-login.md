---
title: "ADR 0005: FastAPI HTTP API on the loopback address with no login"
summary: "stem-service serves its HTTP API with FastAPI and uvicorn, binds to 127.0.0.1 by default, adds no login, and serves stems only from a job's stored outputs."
status: "accepted"
component: "stem-service"
version: "0.5.0"
---
# ADR-0005 - FastAPI HTTP API on the loopback address with no login

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000010-http-api
**Component:** stem-service
**File:** `docs/adr/0005-fastapi-api-on-loopback-with-no-login.md`
**Date:** 2026-11-16

## Context

No process outside Python can submit a job or fetch stems, and the web page in step 6 needs an API. The initiative chart approves `fastapi`, `uvicorn`, `python-multipart`, and `httpx`. It also sets two decisions: add no login, and bind to `127.0.0.1` by default. This is a security trade-off, so an ADR records it.

## Decision

`stem_service/api.py` builds the app with `create_app()`. The app has four routes: `POST /jobs`, `GET /jobs`, `GET /jobs/{id}`, and `GET /jobs/{id}/stems/{name}`. The app starts one worker at start-up and stops it at shutdown.

The service adds no login. It binds to `127.0.0.1`, and an operator who sets `STEMS_HOST` takes on the exposure.

The upload route accepts `.wav`, `.flac`, `.mp3`, and `.m4a` files up to `STEMS_MAX_UPLOAD_MB` (default 500). It keeps only the last part of the client's file name and writes the file into a random folder under `STEMS_DATA_DIR/uploads`.

The stem route takes no path from the request. It looks the stem name up in the job's stored outputs and serves only a match.

The libraries are `fastapi`, `uvicorn`, and `python-multipart` in a `service` extra of the root `pyproject.toml`. `httpx` joins the `dev` extra for the test client. CI installs the `service` extra.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| Flask or the standard library `http.server` | Fewer or no dependencies | No typed models, no OpenAPI output, and hand-written upload parsing | The chart approves FastAPI |
| A login with a token | Safe on a shared host | Adds a secret to manage | The chart says add no login |
| Serve a stem by a path in the URL | Fewer lookups | Opens path traversal | The route needs a lookup in stored outputs |

## Affected Components

| Component | Impact |
|-----------|--------|
| stem-service | Gains `api.py` and `__main__.py`, and a new settings group in `config.py` |
| stem-web | None yet. Step 6 serves its page from the app |

## Consequences

**Positive:**
- A client outside Python can submit a job and fetch stems.
- FastAPI writes the OpenAPI document from the routes.
- A stem request cannot reach a file outside a job's outputs.

**Negative:**
- Four new dependencies join the project.
- Anyone who reaches the port can upload, because the service has no login.

**Risks:**
- An operator who binds to a public address exposes an open upload route.

## Related ADRs

- ADR-0004 sets the job store and worker that the app calls.

## Supersedes

- None.

## Superseded By

- None.
