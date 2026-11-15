# stem-core: quirks

- `tests/test_ci_job.py` and `tests/test_pin_ci.py` check the CI workflow and `pyproject.toml`, so `stem-core` holds tests about the repo. The root layout has no better home for them.
- `htdemucs_ft.yaml` also writes a vocals stem. Pass 2 names it `residual_vocals` so that it never overwrites the pass 1 `vocals.wav`. `split()` deletes that file and leaves it out of the result.
- `audio-separator` may report bare file names. `split()` resolves each name against the output folder.
- The default pytest run adds `-m 'not slow'`. Run the real-model test with `pytest -m slow`.
- The first real call downloads model files into `STEMS_MODEL_DIR`.
- The real-model test feeds a pure tone. The vocals stem of a tone is silent, so the test checks sound in the instrumental only.
- `audio-separator` 0.48.0 on local Python 3.13 also needs `audioread` in the virtual environment. CI on Python 3.12 needs no extra package.
- `stems env` imports `torch` inside `probe_device()` and falls back to `cpu` on any error. The package does not depend on `torch` directly.
- `pyproject.toml` packages `stem_core` from `src/stem-core` with `package-dir`. The pytest `pythonpath` setting does the same job for tests. Later steps add their own packages to `packages`.
- `tests/test_cli.py` runs one subprocess with only `PYTHONPATH` set, so the check sees a fresh interpreter.
- `audio-separator` reports pass 1 stems in its own order, so `split()` sorts them to `vocals.wav` then `instrumental.wav`.
