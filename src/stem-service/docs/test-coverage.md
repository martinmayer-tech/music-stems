# stem-service: test coverage

| Test | Covers |
|------|--------|
| `tests/test_smoke.py` | The `stem_service` package imports and holds a version |
| `tests/test_jobs.py` | REQ-001 add, get, list, claim, finish, and the data folder setting. REQ-002 persistence and `recover()`. REQ-004 import loads no model library |
| `tests/test_api_upload.py` | REQ-001 accepted extensions, rejected extensions, the size limit, name cleaning, and waking the workers |
| `tests/test_api_read.py` | REQ-002 job and list routes with no server path. REQ-003 stem download, refused names, a missing file, and an unfinished job |
| `tests/test_api_service.py` | REQ-004 default host and port, the first-run folders, the entry point, no login, worker shutdown, and a job from upload to download |
| `tests/test_worker.py` | REQ-002 requeue on start. REQ-003 turn-taking, failure handling, idle wake-up, and one worker for each device. REQ-004 model reuse and per-job output folders |
| `tests/test_api_options.py` | REQ-003 stored options, empty values, and a 422 that leaves no job and no file |
| `tests/test_worker_options.py` | REQ-003 the pass-through to `split()`, a six-stem job, a failed job before any model loads, and the pool key |

| `tests/test_docker_image.py` | REQ-001 the base image, FFmpeg, the extra argument, the pin, the runtime settings, the compiler layer, and the `.dockerignore` entries |
| `tests/test_compose.py` | REQ-002 the loopback port, both volumes, the build argument, and the GPU override |
| `tests/test_ci_docker.py` | REQ-003 the CI job builds the CPU image and pushes and runs nothing |
| `tests/test_docker_docs.py` | The purpose doc, the decisions index, and the manifest name the Docker files |

`src/stem-web/tests/test_page_serve.py` covers the `/` route and the `/static` mount.

Unit tests inject a fake separator or a fake `split` function. No test loads a real model.

The image build itself runs in CI and in a local `docker build`. No unit test builds an image.
