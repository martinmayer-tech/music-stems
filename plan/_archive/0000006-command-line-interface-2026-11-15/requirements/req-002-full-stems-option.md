---
title: "Requirement: REQ-002 - Full stems option"
summary: "--full-stems makes stems split print five paths."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-002 - Full stems option

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000006-command-line-interface
**Source:** US-002
**Priority:** must-have

## User Story

As a user, I add `--full-stems`, so that I also get drums, bass, and other.

## Functional Requirements
- `--full-stems` passes `full_stems=True` to `split()`.
- Without the flag, the command passes `full_stems=False`.
- The command prints the paths in the order that `split()` returns them.

## Acceptance Criteria
- [ ] AC-1: Five paths
  - Given a mix file and a fake separator
  - When the user runs `stems split mix.wav --full-stems`
  - Then the command prints 5 paths and exits 0
- [ ] AC-2: Two paths by default
  - Given a mix file and a fake separator
  - When the user runs `stems split mix.wav` with no flag
  - Then the command prints 2 paths

## Dependencies
- REQ-001.
