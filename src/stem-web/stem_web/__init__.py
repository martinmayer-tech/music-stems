"""The web page that the API serves."""

from pathlib import Path

__version__ = "0.0.0"


def static_dir() -> Path:
    """Return the folder that holds `index.html`, `app.js`, and `style.css`."""
    return Path(__file__).resolve().parent / "static"
