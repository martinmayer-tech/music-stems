# stem-core: dependencies

- Runtime: `audio-separator[cpu]==0.48.0` and `audioread==3.1.0`, from the `separation` extra in the root `pyproject.toml`. The engine imports `audioread` and does not install it, so the extra pins it (ADR-0009). The package loads it on the first `split()` call, so `import stem_core` needs no model library.
- Development: `pytest` and `ruff`, from the `dev` extra.
- Install both extras with `pip install ".[dev,separation]"`.
- FFmpeg must be on the path for real separation. The unit tests need no FFmpeg.
