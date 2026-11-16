# Design - 0000016-docker-packaging

## Feature
- Problem: Running the service needs a manual Python and FFmpeg install. A container without a volume downloads every model again.
- Adoption mode: standard-iterative (signal: `docs/about.md` at 0.7.0 and `src/` beside an archive)
- Feature ID: 0000016-docker-packaging
- Discovery: see `plan/current/discovery.md`

## Product Layer
- User stories:
  - US-001: As a user, I build one image with Python 3.12 and FFmpeg, so that I install nothing by hand.
  - US-002: As a user, I run `docker compose up`, so that the page opens on a local port and a restart keeps the models and the jobs.
  - US-003: As a maintainer, I want CI to build the CPU image, so that a broken Dockerfile fails a pull request.
- Acceptance criteria confirmed: 4
- Constraints: add no login. Bind the container to all interfaces and publish on `127.0.0.1` only. Pin `audio-separator` to the `pyproject.toml` version. Publish no image. CI builds the CPU image only.
- Integrations: `audio-separator` 0.48.0, the pinned engine

## Architecture Layer
- Latency target: deferred - recorded in scope
- Availability target: not applicable
- Scalability target: not applicable. One container runs the one worker pool.
- Security: no login by decision (ADR-0005). The compose file publishes on `127.0.0.1` only. The container runs as a non-root user.
- Data privacy: no regulated data
- Observability: the container healthcheck reads `GET /`
- Cost boundary: not constrained

## Engineering Layer
- Stack: Dockerfile on `python:3.12-slim`, Python 3.12, FastAPI, pytest, ruff, GitHub Actions. Build target local. The tests run on the host, and the image build runs in Docker.
- Components: `stem-service` owns the `Dockerfile`, `.dockerignore`, `compose.yaml`, `compose.gpu.yaml`, and their docs.
- Data ownership: `stem-service` owns the `jobs` table. The data volume holds it.
- Deployment: `docker compose up` on one host
- API versioning: not applicable

## Component Paths
- src/stem-service/
- ./Dockerfile
- ./compose.yaml
- ./compose.gpu.yaml
- ./.dockerignore
- .github/workflows/
- docs/
- plan/

## Scope
- In: the image, the build argument, the compose file, the GPU override, the CI build job, tests, docs, and an ADR.
- Out: publishing the image, a separation run in CI, a login, a reverse proxy, and a multi-container setup
- Deferred: nothing

## Assumptions
- The NVIDIA container toolkit is present on a GPU host. Impact if wrong: the GPU job fails at its first run with the engine's error.
- The `python:3.12-slim` image can install `audio-separator[cpu]` wheels. Impact if wrong: the CI build fails and the step reports it.

## Risks
- The image is large because the engine pulls PyTorch. Likelihood high, impact low. The docs name the size.
- A stale `audio-separator` pin in the Dockerfile drifts from `pyproject.toml`. Likelihood medium, impact medium. A test compares the two.
- The container binds to all interfaces and a user publishes it beyond loopback. Likelihood low, impact high. The compose file publishes on `127.0.0.1` and the docs warn about editing it.

## Dependencies
- Upstream: steps 2 to 7 (the engine, the service, the page)
- Downstream: none
- Approved dependencies: `python:3.12-slim` (service), `ffmpeg` (library), `audio-separator[gpu]` (library), from the initiative chart, step 8

## Active Skills
None

## Skill Map
| Requirement | Best-fit Skill | Rationale |
|-------------|----------------|-----------|
| REQ-001 image | ravintio-implement | A Dockerfile checked as text and built in CI |
| REQ-002 compose file | ravintio-implement | YAML checked as text and run locally |
| REQ-003 CI build | ravintio-implement | A workflow job checked as text |

## Repo Instructions
- `agent-permissions.md`: standing commit, push, PR, and squash-merge grants. Never merge or push to `main`.
- `grep-tests-before-moving-files.md`: grep the test folders before moving a file.

## Confirmation
Human confirmed this design before proceeding: draft-accepted (initiative) // Date and Time confirmed: 16 Nov 2026 @ 3:10 a.m. GMT
