# stem-service: risk and scope

Risk level: medium. The component serves an HTTP API with no login.

In scope: the job store, the worker, the model pool, restart recovery, and the HTTP API.
Out of scope: a login, cancel, delete, caller model choice, and a broker.
Deferred: the web page waits for step 6. Model choice and ensembles wait for step 7.

Risks:

- A restart during a job leaves it `running`. `recover()` requeues it.
- A real `Separator` may ignore a changed `output_dir`. The pool sets the attribute before each use, and a real run shows any gap.
- The pool holds each loaded model in memory until the worker stops.
- An operator who sets `STEMS_HOST` to a public address exposes an open upload route. The default is `127.0.0.1`.
- A crafted file name or stem name could reach a file outside the data folder. The upload route keeps the last part of a name, and the stem route serves only names in a job's outputs.
