---
title: "Story Map - 0000016-docker-packaging"
summary: "The backbone of activities and steps, with the requirement that covers each step."
---
# Story Map - 0000016-docker-packaging

> Each row is one step under an activity. The Requirement cell names a requirement or a gap.

## Backbone

| Activity | Step | Story | Requirement |
|----------|------|-------|-------------|
| Build the image | Build one image with Python 3.12 and FFmpeg | US-001 | REQ-001 |
| Run the stack | Run `docker compose up` and keep models and jobs | US-002 | REQ-002 |
| Guard the build | Fail a pull request when the CPU image fails to build | US-003 | REQ-003 |

## Gaps

- Publish the image to a registry: gap: out of scope. The chart says publish no image.
- Run a separation in CI: gap: out of scope. The chart says CI builds the CPU image only.
