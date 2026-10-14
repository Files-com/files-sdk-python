"""Downloads: reading a file's content from its signed download URL.

A download first asks Files.com for the file's download URL with
with_download_identity. When Files.com can bind the download to one
version of the file, it answers with a download identity beside the URL:
an opaque token, the version's exact size, and the headers every request
for its bytes must carry (none, or a strong If-Match). Everything the
download then does is bound to that version:

- The file is fetched in ranges, several at a time, each carrying the
  identity's headers and checked to be exactly the bytes asked for (HTTP
  206, its Content-Range, its length) of a file of the identity's size, and,
  when an ETag comes back where If-Match was sent, of that entity tag. A
  range is written only within its own bytes: one that runs long fails
  before its excess reaches the next range.
- Only the URL's origin may answer: a redirect to another origin, which
  could not enforce the version, fails the download before anything is
  sent there.
- An expired URL is renewed with expected_download_identity, which must
  give the same token and size. A URL has expired when its own signature
  says so (AWS, Files.com, Google or Azure forms), or when storage refuses
  it saying so; a 403 that does not is an error like any other. If Files.com or storage says the version
  is gone (download-identity-unavailable, or HTTP 412), a download to a
  local path starts again, once, from nothing; one to a stream that has
  already received bytes fails with InvalidRequestError.
- A checkpoint keeps the token, size and the ranges written: never a URL or
  header. Resuming renews the identity first.

Without a download identity, a download whose URL names one of Amazon S3's
general-purpose endpoints over HTTPS (_general_purpose_s3), storage that
checks If-Match against the object the URL names and answers 412 once that
object no longer has the tag, binds itself to a version from storage's own
answer, as the .NET SDK's DownloadVersion and DownloadCoordinator do. Its
first range is fetched alone, without a condition, and must be answered 206
from byte 0, unencoded, with a Content-Range naming exactly the bytes it
holds and the file's size, a Content-Length to match if it has one, and one
strong entity tag. That tag, that size and the storage resource the URL
names (its text before the query, kept as a SHA-256) are the version
(_StorageVersion). Every later request carries the tag in If-Match, follows
no redirect, and must be answered 206 with exactly the bytes asked for, of
that size, showing that very tag; a renewed URL must name the same
resource. 412, 416, another size or another tag mean the version changed,
as above. The version is the SDK's record of what storage answered, never a
download identity: none of it goes to Files.com. A checkpoint keeps the
tag, size, resource digest and ranges written; resuming gets a new URL for
the same resource and has storage confirm the version, its first byte with
If-Match, before anything written is used. Fetching the first range alone
is what binds the download, not a warm-up. A first answer of 200 (Range
ignored), 416 (such as for an empty file) or a redirect, or one without a
strong entity tag, binds nothing: the file is then read in one response,
except that a first answer without a strong tag that already holds all of
a file no larger than the range is that one response. Storage that later
answers a range of the version with the whole file, showing the version's
tag, has the ranges stopped, what they wrote discarded and the version read
whole, with If-Match; a stream that has already taken bytes fails instead.

How many ranges such a download fetches at once depends on the storage
its URL names, which chooses a policy: from one
of Amazon S3's general-purpose endpoints, the scaled S3 policy of the
shared adaptive transfer reference (see files_sdk.adaptive), from its
start of 150 ranges at once, with no named startup and no warm-up; from
other storage, such as a server that reads the file for Files.com,
max_concurrency (four by default) at once, as before. max_concurrency caps
either, and tuning (an UploadTuning) chooses otherwise: adaptive=False
keeps max_concurrency (or four), and concurrency settings choose the
configurable controller. Ranges are admitted in order: each takes room in
the TransferLimiter (a file's range the copy buffer it is written through,
a stream's the whole range, which it keeps until it is written in turn),
then a permit from the controller for its first attempt. Each attempt
holds a permit, and then one of the limiter's slots, for that attempt
alone, so a range waiting to be fetched again, or for its URL to be
renewed, holds neither, only its room, and waits for a fresh permit
behind any cooldown, ahead of new ranges. The controller measures a
range from its request until its body has arrived, less the time spent
writing it to a local file, and counts its bytes once the range is
written (or, for a stream, held whole); a 429, 503 or 504 counts when
its headers arrive, with the Retry-After it asks for, even if its body
then fails. A job's adaptive downloads share one controller for the job.

Bound to no version, as from other storage, or from S3 storage whose first
answer binds nothing, nothing shows that two responses are of the same version, however
alike their sizes or metadata, so the file is read whole, in one response,
and never assembled from several. A response cut short, or an expired URL,
starts again from the beginning; a stream that has already received bytes
fails instead. Such a download keeps no checkpoint to resume from.

Storage that names its responses with a download request ID (see
files_sdk.download_status) is asked for that request's status at two
points of such a download:

- When it answers the request for the file with an error that names the
  request (other than an expired URL, which is renewed), the error raised
  stays that answer's error, with storage's own explanation added to it (a
  note, and its download_request_status) when the status has one. A status
  that cannot be read leaves the error as it was. Storage built for the
  status protocol names only its successful answers, so this is for storage
  that names its error answers too.
- When the file arrives without a size to check it against (no
  Content-Length, or an encoded response), nothing is published until the
  status is read. A status reporting the request completed, with a count
  equal to the bytes received, lets it through. A request reported failed
  or error, completed with no count or a different count, any other state
  or none, and a status that cannot be read, such as storage's 404 for a
  request it does not know, fail the download, however few bytes arrived.
  A status still "started" shows only that storage has not recorded the
  request's outcome yet, so the status is read again, as a failed request
  is retried (up to max_network_retries more times, waiting as between
  retries), and judged by the outcome storage reports. A request still
  started after the last read fails the download too. (The Go SDK accepts a
  started status as it stands.)

A response that declares no size and names no request is used unchecked.

A response cut short in the middle of the file is not explained this way:
it is read again, as above.

A download to a local path writes into a temporary file in a private
directory of the SDK's own beside the destination (see files_sdk.localfs)
and renames it into place only once every byte has arrived, so a failed
download leaves the destination as it was. A download to a stream writes
in order, every byte exactly (see files_sdk.writing), and never replays
bytes the stream already has. A response from Files.com's web app instead
of the file fails the download before any of its bytes are used.
"""

import codecs
import collections
import concurrent.futures
import dataclasses
import hashlib
import io
import logging
import os
import re
import tempfile
import threading
import time
from typing import Any, Callable
from urllib.parse import urlsplit

import requests

from files_sdk import download_status
from files_sdk.adaptive import (
    _CONCURRENCY_FIELDS,
    _THROTTLES,
    DEFAULT_TUNING,
    SCALED_S3_MAX_CONCURRENCY,
    Controller,
    UploadTuning,
    default_max_concurrency,
)
from files_sdk.api_client import (
    _CallerError,
    _for_transfer,
    _redact_url_credentials,
)
from files_sdk.checkpoint import (
    checked_checkpoint,
    checked_pause,
    file_store,
    same_file,
    scope,
)
from files_sdk.error import (
    APIConnectionError,
    APIError,
    DeadlineExceededError,
    InvalidParameterError,
    InvalidRequestError,
    OperationCancelledError,
    TransferPausedError,
)
from files_sdk.lifetime import CancellationToken, Lifetime
from files_sdk.localfs import (
    Directory,
    LinkRefused,
    ReplacedStage,
    Stage,
    identity_of,
)
from files_sdk.upload import (
    MAX_CONCURRENCY,
    _admitted,
    _Reservation,
    _signed_url_expiry,
    checked_concurrency,
    checked_progress,
    expiring,
    refused_as_expired,
)
from files_sdk.writing import write_all
import files_sdk.util as util

MiB = 1024 * 1024

DEFAULT_MAX_CONCURRENCY = 4
"""Ranges a download bound to a version fetches at once when it does not
adapt and max_concurrency is not given: from storage other than Amazon S3,
or with UploadTuning(adaptive=False)."""

DEFAULT_RANGE_SIZE = 8 * MiB
"""How much of a file one range covers."""

# Bodies are read and written in pieces this large.
_CHUNK = 64 * 1024

# The copy buffer a range written to a file goes through: filled from the
# network before each write, and what the range holds in the limiter.
_COPY_BUFFER = 4 * _CHUNK

# UploadTuning's settings that only an upload uses: a download refuses them
# rather than ignore them.
_UPLOAD_ONLY = (
    "startup",
    "observer",
    "part_size_tiers",
    "workload_parts_per_worker",
    "min_part_size",
    "ready_parts",
    "ready_bytes",
    "unknown_initial_part_size",
    "unknown_max_part_size",
    "unknown_grow_every",
)

# The domains of Amazon S3's endpoints, and the letters and digits of a
# region's words.
_AWS_DOMAINS = (".amazonaws.com", ".amazonaws.com.cn")
_LOWERCASE = frozenset("abcdefghijklmnopqrstuvwxyz")
_DIGITS = frozenset("0123456789")

# A download that does not adapt, which pauses only as long as storage's
# Retry-After asks.
_STATIC = UploadTuning(adaptive=False, backpressure_pause=0)

_PROGRESS_INTERVAL = 0.25

# Renewals of an expired download URL, and restarts after the version went.
_MAX_RENEWALS = 2
_MAX_RESTARTS = 1

_CONTENT_RANGE = re.compile(r"bytes (\d+)-(\d+)/(\d+|\*)")

# Files.com's web app answers with this header, and an HTML page, when a
# download URL leads to it instead of to the file.
_FRONTEND_HEADER = "X-Files-Frontend-App"

# The API's error type for a download identity it cannot give or renew.
IDENTITY_UNAVAILABLE = "processing-failure/download-identity-unavailable"

# The longest download identity token accepted, and what it may contain.
_MAX_TOKEN = 4096
_TOKEN = re.compile(r"[\x21-\x7e]+")
# A strong entity tag, quoted: no W/ prefix, no wildcard, no quotes or
# control characters inside.
_STRONG_ETAG = re.compile(r'"[\x21\x23-\x7e\x80-\xff]*"')
# The strong entity tag storage's answer binds a download to: ASCII only, as
# every request then sends it in If-Match, where only ASCII is sure to go
# unchanged.
_STORAGE_ETAG = re.compile(r'"[\x21\x23-\x7e]*"')
# A storage resource, as _source_of records it.
_SOURCE = re.compile(r"sha256:[0-9a-f]{64}")


@dataclasses.dataclass(frozen=True)
class DownloadProgress:
    """How far a download has got, as passed to its progress callback.

    bytes_committed counts the bytes that arrived whole (for a stream, that
    it has taken), including those an earlier call with the same checkpoint
    received; for a download read in one response, the bytes of it written
    so far, counted from zero again if it is read again. bytes_received
    counts every byte this call read from the network, including bytes read
    again after a failure. total_bytes is the file's size, once known: for a
    download read in one response, its Content-Length from the start,
    unless the response is encoded. pinned_version says whether the
    download is bound to one version of the file: by a download identity,
    or, from Amazon S3 without one, by storage's own first answer.
    """

    path: str
    total_bytes: int | None
    bytes_committed: int
    bytes_received: int
    ranges_committed: int
    elapsed: float
    bytes_per_second: float
    pinned_version: bool = False


class _SourceChanged(Exception):
    """The version being downloaded is gone, or storage served another."""

    def __init__(self, why):
        super().__init__(why)
        self.why = why


class _Stale(Exception):
    """A URL about to be sent again has expired, by its own signature."""


class _Unbound(Exception):
    """Storage's first answer cannot bind the download to a version (see
    _Download._bind), or its renewed URL names storage that cannot: the file
    is read in one response instead."""


