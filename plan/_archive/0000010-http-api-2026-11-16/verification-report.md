# Verification Report - 0000010-http-api

## What ran

- A virtual environment outside the repo held `pytest`, `ruff`, `fastapi`, `uvicorn`, `python-multipart`, and `httpx` on Python 3.13.
- `python -m stem_service` started on port 8765 with a scratch data folder. A request to `GET /jobs` returned status 200 and `[]`. The process then stopped cleanly.
- A scratch script in `/tmp` ran the app under a real uvicorn server on `127.0.0.1:8771`. The worker used a fake `split` function that writes real files. The script sent each request over a socket with `urllib`.
- The real models did not run, because this step adds no model logic.

## Criteria

| Criterion | Method | Outcome | Observation |
|-----------|--------|---------|-------------|
| An upload returns a job id, and the job reaches `done` | A multipart `POST /jobs` against the live server, then `GET /jobs/{id}` until the status changed | verified | The upload returned 201. The job reached `done` with 5 stems for a `full_stems` upload |
| Each stem of a `done` job downloads as a WAV file | `GET /jobs/{id}/stems/{name}` for each listed name | verified | Each of the 5 requests returned 200 with the type `audio/wav` and a body that starts with `RIFF` |
| An unlisted extension, an oversized upload, an unknown job, and an unknown stem each get a 4xx answer | A `.txt` upload, a 2000-byte upload against a 1000-byte limit, `GET /jobs/zzz`, and `GET /jobs/{id}/stems/nope.wav` | verified | The answers were 415, 413, 404, and 404 |
| The default host is `127.0.0.1` | `python -m stem_service` with no `STEMS_HOST`, and `test_req_004_the_default_address_is_the_loopback_address` | verified | uvicorn logged `Uvicorn running on http://127.0.0.1:8765` |

## Finding

None. A real `Separator` has not run under the API. The `slow` test from step 2 stays the check for real models.
