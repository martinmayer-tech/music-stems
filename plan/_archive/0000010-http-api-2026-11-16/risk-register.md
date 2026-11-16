---
title: "Risk Register - Add the HTTP API"
summary: "Technical, operational, and security risks with their mitigations."
status: "active"
version: "0.1.0"
---
# Risk Register - Add the HTTP API

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000010-http-api
**Version:** 0.5.0
**Overall Risk Level:** medium

## Risks

| ID | Category | Description | Likelihood | Impact | Mitigation | Status |
|----|----------|------------|------------|--------|-----------|--------|
| R-001 | security | A crafted file name or stem name reaches a file outside the data folder | medium | high | The upload route keeps the last part of the name and writes into a random folder. The stem route looks the name up in the job's stored outputs. Tests send `..` and a nested name | open |
| R-002 | security | An operator binds the service to a public address with `STEMS_HOST`, and anyone can upload | low | high | The default is `127.0.0.1`. The docs warn that the service has no login | open |
| R-003 | operational | A large upload fills the disk | low | medium | The route stops at `STEMS_MAX_UPLOAD_MB` and deletes the partial file | open |
| R-004 | technical | The worker thread outlives a test app and holds a database file | medium | low | `create_app()` stops its worker at shutdown. Tests use the app as a context manager | open |
| R-005 | technical | A real `Separator` ignores a changed `output_dir`, so a job writes to the wrong folder | medium | medium | Carried from step 4. The first real run shows any gap | open |

## Assumptions Logged as Risks

| ID | Assumption | Impact if Wrong | Status |
|----|-----------|----------------|--------|
| A-001 | The service trusts a caller on the same host | An open upload route on a shared host | open |
| A-002 | Every finished job lists WAV paths in `outputs` | A stem downloads with the wrong media type | open |
