---
title: "ADR 0007: Allowlisted model options in stem-core"
summary: "stem-core holds the allowlists and validates each option, and every entry point calls it before any model loads."
status: "proposed"
component: "stem-core"
version: "0.7.0"
---
# ADR-0007 - Allowlisted model options in stem-core

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000014-model-ensemble-options
**Component:** stem-core
**File:** `docs/adr/0007-allowlisted-model-options-in-stem-core.md`
**Date:** 2026-11-16

## Context

A caller wants to pick the pass 2 model, a pass 1 ensemble preset, and one stem. The choice crosses three components, because the command, the API, and the page all expose it. A free model name would let a caller make the engine fetch any file. The chart allows the four models of section 8 of the guide and the presets of `audio-separator`.

## Decision

`stem_core.separation` holds the allowlists as tuples and `validate_options()`. It raises `ValueError` with one clear line.

- The command, the API route, and `split()` each call `validate_options()`. The check in `split()` runs before any separator exists, so no model loads for a bad value.
- The API answers a bad value with 422 and stores the set options in `jobs.options`. The table keeps its columns.
- The worker passes the stored options to `split()`. The model pool keys each separator by model file and preset.
- The page lists the allowlist values as text. A test compares them with `stem_core`, so the two lists cannot drift.
- With a preset, `split()` builds a second separator without it for pass 2. The factory gets the keyword `ensemble_preset` only when the caller sets a preset, so a factory with three arguments still works.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| Accept any model name | Reaches every model | A caller can make the engine fetch any file | The chart says reject any model outside the allowlist |
| Check only at the API | One place | The command and the worker skip the check | A queued job would still load a bad model |
| A route that lists the options | The page never drifts | A new route and a new contract | A test already keeps the page and the library in line |

## Affected Components

| Component | Impact |
|-----------|--------|
| stem-core | Gains the allowlists, `validate_options()`, and the `split()` arguments |
| stem-service | Gains three form fields and the worker pass-through |
| stem-web | Gains three selects |

## Consequences

**Positive:**
- A bad option fails fast, before any model loads.
- One module owns the lists.

**Negative:**
- A new preset in a later engine version needs a code change.
- The page repeats the list as text.

**Risks:**
- The pool holds up to 30 separators, so memory grows with use.

## Related ADRs

- ADR-0002 sets separator injection.
- ADR-0004 sets the pooled worker that this decision extends.

## Supersedes

- None.

## Superseded By

- None.
