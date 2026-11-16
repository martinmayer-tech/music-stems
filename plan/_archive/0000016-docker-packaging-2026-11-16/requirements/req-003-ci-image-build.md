---
title: "Requirement: REQ-003 - CI image build"
summary: "A workflow job builds the CPU image on every pull request and runs no separation in it."
status: "active"
version: "0.1.0"
---
# Requirement: REQ-003 - CI image build

**Skill:** [plan](../../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000016-docker-packaging
**Source:** US-003
**Priority:** must-have

## User Story

As a maintainer, I want CI to build the CPU image, so that a broken Dockerfile fails a pull request.

## Functional Requirements
- `.github/workflows/ravintio.yml` gains a `docker` job that runs on a pull request that is open, reopened, or updated.
- The job holds `contents: read` only, checks out with `persist-credentials: false`, and runs `docker build` with `STEMS_EXTRA=cpu`.
- The job pushes no image and runs no container.

## Acceptance Criteria
- [ ] AC-1: Build the CPU image
  - Given the workflow text
  - When a test reads the `docker` job
  - Then it runs `docker build` with `STEMS_EXTRA=cpu`
- [ ] AC-2: Push nothing
  - Given the workflow text
  - When a test reads the `docker` job
  - Then it holds no `docker push`, no `docker run`, and no `packages: write`

## Dependencies
- REQ-001 holds the image.
