"""Transfers of many files: a local directory to Files.com, a remote folder
to a local directory, or a list of files either way.

A job walks its source a little at a time, on the calling thread, and runs
up to max_files file transfers at once with the same engines as single
uploads and downloads, all within the client's TransferLimiter, which is
how several jobs and clients share one budget fairly. An upload job's
adaptive uploads share one controller for each compatible kind of upload,
so one request budget and what it learns, for the job only (see
uploads.UploadScope), and so do a download job's adaptive downloads (see
downloads.DownloadScope). Without max_files, an upload job whose uploads may use
the scaled S3 policy starts with six files and prepares enough to feed that
controller's target, within AUTOMATIC_MAX_FILES. One file failing
does not stop the others: each file's outcome is in the TransferResult the
job returns. Cancelling, closing the client, the deadline and the pause
token stop the whole job; it waits for its transfers before raising.

With a checkpoint, a job records the files it completed and each
unfinished file's own checkpoint, by the pair of paths it transfers
between, for the job's site and workspace. Calling it again with the
checkpoint resumes the unfinished files and skips a completed file only
when the job can show nothing about it changed: for an upload, that the
local file is the one uploaded, unchanged, and the remote file is still
the one it made; for a download, that the local file is still the one the
download made, and that Files.com still offers the same version of the
remote file (by its download identity; a download without one is done
again). Anything else is transferred again.

A job's local directory is opened once, and the folders under it one at a
time, without following links (see files_sdk.localfs), so a link put in
place of a folder cannot lead the job outside it.
"""

import collections
import concurrent.futures
import dataclasses
import json
import math
import os
import stat
import sys
import threading
import time
from typing import Any, Callable, Iterator

from files_sdk.checkpoint import (
    JobCheckpoint,
    checked_checkpoint,
    checked_pause,
    digest,
    scope,
)
from files_sdk.error import (
    DeadlineExceededError,
    InvalidParameterError,
    NotFoundError,
    OperationCancelledError,
    TransferPausedError,
)
from files_sdk.lifetime import CancellationToken, Lifetime
from files_sdk.localfs import Directory
import files_sdk.download as downloads
import files_sdk.path_util as path_util
import files_sdk.upload as uploads
import files_sdk.util as util

DEFAULT_MAX_FILES = 4
"""Files a job transfers at once, when max_files is not given."""

MAX_FILES = 64

AUTOMATIC_MAX_FILES = 128
"""The most files an upload job prepares at once when, without max_files,
it admits files to feed the scaled S3 policy's target: the shared adaptive
upload reference's file-admission cap."""

_PROGRESS_INTERVAL = 0.25

# How often an upload job adapting its file admission rechecks it.
_ADMISSION_INTERVAL = 0.1

# The target file admission assumes before any of a job's uploads has a
# shared controller: hence six files at first.
_TARGET_BEFORE_SCOPE = 4


