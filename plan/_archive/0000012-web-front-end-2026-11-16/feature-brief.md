---
title: "Feature Brief - Add the web front end"
summary: "A plain HTML, CSS, and JavaScript page in stem-web that the API serves. It uploads a file, shows job progress, and plays and downloads each stem."
status: "approved"
version: "0.1.0"
---
# Feature Brief - Add the web front end

**Feature ID:** 0000012-web-front-end

## Business Goal

The API has no user interface. The goal is a self-hosted replacement for a hosted web tool. This step adds a page to `stem-web` that the API serves at its root.

## Features

| Feature | User Stories | Priority | Wave |
|---------|-------------|----------|------|
| Serve the page | As a user, I open the service root in a browser, so that I get the page with no build step. | must-have | 1 |
| Upload | As a user, I choose a file and the full stems option and send it, so that the service queues a job. | must-have | 1 |
| Job progress | As a user, I see my jobs and their status update, so that I know when a job is `done` or `failed`. | must-have | 1 |
| Stem results | As a user, I play each stem of a finished job and download it, so that I can use the stems. | must-have | 1 |

## Waves

One wave. The feature ships when the observable condition passes.

## Target Architecture

### Components

| Component | Type | New or Existing | Responsibility |
|-----------|------|-----------------|---------------|
| stem-web | microfrontend | existing | Holds the page files and `static_dir()`, which names the folder that holds them. |
| stem-service | microservice | existing | Serves the page at `/` and its files under `/static`. |

### Data Ownership

`stem-web` owns no data. It holds static files only. `stem-service` keeps ownership of the `jobs` table and the data folder.

### Integration Points

| From | To | Method | Contract |
|------|-----|--------|----------|
| Browser | API | HTTP | `GET /`, `GET /static/{file}` |
| Page | API | `fetch` | `POST /jobs`, `GET /jobs`, `GET /jobs/{id}`, `GET /jobs/{id}/stems/{name}` |
| API | stem-web | Python call | `stem_web.static_dir()` |

## Stack

| Concern | Decision |
|---------|----------|
| Language | HTML, CSS, JavaScript (browser), Python for the serving route |
| Runtime | Python 3.12 in CI, 3.13 locally |
| Framework | none for the page, FastAPI for the route |
| Frontend | plain HTML, CSS, and JavaScript with no build |
| Database | none |
| ORM | none |
| Testing | pytest with the FastAPI test client. A `node` check runs the pure page logic |
| IaC | none |
| Cloud | none |
| Compute | none |
| CI | GitHub Actions |
| Build target | ci-only |

## Scope Boundaries

### In Scope
- `stem_web/static/index.html`, `app.js`, and `style.css`.
- `stem_web.static_dir()`.
- `GET /` and a `/static` mount in `create_app()`.
- An upload form with the `full_stems` option, a job list that polls, and one player and one download link per stem.
- Tests over HTTP for the served files, and a `node` check of the stem link logic.

### Out of Scope
- A build step, a framework, or browser automation.
- Model choice and ensemble options. Step 7 adds them.
- Cancel or delete a job, a login, and drag-and-drop folders.

### Deferred
- Model choice waits for step 7. It adds a field to the upload form.

## Non-Functional Requirements

| NFR | Target | Measurement |
|-----|--------|-------------|
| Safe rendering | The page puts server text into the document with `textContent` only | A test reads `app.js` for `innerHTML` |
| Static path safety | `/static` serves only files in the page folder | A test requests `..` paths |
| No build | The service serves the files as they sit in the repo | A test fetches each file |

## Constraints and Assumptions

### Constraints
- Use plain HTML, CSS, and JavaScript with no build.
- Test the served files and the API calls over HTTP. Add no browser automation.
- Add no dependency. The chart lists none for this step.
- The page calls only the four existing routes.

### Assumptions
- A user opens the page on the same host or through a trusted tunnel, because the API has no login.

## Scenario Paths

**Happy path:** A user opens `/`, chooses a WAV file, sends it, and watches the job reach `done`. The page then shows one player and one download link per stem.

> The page polls `GET /jobs/{id}` every two seconds.

**First-run path:** The service holds no job. The page loads and the job list reads "No jobs yet."

> The first upload triggers the model download in `audio-separator`, so the first job takes longer.

**Error / sad path:** The API refuses the upload with 413 or 415, a job ends `failed`, or the API is not reachable.

> The page shows the API's error text or the job's error line. It never shows a stem for a failed job.

**Cross-session continuity:** The user reloads the page or opens it later.

> The page reads `GET /jobs` and shows every job with its current status and stems.

## Acceptance Criteria

- [ ] `GET /` returns the page.
- [ ] The page uploads a file with the full stems option through `POST /jobs`.
- [ ] The page polls a job until it is `done` or `failed`.
- [ ] A finished job shows one player and one download link per stem.
