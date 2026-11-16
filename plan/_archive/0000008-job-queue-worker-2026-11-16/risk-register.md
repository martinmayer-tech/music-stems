---
title: "Risk Register - Add the job queue and worker"
summary: "Technical and operational risks with their mitigations."
status: "active"
version: "0.1.0"
---
# Risk Register - Add the job queue and worker

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000008-job-queue-worker
**Version:** 0.4.0
**Overall Risk Level:** low

## Risks

| ID | Category | Description | Likelihood | Impact | Mitigation | Status |
|----|----------|------------|------------|--------|-----------|--------|
| R-001 | operational | A restart during a job leaves it `running` for good | medium | medium | `recover()` returns it to `queued` when the worker starts. A test covers it | open |
| R-002 | technical | Two workers claim the same job | low | high | `claim_next()` runs one `BEGIN IMMEDIATE` transaction and updates the row once | open |
| R-003 | technical | The model cache holds memory for every model it loaded | medium | low | The cache holds at most the two models from `stem-core` for each worker | open |
| R-004 | technical | A real `Separator` ignores a changed `output_dir`, so a job writes to the wrong folder | medium | medium | The pool sets `output_dir` before each use. The first real run in step 5 or 8 shows any gap | open |

## Assumptions Logged as Risks

| ID | Assumption | Impact if Wrong | Status |
|----|-----------|----------------|--------|
| A-001 | A real `Separator` accepts a changed `output_dir` between runs | A model reloads for each job | open |
| A-002 | SQLite in the standard library supports `BEGIN IMMEDIATE` on every CI Python | The claim test fails in CI | open |