class _FileAdmission:
    """How many files an upload job prepares at once when the caller gives
    no max_files and its uploads may use the scaled S3 policy, from the
    shared controller's target t: at least min(cap, max(4, t + t // 4 + 1)),
    with t taken as four before that controller exists, so six files at
    first. While fewer than t // 4 + 1 part attempts wait only for a permit,
    the limit it remembers rises by one per 100 ms since its last change,
    within cap, so that files begun and finished more slowly than their
    parts are sent still feed the target; when enough wait, it falls by one
    per 100 ms to the target's limit. File completions admit replacements
    without restarting that interval. While the target warms up, the
    remembered limit rises in proportion to it, final raise included,
    counting from a target of one for a scope that started warm. This
    prepares files only: request admission and the buffer budget stay
    bounded on their own, and a cap too low for the target leaves it
    unfed."""

    def __init__(self, cap):
        self.cap = cap
        self.remembered: int | None = None
        self.changed = 0.0
        self.reference = 1
        self.warming = False

    def limit(self, view, now, in_progress):
        if view is None:
            # No shared controller yet: its target is taken as four.
            return self._derived(_TARGET_BEFORE_SCOPE)
        target, warming, started_warm, queued = view
        derived = self._derived(target)
        remembered = self.remembered
        if remembered is None:
            # Files prepared before the target was known count toward the
            # startup target of one.
            self.reference = 1 if started_warm else target
            remembered = max(
                self._derived(self.reference), min(self.cap, in_progress)
            )
            self.changed = now
            self.warming = warming or started_warm
        if target > self.reference and self.warming:
            remembered = min(
                self.cap, math.ceil(remembered * target / self.reference)
            )
        self.reference = target
        self.warming = warming
        if now - self.changed >= _ADMISSION_INTERVAL:
            if queued < target // 4 + 1:
                if remembered < self.cap:
                    remembered += 1
                    self.changed = now
            elif remembered > derived:
                remembered -= 1
                self.changed = now
        self.remembered = remembered
        return max(derived, remembered)

    def _derived(self, target):
        return min(self.cap, max(4, target + target // 4 + 1))


@dataclasses.dataclass(frozen=True)
class FileOutcome:
    """What happened to one file or folder of a job.

    kind is "file" or "folder". status is "completed", "failed",
    "skipped" (with reason saying why), "paused" or "cancelled". bytes is
    the file's size, for a completed file. error is the exception a failed
    file raised.
    """

    kind: str
    local_path: str
    remote_path: str
    status: str
    bytes: int = 0
    error: BaseException | None = None
    reason: str | None = None


@dataclasses.dataclass(frozen=True)
class TransferResult:
    """The outcome of every file and folder a job came to, in the order it
    came to them."""

    outcomes: tuple[FileOutcome, ...]

    @property
    def completed(self) -> list[FileOutcome]:
        return [
            outcome
            for outcome in self.outcomes
            if outcome.status == "completed"
        ]

    @property
    def failed(self) -> list[FileOutcome]:
        return [
            outcome for outcome in self.outcomes if outcome.status == "failed"
        ]

    @property
    def skipped(self) -> list[FileOutcome]:
        return [
            outcome for outcome in self.outcomes if outcome.status == "skipped"
        ]

    @property
    def ok(self) -> bool:
        """Whether every file and folder completed or was skipped."""
        return all(
            outcome.status in ("completed", "skipped")
            for outcome in self.outcomes
        )

    def __repr__(self):
        counts = collections.Counter(
            outcome.status for outcome in self.outcomes
        )
        return "<files_sdk.TransferResult {}>".format(
            ", ".join(
                "{} {}".format(count, status)
                for status, count in sorted(counts.items())
            )
            or "empty"
        )


@dataclasses.dataclass(frozen=True)
class TransferJobProgress:
    """How far a job has got, as passed to its progress callback.

    files_found counts the files found so far; scan_complete says whether
    that is all of them. bytes_committed counts the bytes of files
    completed and of parts or ranges of files in progress that arrived.
    """

    files_completed: int
    files_failed: int
    files_skipped: int
    files_found: int
    scan_complete: bool
    bytes_committed: int
    bytes_found: int
    elapsed: float
    bytes_per_second: float


@dataclasses.dataclass
class _Item:
    kind: str  # "file", "folder", or "skip" for one the job will not transfer
    name: str  # How the job's checkpoint knows it: by the paths it is between.
    local_path: str
    remote_path: str
    size: int = 0
    # For an upload, what identifies the local file as found.
    identity: Any = None
    reason: str | None = None
    error: BaseException | None = None
    # What a skipped item is, for its outcome.
    skipped_kind: str = "file"
    # Where under a job's local directory it is.
    parts: tuple[str, ...] | None = None


def _pair_name(source, destination):
    """How a job's checkpoint knows a file of a list of pairs."""
    return json.dumps([source, destination])


def _local_identity(found):
    return [found.st_dev, found.st_ino, found.st_size, found.st_mtime_ns]


def checked_max_files(value) -> int:
    if value is None:
        return DEFAULT_MAX_FILES
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or not 1 <= value <= MAX_FILES
    ):
        raise InvalidParameterError(
            "max_files must be an integer from 1 to {}".format(MAX_FILES)
        )
    return value


class _Job:
    """One job, from its first file to its last. See the module docstring."""

    def __init__(
        self,
        operation,
        direction,
        max_files,
        progress,
        pause,
        checkpoint,
        implicit_files=False,
    ):
        self.operation = operation
        self.direction = direction
        self.max_files = checked_max_files(max_files)
        # The job's shared learning, and, for an upload job with
        # implicit_files (no max_files, and uploads that may use the scaled
        # S3 policy), its file admission adapting to it. A download job
        # admits files only up to max_files.
        self.scope: Any = (
            uploads.UploadScope()
            if direction == "upload"
            else downloads.DownloadScope()
        )
        self.files = (
            _FileAdmission(AUTOMATIC_MAX_FILES)
            if direction == "upload" and implicit_files
            else None
        )
        self.callback = uploads.checked_progress(progress)
        self.pause = checked_pause(pause)
        self.checkpoint: JobCheckpoint | None = checkpoint
        # Transfers a file, returning its bytes and what the checkpoint
        # records of it; and says whether a file the checkpoint recorded is
        # still as it was.
        self.transfer: Callable[[Any, _Item, Any], tuple[int, Any]] | None = (
            None
        )
        self.confirm: Callable[[Any, _Item, Any], bool] | None = None
        # Stops every file's transfer when the operation stops or the job
        # fails.
        self.stopping = CancellationToken()
        lifetime = operation.lifetime
        self.lifetime = Lifetime(
            lifetime.closing, self.stopping, lifetime.deadline
        )
        from files_sdk.api import Operation

        self._operation_class = Operation
        self.outcomes: list[FileOutcome | None] = []
        self.lock = threading.Lock()
        self.in_progress: dict[int, int] = (
            {}
        )  # item index -> bytes committed so far
        self.bytes_done = 0
        self.bytes_found = 0
        self.found = 0
        self.scan_complete = False
        self.started = time.monotonic()
        self.samples: collections.deque[tuple[float, int]] = (
            collections.deque()
        )
        self.reported_at = 0.0

    def _file_limit(self, in_progress):
        if self.files is None or self.scope is None:
            return self.max_files
        view = self.scope.admission()
        if view is None and self.scope.started():
            # Its uploads have controllers, none of them the scaled S3
            # policy's: max_files' default, as for any other upload job.
            return self.max_files
        return self.files.limit(view, time.monotonic(), in_progress)

    def run(self, items: Iterator[_Item]) -> TransferResult:
        stop_watching = self.operation.lifetime.watch(self.stopping.cancel)
        # Workers start only as files do.
        workers = self.max_files if self.files is None else AUTOMATIC_MAX_FILES
        executor = concurrent.futures.ThreadPoolExecutor(
            workers, thread_name_prefix="files_sdk job"
        )
        interval = (
            _PROGRESS_INTERVAL if self.files is None else _ADMISSION_INTERVAL
        )
        in_flight: dict[concurrent.futures.Future[Any], tuple[int, _Item]] = {}
        paused = False
        try:
            try:
                while True:
                    paused = paused or (
                        self.pause is not None and self.pause.paused
                    )
                    while (
                        not paused
                        and not self.scan_complete
                        and len(in_flight) < self._file_limit(len(in_flight))
                    ):
                        self.operation.lifetime.check("transferring files")
                        try:
                            item = next(items)
                        except StopIteration:
                            self.scan_complete = True
                            break
                        index = self._add(item)
                        if item.kind == "skip":
                            self._record(
                                index,
                                item,
                                "failed" if item.error else "skipped",
                                error=item.error,
                            )
                        else:
                            recorded = self._completed_before(item)
                            in_flight[
                                executor.submit(
                                    self._run_one, index, item, recorded
                                )
                            ] = (index, item)
                    if not in_flight and (self.scan_complete or paused):
                        break
                    done, _ = concurrent.futures.wait(
                        list(in_flight),
                        timeout=interval,
                        return_when=concurrent.futures.FIRST_COMPLETED,
                    )
                    for future in done:
                        in_flight.pop(future)
                        future.result()  # Outcomes are recorded by the task; this raises only its bugs.
                    self.operation.lifetime.check("transferring files")
                    self._report()
                    if self.checkpoint is not None:
                        self.checkpoint.save_job()
            except BaseException:
                self.stopping.cancel()
                concurrent.futures.wait(list(in_flight))
                raise
        except BaseException as error:
            result = self._result()
            self._save_quietly(error)
            lifetime = self.operation.lifetime
            if lifetime.stopped and isinstance(
                error, (OperationCancelledError, DeadlineExceededError)
            ):
                error = lifetime.stopped_error("transferring files")
            setattr(error, "result", result)
            raise error from None
        finally:
            executor.shutdown(wait=True)
            stop_watching()
        result = self._result()
        self._report(force=True)
        self._log(result, paused)
        if paused:
            assert self.checkpoint is not None
            self.checkpoint.save_job(final=True)
            raise TransferPausedError(
                "The job was paused. Run it again with the same checkpoint to resume it.",
                checkpoint=self.checkpoint.path,
                result=result,
            )
        if self.checkpoint is not None:
            if result.ok:
                self.checkpoint.clear()
            else:
                self.checkpoint.save_job(final=True)
        return result

    def _add(self, item):
        with self.lock:
            self.outcomes.append(None)
            if item.kind == "file":
                self.found += 1
                self.bytes_found += item.size
            return len(self.outcomes) - 1

    def _completed_before(self, item):
        """What the checkpoint recorded of item's completion, if what can be
        checked locally is unchanged; the rest is confirmed before it is
        skipped."""
        if self.checkpoint is None or item.kind != "file":
            return None
        recorded = self.checkpoint.completed.get(item.name)
        if not isinstance(recorded, dict):
            return None
        if self.direction == "upload":
            return (
                recorded if recorded.get("source") == item.identity else None
            )
        try:
            found = os.lstat(item.local_path)
        except OSError:
            return None
        # The local file must be the very file the download made.
        return (
            recorded
            if recorded.get("output") == _local_identity(found)
            else None
        )

    def _run_one(self, index, item, recorded=None):
        # Runs in a job thread.
        operation = self._operation_class(
            None, self.lifetime, _state=self.operation._state
        )
        with self.lock:
            self.in_progress[index] = 0
        try:
            if recorded is not None:
                if self.confirm is not None and self.confirm(
                    operation, item, recorded
                ):
                    self._record(
                        index,
                        item,
                        "completed",
                        recorded.get("size") or 0,
                        reason="completed before",
                    )
                    return
                if self.checkpoint is not None:
                    self.checkpoint.forget(item.name)
            transferred, record = self.transfer(operation, item, self._file_progress(index))  # type: ignore[misc]
        except TransferPausedError:
            self._record(index, item, "paused")
        except (OperationCancelledError, DeadlineExceededError) as error:
            if self.lifetime.stopped:
                self._record(index, item, "cancelled")
            else:
                self._record(index, item, "failed", error=error)
        except Exception as error:
            self._record(index, item, "failed", error=error)
        else:
            if self.checkpoint is not None and item.kind == "file":
                self.checkpoint.complete(item.name, record)
            self._record(index, item, "completed", transferred)

    def _file_progress(self, index):
        def update(progress):
            with self.lock:
                self.in_progress[index] = progress.bytes_committed

        return update

    def _record(self, index, item, status, size=0, error=None, reason=None):
        outcome = FileOutcome(
            kind=item.kind if item.kind != "skip" else item.skipped_kind,
            local_path=item.local_path,
            remote_path=item.remote_path,
            status=status,
            bytes=size if status == "completed" else 0,
            error=error,
            reason=reason or item.reason,
        )
        with self.lock:
            self.outcomes[index] = outcome
            self.in_progress.pop(index, None)
            if status == "completed":
                self.bytes_done += size

    def _result(self):
        with self.lock:
            return TransferResult(
                tuple(
                    outcome for outcome in self.outcomes if outcome is not None
                )
            )

    def _report(self, force=False):
        if self.callback is None:
            return
        now = time.monotonic()
        if not force and now - self.reported_at < _PROGRESS_INTERVAL:
            return
        with self.lock:
            outcomes = [
                outcome
                for outcome in self.outcomes
                if outcome is not None and outcome.kind == "file"
            ]
            committed = self.bytes_done + sum(self.in_progress.values())
            found, bytes_found = self.found, self.bytes_found
        self.samples.append((now, committed))
        while len(self.samples) > 1 and now - self.samples[0][0] > 5:
            self.samples.popleft()
        first_time, first_committed = self.samples[0]
        self.reported_at = now
        self.callback(
            TransferJobProgress(
                files_completed=sum(
                    1 for outcome in outcomes if outcome.status == "completed"
                ),
                files_failed=sum(
                    1 for outcome in outcomes if outcome.status == "failed"
                ),
                files_skipped=sum(
                    1 for outcome in outcomes if outcome.status == "skipped"
                ),
                files_found=found,
                scan_complete=self.scan_complete,
                bytes_committed=committed,
                bytes_found=bytes_found,
                elapsed=now - self.started,
                bytes_per_second=(
                    (committed - first_committed) / (now - first_time)
                    if now > first_time
                    else 0.0
                ),
            )
        )

    def _save_quietly(self, error):
        if self.checkpoint is None:
            return
        try:
            self.checkpoint.save_job(final=True)
        except OSError as problem:
            error.add_note(
                "The checkpoint {} could not be saved: {}".format(
                    self.checkpoint.path, problem
                )
            )

    def _log(self, result, paused):
        counts = collections.Counter(
            outcome.status for outcome in result.outcomes
        )
        util.log_info(
            "Transfer job finished",
            direction=self.direction,
            completed=counts.get("completed", 0),
            failed=counts.get("failed", 0),
            skipped=counts.get("skipped", 0),
            paused=paused,
            bytes=self.bytes_done,
            seconds=round(time.monotonic() - self.started, 3),
        )


def _open_checkpoint(
    operation, checkpoint, pause, kind, local, remote, params
):
    path = checked_checkpoint(checkpoint, pause)
    if path is None:
        return None
    if local and os.path.commonpath(
        [os.path.realpath(path), os.path.realpath(local)]
    ) == os.path.realpath(local):
        raise InvalidParameterError(
            "The checkpoint of a job must not be inside the local directory it transfers"
        )
    key = {
        **scope(operation.context),
        "local": os.path.realpath(local) if local else "",
        "remote": remote,
        "params": digest(params or {}),
    }
    job = JobCheckpoint(path, kind, key)
    job.open()
    return job


def _run_job(job, items):
    try:
        return job.run(items)
    finally:
        if job.checkpoint is not None:
            job.checkpoint.close()


# Uploads.


def _remote_join(root, relative):
    return "/".join(
        part for part in (path_util.normalize(root), relative) if part
    )


def _entry_status(directory, name):
    """The entry name in directory itself, never through a link, with the
    device and inode its upload checks (a DirEntry's are zero on Windows);
    or the error looking at it raised, as when it is gone since it was
    listed, for it alone."""
    try:
        return directory.lstat(name)
    except OSError as error:
        return error


def _local_items(tree, remote_root) -> Iterator[_Item]:
    """The files and empty folders under tree's directory, a directory at a
    time, in name order. Each directory is opened from the job's directory
    one folder at a time, never through a link; links and special files are
    skipped, not followed. Each file is uploaded only if it is still the
    file found here. An entry that cannot be looked at fails alone; a
    folder that cannot be opened or listed fails as a whole."""
    stack: list[tuple[str, ...]] = [()]
    while stack:
        parts = stack.pop()
        relative = "/".join(parts)
        path = tree.local_path(parts)
        try:
            with tree.open(parts) as directory:
                with os.scandir(
                    directory.fd
                    if directory.fd is not None
                    else directory.path
                ) as scanner:
                    entries = sorted(
                        (
                            (entry.name, _entry_status(directory, entry.name))
                            for entry in scanner
                        ),
                        key=lambda pair: pair[0],
                    )
        except OSError as error:
            yield _Item(
                "skip",
                relative,
                path,
                _remote_join(remote_root, relative),
                error=error,
                skipped_kind="folder",
            )
            continue
        if not entries and relative:
            yield _Item(
                "folder", relative, path, _remote_join(remote_root, relative)
            )
        folders = []
        for entry_name, found in entries:
            name = (
                "{}/{}".format(relative, entry_name)
                if relative
                else entry_name
            )
            local = os.path.join(path, entry_name)
            remote = _remote_join(remote_root, name)
            if isinstance(found, OSError):
                yield _Item("skip", name, local, remote, error=found)
            elif stat.S_ISLNK(found.st_mode):
                yield _Item(
                    "skip", name, local, remote, reason="symbolic link"
                )
            elif stat.S_ISDIR(found.st_mode):
                folders.append(parts + (entry_name,))
            elif stat.S_ISREG(found.st_mode):
                yield _Item(
                    "file",
                    name,
                    local,
                    remote,
                    found.st_size,
                    _local_identity(found),
                )
            else:
                yield _Item(
                    "skip", name, local, remote, reason="not a regular file"
                )
        # Depth first, in name order.
        stack.extend(reversed(folders))


def _given_uploads(files) -> Iterator[_Item]:
    for pair in files:
        local, remote = _pair(pair, "files to upload")
        name = _pair_name(os.path.abspath(local), path_util.normalize(remote))
        try:
            found = os.stat(local)
        except OSError as error:
            yield _Item("skip", name, local, remote, error=error)
            continue
        if not stat.S_ISREG(found.st_mode):
            yield _Item(
                "skip", name, local, remote, reason="not a regular file"
            )
            continue
        yield _Item(
            "file", name, local, remote, found.st_size, _local_identity(found)
        )


def _pair(pair, what):
    if not (isinstance(pair, (tuple, list)) and len(pair) == 2):
        raise InvalidParameterError(
            "Each of the {} must be a pair of paths".format(what)
        )
    first, second = pair
    return os.fspath(first) if isinstance(first, os.PathLike) else first, (
        os.fspath(second) if isinstance(second, os.PathLike) else second
    )


def _uploader(params, max_concurrency, tuning, pause, job):
    params = dict(params or {})
    params.setdefault("mkdir_parents", True)

    def transfer(operation, item, progress):
        if item.kind == "folder":
            from files_sdk.error import DestinationExistsError
            from files_sdk.models.folder import FolderResource

            try:
                # Sent again after a lost answer: a folder that exists is fine.
                FolderResource(operation.replay_safe()).create(
                    item.remote_path, {"mkdir_parents": True}
                )
            except DestinationExistsError:
                pass
            return 0, None
        store = (
            job.checkpoint.slot(item.name)
            if job.checkpoint is not None
            else None
        )
        file = uploads.upload_path(
            operation,
            item.remote_path,
            item.local_path,
            params,
            max_concurrency=max_concurrency,
            progress=progress,
            tuning=tuning,
            pause_token=pause,
            store=store,
            expected=item.identity,
            scope=job.scope,
        )
        return item.size, {
            "source": item.identity,
            "remote": _remote_identity(file),
            "size": item.size,
        }

    return transfer


def _remote_identity(file):
    mtime = getattr(file, "mtime", None)
    return [getattr(file, "size", None), None if mtime is None else str(mtime)]


def _confirm_upload(operation, item, recorded):
    """Whether the remote file is still the one the upload made."""
    from files_sdk.models.file import FileResource

    try:
        found = FileResource(operation).find(item.remote_path)
    except NotFoundError:
        return False
    return getattr(found, "type", "file") != "directory" and _remote_identity(
        found
    ) == recorded.get("remote")


def upload_directory(
    operation,
    local_path,
    remote_path="",
    params=None,
    *,
    max_files=None,
    max_concurrency=None,
    progress=None,
    tuning=None,
    checkpoint=None,
    pause_token=None,
) -> TransferResult:
    """Upload the files and folders under the local directory local_path
    into remote_path."""
    local_root = os.path.abspath(os.fspath(local_path))
    if not os.path.isdir(local_root):
        raise InvalidParameterError(
            "{} is not a local directory".format(local_root)
        )
    remote_root = path_util.normalize(remote_path or "")
    job = _new_job(
        operation,
        "upload",
        max_files,
        progress,
        pause_token,
        max_concurrency,
        tuning,
        params,
    )
    job.checkpoint = _open_checkpoint(
        operation,
        checkpoint,
        job.pause,
        "upload_directory",
        local_root,
        remote_root,
        params,
    )
    job.transfer = _uploader(params, max_concurrency, tuning, job.pause, job)
    job.confirm = _confirm_upload
    try:
        tree = _LocalTree(local_root)
    except BaseException:
        if job.checkpoint is not None:
            job.checkpoint.close()
        raise
    try:
        return _run_job(job, _local_items(tree, remote_root))
    finally:
        tree.close()


def upload_files(
    operation,
    files,
    params=None,
    *,
    max_files=None,
    max_concurrency=None,
    progress=None,
    tuning=None,
    checkpoint=None,
    pause_token=None,
) -> TransferResult:
    """Upload each (local path, remote path) pair of files."""
    job = _new_job(
        operation,
        "upload",
        max_files,
        progress,
        pause_token,
        max_concurrency,
        tuning,
        params,
    )
    job.checkpoint = _open_checkpoint(
        operation, checkpoint, job.pause, "upload_files", "", "", params
    )
    job.transfer = _uploader(params, max_concurrency, tuning, job.pause, job)
    job.confirm = _confirm_upload
    return _run_job(job, _given_uploads(files))


def _new_job(
    operation,
    direction,
    max_files,
    progress,
    pause_token,
    max_concurrency,
    tuning,
    params,
):
    # Everything is checked before anything is sent.
    implicit_files = False
    if direction == "upload":
        uploads.checked_upload_concurrency(max_concurrency)
        chosen = uploads.checked_tuning(tuning, operation.context)
        uploads.split_params(params)
        operation.require_single_completion()
        # Without max_files, an upload job admits files to feed its target
        # when its uploads may use the scaled S3 policy, which they do for
        # S3; static and explicit concurrency tuning never do.
        implicit_files = (
            max_files is None and chosen.policy("s3") == uploads.SCALED_S3
        )
    else:
        uploads.checked_concurrency(max_concurrency)
        downloads.checked_tuning(tuning)
    return _Job(
        operation,
        direction,
        max_files,
        progress,
        pause_token,
        None,
        implicit_files,
    )


# Downloads.


class _LocalTree:
    """A job's local directory, opened once (following any link its path
    is, as the caller chose it), and the folders under it, each opened from
    it one folder at a time without following links. A folder download's
    files go only inside it, and never two remote files to one local file."""

    def __init__(self, root):
        self.path = root
        self.root = Directory.open(root)
        self.taken: set[str] = set()
        self.lock = threading.Lock()

    def close(self):
        self.root.close()

    def local_path(self, parts):
        return os.path.join(self.path, *parts)

    def open(self, parts, create=False) -> Directory:
        """The folder at parts under the directory, opened (and made, if
        create) a folder at a time. A link on the way is refused."""
        if self.root.fd is not None:
            current = Directory(self.path, os.dup(self.root.fd))
        else:
            current = Directory(self.path)
        try:
            for name in parts:
                found = current.child(name, create=create)
                current.close()
                current = found
        except BaseException:
            current.close()
            raise
        return current

    def parts_for(self, relative) -> tuple[str, ...]:
        """Where the remote file relative goes under the directory."""
        parts = relative.split("/")
        if any(
            part in ("", ".", "..")
            or "\x00" in part
            or os.sep in part
            or (os.altsep and os.altsep in part)
            for part in parts
        ):
            raise InvalidParameterError(
                "The remote name {!r} cannot be a local file name".format(
                    relative
                )
            )
        if sys.platform == "win32" and any(":" in part for part in parts):
            raise InvalidParameterError(
                "The remote name {!r} cannot be a local file name".format(
                    relative
                )
            )
        local = self.local_path(parts)
        key = (
            local.casefold() if sys.platform in ("darwin", "win32") else local
        )
        with self.lock:
            if key in self.taken:
                raise InvalidParameterError(
                    "Another remote file has the local name {}".format(local)
                )
            self.taken.add(key)
        return tuple(parts)


def _remote_items(operation, remote_root, tree) -> Iterator[_Item]:
    """The files and empty folders under remote_root, a folder at a time,
    fetching each listing's pages as they are needed."""
    from files_sdk.models.folder import FolderResource

    root_parts = remote_root.split("/") if remote_root else []
    compare_root = [
        path_util.normalize_for_comparison(part) for part in root_parts
    ]
    stack: list[tuple[str, str, str, tuple[str, ...]]] = [
        (remote_root, tree.path, "", ())
    ]
    while stack:
        folder, local_folder, folder_relative, folder_parts = stack.pop()
        try:
            listing = FolderResource(operation).list_for(
                folder, {"per_page": 1000}
            )
        except Exception as error:
            if folder == remote_root:
                raise  # The folder asked for cannot be listed: nothing to do.
            yield _Item(
                "skip",
                folder_relative,
                local_folder,
                folder,
                error=error,
                skipped_kind="folder",
            )
            continue
        folders = []
        empty = True
        try:
            for entry in listing.auto_paging_iter():
                empty = False
                remote = path_util.normalize(entry.path or "")
                remote_parts = remote.split("/")
                compared = [
                    path_util.normalize_for_comparison(part)
                    for part in remote_parts[: len(root_parts)]
                ]
                if root_parts and (
                    len(remote_parts) <= len(root_parts)
                    or compared != compare_root
                ):
                    yield _Item(
                        "skip",
                        remote,
                        "",
                        remote,
                        reason="outside the folder listed",
                    )
                    continue
                relative = "/".join(remote_parts[len(root_parts) :])
                try:
                    parts = tree.parts_for(relative)
                except InvalidParameterError as error:
                    yield _Item("skip", relative, "", remote, error=error)
                    continue
                local = tree.local_path(parts)
                if entry.type == "directory":
                    folders.append((remote, local, relative, parts))
                else:
                    size = entry.size if isinstance(entry.size, int) else 0
                    yield _Item(
                        "file", relative, local, remote, size, parts=parts
                    )
        except Exception as error:
            # A later page failed: the files listed so far still count.
            yield _Item(
                "skip",
                folder_relative,
                local_folder,
                folder,
                error=error,
                skipped_kind="folder",
            )
        if empty and folder != remote_root:
            yield _Item(
                "folder",
                folder_relative,
                local_folder,
                folder,
                parts=folder_parts,
            )
        # Depth first, in listing order.
        stack.extend(reversed(folders))


def _given_downloads(files) -> Iterator[_Item]:
    for pair in files:
        remote, local = _pair(pair, "files to download")
        remote, local = path_util.normalize(remote), os.path.abspath(local)
        yield _Item("file", _pair_name(remote, local), local, remote)


def _downloader(max_concurrency, tuning, pause, job, tree):
    def transfer(operation, item, progress):
        if item.kind == "folder":
            tree.open(item.parts, create=True).close()
            return 0, None
        from files_sdk.models.file import File

        anchor = None
        if tree is not None:
            # A folder's files land only inside it: never through a link.
            anchor = (tree.open(item.parts[:-1], create=True), item.parts[-1])
        else:
            os.makedirs(os.path.dirname(item.local_path), exist_ok=True)
        file = operation.adopt(
            File({"path": item.remote_path, "size": item.size or None})
        )
        store = (
            job.checkpoint.slot(item.name)
            if job.checkpoint is not None
            else None
        )
        outcome: dict[str, Any] = {}
        downloads.download_path(
            operation,
            file,
            None if anchor is not None else item.local_path,
            max_concurrency=max_concurrency,
            progress=progress,
            pause_token=pause,
            store=store,
            anchor=anchor,
            outcome=outcome,
            tuning=tuning,
            scope=job.scope,
        )
        return outcome["size"], {
            "token": outcome["token"],
            "output": outcome["output"],
            "size": outcome["size"],
        }

    return transfer


def _confirm_download(operation, item, recorded):
    """Whether Files.com still offers the version of the remote file the
    download got: never, for one without a download identity."""
    token, size = recorded.get("token"), recorded.get("size")
    if not isinstance(token, str) or not isinstance(size, int):
        return False
    return downloads.unchanged(operation, item.remote_path, token, size)


def download_directory(
    operation,
    remote_path,
    local_path,
    *,
    max_files=None,
    max_concurrency=None,
    progress=None,
    checkpoint=None,
    pause_token=None,
    tuning=None,
) -> TransferResult:
    """Download the files and folders under remote_path into the local
    directory local_path, which is created if need be."""
    local_root = os.path.abspath(os.fspath(local_path))
    remote_root = path_util.normalize(remote_path or "")
    job = _new_job(
        operation,
        "download",
        max_files,
        progress,
        pause_token,
        max_concurrency,
        tuning,
        None,
    )
    # The checkpoint is admitted before anything local is made.
    job.checkpoint = _open_checkpoint(
        operation,
        checkpoint,
        job.pause,
        "download_directory",
        local_root,
        remote_root,
        None,
    )
    try:
        os.makedirs(local_root, exist_ok=True)
        tree = _LocalTree(local_root)
    except BaseException:
        if job.checkpoint is not None:
            job.checkpoint.close()
        raise
    job.transfer = _downloader(max_concurrency, tuning, job.pause, job, tree)
    job.confirm = _confirm_download
    try:
        return _run_job(job, _remote_items(operation, remote_root, tree))
    finally:
        tree.close()


def download_files(
    operation,
    files,
    *,
    max_files=None,
    max_concurrency=None,
    progress=None,
    checkpoint=None,
    pause_token=None,
    tuning=None,
) -> TransferResult:
    """Download each (remote path, local path) pair of files."""
    job = _new_job(
        operation,
        "download",
        max_files,
        progress,
        pause_token,
        max_concurrency,
        tuning,
        None,
    )
    job.checkpoint = _open_checkpoint(
        operation, checkpoint, job.pause, "download_files", "", "", None
    )
    job.transfer = _downloader(max_concurrency, tuning, job.pause, job, None)
    job.confirm = _confirm_download
    return _run_job(job, _given_downloads(files))
