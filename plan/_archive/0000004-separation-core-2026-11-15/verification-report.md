# Verification Report - 0000004-separation-core

## What ran

- A virtual environment outside the repo held `pytest`, `ruff`, and `audio-separator[cpu]==0.48.0` on Python 3.13, plus `audioread`.
- `STEMS_MODEL_DIR` pointed at an empty folder, so the run downloaded the real models.

## Criteria

| Criterion | Method | Outcome | Observation |
|-----------|--------|---------|-------------|
| `split(mix, out)` returns 2 existing WAV paths | `pytest -m slow` with the real model on a three-second tone | verified | 2 paths named `vocals.wav` and `instrumental.wav`, each with frames. The instrumental held sound |
| `split(mix, out, full_stems=True)` returns 5 | A direct call with the real models | verified | 5 absolute paths and 5 files in the folder. No `residual_vocals.wav` stayed |
| Every returned path is absolute | `test_req_001_split_returns_absolute_paths` and the real call | verified | All paths start at the output folder |
| `pyproject.toml` pins `audio-separator` with `==` | `test_req_003_separation_extra_pins_audio_separator_exactly` | verified | The extra reads `audio-separator[cpu]==0.48.0` |
| The CI install step names the extra | `test_req_003_ci_installs_the_separation_extra` | verified | The step runs `pip install ".[dev,separation]"`. The first CI run is the final check |
| The default `pytest` run skips the slow test | `pytest` | verified | 21 passed, 1 deselected |

## Finding

The real run showed that `audio-separator` lists the instrumental before the vocals. The code now sorts pass 1 stems by name. A test covers it.
