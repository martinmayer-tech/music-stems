---
title: "Feature Brief - Add the command-line interface"
summary: "A stems command in stem-core that splits a mix, reports the environment, and lists the models."
status: "approved"
version: "0.1.0"
---
# Feature Brief - Add the command-line interface

**Feature ID:** 0000006-command-line-interface

## Business Goal

A user can reach the separation core only from Python code. The guide calls for a scriptable tool. This step adds a `stems` command that splits a mix from a shell, so scripts and later steps can call it.

## Features

| Feature | User Stories | Priority | Wave |
|---------|-------------|----------|------|
| `stems split` | As a user, I run `stems split mix.wav --output-dir out`, so that I get one output path per line to use in a script. | must-have | 1 |
| Full stems option | As a user, I add `--full-stems`, so that I also get drums, bass, and other. | must-have | 1 |
| `stems env` | As a user, I run `stems env`, so that I see the Python version, FFmpeg, and the device before I split. | should-have | 1 |
| `stems models` | As a user, I run `stems models`, so that I see which models the command uses. | should-have | 1 |

## Waves

One wave. The feature ships when both observable conditions pass.

## Target Architecture

### Components

| Component | Type | New or Existing | Responsibility |
|-----------|------|-----------------|---------------|
| stem-core | component-pack | existing | Holds `split()` and now the `stems` command. |

### Data Ownership

None. `stem-core` owns no data.

### Integration Points

| From | To | Method | Contract |
|------|-----|--------|----------|
| stems command | `split()` | Python call | `split(mix, out, full_stems, separator_factory)` |

## Stack

| Concern | Decision |
|---------|----------|
| Language | Python |
| Runtime | Python 3.12 in CI, 3.13 locally |
| Framework | `argparse` from the standard library |
| Frontend | none |
| Database | none |
| ORM | none |
| Testing | pytest |
| IaC | none |
| Cloud | none |
| Compute | none |
| CI | GitHub Actions |
| Build target | ci-only |

## Scope Boundaries

### In Scope
- A `stems` command with the subcommands `split`, `env`, and `models`.
- A `stems` console script in `pyproject.toml` and `python -m stem_core`.
- Exit code 0 on success. A missing input file or a failed separation exits non-zero with one error line.

### Out of Scope
- A caller-chosen model and ensembles.
- The queue, the API, the web page, and Docker.

### Deferred
- Caller model choice and ensembles wait for step 7.

## Non-Functional Requirements

| NFR | Target | Measurement |
|-----|--------|-------------|
| Exit codes | 0 on success, non-zero on failure | Unit tests check each code |
| Start-up cost | `stems env` and `stems models` import no model library | A unit test checks that `audio_separator` stays out of `sys.modules` |

## Constraints and Assumptions

### Constraints
- Use `argparse`. Add no dependency.
- Unit tests inject a fake separator. The code imports `audio_separator` lazily.

### Assumptions
- `torch` may be absent. `stems env` then reports the device as `cpu`.

## Scenario Paths

**Happy path:** A user runs `stems split mix.wav --output-dir out`. The command prints one absolute path per line and exits 0.

> With `--full-stems` the command prints five paths.

**First-run path:** The model folder holds no models. `audio-separator` downloads them on the first call.

> The first run is slow. Later runs reuse the models.

**Error / sad path:** The input file is missing, or a model fails to load.

> The command prints one error line to standard error, prints no path, and exits non-zero.

**Cross-session continuity:** The command keeps no state. A repeat run rewrites the output files.

> A run that stops midway leaves files that the next run overwrites.

## Acceptance Criteria

- [ ] `stems split mix.wav --output-dir out` exits 0 and prints one output path per line.
- [ ] `stems split` with a missing input file exits non-zero and prints one error line.
- [ ] `--full-stems` prints five paths.
- [ ] `stems env` reports the Python version, FFmpeg, and the device.
- [ ] `stems models` lists the supported models.
