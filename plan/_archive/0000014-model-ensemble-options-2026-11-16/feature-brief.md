---
title: "Feature Brief - Add model choice and ensemble options"
summary: "A caller picks the pass 2 model, a pass 1 ensemble preset, and one stem to write. split(), the stems command, the API, and the page expose the options and reject any value outside an allowlist."
status: "approved"
version: "0.1.0"
---
# Feature Brief - Add model choice and ensemble options

**Feature ID:** 0000014-model-ensemble-options

## Business Goal

Every job uses the two default models. Sections 8 and 9 of the guide list other models and ensembles that trade speed for quality. This step lets a caller choose them, from a fixed allowlist.

## Features

| Feature | User Stories | Priority | Wave |
|---------|-------------|----------|------|
| Options in `split()` | As a developer, I pass a pass 2 model, an ensemble preset, and a single stem to `split()`, so that a job uses the models I want. | must-have | 1 |
| Options in the command | As a user, I pass the same options to `stems split`, so that I choose from the shell. | must-have | 1 |
| Options in the API | As a user, I send the options with `POST /jobs`, so that the queued job uses them. | must-have | 1 |
| Options on the page | As a user, I choose the options on the upload form, so that I need no `curl`. | must-have | 1 |

## Waves

One wave. The feature ships when the observable condition passes.

## Target Architecture

### Components

| Component | Type | New or Existing | Responsibility |
|-----------|------|-----------------|---------------|
| stem-core | library | existing | Holds the allowlists, validates the options, and runs the passes with them. |
| stem-service | microservice | existing | Accepts the options on `POST /jobs`, stores them in `jobs.options`, and passes them to `split()`. |
| stem-web | microfrontend | existing | Adds three selects to the upload form. |

### Data Ownership

`stem-service` keeps ownership of the `jobs` table. The `options` column already exists, so the step adds no field. `stem-core` and `stem-web` own no data.

### Integration Points

| From | To | Method | Contract |
|------|-----|--------|----------|
| Page | API | `fetch` | `POST /jobs` with the form fields `model`, `ensemble_preset`, and `single_stem` |
| API | stem-core | Python call | `validate_options()` |
| Worker | stem-core | Python call | `split(..., model, ensemble_preset, single_stem)` |

## Stack

| Concern | Decision |
|---------|----------|
| Language | Python, HTML, CSS, JavaScript |
| Runtime | Python 3.12 in CI, 3.13 locally |
| Framework | FastAPI for the route, argparse for the command |
| Frontend | plain HTML, CSS, and JavaScript with no build |
| Database | SQLite, no schema change |
| ORM | none |
| Testing | pytest with the FastAPI test client and fake separators |
| IaC | none |
| Cloud | none |
| Compute | none |
| CI | GitHub Actions |
| Build target | ci-only |

## Scope Boundaries

### In Scope
- The allowlists: three pass 2 models, nine ensemble presets, and seven stem names.
- `validate_options()`, and the new `split()` arguments.
- The `--model`, `--ensemble-preset`, and `--single-stem` flags, and the `stems models` listing.
- The three form fields on `POST /jobs`, and the pass-through from the worker to `split()`.
- Three selects on the page.
- Tests, component docs, living docs, and the OpenAPI spec.

### Out of Scope
- A pass 1 model choice. Pass 1 keeps its default model unless a preset replaces it.
- A free-text model name or a model file upload.
- A new route that lists the options.
- A schema change.

### Deferred
- Nothing deferred.

## Non-Functional Requirements

| NFR | Target | Measurement |
|-----|--------|-------------|
| Fail before load | A job that names an unlisted option fails before any model loads | A test counts `load_model` calls on a fake separator |
| Clear error | The error names the option, the bad value, and the allowed values | A test reads the message |

## Constraints and Assumptions

### Constraints
- Reject any value outside the allowlist, at every entry point.
- Add no dependency and no schema change. The chart lists none.
- Unit tests inject a fake separator. One real-model smoke test stays out of CI.

### Assumptions
- The preset names match `audio-separator` 0.48.0, the pinned version.

## Scenario Paths

**Happy path:** A user sends a mix with `htdemucs_6s.yaml` and the full stems option. The job ends `done` and lists drums, bass, other, guitar, and piano stems with the two pass 1 stems.

> Pass 2 keeps the stems that the chosen model writes.

**First-run path:** A user sends no option. The job runs the two default models, as in step 6.

> The first use of a new model downloads it.

**Error / sad path:** A caller names an unlisted model, an unknown preset, an unknown stem, or a stem that the chosen model never writes.

> The caller gets a clear error before any model loads. The API answers 422, and the command exits 1.

**Cross-session continuity:** A queued job holds its options in `jobs.options`.

> A restart requeues the job, and the worker reads the stored options again.

## Acceptance Criteria

- [ ] A job with `htdemucs_6s.yaml` and full stems returns guitar and piano stems.
- [ ] A job that names an unlisted model fails with a clear error before any model loads.
- [ ] A preset and a single stem reach the engine through `split()`.
- [ ] The command, the API, and the page expose the three options.
