"""Where the service keeps its data."""

from __future__ import annotations

import os
from pathlib import Path

DATA_DIR_VARIABLE = "STEMS_DATA_DIR"
DEFAULT_DATA_DIR = "./data"
DATABASE_NAME = "jobs.sqlite3"
JOBS_FOLDER = "jobs"


def resolve_data_dir() -> str:
    """Return the data folder from STEMS_DATA_DIR, or the default."""
    return os.environ.get(DATA_DIR_VARIABLE) or DEFAULT_DATA_DIR


def database_path(data_dir: str | os.PathLike[str] | None = None) -> Path:
    """Return the path of the SQLite file inside the data folder."""
    return Path(data_dir or resolve_data_dir()) / DATABASE_NAME


def job_output_dir(job_id: str, data_dir: str | os.PathLike[str] | None = None) -> Path:
    """Return the folder that holds the output of one job."""
    return Path(data_dir or resolve_data_dir()) / JOBS_FOLDER / job_id
