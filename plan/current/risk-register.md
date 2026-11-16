---
title: "Risk Register - Add model choice and ensemble options"
summary: "Technical, operational, and security risks with their mitigations."
status: "active"
version: "0.1.0"
---
# Risk Register - Add model choice and ensemble options

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000014-model-ensemble-options
**Version:** 0.7.0
**Overall Risk Level:** medium

## Risks

| ID | Category | Description | Likelihood | Impact | Mitigation | Status |
|----|----------|------------|------------|--------|-----------|--------|
| R-001 | security | A caller names a model that makes the engine fetch an unexpected file | low | high | Every entry point checks a fixed allowlist, and `split()` checks again before it loads a model. A test rejects other values | open |
| R-002 | technical | A single stem option deletes stems that the caller wanted | medium | low | The option names the stem to keep. The docs and the command help say so | open |
| R-003 | operational | The model pool holds one separator for each model and preset pair, so memory grows | medium | medium | The allowlists cap the pairs at 30. The docs name the cost | open |
| R-004 | technical | A preset changes the pass 1 stem names, so `split()` finds no vocals file | medium | medium | `split()` keeps its error that names the missing file. The job ends `failed` with that line | open |

## Assumptions Logged as Risks

| ID | Assumption | Impact if Wrong | Status |
|----|-----------|----------------|--------|
| A-001 | The preset names match `audio-separator` 0.48.0 | A preset fails inside the engine and the job ends `failed` | open |
| A-002 | An ensemble pass 1 still writes vocals and instrumental files | Pass 1 raises the error that names the missing file | open |
