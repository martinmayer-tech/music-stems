# Verification Report - 0000006-command-line-interface

## What ran

- A virtual environment outside the repo held `pytest` on Python 3.13. A second install of the built package, with no dependencies, provided the real `stems` console script.
- A scratch script in `/tmp` ran `main()` with a fake separator that writes real files. The real models did not run, because the command adds no model logic.

## Criteria

| Criterion | Method | Outcome | Observation |
|-----------|--------|---------|-------------|
| `stems split mix.wav --output-dir out` exits 0 and prints one path per line | The fake-separator run | verified | Exit 0. Two absolute paths, one per line |
| `stems split` with a missing input file exits non-zero with one error line | The installed `stems` script on a missing file | verified | Exit 1. One line, `stems: error: mix file not found: ...`. No path on standard output |
| `--full-stems` prints five paths | The fake-separator run with the flag | verified | Five paths: vocals, instrumental, drums, bass, other |
| `stems env` reports the Python version, FFmpeg, and the device | The installed script | verified | Three lines: `python`, `ffmpeg` with the real first line, and `device: cpu` |
| `stems models` lists the supported models | The installed script | verified | Two lines that name `model_bs_roformer_ep_317_sdr_12.9755.ckpt` and `htdemucs_ft.yaml` |
| `env` and `models` import no model library | `test_req_004_env_and_models_import_no_model_library` | verified | A fresh interpreter reports `False` for `audio_separator` in `sys.modules` |
| The package installs with a `stems` script | `pip install --no-deps` of a scratch copy | verified | The script runs. The CI install of the extras on Python 3.12 is the final check |

## Finding

None. The real-model path stays covered by the `slow` test from step 2.
