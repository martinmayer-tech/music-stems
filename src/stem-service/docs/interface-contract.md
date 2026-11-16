# stem-service: interface contract

The `stem_service` package exposes `__version__`. Import the rest from its modules. Step 5 adds the HTTP routes.

## `stem_service.config`

| Name | Meaning |
|------|---------|
| `resolve_data_dir()` | Returns `STEMS_DATA_DIR`, or `./data` when the variable is unset or empty |
| `database_path(data_dir=None)` | Returns `{data_dir}/jobs.sqlite3` |
| `job_output_dir(job_id, data_dir=None)` | Returns `{data_dir}/jobs/{job_id}` |

## `stem_service.jobs`

`JobStore(path)` creates the folder, the file, and the `jobs` table when they do not exist. Every call commits before it returns.

| Method | Meaning |
|--------|---------|
| `add(input_path, full_stems=False, options=None)` | Inserts a `queued` job and returns its id |
| `get(job_id)` | Returns a `Job`, or `None` for an unknown id |
| `list()` | Returns every job in creation order |
| `claim_next()` | Moves the oldest `queued` job to `running` and returns it, or returns `None` |
| `mark_done(job_id, outputs)` | Sets `done` and stores the output paths |
| `mark_failed(job_id, error)` | Sets `failed` and stores the first line of the error |
| `recover()` | Returns every `running` job to `queued` and returns how many changed |

A `Job` is a frozen dataclass with `id`, `status`, `input_path`, `full_stems`, `options`, `outputs`, `error`, `created_at`, `started_at`, and `finished_at`. A job moves from `queued` to `running`, then to `done` or `failed`.

## `stem_service.worker`

| Name | Meaning |
|------|---------|
| `Worker(store, data_dir=None, separator_factory=None, split_func=split, name="default", poll_interval=0.5)` | One thread that claims jobs and runs them one at a time |
| `Worker.start(recover=True)` | Starts the thread. With `recover`, it first requeues interrupted jobs |
| `Worker.stop()` | Ends the thread after the current job |
| `Worker.wake()` | Tells an idle worker to look for a job now |
| `start_workers(store, devices, **options)` | Requeues interrupted jobs once, then starts one `Worker` for each device name |
| `ModelPool(base_factory=None)` | Builds one separator for each model and keeps it loaded |

The worker calls `split_func(input_path, out_dir, full_stems, pool.factory)`. The pool factory returns a `PooledSeparator` that loads each model on its first request only.

## Settings

| Variable | Default | Meaning |
|----------|---------|---------|
| `STEMS_DATA_DIR` | `./data` | The folder that holds `jobs.sqlite3` and the `jobs/` output folders |
| `STEMS_MODEL_DIR` | `./models` | The model folder that stem-core reads |
