# stem-service: dependencies

- Runtime: Python standard library (`sqlite3`, `threading`) and the `stem_core` package from this repo.
- HTTP API: `fastapi`, `uvicorn`, and `python-multipart`, from the `service` extra in the root `pyproject.toml`.
- Development: `pytest`, `ruff`, and `httpx` (the test client), from the `dev` extra in the root `pyproject.toml`.
- `audio-separator` comes in through stem-core and loads on the first real job only.
