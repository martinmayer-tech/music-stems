# stem-service: dependencies

- Runtime: Python standard library (`sqlite3`, `threading`) and the `stem_core` package from this repo.
- Web page: `stem_web.static_dir()` from the stem-web component in this repo. The page files need no library.
- HTTP API: `fastapi`, `uvicorn`, and `python-multipart`, from the `service` extra in the root `pyproject.toml`.
- Development: `pytest`, `ruff`, and `httpx` (the test client), from the `dev` extra in the root `pyproject.toml`.
- `audio-separator` comes in through stem-core and loads on the first real job only.
- Image: `python:3.12-slim` and the Debian package `ffmpeg`. The `AUDIO_SEPARATOR_VERSION` build argument repeats the pin of the `separation` extra, and `tests/test_docker_image.py` keeps the two equal.
- Build only: the Debian package `gcc`, which the `pip install` layer adds and removes, because `diffq` has no wheel.
- GPU image: `audio-separator[gpu]`, which the build argument `STEMS_EXTRA=gpu` selects, and the NVIDIA container toolkit on the host.
