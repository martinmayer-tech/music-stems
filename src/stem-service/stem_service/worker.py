"""The worker thread and the model pool."""

from __future__ import annotations

import os
import threading
from collections.abc import Callable, Iterable
from typing import Any

from stem_core.separation import default_separator_factory, split

from stem_service.config import job_output_dir, resolve_data_dir
from stem_service.jobs import Job, JobStore

DEFAULT_POLL_INTERVAL = 0.5

SeparatorFactory = Callable[[str, str, str], Any]


class PooledSeparator:
    """The separator that split() sees. It hands each model request to the pool."""

    def __init__(self, pool: ModelPool, output_dir: str, output_format: str, model_dir: str):
        self._pool = pool
        self._output_dir = output_dir
        self._output_format = output_format
        self._model_dir = model_dir
        self._current: Any = None

    def load_model(self, model_filename: str) -> None:
        """Select a model. The pool loads it on its first request only."""
        self._current = self._pool.acquire(
            model_filename, self._output_dir, self._output_format, self._model_dir
        )

    def separate(self, *args: Any, **kwargs: Any) -> Any:
        """Run the separator that holds the last selected model."""
        return self._current.separate(*args, **kwargs)


class ModelPool:
    """Builds one separator for each model and keeps it loaded."""

    def __init__(self, base_factory: SeparatorFactory | None = None) -> None:
        self._base_factory = base_factory or default_separator_factory
        self._separators: dict[str, Any] = {}

    def acquire(
        self, model_filename: str, output_dir: str, output_format: str, model_dir: str
    ) -> Any:
        """Return the loaded separator for a model, pointed at output_dir."""
        separator = self._separators.get(model_filename)
        if separator is None:
            separator = self._base_factory(output_dir, output_format, model_dir)
            separator.load_model(model_filename=model_filename)
            self._separators[model_filename] = separator
        else:
            separator.output_dir = output_dir
        return separator

    def factory(self, output_dir: str, output_format: str, model_dir: str) -> PooledSeparator:
        """Match the separator factory signature that split() expects."""
        return PooledSeparator(self, output_dir, output_format, model_dir)


def _error_line(exc: BaseException) -> str:
    text = str(exc).strip().splitlines()
    return text[0].strip() if text else type(exc).__name__


class Worker:
    """Runs queued jobs one at a time on its own thread."""

    def __init__(
        self,
        store: JobStore,
        data_dir: str | os.PathLike[str] | None = None,
        separator_factory: SeparatorFactory | None = None,
        split_func: Callable[..., list[str]] = split,
        name: str = "default",
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> None:
        self.store = store
        self.data_dir = data_dir or resolve_data_dir()
        self.name = name
        self.poll_interval = poll_interval
        self._split = split_func
        self._pool = ModelPool(separator_factory)
        self._stop = threading.Event()
        self._wake = threading.Event()
        self._thread: threading.Thread | None = None

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self, recover: bool = True) -> None:
        """Start the thread. Requeue jobs that a restart interrupted first."""
        if self.is_running:
            return
        if recover:
            self.store.recover()
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, name=f"worker-{self.name}", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """End the thread after the current job."""
        self._stop.set()
        self._wake.set()
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def wake(self) -> None:
        """Tell an idle worker to look for a job now."""
        self._wake.set()

    def _run(self) -> None:
        while not self._stop.is_set():
            job = self.store.claim_next()
            if job is None:
                self._wake.wait(self.poll_interval)
                self._wake.clear()
                continue
            self._run_job(job)

    def _run_job(self, job: Job) -> None:
        out_dir = job_output_dir(job.id, self.data_dir)
        try:
            paths = self._split(job.input_path, out_dir, job.full_stems, self._pool.factory)
        except Exception as exc:  # noqa: BLE001 - any failure ends this job and no other
            self.store.mark_failed(job.id, _error_line(exc))
        else:
            self.store.mark_done(job.id, paths)


def start_workers(store: JobStore, devices: Iterable[str], **worker_options: Any) -> list[Worker]:
    """Start one worker for each device name. Requeue interrupted jobs once."""
    store.recover()
    workers = [Worker(store, name=device, **worker_options) for device in devices]
    for worker in workers:
        worker.start(recover=False)
    return workers
