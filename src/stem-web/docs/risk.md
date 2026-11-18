# stem-web: risk and scope

Risk level: medium. The page shows server text and has no browser test.

In scope: the page files, `static_dir()`, an upload form, a polling job list, and one player and one download link for each stem.
In scope also: three selects for the model options.
Out of scope: a build step, a UI library, browser automation, a login, cancel, and delete.
Deferred: nothing.

Risks:

- Server text such as a file name or an error line could run as markup. The script uses `textContent` and `setAttribute` only, and a test rejects `innerHTML`.
- The page repeats the allowlists as text. A test compares them with `stem_core`, so a new model needs a change in both places.
- The DOM code has no browser test, by decision. A `node` test covers `stemLinks` only.
- `stem-service` imports `stem_web`. An operator who runs the service outside the repo layout needs `src/stem-web` on the Python path. Step 8 packages both.
