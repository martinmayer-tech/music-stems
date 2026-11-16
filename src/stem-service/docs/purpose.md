# stem-service: purpose

stem-service holds the job store, the worker, and the HTTP API. Step 4 added the job store and the worker. Step 5 added the HTTP API.

The component owns the SQLite table `jobs`. A caller adds a job, and a worker runs it through `split()` from stem-core. The worker loads each model once and runs one job at a time.

The HTTP API takes an upload and three optional model options, queues a job, reports its status, and serves each stem as a WAV file. It binds to `127.0.0.1` by default and has no login.

The component also serves the web page of stem-web at `/`. The page calls this component over HTTP. This component calls stem-core to separate audio.

Run the service with `python -m stem_service`. It needs the `service` extra of the root `pyproject.toml`.

## Run it in Docker

The `Dockerfile` and `compose.yaml` at the repo root package the service. Run `docker compose up --build` and open `http://127.0.0.1:8000`.

- The image starts from `python:3.12-slim` and installs FFmpeg. It runs as the non-root user `stems`.
- The compose file mounts the named volume `models` at `/models` and the named volume `data` at `/data`. A restart keeps the models and the finished jobs. `docker compose down -v` removes both volumes.
- The compose file publishes the port on `127.0.0.1` only. The service has no login, so keep that prefix.
- The build argument `STEMS_EXTRA` selects the `audio-separator` extra. It defaults to `cpu`. Run `docker compose -f compose.yaml -f compose.gpu.yaml up --build` for the GPU extra. The host needs the NVIDIA container toolkit.
- The image is large because the engine pulls PyTorch. The first job downloads each model once.
- A job fails in the image until `audioread` joins the dependencies. Backlog entry 0000023 tracks it.
- CI builds the CPU image on every pull request. The project publishes no image.
