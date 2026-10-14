"""Pausing transfers, and the checkpoints that let a later call resume one.

A checkpoint is a small JSON file, at a path the caller chooses, recording
what a transfer has proven so far, so that a later call with the same
checkpoint continues the transfer instead of starting it again. For an
upload that is the upload's reference, where each planned part lies, the
ETags of the parts storage accepted and whether its completion has been
sent; for a download, the version of the remote file it is bound to (its
download identity's token and size, or the entity tag, size and storage
resource digest storage's own answer bound), the temporary file the SDK fills beside the
destination and the byte ranges written to it. It is for one transfer: the
source and destination, and the site and workspace, never a credential. A
checkpoint never holds a URL, credential or header: signed URLs are asked
for again when a transfer resumes.

Each save writes a new file, flushed to disk, that then replaces the old
one, and a download flushes the bytes a checkpoint records before the
checkpoint itself, so a crash or power loss can lose recent progress but a
checkpoint never claims bytes that were not written (on storage that
honors flushes). A lock file beside the checkpoint keeps two transfers
from using it at once; the operating system releases the lock if the
process dies.

What a checkpoint says decides which bytes are not sent or fetched again
and whether an upload may be completed, so its contents are used only from
where no other principal can have written them (files_sdk.access decides,
on each system, from its permissions and access control lists): a
checkpoint and its lock file must be files of the process's own user that
no one else can change, in a folder that only that user or the system can
change, reached through folders and links that only they can change. That
is checked before the checkpoint is read, and again before each save and
removal, which also refuses a checkpoint replaced since this transfer read
or wrote it. A new checkpoint or lock file is private from the moment it
exists: on macOS, where a new file takes the access control list its folder
passes on, it is made in a staging folder of the SDK's own beside the
checkpoint, made owner-only and without an access control list before
anything is made in it, and then renamed (a checkpoint) or linked (a lock
file, never replacing another) into place; on Linux the owner-only
permissions it is made with limit any list it inherits; on Windows a folder
that would pass new files access for anyone else is refused before anything
is made in it. Its digest only recognizes a checkpoint that is damaged
or incomplete: anyone who can write the file could compute it. Code running
as the same user, or as the system or an administrator, is trusted like
the SDK itself.
"""

import errno
import hashlib
import json
import os
import sys
import threading
import time
import uuid
from typing import Any

from files_sdk import access
from files_sdk.error import InvalidParameterError, InvalidRequestError
from files_sdk.transport import url_origin

_FORMAT = 1

# A checkpoint is saved at most this often while a transfer runs, and
# always when it stops.
_SAVE_INTERVAL = 1.0


class PauseToken:
    """A one-way signal that pauses the transfers it is given to.

    Pass it as pause_token to a transfer that has a checkpoint. After
    pause(), which any thread can call, the transfer starts nothing new,
    lets the parts or ranges in progress finish, saves its checkpoint and
    raises TransferPausedError. Calling it again with the same checkpoint
    resumes it. Unlike cancelling, pausing does not stop requests already
    in progress, so it can take as long as they do.
    """

    def __init__(self):
        self._paused = threading.Event()

    @property
    def paused(self) -> bool:
        return self._paused.is_set()

    def pause(self) -> None:
        self._paused.set()

    def __repr__(self):
        return "<PauseToken {}>".format("paused" if self.paused else "active")


def checked_pause(value) -> PauseToken | None:
    if value is not None and not isinstance(value, PauseToken):
        raise InvalidParameterError(
            "pause_token must be a files_sdk.PauseToken"
        )
    return value


def checked_checkpoint(value, pause) -> str | None:
    """value as an absolute path, or None. Pausing needs a checkpoint to
    resume from."""
    if value is None:
        if pause is not None:
            raise InvalidParameterError(
                "pause_token needs a checkpoint to resume from"
            )
        return None
    if not isinstance(value, (str, os.PathLike)):
        raise InvalidParameterError("checkpoint must be a local path")
    path = os.fspath(value)
    if not isinstance(path, str) or not path:
        raise InvalidParameterError("checkpoint must be a local path")
    return os.path.abspath(path)