class _RangesIgnored(Exception):
    """Storage answered a range of the version it bound with the whole file,
    showing that version's tag: the version is read whole instead (see
    _Download._whole_version)."""


class _CallerFailure(_CallerError):
    """The caller's stream raised error while the SDK wrote to it, or the
    caller's progress callback raised it while a response was being read."""


class _Paused(Exception):
    """The download's pause token was paused."""


def _frontend_error():
    return APIConnectionError(
        "The download URL led to the Files.com web app instead of the file, so "
        "nothing was written. Download the file again; if this persists, "
        "contact Files.com support."
    )


def _changed_error(path, why=None):
    return InvalidRequestError(
        "The remote file {} changed while it was being downloaded{}, so the "
        "download was not completed. Download it again.".format(
            path, " ({})".format(why) if why else ""
        )
    )


def _unusable(problem):
    return APIConnectionError(
        "Received an unusable response from file storage: {}".format(problem)
    )


def _invalid_identity(problem):
    return APIConnectionError(
        "Received an invalid download identity from Files.com: {}".format(
            problem
        )
    )


def _whole_number(value):
    return (
        isinstance(value, int) and not isinstance(value, bool) and value >= 0
    )


def _error_type(error):
    body = getattr(error, "json_body", None)
    return body.get("type") if isinstance(body, dict) else None


@dataclasses.dataclass(frozen=True, repr=False)
class _Identity:
    """A download identity: the token, size and required headers of the one
    version of a file a download is bound to. The token is not a
    permission; nothing about it is logged."""

    token: str
    size: int
    headers: tuple[tuple[str, str], ...]

    def __repr__(self):
        return "<download identity of {} bytes>".format(self.size)

    @property
    def if_match(self):
        return dict(self.headers).get("If-Match")

    @classmethod
    def of(cls, record) -> "_Identity | None":
        """The identity in a download's record, or None when there is none.
        Any other shape raises: the download fails rather than guess what
        version it would pin."""
        value = (
            record.get("download_identity")
            if isinstance(record, dict)
            else None
        )
        if value is None:
            return None
        if (
            not isinstance(value, dict)
            or value.get("version") != 1
            or isinstance(value.get("version"), bool)
        ):
            raise _invalid_identity("it is not version 1")
        token, size, headers = (
            value.get("token"),
            value.get("size"),
            value.get("required_headers"),
        )
        if (
            not isinstance(token, str)
            or len(token) > _MAX_TOKEN
            or not _TOKEN.fullmatch(token)
        ):
            raise _invalid_identity("its token is missing or malformed")
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise _invalid_identity("its size is not a whole number of bytes")
        if not isinstance(headers, dict):
            raise _invalid_identity("its required_headers is not an object")
        if not headers:
            return cls(token, size, ())
        [(name, header)] = list(headers.items())[:1]
        if (
            len(headers) > 1
            or not isinstance(name, str)
            or name.lower() != "if-match"
        ):
            raise _invalid_identity(
                "its required_headers may hold only If-Match"
            )
        if not isinstance(header, str) or not _STRONG_ETAG.fullmatch(header):
            raise _invalid_identity(
                "its If-Match is not one strong entity tag"
            )
        return cls(token, size, (("If-Match", header),))

    def renewed(self, record) -> "_Identity":
        """The identity of a renewal of this one, which must be this one: the
        same token and size. Its headers are the renewal's."""
        other = _Identity.of(record)
        if (
            other is None
            or other.token != self.token
            or other.size != self.size
        ):
            raise _SourceChanged(
                "Files.com no longer offers the version being downloaded"
            )
        return other


@dataclasses.dataclass(frozen=True, repr=False)
class _StorageVersion:
    """The version of a file that a download Files.com gave no identity for
    is bound to by its storage's own answer to the first range (see
    _Download._bind), as the .NET SDK's DownloadVersion is: the strong entity
    tag storage sent, which every later request carries in If-Match; the
    file's size, at least 1, which that answer's Content-Range stated; and
    the storage resource the answer came from (_source_of), which the tag
    belongs to. It is the SDK's record of what storage answered, not a
    download identity: it has no token, none of it is ever sent to
    Files.com, and it grants nothing by itself."""

    etag: str
    size: int
    source: str

    def __repr__(self):
        return "<storage version of {} bytes>".format(self.size)

    @property
    def headers(self):
        return (("If-Match", self.etag),)

    @property
    def if_match(self):
        return self.etag


def _source_of(url):
    """The storage resource url names, as the .NET SDK's
    DownloadVersion.SourceOf reads it: its text before the query and
    fragment, which hold the signature and its expiry and change with every
    URL Files.com gives for the same object, as its SHA-256, so that no part
    of a URL, which may hold a credential in its path, is recorded."""
    resource = re.split(r"[?#]", url, maxsplit=1)[0]
    return "sha256:" + hashlib.sha256(resource.encode("utf-8")).hexdigest()


class _Spans:
    """The byte ranges of a file known to be written, kept merged."""

    def __init__(self, spans=()):
        self._lock = threading.Lock()
        self._spans: list[list[int]] = []
        for start, end in spans:
            self.add(start, end)

    def add(self, start, end):
        with self._lock:
            merged = []
            for span in self._spans:
                if span[1] + 1 < start or end + 1 < span[0]:
                    merged.append(span)
                else:
                    start, end = min(start, span[0]), max(end, span[1])
            merged.append([start, end])
            merged.sort()
            self._spans = merged

    def clear(self):
        with self._lock:
            self._spans = []

    def total(self):
        with self._lock:
            return sum(end - start + 1 for start, end in self._spans)

    def missing(self, size):
        """The ranges of a file of size bytes not yet written, in order."""
        with self._lock:
            spans = [list(span) for span in self._spans]
        gaps, position = [], 0
        for start, end in spans:
            if start > position:
                gaps.append((position, min(start, size) - 1))
            position = max(position, end + 1)
        if position < size:
            gaps.append((position, size - 1))
        return [gap for gap in gaps if gap[0] <= gap[1]]

    def state(self):
        with self._lock:
            return [list(span) for span in self._spans]


class _Progress:
    def __init__(self, path, callback):
        self._lock = threading.Lock()
        self._path = path
        self._callback = callback
        self._started = time.monotonic()
        self._samples: collections.deque[tuple[float, int]] = (
            collections.deque()
        )
        self._reported_at = 0.0
        self._reported = None
        self.total: int | None = None
        self.pinned = False
        self.committed = 0
        self.received = 0
        self.ranges = 0

    def add_received(self, count):
        with self._lock:
            self.received += count

    def elapsed(self):
        return time.monotonic() - self._started

    def commit(self, length, ranges=1):
        with self._lock:
            self.committed += length
            self.ranges += ranges

    def reset(self, committed=0):
        with self._lock:
            self.committed = committed
            self.ranges = 0
            # The rate starts again from here.
            self._samples.clear()

    def report(self, force=False):
        if self._callback is None:
            return
        now = time.monotonic()
        if not force and now - self._reported_at < _PROGRESS_INTERVAL:
            return
        with self._lock:
            counts = (self.committed, self.received, self.ranges)
        if counts == self._reported and not force:
            return
        self._samples.append((now, counts[0]))
        while len(self._samples) > 1 and now - self._samples[0][0] > 5:
            self._samples.popleft()
        first_time, first_committed = self._samples[0]
        rate = (
            (counts[0] - first_committed) / (now - first_time)
            if now > first_time
            else 0.0
        )
        self._reported_at, self._reported = now, counts
        self._callback(
            DownloadProgress(
                path=self._path,
                total_bytes=self.total,
                bytes_committed=counts[0],
                bytes_received=counts[1],
                ranges_committed=counts[2],
                elapsed=now - self._started,
                bytes_per_second=rate,
                pinned_version=self.pinned,
            )
        )


class _PathDestination:
    """A local file, replaced only once the whole download has arrived.

    Bytes go into a temporary file in a private directory of the SDK's own
    beside the destination (see files_sdk.localfs), which takes the place
    of the destination with the destination's permissions (or, for a new
    file, those a new file would get), without any set-user-ID,
    set-group-ID or sticky bit. A download to a path follows a symbolic
    link the path is, so the file it leads to is replaced; a folder
    download's file (confined) is refused if it is a link, and the folders
    to it are opened one at a time without following links.
    """

    ordered = False

    def __init__(self, parent, name, stage, confined):
        self.parent = parent
        self.name = name
        self.stage = stage
        self.confined = confined
        self.path = parent.join(name)
        # The device, inode, size and modification time of the file
        # published, as a job records it.
        self.published: list[int] | None = None

    @classmethod
    def create(cls, parent, name, confined):
        if confined and parent.is_link(name):
            parent.close()
            raise LinkRefused(
                "{} is a symbolic link; a folder download does not write through links".format(
                    parent.join(name)
                )
            )
        try:
            stage = Stage.create(parent, name)
        except BaseException:
            parent.close()
            raise
        return cls(parent, name, stage, confined)

    @classmethod
    def adopt(cls, parent, name, state, size, confined):
        stage = Stage.adopt(parent, state, size)
        return (
            cls(parent, name, stage, confined) if stage is not None else None
        )

    def prepare(self, size):
        self.stage.truncate(size)

    def write_at(self, offset, chunks, lifetime, limit=None):
        """Write chunks at offset, never more than limit bytes: a chunk
        that would go beyond them raises before any of it is written, so a
        response that runs long cannot overwrite the bytes after its own.
        Returns the bytes written."""
        written = 0
        for chunk in chunks:
            lifetime.check("writing the download")
            if limit is not None and written + len(chunk) > limit:
                raise requests.exceptions.ChunkedEncodingError(
                    "A response ran long"
                )
            self.stage.write_at(offset + written, chunk)
            written += len(chunk)
        return written

    def write_all(self, chunks, lifetime, limit=None):
        return self.write_at(0, chunks, lifetime, limit)

    @staticmethod
    def may_retry():
        # Every attempt rewrites its bytes from their offset.
        return True

    @staticmethod
    def exposed():
        return False

    def restart(self):
        self.stage.truncate(0)

    def sync(self):
        self.stage.sync()

    def state(self):
        return self.stage.state()

    def finish(self, lifetime):
        """Publish the download in place of the destination."""
        lifetime.check("completing the download")
        try:
            self.stage.publish(self.name, self.confined)
            found = self.parent.lstat(self.name)
            if identity_of(found) == self.stage.file_identity:
                self.published = [
                    found.st_dev,
                    found.st_ino,
                    found.st_size,
                    found.st_mtime_ns,
                ]
        except ReplacedStage as error:
            raise InvalidRequestError(
                "The download's temporary file {} was replaced by another file, so the "
                "download was not completed.".format(error)
            ) from None
        # Only once published: discard or keep, which follow a failure, still
        # reach the private directory through it if the directory has moved.
        self.parent.close()

    def discard(self):
        self.stage.discard()
        self.parent.close()

    def keep(self):
        """Leave the temporary file for a checkpoint."""
        self.stage.keep()
        self.parent.close()


