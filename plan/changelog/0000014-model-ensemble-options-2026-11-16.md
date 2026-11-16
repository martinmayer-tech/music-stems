# Changelog (0000014-model-ensemble-options, 16 Nov 2026)

**Feature:** Add model choice and ensemble options
**Version:** set by the merge queue at merge
**PR:** 11

## What changed

- `stem-core` gains three allowlists, `PASS_TWO_MODELS`, `ENSEMBLE_PRESETS`, and `SINGLE_STEMS`, and `validate_options()`.
- `split()` takes the keyword arguments `model`, `ensemble_preset`, and `single_stem`. It validates them before any model loads.
- With `htdemucs_6s.yaml`, pass 2 also writes guitar and piano stems.
- A preset goes to pass 1 only. Pass 2 builds its own separator without it.
- `stems split` takes `--model`, `--ensemble-preset`, and `--single-stem`. `stems models` lists the allowed values.
- `POST /jobs` takes the optional fields `model`, `ensemble_preset`, and `single_stem`. A bad value gets status 422. The route stores the set options in `jobs.options`, and the worker passes them to `split()`.
- The model pool keys each separator by model file and preset.
- The page gains three selects with a `Default` option.
- Added ADR 0007, the OpenAPI spec for the new fields, and updated the component docs and the living docs.

## Why

Every job used the two default models. Sections 8 and 9 of the guide list other models and ensembles that trade speed for quality. A caller now picks them from a fixed allowlist.

## Deviations

- The existing `stems models` test counted exactly two lines. The agent changed it to check the first two lines, so the new listing lines can follow.
- The P0 baseline record waited for the clean-clone run to end, so the agent recorded it in P2.

## Validation results

- `ruff check .` exits 0. `pytest` gives 156 passed and 1 deselected. The full pack suite gives 0 new failures and 61 inherited failures.
- A live service accepted a job with `htdemucs_6s.yaml` and full stems. The job listed guitar and piano stems. A job with an unlisted model got 422 and loaded no model.
- A browser upload with `htdemucs_6s.yaml` showed 7 players and 7 download links.
- `pip-audit` reports no known vulnerabilities.
- No real model ran. Fake separators cover every preset and stem name.

## Skipped phases

None.