def same_file(first, second) -> bool:
    """Whether two local paths name the same file, as far as can be told."""
    try:
        return os.path.samefile(first, second)
    except OSError:
        return os.path.realpath(first) == os.path.realpath(second)


def site(base_url) -> str:
    """The origin of base_url, as a checkpoint records the site it is for."""
    return "{}://{}:{}".format(*url_origin(base_url))


def scope(context) -> dict[str, Any]:
    """What a checkpoint records of where its transfer runs: the site and
    workspace, never a credential. A checkpoint made for another site or
    workspace is refused."""
    workspace = context.workspace_id
    return {
        "site": site(context.base_url),
        "workspace": None if workspace is None else str(workspace),
    }


_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
_CLOEXEC = getattr(os, "O_CLOEXEC", 0)
_BINARY = getattr(os, "O_BINARY", 0)


def trusted_problem(directory) -> str | None:
    """Why a checkpoint in directory could have been written or replaced by
    a principal other than this process's user, or None (see
    files_sdk.access.namespace_problem)."""
    return access.namespace_problem(directory)


def _open_nofollow(path, flags, what):
    """A descriptor for path that is not a symbolic link (nor, on Windows,
    a link or junction), or _NotTrusted."""
    if access.WINDOWS:
        try:
            if access.redirects(os.lstat(path)):
                raise _NotTrusted("its {} is a link".format(what))
        except FileNotFoundError:
            pass
    try:
        return os.open(path, flags | _NOFOLLOW | _CLOEXEC | _BINARY, 0o600)
    except OSError as error:
        if (
            _NOFOLLOW
            and error.errno in (errno.ELOOP, errno.EMLINK)
            and os.path.islink(path)
        ):
            raise _NotTrusted(
                "its {} is a symbolic link".format(what)
            ) from None
        raise


# Whether new checkpoint and lock files are made in a staging folder: on
# macOS, where a new file takes the access control list its folder passes on
# the moment it is made, and a descriptor opened then outlasts any change.
_STAGED = sys.platform == "darwin"
# What link() answers on a file system without hard links.
_NO_LINKS = frozenset(
    code
    for code in (
        errno.EPERM,
        getattr(errno, "ENOTSUP", None),
        getattr(errno, "EOPNOTSUPP", None),
    )
    if code is not None
)


class _Staging:
    """A folder of the SDK's own beside a checkpoint, where its new files are
    made so that no one else can reach them from the moment they exist: it
    is made owner-only, and its access control list removed, before any
    file is made in it (access.private_folder_problem). Files leave it by
    rename or link; it is removed afterwards, with whatever the SDK made in
    it. One left by a crash is never read."""

    def __init__(self, directory, base):
        self.path = os.path.join(
            directory, ".{}.{}.stage".format(base, uuid.uuid4().hex)
        )
        self.made: list[str] = []
        os.mkdir(self.path, 0o700)
        try:
            self.fd = os.open(
                self.path,
                os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0)
                | _NOFOLLOW
                | _CLOEXEC,
            )
        except BaseException:
            _rmdir(self.path)
            raise
        try:
            problem = access.private_folder_problem(self.fd)
        except BaseException:
            self.close()
            raise
        if problem is not None:
            self.close()
            raise _NotTrusted(problem)

    def create(self, name, flags):
        """A new owner-only file name here, open with flags, or _NotTrusted
        if it is not private."""
        handle = os.open(
            name,
            flags | os.O_CREAT | os.O_EXCL | _NOFOLLOW | _CLOEXEC | _BINARY,
            0o600,
            dir_fd=self.fd,
        )
        self.made.append(name)
        return _checked(
            handle,
            access.new_file_problem,
            "checkpoint file" if name == "checkpoint" else "lock file",
        )

    def join(self, name):
        return os.path.join(self.path, name)

    def close(self):
        for name in self.made:
            try:
                os.unlink(name, dir_fd=self.fd)
            except FileNotFoundError:
                pass  # Renamed into place.
            except OSError:
                pass
        os.close(self.fd)
        _rmdir(self.path)


