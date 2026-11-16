# Component registry

> Living document. Reflects current system state.

Last updated: 0000016-docker-packaging

| Component | Type | Purpose | Status |
|-----------|------|---------|--------|
| [stem-core](../src/stem-core/docs/purpose.md) | component-pack | The two-pass separation function with model options, and the `stems` command | active (`split()`, the model options, and the `stems` command built) |
| [stem-service](../src/stem-service/docs/purpose.md) | microservice | The job store, the worker, the HTTP API, the route that serves the page, and the Docker image | active (job store, worker, HTTP API, page route, and Docker files built) |
| [stem-web](../src/stem-web/docs/purpose.md) | microfrontend | The web page that the API serves | active (page built) |
