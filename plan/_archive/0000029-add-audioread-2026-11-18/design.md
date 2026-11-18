# Design - 0000029-add-audioread

## Feature
- Problem: A user who runs the built image gets a `failed` job with `No module named 'audioread'`.
- Adoption mode: standard-iterative (signal: `docs/about.md` at 0.8.0 and `src/` beside an archive)
- Feature ID: 0000029-add-audioread
- Discovery: see `plan/current/discovery.md`

## Product Layer
- User stories:
  - US-001: As a user, I run `docker compose up --build` and upload a track, so that the job ends `done` with no manual install.
  - US-002: As a developer, I install the `separation` extra, so that a local `stems split` finds `audioread`.
- Acceptance criteria confirmed: 3
  - AC-1: the `separation` extra in `pyproject.toml` pins `audioread` with `==`.
  - AC-2: the `Dockerfile` installs `audioread` at the same version, and a test compares the two pins.
  - AC-3: a job uploaded to a fresh image from `docker compose up --build` ends `done` with `vocals.wav` and `instrumental.wav`.
- Constraints: change no model, no API, and no page. Keep the `audio-separator` pin at 0.48.0.
- Integrations: `audio-separator` 0.48.0, the pinned engine

## Architecture Layer
- Latency target: not applicable
- Availability target: not applicable
- Scalability target: not applicable
- Security: no change. No login by decision (ADR-0005). The data is the user's own audio on their own machine.
- Data privacy: no regulated data
- Observability: standard defaults
- Cost boundary: not constrained

## Engineering Layer
- Stack: Python 3.12 in the image, pytest, ruff, Dockerfile, GitHub Actions. Build target local.
- Components: `stem-core` owns the `separation` extra and its dependency doc. `stem-service` owns the `Dockerfile` and its tests.
- Data ownership: no change
- Deployment: `docker compose up` on one host
- API versioning: not applicable

## Component Paths
- src/stem-core/
- src/stem-service/
- ./pyproject.toml
- ./Dockerfile
- docs/
- plan/

## Scope
- In:
  - `audioread==3.1.0` in the `separation` extra
  - an `AUDIOREAD_VERSION` build argument in the `Dockerfile`, and its install
  - a test that compares the two pins
  - the dependency docs of `stem-core` and `stem-service`
  - one real job through a fresh image, run by hand
  - the removal of backlog entry 0000023
  - a patch bump to 0.8.1
- Out: a newer `audio-separator`, a separation run in CI, the GPU image run, and the pack gaps in entries 0000018 to 0000028
- Deferred: nothing

## Assumptions
- `audioread` 3.1.0 works with `audio-separator` 0.48.0 on Python 3.12. Impact if wrong: the hand-run job fails, and the run pins the version that step 8 installed.

## Risks
- The two `audioread` pins drift apart. Likelihood medium, impact medium. A test compares them.
- `audio-separator` 0.48.0 misses another module that the first job did not reach. Likelihood low, impact medium. The hand-run job covers pass 1, and the run reports what pass 2 shows.

## Dependencies
- Upstream: initiative 0000001, steps 2 and 8
- Downstream: none
- Approved dependencies: `audioread` 3.1.0 (library), approved by the human at the design gate

## Active Skills
None

## Skill Map
| Requirement | Best-fit Skill | Rationale |
|-------------|----------------|-----------|
| REQ-001 pinned `audioread` in the extra and the image | ravintio-implement | Two text files that tests read |
| REQ-002 fresh image runs a job | ravintio-validate-and-accept | A hand-run check with evidence |

## Repo Instructions
- `agent-permissions.md`: standing commit, push, PR, and squash-merge grants. Never merge or push to `main`.
- `grep-tests-before-moving-files.md`: grep the test folders before moving a file.

## Confirmation
Human confirmed this design before proceeding: yes // Date and Time confirmed: 18 Nov 2026 @ 07:21 a.m. GMT
