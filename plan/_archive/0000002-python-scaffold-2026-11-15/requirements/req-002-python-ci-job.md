---
title: "Requirement: REQ-002 - Python CI job"
summary: "A workflow job that lints and tests Python code on pull requests."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-002 - Python CI job

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000002-python-scaffold
**Source:** US-002
**Priority:** must-have

## User Story

As a maintainer, I see a red check when a pull request fails a test. I see a green check when it passes, so that I trust each merge.

## Functional Requirements
- A job named `python` in `.github/workflows/ravintio.yml` runs on pull requests to `main` and `initiative/**`.
- The job uses Python 3.12, installs the dev extra, runs `ruff check .`, and then runs `pytest`.
- The job reads the repo and writes nothing.
- The job skips the `closed` pull request action.

## Acceptance Criteria
- [ ] AC-1: Red on failure
  - Given a pull request with a failing unit test
  - When the `python` job runs
  - Then the job exits non-zero and the check is red
- [ ] AC-2: Green on success
  - Given a pull request with passing tests and clean lint
  - When the `python` job runs
  - Then the job exits 0 and the check is green

## Dependencies
- REQ-001 supplies the tools and tests that the job runs.
