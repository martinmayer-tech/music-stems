---
title: "Security Report - 0000016-docker-packaging"
summary: "Findings for the Dockerfile, the compose files, and the CI image build."
---
# Security Report - 0000016-docker-packaging

## Findings

| Finding | Location | Severity | Mitigation |
|---------|----------|----------|------------|
| The container binds to all interfaces, so a published port reaches an upload route with no login | `Dockerfile` (`STEMS_HOST=0.0.0.0`), `compose.yaml` | Medium | The compose file publishes `127.0.0.1` only. A test checks the line, and a comment in the file warns about editing it |
| The container could run as root | `Dockerfile` | Low | The image sets `USER stems` (uid 1000). A test checks for a `USER` line |
| The compiler stays in the image | `Dockerfile` install layer | Low | The same layer purges `gcc` and `libc6-dev` |
| The base image and the PyPI packages carry unknown vulnerabilities | `python:3.12-slim`, `pyproject.toml` | Low | Not scanned. The step adds no Python dependency. The image pins `audio-separator` |
| The CI job could push or run an image | `.github/workflows/ravintio.yml`, job `docker` | Low | The job holds `contents: read`, runs `docker build` only, and a test rejects `docker push`, `docker run`, and `packages: write` |
| The build context could leak the plan or the git history | `.dockerignore` | Low | The file excludes `.git`, `plan`, `ravintio-zero`, `data`, and caches. A test checks three of them |
| Credentials and secrets | whole step | none | The step handles none |

## Risk register cross-check

- R-001 (public publish): mitigated by the loopback port line and its test.
- R-002 (pin drift): mitigated by a test that compares the two pins.
- R-003 (image size): open. The docs name it. It measured 10.8 GB on arm64.
- R-004 (volume ownership): mitigated. The agent restarted the stack, and the user `stems` wrote to both volumes.

## Overall risk rating

Medium, because the service has no login by decision. The step adds no unmitigated critical or high finding.

## Top actions before production

- Approve `audioread` so a job can run in the image (backlog 0000023).
- Keep the `127.0.0.1` prefix on the published port.
