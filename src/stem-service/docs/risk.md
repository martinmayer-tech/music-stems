# stem-service: risk and scope

Risk level: low. The component runs no network surface yet.

In scope: the job store, the worker, the model pool, and restart recovery.
Out of scope: the HTTP API, uploads, cancel, caller model choice, and a broker.
Deferred: the HTTP API waits for step 5. Model choice and ensembles wait for step 7.

Risks:

- A restart during a job leaves it `running`. `recover()` requeues it.
- A real `Separator` may ignore a changed `output_dir`. The pool sets the attribute before each use, and a real run shows any gap.
- The pool holds each loaded model in memory until the worker stops.
