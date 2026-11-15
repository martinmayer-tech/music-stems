---
title: "Requirement: REQ-004 - Model list"
summary: "stems models lists the models that stems split uses."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-004 - Model list

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000006-command-line-interface
**Source:** US-004
**Priority:** should-have

## User Story

As a user, I run `stems models`, so that I see which models the command uses.

## Functional Requirements
- `stems models` prints one line for each model that `split()` uses: the role, then the model file name.
- The lines come from the `VOCALS_MODEL` and `FULL_STEMS_MODEL` constants in `stem_core.separation`.
- The command imports no model library and exits 0.

## Acceptance Criteria
- [ ] AC-1: Both models listed
  - Given the `stem_core` package
  - When the user runs `stems models`
  - Then the output names `model_bs_roformer_ep_317_sdr_12.9755.ckpt` and `htdemucs_ft.yaml` and the exit code is 0
- [ ] AC-2: No model library
  - Given a fresh interpreter
  - When the user runs `stems models`
  - Then `audio_separator` stays out of `sys.modules`

## Dependencies
- Step 7 extends this list.
