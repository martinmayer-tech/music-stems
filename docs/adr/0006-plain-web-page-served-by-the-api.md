---
title: "ADR 0006: Plain web page served by the API"
summary: "stem-web holds a build-free HTML, CSS, and JavaScript page that stem-service serves at its root."
status: "proposed"
component: "stem-web"
version: "0.6.0"
---
# ADR-0006 - Plain web page served by the API

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000012-web-front-end
**Component:** stem-web
**File:** `docs/adr/0006-plain-web-page-served-by-the-api.md`
**Date:** 2026-11-16

## Context

The API has no user interface. The initiative chart sets two decisions. The page uses plain HTML, CSS, and JavaScript with no build. Tests check the served files and the API calls over HTTP, with no browser automation. The page crosses two components, because `stem-web` holds the files and `stem-service` serves them.

## Decision

`stem-web` holds `stem_web/static/index.html`, `app.js`, and `style.css`. It exposes `static_dir()`, which returns that folder.

`create_app()` in `stem-service` serves `index.html` at `GET /` and mounts the folder at `/static`. The page calls the four job routes with `fetch` from the same origin, so it needs no CORS setting.

The script writes server text with `textContent` only. It builds each stem URL with `encodeURIComponent`.

The stem link logic is a pure function, `stemLinks()`. A `node` test runs it. `app.js` exports it only when `module` exists, so the browser ignores the export.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| A framework with a build step | Components and a store | A build tool and a lock file join the repo | The chart says use no build |
| A separate static server | Splits the page from the API | Needs CORS and a second process | The chart wants a self-hosted service in one process |
| Browser automation tests | Tests the real page | A browser joins CI | The chart says add none |

## Affected Components

| Component | Impact |
|-----------|--------|
| stem-web | Gains the page files and `static_dir()` |
| stem-service | Gains `GET /` and the `/static` mount, and imports `stem_web` |

## Consequences

**Positive:**
- A user needs only a browser.
- The repo holds no build tool.
- The page and the API share one origin.

**Negative:**
- `stem-service` depends on `stem-web` at import time.
- The page has no browser test. A `node` test covers the pure logic only.

**Risks:**
- A bug in the DOM code reaches users, because no test runs it.

## Related ADRs

- ADR-0005 sets the routes that the page calls and the loopback bind.

## Supersedes

- None.

## Superseded By

- None.
