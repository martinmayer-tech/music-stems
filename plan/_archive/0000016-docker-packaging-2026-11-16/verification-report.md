---
title: "Verification Report - 0000016-docker-packaging"
summary: "How the acceptance criteria were checked by running the image and the compose stack."
---
# Verification Report - 0000016-docker-packaging

## What ran

The agent built the CPU image with `docker build` on an arm64 Docker Desktop host. It started the stack with `docker compose -p step8 up -d --build` on port 18000. It removed the stack and its volumes afterwards.

## Criteria

| Criterion | Method | Outcome | Evidence |
|-----------|--------|---------|----------|
| `docker build` of the CPU image succeeds | Local build | verified | The build ended with the image `music-stems:step8`, 10.8 GB on disk. CI checks it again on x86 |
| `docker compose up` serves the page on a local port | `curl` against `127.0.0.1:18000/` | verified | Status 200. `GET /jobs` returned `[]`. The healthcheck reported `healthy`. The process ran as the user `stems` |
| A restart keeps the models and the finished jobs | `compose restart`, then `compose down` and `up` | verified | The job list held the same job id after both. A marker file in `/models` survived both. A real job downloaded its model into `/models` |
| A build argument selects the GPU extra | Text check of the Dockerfile and `compose.gpu.yaml` | unverified (docs only) | A unit test reads `audio-separator[${STEMS_EXTRA}]` and the override. No GPU host was available, so no GPU image was built |
| A job ends `done` in the image | Upload of a tone file | failed, then verified after a manual fix | The first job ended `failed` with `No module named 'audioread'`. After `pip install audioread` in the container, a job ended `done` with `vocals.wav` and `instrumental.wav`. Backlog entry 0000023 tracks the fix |

## Finding

The image cannot separate audio as built. `audio-separator` 0.48.0 imports `audioread`, and `librosa` 1.0.1 no longer installs it. The chart lists no `audioread` row, so the dependency rule stops the agent from adding it. The finding goes to the human in the PR.
