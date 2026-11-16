# stem-service: purpose

stem-service holds the job store, the worker, and the HTTP API. Step 4 added the job store and the worker. Step 5 added the HTTP API.

The component owns the SQLite table `jobs`. A caller adds a job, and a worker runs it through `split()` from stem-core. The worker loads each model once and runs one job at a time.

The HTTP API takes an upload and three optional model options, queues a job, reports its status, and serves each stem as a WAV file. It binds to `127.0.0.1` by default and has no login.

The component also serves the web page of stem-web at `/`. The page calls this component over HTTP. This component calls stem-core to separate audio.

Run the service with `python -m stem_service`. It needs the `service` extra of the root `pyproject.toml`.
