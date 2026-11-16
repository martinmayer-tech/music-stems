---
title: "Discovery - 0000002-python-scaffold"
summary: "Raw discovery-pass findings: what the orchestrator knew before coaching began."
---
# Discovery - 0000002-python-scaffold

## Header (all modes)

| Field | Value |
|-------|-------|
| Adoption mode detected | `standard-iterative` |
| Detection signal | `docs/about.md` at 0.0.0 and `src/` present. Initiative step, so the chart is the source of truth |
| Git pre-flight | Branch `feat/0000002-python-scaffold`, cut by the driver from `initiative/0000001-stem-separation-service` |
| Skills inbox | empty |
| Track | full |

## Mode Findings

### Standard Iterative

- Current version (`docs/about.md`): `0.0.0`. Step 1 releases `0.1.0` (chart Decisions row).
- Prior features (`plan/_archive/`): none.
- Constraining ADRs: none for the application. Pack ADRs do not apply.
- Component / data-ownership map: none. `product.yml` lists `components: []`. `src/` holds only `README.md`.
- Repo instructions: `ravintio-overrides/instructions/` holds `agent-permissions.md` and `grep-tests-before-moving-files.md`.
- Pending migration: 0007. No `Migration:` row in the chart, so the step records `Migration pending: 0007` and carries on.
- Backlog: entry 0000003 (python scaffold) is the only entry the step uses.
- Toolchain: `ravintio.yml` runs the pack checks only. No Python job exists.
