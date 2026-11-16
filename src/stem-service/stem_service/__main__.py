"""Run the HTTP API with `python -m stem_service`."""

from __future__ import annotations

from stem_service.api import create_app
from stem_service.config import resolve_host, resolve_port


def main() -> None:
    """Serve the app on STEMS_HOST and STEMS_PORT. The host defaults to 127.0.0.1."""
    import uvicorn

    uvicorn.run(create_app(), host=resolve_host(), port=resolve_port())


if __name__ == "__main__":
    main()
