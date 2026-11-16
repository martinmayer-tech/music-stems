# stem-web: test coverage

| Test | Covers |
|------|--------|
| `tests/test_smoke.py` | The `stem_web` package imports and holds a version |
| `tests/test_page_serve.py` | REQ-001 `static_dir()`, the page at `/`, the files under `/static`, and refused paths |
| `tests/test_page_script.py` | REQ-002 form fields and the upload call. REQ-003 the job list, the empty text, polling, and no `innerHTML` |
| `tests/test_stem_links.py` | REQ-004 `stemLinks` under `node`, encoded names, and the done-only render |

Tests check the served files and the API calls over HTTP. No test starts a browser.
