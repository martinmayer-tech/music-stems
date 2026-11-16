# Verification Report - 0000008-job-queue-worker

## What ran

- A virtual environment outside the repo held `pytest` and `ruff` on Python 3.13.
- A scratch script in `/tmp` queued three jobs on one `JobStore`. It claimed one job and left it `running` to mimic a crash. It then called `recover()` and ran one `Worker` with a fake separator that writes real files and records each load, start, and end.
- The real models did not run, because this step adds no model logic.

## Criteria

| Criterion | Method | Outcome | Observation |
|-----------|--------|---------|-------------|
| Two jobs queued together never overlap in run time | The scratch run with a 0.1 second fake separation | verified | Each job's start and end events appear before the next job's start event |
| The second job loads no model that the first already loaded | The scratch run with one plain job and one `full_stems` job | verified | Two loads in total: `model_bs_roformer_ep_317_sdr_12.9755.ckpt` and `htdemucs_ft.yaml`. The recovered plain job and the later plain job triggered no extra load |
| A job moves through `queued`, `running`, and `done`, or ends as `failed` | The scratch run and `test_req_003_a_failed_job_does_not_stop_the_worker` | verified | Three jobs ended `done` with 2, 5, and 2 outputs. The failure test shows `failed` with one error line |
| A job survives a restart of the store | The scratch run, `recover()`, and `test_req_002_jobs_persist_across_a_new_store` | verified | `recover()` returned 1 and the job ran to `done` on a second `JobStore` object |
| Importing the package loads no model library | `test_req_004_import_loads_no_model_library` | verified | A fresh interpreter reports `False` for `audio_separator` in `sys.modules` |

## Finding

None. A real `Separator` has not run under the pool. The `slow` test from step 2 stays the check for real models.
