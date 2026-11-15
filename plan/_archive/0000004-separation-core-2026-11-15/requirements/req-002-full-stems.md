---
title: "Requirement: REQ-002 - Full stems"
summary: "full_stems=True adds a second pass that returns drums, bass, and other."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-002 - Full stems

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000004-separation-core
**Source:** US-002
**Priority:** must-have

## User Story

As a developer, I call `split(mix, out, full_stems=True)`, so that I also get drums, bass, and other.

## Functional Requirements
- Pass 2 loads `htdemucs_ft.yaml` and separates the instrumental file that pass 1 wrote.
- Pass 2 names its stems `drums`, `bass`, and `other`.
- Pass 2 renames the residual vocals stem so that it never overwrites the pass 1 vocals file. The function drops that residual file and leaves it out of the result.
- The result lists the two pass 1 paths and then the three pass 2 paths.

## Acceptance Criteria
- [ ] AC-1: Five paths
  - Given a mix file and a fake separator
  - When the developer calls `split(mix, out, full_stems=True)`
  - Then the call returns 5 absolute paths
- [ ] AC-2: Pass 1 vocals survive
  - Given the same call
  - When the call returns
  - Then the `vocals.wav` file from pass 1 still holds its pass 1 content
- [ ] AC-3: Pass 2 input
  - Given the same call
  - When pass 2 starts
  - Then the separator receives the instrumental path from pass 1

## Dependencies
- REQ-001 supplies pass 1.
