---
title: "Initiative: 0000001 - Stem separation service"
summary: "A self-hosted, scriptable stem separation service with a Python core, a CLI, a job queue, an HTTP API, a web page, and a Docker image."
status: "active"  # proposed | charted | active | delivered | blocked
---
# Initiative: 0000001 - Stem separation service

**Goal:** Build the solution in `open-source-stem-separation-guide.md`. The result is a self-hosted service that splits a mix into stems with `audio-separator`, for non-commercial use.

**Branch:** initiative/0000001-stem-separation-service

**Status:** active

**Position:** 8

**Speed:** standard

**Step CI fixes:** allowed

**Concurrency:** 1

## Components

The steps build three components under `src/`.

| Component | Holds | Steps |
|-----------|-------|-------|
| `stem-core` | The two-pass `split()` function and the `stems` command | 2, 3, 7 |
| `stem-service` | The job store, the worker, and the HTTP API | 4, 5, 7 |
| `stem-web` | The web page that the API serves | 6, 7 |

## Stop conditions

- A step prints a `Blocked:` line.
- CI fails on a step PR and the fix lies outside the step's scope.
- A step needs a library or service that no `## Dependencies` row lists.
- A step needs a destructive schema change.

## Schema changes

**Unpredicted additive changes:** pre-approved

| Step | Component | Change | Kind |
|------|-----------|--------|------|
| 1 | none | none | none |
| 2 | none | none | none |
| 3 | none | none | none |
| 4 | stem-service | New SQLite table `jobs`: `id TEXT`, `status TEXT`, `input_path TEXT`, `full_stems INTEGER`, `options TEXT`, `outputs TEXT`, `error TEXT`, `created_at TEXT`, `started_at TEXT`, `finished_at TEXT` | additive |
| 5 | none | none | none |
| 6 | none | none | none |
| 7 | none | none | none |
| 8 | none | none | none |

## Dependencies

| Step | Name | Kind | Purpose |
|------|------|------|---------|
| 1 | pytest | library | Unit test runner |
| 1 | ruff | library | Lint and format check |
| 2 | audio-separator[cpu] | library | The separation engine, at one exact version |
| 3 | none | none | The command uses `argparse` from the standard library |
| 4 | none | none | The job store uses `sqlite3` from the standard library |
| 5 | fastapi | library | The HTTP API |
| 5 | uvicorn | library | The server that runs the API |
| 5 | python-multipart | library | File upload parsing for FastAPI |
| 5 | httpx | library | The test client for the API tests |
| 6 | none | none | The page uses plain HTML, CSS, and JavaScript |
| 7 | none | none | none |
| 8 | python:3.12-slim | service | The base image |
| 8 | ffmpeg | library | The Debian package that the image installs |
| 8 | audio-separator[gpu] | library | The GPU extra, which a build argument selects |

## Decisions

| Step | Fork | Pre-approved answer | Bump effect |
|------|------|---------------------|-------------|
| 1 | Which version step 1 releases | `docs/about.md` and `product.yml` hold `0.0.0`, so step 1 releases `0.1.0`. Step 1 adds each new component to `product.yml` | none |
| 1-8 | Whether the product version tracks the pack version | It never does. `ravintio-zero/version-files.txt` lists `docs/about.md` and `product.yml` only. No step edits that list or `ravintio-zero/component.yml` | none |
| 1-8 | Which Python version to target | Target Python 3.12 in CI and in Docker. Set `requires-python` to `>=3.10`. Local runs use Python 3.13 | none |
| 1-8 | A step finds work outside its scope | File a backlog entry and keep the step's scope | none |
| 2 | Which `audio-separator` version to pin | Pin the newest PyPI release on the day step 2 runs, with `==` | none |
| 2-8 | Tests need a real model | Unit tests inject a fake separator, and the code imports `audio_separator` lazily. One real-model smoke test carries the `slow` marker and stays out of CI | none |
| 2 | `separate()` returns relative paths | Resolve each path against the output folder and return absolute paths | none |
| 2 | `audio-separator` fails to install on local Python 3.13 | Run the unit tests without it and rely on CI for the install check | none |
| 3 | Which CLI library to use | Use `argparse`. Name the command `stems` | none |
| 4 | Which queue backend to use | Use one SQLite file and one worker thread per device. Add no broker | none |
| 4 | Where the service keeps its data | Read `STEMS_DATA_DIR`, default `./data`. Read `STEMS_MODEL_DIR` for models | none |
| 5 | Whether the API needs a login | Add no login. Bind to `127.0.0.1` by default | none |
| 5 | Which uploads to accept | Accept WAV, FLAC, MP3, and M4A up to 500 MB. Read the limit from `STEMS_MAX_UPLOAD_MB` | none |
| 6 | Which front-end toolchain to use | Use plain HTML, CSS, and JavaScript with no build | none |
| 6 | How to test the page | Test the served files and the API calls over HTTP. Add no browser automation | none |
| 7 | Which models a caller may pick | Allow the four models in section 8 of the guide and the ensemble presets of `audio-separator` | none |
| 8 | Whether CI builds the GPU image | CI builds the CPU image only and runs no separation in it | none |
| 8 | Whether to publish the image | Publish no image | none |

