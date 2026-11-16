# Design - 0000008-job-queue-worker

## Feature
- Problem: Each `split()` call loads its models again. Two calls can compete for one GPU. A service that takes several uploads cannot run them safely.
- Adoption mode: standard-iterative (signal: `docs/about.md` at 0.3.0 and `src/` beside an archive)
- Feature ID: 0000008-job-queue-worker
- Discovery: see `plan/current/discovery.md`

## Product Layer
- User stories:
  - US-001: As a caller, I add a job and read its status, so that I can follow it from `queued` to `done` or `failed`.
  - US-002: As a caller, I restart the service, so that queued jobs still run and a half-run job runs again.
  - US-003: As a caller, I queue two jobs, so that they run one after the other and never overlap.
  - US-004: As a caller, I queue two jobs, so that the second loads no model that the first already loaded.
- Acceptance criteria confirmed: 4
- Constraints: one SQLite file and one worker thread per device, no broker. `STEMS_DATA_DIR` (default `./data`) and `STEMS_MODEL_DIR`. No new dependency. Unit tests use a fake separator.
- Integrations: `split()` from `stem_core.separation`

## Architecture Layer
- Latency target: deferred - recorded in scope
- Availability target: not applicable
- Scalability target: one worker thread per device, jobs run one at a time per worker
- Security: no network surface, no auth, data classification none. The store runs parameterised SQL only. Paths come from the caller of the Python API, and step 5 validates upload names.
- Data privacy: no regulated data
- Observability: a job row holds status, timestamps, and one error line
- Cost boundary: not constrained

## Engineering Layer
- Stack: Python 3.12 (CI) / sqlite3 and threading from the standard library / pytest / ruff / GitHub Actions / Build target ci-only
- Components: `stem-service` holds `stem_service/config.py`, `jobs.py`, and `worker.py`.
- Data ownership: `stem-service` owns the SQLite table `jobs`.
- Deployment: none
- API versioning: not applicable

## Component Paths
- src/stem-service/
- docs/
- plan/

## Scope
- In: the `jobs` table and `JobStore`, `Worker`, a helper that starts one worker per device, the separator cache, restart recovery, and unit tests
- Out: the HTTP API, uploads, the web page, caller model choice, ensembles, a broker
- Deferred: the HTTP API waits for step 5. Caller model choice waits for step 7.

## Assumptions
- A real `Separator` accepts a changed `output_dir` between runs. Impact if wrong: a model reloads for each job. The fake-separator tests cannot detect this.
- Python threads suffice because the heavy work runs in native code - impact if wrong: none for correctness.

## Risks
- A restart during a job leaves it `running`. Likelihood medium, impact medium. `JobStore.recover()` returns it to `queued` at start.
- Two workers claim one job. Likelihood low, impact high. `claim_next()` updates the row inside one transaction and checks the row count.
- The model cache holds memory for every model. Likelihood medium, impact low. The cache holds at most the two models from `stem-core`.

## Dependencies
- Upstream: step 2 (`split()`)
- Downstream: step 5 queues uploads. Step 7 passes model options.
- Approved dependencies: none

## Active Skills
None

## Skill Map
| Requirement | Best-fit Skill | Rationale |
|-------------|----------------|-----------|
| REQ-001 job store | ravintio-implement | One module with a temporary-file database |
| REQ-002 restart recovery | ravintio-implement | Reopens the file in a test |
| REQ-003 worker | ravintio-implement | Threads with a fake separator |
| REQ-004 model reuse | ravintio-implement | A counting fake separator |

## Repo Instructions
- `agent-permissions.md`: standing commit, push, PR, and squash-merge grants. Never merge or push to `main`.
- `grep-tests-before-moving-files.md`: grep the test folders before moving a file.

## Confirmation
Human confirmed this design before proceeding: draft-accepted (initiative) // Date and Time confirmed: 15 Nov 2026 @ 11:55 p.m. GMT
