# Design - 0000002-python-scaffold

## Feature
- Problem: The repo has no Python project, no test or lint tooling, and no CI job for Python code.
- Adoption mode: standard-iterative (signal: `docs/about.md` and `src/` present, no archive)
- Feature ID: 0000002-python-scaffold
- Discovery: see `plan/current/discovery.md`

## Product Layer
- User stories:
  - US-001: As a developer, I run `pytest` and `ruff` from the repo root, so that every later step has one way to test and lint.
  - US-002: As a maintainer, I see a red check when a pull request fails a test. I see a green check when it passes, so that I trust each merge.
  - US-003: As a maintainer, I read the product version from `docs/about.md` and `product.yml`, so that the merge queue can set it.
- Acceptance criteria confirmed: 5
- Constraints: Python 3.12 in CI, `requires-python >=3.10`, local Python 3.13. The product version never tracks the pack version.
- Integrations: none

## Architecture Layer
- Latency target: not applicable
- Availability target: not applicable
- Scalability target: not applicable
- Security: no network surface, no auth, data classification none. CI job uses `contents: read`.
- Data privacy: no regulated data
- Observability: standard defaults
- Cost boundary: not constrained

## Engineering Layer
- Stack: Python 3.12 (CI) / pytest / ruff / GitHub Actions / Build target ci-only
- Components: `stem-core` (core separation, later steps), `stem-service` (queue and API, later steps), `stem-web` (web page, later steps). Each holds a package skeleton and one smoke test in this step.
- Data ownership: none
- Deployment: none
- API versioning: not applicable

## Component Paths
- src/stem-core/
- src/stem-service/
- src/stem-web/
- ./pyproject.toml
- .gitignore
- ./product.yml
- .github/workflows/
- docs/
- plan/

## Scope
- In: root `pyproject.toml` with pytest and ruff settings, three component skeletons with manifests and docs, a Python CI job, `product.yml` component list
- Out: any separation, CLI, queue, API, web, or Docker code
- Deferred: `audio-separator` install (step 2)

## Assumptions
- `pytest` and `ruff` install from PyPI in CI - impact if wrong: the CI job fails and the step stops

## Risks
- A new workflow job could break the existing pack checks. Likelihood low, impact medium. The job is separate from the existing jobs.

## Dependencies
- Upstream: none
- Downstream: steps 2 to 8 build on the layout
- Approved dependencies: pytest (library), ruff (library)

## Active Skills
None

## Skill Map
| Requirement | Best-fit Skill | Rationale |
|-------------|----------------|-----------|
| Project layout and tooling | ravintio-implement | Config and skeleton files with smoke tests |
| CI job | ravintio-implement | One workflow job |
| Component docs | ravintio-implement | Manifests and docs land with the code |

## Repo Instructions
- `agent-permissions.md`: standing commit, push, PR, and squash-merge grants. Never merge or push to `main`.
- `grep-tests-before-moving-files.md`: grep the test folders before moving a file.

## Confirmation
Human confirmed this design before proceeding: draft-accepted (initiative) // Date and Time confirmed: 15 Nov 2026 @ 08:53 PM GMT
