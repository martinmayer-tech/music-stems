---
title: "Risk Register - Add the Docker image and compose file"
summary: "Technical, operational, and security risks with their mitigations."
status: "active"
version: "0.1.0"
---
# Risk Register - Add the Docker image and compose file

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000016-docker-packaging
**Version:** 0.8.0
**Overall Risk Level:** medium

## Risks

| ID | Category | Description | Likelihood | Impact | Mitigation | Status |
|----|----------|------------|------------|--------|-----------|--------|
| R-001 | security | The container binds to all interfaces and a user publishes it beyond loopback, so anyone on the network can upload | low | high | `compose.yaml` publishes on `127.0.0.1`. A test checks the line. The docs warn about editing it | open |
| R-002 | technical | The `audio-separator` pin in the Dockerfile drifts from `pyproject.toml` | medium | medium | A test compares the two | open |
| R-003 | operational | The image is large because the engine pulls PyTorch | high | low | The docs name the size. The CPU extra is the default | open |
| R-004 | technical | A volume owned by root blocks the non-root user from writing | medium | medium | The Dockerfile creates `/data` and `/models` with the service user as owner, so a new named volume inherits it | open |

## Assumptions Logged as Risks

| ID | Assumption | Impact if Wrong | Status |
|----|-----------|----------------|--------|
| A-001 | The NVIDIA container toolkit is present on a GPU host | The GPU job fails at its first run with the engine's error | open |
| A-002 | `python:3.12-slim` installs the `audio-separator[cpu]` wheels | The CI build fails and the step reports it | open |
