# Security Report - Add audioread to the image and the separation extra

**Skill:** [validate-and-accept](../skills/ravintio-validate-and-accept/SKILL.md)
**Feature:** 0000029-add-audioread
**Version:** 0.8.1

> It is advisory - the review makes no code changes. All findings require human review before action.

## Summary

**Overall Risk Assessment:** low
**Components Reviewed:** stem-core, stem-service
**Review Scope:** dependency audit and a review of the changed lines

The run changes one line in `pyproject.toml` and three lines in the `Dockerfile`. It adds no route, no input, no file access, and no credential.

## Findings

| ID | Severity | Category | Component | Description | Recommendation | Status |
|----|----------|----------|-----------|-------------|----------------|--------|
| S-001 | low | dependency | stem-core | `pyproject.toml` and the `Dockerfile` pin `audioread` by version and not by hash, as they do for the engine | Add hashes if the project later adopts a lock file | accepted |
| S-002 | medium | data-exposure | stem-service | A later job overwrites the stems of the first job in `/data/jobs/{id}`, so one upload can replace the result of another. The service has one local user by design (ADR-0005). The run did not cause this fault | Fix through backlog entry 0000031 | open |

## Dependency Audit

| Package | Current Version | Known CVEs | Severity | Action Required |
|---------|----------------|------------|----------|----------------|
| audioread | 3.1.0 | none known to the agent. No audit tool ran, because the stack declares none | low | accept-risk |

`audioread` decodes audio through FFmpeg and other back ends. The image already holds FFmpeg, and the engine already decodes user uploads, so the library opens no new input path.

## Threat Model

| Threat | Attack Vector | Affected Component | Likelihood | Impact | Existing Mitigation | Gap |
|--------|--------------|-------------------|------------|--------|--------------------|----|
| A crafted audio file exploits a decoder | Upload through `POST /jobs` | stem-service | low | medium | The port is published on `127.0.0.1` only, and the container runs as a non-root user | No change from version 0.8.0 |

## Risk register cross-check

- R-001, pin drift: mitigated. A test compares the two pins.
- R-002, another missing module: not seen. Pass 1 ran, and pass 2 loaded its model.
- R-003, a stale exact pin: open by decision.

## Recommendations

1. Fix backlog entry 0000031 before relying on more than one job per container start.
