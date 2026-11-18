# stem-core: dependencies

- Runtime: `audio-separator[cpu]==0.48.0`, from the `separation` extra in the root `pyproject.toml`. The package loads it on the first `split()` call, so `import stem_core` needs no model library.
- Development: `pytest` and `ruff`, from the `dev` extra.
- Install both extras with `pip install ".[dev,separation]"`.
- FFmpeg must be on the path for real separation. The unit tests need no FFmpeg.
