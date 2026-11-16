# Design - 0000012-web-front-end

## Feature
- Problem: The API has no user interface. A person must use `curl` to upload a mix and fetch stems.
- Adoption mode: standard-iterative (signal: `docs/about.md` at 0.5.0 and `src/` beside an archive)
- Feature ID: 0000012-web-front-end
- Discovery: see `plan/current/discovery.md`

## Product Layer
- User stories:
  - US-001: As a user, I open the service root in a browser, so that I get the page with no build step.
  - US-002: As a user, I choose a file and the full stems option and send it, so that the service queues a job.
  - US-003: As a user, I see my jobs and their status update, so that I know when a job is `done` or `failed`.
  - US-004: As a user, I play each stem of a finished job and download it, so that I can use the stems.
- Acceptance criteria confirmed: 4
- Constraints: plain HTML, CSS, and JavaScript with no build. Tests check the served files and the API calls over HTTP. No browser automation. No new dependency.
- Integrations: the four routes of the HTTP API

## Architecture Layer
- Latency target: deferred - recorded in scope
- Availability target: not applicable
- Scalability target: the page polls one job every two seconds and the job list every five seconds
- Security: no login by decision. The page writes server text with `textContent` and never `innerHTML`. It builds stem URLs with `encodeURIComponent`. `/static` serves files from one folder only.
- Data privacy: no regulated data. The page stores nothing in the browser.
- Observability: the page shows each job's status and error line from the API.
- Cost boundary: not constrained

## Engineering Layer
- Stack: HTML, CSS, and JavaScript. Python 3.12 (CI) with FastAPI. pytest with the FastAPI test client. `node` for one pure-function test. ruff. GitHub Actions. Build target ci-only.
- Components: `stem-web` gains `stem_web/static/index.html`, `app.js`, and `style.css`, and `static_dir()`. `stem-service` gains `GET /` and a `/static` mount in `create_app()`.
- Data ownership: `stem-web` owns no data. `stem-service` owns the `jobs` table and the `uploads` folder.
- Deployment: none
- API versioning: not applicable. The page and the API ship together.

## Component Paths
- src/stem-web/
- src/stem-service/
- docs/
- plan/

## Scope
- In: the page files, `static_dir()`, the `/` route, and the `/static` mount.
- In: an upload form, a polling job list, and one player and one download link per stem.
- In: tests and docs.
- Out: a build step, a framework, browser automation, model choice, cancel, delete, and a login
- Deferred: model choice waits for step 7.

## Assumptions
- The user reaches the page on the loopback address or through a trusted tunnel. Impact if wrong: an operator who exposes the service gives anyone the upload form.
- A `done` job lists WAV stem names in `stems`. Impact if wrong: a player cannot decode a stem.

## Risks
- Server text such as a file name or an error line runs as markup. Likelihood medium, impact high. The page uses `textContent` and `setAttribute` only, and a test rejects `innerHTML`.
- The `/static` mount serves a file outside the page folder. Likelihood low, impact high. The mount names one folder, and a test requests `..` paths.
- The page logic breaks and no browser test catches it. Likelihood medium, impact medium. The stem link logic is a pure function that a `node` test runs.

## Dependencies
- Upstream: step 5 (the four routes)
- Downstream: step 7 adds a model field to the same form. Step 8 packages the service.
- Approved dependencies: none (initiative chart, step 6)

## Active Skills
None

## Skill Map
| Requirement | Best-fit Skill | Rationale |
|-------------|----------------|-----------|
| REQ-001 serve the page | ravintio-implement | One route and static files with the test client |
| REQ-002 upload form | ravintio-implement | Served HTML and script, checked as text |
| REQ-003 job progress | ravintio-implement | Polling logic checked as text and by `node` |
| REQ-004 stem results | ravintio-implement | A pure function that `node` runs |

## Repo Instructions
- `agent-permissions.md`: standing commit, push, PR, and squash-merge grants. Never merge or push to `main`.
- `grep-tests-before-moving-files.md`: grep the test folders before moving a file.

## Confirmation
Human confirmed this design before proceeding: draft-accepted (initiative) // Date and Time confirmed: 16 Nov 2026 @ 1:33 a.m. GMT
