---
title: "Discovery - 0000029-add-audioread"
summary: "Raw discovery-pass findings: what the orchestrator knew before coaching began."
---
# Discovery - 0000029-add-audioread

## Header (all modes)

| Field | Value |
|-------|-------|
| Adoption mode detected | `standard-iterative` |
| Detection signal | `docs/about.md` at 0.8.0 and `src/` beside an archive |
| Git pre-flight | Branch `feat/0000029-add-audioread`, cut from `main` at `49f0da3`. `main` matches `origin/main` |
| Skills inbox | empty |
| Track | light |

## Mode Findings

### Standard Iterative

- Current version (`docs/about.md` and `product.yml`): `0.8.0`. The version policy is `explicit`.
- Prior features (`plan/_archive/`): 0000002 to 0000016, the eight steps of initiative 0000001.
- Constraining ADRs: `docs/adr/0001` to `0007`. None rules on `audioread`.
- Component map: `stem-core` holds `split()` and the `stems` command. `stem-service` holds the job store, the worker, the API, and the Docker files. `stem-web` holds the page files.
- Repo instructions: `agent-permissions.md` and `grep-tests-before-moving-files.md`.
- Pending migrations: 0007 and 0009. Neither `Applies when:` condition holds in this repo.
- Backlog: entry 0000023 is the source of this run. Entries 0000018 to 0000022 and 0000024 to 0000028 describe pack gaps.
- The fault: a job in the CPU image ends `failed` with `No module named 'audioread'`. `audio-separator` 0.48.0 imports `audioread`, and `librosa` 1.0.1 no longer installs it.
- Finding beyond the entry: the `Dockerfile` installs `.[service]` and `audio-separator` by name. It does not install the `separation` extra. A change to the extra alone leaves the image broken.
- Existing seams: the `separation` extra in `pyproject.toml` pins `audio-separator[cpu]==0.48.0`. The `Dockerfile` repeats the pin in `AUDIO_SEPARATOR_VERSION`. `src/stem-core/tests/test_pin_ci.py` and `src/stem-service/tests/test_docker_image.py` read both files as text.
- Package index: `audioread` 3.1.0 is the latest release.
- Local toolchain: Docker 29.9.3 and Python 3.13.16.
- Baseline: the pack suite runs in a clean clone. Its output goes to `plan/current/baseline-failures.md`.