class _StreamDestination:
    """A writable stream the caller owns, written in order and left open.
    It is never truncated or rewound, so a failed download can leave part of
    the content in it; every byte it took is counted, and none is sent to it
    twice."""

    ordered = True

    def __init__(self, stream, text):
        if not callable(getattr(stream, "write", None)):
            raise InvalidParameterError(
                "The download destination must be a writable stream"
            )
        self.stream = stream
        self.decoder = (
            codecs.getincrementaldecoder("utf-8")() if text else None
        )
        # Bytes the stream has taken (for text, bytes decoded into what it
        # took), and whether it has taken anything at all.
        self.written = 0
        self.touched = False

    def prepare(self, size):
        pass

    def _write(self, piece):
        try:
            return self.stream.write(piece)
        except Exception as error:
            # Carried unchanged through the request machinery, which would
            # otherwise take a network-looking failure of the caller's own
            # stream for the download's and retry it.
            raise _CallerFailure(error) from None

    def write(self, data, check=None, delivered=None):
        """Write data exactly, in pieces of plain bytes, as the stream would
        get them from a response. check runs before each write after the
        first; delivered hears each count of bytes the stream took."""

        def took(count):
            self.touched = True

        for offset in range(0, len(data), _CHUNK):
            if offset and check is not None:
                check()
            piece = bytes(data[offset : offset + _CHUNK])
            if self.decoder is not None:
                text = self.decoder.decode(piece)
                if text:
                    write_all(self.stream, text, check, took, self._write)
                self.written += len(piece)
                if delivered is not None:
                    delivered(len(piece))
                continue

            def counted(count):
                self.touched = True
                self.written += count
                if delivered is not None:
                    delivered(count)

            write_all(self.stream, piece, check, counted, self._write)

    def write_all(self, chunks, lifetime, limit=None):
        def check():
            lifetime.check("writing the download")

        total = 0
        for chunk in chunks:
            if total:
                check()
            if limit is not None and total + len(chunk) > limit:
                # Checked before the stream sees any of it.
                raise requests.exceptions.ChunkedEncodingError(
                    "A response ran long"
                )
            self.write(chunk, check)
            total += len(chunk)
        return total

    def may_retry(self):
        # Bytes the caller's stream has taken cannot be taken back.
        return not self.touched

    def exposed(self):
        return self.touched

    def restart(self):
        if self.touched:
            raise AssertionError("a stream that took bytes is never restarted")

    def sync(self):
        flush = getattr(self.stream, "flush", None)
        if callable(flush):
            flush()

    def finish(self, lifetime):
        if self.decoder is not None:
            text = self.decoder.decode(b"", final=True)
            if text:
                write_all(self.stream, text, None, None, self._write)

    def discard(self):
        pass

    def keep(self):
        pass


