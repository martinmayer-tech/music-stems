---
title: "Requirement: REQ-001 - Options in split()"
summary: "split() takes a pass 2 model, an ensemble preset, and a single stem, and rejects any value outside the allowlists."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-001 - Options in split()

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000014-model-ensemble-options
**Source:** US-001
**Priority:** must-have

## User Story

As a developer, I pass model options to `split()`, so that a job uses the models I want.

## Functional Requirements
- `stem_core.separation` holds three allowlists: `PASS_TWO_MODELS` (`htdemucs_ft.yaml`, `htdemucs_6s.yaml`, `htdemucs.yaml`), `ENSEMBLE_PRESETS` (the nine preset names of `audio-separator` 0.48.0), and `SINGLE_STEMS` (`vocals`, `instrumental`, `drums`, `bass`, `other`, `guitar`, `piano`).
- `validate_options(model, ensemble_preset, single_stem)` raises `ValueError` for a value outside its allowlist. The message names the option, the bad value, and the allowed values. It also raises for `guitar` or `piano` when the model is not `htdemucs_6s.yaml`.
- `split()` takes the keyword arguments `model`, `ensemble_preset`, and `single_stem`, all `None` by default. It calls `validate_options()` before it builds a separator, so no model loads for a bad value.
- With `model` unset, pass 2 uses `htdemucs_ft.yaml`. With `htdemucs_6s.yaml`, pass 2 also keeps `guitar` and `piano`.
- With `ensemble_preset` set, pass 1 builds its separator with that preset. Pass 2 builds a separate separator with no preset.
- With `single_stem` set, `split()` runs only the passes that write that stem, deletes the other stem files, and returns the one path. A pass 2 stem implies pass 2.

## Acceptance Criteria
- [ ] AC-1: Pick the 6-stem model
  - Given a fake separator and `full_stems` set
  - When `split()` runs with `model` set to `htdemucs_6s.yaml`
  - Then the result holds `vocals`, `instrumental`, `drums`, `bass`, `other`, `guitar`, and `piano` paths
- [ ] AC-2: Reject an unlisted value
  - Given a fake separator that counts `load_model` calls
  - When `split()` runs with a model, preset, or stem outside the allowlists, or with `guitar` and a model that never writes it
  - Then it raises `ValueError` that names the value, and the fake never loads a model
- [ ] AC-3: Pass a preset and a single stem
  - Given a fake separator that records its factory calls
  - When `split()` runs with `ensemble_preset` and `single_stem` set
  - Then pass 1 gets the preset, pass 2 gets none, and the result holds only the named stem

## Dependencies
- None.
