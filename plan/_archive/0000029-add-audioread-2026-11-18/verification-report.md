---
title: "Verification Report - 0000029-add-audioread"
summary: "How the acceptance criteria were checked by building a fresh image and running real jobs in it."
---
# Verification Report - 0000029-add-audioread

## What ran

The agent built the CPU image with `docker compose build --no-cache` on an arm64 Docker Desktop host. It started the stack with `docker compose -p stems-verify up -d` on port 8010, with new volumes. It ran no command in the container before the first upload. It removed the stack and its volumes afterwards.

## Criteria

| Criterion | Method | Outcome | Evidence |
|-----------|--------|---------|----------|
| REQ-001 AC-1: the `separation` extra pins `audioread` | Read `pyproject.toml`, and run the unit test | verified | The extra holds `audioread==3.1.0`. `test_req_001_ac_1_separation_extra_pins_audioread_exactly` passes |
| REQ-001 AC-2: the image installs `audioread` | `docker run --rm music-stems:local python -c "import audioread"` | verified | Exit 0. The installed versions are `audioread` 3.1.0 and `audio-separator` 0.48.0 |
| REQ-001 AC-3: the two pins are equal | Unit test | verified | `test_req_001_ac_3_audioread_pin_matches_pyproject` passes |
| REQ-002 AC-1: a fresh image imports the library | The same `docker run` as AC-2 | verified | Exit 0 with no command after the build |
| REQ-002 AC-2: a job ends `done` with two stems | `POST /jobs` with an 8 second tone, then `GET /jobs` | verified | The first job ended `done` with `vocals.wav` and `instrumental.wav`. Both files sat in its job folder at 1.4 MB each |

## Finding outside the criteria

The agent uploaded two more jobs to the same container. Both lost their stems, for a cause that `audioread` does not touch.

- A full stems job ended `failed` with `Error opening '/data/jobs/{id}/instrumental.wav': System error.` Its pass 1 stems landed in the first job's folder.
- A third plain job ended `done`, but its folder was empty and its stem download returned 404.

The reused separator keeps the folder of the first job. Backlog entry 0000031 holds the detail. Pass 2 did load `htdemucs_ft.yaml` with no missing module, so risk R-002 did not occur up to that point.

## Not verified

- The GPU image. No GPU host was available.
- A full stems job from start to end, because of the finding above.
