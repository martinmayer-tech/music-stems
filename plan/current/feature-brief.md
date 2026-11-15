---
title: "Feature Brief - Add the two-pass separation core"
summary: "A split() function in stem-core that wraps audio-separator in two passes."
status: "approved"
version: "0.1.0"
---
# Feature Brief - Add the two-pass separation core

**Feature ID:** 0000004-separation-core

## Business Goal

No code wraps `audio-separator` today. Sections 3 and 7 of `open-source-stem-separation-guide.md` describe a two-pass pipeline that exists only as a sketch. This step builds the function that every later step calls.

## Features

| Feature | User Stories | Priority | Wave |
|---------|-------------|----------|------|
| Two-pass `split()` | As a developer, I call `split(mix, out)` and get the vocals and instrumental WAV paths, so that I split a mix with one call. | must-have | 1 |
| Optional full stems | As a developer, I call `split(mix, out, full_stems=True)` and get five WAV paths, so that I also get drums, bass, and other. | must-have | 1 |
| Configured models and pin | As an operator, I set `STEMS_MODEL_DIR` and install one pinned `audio-separator` version, so that models persist and results repeat. | must-have | 1 |

## Waves

One wave. The feature ships when both observable conditions pass.

## Target Architecture

### Components

| Component | Type | New or Existing | Responsibility |
|-----------|------|-----------------|---------------|
| stem-core | component-pack | existing | Holds `split()`. Step 3 adds the `stems` command. |

### Data Ownership

None. `stem-core` owns no data.

### Integration Points

| From | To | Method | Contract |
|------|-----|--------|----------|
| stem-core | audio-separator | Python API | `Separator`, `load_model`, `separate` |

## Stack

| Concern | Decision |
|---------|----------|
| Language | Python |
| Runtime | Python 3.12 in CI, 3.13 locally |
| Framework | none |
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
- `split(mix_path, out_dir, full_stems=False)` in `stem_core`.
- Pass 1 with `model_bs_roformer_ep_317_sdr_12.9755.ckpt`. Pass 2 with `htdemucs_ft.yaml` on the instrumental.
- WAV output, the model folder from `STEMS_MODEL_DIR`, and absolute returned paths.
- A `separation` extra in `pyproject.toml` that pins `audio-separator[cpu]` with `==`.
- One `slow` smoke test with a real model.

### Out of Scope
- The `stems` command, the queue, the API, the web page, and Docker.
- Model choice by the caller and ensembles.

### Deferred
- Model choice and ensembles wait for step 7.

## Non-Functional Requirements

| NFR | Target | Measurement |
|-----|--------|-------------|
| Repeatability | One exact `audio-separator` version | `pyproject.toml` pins it with `==` |

## Constraints and Assumptions

### Constraints
- Unit tests inject a fake separator and import `audio_separator` lazily.
- The real-model test carries the `slow` marker and stays out of CI.

### Assumptions
- `audio-separator[cpu]` installs on Python 3.12 in CI. It may not install on local Python 3.13.

## Scenario Paths

**Happy path:** A developer calls `split` on a WAV mix. Pass 1 writes vocals and instrumental. The call returns two absolute paths.

> The call returns the two paths, or five with `full_stems=True`.

**First-run path:** The model folder holds no models. `audio-separator` downloads them into `STEMS_MODEL_DIR` on first use.

> The first call is slow. Later calls reuse the models.

**Error / sad path:** The mix file is missing, or a model fails to load.

> The function raises an error and returns no partial list.

**Cross-session continuity:** The function keeps no state. A repeat call rewrites the output files.

> A run that stops mid-way leaves files that the next call overwrites.

## Acceptance Criteria

- [ ] `split(mix, out)` returns 2 existing WAV paths.
- [ ] `split(mix, out, full_stems=True)` returns 5.
- [ ] Every returned path is absolute.
- [ ] `pyproject.toml` pins `audio-separator` with `==`.
