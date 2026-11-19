---
title: "Risk Register - Add audioread to the image and the separation extra"
summary: "Technical, operational, and security risks with their mitigations."
status: "active"
version: "0.1.0"
---
# Risk Register - Add audioread to the image and the separation extra

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000029-add-audioread
**Version:** 0.8.1
**Overall Risk Level:** low

## Risks

| ID | Category | Description | Likelihood | Impact | Mitigation | Status |
|----|----------|------------|------------|--------|-----------|--------|
| R-001 | technical | The `audioread` pin in the `Dockerfile` drifts from `pyproject.toml` | medium | medium | A test compares the two | open |
| R-002 | technical | `audio-separator` 0.48.0 misses another module that pass 1 does not reach | low | medium | P3 runs a real job in a fresh image and reports what it shows | open |
| R-003 | operational | An exact pin holds `audioread` at 3.1.0 after a later fix release | low | low | The pin sits beside the engine pin, so one edit moves both | open |

## Assumptions Logged as Risks

| ID | Assumption | Impact if Wrong | Status |
|----|-----------|----------------|--------|
| A-001 | `audioread` 3.1.0 works with `audio-separator` 0.48.0 on Python 3.12 | The hand-run job fails, and the run stops with the engine's error | open |
