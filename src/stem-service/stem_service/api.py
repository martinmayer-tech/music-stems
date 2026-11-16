"""The HTTP API: upload a mix, follow its job, and download each stem."""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Form, HTTPException, UploadFile

from stem_service.config import (
    database_path,
    resolve_data_dir,
    resolve_max_upload_bytes,
    uploads_dir,
)
from stem_service.jobs import DONE, Job, JobStore
from stem_service.worker import start_workers

ALLOWED_EXTENSIONS = (".wav", ".flac", ".mp3", ".m4a")
CHUNK_SIZE = 1024 * 1024
DEVICES = ("default",)


def _job_json(job: Job) -> dict[str, Any]:
    """Describe a job for a caller. The result holds no server path."""
    stems = None
    if job.status == DONE and job.outputs is not None:
        stems = [Path(p).name for p in job.outputs]
    return {
        "id": job.id,
        "status": job.status,
        "full_stems": job.full_stems,
        "stems": stems,
        "error": job.error,
        "created_at": job.created_at,
        "started_at": job.started_at,
        "finished_at": job.finished_at,
    }


def _client_file_name(raw: str | None) -> str:
    """Keep the last part of a name that the client sent, whatever its separator."""
    return (raw or "").replace("\\", "/").split("/")[-1].strip()


def create_app(
    data_dir: str | os.PathLike[str] | None = None,
    *,
    run_workers: bool = True,
    worker_options: dict[str, Any] | None = None,
    max_upload_bytes: int | None = None,
) -> FastAPI:
    """Build the app. It creates the data folder, the database, and the uploads folder."""
    data_dir = data_dir or resolve_data_dir()
    limit = max_upload_bytes if max_upload_bytes is not None else resolve_max_upload_bytes()
    store = JobStore(database_path(data_dir))
    uploads = uploads_dir(data_dir)
    uploads.mkdir(parents=True, exist_ok=True)
    options = {"data_dir": data_dir, **(worker_options or {})}

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.workers = start_workers(store, DEVICES, **options) if run_workers else []
        try:
            yield
        finally:
            for worker in app.state.workers:
                worker.stop()
            app.state.workers = []

    app = FastAPI(title="Stem service", lifespan=lifespan)
    app.state.store = store
    app.state.workers = []

    @app.post("/jobs", status_code=201)
    async def create_job(file: UploadFile, full_stems: bool = Form(False)) -> dict[str, Any]:
        name = _client_file_name(file.filename)
        if Path(name).suffix.lower() not in ALLOWED_EXTENSIONS:
            raise HTTPException(415, "The file must be WAV, FLAC, MP3, or M4A.")
        if file.size is not None and file.size > limit:
            raise HTTPException(413, "The upload is larger than the limit.")
        folder = uploads / uuid.uuid4().hex
        folder.mkdir(parents=True)
        target = folder / name
        written = 0
        try:
            with target.open("wb") as out:
                while chunk := await file.read(CHUNK_SIZE):
                    written += len(chunk)
                    if written > limit:
                        raise HTTPException(413, "The upload is larger than the limit.")
                    out.write(chunk)
        except BaseException:
            target.unlink(missing_ok=True)
            folder.rmdir()
            raise
        job_id = store.add(target, full_stems)
        for worker in app.state.workers:
            worker.wake()
        return _job_json(store.get(job_id))

    return app