class _Download:
    """One download, from its first request to the last byte written. See
    the module docstring."""

    def __init__(
        self,
        operation,
        file,
        destination,
        max_concurrency,
        progress,
        range_size,
        pause=None,
        tuning=None,
        scope=None,
    ):
        from files_sdk.api import Operation

        self.operation = operation
        self.file = file
        self.destination = destination
        # The caller's cap on the ranges in progress, or None; its tuning,
        # or None; and a job's DownloadScope, for one shared controller.
        self.max_concurrency = max_concurrency
        self.tuning = tuning
        self.scope = scope
        # What admits the ranges' attempts, once the download fetches ranges.
        self.controller: Controller | None = None
        self.settings: Any = None
        self.range_size = range_size
        self.limiter = operation.context.transfer_limiter
        self.progress = _Progress(file.path, progress)
        self.pause = pause
        self.store: Any = None
        self._operation_class = Operation
        self.uri: str | None = None
        # The version the download is bound to: Files.com's download
        # identity, or, without one, the version storage's first answer bound
        # it to (_StorageVersion); None while it is bound to none.
        self.identity: _Identity | _StorageVersion | None = None
        # The version a checkpoint recorded, renewed (an identity) or
        # confirmed by storage (a storage version) before anything else.
        self.expected: _Identity | _StorageVersion | None = None
        # Whether the first range is being fetched to bind the download (_bind).
        self.establishing = False
        # The bytes written: at their offsets in a file, or, for a stream,
        # from its start up to next_start.
        self.done = _Spans()
        self.next_start = 0
        self.resumed = False
        # Whether bytes were written since the checkpoint was last saved.
        self.dirty = False
        self.renewals = 0
        self.renewing = threading.Lock()
        # Which URL self.uri is: 0 for the file's own, then one more for each
        # Files.com gives. One it gave is tried once as given; one that was
        # tried is renewed before it is sent again once it has expired.
        self.issue = 0
        self.tried: set[int] = set()
        self.mode = "ranges"
        self.restarts = 0
        self._start_attempt()

    def resume(self, expected, spans):
        """Continue from what a checkpoint recorded: the version (an
        identity's token and size, or a storage version) and the ranges
        written."""
        self.expected = expected
        for start, end in spans:
            self.done.add(start, end)
        if self.destination.ordered and spans:
            self.next_start = spans[0][1] + 1
            # The stream has the earlier call's bytes of this version, so it
            # can never start again with another.
            self.destination.touched = True
        self.resumed = bool(spans)
        self.progress.reset(self.done.total())
        self.progress.total = expected.size if expected is not None else None

    def _start_attempt(self):
        """A stop signal of its own for this attempt's requests, which the
        operation stopping or the attempt failing cancels."""
        self.stopping = CancellationToken()
        lifetime = self.operation.lifetime
        self.lifetime = Lifetime(
            lifetime.closing, self.stopping, lifetime.deadline
        )
        self.workers = self._operation_class(
            None, self.lifetime, _state=self.operation._state
        )
        if lifetime.stopped:
            self.stopping.cancel()
        self.in_flight: dict[
            concurrent.futures.Future[Any], tuple[int, _Reservation]
        ] = {}
        # A stream's ranges that arrived ahead of their turn.
        self.arrived: dict[int, tuple[bytearray, _Reservation]] = {}

    def _check_lifetime(self):
        self.operation.lifetime.check("writing the download")

    def run(self):
        # The current attempt's signal, whichever attempt that is.
        stop_watching = self.operation.lifetime.watch(
            lambda: self.stopping.cancel()
        )
        try:
            while True:
                try:
                    self._download()
                    break
                except _SourceChanged as changed:
                    # A stream that took bytes has part of the old version.
                    if (
                        self.destination.exposed()
                        or self.restarts >= _MAX_RESTARTS
                    ):
                        raise _changed_error(
                            self.file.path, changed.why
                        ) from None
                    self.restarts += 1
                    util.log_info(
                        "Download starting again",
                        reason=changed.why,
                        path=self.file.path,
                    )
                    self._restart()
            self.destination.finish(self.operation.lifetime)
            if self.store is not None:
                self.store.clear()
            self.progress.report(force=True)
            util.log_info(
                "Download finished",
                size=self.progress.committed,
                bytes_received=self.progress.received,
                mode=self.mode,
                pinned_version=self.identity is not None,
                bound_by=(
                    "storage"
                    if isinstance(self.identity, _StorageVersion)
                    else "identity" if self.identity is not None else None
                ),
                concurrency=self._concurrency(),
                peak_target=(
                    self.controller.stats["peak"]
                    if self.controller is not None
                    else None
                ),
                ranges=self.progress.ranges,
                resumed=self.resumed,
                restarts=self.restarts,
                renewals=self.renewals,
                seconds=round(self.progress.elapsed(), 3),
            )
            return self.file
        except _Paused:
            store = self.store
            self._save_state(final=True)
            raise TransferPausedError(
                "The download of {} was paused. Download it again with the same "
                "checkpoint to resume it.".format(self.file.path),
                checkpoint=store.path if store is not None else None,
            ) from None
        except BaseException as error:
            caller = error.error if isinstance(error, _CallerFailure) else None
            if self.store is None:
                self.destination.discard()
            else:
                self._save_quietly(caller or error)
            if caller is not None:
                # The caller's own exception, as their stream raised it.
                raise caller from None
            lifetime = self.operation.lifetime
            if lifetime.stopped and isinstance(
                error, (OperationCancelledError, DeadlineExceededError)
            ):
                raise lifetime.stopped_error("downloading") from None
            raise
        finally:
            stop_watching()

    def _restart(self):
        """Start again from nothing, with a new negotiation."""
        self.uri = None
        self.identity = None
        self.expected = None
        self.done.clear()
        self.next_start = 0
        self.progress.reset()
        self.destination.restart()
        self._start_attempt()

    # Negotiating and renewing the URL.

    def _lookup(self, operation, params):
        """Ask Files.com for the file's download, with params. Returns its
        URL and the response's record, whose attributes the file takes, with
        the client and site the request ended at."""
        from files_sdk.api import path_value
        from files_sdk.models.file import File

        path = str(self.file.path)
        # As the generated download operation sends it.
        response = operation.request(
            "GET",
            "/files/{}".format(path_value(path)),
            {"path": path, **params},
        )
        record = response.data
        fresh = operation.decode_model(response, File)
        self.file.set_attributes(
            {**self.file.get_attributes(), **fresh.get_attributes()}
        )
        # As a relocated operation leaves them, for the file's later operations.
        self.file._context = fresh._context
        uri = record.get("download_uri") if isinstance(record, dict) else None
        if not isinstance(uri, str) or not uri:
            raise InvalidRequestError(
                "Files.com gave no download URL for {}".format(self.file.path)
            )
        # The identity that came with the URL, for the file's later
        # downloads, whether or not the File model has an attribute for it.
        setattr(
            self.file,
            "_files_sdk_download",
            (uri, record.get("download_identity")),
        )
        return uri, record

    def _negotiate(self, operation):
        """A URL and identity for the file as it is now: with an identity
        where Files.com can give one, else without."""
        try:
            uri, record = self._lookup(
                operation, {"with_download_identity": True}
            )
        except APIError as error:
            if _error_type(error) != IDENTITY_UNAVAILABLE:
                raise
            util.log_info(
                "Download without a download identity",
                reason="Files.com cannot identify the version",
                path=self.file.path,
            )
            uri, _record = self._lookup(operation, {})
            return uri, None
        return uri, _Identity.of(record)

    def _renewal(self, operation, identity):
        """A new URL for the version identity names, with the same identity."""
        try:
            uri, record = self._lookup(
                operation,
                {
                    "with_download_identity": True,
                    "expected_download_identity": identity.token,
                },
            )
        except APIError as error:
            if (
                error.http_status == 412
                or _error_type(error) == IDENTITY_UNAVAILABLE
            ):
                raise _SourceChanged(
                    "Files.com no longer offers the version being downloaded"
                ) from None
            raise
        return uri, identity.renewed(record)

    def _storage_renewal(self, operation, version):
        """A new URL for the version storage bound the download to: the
        file's download URL as Files.com gives it now, asked for as any
        download without an identity asks, which must name the storage
        resource the version came from, at storage that can bind it. A URL
        for another resource is not shown to be that version, whatever entity
        tag it would serve, so the version is then gone. Nothing of the
        version is sent to Files.com."""
        uri, _record = self._lookup(operation, {})
        if not _general_purpose_s3(uri) or _source_of(uri) != version.source:
            raise _SourceChanged(
                "Files.com gave a URL for another storage resource than the version's"
            )
        return uri

    def _begin(self):
        """The URL and identity to start with: those a checkpoint's version
        renews to, the file's own (at first), or a new negotiation's. A
        checkpoint's storage version is confirmed by storage before anything
        else (_confirm_version)."""
        if isinstance(self.expected, _StorageVersion):
            self.uri = self._storage_renewal(self.operation, self.expected)
            self.identity = self.expected
            self.issue += 1
            self._confirm_version()
            return
        if self.expected is not None:
            self.uri, self.identity = self._renewal(
                self.operation, self.expected
            )
            self.issue += 1
            return
        own = getattr(self.file, "download_uri", None)
        if self.restarts == 0 and isinstance(own, str) and own:
            kept = getattr(self.file, "_files_sdk_download", None)
            value = (
                kept[1]
                if kept is not None and kept[0] == own
                else getattr(self.file, "download_identity", None)
            )
            self.uri = own
            self.identity = _Identity.of({"download_identity": value})
            return
        self.uri, self.identity = self._negotiate(self.operation)
        self.issue += 1

    def _resolve(self, operation, stale):
        """A new URL after the URL numbered stale proved expired, unless
        another range renewed it already; None once no more renewals are
        allowed. An identified download renews its version, and one storage
        bound gets a URL for the version's resource; one bound to no version
        renews to the file as it is now, which its one whole response then
        reads from the start. (A renewed URL can be the same text.)"""
        with self.renewing:
            if self.issue != stale:
                return self.uri
            if self.renewals >= _MAX_RENEWALS:
                return None
            self.renewals += 1
            if self.identity is None:
                self.uri, _record = self._lookup(operation, {})
            elif isinstance(self.identity, _StorageVersion):
                self.uri = self._storage_renewal(operation, self.identity)
            else:
                self.uri, self.identity = self._renewal(
                    operation, self.identity
                )
            self.issue += 1
            return self.uri

    def _request(
        self,
        operation,
        headers,
        consume,
        may_retry=None,
        attempts=None,
        size: int | Callable[[], int] = 0,
    ):
        """GET the download URL with headers and the identity's required
        headers, handing each response to consume. An expired URL is renewed,
        at most twice in all: before it is sent again once its own signature
        says it has expired (a URL Files.com has just given is tried once, as
        given), and after storage refuses it saying so, or with a 403 once
        that time has come. The URL is always sent exactly as given.

        attempts, if given, is what each attempt at a range holds while it
        runs (see _Attempts); size is the bytes an attempt that succeeds
        reports to the controller, or a function giving them once consume has
        validated what arrived. It holds them from just before its request is
        built until it ends, the controller's permit and then a slot in the
        TransferLimiter. A retry's wait and a renewal of the URL hold
        neither: the attempt after them waits for a fresh permit, behind any
        cooldown and ahead of new ranges, and then for a slot. The
        controller hears the attempt go to the network, a throttle its
        response's headers carry (even if the body then fails), and how it
        ended; consume tells it when the body has arrived.

        The first range of a download storage's answer is to bind
        (establishing), and every request of one it bound, is answered only
        by the URL's own resource: a redirect is its answer, not followed."""
        while True:
            uri, identity, issue = self.uri, self.identity, self.issue
            assert uri is not None
            establishing = self.establishing and identity is None
            expires = _signed_url_expiry(uri)
            sent = dict(headers)
            if identity is not None:
                sent.update(identity.headers)

            def build():
                if self._stale(issue, expires):
                    raise _Stale()
                if establishing and not _general_purpose_s3(uri):
                    # Renewed to a URL for storage that cannot bind the download.
                    raise _Unbound()
                if attempts is not None:
                    attempts.start()
                request = requests.Request(
                    "GET",
                    uri,
                    headers=operation.api_client._transfer_headers(sent),
                )
                if establishing or isinstance(identity, _StorageVersion):
                    request.files_no_redirect = True  # type: ignore[attr-defined]
                elif identity is not None:
                    # Only the URL's origin is approved to serve this version,
                    # so a redirect to another is refused before it is
                    # followed: neither the If-Match nor the read goes where
                    # the version cannot be enforced.
                    request.files_same_origin = True  # type: ignore[attr-defined]
                return request

            # The last answer storage gave this URL: its status and the
            # download request it names.
            answer = {}

            def answered(response, uri=uri, identity=identity, answer=answer):
                answer["status"] = response.status_code
                answer["request_id"] = download_status.request_id_of(response)
                consume(response, uri, identity)

            hooks: dict[str, Any] = {}
            if attempts is not None:

                def headers_arrived(status, retry_after):
                    if status in _THROTTLES:
                        # Storage pushed back: that counts now, before the
                        # body, and the attempt is no longer on the network.
                        attempts.permit.answered(status, retry_after)

                def ended(status, retry_after):
                    attempts.end(
                        status, retry_after, size() if callable(size) else size
                    )

                hooks = {
                    "on_send": attempts.permit.begin,
                    "on_headers": headers_arrived,
                    "observe": ended,
                    "on_abandon": attempts.release,
                }
            try:
                return operation.api_client._execute(
                    operation,
                    build,
                    transfer=True,
                    consume=answered,
                    may_retry=may_retry,
                    **hooks,
                )
            except _Stale:
                # Nothing was sent with it; without a renewal left, it is
                # sent as it is next time. Renewing is not an attempt, so
                # it holds neither a permit nor a slot.
                if attempts is not None:
                    attempts.release()
                self._resolve(operation, issue)
            except APIError as error:
                if error.http_status == 412 and identity is not None:
                    raise _SourceChanged(
                        "storage refused the version being downloaded"
                    ) from None
                if error.http_status == 416 and isinstance(
                    identity, _StorageVersion
                ):
                    raise _SourceChanged(
                        "storage has fewer bytes than the version (HTTP 416)"
                    ) from None
                if not refused_as_expired(error, expires):
                    if identity is None and not establishing:
                        self._explain(operation, error, uri, answer)
                    raise self._named(error)
                if identity is None and not self.destination.may_retry():
                    raise self._named(
                        error
                    )  # Its one response already reached the stream.
                if self._resolve(operation, issue) is None:
                    raise self._named(error)

    def _named(self, error):
        """error, storage's refusal of this download's URL, naming the file
        it was for."""
        return _for_transfer(
            error, "the download of {}".format(self.file.path)
        )

    def _stale(self, issue, expires):
        """Whether the URL numbered issue, about to be sent, has expired and
        is to be renewed first: never on the first try of a URL Files.com
        has just given, nor once no renewal is left. Otherwise records the
        try."""
        first_try = issue > 0 and issue not in self.tried
        if (
            expiring(expires)
            and not first_try
            and self.renewals < _MAX_RENEWALS
        ):
            return True
        self.tried.add(issue)
        return False

    # Storage's status of a download request (see files_sdk.download_status).

    def _explain(self, operation, error, uri, answer):
        """Add storage's own explanation to error, its error answer to a
        request for the whole file at uri, when that answer named its
        download request and the request's status has an error. (Storage
        built for the status protocol names only successful answers, so this
        is for storage that also names its error answers, which the Go SDK
        reads the same way.) error stays the error raised: nothing that
        happens reading the status, a cancellation or a 404 for a request
        storage does not know included, replaces it."""
        request_id = answer.get("request_id")
        if request_id is None or answer.get("status") != error.http_status:
            return
        try:
            status = download_status.read(operation, uri, request_id)
        except Exception as problem:
            util.log_info(
                "Download request status unavailable",
                reason=type(problem).__name__,
                path=self.file.path,
            )
            return
        if status.error is None:
            return
        error.download_request_status = status
        error.add_note(
            "File storage's status of this download request: "
            + _redact_url_credentials(status.explanation())
        )

    def _confirm(self, uri, request_id, received):
        """Raise unless storage's status of the download request
        request_id lets received bytes through, for a file whose response
        declared no size to check them against. A status reporting the
        request completed, with a count equal to received, confirms them,
        however few. Failed or error, completed with no count or a different
        count, any other state or none, and a status that cannot be read,
        storage's 404 for a request it does not know included, raise. A
        status still "started" is read again, up to max_network_retries more
        times after the waits between API request retries, until it reports
        another state, which is then judged as above; one still started
        after the last read raises too. The waits end at once, raising, when
        the operation is cancelled, closed or out of time. (The Go SDK
        accepts a started status as it stands; that shows nothing of the
        bytes.)"""
        path = self.file.path
        taken = (
            " The stream has already received them."
            if self.destination.exposed()
            else " Nothing was written."
        )

        def unconfirmed(why, status=None):
            error = APIConnectionError(
                "The download of {} could not be confirmed: its response declared no size, and file "
                "storage's status of the download request {}.{}".format(
                    path, why, taken
                )
            )
            error.download_request_status = status
            return error

        context = self.operation.context
        retries = 0
        while True:
            try:
                status = download_status.read(self.operation, uri, request_id)
            except (OperationCancelledError, DeadlineExceededError):
                raise
            except Exception as problem:
                raise unconfirmed(
                    "could not be read ({})".format(
                        download_status.reason(problem)
                    )
                ) from problem
            if status.status != "started":
                break
            # Storage has not recorded the request's outcome yet. The Go SDK
            # trusts what arrived at this point; this reads the status again,
            # as a request is retried, and without an outcome confirms nothing.
            if retries >= context.max_network_retries:
                reads = retries + 1
                raise unconfirmed(
                    "still reports the request started after {} read{}".format(
                        reads, "" if reads == 1 else "s"
                    ),
                    status,
                )
            # The backoff between retries of an API request.
            wait = self.operation.api_client._retry_delay(
                context, retries, None, transfer=False
            )
            retries += 1
            util.log_info(
                "Waiting for the download request status", path=path, wait=wait
            )
            self.operation.lifetime.sleep(
                wait, "waiting for the download request status"
            )
        if status.failed:
            explanation = _redact_url_credentials(status.explanation())
            error = APIError(
                "File storage reports that the download of {} did not complete: {}.{}".format(
                    path, explanation, taken
                ),
                http_status=status.http_code,
            )
            error.download_request_status = status
            raise error
        if status.status != "completed":
            raise unconfirmed(
                "does not report that the request completed", status
            )
        elif status.bytes_transferred is None:
            raise unconfirmed("reports no count of the bytes it read", status)
        elif status.bytes_transferred != received:
            error = APIConnectionError(
                "The download of {} ended after {} bytes, but file storage's status of the download request "
                "reports {} bytes transferred.{}".format(
                    path, received, status.bytes_transferred, taken
                )
            )
            error.download_request_status = status
            raise error
        util.log_info(
            "Download request status",
            path=path,
            status=status.status,
            size=received,
            bytes_transferred=status.bytes_transferred,
        )

    # Checking responses.

    @staticmethod
    def _check_frontend(response):
        if _FRONTEND_HEADER in response.headers:
            raise _frontend_error()

    @staticmethod
    def _encoded(response):
        return response.headers.get(
            "Content-Encoding", "identity"
        ).strip().lower() not in ("identity", "")

    def _check_version(self, response, uri, identity):
        """Raise unless an identified response is of that version: with an
        If-Match, an ETag that comes back must be that very strong entity
        tag. A response without one is taken, as the contract allows: it
        came from the URL's own origin, which the If-Match went to and which
        enforces it, since a redirect elsewhere is never followed. A version
        storage bound shows its tag in every answer, as it did in the one
        that bound it, so one without it cannot be shown to be that version."""
        if isinstance(identity, _StorageVersion):
            etag = response.headers.get("ETag")
            if etag is None:
                raise _unusable(
                    "storage answered without the entity tag the download's version was asked to match"
                )
            if etag != identity.etag:
                raise _SourceChanged(
                    "storage served another version (its ETag differs)"
                )
            return
        if identity is None or identity.if_match is None:
            return
        etag = response.headers.get("ETag")
        if etag is None:
            return
        if not _STRONG_ETAG.fullmatch(etag):
            raise _unusable(
                "storage showed a weak or malformed ETag for the download's version"
            )
        if etag != identity.if_match:
            raise _SourceChanged(
                "storage served another version (its ETag differs)"
            )

    def _check_range(self, response, uri, identity, start, end):
        """Raise unless response is exactly bytes start-end of the version."""
        if (
            isinstance(identity, _StorageVersion)
            and response.status_code != 206
        ):
            # Such as a redirect, which a request bound by storage does not
            # follow. (Its whole file, from storage that ignores Range, is
            # handled before this is asked.)
            raise _unusable(
                "a request for bytes {}-{} was answered with HTTP {}".format(
                    start, end, response.status_code
                )
            )
        self._check_version(response, uri, identity)
        if response.status_code != 206:
            raise _unusable(
                "a request for bytes {}-{} was answered with HTTP {}".format(
                    start, end, response.status_code
                )
            )
        if self._encoded(response):
            raise _unusable("a range came encoded")
        match = _CONTENT_RANGE.fullmatch(
            response.headers.get("Content-Range", "").strip()
        )
        if not match or match.group(3) == "*":
            raise _unusable("a range response had no usable Content-Range")
        got_start, got_end, got_total = (
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
        )
        if got_total != identity.size:
            raise _SourceChanged(
                "storage sent part of a file of {} bytes, not of the version's {}".format(
                    got_total, identity.size
                )
            )
        if got_start != start or got_end != end:
            raise _unusable(
                "a range response covered other bytes than asked for"
            )
        length = response.headers.get("Content-Length")
        if length is not None and int(length) != end - start + 1:
            raise _unusable("a range response had the wrong Content-Length")

    def _bind(self, response, uri, end):
        """Bind a download Files.com gave no identity to a version from
        storage's answer to its first range, bytes 0 to end, as the .NET SDK
        does (DownloadCoordinator.Establish): a 206 from byte 0, unencoded,
        whose Content-Range states the file's size, at least 1, and names
        exactly the bytes it holds, the range asked for or, for a smaller
        file, all of it, with a Content-Length to match if it has one. Its
        one strong entity tag, that size and the storage resource uri names
        are the version, whose tag every later request carries. Returns the
        last byte the answer holds. An answer without one strong entity tag
        binds nothing: for a file larger than the range it raises _Unbound,
        since nothing would show that the file's other bytes are of the same
        version, and the file is read in one response instead; for a file no
        larger than the range, as in .NET, the answer is the whole file, the
        download's one response, unbound, and the destination is prepared
        for exactly its size before it is written, so nothing an earlier
        attempt wrote of a longer file remains after it. Without a
        Content-Length, that answer must also have the size Files.com stated
        for the file, if it stated one, as a whole answer must: its own
        Content-Range does not stand in for that."""
        if response.status_code != 206:
            raise _unusable(
                "the first range was answered with HTTP {}".format(
                    response.status_code
                )
            )
        if self._encoded(response):
            raise _unusable("a range came encoded")
        match = _CONTENT_RANGE.fullmatch(
            response.headers.get("Content-Range", "").strip()
        )
        if not match or match.group(3) == "*" or int(match.group(3)) < 1:
            raise _unusable(
                "the first range's answer had no Content-Range stating the file's size"
            )
        size = int(match.group(3))
        last = min(end, size - 1)
        if int(match.group(1)) != 0 or int(match.group(2)) != last:
            raise _unusable(
                "a range response covered other bytes than asked for"
            )
        length = response.headers.get("Content-Length")
        if length is not None and int(length) != last + 1:
            raise _unusable("a range response had the wrong Content-Length")
        etag = response.headers.get("ETag")
        if etag is None or not _STORAGE_ETAG.fullmatch(etag):
            if last + 1 < size:
                raise _Unbound()
            stated = getattr(self.file, "size", None)
            if length is None and _whole_number(stated) and stated != size:
                raise _unusable(
                    "the first range's answer held the {} bytes its Content-Range named as the whole file, without "
                    "a Content-Length, not the {} bytes Files.com stated for the file".format(
                        size, stated
                    )
                )
            # Not of a version: whatever an earlier attempt's answer bound.
            self.identity = None
            self.progress.pinned = False
            self.progress.total = size
            # The file is exactly this answer: an earlier attempt, cut short,
            # may have written more of a longer file than this one writes
            # over. (A stream's attempts write only to their own buffer.)
            self.destination.prepare(size)
            return last
        self.identity = _StorageVersion(etag, size, _source_of(uri))
        self.progress.total = size
        self.progress.pinned = True
        return last

    def _confirm_version(self):
        """Have storage confirm the version a checkpoint recorded, which its
        answer had bound, before anything written for it is used, as the
        .NET SDK does (DownloadCoordinator.ConfirmAsync): its first byte,
        asked for with its entity tag in If-Match, must come back as exactly
        that byte of the version (_check_range), or as the whole file from
        storage that now ignores Range, showing the version's tag and, if it
        declares one, the version's length, whose body is not read. 412,
        416, another size or another entity tag show it gone
        (_SourceChanged); any other failure is the download's. As there,
        each attempt holds a request slot in the TransferLimiter, from just
        before its request is built until it ends, and the controller
        neither admits nor measures it."""

        def consume(response, uri, identity):
            self._check_frontend(response)
            if response.status_code >= 400:
                response.content
                return
            if response.status_code == 200:
                self._check_version(response, uri, identity)
                length = response.headers.get("Content-Length")
                if length is not None and int(length) != identity.size:
                    raise _SourceChanged(
                        "storage has {} bytes where the version has {}".format(
                            length, identity.size
                        )
                    )
                # Confirmed; the ranges will find that Range is ignored.
                response.close()
                return
            self._check_range(response, uri, identity, 0, 0)
            self._read_range(response, 1)

        attempts = _Attempts(_Unadmitted(), self.limiter, self.lifetime)
        try:
            self._request(
                self.operation,
                {"Range": "bytes=0-0", "Accept-Encoding": "identity"},
                consume,
                may_retry=lambda: True,
                attempts=attempts,
                size=1,
            )
        finally:
            attempts.release()

    # The whole download.

    def _check_pause(self):
        if self.pause is not None and self.pause.paused:
            raise _Paused()

    def _download(self):
        self._check_pause()
        if self.uri is None:
            self._begin()
        try:
            if (
                self.identity is None
                and _general_purpose_s3(self.uri)
                and self._establish()
            ):
                return
            identity = self.identity
            self.progress.pinned = identity is not None
            if identity is None:
                self.mode = "whole"
                self._whole()
                return
            self.mode = "ranges"
            self.progress.total = identity.size
            self.destination.prepare(identity.size)
            if identity.size == 0:
                self._empty()
                return
            ranges = [
                (offset, min(offset + self.range_size, gap_end + 1) - 1)
                for gap_start, gap_end in self.done.missing(identity.size)
                for offset in range(gap_start, gap_end + 1, self.range_size)
            ]
            self._save_state()
            if ranges:
                self._fetch(ranges)
        except _RangesIgnored:
            self._whole_version()

    def _establish(self):
        """Bind a download Files.com gave no identity to a version from its
        storage's own answer, where its URL names storage that can bind it
        (_general_purpose_s3). Its first range is fetched alone, without a
        condition, as any range is, within the limiter and the controller,
        and storage's answer binds the download (_bind), which then fetches
        the rest of the ranges as a download with an identity does. Fetching
        that range alone is what binding takes, not a warm-up: the controller
        starts where its policy says. When the answer binds nothing, nothing
        it held is used, and the file is read in one response instead; when
        it is already the whole of a file no larger than the range, unbound,
        it is the download's one response. Returns whether that answer was
        all of the download."""
        self.mode = "ranges"
        self.establishing = True
        try:
            self._fetch([(0, self.range_size - 1)])
        except _Unbound:
            self._start_attempt()
            self.controller = self.settings = None
            util.log_info(
                "Download in one response",
                reason="storage's first answer binds no version",
                path=self.file.path,
            )
            return False
        finally:
            self.establishing = False
        return self.identity is None

    def _whole_version(self):
        """Read the version storage bound in one response, once storage has
        answered a request for a range of it with the whole file, its tag
        shown, as the .NET SDK does (FetchWholeAsync, bound): the ranges in
        progress have been stopped and have given back what they held, and
        what they wrote is discarded. The request carries the version's
        If-Match, follows no redirect, and must be answered 200 with the
        version's tag, unencoded, with exactly the version's size. As there,
        it holds room in the TransferLimiter for the copy buffer it goes
        through, and each attempt a request slot; the controller neither
        admits nor measures it. A stream that has already taken bytes cannot
        take the file again, so the download fails instead."""
        if self.destination.exposed():
            raise _unusable(
                "storage answered a range with the whole file after part of the file had reached the stream"
            )
        util.log_info(
            "Download in one response",
            reason="storage ignores Range",
            path=self.file.path,
        )
        self._start_attempt()
        self.done.clear()
        self.next_start = 0
        self.destination.restart()
        self.progress.reset()
        self.mode = "whole"
        version = self.identity
        assert isinstance(version, _StorageVersion)
        size = version.size

        def consume(response, uri, identity):
            self._check_frontend(response)
            if response.status_code >= 400:
                response.content
                return
            if response.status_code != 200:
                raise _unusable(
                    "a request for the whole version was answered with HTTP {}".format(
                        response.status_code
                    )
                )
            self._check_version(response, uri, identity)
            if self._encoded(response):
                raise _unusable("the whole version came encoded")
            declared = response.headers.get("Content-Length")
            if declared is not None and int(declared) != size:
                raise _SourceChanged(
                    "storage sent {} bytes where the version has {}".format(
                        declared, size
                    )
                )
            self.destination.prepare(0)
            self.progress.reset()
            written = self.destination.write_all(
                self._reported(self._chunks(response)), self.lifetime, size
            )
            if written != size:
                raise requests.exceptions.ChunkedEncodingError(
                    "The download ended early"
                )
            self.done.add(0, size - 1)
            self.next_start = size
            self.dirty = True
            self.progress.commit(
                0
            )  # The response, as the download's one range.

        room = _admitted(
            self.limiter, min(_COPY_BUFFER, size), self.lifetime, slot=False
        )
        attempts = _Attempts(_Unadmitted(), self.limiter, self.lifetime)
        try:
            self._request(
                self.operation,
                {"Accept-Encoding": "identity"},
                consume,
                may_retry=self.destination.may_retry,
                attempts=attempts,
                size=size,
            )
        finally:
            attempts.release()
            room.release()

    def _whole(self):
        """Read the file in one response, decoded as it came, writing it from
        the start (again, after a response cut short, where the destination
        can take it)."""

        # The response whose bytes storage's status is to confirm.
        unconfirmed = {}

        def consume(response, uri, identity):
            self._check_frontend(response)
            if response.status_code >= 400:
                response.content  # The error, for handle_error_response.
                return
            if response.status_code != 200:
                # Part of the file, or no file, where all of it was asked
                # for: never taken for the whole of a shorter file.
                raise _unusable(
                    "a request for the whole file was answered with HTTP {}".format(
                        response.status_code
                    )
                )
            unconfirmed.clear()
            self.destination.prepare(0)
            self.progress.reset()
            declared = response.headers.get("Content-Length")
            limit = (
                int(declared)
                if declared is not None and not self._encoded(response)
                else None
            )
            # The size, before any of it arrives; an encoded response's is
            # known only once it is decoded.
            self.progress.total = limit
            written = self.destination.write_all(
                self._reported(self._chunks(response)), self.lifetime, limit
            )
            if limit is not None and written != limit:
                raise requests.exceptions.ChunkedEncodingError(
                    "The download ended early"
                )
            request_id = download_status.request_id_of(response)
            if limit is None and request_id is not None:
                unconfirmed.update(
                    uri=uri, request_id=request_id, received=written
                )
            self.progress.total = written
            self.progress.commit(
                0
            )  # The response, as the download's one range.

        self._request(
            self.operation, {}, consume, may_retry=self.destination.may_retry
        )
        if unconfirmed:
            self._confirm(
                unconfirmed["uri"],
                unconfirmed["request_id"],
                unconfirmed["received"],
            )

    def _empty(self):
        """Fetch an empty version: one request for the whole of it, whose
        answer must be of that version and have no bytes."""

        def consume(response, uri, identity):
            self._check_frontend(response)
            if response.status_code >= 400:
                response.content
                return
            self._check_version(response, uri, identity)
            if response.status_code != 200:
                raise _unusable(
                    "a request for an empty file was answered with HTTP {}".format(
                        response.status_code
                    )
                )
            if response.content:
                raise _SourceChanged(
                    "storage sent bytes for a version of no bytes"
                )
            self.progress.commit(0)

        self._request(
            self.operation,
            {"Accept-Encoding": "identity"},
            consume,
            may_retry=lambda: True,
        )

    def _chunks(self, response):
        # A range is never encoded, so only a whole answer is ever decoded.
        offset = 0
        for chunk in response.iter_content(_CHUNK):
            self.lifetime.check("downloading")
            self.progress.add_received(len(chunk))
            if util.enabled(logging.DEBUG):
                util.log_debug("Download body", offset=offset, data=chunk)
            offset += len(chunk)
            yield chunk

    def _reported(self, chunks):
        """chunks, each counted as committed once the destination has taken
        it, with progress reported as they go, on this, the calling thread.
        The callback's exception is the caller's, never the response's."""
        for chunk in chunks:
            yield chunk
            self.progress.commit(len(chunk), ranges=0)
            try:
                self.progress.report()
            except Exception as error:
                raise _CallerFailure(error) from None

    def _take_range(self, start, end, response, buffer, permit=None):
        """Take one range's body, which must be exactly its length: written
        at its offset through buffer, a file's copy buffer, or, for a
        stream, read into buffer, all of it, to be written in turn. Only a
        whole range counts as written: one that fails part way leaves bytes
        only inside its own range, which the next attempt writes over.
        permit, the attempt's, hears when the body has arrived, and when
        the attempt writes to the file, which is not network time."""
        length = end - start + 1
        if self.destination.ordered:
            self._read_range(response, length, buffer)
            if permit is not None:
                permit.answered(response.status_code)
            return
        size = len(buffer)
        received = filled = written = 0
        with memoryview(buffer) as view:
            for chunk in self._chunks(response):
                if received + len(chunk) > length:
                    raise requests.exceptions.ChunkedEncodingError(
                        "A range ran long"
                    )
                received += len(chunk)
                if received == length and permit is not None:
                    # The whole body has arrived: what follows is local.
                    permit.answered(response.status_code)
                taken = 0
                while taken < len(chunk):
                    count = min(size - filled, len(chunk) - taken)
                    view[filled : filled + count] = (
                        chunk
                        if count == len(chunk)
                        else chunk[taken : taken + count]
                    )
                    filled += count
                    taken += count
                    if filled == size:
                        self._write(start + written, view, permit)
                        written += filled
                        filled = 0
            if received != length:
                raise requests.exceptions.ChunkedEncodingError(
                    "A range ended early"
                )
            if filled:
                self._write(start + written, view[:filled], permit)
        self.done.add(start, end)
        self.dirty = True
        self.progress.commit(length)

    def _write(self, offset, data, permit):
        """Write data, a full copy buffer or a range's last bytes, at offset
        in the file. While it writes, an attempt still receiving its body is
        off the network: that time is the destination's."""
        if permit is not None:
            permit.writing(True)
        try:
            self.destination.write_at(offset, (data,), self.lifetime)
        finally:
            if permit is not None:
                permit.writing(False)

    def _deliver(self, data):
        """Write the next range of a stream, counting each byte it takes."""

        def delivered(count):
            self.done.add(self.next_start, self.next_start + count - 1)
            self.next_start += count
            self.dirty = True
            self.progress.commit(count, ranges=0)

        self.destination.write(data, self._check_lifetime, delivered)
        self.progress.commit(0)

    def _read_range(self, response, length, data=None):
        """A range's body in one buffer of exactly its length, data if
        given, so holding it takes what the limiter counts for it."""
        if data is None:
            data = bytearray(length)
        filled = 0
        with memoryview(data) as view:
            for chunk in self._chunks(response):
                if filled + len(chunk) > length:
                    raise requests.exceptions.ChunkedEncodingError(
                        "A range ran long"
                    )
                view[filled : filled + len(chunk)] = chunk
                filled += len(chunk)
        if filled != length:
            raise requests.exceptions.ChunkedEncodingError(
                "A range ended early"
            )
        return data

    # Parallel ranges.

    def _admission(self) -> Controller:
        """The controller that admits the ranges' attempts, chosen once the
        download fetches ranges, by its tuning and the storage its URL names
        (see _settings): a job's for an adaptive download in a job, which
        its other adaptive downloads of the same settings share, otherwise
        the download's own."""
        controller = self.controller
        if controller is None:
            settings = _settings(
                self.tuning,
                _general_purpose_s3(self.uri),
                self.max_concurrency,
            )
            self.settings = settings
            if self.scope is not None and settings.adaptive:
                controller = self.scope.controller(settings)
            else:
                controller = Controller(settings)
            self.controller = controller
        return controller

    def _concurrency(self):
        """How the download chose how many ranges to fetch at once, for its
        log: None when it read the file in one response."""
        settings = self.settings
        if settings is None:
            return None
        return settings.policy if settings.adaptive else "static"

    def _fetch(self, ranges):
        """Fetch ranges, in order, each first taking room in the limiter (a
        file's range its copy buffer, until it is written; a stream's all of
        it, until it is written in turn), then a permit for its first
        attempt from the controller, as many at once as its target allows.
        While a range waits for either, ranges that arrived are collected and
        a stream's written in turn, so that room frees. Workers are started
        as ranges are, up to twice the most the policy allows at once, since
        a range waiting to be fetched again holds no permit."""
        controller = self._admission()
        most = 2 * self.settings.max_concurrency
        executor = concurrent.futures.ThreadPoolExecutor(
            most, thread_name_prefix="files_sdk download"
        )
        pending = collections.deque(ranges)
        # A range with its room in the limiter, waiting for a permit.
        ready: list[tuple[int, int, _Reservation]] = []

        def while_waiting():
            # Room frees as ranges are written, which for a stream happens
            # here, so keep writing while waiting for it.
            self._check_pause()
            self._collect(timeout=0)
            self.progress.report()

        try:
            try:
                while pending or ready or self.in_flight:
                    self._check_pause()
                    while (pending or ready) and len(self.in_flight) < most:
                        if not ready:
                            if not controller.room():
                                break
                            start, end = pending.popleft()
                            ready.append(
                                (
                                    start,
                                    end,
                                    self._reserve(start, end, while_waiting),
                                )
                            )

                        def submit_ready(
                            permit,
                            waiting: tuple[int, int, _Reservation] = ready[0],
                        ):
                            self._submit(executor, *waiting, permit)

                        if not controller.admit(submit_ready):
                            break
                        ready.clear()
                    if self.in_flight:
                        self._collect(timeout=_PROGRESS_INTERVAL)
                    elif controller.pause_left():
                        # The storage service asked to wait before more ranges.
                        self.operation.lifetime.sleep(
                            min(controller.pause_left(), _PROGRESS_INTERVAL),
                            "waiting to download",
                        )
                    else:
                        # Other downloads of the job hold every permit.
                        controller.wait_for_room(_PROGRESS_INTERVAL)
                    self.operation.lifetime.check("downloading")
                    self.progress.report()
            except _Paused:
                # Let the ranges in progress finish, keeping what arrives.
                while self.in_flight:
                    self._collect(timeout=_PROGRESS_INTERVAL, keep_going=True)
                    self.operation.lifetime.check("pausing the download")
                    self.progress.report()
                raise
        except _Paused:
            raise
        except BaseException:
            self.stopping.cancel()
            concurrent.futures.wait(list(self.in_flight))
            raise
        finally:
            executor.shutdown(wait=True)
            for _start, _end, reservation in ready:
                reservation.release()
            for _start, reservation in self.in_flight.values():
                reservation.release()
            self.in_flight.clear()
            for _data, reservation in self.arrived.values():
                reservation.release()
            self.arrived.clear()

    def _reserve(self, start, end, while_waiting):
        """Room in the limiter for the range start-end, without a slot,
        which each attempt at it takes for itself: a stream's whole range,
        held until it is written in turn; a file's range the copy buffer it
        is written through. Time without it is the limiter's, not the
        network's: the controller hears so."""
        length = end - start + 1
        held = (
            length if self.destination.ordered else min(_COPY_BUFFER, length)
        )
        controller = self.controller
        assert controller is not None
        reservation = _admitted(
            self.limiter,
            held,
            self.operation.lifetime,
            while_waiting,
            lambda: controller.note_shortfall("limiter"),
            slot=False,
        )
        controller.note_shortfall("no part ready")
        return reservation

    def _submit(self, executor, start, end, reservation, permit):
        """Hand the range to a worker with the permit for its first attempt,
        within the controller's admission; it takes the permit back if this
        raises. The range's room is then the worker's to give back."""
        future = executor.submit(
            self._fetch_range, start, end, reservation, permit
        )
        self.in_flight[future] = (start, reservation)

    def _collect(self, timeout, keep_going=False):
        """Take finished ranges, raising the first failure unless
        keep_going, and write a stream's ranges that are next in turn."""
        if self.in_flight:
            finished, _ = concurrent.futures.wait(
                list(self.in_flight),
                timeout=timeout,
                return_when=concurrent.futures.FIRST_COMPLETED,
            )
            for future in finished:
                error = future.exception()
                if error is not None and not keep_going:
                    raise error
                start, reservation = self.in_flight.pop(future)
                if error is not None:
                    reservation.release()
                elif self.destination.ordered:
                    self.arrived[start] = (future.result(), reservation)
        while self.next_start in self.arrived:
            data, reservation = self.arrived.pop(self.next_start)
            try:
                self._deliver(data)
            finally:
                reservation.release()
        # Called at least every _PROGRESS_INTERVAL while ranges are in
        # progress, so progress is saved even while none arrive.
        self._save_state()

    def _fetch_range(self, start, end, reservation, permit):
        # Runs in a worker thread, which owns the permit for the range's
        # first attempt, and, for a file, its room. The range's buffer, which
        # its room in the limiter counts, serves every attempt at it: a
        # file's copy buffer, or a stream's whole range, returned to be
        # written in turn. A file's range gives its room back as soon as it
        # is written, and every range its permit and slot as soon as it
        # ends, whatever it ends with, an allocation that fails included.
        attempts = None
        result: dict[str, Any] = {}
        try:
            attempts = _Attempts(permit, self.limiter, self.lifetime)
            length = end - start + 1
            buffer = bytearray(
                reservation.size if not self.destination.ordered else length
            )
            # The bytes an attempt that succeeds reports to the controller:
            # those it validated and took, which, for a first range planned
            # before the file's size was known, can be fewer than planned.
            measured = [length]

            def consume(response, uri, identity):
                self._check_frontend(response)
                if identity is None and (
                    response.status_code in (200, 416)
                    or 300 <= response.status_code < 400
                ):
                    # The first range of a download storage is to bind (only
                    # it is fetched without a version), answered with the
                    # whole file, Range ignored, a range that cannot be
                    # satisfied, such as of an empty file, or a redirect,
                    # which it does not follow: nothing that binds it.
                    raise _Unbound()
                if (
                    isinstance(identity, _StorageVersion)
                    and response.status_code == 200
                ):
                    # Storage now ignores Range for the version it bound: its
                    # whole file must show the version's tag, and is then read
                    # whole as that version (_whole_version), not from here.
                    self._check_version(response, uri, identity)
                    raise _RangesIgnored()
                if response.status_code >= 400:
                    response.content
                    return
                if identity is None:
                    last = self._bind(response, uri, end)
                else:
                    # The first range, planned before the file's size was
                    # known, is exactly the bytes the version has of it.
                    last = min(end, identity.size - 1)
                    self._check_range(response, uri, identity, start, last)
                if (
                    self.destination.ordered
                    and len(buffer) != last - start + 1
                ):
                    # Within the room taken for the whole range.
                    del buffer[last - start + 1 :]
                    buffer.extend(bytes(last - start + 1 - len(buffer)))
                measured[0] = last - start + 1
                self._take_range(start, last, response, buffer, permit)
                result["data"] = buffer if self.destination.ordered else None

            self._request(
                self.workers,
                {
                    "Range": "bytes={}-{}".format(start, end),
                    "Accept-Encoding": "identity",
                },
                consume,
                may_retry=lambda: True,
                attempts=attempts,
                size=lambda: measured[0],
            )
        finally:
            if attempts is not None:
                attempts.release()
            permit.release()
            if not self.destination.ordered:
                reservation.release()
        return result.get("data")

    # Checkpoints.

    def _state(self):
        """What a checkpoint records of the version: an identity's token and
        size, or a storage version's entity tag, size and resource digest;
        never a URL or credential."""
        identity = self.identity
        assert identity is not None
        if isinstance(identity, _StorageVersion):
            recorded = {
                "storage": [identity.etag, identity.size, identity.source]
            }
        else:
            recorded = {"identity": [identity.token, identity.size]}
        if self.destination.ordered:
            return {**recorded, "delivered": self.next_start}
        return {
            **recorded,
            "stage": self.destination.state(),
            "written": self.done.state(),
        }

    def _save_state(self, final=False):
        """Save the checkpoint, when it is due or final. What it records is
        flushed to disk first. Only a download bound to a version keeps one:
        one read whole cannot continue from part of a response. A download
        that has written nothing keeps no checkpoint or temporary file."""
        if self.store is None or not (
            final or (self.dirty and self.store.due())
        ):
            return
        if final and (self.identity is None or not self.done.total()):
            self.destination.discard()
            self.store.clear()
            return
        if self.identity is None:
            return
        self.dirty = False
        if not final:
            self.destination.sync()
            self.store.save(self._state(), final)
            return
        try:
            self.destination.sync()
            self.store.save(self._state(), final)
        except BaseException:
            # No checkpoint will find the temporary file.
            self.destination.discard()
            raise
        self.destination.keep()

    def _save_quietly(self, error):
        try:
            self._save_state(final=True)
        except OSError as problem:
            error.add_note(
                "The checkpoint {} could not be saved: {}".format(
                    self.store.path, problem
                )
            )


