---
title: "Scope - Add the two-pass separation core"
summary: "Defines explicit boundaries of what is in scope and out of scope."
status: "active"
version: "0.1.0"
---
# Scope - Add the two-pass separation core

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000004-separation-core
**Version:** 0.2.0

## In Scope

- `split()` in `stem_core/separation.py`, exported from `stem_core`.
- Pass 1 and the optional pass 2, with WAV output and absolute paths.
- The `STEMS_MODEL_DIR` setting.
- The pinned `separation` extra and the CI install.
- One `slow` smoke test with a real model.
- Component docs and the architecture docs that the code changes.

## Out of Scope

- The `stems` command, the queue, the API, the web page, and Docker.
- Model choice by the caller and ensembles.
- Pick a model per call: gap: out of scope.

## Deferred

- Model choice and ensembles wait for step 7.
- The `stems` command waits for step 3.
