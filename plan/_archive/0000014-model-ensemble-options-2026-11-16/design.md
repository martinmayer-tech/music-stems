# Design - 0000014-model-ensemble-options

## Feature
- Problem: Every job uses the two default models. A caller cannot pick a faster or a richer model, an ensemble, or one stem.
- Adoption mode: standard-iterative (signal: `docs/about.md` at 0.6.0 and `src/` beside an archive)
- Feature ID: 0000014-model-ensemble-options
- Discovery: see `plan/current/discovery.md`

## Product Layer
- User stories:
  - US-001: As a developer, I pass model options to `split()`, so that a job uses the models I want.
  - US-002: As a user, I pass the same options to `stems split`, so that I choose from the shell.
  - US-003: As a user, I send the options with `POST /jobs`, so that the queued job uses them.
  - US-004: As a user, I choose the options on the upload form, so that I need no `curl`.
- Acceptance criteria confirmed: 4
- Constraints: reject any value outside an allowlist at every entry point. Add no dependency and no schema change. Unit tests inject a fake separator.
- Integrations: `audio-separator` 0.48.0, the pinned engine

## Architecture Layer
- Latency target: deferred - recorded in scope
- Availability target: not applicable
- Scalability target: not applicable. Each option adds no new queue or thread.
- Security: no login by decision. Every option is a fixed string from an allowlist. A request never supplies a model path or a file name for a model.
- Data privacy: no regulated data
- Observability: a failed job stores one error line that names the bad option
- Cost boundary: not constrained

## Engineering Layer
- Stack: Python 3.12 (CI) with FastAPI and argparse. HTML, CSS, and JavaScript for the page. pytest with fake separators. ruff. GitHub Actions. Build target ci-only.
- Components: `stem-core` gains the allowlists, `validate_options()`, and the new `split()` arguments. `stem-service` gains three form fields and the worker pass-through. `stem-web` gains three selects.
- Data ownership: `stem-service` owns the `jobs` table. `stem-core` and `stem-web` own no data.
- Deployment: none
- API versioning: not applicable. The new form fields are optional.

## Component Paths
- src/stem-core/
- src/stem-service/
- src/stem-web/
- docs/
- plan/

## Scope
- In: the allowlists, `validate_options()`, and the `split()` arguments.
- In: the command flags, the form fields, the worker pass-through, and three selects.
- In: tests, docs, and the OpenAPI spec.
- Out: a pass 1 model choice, a free-text model name, a route that lists the options, and a schema change
- Deferred: nothing

## Assumptions
- The preset names match `audio-separator` 0.48.0. Impact if wrong: a preset fails inside the engine and the job ends `failed` with the engine's error line.
- An ensemble pass 1 still writes vocals and instrumental files. Impact if wrong: pass 1 raises the existing error that names the missing file.

## Risks
- A caller names a model that the engine downloads from an unexpected source. Likelihood low, impact high. The allowlist holds fixed names and a test rejects any other value.
- A single stem option deletes a stem that the caller wants. Likelihood medium, impact low. The option names the stem to keep, and the docs say so.
- The pool loads one separator for each model and preset pair, so memory grows. Likelihood medium, impact medium. The allowlist caps the pairs at 30.

## Dependencies
- Upstream: steps 2 to 6 (the engine seam, the command, the worker, the API, the page)
- Downstream: step 8 packages the service
- Approved dependencies: none (initiative chart, step 7)

## Active Skills
None

## Skill Map
| Requirement | Best-fit Skill | Rationale |
|-------------|----------------|-----------|
| REQ-001 options in split() | ravintio-implement | One module and a fake separator |
| REQ-002 options in the command | ravintio-implement | argparse flags with an injected split function |
| REQ-003 options in the API | ravintio-implement | Form fields and the worker with the test client |
| REQ-004 options on the page | ravintio-implement | Served HTML checked as text |

## Repo Instructions
- `agent-permissions.md`: standing commit, push, PR, and squash-merge grants. Never merge or push to `main`.
- `grep-tests-before-moving-files.md`: grep the test folders before moving a file.

## Confirmation
Human confirmed this design before proceeding: draft-accepted (initiative) // Date and Time confirmed: 16 Nov 2026 @ 2:12 a.m. GMT
