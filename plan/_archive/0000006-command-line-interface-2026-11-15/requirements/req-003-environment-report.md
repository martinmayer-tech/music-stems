---
title: "Requirement: REQ-003 - Environment report"
summary: "stems env reports the Python version, FFmpeg, and the device."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-003 - Environment report

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000006-command-line-interface
**Source:** US-003
**Priority:** should-have

## User Story

As a user, I run `stems env`, so that I see the Python version, FFmpeg, and the device before I split.

## Functional Requirements
- `stems env` prints three lines: `python: {version}`, `ffmpeg: {first line of ffmpeg -version, or not found}`, and `device: {cuda, mps, or cpu}`.
- The command reports `cpu` when `torch` is absent or its import fails.
- The command runs `ffmpeg` with an argument list and no shell. A missing binary is not an error.
- The command exits 0 in every case and loads no model.

## Acceptance Criteria
- [ ] AC-1: Three lines
  - Given injected probes for Python, FFmpeg, and the device
  - When the user runs `stems env`
  - Then the command prints the three lines and exits 0
- [ ] AC-2: Missing tools
  - Given probes that find no FFmpeg and no `torch`
  - When the user runs `stems env`
  - Then the command prints `ffmpeg: not found` and `device: cpu` and exits 0

## Dependencies
- None.
