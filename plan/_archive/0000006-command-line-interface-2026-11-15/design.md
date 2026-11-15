# Design - 0000006-command-line-interface

## Feature
- Problem: A user can reach the separation core only from Python code, so no script can split a mix from a shell.
- Adoption mode: standard-iterative (signal: `docs/about.md` at 0.2.0 and `src/` beside an archive)
- Feature ID: 0000006-command-line-interface
- Discovery: see `plan/current/discovery.md`

## Product Layer
- User stories:
  - US-001: As a user, I run `stems split mix.wav --output-dir out`, so that I get one output path per line to use in a script.
  - US-002: As a user, I add `--full-stems`, so that I also get drums, bass, and other.
  - US-003: As a user, I run `stems env`, so that I see the Python version, FFmpeg, and the device before I split.
  - US-004: As a user, I run `stems models`, so that I see which models the command uses.
- Acceptance criteria confirmed: 5
- Constraints: `argparse` only, no new dependency. Python 3.12 in CI, `requires-python >=3.10`. Unit tests use a fake separator. The code imports `audio_separator` lazily.
- Integrations: `split()` from `stem_core.separation`

## Architecture Layer
- Latency target: deferred - recorded in scope
- Availability target: not applicable
- Scalability target: not applicable
- Security: no network surface, no auth, data classification none. The command reads a caller-supplied path and writes to a caller-supplied folder. It runs `ffmpeg -version` with an argument list and no shell.
- Data privacy: no regulated data
- Observability: standard defaults. Results go to standard output and errors to standard error.
- Cost boundary: not constrained

## Engineering Layer
- Stack: Python 3.12 (CI) / argparse / pytest / ruff / GitHub Actions / Build target ci-only
- Components: `stem-core` holds the command in `stem_core/cli.py`, with `stem_core/__main__.py` for `python -m stem_core`.
- Data ownership: none
- Deployment: none. A `stems` console script in `pyproject.toml` installs the command.
- API versioning: not applicable

## Component Paths
- src/stem-core/
- docs/
- plan/
- pyproject.toml

## Scope
- In: `stems split` with `--output-dir` and `--full-stems`, `stems env`, `stems models`, the console script, `python -m stem_core`, exit codes, and unit tests with a fake separator
- Out: caller model choice, ensembles, the queue, API, web page, Docker
- Deferred: caller model choice and ensembles wait for step 7

## Assumptions
- `torch` may be absent in the test environment - impact if wrong: none, because `stems env` reports `cpu` when the import fails.
- `ffmpeg` may be absent - impact if wrong: none, because `stems env` reports `not found` and exits 0.

## Risks
- Packaging `stem_core` for the console script changes the install in CI. Likelihood low, impact medium. CI runs `pip install ".[dev,separation]"` on the pull request and shows any failure.
- `stems env` probes differ per machine. Likelihood medium, impact low. Tests inject the probes.

## Dependencies
- Upstream: step 2 (`split()`)
- Downstream: steps 4, 5, and 7 call `split()`. Step 7 extends `stems models`.
- Approved dependencies: none

## Active Skills
None

## Skill Map
| Requirement | Best-fit Skill | Rationale |
|-------------|----------------|-----------|
| REQ-001 `stems split` | ravintio-implement | One module with injected-fake tests |
| REQ-002 `stems env` and `stems models` | ravintio-implement | Pure functions with injected probes |
| REQ-003 console script and module entry | ravintio-implement | Config change with a subprocess test |

## Repo Instructions
- `agent-permissions.md`: standing commit, push, PR, and squash-merge grants. Never merge or push to `main`.
- `grep-tests-before-moving-files.md`: grep the test folders before moving a file.

## Confirmation
Human confirmed this design before proceeding: draft-accepted (initiative) // Date and Time confirmed: 15 Nov 2026 @ 10:54 p.m. GMT
