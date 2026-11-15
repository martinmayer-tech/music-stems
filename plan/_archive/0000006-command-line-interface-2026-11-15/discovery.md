---
title: "Discovery - 0000006-command-line-interface"
summary: "Raw discovery-pass findings: what the orchestrator knew before coaching began."
---
# Discovery - 0000006-command-line-interface

## Header (all modes)

| Field | Value |
|-------|-------|
| Adoption mode detected | `standard-iterative` |
| Detection signal | `docs/about.md` at 0.2.0 and `src/` beside an archive. The chart is the source of truth |
| Git pre-flight | Branch `feat/0000006-command-line-interface`, cut by the driver from `initiative/0000001-stem-separation-service` |
| Skills inbox | empty |
| Track | full |

## Mode Findings

### Standard Iterative

- Current version (`docs/about.md`): `0.2.0`. Step 3 bumps minor to `0.3.0`. The merge queue writes it.
- Prior features (`plan/_archive/`): 0000002-python-scaffold and 0000004-separation-core (2026-11-15).
- Constraining ADRs: `docs/adr/0001-python-tooling.md` and the ADR that step 2 added for the `split()` design.
- Component map: `stem-core` holds `split()` in `stem_core/separation.py`. It owns no data.
- Repo instructions: `agent-permissions.md` and `grep-tests-before-moving-files.md`.
- Pending migrations: 0007 and 0009. No `Migration:` row in the chart, so the step records `Migration pending` and carries on.
- Backlog: entry 0000007 is the step's entry. Entry 0000018 is not for this step.
- Queue: `plan/.initiative-queue/` holds no item that names step 3.
- Toolchain: `pytest`, `ruff`, and a `python` CI job exist. `argparse` comes from the standard library, so the step adds no dependency.
- Existing API: `split(mix_path, out_dir, full_stems, separator_factory)` returns absolute path strings. `resolve_model_dir()` reads `STEMS_MODEL_DIR`.