def _rmdir(path):
    try:
        os.rmdir(path)
    except OSError:
        pass  # Not empty, or already gone: never read.


def _checked(handle, check, what):
    """handle, once check(handle, what) finds no problem; otherwise it is
    closed and _NotTrusted (or check's own error) raised."""
    try:
        problem = check(handle, what)
    except BaseException:
        os.close(handle)
        raise
    if problem is not None:
        os.close(handle)
        raise _NotTrusted(problem)
    return handle


class _NotTrusted(Exception):
    """Why a checkpoint could have been written by another user."""


class UntrustedCheckpointError(PermissionError):
    """A checkpoint that a transfer was using could no longer be saved or
    removed safely: its folder can now be changed by other users, or the
    checkpoint was replaced since the transfer read or wrote it. It is an
    OSError, so a transfer that stops because of another error notes it on
    that error rather than hiding it."""


def digest(value) -> str:
    """A SHA-256 of value's canonical JSON, to recognize the same params
    without storing them."""
    text = json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=str
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class CheckpointFile:
    """One checkpoint file, locked while a transfer uses it.

    key names the transfer the checkpoint belongs to; a checkpoint made
    for another transfer is refused rather than overwritten. Its contents
    are used only from where no other user can have written them (see the
    module's documentation).
    """

    def __init__(self, path, kind, key):
        self.path = path
        self.kind = kind
        self.key = key
        self._lock_path = path + ".lock"
        self._lock_handle: int | None = None
        self._saved_at: float | None = None
        # The file this transfer last read or wrote as its checkpoint (device
        # and inode), or None while there is none; a save or removal refuses
        # a checkpoint that is no longer that file.
        self._identity: tuple[int, int] | None = None
        # Held while a save builds and writes its state, so saves from
        # several threads are written in the order they were made.
        self._guard = threading.RLock()

    # Locking.

    def open(self) -> Any:
        """Lock the checkpoint and return the state it holds, or None when
        there is none yet. A checkpoint where another user could have
        written it is refused before anything is created or read."""
        try:
            problem = trusted_problem(
                os.path.dirname(self.path)
            ) or access.inheritance_problem(os.path.dirname(self.path))
            if problem is not None:
                raise _NotTrusted(problem)
            self._lock()
        except _NotTrusted as untrusted:
            raise self._untrusted(untrusted) from None
        try:
            return self._load()
        except _NotTrusted as untrusted:
            self.close()
            raise self._untrusted(untrusted) from None
        except BaseException:
            self.close()
            raise

    def _untrusted(self, untrusted):
        return InvalidRequestError(
            "The checkpoint {} cannot be used because {}. What a checkpoint says decides "
            "what a transfer does not send, fetch or complete again, so it is used only "
            "from where no other user can change it: a checkpoint file of your own that "
            "other users cannot write, in a folder that only you or the system can "
            "change (or a sticky folder such as /tmp), reached through folders and links "
            "that only you or the system can change. Keep it somewhere private, or remove "
            "it to start the transfer again.".format(self.path, untrusted)
        )

    def _lock(self):
        while True:
            try:
                handle = _open_nofollow(
                    self._lock_path, os.O_RDWR, "lock file"
                )
            except FileNotFoundError:
                handle = _make_lock(self._lock_path)
                if handle is None:
                    continue  # Another transfer made it first: lock that one.
            else:
                handle = _checked(handle, access.file_problem, "lock file")
            try:
                _lock_handle(handle)
            except OSError:
                os.close(handle)
                raise InvalidRequestError(
                    "The checkpoint {} is in use by another transfer. Wait for it "
                    "to stop, or give this transfer a checkpoint of its own.".format(
                        self.path
                    )
                ) from None
            # A transfer that finished may have removed the lock file after
            # this one opened it; lock the file that is there now instead.
            try:
                if os.path.samestat(
                    os.fstat(handle), os.stat(self._lock_path)
                ):
                    self._lock_handle = handle
                    return
            except FileNotFoundError:
                pass
            os.close(handle)

    def close(self):
        """Unlock the checkpoint."""
        handle, self._lock_handle = self._lock_handle, None
        if handle is None:
            return
        if not os.path.exists(self.path) and sys.platform != "win32":
            # Nothing left to protect. (Windows cannot remove an open file.)
            _remove(self._lock_path)
        os.close(handle)
        if not os.path.exists(self.path) and sys.platform == "win32":
            _remove(self._lock_path)

    # Reading and writing.

    def _load(self):
        try:
            handle = _open_nofollow(self.path, os.O_RDONLY, "file")
        except FileNotFoundError:
            self._identity = None
            return None
        with os.fdopen(handle, "rb") as file:
            problem = access.file_problem(file.fileno(), "file")
            if problem is not None:
                raise _NotTrusted(problem)
            found = os.fstat(file.fileno())
            self._identity = (found.st_dev, found.st_ino)
            text = file.read()
        try:
            document = json.loads(text)
        except ValueError:
            raise self._invalid("it is not JSON") from None
        if (
            not isinstance(document, dict)
            or "files_sdk_checkpoint" not in document
        ):
            raise self._invalid("it is not a files_sdk checkpoint")
        if document.get("files_sdk_checkpoint") != _FORMAT:
            raise self._invalid("it was written by another version of the SDK")
        body = {
            name: document.get(name)
            for name in ("files_sdk_checkpoint", "kind", "key", "state")
        }
        if document.get("sha256") != digest(body):
            raise self._invalid("it is incomplete or was changed")
        if (
            document.get("kind") != self.kind
            or document.get("key") != self.key
        ):
            raise InvalidParameterError(
                "The checkpoint {} belongs to another transfer ({}). Give this "
                "transfer another checkpoint, or remove that one to start this "
                "transfer again.".format(self.path, self._difference(document))
            )
        return document.get("state")

    def _difference(self, document):
        if document.get("kind") != self.kind:
            return "a {} rather than a {}".format(
                document.get("kind"), self.kind
            )
        theirs = (
            document.get("key")
            if isinstance(document.get("key"), dict)
            else {}
        )
        names = sorted(
            name
            for name in set(theirs) | set(self.key)
            if theirs.get(name) != self.key.get(name)
        )
        return (
            "its {} differ".format(", ".join(names))
            if len(names) > 1
            else "its {} differs".format(names[0])
        )

    def _invalid(self, why):
        return InvalidRequestError(
            "The checkpoint {} cannot be used because {}. Remove it to start the "
            "transfer again.".format(self.path, why)
        )

    def due(self) -> bool:
        """Whether a save that is not final would be written now."""
        return (
            self._saved_at is None
            or time.monotonic() - self._saved_at >= _SAVE_INTERVAL
        )

    def save(self, state, final=False) -> bool:
        """Write state, if final or it is due. Returns whether it wrote."""
        with self._guard:
            if not final and not self.due():
                return False
            self._check_unchanged("saved")
            body = {
                "files_sdk_checkpoint": _FORMAT,
                "kind": self.kind,
                "key": self.key,
                "state": state,
            }
            document = dict(body, sha256=digest(body))
            # The file in place is this transfer's as soon as it is renamed
            # there, even if flushing its folder then fails.
            self._identity = _replace(
                self.path,
                json.dumps(document, separators=(",", ":")).encode("utf-8"),
            )
            sync_directory(os.path.dirname(self.path))
            self._saved_at = time.monotonic()
            return True

    def clear(self):
        """Remove the checkpoint: the transfer it recorded is complete."""
        with self._guard:
            self._check_unchanged("removed")
            _remove(self.path)
            self._identity = None

    def _check_unchanged(self, done):
        """Raise UntrustedCheckpointError unless the checkpoint is still where
        no other user can change it and is the file this transfer last read
        or wrote (or still absent)."""
        problem = trusted_problem(
            os.path.dirname(self.path)
        ) or access.inheritance_problem(os.path.dirname(self.path))
        if problem is None:
            try:
                found = os.lstat(self.path)
            except FileNotFoundError:
                current = None
            else:
                current = (found.st_dev, found.st_ino)
            if current != self._identity:
                problem = (
                    "it was replaced since this transfer read or wrote it"
                )
        if problem is not None:
            raise UntrustedCheckpointError(
                errno.EACCES,
                "The checkpoint {} was not {} because {}".format(
                    self.path, done, problem
                ),
            )


