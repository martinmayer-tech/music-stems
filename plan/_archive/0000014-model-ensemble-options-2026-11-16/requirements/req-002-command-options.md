---
title: "Requirement: REQ-002 - Options in the command"
summary: "stems split takes --model, --ensemble-preset, and --single-stem, and stems models lists the allowed values."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-002 - Options in the command

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000014-model-ensemble-options
**Source:** US-002
**Priority:** must-have

## User Story

As a user, I pass the same options to `stems split`, so that I choose from the shell.

## Functional Requirements
- `stems split` takes `--model`, `--ensemble-preset`, and `--single-stem`. Each defaults to unset.
- The command passes only the options that the user set to `split()` as keyword arguments.
- A `ValueError` from `split()` prints one `stems: error:` line and exits 1, as any other failure does.
- `stems models` also lists the pass 2 models, the ensemble presets, and the single stems. It imports no model library.

## Acceptance Criteria
- [ ] AC-1: Pass the options through
  - Given an injected split function that records its call
  - When `stems split` runs with the three flags
  - Then the function receives `model`, `ensemble_preset`, and `single_stem` with those values
- [ ] AC-2: Pass nothing when unset
  - Given an injected split function that records its call
  - When `stems split` runs with no option flag
  - Then the function receives no option keyword argument
- [ ] AC-3: List the allowed values
  - Given a fresh interpreter
  - When `stems models` runs
  - Then the output lists every allowed model, preset, and stem, and exit code 0

## Dependencies
- REQ-001 holds the allowlists.
