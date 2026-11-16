# stem-service: test coverage

| Test | Covers |
|------|--------|
| `tests/test_smoke.py` | The `stem_service` package imports and holds a version |
| `tests/test_jobs.py` | REQ-001 add, get, list, claim, finish, and the data folder setting. REQ-002 persistence and `recover()`. REQ-004 import loads no model library |
| `tests/test_worker.py` | REQ-002 requeue on start. REQ-003 turn-taking, failure handling, idle wake-up, and one worker for each device. REQ-004 model reuse and per-job output folders |

Unit tests inject a fake separator. No test loads a real model.
