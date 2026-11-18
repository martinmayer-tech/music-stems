---
title: "ADR 0002: Separator injection, lazy import, and a pinned extra"
summary: "split() builds its separator through an injectable factory, imports audio_separator late, and installs the library from a pinned optional extra."
status: "accepted"
component: "stem-core"
version: "0.2.0"
---
# ADR-0002 - Separator injection, lazy import, and a pinned extra

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000004-separation-core
**Component:** stem-core
**File:** `docs/adr/0002-separator-injection-and-pin.md`
**Date:** 2026-11-15

## Context

`audio-separator` pulls in large machine learning libraries and downloads model files. Local Python 3.13 may not install it. Unit tests must run fast and without a model. Later steps import `stem_core` in the CLI, the worker, and the API, so a plain import must stay cheap.

## Decision

`split()` takes an optional `separator_factory` argument. When the caller passes none, the function imports `audio_separator.separator` at the first call and builds `Separator`. Unit tests pass a fake factory. The root `pyproject.toml` lists `audio-separator[cpu]==0.48.0` in a `separation` extra. The `python` CI job installs the `dev` and `separation` extras. One real-model test carries the `slow` marker and stays out of CI.

## Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|-------------|
| Hard dependency in the `project` table | One install command | Every install pulls the model libraries, including the dev setup on Python 3.13 | The chart tells the step to run unit tests without the package |
| Patch `Separator` with a mock library | No new argument | Tests couple to import paths | An argument is explicit and needs no patching |
| A range pin such as `>=0.48` | Gets fixes | The guide warns that defaults changed between releases | The chart requires `==` |

## Affected Components

| Component | Impact |
|-----------|--------|
| stem-core | Gains `split()` and a factory argument |
| stem-service | Calls `split()` in step 4 and installs the extra |

## Consequences

**Positive:**
- Unit tests run in seconds with no model.
- A plain `import stem_core` loads no machine learning library.

**Negative:**
- The real install path gets a check only in CI and in the `slow` test.
- Callers who want the CPU build must install the extra.

**Risks:**
- A fake separator may drift from the real one. The `slow` test covers the real output.

## Related ADRs

- ADR-0001 sets the tooling and layout.

## Supersedes

- None.

## Superseded By

- None.
