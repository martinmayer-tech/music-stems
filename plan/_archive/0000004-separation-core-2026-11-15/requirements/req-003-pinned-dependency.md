---
title: "Requirement: REQ-003 - Pinned dependency and CI install"
summary: "One exact audio-separator version, installed by CI through a separation extra."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-003 - Pinned dependency and CI install

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000004-separation-core
**Source:** US-003
**Priority:** must-have

## User Story

As an operator, I set `STEMS_MODEL_DIR` and install one pinned `audio-separator` version, so that models persist and results repeat.

## Functional Requirements
- `pyproject.toml` holds a `separation` extra with `audio-separator[cpu]==0.48.0`.
- The `python` CI job installs the `dev` and `separation` extras.
- One test marked `slow` runs a real model and stays out of the CI run.
- The `slow` test skips itself when `audio_separator` does not import.

## Acceptance Criteria
- [ ] AC-1: Exact pin
  - Given the root `pyproject.toml`
  - When a test reads the `separation` extra
  - Then it finds `audio-separator[cpu]` pinned with `==`
- [ ] AC-2: CI install
  - Given the `python` job in the workflow
  - When a test reads the job
  - Then the install step names the `separation` extra
- [ ] AC-3: Slow test excluded
  - Given the pytest settings
  - When CI runs `pytest`
  - Then the `slow` test does not run

## Dependencies
- REQ-001 supplies the function that the slow test calls.
