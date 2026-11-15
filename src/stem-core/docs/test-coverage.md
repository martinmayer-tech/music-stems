# stem-core: test coverage

| Test | Covers |
|------|--------|
| `tests/test_smoke.py` | The `stem_core` package imports and holds a version |
| `tests/test_ci_job.py` | The `python` job in `.github/workflows/ravintio.yml` lints, tests, and uses Python 3.12 |
| `tests/test_separation.py` | `split()` with a fake separator: path count, absolute paths, models, WAV output, the model folder, a missing mix, and pass 2 |
| `tests/test_pin_ci.py` | The `==` pin of the `separation` extra, the CI install, and the `slow` marker |
| `tests/test_cli.py` | The `stems` command with a fake separator and injected probes: paths, exit codes, error lines, `--full-stems`, `env`, `models`, and the absence of `audio_separator` after `env` and `models` |
| `tests/test_entry_points.py` | The `stems` entry in `pyproject.toml`, the packaging, the pin, and `python -m stem_core` on a missing file |
| `tests/test_real_model.py` | One real-model run. It carries the `slow` marker and runs with `pytest -m slow` |
