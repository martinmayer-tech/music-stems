---
title: "Scope - Add the command-line interface"
summary: "Defines explicit boundaries of what is in scope and out of scope."
status: "active"
version: "0.1.0"
---
# Scope - Add the command-line interface

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000006-command-line-interface
**Version:** 0.3.0

## In Scope

- `stem_core/cli.py` with `main()` and the subcommands `split`, `env`, and `models`.
- `stem_core/__main__.py` for `python -m stem_core`.
- A `stems` console script and the packaging that installs `stem_core`.
- Unit tests with a fake separator and injected probes.
- Component docs and the architecture docs that the code changes.

## Out of Scope

- Model choice by the caller and ensembles.
- Pick a model per call: gap: out of scope.
- The queue, the API, the web page, and Docker.

## Deferred

- Model choice and ensembles wait for step 7. They also extend `stems models`.