## Baselines

| Step | Target | Baseline | Source |
|------|--------|----------|--------|
| 1 | none | none | none |
| 2 | none | none | none |
| 3 | none | none | none |
| 4 | none | none | none |
| 5 | none | none | none |
| 6 | none | none | none |
| 7 | none | none | none |
| 8 | none | none | none |

## Criteria

| Step | Criterion | Noise and margin | Checked in |
|------|-----------|------------------|------------|
| 1 | The Python job runs lint and unit tests on a pull request to `initiative/**` | An exact pass or fail, with no noise | CI |
| 2 | `split()` returns 2 paths, and 5 with `full_stems` | An exact count, with no noise | local |
| 2 | The real-model smoke test writes vocals and instrumental WAV files that hold sound | The model download makes the run time vary. The test sets no time limit | local |
| 3 | `stems split` exits 0 for a valid file and non-zero for a missing one | An exact exit code, with no noise | local |
| 4 | Two queued jobs on one device never overlap | Exact with a fake separator | local |
| 5 | An upload reaches `done` and each stem downloads as WAV | Exact with a fake separator | local |
| 6 | The API root returns the page | An exact pass or fail, with no noise | local |
| 7 | A job that names an unlisted model fails before any model loads | An exact pass or fail, with no noise | local |
| 8 | `docker build` of the CPU image succeeds | Network speed makes the build time vary. The check sets no time limit | CI |

## P1 skips

| Step | Skip P1 | Reason |
|------|---------|--------|
| 1 | no | The step adds a project layout and a CI job |
| 2 | no | The step adds code |
| 3 | no | The step adds code |
| 4 | no | The step adds code and a schema |
| 5 | no | The step adds code |
| 6 | no | The step adds code |
| 7 | no | The step adds code |
| 8 | no | The step adds a Dockerfile and a CI job |

## Steps

| Step | Feature id | Title | Backlog entries | Bump | Version | Status | Lane | After |
|------|------------|-------|-----------------|------|---------|--------|------|-------|
| 1 | 0000002-python-scaffold | Scaffold the Python project and its CI | 0000003 | minor | 0.1.0 | merged | app | |
| 2 | 0000004-separation-core | Add the two-pass separation core | 0000005 | minor | 0.2.0 | merged | app | 1 |
| 3 | 0000006-command-line-interface | Add the command-line interface | 0000007 | minor | 0.3.0 | merged | app | 2 |
| 4 | 0000008-job-queue-worker | Add the job queue and worker | 0000009 | minor | 0.4.0 | merged | app | 3 |
| 5 | 0000010-http-api | Add the HTTP API | 0000011 | minor | 0.5.0 | merged | app | 4 |
| 6 | 0000012-web-front-end | Add the web front end | 0000013 | minor | 0.6.0 | merged | app | 5 |
| 7 | 0000014-model-ensemble-options | Add model choice and ensemble options | 0000015 | minor | 0.7.0 | merged | app | 6 |
| 8 | 0000016-docker-packaging | Add the Docker image and compose file | 0000017 | minor | | pending | app | 7 |

## Merges

The merge queue adds one row for each step it merges. See the merge queue section of the roadmap standards.

| Step | PR | Merge commit | Version | Merged at |
|------|----|--------------|---------|-----------|
| 1 | #5 | tag v0.1.0 | 0.1.0 | 2026-11-15T22:00:11Z |
| 2 | #6 | tag v0.2.0 | 0.2.0 | 2026-11-15T22:50:35Z |
| 3 | #7 | tag v0.3.0 | 0.3.0 | 2026-11-15T23:51:17Z |
| 4 | #8 | tag v0.4.0 | 0.4.0 | 2026-11-16T00:29:27Z |
| 5 | #9 | tag v0.5.0 | 0.5.0 | 2026-11-16T01:27:02Z |
| 6 | #10 | tag v0.6.0 | 0.6.0 | 2026-11-16T02:06:56Z |
| 7 | #11 | tag v0.7.0 | 0.7.0 | 2026-11-16T03:04:03Z |
