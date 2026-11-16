# stem-service: quirks

- `JobStore` opens one SQLite connection for each call. This keeps each thread on its own connection, and `claim_next()` uses `BEGIN IMMEDIATE` so two workers never claim one job.
- `start_workers` requeues interrupted jobs once and starts each worker with `recover=False`. A second worker that recovered on its own would requeue the job that the first worker runs.
- The pool sets `output_dir` on a reused separator. The fake separators in the tests accept it, and a real `audio-separator` `Separator` has not run under the pool yet.
- The `device` of a worker is a label. The worker passes no device to `audio-separator`, which picks its own.
- Tests that start a worker use a poll interval of 0.01 seconds and wait up to 10 seconds for a job.
