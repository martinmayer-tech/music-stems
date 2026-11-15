---
title: "Risk Register - Add the command-line interface"
summary: "Technical and operational risks with their mitigations."
status: "active"
version: "0.1.0"
---
# Risk Register - Add the command-line interface

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000006-command-line-interface
**Version:** 0.3.0
**Overall Risk Level:** low

## Risks

| ID | Category | Description | Likelihood | Impact | Mitigation | Status |
|----|----------|------------|------------|--------|-----------|--------|
| R-001 | technical | Packaging `stem_core` changes the install and breaks the CI install step | low | medium | Read the CI result of `pip install ".[dev,separation]"` before P3 ends | open |
| R-002 | technical | `stems env` output differs per machine, so tests become flaky | medium | low | Tests inject the probes and never call the real tools | open |
| R-003 | technical | A plain import of `stem_core.cli` loads `audio_separator` and slows `env` and `models` | low | medium | A test checks `sys.modules` after `models` runs | open |

## Assumptions Logged as Risks

| ID | Assumption | Impact if Wrong | Status |
|----|-----------|----------------|--------|
| A-001 | `torch` may be absent in the test environment | None, because `env` reports `cpu` | open |
| A-002 | `ffmpeg` may be absent in the test environment | None, because `env` reports `not found` | open |
