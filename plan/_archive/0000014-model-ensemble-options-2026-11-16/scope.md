---
title: "Scope - Add model choice and ensemble options"
summary: "Defines explicit boundaries of what is in scope and out of scope."
status: "active"
version: "0.1.0"
---
# Scope - Add model choice and ensemble options

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000014-model-ensemble-options
**Version:** 0.7.0

## In Scope

- The allowlists, `validate_options()`, and the `split()` keyword arguments.
- The `stems split` flags and the longer `stems models` listing.
- The three form fields on `POST /jobs`, and the pass-through from the worker to `split()`.
- A model pool key that holds the model file and the preset.
- Three selects on the page and the `optionFields()` function.
- Tests, the OpenAPI spec for the new fields, the component docs, and the living docs.

## Out of Scope

- Pick the pass 1 model: gap: out of scope.
- Type a free model name: gap: out of scope.
- A route that lists the options: gap: out of scope.
- A schema change.

## Deferred

- Nothing deferred.
