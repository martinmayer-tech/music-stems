# stem-web: risk and scope

Risk level: medium. The page shows server text and has no browser test.

In scope: the page files, `static_dir()`, an upload form, a polling job list, and one player and one download link for each stem.
Out of scope: a build step, a UI library, browser automation, a login, cancel, delete, and model choice.
Deferred: model choice waits for step 7.

Risks:

- Server text such as a file name or an error line could run as markup. The script uses `textContent` and `setAttribute` only, and a test rejects `innerHTML`.
- The DOM code has no browser test, by decision. A `node` test covers `stemLinks` only.
- `stem-service` imports `stem_web`. An operator who runs the service outside the repo layout needs `src/stem-web` on the Python path. Step 8 packages both.
