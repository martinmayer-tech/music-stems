"""Where the service keeps its data."""

from __future__ import annotations

import os
from pathlib import Path

DATA_DIR_VARIABLE = "STEMS_DATA_DIR"
DEFAULT_DATA_DIR = "./data"
DATABASE_NAME = "jobs.sqlite3"
JOBS_FOLDER = "jobs"
UPLOADS_FOLDER = "uploads"

HOST_VARIABLE = "STEMS_HOST"
DEFAULT_HOST = "127.0.0.1"
PORT_VARIABLE = "STEMS_PORT"
DEFAULT_PORT = 8000
MAX_UPLOAD_VARIABLE = "STEMS_MAX_UPLOAD_MB"
DEFAULT_MAX_UPLOAD_MB = 500


def resolve_data_dir() -> str:
    """Return the data folder from STEMS_DATA_DIR, or the default."""
    return os.environ.get(DATA_DIR_VARIABLE) or DEFAULT_DATA_DIR


def database_path(data_dir: str | os.PathLike[str] | None = None) -> Path:
    """Return the path of the SQLite file inside the data folder."""
    return Path(data_dir or resolve_data_dir()) / DATABASE_NAME


def job_output_dir(job_id: str, data_dir: str | os.PathLike[str] | None = None) -> Path:
    """Return the folder that holds the output of one job."""
    return Path(data_dir or resolve_data_dir()) / JOBS_FOLDER / job_id


def uploads_dir(data_dir: str | os.PathLike[str] | None = None) -> Path:
    """Return the folder that holds uploaded files."""
    return Path(data_dir or resolve_data_dir()) / UPLOADS_FOLDER


def resolve_host() -> str:
    """Return the bind address from STEMS_HOST, or the loopback address."""
    return os.environ.get(HOST_VARIABLE) or DEFAULT_HOST


def resolve_port() -> int:
    """Return the port from STEMS_PORT, or the default."""
    return int(os.environ.get(PORT_VARIABLE) or DEFAULT_PORT)


def resolve_max_upload_bytes() -> int:
    """Return the upload limit in bytes from STEMS_MAX_UPLOAD_MB, or the default."""
    megabytes = int(os.environ.get(MAX_UPLOAD_VARIABLE) or DEFAULT_MAX_UPLOAD_MB)
    return megabytes * 1024 * 1024
