---
title: "Requirement: REQ-003 - Product version record"
summary: "The product manifest lists the three components, and each has a manifest and docs."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-003 - Product version record

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000002-python-scaffold
**Source:** US-003
**Priority:** must-have

## User Story

As a maintainer, I read the product version from `docs/about.md` and `product.yml`, so that the merge queue can set it.

## Functional Requirements
- `product.yml` lists `stem-core`, `stem-service`, and `stem-web` under `components`, each with its `component.yml` path.
- Each component folder holds a `component.yml` and a `docs/` folder with a README.
- Step 1 leaves `version` at `0.0.0` in `docs/about.md` and `product.yml`. The merge queue sets `0.1.0` at merge.
- The two version files hold the same version at all times.

## Acceptance Criteria
- [ ] AC-1: Components listed
  - Given the repo after this step
  - When the maintainer opens `product.yml`
  - Then it lists three components and each path exists
- [ ] AC-2: Versions match
  - Given the repo after this step
  - When `node ravintio-zero/scripts/merge-queue.mjs versions` runs
  - Then it exits 0

## Dependencies
- REQ-001 creates the component folders.
