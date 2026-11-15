---
title: "Requirement: REQ-001 - Two-pass split"
summary: "split() writes vocals and instrumental WAV files and returns their absolute paths."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-001 - Two-pass split

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000004-separation-core
**Source:** US-001
**Priority:** must-have

## User Story

As a developer, I call `split(mix, out)`, so that I get the vocals and instrumental WAV paths.

## Functional Requirements
- `stem_core.split(mix_path, out_dir, full_stems=False)` runs pass 1 with `model_bs_roformer_ep_317_sdr_12.9755.ckpt`.
- The function sets WAV output and names the stems `vocals` and `instrumental`.
- The function reads the model folder from `STEMS_MODEL_DIR` and defaults to `./models`.
- The function resolves each returned path against the output folder and returns absolute paths.
- The function imports `audio_separator` when it first runs. A caller may inject a separator factory.
- A missing mix file raises `FileNotFoundError` before any model loads.

## Acceptance Criteria
- [ ] AC-1: Two paths
  - Given a mix file and a fake separator that writes two stems
  - When the developer calls `split(mix, out)`
  - Then the call returns 2 existing paths that end in `.wav`
- [ ] AC-2: Absolute paths
  - Given a separator that returns relative file names
  - When the developer calls `split(mix, out)`
  - Then every returned path is absolute and sits in the output folder
- [ ] AC-3: Missing mix
  - Given a mix path that does not exist
  - When the developer calls `split`
  - Then the call raises `FileNotFoundError` and loads no model

## Dependencies
- None.
