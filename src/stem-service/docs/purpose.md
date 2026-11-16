# stem-service: purpose

stem-service holds the job store, the worker, and the HTTP API. Step 4 adds the job store and the worker. Step 5 adds the HTTP API.

The component owns the SQLite table `jobs`. A caller adds a job, and a worker runs it through `split()` from stem-core. The worker loads each model once and runs one job at a time.

The web page calls this component over HTTP in later steps. This component calls stem-core to separate audio.
