# stem-service: quirks

- `JobStore` opens one SQLite connection for each call. This keeps each thread on its own connection, and `claim_next()` uses `BEGIN IMMEDIATE` so two workers never claim one job.
- `start_workers` requeues interrupted jobs once and starts each worker with `recover=False`. A second worker that recovered on its own would requeue the job that the first worker runs.
- The pool sets `output_dir` on a reused separator. The fake separators in the tests accept it, and a real `audio-separator` `Separator` has not run under the pool yet.
- The `device` of a worker is a label. The worker passes no device to `audio-separator`, which picks its own.
- `create_app()` builds the store and the `uploads` folder when it runs. It starts the worker when the app starts, and it stops the worker at shutdown. A test that skips the worker passes `run_workers=False`.
- The upload route checks the size twice. It rejects a known size before the copy, and it counts bytes during the copy. FastAPI has already buffered the body by then, so the limit protects the data folder and not the memory.
- A plain `..` in a URL never reaches the stem route, because HTTP clients collapse it. The route still looks every name up in the job's outputs.
- `create_app()` imports `stem_web` for the page folder. Run the service with `src/stem-web` on the Python path, as `pyproject.toml` sets for the tests.
- Tests that start a worker use a poll interval of 0.01 seconds and wait up to 10 seconds for a job.
