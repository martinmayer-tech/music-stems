# Design - 0000004-separation-core

## Feature
- Problem: No code wraps `audio-separator`, so nothing can split a mix into stems.
- Adoption mode: standard-iterative (signal: `docs/about.md` at 0.1.0 and `src/` beside an archive)
- Feature ID: 0000004-separation-core
- Discovery: see `plan/current/discovery.md`

## Product Layer
- User stories:
  - US-001: As a developer, I call `split(mix, out)`, so that I get the vocals and instrumental WAV paths.
  - US-002: As a developer, I call `split(mix, out, full_stems=True)`, so that I also get drums, bass, and other.
  - US-003: As an operator, I set `STEMS_MODEL_DIR` and install one pinned `audio-separator` version, so that models persist and results repeat.
- Acceptance criteria confirmed: 4
- Constraints: Python 3.12 in CI, `requires-python >=3.10`. Unit tests use a fake separator. The real-model test carries the `slow` marker.
- Integrations: `audio-separator` through its Python API

## Architecture Layer
- Latency target: deferred - recorded in scope
- Availability target: not applicable
- Scalability target: not applicable
- Security: no network surface, no auth, data classification none. The function reads a caller-supplied path and writes to a caller-supplied folder.
- Data privacy: no regulated data
- Observability: standard defaults
- Cost boundary: not constrained

## Engineering Layer
- Stack: Python 3.12 (CI) / pytest / ruff / GitHub Actions / Build target ci-only
- Components: `stem-core` holds `split()` in `stem_core/separation.py`.
- Data ownership: none
- Deployment: none
- API versioning: not applicable

## Component Paths
- src/stem-core/
- docs/
- plan/
- pyproject.toml
- .github/workflows/

## Scope
- In: `split()`, the two models, WAV output, `STEMS_MODEL_DIR`, absolute paths, the pinned `separation` extra, a CI install, one `slow` smoke test
- Out: the `stems` command, queue, API, web page, Docker, caller model choice, ensembles
- Deferred: caller model choice and ensembles wait for step 7

## Assumptions
- `audio-separator[cpu]==0.48.0` installs on Python 3.12 in CI - impact if wrong: the CI job fails and the step takes a CI fix.
- `separate()` may return relative paths - impact if wrong: none, because the code resolves each path against the output folder.

## Risks
- The pinned package fails to install in CI. Likelihood low, impact medium. The step adjusts the pin or the extra.
- Pass 2 names its input file differently than the guide shows. Likelihood medium, impact low. The code passes the exact pass 1 path.

## Dependencies
- Upstream: step 1 (layout and CI)
- Downstream: steps 3, 4, and 7 call `split()`
- Approved dependencies: audio-separator[cpu] (library, one exact version)

## Active Skills
None

## Skill Map
| Requirement | Best-fit Skill | Rationale |
|-------------|----------------|-----------|
| REQ-001 two-pass split | ravintio-implement | One function with injected-fake tests |
| REQ-002 pinned dependency and CI | ravintio-implement | Config and workflow change |

## Repo Instructions
- `agent-permissions.md`: standing commit, push, PR, and squash-merge grants. Never merge or push to `main`.
- `grep-tests-before-moving-files.md`: grep the test folders before moving a file.

## Confirmation
Human confirmed this design before proceeding: draft-accepted (initiative) // Date and Time confirmed: 15 Nov 2026 @ 10:06 PM GMT
