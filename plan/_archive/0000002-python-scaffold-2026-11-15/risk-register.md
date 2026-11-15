---
title: "Risk Register - Scaffold the Python project and its CI"
summary: "Technical and operational risks with their mitigations."
status: "active"
version: "0.1.0"
---
# Risk Register - Scaffold the Python project and its CI

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000002-python-scaffold
**Version:** 0.1.0
**Overall Risk Level:** low

## Risks

| ID | Category | Description | Likelihood | Impact | Mitigation | Status |
|----|----------|------------|------------|--------|-----------|--------|
| R-001 | technical | The new `python` job breaks a pack test that counts workflow jobs | medium | medium | Grep the tests for `ravintio.yml` and run the full suite before P3 | open |
| R-002 | operational | `ruff` reads pack scripts or fixtures and fails on code that is not Python | low | medium | Set `extend-exclude` for `ravintio-zero` and `plan` in `pyproject.toml` | open |

## Assumptions Logged as Risks

| ID | Assumption | Impact if Wrong | Status |
|----|-----------|----------------|--------|
| A-001 | `pytest` and `ruff` install from PyPI in CI | The job fails and the step stops | open |
