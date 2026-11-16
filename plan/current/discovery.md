---
title: "Discovery - 0000014-model-ensemble-options"
summary: "Raw discovery-pass findings: what the orchestrator knew before coaching began."
---
# Discovery - 0000014-model-ensemble-options

## Header (all modes)

| Field | Value |
|-------|-------|
| Adoption mode detected | `standard-iterative` |
| Detection signal | `docs/about.md` at 0.6.0 and `src/` beside an archive. The chart is the source of truth |
| Git pre-flight | Branch `feat/0000014-model-ensemble-options`, cut by the driver from `initiative/0000001-stem-separation-service` |
| Skills inbox | empty |
| Track | full |

## Mode Findings

### Standard Iterative

- Current version (`docs/about.md`): `0.6.0`. Step 7 bumps minor to `0.7.0`. The merge queue writes it.
- Prior features (`plan/_archive/`): 0000002 to 0000012, one for each of steps 1 to 6.
- Constraining ADRs: `docs/adr/0001` to `0006`. ADR-0002 sets separator injection and the engine pin. ADR-0004 sets the pooled worker. ADR-0006 sets the plain page.
- Component map: `stem-core` holds `split()` and the `stems` command. `stem-service` holds the job store, the pooled worker, and the API. `stem-web` holds the page files.
- Repo instructions: `agent-permissions.md` and `grep-tests-before-moving-files.md`.
- Pending migrations: 0007 and 0009. No `Migration:` row in the chart, so the step records `Migration pending` and carries on.
- Backlog: entry 0000015 is the step's entry. Entry 0000017 belongs to step 8. Entries 0000018 to 0000021 are not for this step.
- Queue: no `plan/.initiative-queue/` folder exists, so no item names step 7.
- Schema: the chart lists no change for step 7. The `jobs.options` column already exists and holds a JSON object.
- Dependencies: the chart lists none for step 7.
- Engine facts, read from the `audio-separator` 0.48.0 wheel: `Separator` takes `ensemble_preset` and `output_single_stem`. With a preset, `load_model` swaps the default pass 1 model for the preset's models. The wheel lists nine presets in `ensemble_presets.json`.
- Existing seams: `split()` takes a separator factory with three arguments. The worker's `ModelPool` keys separators by model file name. The store writes `jobs.options` and no code reads it.
- Local toolchain: Python 3.13 with a virtual environment outside the repo. Node runs the pack scripts.
- Baseline: the pack suite runs in a clean clone. Its output goes to `plan/current/baseline-failures.md`.
