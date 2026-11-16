# stem-web: dependencies

- Runtime: none. The page uses the browser and its own script, with no library and no build.
- Served by: stem-service, which imports `static_dir()` from `stem_web`.
- Development: `pytest` and `ruff`, from the `dev` extra in the root `pyproject.toml`. `httpx` gives the test client. `node` runs the `stemLinks` tests, and the tests skip when `node` is absent.