def _checked(max_concurrency, progress, range_size):
    """The caller's cap on the ranges in progress (or None), progress
    callback and range size, checked before anything is sent."""
    concurrency = checked_concurrency(max_concurrency, MAX_CONCURRENCY)
    if range_size is None:
        range_size = DEFAULT_RANGE_SIZE
    if (
        isinstance(range_size, bool)
        or not isinstance(range_size, int)
        or range_size < 1
    ):
        raise InvalidParameterError(
            "range_size must be an integer of 1 or more"
        )
    return concurrency, checked_progress(progress), range_size


def checked_tuning(tuning) -> UploadTuning | None:
    """A download's tuning: an UploadTuning without the settings only an
    upload uses, or None."""
    if tuning is None:
        return None
    if not isinstance(tuning, UploadTuning):
        raise InvalidParameterError("tuning must be a files_sdk.UploadTuning")
    given = [
        name for name in _UPLOAD_ONLY if getattr(tuning, name) is not None
    ]
    if given:
        raise InvalidParameterError(
            "UploadTuning.{} applies only to uploads; leave it out of a download's tuning".format(
                ", ".join(given)
            )
        )
    return tuning


def _general_purpose_s3(url):
    """Whether url is an HTTPS URL, on the default port and without user
    information, of an object at one of Amazon S3's general-purpose
    endpoints (_general_purpose_endpoint), as Files.com's S3 download URLs
    are, as the .NET SDK's DownloadVersion.CanBind reads it. It chooses the
    policy of a download bound to a version, and whether a download Files.com
    gave no identity may bind itself to one from storage's answer
    (_Download._bind): storage that checks If-Match against the object the
    URL names, which HTTPS authenticates. The host itself binds nothing; only
    that answer, checked, does. Asked of every URL such a download is bound
    from, as renewed."""
    try:
        parts = urlsplit(url or "")
        port = parts.port
    except ValueError:
        return False
    return (
        parts.scheme == "https"
        and port in (None, 443)
        and parts.username is None
        and len(parts.path) > 1
        and _general_purpose_endpoint(parts.hostname or "")
    )


