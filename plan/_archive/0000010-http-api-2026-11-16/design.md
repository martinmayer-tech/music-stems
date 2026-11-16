# Design - 0000010-http-api

## Feature
- Problem: No process outside Python can submit a job or fetch stems. The web page in step 6 needs an API to call.
- Adoption mode: standard-iterative (signal: `docs/about.md` at 0.4.0 and `src/` beside an archive)
- Feature ID: 0000010-http-api
- Discovery: see `plan/current/discovery.md`

## Product Layer
- User stories:
  - US-001: As a caller, I upload an audio file, so that the service queues a job for it.
  - US-002: As a caller, I read one job or the list of jobs, so that I can follow a job to `done` or `failed`.
  - US-003: As a caller, I download each stem of a finished job, so that I get a WAV file.
  - US-004: As an operator, I start the service, so that it binds to `127.0.0.1` and rejects unlisted or oversized uploads.
- Acceptance criteria confirmed: 4
- Constraints: no login, bind to `127.0.0.1` by default, WAV, FLAC, MP3, and M4A up to `STEMS_MAX_UPLOAD_MB` (default 500). Unit tests use a fake separator.
- Integrations: `JobStore` and `start_workers()` from `stem-service`

## Architecture Layer
- Latency target: deferred - recorded in scope
- Availability target: not applicable
- Scalability target: one worker thread per device, as in step 4
- Security: no auth by decision, loopback bind by default, data classification none. Uploads keep only a sanitised file name inside a folder named by a random id. Stem requests resolve against the job's stored output list, so a name never reaches the file system unchecked.
- Data privacy: no regulated data. Uploaded audio stays on the local disk.
- Observability: a job row holds status, timestamps, and one error line. The API returns them.
- Cost boundary: not constrained

## Engineering Layer
- Stack: Python 3.12 (CI) / FastAPI and uvicorn / sqlite3 and threading from the standard library / pytest and httpx / ruff / GitHub Actions / Build target ci-only
- Components: `stem-service` gains `stem_service/api.py` and `stem_service/__main__.py`.
- Data ownership: `stem-service` owns the SQLite table `jobs` and the `uploads` folder.
- Deployment: none
- API versioning: not applicable. The routes carry no version prefix until a second client needs one.

## Component Paths
- src/stem-service/
- docs/
- plan/

## Scope
- In: the four routes, upload validation, the app factory, the `python -m stem_service` entry point, the `service` dependency extra, a CI install update, and unit tests
- Out: a login, the web page, caller model choice, ensembles, cancel, delete, and a broker
- Deferred: the web page waits for step 6. Caller model choice waits for step 7.

## Assumptions
- The service trusts a caller on the same host. Impact if wrong: an operator who binds to a public address with `STEMS_HOST` exposes an open upload endpoint.
- A finished job lists WAV paths in `outputs`. Impact if wrong: a stem downloads with the wrong media type.

## Risks
- A large upload fills the disk. Likelihood low, impact medium. The limit from `STEMS_MAX_UPLOAD_MB` stops the copy, and the API deletes a partial file.
- A crafted file name or stem name reaches outside the data folder. Likelihood medium, impact high. The API drops the directory part of an upload name, and it serves only paths in the job's `outputs`.
- The worker thread outlives a test app. Likelihood medium, impact low. The app factory stops its workers on shutdown, and tests pass `start_workers=False` or a fake.

## Dependencies
- Upstream: step 4 (`JobStore`, `start_workers`)
- Downstream: step 6 serves a page from the app. Step 7 passes model options through the same upload route.
- Approved dependencies: `fastapi`, `uvicorn`, `python-multipart`, and `httpx` (initiative chart, step 5)

## Active Skills
None

## Skill Map
| Requirement | Best-fit Skill | Rationale |
|-------------|----------------|-----------|
| REQ-001 upload route | ravintio-implement | One module with the test client |
| REQ-002 status routes | ravintio-implement | The test client reads the store |
| REQ-003 stem download | ravintio-implement | The test client reads files from a fake job |
| REQ-004 safe defaults and entry point | ravintio-implement | Unit tests read config and the host |

## Repo Instructions
- `agent-permissions.md`: standing commit, push, PR, and squash-merge grants. Never merge or push to `main`.
- `grep-tests-before-moving-files.md`: grep the test folders before moving a file.

## Confirmation
Human confirmed this design before proceeding: draft-accepted (initiative) // Date and Time confirmed: 16 Nov 2026 @ 12:35 a.m. GMT
