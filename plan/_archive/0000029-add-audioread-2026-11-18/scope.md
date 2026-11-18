---
title: "Scope - Add audioread to the image and the separation extra"
summary: "Defines explicit boundaries of what is in scope and out of scope."
status: "active"
version: "0.1.0"
---
# Scope - Add audioread to the image and the separation extra

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000029-add-audioread
**Version:** 0.8.1

## In Scope

- `audioread==3.1.0` in the `separation` extra of `pyproject.toml`.
- The build argument `AUDIOREAD_VERSION` in the `Dockerfile`, and its install.
- Tests that read both files as text and compare the pins.
- The component docs, the living docs, and ADR-0009.
- One real job through a fresh image, run by hand.
- The removal of backlog entry 0000023.

## Out of Scope

- Run a separation in CI: gap: out of scope.
- Run a job in the GPU image: gap: out of scope.
- A newer `audio-separator`.
- The pack gaps in backlog entries 0000018 to 0000030.

## Deferred

- Nothing deferred.