def _general_purpose_endpoint(host):
    """Whether host is one of Amazon S3's general-purpose endpoints, as the
    reference's AwsMultipartRoute.IsGeneralPurposeEndpoint reads it: s3,
    s3.<region>, s3-<region> or s3.dualstack.<region>, under amazonaws.com
    or amazonaws.com.cn, alone or after a bucket of one or more labels, none
    of them empty. The last label that is s3 is the endpoint's. Not S3's
    accelerate, FIPS, website, access point, Object Lambda, Outposts,
    Express or control endpoints, nor a host that only resembles S3's."""
    host = host.lower()
    within = None
    for domain in _AWS_DOMAINS:
        if host.endswith(domain):
            within = host[: -len(domain)]
            break
    if not within:
        return False
    labels = within.split(".")
    if "s3" in labels:
        endpoint = len(labels) - 1 - labels[::-1].index("s3")
        after = labels[endpoint + 1 :]
        known = (
            not after
            or (len(after) == 1 and _region(after[0]))
            or (
                len(after) == 2
                and after[0] == "dualstack"
                and _region(after[1])
            )
        )
        if not known:
            return False
    else:
        endpoint = len(labels) - 1
        if not labels[endpoint].startswith("s3-") or not _region(
            labels[endpoint][3:]
        ):
            return False
    return all(labels[:endpoint])


