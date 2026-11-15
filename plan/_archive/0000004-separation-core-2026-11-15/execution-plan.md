# Execution Plan - Add the two-pass separation core

> Every requirement traces to a user story in the confirmed design.

**Skill:** [plan](../../ravintio-zero/skills/ravintio-plan/SKILL.md)
**Feature:** 0000004-separation-core
**Version:** 0.2.0
**Status:** active

## Active Skills

| Skill | Scope | Purpose |
|-------|-------|---------|
| ravintio-implement | plan | Builds each unit with tests and docs |

## Functional Requirements Directory

Functional requirements are split into individual files, one user story per file, at `plan/current/requirements/`.

| File | Requirement |
|------|------------|
| [req-001-two-pass-split.md](requirements/req-001-two-pass-split.md) | `split()` returns the vocals and instrumental paths |
| [req-002-full-stems.md](requirements/req-002-full-stems.md) | `full_stems=True` adds drums, bass, and other |
| [req-003-pinned-dependency.md](requirements/req-003-pinned-dependency.md) | One pinned `separation` extra, installed by CI |

## Non-Functional Requirements

| ID | Category | Requirement | Target | Measurement |
|----|----------|------------|--------|-------------|
| NFR-001 | Repeatability | One exact `audio-separator` version | `==` pin in `pyproject.toml` | A test reads the extra |
| NFR-002 | Speed of tests | Unit tests need no model | Zero model downloads in CI | The `slow` marker excludes the real test |

## API Summary

None. The step builds a Python function and no endpoint.

## Data Model Summary

None. The step owns no data.

## Component Interactions

```mermaid
flowchart LR
    A[Caller] -->|split| B[stem_core.separation]
    B -->|Separator| C[audio-separator]
    C -->|downloads| D[STEMS_MODEL_DIR]
```

## Test impact

| Cause | Test | Unit |
|-------|------|------|
| Workflow job or step edit | `ravintio-zero/tests/test-0000327-req-002-ci-job.sh`, `test-0000317-req-001-003-004-rules-ignores-checks.sh`, `test-0000390-req-003-enforcement-points.sh`, and `src/stem-core/tests/test_ci_job.py` | U2-pin-ci |
| Backlog entry id | `ravintio-zero/tests/test-0000005-pack-governance.sh` and three more name `0000005` for pack reasons that do not touch this entry | U1-core |
| New test file | `test-0000042-req-008-pack-prose.sh`, `test-0000164-req-008-no-process-substitution-loops.sh` | U1-core |
| New tracked file | `test-0000042-req-010-pack-wording-allowlist.sh` | U4-docs |
| Skill count, skill-text budget, size cap, reference file edit, non-suite file, fixture-pinned line | none found | none |

## Branch-point reads

| File | Commit read | Unit |
|------|-------------|------|
| `pyproject.toml` | `a4aed6b` (local) | U2-pin-ci |
| `.github/workflows/ravintio.yml` | `a4aed6b` (local) | U2-pin-ci |
| `src/stem-core/stem_core/__init__.py` | `a4aed6b` (local) | U1-core |
| `src/stem-core/stem_core/separation.py` | new | U1-core |
| `src/stem-core/tests/test_separation.py` | new | U1-core |
| `src/stem-core/tests/test_pin_ci.py` | new | U2-pin-ci |
| `src/stem-core/tests/test_real_model.py` | new | U3-smoke |
| `src/stem-core/component.yml` | `a4aed6b` (local) | U4-docs |
| `src/stem-core/docs/` (six files) | `a4aed6b` (local) | U4-docs |
| `docs/component-registry.md`, `docs/dependency-graph.md`, `docs/architecture-overview.md`, `docs/decisions-index.md` | `a4aed6b` (local) | U4-docs |

## Concurrency plan

| Unit | Depends on | Writes | Batch | Sequential reason | Shared resources |
|------|-----------|--------|-------|-------------------|------------------|
| U1-core | none | `src/stem-core/stem_core/separation.py`, `src/stem-core/stem_core/__init__.py`, `src/stem-core/tests/test_separation.py` | 1 | none | none |
| U2-pin-ci | none | `pyproject.toml`, `.github/workflows/ravintio.yml`, `src/stem-core/tests/test_pin_ci.py` | 1 | none | none |
| U3-smoke | U1-core | `src/stem-core/tests/test_real_model.py` | 2 | Calls the function that U1-core writes | none |
| U4-docs | U1-core, U2-pin-ci, U3-smoke | `src/stem-core/component.yml`, the `docs/` set of `stem-core`, `docs/component-registry.md`, `docs/dependency-graph.md`, `docs/architecture-overview.md`, `docs/decisions-index.md` | 3 | Describes the finished code | none |

## Assumptions

| ID | Assumption | Impact if Wrong |
|----|-----------|----------------|
| A-001 | `audio-separator[cpu]==0.48.0` installs on Python 3.12 in CI | The job fails and the step adjusts the pin |

## Open Questions

None.
