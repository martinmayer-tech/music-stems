---
title: "Risk Register - Add the two-pass separation core"
summary: "Technical and operational risks with their mitigations."
status: "active"
version: "0.1.0"
---
# Risk Register - Add the two-pass separation core

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000004-separation-core
**Version:** 0.2.0
**Overall Risk Level:** medium

## Risks

| ID | Category | Description | Likelihood | Impact | Mitigation | Status |
|----|----------|------------|------------|--------|-----------|--------|
| R-001 | technical | The pinned package fails to install in CI | low | medium | Pin the newest release and read the CI result before P3 ends | open |
| R-002 | technical | Pass 2 writes a vocals stem that overwrites the pass 1 vocals file | high | high | Name the pass 2 vocals stem differently and drop it. A test checks the pass 1 file | open |
| R-003 | technical | The real separator names its files in a way the fake does not | medium | low | The code resolves paths against the output folder. The slow test checks real output | open |
| R-004 | operational | The first call downloads large model files | high | low | Document `STEMS_MODEL_DIR` and the first-run delay | open |

## Assumptions Logged as Risks

| ID | Assumption | Impact if Wrong | Status |
|----|-----------|----------------|--------|
| A-001 | `audio-separator[cpu]==0.48.0` installs on Python 3.12 in CI | The CI job fails and the step adjusts the pin | open |