def _region(label):
    """Whether label is an AWS region, such as us-east-1, eu-central-2 or
    us-gov-west-1: two letters, words of letters, then a number, in ASCII."""
    words = label.split("-")
    if len(words) < 3 or len(words[0]) != 2 or not all(words):
        return False
    return (
        all(set(word) <= _LOWERCASE for word in words[:-1])
        and set(words[-1]) <= _DIGITS
    )


def _settings(tuning, s3, max_concurrency):
    """The controller settings of a download bound to a version, which
    fetches ranges: from Amazon S3 (s3), unless tuning says otherwise, the
    scaled S3 policy from its start of 150 ranges at once, or
    max_concurrency if lower, adapting as uploads do but with no named
    startup and no warm-up; from other storage, max_concurrency (or four) at once, as
    before. tuning given is used as it is, whatever the storage: with
    adaptive=False, max_concurrency (or four) at once; with concurrency
    settings, the configurable controller with that storage's defaults for
    the rest. max_concurrency caps every policy. A download that does not
    adapt pauses after pushback only as long as storage's Retry-After asks,
    as before, unless tuning gives a backpressure_pause."""
    target_class = "s3" if s3 else "generic"
    if tuning is not None and not tuning.adaptive:
        settings = tuning.settings(
            target_class, max_concurrency or DEFAULT_MAX_CONCURRENCY
        )
        return (
            settings
            if tuning.backpressure_pause is not None
            else dataclasses.replace(settings, backpressure_pause=0.0)
        )
    if tuning is not None and any(
        getattr(tuning, name) is not None for name in _CONCURRENCY_FIELDS
    ):
        return tuning.settings(
            target_class,
            max_concurrency or default_max_concurrency(target_class, tuning),
        )
    if s3:
        settings = DEFAULT_TUNING.settings(
            "s3", max_concurrency or SCALED_S3_MAX_CONCURRENCY
        )
        return dataclasses.replace(settings, startup=None)
    return _STATIC.settings(
        "generic", max_concurrency or DEFAULT_MAX_CONCURRENCY
    )


class _Attempts:
    """What each attempt at one range holds while it runs: the controller's
    permit (the first attempt's comes with the range's admission), then a
    slot in the TransferLimiter of its own. Neither is held between
    attempts, through a retry's wait or a renewal of the URL; the range's
    room in the limiter stays with the range. Used by one worker thread."""

    def __init__(self, permit, limiter, lifetime):
        self.permit = permit
        self.limiter = limiter
        self.lifetime = lifetime
        self.slot: _Reservation | None = None

    def start(self):
        """Just before an attempt's request is built: a permit, if the
        attempt has none yet, behind any cooldown and ahead of new ranges;
        then a slot. Neither wait is under the other's lock."""
        self.permit.acquire(self.lifetime)
        if self.slot is None:
            self.slot = self.limiter._attempt(self.lifetime)

    def end(self, status, retry_after, size):
        """The attempt ended with status: the controller hears how, and both
        go back."""
        self.permit.end(status, retry_after, size)
        self._give_back_slot()

    def release(self):
        """Give back what an attempt holds without a measurement: it
        stopped, its URL is to be renewed, or the range is done. Safe to
        repeat."""
        self.permit.release()
        self._give_back_slot()

    def _give_back_slot(self):
        slot, self.slot = self.slot, None
        if slot is not None:
            slot.release()


class _Unadmitted:
    """The permit of a request the controller neither admits nor measures,
    the storage confirmation of a checkpoint's version or the whole read of
    a version whose storage ignores Range (see _Download._confirm_version
    and _whole_version): it holds nothing, so each attempt holds only its
    slot in the TransferLimiter (_Attempts)."""

    def acquire(self, lifetime):
        pass

    def begin(self):
        pass

    def answered(self, status=None, retry_after=None):
        pass

    def writing(self, active):
        pass

    def end(self, status, retry_after, size):
        pass

    def release(self):
        pass


class DownloadScope:
    """What a job's downloads share: for each kind of adaptive download (its
    resolved settings), one controller, and so one request budget, one
    target and what it learns, for the job's lifetime only. A file's
    downloads inherit its target, measurements, epoch and cooldown, and a
    file finishing resets nothing. A static download keeps its own, as does
    another job, or a standalone download, even through the same
    TransferLimiter."""

    def __init__(self):
        self._lock = threading.Lock()
        self._controllers: dict[Any, Controller] = {}

    def controller(self, settings) -> Controller:
        with self._lock:
            controller = self._controllers.get(settings)
            if controller is None:
                controller = self._controllers[settings] = Controller(
                    settings, shared=True
                )
            return controller


def _open_store(operation, file, checkpoint, destination_name, local_paths):
    """The checkpoint at checkpoint (a local path) for downloading file, and
    its handle, opened and locked; or (None, None)."""
    if checkpoint is None:
        return None, None
    for local in local_paths:
        if same_file(checkpoint, local):
            raise InvalidParameterError(
                "The checkpoint must be a file of its own, not {}".format(
                    local
                )
            )
    key = {
        **scope(operation.context),
        "remote": file.path,
        "destination": destination_name,
    }
    handle, store = file_store(checkpoint, "download", key)
    return handle, store


