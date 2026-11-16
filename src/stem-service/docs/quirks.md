# stem-service: quirks

- `JobStore` opens one SQLite connection for each call. This keeps each thread on its own connection, and `claim_next()` uses `BEGIN IMMEDIATE` so two workers never claim one job.
- `start_workers` requeues interrupted jobs once and starts each worker with `recover=False`. A second worker that recovered on its own would requeue the job that the first worker runs.
- The pool sets `output_dir` on a reused separator. The fake separators in the tests accept it, and a real `audio-separator` `Separator` has not run under the pool yet.
- The `device` of a worker is a label. The worker passes no device to `audio-separator`, which picks its own.
- `create_app()` builds the store and the `uploads` folder when it runs. It starts the worker when the app starts, and it stops the worker at shutdown. A test that skips the worker passes `run_workers=False`.
- The upload route checks the size twice. It rejects a known size before the copy, and it counts bytes during the copy. FastAPI has already buffered the body by then, so the limit protects the data folder and not the memory.
- A plain `..` in a URL never reaches the stem route, because HTTP clients collapse it. The route still looks every name up in the job's outputs.
- `create_app()` imports `stem_web` for the page folder. Run the service with `src/stem-web` on the Python path, as `pyproject.toml` sets for the tests.
- The upload route validates the options before it writes the file. `split()` validates them again, so a job that holds a bad option still fails before any model loads.
- The model pool keys a separator by model file and preset. A preset separator is separate from a plain one.
- Tests that start a worker use a poll interval of 0.01 seconds and wait up to 10 seconds for a job.
- The image sets `STEMS_HOST=0.0.0.0`. The default outside Docker stays `127.0.0.1`. Docker forwards a published port to the container address, so a loopback bind inside the container would never answer.
- The root `pyproject.toml` installs `stem_core` only. The image sets `PYTHONPATH` to the three `src` folders so `python -m stem_service` finds the others.
- `diffq`, a dependency of `audio-separator`, builds from source. The image installs `gcc` in the layer that runs `pip install` and removes it in the same layer.
- The `AUDIO_SEPARATOR_VERSION` build argument repeats the `pyproject.toml` pin.