class JobCheckpoint(CheckpointFile):
    """The checkpoint of a job of many files: the files completed, with what
    identified each when it was, and the state of each file in progress,
    which the file's transfer saves through its slot."""

    def __init__(self, path, kind, key):
        super().__init__(path, kind, key)
        self.completed: dict[str, Any] = {}
        self.pending: dict[str, Any] = {}
        self._state_lock = threading.Lock()
        # Whether anything changed since the job's checkpoint was saved.
        self.dirty = False

    def open(self):
        state = super().open()
        if state is not None:
            if not (
                isinstance(state, dict)
                and isinstance(state.get("completed"), dict)
                and isinstance(state.get("pending"), dict)
            ):
                self.close()
                raise self._invalid("it is not a checkpoint of a job")
            self.completed = dict(state["completed"])
            self.pending = dict(state["pending"])
        return state

    def slot(self, name) -> "_Slot":
        return _Slot(self, name)

    def complete(self, name, identity):
        with self._state_lock:
            self.pending.pop(name, None)
            self.completed[name] = identity
            self.dirty = True
        self.save_job()

    def forget(self, name):
        with self._state_lock:
            self.pending.pop(name, None)
            self.completed.pop(name, None)

    def save_job(self, final=False) -> bool:
        """Save the job's checkpoint: when final, or when something changed
        and a save is due."""
        with self._guard:
            if not final and not (self.dirty and self.due()):
                return False
            with self._state_lock:
                state = {
                    "completed": dict(self.completed),
                    "pending": dict(self.pending),
                }
                self.dirty = False
            return self.save(state, True)


