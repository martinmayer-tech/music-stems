"""The job store: one SQLite table that this component owns."""

from __future__ import annotations

import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

QUEUED = "queued"
RUNNING = "running"
DONE = "done"
FAILED = "failed"
STATUSES = (QUEUED, RUNNING, DONE, FAILED)

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'queued'
        CHECK (status IN ('queued', 'running', 'done', 'failed')),
    input_path TEXT NOT NULL,
    full_stems INTEGER NOT NULL DEFAULT 0 CHECK (full_stems IN (0, 1)),
    options TEXT NOT NULL DEFAULT '{}',
    outputs TEXT,
    error TEXT,
    created_at TEXT NOT NULL,
    started_at TEXT,
    finished_at TEXT
);
CREATE INDEX IF NOT EXISTS jobs_status_created ON jobs (status, created_at);
"""

COLUMNS = (
    "id, status, input_path, full_stems, options, outputs, error, "
    "created_at, started_at, finished_at"
)


@dataclass(frozen=True)
class Job:
    """One row of the jobs table."""

    id: str
    status: str
    input_path: str
    full_stems: bool
    options: dict[str, Any]
    outputs: list[str] | None
    error: str | None
    created_at: str
    started_at: str | None
    finished_at: str | None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def _job(row: sqlite3.Row | tuple[Any, ...]) -> Job:
    outputs = json.loads(row[5]) if row[5] is not None else None
    return Job(
        id=row[0],
        status=row[1],
        input_path=row[2],
        full_stems=bool(row[3]),
        options=json.loads(row[4]),
        outputs=outputs,
        error=row[6],
        created_at=row[7],
        started_at=row[8],
        finished_at=row[9],
    )


def _one_line(text: str) -> str:
    lines = str(text).strip().splitlines()
    return lines[0].strip() if lines else ""


class JobStore:
    """Reads and writes the jobs table. Every call commits before it returns."""

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        try:
            yield conn
        finally:
            conn.close()

    def add(
        self,
        input_path: str | os.PathLike[str],
        full_stems: bool = False,
        options: dict[str, Any] | None = None,
    ) -> str:
        """Insert a queued job and return its id."""
        job_id = uuid.uuid4().hex
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO jobs (id, status, input_path, full_stems, options, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    job_id,
                    QUEUED,
                    str(input_path),
                    int(bool(full_stems)),
                    json.dumps(options or {}),
                    _now(),
                ),
            )
        return job_id

    def get(self, job_id: str) -> Job | None:
        """Return one job, or None for an unknown id."""
        with self._connect() as conn:
            row = conn.execute(f"SELECT {COLUMNS} FROM jobs WHERE id = ?", (job_id,)).fetchone()
        return _job(row) if row else None

    def list(self) -> list[Job]:
        """Return every job in creation order."""
        with self._connect() as conn:
            rows = conn.execute(f"SELECT {COLUMNS} FROM jobs ORDER BY created_at, rowid").fetchall()
        return [_job(r) for r in rows]

    def claim_next(self) -> Job | None:
        """Move the oldest queued job to running and return it."""
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                row = conn.execute(
                    f"SELECT {COLUMNS} FROM jobs WHERE status = ? "
                    "ORDER BY created_at, rowid LIMIT 1",
                    (QUEUED,),
                ).fetchone()
                if row is None:
                    conn.execute("COMMIT")
                    return None
                conn.execute(
                    "UPDATE jobs SET status = ?, started_at = ? WHERE id = ?",
                    (RUNNING, _now(), row[0]),
                )
                conn.execute("COMMIT")
            except BaseException:
                conn.execute("ROLLBACK")
                raise
        return self.get(row[0])

    def mark_done(self, job_id: str, outputs: list[str]) -> None:
        """Set a job to done and store its output paths."""
        with self._connect() as conn:
            conn.execute(
                "UPDATE jobs SET status = ?, outputs = ?, finished_at = ? WHERE id = ?",
                (DONE, json.dumps([str(p) for p in outputs]), _now(), job_id),
            )

    def mark_failed(self, job_id: str, error: str) -> None:
        """Set a job to failed and store one error line."""
        with self._connect() as conn:
            conn.execute(
                "UPDATE jobs SET status = ?, error = ?, finished_at = ? WHERE id = ?",
                (FAILED, _one_line(error), _now(), job_id),
            )

    def recover(self) -> int:
        """Return every running job to queued. Return how many changed."""
        with self._connect() as conn:
            cursor = conn.execute(
                "UPDATE jobs SET status = ?, started_at = NULL WHERE status = ?",
                (QUEUED, RUNNING),
            )
            return cursor.rowcount
