# stem-web: interface contract

The `stem_web` package exposes `__version__` and `static_dir()`.

| Name | Meaning |
|------|---------|
| `static_dir()` | Returns the folder `stem_web/static` as a `Path`. It holds `index.html`, `app.js`, and `style.css` |

## The page

| File | Meaning |
|------|---------|
| `index.html` | The upload form with a file input, a `full_stems` checkbox, three selects named `model`, `ensemble_preset`, and `single_stem`, and a submit button. It also holds the job list `#jobs` and the status line `#status` |
| `app.js` | Posts the upload, reads `GET /jobs`, and renders each job |
| `style.css` | Styles the page |

`app.js` calls `POST /jobs`, `GET /jobs`, and `GET /jobs/{id}/stems/{name}` of stem-service. It calls no other route.

## Script behaviour

- The script polls `GET /jobs` every two seconds while a job is `queued` or `running`.
- It writes server text with `textContent` and never `innerHTML`.
- `stemLinks(jobId, stems)` returns one `{name, url}` entry for each stem name. It encodes the id and the name with `encodeURIComponent`.
- A `done` job shows one `audio` player and one download link for each stem. Any other status shows none.
- `optionFields(values)` returns a `[name, value]` pair for each select that holds a non-empty value. The upload sends only those fields.
- Each select lists the values of its allowlist in `stem_core.separation`. A test keeps the two in line.
- When `module` exists, the script exports `stemLinks`, `hasUnfinishedJob`, and `optionFields` so that `node` can test them.