class _Slot:
    """One file's part of a job checkpoint, used as a transfer's checkpoint."""

    def __init__(self, job, name):
        self.job = job
        self.name = name
        self.path = job.path

    def load(self):
        return self.job.pending.get(self.name)

    def due(self):
        return self.job.due()

    def save(self, state, final=False, durable=False):
        with self.job._state_lock:
            self.job.pending[self.name] = state
            self.job.dirty = True
        if durable:
            # Needed on disk now, such as before an upload completes.
            return self.job.save_job(final=True)
        # A job saves its checkpoint when it stops, so a file's final state
        # need not be written on its own.
        return self.job.save_job() if not final else True

    def clear(self):
        with self.job._state_lock:
            self.job.pending.pop(self.name, None)
            self.job.dirty = True


class _FileStore:
    """A CheckpointFile as a transfer's checkpoint: the state it held when
    it was opened, and the file to save to."""

    def __init__(self, checkpoint, state):
        self.checkpoint = checkpoint
        self.path = checkpoint.path
        self._state = state

    def load(self):
        return self._state

    def due(self):
        return self.checkpoint.due()

    def save(self, state, final=False, durable=False):
        return self.checkpoint.save(state, final or durable)

    def clear(self):
        self.checkpoint.clear()


def file_store(path, kind, key) -> tuple[CheckpointFile, _FileStore]:
    """Open the checkpoint at path for one transfer."""
    checkpoint = CheckpointFile(path, kind, key)
    return checkpoint, _FileStore(checkpoint, checkpoint.open())


