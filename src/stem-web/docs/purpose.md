# stem-web: purpose

stem-web holds the web page that the API serves. The page uses plain HTML, CSS, and JavaScript with no build.

A user opens the service root in a browser. The page uploads a file with the full stems option and three model selects, lists each job, and polls until each job ends. For a finished job, it shows one player and one download link for each stem.

stem-service serves the page at `/` and its files under `/static`. The page calls the HTTP API of stem-service from the same origin.

This component owns no data, so it has no data contract.
