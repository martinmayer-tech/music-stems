---
title: "Discovery - 0000008-job-queue-worker"
summary: "Raw discovery-pass findings: what the orchestrator knew before coaching began."
---
# Discovery - 0000008-job-queue-worker

## Header (all modes)

| Field | Value |
|-------|-------|
| Adoption mode detected | `standard-iterative` |
| Detection signal | `docs/about.md` at 0.3.0 and `src/` beside an archive. The chart is the source of truth |
| Git pre-flight | Branch `feat/0000008-job-queue-worker`, cut by the driver from `initiative/0000001-stem-separation-service` |
| Skills inbox | empty |
| Track | full |

## Mode Findings

### Standard Iterative

- Current version (`docs/about.md`): `0.3.0`. Step 4 bumps minor to `0.4.0`. The merge queue writes it.
- Prior features (`plan/_archive/`): 0000002-python-scaffold, 0000004-separation-core, and 0000006-command-line-interface (2026-11-15).
- Constraining ADRs: `docs/adr/0001-python-tooling.md`, `0002-separator-injection-and-pin.md`, and `0003-stems-command-and-packaging.md`.
- Component map: `stem-core` holds `split()` and `stems`. `stem-service` holds a package skeleton and one smoke test. It owns no data yet.
- Repo instructions: `agent-permissions.md` and `grep-tests-before-moving-files.md`.
- Pending migrations: 0007 and 0009. No `Migration:` row in the chart, so the step records `Migration pending` and carries on.
- Backlog: entry 0000009 is the step's entry. Entry 0000018 is not for this step.
- Queue: `plan/.initiative-queue/` holds no item that names step 4.
- Schema: the chart approves one additive row for step 4, the SQLite table `jobs`. `stem-service` becomes the owner of that data.
- Toolchain: `pytest`, `ruff`, and a `python` CI job exist. `sqlite3` and `threading` come from the standard library, so the step adds no dependency.
- Existing API: `split(mix_path, out_dir, full_stems, separator_factory)` returns absolute path strings. `resolve_model_dir()` reads `STEMS_MODEL_DIR`. The factory takes `(output_dir, output_format, model_file_dir)`. A separator exposes `load_model(model_filename=)` and `separate(path, names)`.