def _make_lock(path):
    """A new lock file at path, private from the moment it exists, open for
    reading and writing; or None when another transfer made one first."""
    if not _STAGED:
        try:
            handle = _open_nofollow(
                path, os.O_RDWR | os.O_CREAT | os.O_EXCL, "lock file"
            )
        except FileExistsError:
            return None
        return _checked(handle, access.new_file_problem, "lock file")
    staging = _Staging(os.path.dirname(path), os.path.basename(path))
    try:
        handle = staging.create("lock", os.O_RDWR)
        try:
            # A link, unlike a rename, never replaces a lock file already there.
            os.link(staging.join("lock"), path)
        except FileExistsError:
            os.close(handle)
            return None
        except OSError as error:
            if error.errno not in _NO_LINKS:
                os.close(handle)
                raise
            if access.acl_supported(staging.fd):
                os.close(handle)
                raise _NotTrusted(
                    "its folder's file system keeps access control lists but has no hard links, so a new "
                    "lock file cannot be private from the moment it exists"
                ) from None
            # No hard links here, and no access control lists to inherit
            # either: a lock file made in place is as private.
            os.close(handle)
            try:
                handle = _open_nofollow(
                    path, os.O_RDWR | os.O_CREAT | os.O_EXCL, "lock file"
                )
            except FileExistsError:
                return None
            return _checked(handle, access.new_file_problem, "lock file")
        return handle
    finally:
        staging.close()


def _replace(path, data):
    """Replace path with data, so that path always holds either the old
    contents or all of the new, the file flushed to disk (its folder is
    not). The new file is private from the moment it exists (see the
    module's documentation). Returns its identity (device and inode)."""
    try:
        if _STAGED:
            staging = _Staging(os.path.dirname(path), os.path.basename(path))
            try:
                return _write_new(
                    staging.create("checkpoint", os.O_WRONLY),
                    data,
                    staging.join("checkpoint"),
                    path,
                )
            finally:
                staging.close()
        temporary = os.path.join(
            os.path.dirname(path),
            ".{}.{}.tmp".format(os.path.basename(path), uuid.uuid4().hex),
        )
        handle = os.open(
            temporary,
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | _NOFOLLOW
            | _CLOEXEC
            | _BINARY,
            0o600,
        )
        try:
            handle = _checked(
                handle, access.new_file_problem, "checkpoint file"
            )
            return _write_new(handle, data, temporary, path)
        except BaseException:
            _remove(temporary)
            raise
    except _NotTrusted as untrusted:
        raise UntrustedCheckpointError(
            errno.EACCES,
            "The checkpoint {} was not saved because {}".format(
                path, untrusted
            ),
        ) from None


def _write_new(handle, data, source, path):
    """Write data to the new file open as handle, flush it and rename it
    from source to path. Returns its identity."""
    with os.fdopen(handle, "wb") as file:
        file.write(data)
        file.flush()
        os.fsync(file.fileno())
        found = os.fstat(file.fileno())
    os.replace(source, path)
    return (found.st_dev, found.st_ino)


def sync_directory(directory):
    """Flush a directory's entries, so a file renamed into it stays there
    after a power loss. Returns False where that cannot be done: Windows
    has no such flush, and some file systems refuse to flush a directory
    (EINVAL or ENOTSUP), so there a rename is not safe from power loss.
    Raises any other failure, such as an I/O error: the entry is then not
    known to be on disk."""
    if sys.platform == "win32":
        return False
    handle = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(handle)
    except OSError as error:
        if error.errno not in _UNSUPPORTED_FLUSH:
            raise
        return False
    finally:
        os.close(handle)
    return True


# What a file system that cannot flush a directory answers.
_UNSUPPORTED_FLUSH = frozenset(
    code
    for code in (
        errno.EINVAL,
        getattr(errno, "ENOTSUP", None),
        getattr(errno, "EOPNOTSUPP", None),
    )
    if code is not None
)


def _remove(path):
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass
    except PermissionError:
        if sys.platform != "win32":
            raise


if sys.platform == "win32":
    import msvcrt

    def _lock_handle(handle):
        msvcrt.locking(handle, msvcrt.LK_NBLCK, 1)

else:
    import fcntl

    def _lock_handle(handle):
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
