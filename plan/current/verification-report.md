---
title: "Verification Report - 0000014-model-ensemble-options"
summary: "What the agent ran and observed for each acceptance criterion."
---
# Verification Report - 0000014-model-ensemble-options

## Setup

The agent started `create_app()` under uvicorn on `127.0.0.1:8766`. The service used a fake separator that records each model load and writes small WAV files. The data folder started empty. The agent sent requests with `curl`, then used the page in a browser.

## Criteria

| Criterion | Method | Outcome | Evidence |
|-----------|--------|---------|----------|
| A job with `htdemucs_6s.yaml` and full stems returns guitar and piano stems | `curl` against the running service | verified | The job reached `done` with the stems `vocals`, `instrumental`, `drums`, `bass`, `other`, `guitar`, and `piano` |
| A job that names an unlisted model fails with a clear error before any model loads | `curl` and the load log | verified | Status 422 with the detail `unknown model 'evil.ckpt'. Allowed values: htdemucs_ft.yaml, htdemucs_6s.yaml, htdemucs.yaml`. The load log holds no entry for it |
| A stem that the model never writes is refused | `curl` | verified | `single_stem=guitar` with the default model gave 422 and the detail `single stem 'guitar' needs the model htdemucs_6s.yaml` |
| A preset and a single stem reach the engine | `curl` and the load log | verified | The job ended `done` with one stem, `vocals.wav`. The load log shows pass 1 built with `preset=vocal_balanced` |
| The page exposes the three options | Browser load and click-through | verified | The page held 3 selects. A browser upload with `htdemucs_6s.yaml` gave a job with 7 players and 7 download links |
| The page shows the error for a bad value | Browser click-through | verified | A forced `evil.ckpt` option wrote the 422 detail text to the status line |
| The command exposes the options | Unit test only | verified by test | `test_cli_options.py` runs `stems split` with an injected function and `stems models` in a fresh interpreter. No run used a real model |

## Notes

- The browser console showed the known 404 for `/favicon.ico` and one entry for the 422 answer. Neither points to a defect.
- No real model ran. The real preset names and stem names rest on the 0.48.0 wheel, as the risk register states.