def _recorded(store, ordered):
    """The version (an identity's token and size, or a storage version) and
    written ranges a checkpoint recorded, and, for a file, its stage's
    record."""
    if store is None:
        return None, [], None
    state = store.load()
    if state is None:
        return None, [], None
    try:
        expected: _Identity | _StorageVersion
        if "storage" in state:
            etag, size, source = state["storage"]
            if (
                not isinstance(etag, str)
                or len(etag) > _MAX_TOKEN
                or not _STORAGE_ETAG.fullmatch(etag)
                or not _whole_number(size)
                or size < 1
                or not isinstance(source, str)
                or not _SOURCE.fullmatch(source)
            ):
                raise ValueError("storage")
            expected = _StorageVersion(etag, size, source)
        else:
            token, size = state["identity"]
            if (
                not isinstance(token, str)
                or not _TOKEN.fullmatch(token)
                or len(token) > _MAX_TOKEN
                or not _whole_number(size)
            ):
                raise ValueError("identity")
            expected = _Identity(token, size, ())
        if ordered:
            delivered = state["delivered"]
            if not _whole_number(delivered) or delivered > size:
                raise ValueError("delivered")
            return expected, ([(0, delivered - 1)] if delivered else []), None
        spans = state["written"]
        if not all(
            isinstance(span, list)
            and len(span) == 2
            and _whole_number(span[0])
            and _whole_number(span[1])
            and span[0] <= span[1] < size
            for span in spans
        ):
            raise ValueError("written")
        return expected, [tuple(span) for span in spans], state["stage"]
    except (KeyError, TypeError, ValueError):
        raise InvalidRequestError(
            "The checkpoint {} does not describe a download. Remove it to "
            "download again.".format(store.path)
        ) from None


def download_path(
    operation,
    file,
    local_path=None,
    *,
    max_concurrency=None,
    progress=None,
    range_size=None,
    checkpoint=None,
    pause_token=None,
    store=None,
    anchor=None,
    outcome=None,
    tuning=None,
    scope=None,
):
    """Download file to local_path within operation and return the File.
    With checkpoint (a local path), or store (a job's slot), the download
    can be paused and resumed. anchor, for a folder download's file, is the
    open Directory it goes in and its name there, which it takes over.
    outcome, a dict, gets the download identity token (or None), the
    published file's identity and the size, for a job's checkpoint. tuning
    and max_concurrency choose how many ranges are fetched at once (see
    _settings); scope, a job's DownloadScope, shares its controller."""
    try:
        settings = _checked(max_concurrency, progress, range_size)
        tuning = checked_tuning(tuning)
        pause = checked_pause(pause_token)
        checkpoint = (
            checked_checkpoint(checkpoint, pause) if store is None else None
        )
        operation.lifetime.check("download")
    except BaseException:
        if anchor is not None:
            anchor[0].close()
        raise
    if anchor is not None:
        parent, name = anchor
        confined = True
    else:
        assert local_path is not None
        target = os.path.realpath(os.fspath(local_path))
        parent, name = Directory.open(
            os.path.dirname(target)
        ), os.path.basename(target)
        confined = False
    target = parent.join(name)
    try:
        handle, opened = _open_store(
            operation, file, checkpoint, target, [target]
        )
    except BaseException:
        parent.close()
        raise
    store = store or opened
    try:
        try:
            expected, spans, stage = _recorded(store, ordered=False)
        except BaseException:
            parent.close()
            raise
        destination = None
        if stage is not None and expected is not None:
            destination = _PathDestination.adopt(
                parent, name, stage, expected.size, confined
            )
            if destination is None:
                util.log_info(
                    "Download checkpoint not used",
                    reason="its temporary file is gone, changed or no longer private",
                    path=file.path,
                )
        if destination is None:
            expected, spans = None, []
            destination = _PathDestination.create(parent, name, confined)
        try:
            download = _Download(
                operation,
                file,
                destination,
                *settings,
                pause=pause,
                tuning=tuning,
                scope=scope,
            )
        except BaseException:
            destination.discard()
            raise
        download.store = store
        download.resume(expected, spans)
        result = download.run()
        if outcome is not None:
            # Only a download identity's: a job confirms a file downloaded
            # before only through Files.com (unchanged), so one storage bound
            # is downloaded again, as one bound to no version is.
            outcome.update(
                token=(
                    download.identity.token
                    if isinstance(download.identity, _Identity)
                    else None
                ),
                output=destination.published,
                size=download.progress.committed,
            )
        return result
    finally:
        if handle is not None:
            handle.close()


def download_stream(
    operation,
    file,
    stream,
    *,
    text=False,
    max_concurrency=None,
    progress=None,
    range_size=None,
    checkpoint=None,
    pause_token=None,
    store=None,
    tuning=None,
):
    """Download file into stream, in order, within operation and return the
    File. With a checkpoint, a later call resumes into a stream positioned
    just after what the earlier one wrote, such as a file opened with "ab".
    tuning and max_concurrency work as for download_path."""
    settings = _checked(max_concurrency, progress, range_size)
    tuning = checked_tuning(tuning)
    pause = checked_pause(pause_token)
    checkpoint = (
        checked_checkpoint(checkpoint, pause) if store is None else None
    )
    destination = _StreamDestination(stream, text)
    operation.lifetime.check("download")
    handle, opened = _open_store(operation, file, checkpoint, "stream", [])
    store = store or opened
    try:
        expected, spans, _stage = _recorded(store, ordered=True)
        if spans and store is not None:
            _check_position(stream, spans[0][1] + 1, store.path)
        download = _Download(
            operation, file, destination, *settings, pause=pause, tuning=tuning
        )
        download.store = store
        download.resume(expected, spans)
        return download.run()
    finally:
        if handle is not None:
            handle.close()


def unchanged(operation, path, token, size):
    """Whether Files.com still offers the version of the remote file path
    whose download identity has token and size."""
    from files_sdk.models.file import File

    file = operation.adopt(File({"path": path}))
    download = _Download(
        operation, file, _Unwritten(), 1, None, DEFAULT_RANGE_SIZE
    )
    try:
        download._renewal(operation, _Identity(token, size, ()))
    except _SourceChanged:
        return False
    return True


def _check_position(stream, delivered, path):
    """Raise unless stream is where a resumed download continues: just after
    the delivered bytes the checkpoint recorded."""
    try:
        position = stream.tell()
    except (AttributeError, OSError, ValueError):
        position = None
    if position != delivered:
        raise InvalidParameterError(
            "The checkpoint {} recorded {} bytes written to the stream, but the "
            "stream is at {}. Resume into a stream just after those bytes (for "
            'a file, truncate it to {} bytes and open it with "ab"), or remove '
            "the checkpoint to download again.".format(
                path,
                delivered,
                "an unknown position" if position is None else position,
                delivered,
            )
        )


READ_RANGE_SIZE = 4 * MiB
"""How much of a file a remote file opened for reading fetches at a time."""


class _Unwritten:
    """The destination of a RemoteReader's download, which reads rather than
    writes: nothing reaches the caller until a response is taken whole."""

    ordered = True

    @staticmethod
    def may_retry():
        return True

    @staticmethod
    def exposed():
        return False


class RemoteReader(io.RawIOBase):
    """The bytes of a remote file, read in order from its start, for a File
    opened for reading.

    With a download identity, it fetches a range of READ_RANGE_SIZE bytes at
    a time, as reads need them, so it holds at most one range; every range
    must be the bytes asked for, of that version, and a version that goes
    while the file is read raises InvalidRequestError. Without one, the
    file is read whole, in one response, into a temporary file of the SDK's
    own beyond READ_RANGE_SIZE bytes, and read from there. It cannot seek.

    Once a read has fetched any of it, the File's size is the file's size as
    storage states it: the version's, which every range's Content-Range must
    name, or the whole answer's Content-Length, which its body must match,
    unless that answer is encoded. Otherwise it is None, never the size the
    API's record of the file states.
    """

    def __init__(self, operation, file, range_size=None):
        super().__init__()
        self._download = _Download(
            operation,
            file,
            _Unwritten(),
            1,
            None,
            range_size or READ_RANGE_SIZE,
        )
        # Reads stop when the operation does, as its requests do.
        self._download.lifetime = operation.lifetime
        self._operation = operation
        self._range_size = range_size or READ_RANGE_SIZE
        self._buffer = memoryview(b"")
        self._position = 0
        self._spool: Any = None
        self._ended = False

    def readable(self):
        return True

    def readinto(self, buffer):
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        with memoryview(buffer) as target:
            target = target.cast("B")
            if not target:
                return 0
            if self._spool is not None:
                return self._spool.readinto(target)
            if not self._buffer and not self._ended:
                self._fill()
            if self._spool is not None:
                return self._spool.readinto(target)
            count = min(len(target), len(self._buffer))
            target[:count] = self._buffer[:count]
            self._buffer = self._buffer[count:]
            self._position += count
            return count

    def _fill(self):
        download = self._download
        operation = self._operation
        # Let go of the range read before, so at most one is held.
        self._buffer = memoryview(b"")
        operation.lifetime.check("reading the file")
        try:
            if download.uri is None:
                download._begin()
            identity = download.identity
            if identity is None:
                self._spool_whole()
                return
            if self._position >= identity.size:
                # Only a version of no bytes ends before its first range,
                # which no storage answer then sizes: the identity does.
                self._settle_size(identity.size)
                self._ended = True
                return
            start = self._position
            end = min(start + self._range_size, identity.size) - 1
            got: dict[str, Any] = {}

            def consume(response, uri, current):
                download._check_frontend(response)
                if response.status_code >= 400:
                    response.content
                    return
                download._check_range(response, uri, current, start, end)
                got["data"] = download._read_range(response, end - start + 1)

            download._request(
                operation,
                {
                    "Range": "bytes={}-{}".format(start, end),
                    "Accept-Encoding": "identity",
                },
                consume,
                may_retry=lambda: True,
            )
        except _SourceChanged as changed:
            # Part of the file has already been read, so it cannot start again.
            raise _changed_error(download.file.path, changed.why) from None
        self._buffer = memoryview(got["data"])
        # Storage's Content-Range named the version's size (_check_range).
        self._settle_size(identity.size)
        if end + 1 >= identity.size:
            self._ended = True

    def _spool_whole(self):
        download = self._download
        # The spooled response, and what storage's status is to confirm.
        got: dict[str, Any] = {}

        def consume(response, uri, identity):
            download._check_frontend(response)
            if response.status_code >= 400:
                response.content
                return
            if response.status_code != 200:
                raise _unusable(
                    "a request for the whole file was answered with HTTP {}".format(
                        response.status_code
                    )
                )
            spool = tempfile.SpooledTemporaryFile(max_size=self._range_size)
            try:
                for chunk in download._chunks(response):
                    spool.write(chunk)
                size = spool.tell()
                declared = response.headers.get("Content-Length")
                untrusted = declared is None or download._encoded(response)
                if (
                    declared is not None
                    and not untrusted
                    and size != int(declared)
                ):
                    raise requests.exceptions.ChunkedEncodingError(
                        "The download ended early"
                    )
                spool.seek(0)
            except BaseException:
                spool.close()
                raise
            if "spool" in got:
                got["spool"].close()
            request_id = download_status.request_id_of(response)
            got.update(
                spool=spool,
                confirm=(
                    (uri, request_id, size)
                    if untrusted and request_id
                    else None
                ),
                # Only an unencoded Content-Length, which the body matched,
                # says the file's size.
                size=None if untrusted else size,
            )

        try:
            download._request(
                self._operation, {}, consume, may_retry=lambda: True
            )
            if got["confirm"] is not None:
                # Nothing reaches the caller until storage confirms it.
                download._confirm(*got["confirm"])
        except BaseException:
            if "spool" in got:
                got["spool"].close()
            raise
        if self._spool is not None:
            self._spool.close()
        self._spool = got["spool"]
        self._settle_size(got["size"])
        self._ended = True

    def _settle_size(self, size):
        """Give the File the size storage states for it, or None where
        storage states none the SDK can trust, once the requests that may
        renew its URL, and with it take the API record's size, are done."""
        self._download.file.size = size

    def close(self):
        if self._spool is not None:
            self._spool.close()
            self._spool = None
        self._buffer = memoryview(b"")
        super().close()
