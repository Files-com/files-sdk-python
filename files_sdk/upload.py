"""Uploads: sending a file's bytes to Files.com in the parts it asks for.

An upload begins with begin_upload, which answers with the first part's
signed storage URL and says how the rest may go: whether parts can be sent
in parallel (parallel_parts) and retried (retry_parts), how large each part
is, and how many there can be. The SDK sends each part's bytes to storage
with the method and headers Files.com gave, and completes the upload by
creating the file with the ETags storage returned, in part order.

One _Upload coordinates each upload from the calling thread. It asks for
parts, assigns each one its fixed place in the file (part number, offset
and length) before any of its bytes are read, and hands parts to worker
threads, several at a time only when Files.com allows parallel parts and
the size is known. A stream's part is read once into a buffer the SDK owns,
so a retry sends exactly the bytes the first attempt sent, whatever happens
to the stream meanwhile. A local file's part is read from the file as it is
sent, through a small copy buffer, and each retry reads the same range
again (a part no larger than that buffer, or any part while DEBUG logging
is on, is read whole before it starts). The file must not change while it
uploads: it is checked around every read and before the upload completes,
by its metadata and, on Windows, by Windows' notice of a write where
Windows gives one (see _PathSource), and a change found fails the upload,
though no check can find every change. A
TransferLimiter bounds the parts in progress and the bytes their buffers
hold, across every upload that shares it. Each attempt to send a part holds
a permit from the upload's controller (see files_sdk.adaptive) for that
attempt alone; a part waiting to be sent again waits for a new one.

Everything runs within the upload's operation (see files_sdk.lifetime):
cancelling it, closing the client or reaching the deadline stops admitting
parts, stops the requests in progress and waits for the workers before the
upload raises. The request that completes the upload is sent once all
parts have arrived, and is never sent again once it may have been received.

With a checkpoint (see files_sdk.checkpoint), an upload records its
reference, every part it has placed and the ETags of those that arrived,
so a later call can resume it: the parts that arrived are kept, the rest
are sent again with the same number, offset and length and fresh URLs.
Pausing stops placing parts, lets those in progress finish and saves the
checkpoint. The checkpoint's completion says whether the request that
completes the upload is still to send ("pending"), was about to be sent
("completing", saved to disk before it is), or may have been received
("uncertain"); a later call completes only a pending upload. A pending
upload whose file was seen to change, even while pausing, keeps nothing to
resume: what arrived may hold the file's earlier bytes, which its recorded
metadata cannot tell apart. So one that fails for another reason looks at
its file once more before its checkpoint is kept, and a call that sees the
file change before it takes up the pending upload its checkpoint records,
as when it was paused before it began, forgets that one too. One that may
already have completed is kept as it was, whatever the file did.
"""

import collections
import concurrent.futures
import contextlib
import dataclasses
from datetime import datetime, timezone
import hashlib
import io
import logging
import math
import os
import sys
import tempfile
import threading
import time
from typing import Any
from urllib.parse import parse_qsl, unquote, urlsplit

from files_sdk.api_client import (
    _for_transfer,
    _RetryDeclined,
    unexpected_response_error,
)
from files_sdk.error import (
    APIConnectionError,
    APIError,
    DeadlineExceededError,
    InvalidParameterError,
    InvalidRequestError,
    NotImplementedError,
    OperationCancelledError,
    TransferPausedError,
)
from files_sdk.adaptive import (
    DEFAULT_TUNING,
    SCALED_S3,
    SCALED_S3_MAX_CONCURRENCY,
    TARGET_CLASSES,
    Controller,
    Observer,
    UploadTuning,
    _SizeFeedback,
    default_max_concurrency,
    knobs,
)
from files_sdk.checkpoint import (
    checked_checkpoint,
    checked_pause,
    digest,
    file_store,
    same_file,
    scope,
)
from files_sdk.lifetime import CancellationToken, Lifetime
import files_sdk.util as util

MiB = 1024 * 1024

DEFAULT_MAX_CONCURRENCY = 4
"""Parts a non-adaptive upload sends at once, when Files.com allows
parallel parts and max_concurrency is not given."""

MAX_CONCURRENCY = SCALED_S3_MAX_CONCURRENCY
"""The most ranges one download, or a job's adaptive downloads together,
can fetch at once: the scaled S3 policy's maximum, and the largest
max_concurrency a download accepts."""

MAX_UPLOAD_CONCURRENCY = SCALED_S3_MAX_CONCURRENCY
"""The most parts one upload, or a job's uploads together, can send at
once: the scaled S3 policy's maximum, and the largest max_concurrency an
upload accepts."""

OWNED_MAX_BYTES = 128 * MiB
"""The bytes a client's own TransferLimiter lets transfers buffer at once."""

MAX_BUFFERED_PART = 5 * 1024 * MiB
"""The most bytes the SDK holds in memory for one part: a stream's part,
held whole until storage has it, what is written to a remote file, or a
local file's part read whole for DEBUG logging. Every part Amazon S3
accepts fits. The part size Files.com gives is the most a part may hold,
not what is read: a part holds only what is left of the source, so a large
part size fails nothing by itself. A stream part that would hold more than
this fails the upload instead, before it is read when the stream's size
shows that; a local file's part is sent from the file."""

# How often, at most, an upload reports its progress.
_PROGRESS_INTERVAL = 0.25

# Streams are read in pieces this large, so that stopping an upload takes
# effect between them.
_READ_SIZE = MiB

# A local file's part is sent through a copy buffer of at most this many
# bytes, which is what it holds in the limiter.
_COPY_SIZE = 64 * 1024

# A signed URL is renewed when it expires within this many seconds, since
# the storage service's clock and the local one can differ.
_EXPIRY_MARGIN = 60

# Renewals of one part's URL once it has expired, before or after sending it.
_MAX_RENEWALS = 2

# The one way of sending a part that Files.com describes: the part's bytes
# as the request body, with its length in Content-Length.
_BODY_SEND = {"partsize": "required-header Content-Length", "partdata": "body"}
_METHODS = frozenset({"PUT", "POST", "PATCH"})

# Parameters the SDK sets itself. begin_upload accepts the others, and the
# request that completes the upload also takes these.
_OWN_PARAMS = frozenset(
    {"ref", "part", "parts", "size", "restart", "action", "etags", "length"}
)
_FINISH_PARAMS = frozenset(
    {
        "mkdir_parents",
        "with_rename",
        "buffered_upload",
        "custom_metadata",
        "provided_mtime",
    }
)
_FINISH_ONLY_PARAMS = frozenset({"custom_metadata", "provided_mtime"})


class TransferLimiter:
    """A budget for the upload parts and download requests in progress: how
    many there can be at once, and how many bytes the SDK's buffers for
    them can hold.

    Each upload part holds one of max_parts slots, from before its bytes are
    read (or, for a remote file opened for writing, before the first is
    written) until storage has answered for it, and room for its bytes: a
    stream's part (and a remote file's) its whole size, since the SDK holds
    those bytes until then; a local file's part the copy buffer it is sent
    through, at most 64 KiB, since its bytes are read from the file as they
    are sent (its whole size while DEBUG logging is on, which logs every
    byte). A part waiting to be sent again keeps its slot and room. A
    resumed upload reads each part that arrived before again, to check it is
    the same, holding a slot and room for one read of at most 1 MiB while it
    does. Each range a download fetches holds room from before it is
    requested until it is written: to a file, the copy buffer it is written
    through, at most 256 KiB; to a stream, the whole range, which is written
    only after the ranges before it. Each attempt to fetch it holds a slot
    of its own, from just before its request is sent until it ends, so a
    range waiting to be fetched again, or for its URL to be renewed, holds
    its room but no slot. Directory and file-list transfers hold room this
    way for each file in progress. So max_bytes bounds the bytes buffered
    at once, not the size of the files moved.

    Give one limiter to several clients to cap their transfers together; it
    holds no credentials or other client state. A limiter you give is a hard
    budget that the SDK never raises, and transfers sharing it do not share
    what they learn about the network. A client given none has its own, of
    1024 parts and 128 MiB; TransferLimiter() itself defaults to 32 parts and
    256 MiB. Transfers waiting for room or a slot
    are admitted in the order they asked, so one cannot take the whole
    budget for long. A download attempt waits in that order for its slot
    too, but its range already holds its room, so it goes ahead of those
    waiting only for room they cannot have yet; never of one that asked
    earlier for a slot it could use. A part or range larger than
    max_bytes waits until no other holds room and then runs alone, so it can
    never wait forever.

    The budget does not cover a download read whole, in one response
    (without a download identity), which is written as it arrives, or a
    remote file opened for reading. Nor does it cover what the caller's own
    objects hold, such as a stream's internal buffer, or memory the HTTP
    libraries use while sending and receiving.
    """

    def __init__(self, max_parts: int = 32, max_bytes: int = 256 * MiB):
        self._max_parts = _positive("max_parts", max_parts)
        self._max_bytes = _positive("max_bytes", max_bytes)
        self._condition = threading.Condition()
        # Slots in use; bytes held; and reservations granted from the queue
        # that hold room, with or without a slot now, which is what keeps a
        # part or range larger than max_bytes from running beside others.
        self._parts = 0
        self._bytes = 0
        self._holding = 0
        self._waiting: collections.deque[_Reservation] = collections.deque()
        # Whether the SDK made it for a client given none, rather than the
        # caller.
        self._owned = False

    @classmethod
    def _client_owned(cls) -> "TransferLimiter":
        """The budget of a client given no limiter: as many parts as an
        upload can send at once, and 128 MiB of buffers."""
        limiter = cls(MAX_UPLOAD_CONCURRENCY, OWNED_MAX_BYTES)
        limiter._owned = True
        return limiter

    @property
    def max_parts(self) -> int:
        """The most upload parts and download attempts that can hold a slot
        at once."""
        return self._max_parts

    @property
    def max_bytes(self) -> int:
        """The most bytes upload parts and download ranges can hold at
        once, except for one part or range larger than this, which runs
        alone."""
        return self._max_bytes

    @property
    def parts_in_use(self) -> int:
        """Upload parts and download attempts holding a slot now."""
        return self._parts

    @property
    def bytes_in_use(self) -> int:
        """Bytes held now: the room held by upload parts and download ranges,
        and any bytes a stream returned beyond what an upload asked for,
        kept for its next part."""
        return self._bytes

    def __repr__(self):
        return "<files_sdk.TransferLimiter {}/{} parts, {}/{} bytes>".format(
            self._parts, self._max_parts, self._bytes, self._max_bytes
        )

    def _request(self, size, slot=True) -> "_Reservation":
        """A reservation of size bytes, and one slot unless slot is False
        (a download range's room, whose attempts take slots of their own:
        _attempt), granted now if there is room and no one is waiting ahead
        of it."""
        reservation = _Reservation(self, size, slot=slot, room=True)
        with self._condition:
            self._waiting.append(reservation)
            self._grant()
        return reservation

    def _take(self, size) -> "_Reservation":
        """Count size bytes the SDK already holds, without a slot or a wait.
        Parts wait until they fit again."""
        reservation = _Reservation(self, size, slot=False)
        with self._condition:
            self._bytes += size
            reservation.granted = True
        return reservation

    def _attempt(self, lifetime) -> "_Reservation":
        """A slot for one attempt at a download range, whose room the range
        already holds, until the attempt ends. It waits in line with the
        other reservations, needing no room (see _grant). Raises, holding
        nothing, if lifetime ends first."""
        reservation = _Reservation(self, 0, slot=True)
        stop_waking = lifetime.watch(self._wake)
        try:
            with self._condition:
                self._waiting.append(reservation)
                self._grant()
                while not reservation.granted:
                    lifetime.check("waiting to download")
                    self._condition.wait(_PROGRESS_INTERVAL)
            lifetime.check("waiting to download")
        except BaseException:
            # Out of line, or the slot given back.
            reservation.release()
            raise
        finally:
            stop_waking()
        return reservation

    def _grant(self):
        # Called with the condition held. Grant waiting reservations in the
        # order they asked, while they fit. Room is granted strictly in that
        # order: one that cannot have its room, within max_bytes unless
        # nothing holds room, or the slot it needs, holds back the room of
        # every one after it. A slot goes to the earliest one waiting for a
        # slot it can use: so a download attempt, which needs no room, goes
        # ahead only of those waiting for room they cannot have yet, and no
        # later reservation takes a slot ahead of an earlier attempt.
        room_waits = slot_waits = False
        granted = []
        for waiting in self._waiting:
            if room_waits and (slot_waits or self._parts >= self._max_parts):
                break  # Nothing after this can be granted.
            if waiting.room:
                if room_waits:
                    continue
                if (
                    self._holding
                    and self._bytes + waiting.size > self._max_bytes
                ):
                    room_waits = True
                    continue
                if waiting.slot and (
                    slot_waits or self._parts >= self._max_parts
                ):
                    room_waits = slot_waits = True
                    continue
                self._holding += 1
                self._bytes += waiting.size
            elif slot_waits or self._parts >= self._max_parts:
                slot_waits = True
                continue
            if waiting.slot:
                self._parts += 1
            waiting.granted = True
            granted.append(waiting)
        for waiting in granted:
            self._waiting.remove(waiting)
        self._condition.notify_all()

    def _release(self, reservation):
        with self._condition:
            if reservation.released:
                return
            reservation.released = True
            if reservation.granted:
                self._bytes -= reservation.size
                if reservation.slot:
                    self._parts -= 1
                if reservation.room:
                    self._holding -= 1
            else:
                self._waiting.remove(reservation)
            self._grant()

    def _wake(self):
        with self._condition:
            self._condition.notify_all()


def _positive(name, value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise InvalidParameterError(
            "{} must be an integer of 1 or more".format(name)
        )
    return value


class _Reservation:
    """Room in a TransferLimiter, from when it is granted until released."""

    # Seconds the reservation waited for room, once granted.
    waited = 0.0

    def __init__(self, limiter, size, slot, room=False):
        self.limiter = limiter
        self.size = size
        self.slot = slot
        # Whether it waits in line for room, and so, once granted, holds
        # it: not a download attempt's slot, nor bytes already held (_take).
        self.room = room
        self.granted = False
        self.released = False

    def wait(self, timeout):
        """Wait up to timeout seconds to be granted. Returns whether it is."""
        condition = self.limiter._condition
        with condition:
            if not self.granted:
                condition.wait(timeout)
            return self.granted

    def release(self):
        """Give the room back, or stop waiting for it. Safe to repeat."""
        self.limiter._release(self)


@dataclasses.dataclass(frozen=True)
class UploadProgress:
    """How far an upload has got, as passed to its progress callback.

    bytes_committed counts the bytes of parts storage has accepted;
    bytes_sent counts every byte put on the network, including parts sent
    again after a failure. bytes_per_second is the rate of committed bytes
    over the last few seconds. total_bytes is None when the size is not
    known in advance.
    """

    path: str
    total_bytes: int | None
    bytes_committed: int
    bytes_sent: int
    parts_committed: int
    elapsed: float
    bytes_per_second: float


def _unexpected(problem):
    """The error for an upload part description the SDK cannot use, when
    there is no response to attach."""
    return APIConnectionError(
        "Received an unexpected response from the Files.com API: {}".format(
            problem
        )
    )


def checked_concurrency(value, most=MAX_CONCURRENCY) -> int | None:
    if value is None:
        return None
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or not 1 <= value <= most
    ):
        raise InvalidParameterError(
            "max_concurrency must be an integer from 1 to {}".format(most)
        )
    return value


def checked_upload_concurrency(value) -> int | None:
    """An upload's max_concurrency: a cap on the parts it sends at once,
    whatever chooses how many."""
    return checked_concurrency(value, MAX_UPLOAD_CONCURRENCY)


def checked_tuning(value, context) -> UploadTuning:
    if value is None:
        return context.upload_tuning or DEFAULT_TUNING
    if not isinstance(value, UploadTuning):
        raise InvalidParameterError("tuning must be a files_sdk.UploadTuning")
    return value


def checked_progress(value):
    if value is not None and not callable(value):
        raise InvalidParameterError("progress must be callable")
    return value


def split_params(params) -> tuple[dict[str, Any], dict[str, Any]]:
    """The caller's params for an upload, split into those for begin_upload
    and those for the request that completes the upload. Raises for a
    parameter the SDK sets itself."""
    if params is None:
        params = {}
    if not isinstance(params, dict):
        raise InvalidParameterError("params must be a dictionary")
    own = sorted(name for name in params if name in _OWN_PARAMS)
    if own:
        raise InvalidParameterError(
            "The SDK sets {} for an upload; leave {} out of params".format(
                ", ".join(own), "it" if len(own) == 1 else "them"
            )
        )
    for name, kind in (
        ("mkdir_parents", bool),
        ("with_rename", bool),
        ("buffered_upload", bool),
        ("with_direct_connection_info", bool),
        ("custom_metadata", dict),
        ("provided_mtime", str),
    ):
        if name in params and not isinstance(params[name], kind):
            raise InvalidParameterError(
                "Bad parameter: {} must be a {}".format(name, kind.__name__)
            )
    begin = {
        name: value
        for name, value in params.items()
        if name not in _FINISH_ONLY_PARAMS
    }
    finish = {
        name: value for name, value in params.items() if name in _FINISH_PARAMS
    }
    return begin, finish


def utc_mtime(seconds) -> str:
    """A modification time for provided_mtime: UTC without an offset, as the
    API has always received it."""
    return (
        datetime.fromtimestamp(seconds, timezone.utc)
        .replace(tzinfo=None)
        .isoformat()
    )


def _expiry(value):
    """A part URL's expiry as a time.time() value, or None if the API gave
    none it could parse."""
    if not isinstance(value, str) or not value:
        return None
    try:
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.timestamp()


# Signed URL forms that say when they stop working: a signing time and a
# lifetime in seconds (AWS, Files.com and Google), or an expiry time with
# the permissions it grants (an Azure shared access signature).
_SIGNED_LIFETIMES = (
    ("x-amz-date", "x-amz-expires"),
    ("x-files-date", "x-files-expires"),
    ("x-goog-date", "x-goog-expires"),
)


def _signed_url_expiry(url):
    """When a signed URL's own query says it expires, as a time.time()
    value, or None if it says nothing the SDK can read."""
    query = {}
    for name, value in parse_qsl(urlsplit(url).query, keep_blank_values=True):
        query.setdefault(name.lower(), value)
    found = []
    for signed, lifetime in _SIGNED_LIFETIMES:
        try:
            start = datetime.strptime(query[signed], "%Y%m%dT%H%M%SZ").replace(
                tzinfo=timezone.utc
            )
            found.append(start.timestamp() + int(query[lifetime]))
        except (KeyError, ValueError):
            pass
    if "sp" in query:
        found.append(_expiry(query.get("se")))
    found = [moment for moment in found if moment is not None]
    return min(found) if found else None


def _grant_expiry(expires, url):
    """The earlier of what a part's description and its URL say about when
    the URL expires, or None if neither says."""
    known = [
        moment
        for moment in (_expiry(expires), _signed_url_expiry(url))
        if moment is not None
    ]
    return min(known) if known else None


def expiring(expires):
    """Whether a signed URL that expires at expires (a time.time() value, or
    None if unknown) has expired, or will within _EXPIRY_MARGIN."""
    return expires is not None and time.time() >= expires - _EXPIRY_MARGIN


def refused_as_expired(error, expires):
    """Whether storage refused a signed URL that expires at expires because
    it has expired: its answer says so (see api_client), or it is a 403 once
    that time has come. Any other refusal, a 403 included, is not."""
    return getattr(error, "files_storage_expired", False) or (
        error.http_status == 403 and expiring(expires)
    )


@dataclasses.dataclass(frozen=True, repr=False)
class _Grant:
    """One part as begin_upload described it. Its URL is a credential, so
    it has no repr."""

    record: dict[str, Any]
    ref: str
    number: int
    partsize: int
    upload_uri: str
    method: str
    headers: tuple[tuple[str, str], ...]
    expires: float | None
    parallel: bool
    retry: bool
    offset_query: bool
    available_parts: int | None
    variable_limits: "_Limits | None" = None
    target_class: str = "generic"

    @classmethod
    def parse(cls, response, record) -> "_Grant":
        """The grant in one begin_upload record. Raises for a malformed
        record, and for a way of sending a part the SDK does not support,
        before anything is sent to storage."""
        if not isinstance(record, dict):
            raise unexpected_response_error(
                response, "an upload part was not a JSON object"
            )

        def value(name, kind, required=True) -> Any:
            item = record.get(name)
            if item is None and not required:
                return None
            if (
                isinstance(item, bool)
                and kind is not bool
                or not isinstance(item, kind)
            ):
                raise unexpected_response_error(
                    response, "an upload part had no valid {}".format(name)
                )
            return item

        headers = value("headers", dict, required=False) or {}
        if not all(
            isinstance(k, str) and isinstance(v, str)
            for k, v in headers.items()
        ):
            raise unexpected_response_error(
                response, "an upload part had invalid headers"
            )
        upload_uri = value("upload_uri", str)
        grant = cls(
            record=record,
            ref=value("ref", str),
            number=value("part_number", int),
            partsize=value("partsize", int),
            upload_uri=upload_uri,
            method=(
                value("http_method", str, required=False) or "PUT"
            ).upper(),
            headers=tuple(headers.items()),
            expires=_grant_expiry(record.get("expires"), upload_uri),
            parallel=record.get("parallel_parts") is True,
            retry=record.get("retry_parts") is not False,
            offset_query=record.get("part_offset_query") is True,
            available_parts=value("available_parts", int, required=False),
            variable_limits=_Limits.parse(record.get("variable_part_limits")),
            target_class=_target_class(record.get("upload_target_class")),
        )
        if grant.number < 1 or grant.partsize < 0:
            raise unexpected_response_error(
                response, "an upload part had an invalid size or number"
            )
        unsupported = []
        if grant.method not in _METHODS:
            unsupported.append("HTTP method {}".format(grant.method))
        if record.get("parameters"):
            unsupported.append("extra parameters with the part")
        send = record.get("send")
        if send not in (None, {}, _BODY_SEND):
            unsupported.append("send instructions {!r}".format(send))
        if unsupported:
            raise NotImplementedError(
                "Files.com asked for this upload to be sent in a way the SDK "
                "does not support ({}), so nothing was sent. Please report "
                "this to Files.com support.".format("; ".join(unsupported))
            )
        return grant

    @classmethod
    def from_model(cls, part) -> "_Grant":
        """The grant of a FileUploadPart that upload_chunks returned."""
        record = part.get_attributes()
        return cls(
            record=record,
            ref=part.ref,
            number=part.part_number,
            partsize=part.partsize or 0,
            upload_uri=part.upload_uri or "",
            method=(part.http_method or "PUT").upper(),
            headers=tuple((part.headers or {}).items()),
            expires=_grant_expiry(part.expires, part.upload_uri or ""),
            parallel=part.parallel_parts is True,
            retry=part.retry_parts is not False,
            offset_query=False,
            available_parts=part.available_parts,
        )

    def url(self, offset, with_offset):
        """The URL to send the part at offset to: the signed URL exactly as
        given, with part_offset set when the upload sends offsets."""
        if not with_offset:
            return self.upload_uri
        url, hash_, fragment = self.upload_uri.partition("#")
        base, _, query = url.partition("?")
        pairs = [
            pair
            for pair in query.split("&")
            if pair and pair.partition("=")[0] != "part_offset"
        ]
        pairs.append("part_offset={}".format(offset))
        return "{}?{}{}{}".format(base, "&".join(pairs), hash_, fragment)


@dataclasses.dataclass(repr=False)
class _Part:
    """A part's fixed place in the file, and the grant to send it with.
    The grant can be renewed, and a part resumed from a checkpoint has none
    until it is; the number, offset and length never change. partsize is
    the size Files.com gave the part (or, for part sizes the upload chose,
    its length); digest, for a checkpoint, the SHA-256 of its bytes when
    they can be read again only to check them."""

    number: int
    offset: int
    length: int
    grant: "_Grant | None"
    partsize: int = 0
    digest: str | None = None

    def __repr__(self):
        return "<upload part {} at {}, {} bytes>".format(
            self.number, self.offset, self.length
        )


class _Planner:
    """Where each part of an upload of known size goes. Parts are placed in
    order as Files.com describes them: each starts where the one before
    ended and is as long as its part size, or what is left. This is integer
    arithmetic alone, so planning an upload of any size allocates nothing."""

    def __init__(self, size):
        self.size = size
        self.number = 1
        self.offset = 0
        self.latest = 0

    @property
    def done(self):
        """Whether every byte has a part (an empty upload has one part)."""
        return self.number > 1 and self.offset >= self.size

    def length(self, grant):
        """How long the next part would be with grant."""
        return min(grant.partsize, self.size - self.offset)

    def place(self, grant, length=None) -> _Part:
        """The next part, with grant, of length (by default, as length()
        says now)."""
        if length is None:
            length = self.length(grant)
        if length <= 0 and self.size:
            raise _unexpected("upload part {} had no size".format(self.number))
        part = _Part(self.number, self.offset, length, grant, grant.partsize)
        self.number += 1
        self.offset += length
        self.latest = grant.partsize
        return part

    def restore(self, number, offset, latest, parts):
        """Continue after parts, placed before, which end at offset."""
        self.number, self.offset, self.latest = number, offset, latest

    def parts_left(self):
        """At most how many parts are left. Part sizes never shrink, so the
        latest one bounds it."""
        return max(1, math.ceil((self.size - self.offset) / self.latest))


def _target_class(value) -> str:
    """upload_target_class, or generic for an absent or unknown one."""
    return (
        value
        if isinstance(value, str) and value in TARGET_CLASSES
        else "generic"
    )


# Query parameters that bind a part's length or bytes to its signed URL.
_BINDING_QUERY = frozenset(
    {
        "x-amz-content-sha256",
        "x-amz-sdk-checksum-algorithm",
        "x-amz-decoded-content-length",
        "content-md5",
        "content-length",
    }
)


def _aws_multipart_route(record, number):
    """The resource (the URL before its query) and upload ID of an ordinary
    multipart upload straight to Amazon S3, as begin_upload's record for
    part number shows it, or None. As the .NET SDK reads it
    (AwsMultipartRoute.Of), every condition must hold: an ordinary write
    (action put/write) sent with PUT; no direct connection information;
    no required headers or parameters; the part's bytes as the body with
    exactly their length as Content-Length; an HTTPS URL without a fragment
    at one of S3's general-purpose endpoints (see
    files_sdk.download._general_purpose_s3); and a SigV4 presigned
    UploadPart query: one partNumber naming this part, one uploadId, one
    AWS4-HMAC-SHA256 X-Amz-Algorithm, one X-Amz-Credential scoped to s3,
    X-Amz-SignedHeaders of host alone, so that neither the part's length
    nor its bytes are signed, and one X-Amz-Signature, with no checksum,
    digest or length among its parameters. A host that only resembles
    S3's, a custom endpoint or any other URL is not this route."""
    from files_sdk.download import _general_purpose_s3

    part_number = record.get("part_number")
    if (
        record.get("action") != "put/write"
        or record.get("http_method") != "PUT"
        or record.get("direct_connection_info") is not None
        or (part_number is not None and part_number != number)
        or record.get("headers") not in (None, {})
        or record.get("parameters") not in (None, {})
        or record.get("send") != _BODY_SEND
    ):
        return None
    uri = record.get("upload_uri")
    if not isinstance(uri, str) or "#" in uri or not _general_purpose_s3(uri):
        return None
    resource, mark, query = uri.partition("?")
    if not mark:
        return None
    values: dict[str, list[str]] = {}
    for pair in query.split("&"):
        name, equals, value = pair.partition("=")
        if not equals or not name:
            return None
        name = unquote(name)
        lowered = name.lower()
        if lowered.startswith("x-amz-checksum") or lowered in _BINDING_QUERY:
            return None
        values.setdefault(name, []).append(unquote(value))

    def single(name):
        found = values.get(name, [])
        return found[0] if len(found) == 1 else None

    upload_id, credential = single("uploadId"), single("X-Amz-Credential")
    if (
        single("partNumber") != str(number)
        or not upload_id
        or single("X-Amz-Algorithm") != "AWS4-HMAC-SHA256"
        or credential is None
        or not credential.endswith("/s3/aws4_request")
        or single("X-Amz-SignedHeaders") != "host"
        or not single("X-Amz-Signature")
    ):
        return None
    return resource, upload_id


@dataclasses.dataclass(frozen=True)
class _Limits:
    """A variable_part_limits grant: the upload may choose part sizes, each
    but the last at least min_nonfinal_bytes, none over max_part_bytes, no
    more than max_parts of them, for a file of at most max_file_bytes."""

    min_nonfinal_bytes: int
    max_part_bytes: int
    max_parts: int
    max_file_bytes: int

    @classmethod
    def parse(cls, value) -> "_Limits | None":
        """The grant, or None unless all four limits are positive integers:
        a partial grant allows nothing."""
        names = [field.name for field in dataclasses.fields(cls)]
        if not isinstance(value, dict):
            return None
        numbers = [value.get(name) for name in names]
        limits_given = [
            n
            for n in numbers
            if isinstance(n, int) and not isinstance(n, bool) and n > 0
        ]
        if len(limits_given) != len(names):
            return None
        limits = cls(*limits_given)
        return (
            limits
            if limits.min_nonfinal_bytes <= limits.max_part_bytes
            else None
        )

    def fits(self, size, available=None) -> bool:
        """Whether a file of size bytes can be split within these limits,
        and within available part numbers if Files.com gave a number."""
        return 0 < size <= self.max_file_bytes and math.ceil(
            size / self.max_part_bytes
        ) <= self.allowance(available)

    def allowance(self, available=None) -> int:
        """The parts these limits allow, and no more than available."""
        return (
            self.max_parts
            if available is None
            else min(self.max_parts, available)
        )

    def covers(self, planner) -> bool:
        """Whether the parts planner has placed are still within these."""
        return (
            planner.largest <= self.max_part_bytes
            and (planner.smallest_nonfinal or self.min_nonfinal_bytes)
            >= self.min_nonfinal_bytes
            and planner.number - 1 <= self.max_parts
            and planner.size <= self.max_file_bytes
        )


class _VariablePlanner(_Planner):
    """Parts whose sizes the upload chooses, within a variable_part_limits
    grant. Each part is sized when it is placed, so parts not yet placed can
    follow a change in how many parts go at once, or what the file's size
    feedback learned (sizer); placed parts never change. Parts are the
    preferred size for the upload's size, smaller for small uploads so there
    are enough of them, and never so small that the rest of the file would
    need more part numbers than the grant allows and Files.com makes
    available (available)."""

    def __init__(
        self, size, limits, settings, concurrency, sizer=None, available=None
    ):
        super().__init__(size)
        self.limits = limits
        self.settings = settings
        self.concurrency = concurrency
        self.sizer: _SizeFeedback | None = sizer
        self.allowance = limits.allowance(available)
        self.largest = 0
        self.smallest_nonfinal = None

    def length(self, grant=None):
        remaining = self.size - self.offset
        slots = self.allowance - (self.number - 1)
        least = math.ceil(remaining / max(slots, 1))
        if self.sizer is not None:
            preferred = self.sizer.size
        else:
            preferred = _preferred_part_size(
                self.settings, self.size, self.concurrency()
            )
        length = min(
            max(preferred, least, self.limits.min_nonfinal_bytes),
            self.limits.max_part_bytes,
        )
        return min(length, remaining)

    def place(self, grant, length=None) -> _Part:
        if length is None:
            length = self.length()
        part = _Part(self.number, self.offset, length, grant, length)
        self.number += 1
        self.offset += length
        self.latest = length
        self.largest = max(self.largest, length)
        if not self.done:
            self.smallest_nonfinal = min(
                self.smallest_nonfinal or length, length
            )
        return part

    def parts_left(self):
        """At most how many parts are left: never more than the part numbers
        left, so grants are never asked for beyond them."""
        return max(
            1, min(super().parts_left(), self.allowance - (self.number - 1))
        )

    def restore(self, number, offset, latest, parts):
        super().restore(number, offset, latest, parts)
        self.largest = max((part.length for part in parts), default=0)
        nonfinal = [
            part.length
            for part in parts
            if part.offset + part.length < self.size
        ]
        self.smallest_nonfinal = min(nonfinal) if nonfinal else None


def _preferred_part_size(settings, size, concurrency):
    """The part size settings prefer for an upload of size bytes: their
    tier's, or smaller so the upload has the parts its workload wants (under
    the scaled S3 policy, workload_parts_per_worker parts in all; otherwise
    that many for each part sent at once), down to min_part_size."""
    preferred = settings.preferred_part_size(size)
    wanted = settings.workload_parts_per_worker
    if settings.policy != SCALED_S3 or settings.explicit_sizes:
        wanted *= max(1, concurrency)
    if math.ceil(size / preferred) < wanted:
        preferred = max(
            settings.min_part_size, _floor_mib_power(math.ceil(size / wanted))
        )
    return preferred


def _floor_mib_power(size):
    """The largest power-of-two number of MiB not over size, at least 1 MiB."""
    mib = max(1, size // MiB)
    return (1 << (mib.bit_length() - 1)) * MiB


if sys.platform == "win32":
    import ctypes
    import msvcrt
    from ctypes import wintypes

    from files_sdk import windows_file

    class _FileBasicInfo(ctypes.Structure):
        """FILE_BASIC_INFO. Its times are FILETIME ticks (LARGE_INTEGER
        counts of 100 ns)."""

        _fields_ = [
            ("CreationTime", ctypes.c_int64),
            ("LastAccessTime", ctypes.c_int64),
            ("LastWriteTime", ctypes.c_int64),
            ("ChangeTime", ctypes.c_int64),
            ("FileAttributes", wintypes.DWORD),
        ]

    # GetFileInformationByHandleEx, from a kernel32 of the SDK's own so that
    # its argument types are set for it alone, and its FileBasicInfo class.
    _get_file_information = ctypes.WinDLL(
        "kernel32", use_last_error=True
    ).GetFileInformationByHandleEx
    _get_file_information.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        ctypes.c_void_p,
        wintypes.DWORD,
    )
    _get_file_information.restype = wintypes.BOOL
    _FILE_BASIC_INFO_CLASS = 0

    def _change_time(file):
        """When Windows last changed the open file's data or attributes, in
        FILETIME ticks. Python cannot say: its ctime is the creation time
        from os.stat, and from os.fstat too before Python 3.12. The handle
        belongs to the file's descriptor; it is borrowed, not closed."""
        info = _FileBasicInfo()
        handle = msvcrt.get_osfhandle(file.fileno())
        if not _get_file_information(
            handle,
            _FILE_BASIC_INFO_CLASS,
            ctypes.byref(info),
            ctypes.sizeof(info),
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        return info.ChangeTime


class _PathSource:
    """A local file, read by part with a handle of its own for each read.

    It must not change while it uploads. The SDK looks for changes, and a
    change it finds fails the upload instead of completing it with mixed
    contents, but no check finds every change. Its device, inode, size,
    modification time and status change time are checked around every read
    and before the upload completes. On Windows, where Python's ctime is not
    the status change time (see _change_time), the change time is read from
    Windows for each open handle instead, and the file at the path is opened
    again before the upload completes. Since Windows can leave all of that
    as it was after a write, the upload of a file on a local disk also asks
    Windows for notice of any write (files_sdk.windows_file), before anything
    of the file is looked at and until the upload is over; where Windows
    gives none, the metadata alone is checked. Once a change is seen, every
    later check fails too. A checkpoint records the identity os.stat gives,
    as it always has, which a later call compares: equal metadata does not
    prove equal bytes. close() releases what the source holds.
    """

    ordered = False

    def __init__(self, path, *, send_mtime=True, owned=False, expected=None):
        self.path = os.fspath(path)
        # Whether a change was seen: every check after it fails too.
        self.changed_seen = False
        # Windows' notice of a write, asked for before anything of the file
        # is looked at, so that a write from then on is noticed whatever it
        # leaves of the metadata; None elsewhere, and where Windows gives
        # none.
        self._guard = (
            windows_file.acquire(self.path)
            if sys.platform == "win32"
            else None
        )
        try:
            stat = os.stat(self.path)
            if expected is not None and [
                stat.st_dev,
                stat.st_ino,
                stat.st_size,
                stat.st_mtime_ns,
            ] != list(expected):
                # Not the file a job found at this path, or it changed since.
                raise InvalidRequestError(
                    "The file {} changed or was replaced after it was found, so it was "
                    "not uploaded.".format(self.path)
                )
            self.size = stat.st_size
            self.mtime = stat.st_mtime if send_mtime else None
            self._identity = self._identity_of(stat)
            # What every read is checked against (see _live_identity): the
            # identity above, or on Windows the opened file's, which must be the
            # file just found at the path.
            self._live = self._identity
            if sys.platform == "win32":
                with open(self.path, "rb") as file:
                    self._live = self._live_identity(file)
                if self._live[:4] != self._identity[:4]:
                    raise self._changed()
                if self._guard is not None:
                    # The notice must be of the very file just found at the
                    # path, and of no write since it was granted.
                    if (
                        self._identity_of(self._guard.stat())[:4]
                        != self._identity[:4]
                    ):
                        raise self._changed()
                    self._check_guard()
        except BaseException:
            self.close()
            raise
        # The SDK's own copy of a stream, made again for each call: its
        # parts are checked by their bytes when an upload resumes.
        self.owned = owned
        self.record_digests = False

    def close(self):
        """Release what the source holds (Windows' notice of writes), once
        the upload is over: its parts' workers and bodies have finished.
        Safe to repeat."""
        if self._guard is not None:
            self._guard.close()

    @property
    def check_on_resume(self):
        return self.owned

    def checkpoint_state(self):
        return (
            {"size": self.size}
            if self.owned
            else {"size": self.size, "identity": list(self._identity)}
        )

    @staticmethod
    def _identity_of(stat):
        return (
            stat.st_dev,
            stat.st_ino,
            stat.st_size,
            stat.st_mtime_ns,
            stat.st_ctime_ns,
        )

    def _live_identity(self, file):
        """The identity of file, opened from the path, to check against the
        one the upload began with: as _identity_of gives it from os.fstat,
        except that on Windows the change time is Windows' own. A file whose
        change time cannot be read is not uploaded unchecked."""
        stat = os.fstat(file.fileno())
        if sys.platform != "win32":
            return self._identity_of(stat)
        try:
            changed = _change_time(file)
        except OSError as error:
            raise InvalidRequestError(
                "The file {} could not be checked for changes ({}), so the "
                "upload was not completed.".format(self.path, error)
            ) from error
        return (
            stat.st_dev,
            stat.st_ino,
            stat.st_size,
            stat.st_mtime_ns,
            changed,
        )

    def _changed(self):
        self.changed_seen = True
        return InvalidRequestError(
            "The file {} changed while it was being uploaded, so the upload was "
            "not completed. Upload it again once it has stopped changing.".format(
                self.path
            )
        )

    def _check_guard(self):
        """Raise if a change was seen, or Windows has told of a write since
        the upload began, or can no longer tell (its notice ended)."""
        if self.changed_seen or (
            self._guard is not None and not self._guard.intact()
        ):
            raise self._changed()

    def _check_live(self, file):
        """Raise unless file, opened from the path, is still the file the
        upload began with, unchanged as far as can be seen."""
        self._check_guard()
        if self._live_identity(file) != self._live:
            raise self._changed()

    def body(self, part, lifetime):
        """What sends a part not read whole: a _PartBody that reads its
        bytes from the file as they are sent."""
        lifetime.check("reading the file")
        return _PartBody(self, part)

    def read_part(self, part, lifetime):
        """The part's bytes, read with a handle of its own."""
        lifetime.check("reading the file")
        with open(self.path, "rb") as file:
            self._check_live(file)
            file.seek(part.offset)
            data = file.read(part.length)
            if len(data) != part.length:
                raise self._changed()
            self._check_live(file)
        if self.record_digests:
            part.digest = hashlib.sha256(data).hexdigest()
        return data

    def check(self, part, lifetime):
        """Raise unless part's bytes are the ones a checkpoint recorded."""
        found = hashlib.sha256()
        with open(self.path, "rb") as file:
            file.seek(part.offset)
            left = part.length
            while left:
                lifetime.check("checking the stream")
                data = file.read(min(left, _READ_SIZE))
                if not data:
                    break
                found.update(data)
                left -= len(data)
        if found.hexdigest() != part.digest:
            raise _different_stream(part)

    def check_unchanged(self):
        """Raise unless the file at the path is still the one the upload
        began with, unchanged as far as can be seen: no change seen, and no
        write Windows told of. On Windows it is opened first, for the change
        time a rewrite since its last part was read leaves."""
        self._check_guard()
        if sys.platform == "win32":
            with open(self.path, "rb") as file:
                self._check_live(file)
        if self._identity_of(os.stat(self.path)) != self._identity:
            raise self._changed()


class _PartBody:
    """A local file's part as a request body: read from the file while it
    is sent, at most _COPY_SIZE bytes at a time, with a handle of its own,
    so the part holds no more than that in memory. Each attempt reads the
    same range again from its start (rewind); the file is checked to be the
    one the upload began with when the range is opened and once it is all
    read, so a change fails the upload rather than sending other bytes."""

    def __init__(self, source, part):
        self._source = source
        self._part = part
        self._file = None
        self._read = 0
        self._hash = None

    def __repr__(self):
        return "<upload part {} body, {} bytes>".format(
            self._part.number, self._part.length
        )

    def __len__(self):
        return self._part.length

    def __iter__(self):
        while True:
            piece = self.read(_COPY_SIZE)
            if not piece:
                return
            yield piece

    def tell(self):
        return self._read

    def seek(self, offset, whence=0):
        # Requests rewinds a body this way to follow a redirect.
        if offset != 0 or whence != 0:
            raise io.UnsupportedOperation(
                "an upload part body can only be rewound"
            )
        self.rewind()
        return 0

    def rewind(self):
        self.close()
        self._read = 0

    def read(self, size: int | None = -1):
        source, part = self._source, self._part
        if self._file is None:
            self._file = open(source.path, "rb")
            source._check_live(self._file)
            self._file.seek(part.offset)
            self._hash = hashlib.sha256() if source.record_digests else None
        left = part.length - self._read
        if not left:
            return b""
        wanted = min(
            left, _COPY_SIZE if size is None or size < 0 else size, _COPY_SIZE
        )
        data = self._file.read(wanted)
        if len(data) != wanted:
            raise source._changed()
        self._read += wanted
        if self._hash is not None:
            self._hash.update(data)
        if self._read == part.length:
            source._check_live(self._file)
            if self._hash is not None:
                part.digest = self._hash.hexdigest()
        return data

    def close(self):
        if self._file is not None:
            self._file.close()
            self._file = None


class _StreamSource:
    """A binary stream the caller owns, read in order from where it is.

    The SDK never seeks or closes it. A short read is not the end: reading
    continues until the part is full, and only an empty read is the end.
    With a declared size, exactly that many bytes are read, and ending
    sooner fails the upload. Bytes a read returns beyond what was asked
    are kept for the next part and counted in the limiter.
    """

    ordered = True
    check_on_resume = True
    owned = False

    def __init__(self, stream, size, limiter):
        if not callable(getattr(stream, "read", None)):
            raise InvalidParameterError(
                "The upload source must be a binary stream with a read() method"
            )
        self._stream = stream
        self.size = size
        self._limiter = limiter
        self._carry = b""
        self._carry_reservation = None
        self.consumed = 0

    def read(self, length, lifetime, *, may_end=False):
        """The next length bytes, or fewer at the end when may_end. At most
        MAX_BUFFERED_PART of them are held: a longer read raises, at once
        when all length bytes are needed, and otherwise once that much is
        read and the stream has more."""
        if length > MAX_BUFFERED_PART:
            if may_end:
                data = self.read(MAX_BUFFERED_PART, lifetime, may_end=True)
                if len(data) < MAX_BUFFERED_PART or self.ended(lifetime):
                    return data
            raise _held_too_long()
        buffer = io.BytesIO()
        filled = 0
        if self._carry:
            filled = buffer.write(self._carry[:length])
            self._set_carry(self._carry[filled:])
        while filled < length:
            lifetime.check("reading the stream")
            wanted = min(length - filled, _READ_SIZE)
            data = self._stream.read(wanted)
            if data is None:
                # A non-blocking stream with no data ready yet. Treating
                # that as the end would upload a truncated file, and the
                # SDK does not wait for more.
                raise InvalidParameterError(
                    "The upload stream has no data ready but has not ended "
                    "(read() returned None). Uploads need a blocking stream."
                )
            if isinstance(data, str):
                raise InvalidParameterError(
                    "The upload stream returned text; open it in binary mode"
                )
            count = len(data)
            if not count:
                if may_end:
                    break
                raise InvalidRequestError(
                    "The upload stream ended after {} bytes, before the {} "
                    "bytes given as its size, so the upload was not "
                    "completed.".format(self.consumed + filled, self.size)
                )
            used = min(count, wanted)
            filled += buffer.write(memoryview(data)[:used])
            if count > used:
                self._set_carry(bytes(memoryview(data)[used:]))
        self.consumed += filled
        # A BytesIO holding exactly its bytes hands them over without a copy.
        return buffer.getvalue()

    def ended(self, lifetime):
        """Whether the stream has no more bytes: found by reading one, which
        the next read returns first."""
        if self._carry:
            return False
        data = self.read(1, lifetime, may_end=True)
        if not data:
            return True
        self.consumed -= len(data)
        self._set_carry(data + self._carry)
        return False

    def checkpoint_state(self):
        return {"size": self.size}

    def check(self, part, lifetime):
        """Read the part's bytes again, in order, and raise unless they are
        the ones a checkpoint recorded. Holds at most one read at a time."""
        found = hashlib.sha256()
        left = part.length
        while left:
            data = self.read(min(left, _READ_SIZE), lifetime)
            found.update(data)
            left -= len(data)
        if found.hexdigest() != part.digest:
            raise _different_stream(part)

    def _set_carry(self, carry):
        if self._carry_reservation is not None:
            self._carry_reservation.release()
            self._carry_reservation = None
        self._carry = carry
        if carry:
            self._carry_reservation = self._limiter._take(len(carry))

    def discard(self):
        self._set_carry(b"")


def _held_too_long():
    return InvalidRequestError(
        "A part of this upload would hold more than the {} bytes the SDK holds "
        "in memory for one part, so the upload was not completed. upload_file(), "
        "or upload_stream() with spool_limit, sends parts from a file "
        "instead.".format(MAX_BUFFERED_PART)
    )


def _different_stream(part):
    return InvalidRequestError(
        "The upload's bytes {} to {} differ from those the checkpoint recorded, "
        "so it was not resumed. Give the same bytes from the same start, or "
        "remove the checkpoint to upload them again.".format(
            part.offset, part.offset + part.length - 1
        )
    )


class _Progress:
    """The committed and sent byte counts of one upload, updated by its
    workers and reported from its coordinator."""

    def __init__(self, path, total, callback):
        self._lock = threading.Lock()
        self._path = path
        self._total = total
        self._callback = callback
        self._started = time.monotonic()
        self._samples: collections.deque[tuple[float, int]] = (
            collections.deque()
        )
        self._reported_at = 0.0
        self._reported = None
        self.committed = 0
        self.sent = 0
        self.parts = 0

    def add_sent(self, count):
        with self._lock:
            self.sent += count

    def elapsed(self):
        return time.monotonic() - self._started

    def commit(self, length):
        with self._lock:
            self.committed += length
            self.parts += 1

    def restore(self, committed, parts):
        """Count the parts an earlier call committed."""
        with self._lock:
            self.committed, self.parts = committed, parts

    def report(self, force=False):
        """Call the callback, at most every _PROGRESS_INTERVAL seconds
        unless force, when something has changed."""
        if self._callback is None:
            return
        now = time.monotonic()
        if not force and now - self._reported_at < _PROGRESS_INTERVAL:
            return
        with self._lock:
            counts = (self.committed, self.sent, self.parts)
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
            UploadProgress(
                path=self._path,
                total_bytes=self._total,
                bytes_committed=counts[0],
                bytes_sent=counts[1],
                parts_committed=counts[2],
                elapsed=now - self._started,
                bytes_per_second=rate,
            )
        )


class _Stale(Exception):
    """A part's URL, about to be sent again, has expired by what is known of
    its expiry."""


class _Session:
    """The part of an upload that talks to Files.com and storage: asking
    for parts, checking each grant against what the upload has already
    relied on, and sending one part."""

    def __init__(self, operation, destination, begin_params):
        self.operation = operation
        self.destination = destination
        self.begin_params = begin_params
        self.first: _Grant | None = None
        self.parallel = False
        # The planner, once the upload chooses its own part sizes.
        self.variable: _VariablePlanner | None = None
        # For an upload resumed from a checkpoint: its reference, and
        # whether its parts were sent with offsets.
        self.resumed_ref: str | None = None
        self.offsets: bool | None = None

    @property
    def ref(self):
        return self.first.ref if self.first is not None else self.resumed_ref

    @property
    def with_offsets(self):
        # Offsets are sent on every part or none, so the first part decides.
        if self.offsets is not None:
            return self.offsets
        return self.first is not None and self.first.offset_query

    def resume(self, operation, ref, number) -> "_Grant":
        """Continue the upload ref with a grant for part number."""
        self.resumed_ref = ref
        return self.begin(operation, number=number, count=1)[0]

    def begin(
        self, operation, size=None, number=1, count=None
    ) -> list[_Grant]:
        """Grants for parts number, number + 1, ...: count of them if
        count, else as many as the API gives. The first call starts the
        upload."""
        params = dict(self.begin_params)
        if self.ref is None:
            if size is not None:
                params["size"] = size
        else:
            params["ref"] = self.ref
            params["part"] = number
            if count and count > 1:
                params["parts"] = count
        from files_sdk.api import path_value

        path = "/file_actions/begin_upload/{}".format(
            path_value(self.destination)
        )
        # Sent again after a lost answer: an upload Files.com began but the
        # SDK never heard of is never completed, and a part's URL can be
        # issued again.
        response = operation.replay_safe().request("POST", path, params)
        records = response.data
        if not isinstance(records, list) or not records:
            raise unexpected_response_error(
                response, "begin_upload returned no parts"
            )
        grants = [_Grant.parse(response, record) for record in records]
        for index, grant in enumerate(grants):
            self._check(response, grant, number + index)
        if self.first is None:
            grants[0] = self._described(grants[0], records, number)
            self.first = grants[0]
        return grants[: count or len(grants)]

    def _described(self, first, records, number):
        """first, the first grant of the session's first answer (records,
        the first for part number), with the kind of storage its parts show
        when Files.com names none the SDK knows: s3 when every part of the
        answer is for one ordinary multipart upload straight to Amazon S3
        (_aws_multipart_route), as the .NET SDK reads one (UploadGrant.Of).
        Only an answer to a request for direct connection information can
        show that the parts go to no Files.com Agent or Integration Worker:
        without that request, or with any such information in the answer,
        complete or not, the kind stays generic. A kind Files.com names
        stays as named. It chooses defaults, and grants nothing."""
        if self.begin_params.get("with_direct_connection_info") is not True:
            return first
        if any(
            record.get("upload_target_class") in TARGET_CLASSES
            for record in records
        ):
            return first
        routes = [
            _aws_multipart_route(record, number + index)
            for index, record in enumerate(records)
        ]
        if routes[0] is None or any(route != routes[0] for route in routes):
            return first
        return dataclasses.replace(first, target_class="s3")

    def _check(self, response, grant, number):
        """Raise, before any of its bytes are sent, if a grant does not fit
        the parts the upload has already planned and sent."""
        problem = None
        if grant.number != number:
            problem = "part {} was returned for part {}".format(
                grant.number, number
            )
        elif self.ref is not None and grant.ref != self.ref:
            problem = "part {} belongs to a different upload".format(number)
        elif self.first is not None or self.resumed_ref is not None:
            if self.with_offsets and not grant.offset_query:
                problem = (
                    "part {} withdrew the part_offset the upload sends".format(
                        number
                    )
                )
            elif self.parallel and not grant.parallel:
                problem = "part {} withdrew permission to send parts in parallel".format(
                    number
                )
            elif self.variable is not None and not (
                grant.variable_limits is not None
                and grant.variable_limits.covers(self.variable)
            ):
                problem = "part {} withdrew or narrowed the part sizes the upload chose".format(
                    number
                )
        limit = (self.first or grant).available_parts
        if problem is None and limit is not None and number > limit:
            problem = "the upload needs more than the {} parts allowed".format(
                limit
            )
        if problem is not None:
            raise unexpected_response_error(response, problem)

    def renew(self, operation, part) -> _Grant:
        """A new grant for part, the same part with a fresh URL."""
        [grant] = self.begin(operation, number=part.number, count=1)
        # _check has already required a variable grant to cover the part.
        if self.variable is None and grant.partsize != part.partsize:
            raise InvalidRequestError(
                "Files.com changed the size of part {} of this upload when "
                "renewing its URL, so it was not sent again and the upload "
                "was not completed.".format(part.number)
            )
        return grant

    def send(self, operation, part, data, sent, permit=None):
        """Send part's bytes (bytes, or a _PartBody), renewing its URL when
        it has expired: before sending it at all, once its known expiry has
        come; before sending it again after a failure, once that time has
        come by the end of the retry's wait; and after storage refuses it as
        expired, either saying so or once that time has come, if parts may be
        sent again. A URL Files.com has just given is first sent as given,
        however soon it expires. Renewals are at most _MAX_RENEWALS in all
        (a part with no URL yet gets its first without counting); a retry
        whose URL has expired with none left is not sent, and the part fails
        with its last attempt's error. Any other refusal is raised. Returns
        the ETag storage gave, or None.
        sent hears the bytes of each attempt. permit, if given, is the
        controller's permit for the first attempt: each attempt holds one,
        from when it is admitted until it ends, and every later attempt
        waits for a fresh one, so none is held through a retry's delay. A
        renewal of the part's URL, before any attempt or after a refusal, is
        negotiation, not an attempt: the permit goes back for it and the
        attempt after it waits for a fresh one. The controller hears
        each attempt go to the network once its request is built and logged,
        its response's headers arrive (with any throttle and Retry-After they
        announce, which hold later attempts back even if the body then
        fails), and how it ended once its body is read, or that it stopped
        with the operation, which teaches it nothing. The permit goes back
        however sending ends."""
        renewals = 0
        # Attempts with the URL being sent, so that a retry is told apart.
        tries = 0
        # Without a permit: when a throttle its response's headers announced
        # ends, even if the body that followed them failed.
        throttled_until = 0.0

        def attempt():
            # The request is about to be built: take a permit, if this
            # attempt has none yet (behind any cooldown), and send the body
            # from its start. A retry whose URL has expired by now, its
            # waits over, is never sent: the URL is renewed first, or, with
            # no renewal left, the part fails as the attempt before did.
            nonlocal tries
            if permit is not None:
                permit.acquire(operation.lifetime)
            elif throttled_until > time.monotonic():
                operation.lifetime.sleep(
                    throttled_until - time.monotonic(), "retry wait"
                )
            tries += 1
            if tries > 1 and expiring(grant.expires):
                if renewals < _MAX_RENEWALS:
                    raise _Stale()
                raise _RetryDeclined(
                    "The part was not sent again: its URL had expired, and had "
                    "been renewed as often as the SDK allows."
                )
            rewind = getattr(data, "rewind", None)
            if rewind is not None:
                rewind()
            sent(len(data))

        def sending():
            if permit is not None:
                permit.begin()

        def answered(status, retry_after):
            nonlocal throttled_until
            if permit is not None:
                permit.answered(status, retry_after)
            elif retry_after:
                # Only a throttle (429, 503 or 504) carries one; a shorter
                # one never shortens the wait.
                throttled_until = max(
                    throttled_until, time.monotonic() + retry_after
                )

        def outcome(status, retry_after):
            if permit is not None:
                permit.end(status, retry_after, len(data))

        def abandoned():
            if permit is not None:
                permit.release()

        try:
            # A part with no URL yet, or one that expired while it waited, gets
            # a new one before anything is sent. Every URL renewed after that
            # is first sent as given.
            grant = part.grant
            if grant is None or expiring(grant.expires):
                if permit is not None:
                    permit.release()
                if grant is not None:
                    renewals += 1
                part.grant = grant = self.renew(operation, part)
            while True:
                headers = dict(grant.headers)
                headers["Content-Length"] = str(len(data))
                tries = 0
                try:
                    response = operation.api_client.send_remote_request(
                        grant.method,
                        grant.url(part.offset, self.with_offsets),
                        headers,
                        data,
                        may_retry=lambda: grant.retry,
                        on_attempt=attempt,
                        on_outcome=outcome,
                        on_send=sending,
                        on_headers=answered,
                        on_abandon=abandoned,
                    )
                except _Stale:
                    # Nothing was sent with it. The renewal is negotiation:
                    # the permit goes back, and the part is sent to its new
                    # URL with a fresh one.
                    if permit is not None:
                        permit.release()
                    renewals += 1
                    part.grant = grant = self.renew(operation, part)
                    continue
                except APIError as error:
                    if (
                        refused_as_expired(error, grant.expires)
                        and grant.retry
                        and renewals < _MAX_RENEWALS
                    ):
                        renewals += 1
                        part.grant = grant = self.renew(operation, part)
                        continue
                    if not grant.retry:
                        error.add_note(
                            "Files.com does not allow parts of this upload to be "
                            "sent again, so the whole upload must be started again."
                        )
                    raise _for_transfer(
                        error, "the upload of {}".format(self.destination)
                    )
                etag = response.headers.get("ETag")
                return etag.strip('"') if etag else None
        finally:
            if permit is not None:
                permit.release()
            close = getattr(data, "close", None)
            if close is not None:
                close()

    def finish(self, size, etags, finish_params, completion=None) -> Any:
        """Complete the upload within completion (this upload's operation's
        completion(), by default): the request is not sent again once it
        may have been received, and a lost answer raises."""
        from files_sdk.models.file import FileResource

        params = dict(finish_params)
        params.update(
            {
                "action": "end",
                "etags": [
                    {"etag": etag, "part": number}
                    for number, etag in sorted(etags.items())
                    if etag
                ],
                "ref": self.ref,
                "size": size,
            }
        )
        return FileResource(completion or self.operation.completion()).create(
            self.destination, params
        )


def _not_completed(completion, error):
    """Whether error proves the request that completes an upload did not
    complete it: it was never handed to the network, the SDK knows it was
    not sent, or Files.com's answer shows it was not carried out (see
    APIError.remote_outcome_unknown). Anything else once it may have been
    sent, an error answer of any status included, leaves the upload possibly
    complete."""
    if not completion.dispatched:
        return True
    if isinstance(error, (APIConnectionError, OperationCancelledError)):
        return error.phase == "request" and not error.remote_outcome_unknown
    return isinstance(error, APIError) and not error.remote_outcome_unknown


class _Paused(Exception):
    """The upload's pause token was paused."""


class _Upload:
    """One upload of a local file or a stream of known size, from its first
    request to the one that completes it. See the module docstring."""

    def __init__(
        self,
        operation,
        destination,
        source,
        params,
        max_concurrency,
        progress,
        tuning,
        pause=None,
        scope=None,
    ):
        begin_params, self.finish_params = split_params(params)
        # Asked for with every negotiation, as the .NET SDK asks, unless the
        # caller says otherwise: only an answer to it can show that the parts
        # go to no Files.com Agent or Integration Worker, which an ordinary
        # S3 upload needs before its kind is read from its parts
        # (_Session._described). The parts are still sent to the URLs given.
        begin_params.setdefault("with_direct_connection_info", True)
        self.operation = operation
        self.source = source
        self.destination = destination
        self.session = _Session(operation, destination, begin_params)
        self.requested_concurrency = checked_upload_concurrency(
            max_concurrency
        )
        # A job's shared learning, if the upload belongs to one.
        self.scope: UploadScope | None = scope
        # The file's part-size feedback, under the scaled S3 policy.
        self.sizer: _SizeFeedback | None = None
        # Whether parts wait only for a permit, as file admission sees it.
        self.waiting_for_permit = False
        self.tuning = checked_tuning(tuning, operation.context)
        self.limiter = operation.context.transfer_limiter
        self.progress = _Progress(
            destination, source.size, checked_progress(progress)
        )
        self.pause = checked_pause(pause)
        # Where the upload keeps its checkpoint, if it has one.
        self.store: Any = None
        # Stops the workers' requests: cancelled when the operation stops,
        # and when the upload fails, so that its other parts stop too.
        self.stopping = CancellationToken()
        lifetime = operation.lifetime
        self.lifetime = Lifetime(
            lifetime.closing, self.stopping, lifetime.deadline
        )
        from files_sdk.api import Operation

        self.workers = Operation(None, self.lifetime, _state=operation._state)
        self.in_flight: dict[
            concurrent.futures.Future[Any], tuple[_Part, _Reservation]
        ] = {}
        self.ready: collections.deque[tuple[_Part, _Reservation, Any]] = (
            collections.deque()
        )
        # Every part placed so far, and the numbers of those that arrived.
        self.placed: dict[int, _Part] = {}
        self.committed: set[int] = set()
        self.etags: dict[int, str | None] = {}
        self.planner: _Planner = _Planner(source.size)
        self.controller: Controller | None = None
        self.settings: Any = None
        self.plan = "server"
        self.resumed = False
        self.completion = "pending"
        # Whether parts arrived since the checkpoint was last saved.
        self.dirty = False
        # Whether the checkpoint's state was forgotten because the source was
        # seen to change (_invalidate): nothing is saved after that.
        self.invalidated = False
        # Delivers observations, when tuning has an observer.
        self.observer: Observer | None = None

    def run(self):
        stop_watching = self.operation.lifetime.watch(self.stopping.cancel)
        # Workers start only as parts do. A part waiting to be sent again
        # keeps its worker but not its permit, so there can be up to twice
        # as many parts in progress as attempts.
        executor = concurrent.futures.ThreadPoolExecutor(
            2 * MAX_UPLOAD_CONCURRENCY, thread_name_prefix="files_sdk upload"
        )
        if self.scope is not None:
            self.scope.joined(self)
        outcome = "failed"
        try:
            paused = False
            try:
                try:
                    self._send_parts(executor)
                except _Paused:
                    self._drain()
                    # What arrived is kept for resuming only while it is of
                    # the file as it is: a change seen while draining, or
                    # found now, fails the upload instead, which forgets it.
                    self._check_source()
                    paused = True
            except BaseException as error:
                # Stop the other parts and wait for them before raising.
                self.stopping.cancel()
                self._settle()
                primary = self._primary(error)
                self._save_quietly(primary)
                raise primary from None
            if paused:
                outcome = "paused"
                self._save_state(final=True)
                raise TransferPausedError(
                    "The upload to {} was paused. Upload it again with the same "
                    "checkpoint to resume it.".format(self.destination),
                    checkpoint=self.store.path,
                )
            file = self._complete()
            outcome = "completed"
            return file
        finally:
            executor.shutdown(wait=True)
            stop_watching()
            if self.scope is not None:
                self.scope.left(self)
            if self.sizer is not None and self.controller is not None:
                self.controller.remove_sizer(self.sizer)
            if isinstance(self.source, _StreamSource):
                self.source.discard()
            if self.observer is not None:
                _finish_observing(
                    self.observer, self._observed_details(outcome)
                )

    def _observed_details(self, outcome=None):
        """What an observation records of the upload: never its paths."""
        settings = self.settings
        details = {
            "target_class": (
                settings.target_class if settings is not None else None
            ),
            "adaptive": settings.adaptive if settings is not None else None,
            "policy": settings.policy if settings is not None else None,
            "startup": settings.startup if settings is not None else None,
            "plan": self.plan,
            "parallel": self.session.parallel,
            "max_concurrency": (
                settings.max_concurrency if settings is not None else None
            ),
            "size": self.source.size,
            "resumed": self.resumed,
            # Whose budget bounds it: the client's own, or one the caller gave.
            "limiter": "client" if self.limiter._owned else "caller",
            "limiter_max_parts": self.limiter.max_parts,
            "limiter_max_bytes": self.limiter.max_bytes,
            "shared_controller": (
                self.controller.shared if self.controller is not None else None
            ),
        }
        if outcome is None:
            return details
        return {
            **details,
            "outcome": outcome,
            "parts": self.progress.parts,
            "bytes_committed": self.progress.committed,
            "bytes_sent": self.progress.sent,
        }

    def _has_runway(self):
        # Parts are read ahead only from a stream sent in parallel.
        return self.source.ordered and self.session.parallel

    def _observed_state(self):
        runway = self._has_runway()
        return (
            self._target_now() if self.session.parallel else 1,
            sum(1 for future in self.in_flight if not future.done()),
            len(self.ready) if runway else None,
            (
                sum(part.length for part, _reservation, _data in self.ready)
                if runway
                else None
            ),
            (
                self.controller.attempts_in_progress()
                if self.controller is not None
                else None
            ),
        )

    def _complete(self):
        try:
            self.progress.report(force=True)
            self.operation.lifetime.check("completing the upload")
            self._check_source()
        except BaseException as error:
            # Still pending: the checkpoint keeps what it last saved, unless
            # the file is seen to have changed (_forget_if_changed).
            self._forget_if_changed(error)
            raise
        # Saved, to disk, before the request that completes the upload is
        # sent: if the process dies or the answer is lost from here on, a
        # later call finds the upload may be complete, and does not
        # complete it again.
        self.completion = "completing"
        try:
            self._save_state(final=True, durable=True)
        except BaseException as error:
            # Not known to be on disk, so the upload is not completed; it
            # stays pending for a later call, if the checkpoint can say so.
            self.completion = "pending"
            self._save_quietly(error)
            raise
        completion = self.operation.completion()
        try:
            file = self.session.finish(
                self.source.size, self.etags, self._finish_params(), completion
            )
        except BaseException as error:
            self.completion = (
                "pending" if _not_completed(completion, error) else "uncertain"
            )
            self._save_quietly(error)
            raise
        if self.store is not None:
            self.store.clear()
        self._log_summary()
        return file

    def _primary(self, error):
        """The error to raise for a failed upload. Parts stopped because the
        caller cancelled, closed the client or ran out of time raise that
        stop, which left the upload incomplete: nothing it asked Files.com
        to do can have taken effect."""
        lifetime = self.operation.lifetime
        if lifetime.stopped and isinstance(
            error, (OperationCancelledError, DeadlineExceededError)
        ):
            return lifetime.stopped_error("uploading")
        return error

    def _finish_params(self):
        params = dict(self.finish_params)
        if (
            isinstance(self.source, _PathSource)
            and self.source.mtime is not None
        ):
            params.setdefault("provided_mtime", utc_mtime(self.source.mtime))
        return params

    def _setup(self, first, plan=None):
        """Choose how the upload goes, from its first grant: in parallel only
        when Files.com allows it; adaptively unless tuning says not; with
        part sizes of its own only when Files.com grants them and they can
        fit the file. A resumed upload keeps the plan it had. Sets the
        planner."""
        size = self.source.size
        target_class = first.target_class if first is not None else "generic"
        settings = self.tuning.settings(target_class, self._cap(target_class))
        self.settings = settings
        if first is None:
            return
        self.session.parallel = first.parallel and settings.max_concurrency > 1
        if self.scope is not None and settings.adaptive:
            # A job's adaptive uploads of one kind share a controller, and so
            # one request budget and what it learns: a file Files.com asks to
            # send one part at a time, or every file under a cap of one,
            # included. Such a file still sends one part at a time.
            self.controller = self.scope.controller(settings)
        elif self.session.parallel:
            # A static upload, or one on its own, keeps its own budget.
            self.controller = Controller(settings)
        limits = first.variable_limits
        # The part numbers an upload choosing its sizes may use: what its
        # variable limits allow, and no more than Files.com makes available.
        available = first.available_parts
        if plan == "variable" and (
            limits is None or not limits.fits(size, available)
        ):
            raise self._cannot_resume(
                "Files.com no longer lets it choose its own part sizes"
            )
        if limits is not None and size > 0 and plan != "server":
            if limits.fits(size, available):
                if settings.size_feedback and self.controller is not None:
                    preferred = _preferred_part_size(
                        settings, size, settings.initial_concurrency
                    )
                    self.sizer = _SizeFeedback(
                        self.controller, preferred, limits.max_part_bytes
                    )
                    self.controller.add_sizer(self.sizer)
                planner = _VariablePlanner(
                    size,
                    limits,
                    settings,
                    self._target_now,
                    self.sizer,
                    available,
                )
                self.session.variable = planner
                self.plan = "variable"
                self.planner = planner
                return
            if (
                available is not None
                and limits.fits(size)
                and math.ceil(size / max(first.partsize, 1)) > available
            ):
                # Neither sizes of its own nor Files.com's fit the part
                # numbers available: refused before anything is sent.
                raise InvalidRequestError(
                    "The upload to {} needs more parts than the {} Files.com makes available for it, "
                    "so nothing was sent.".format(self.destination, available)
                )
            self.plan = "server (variable_part_limits cannot fit the file)"
        self.planner = _Planner(size)

    def _cap(self, target_class):
        if self.requested_concurrency is not None:
            return self.requested_concurrency
        return (
            default_max_concurrency(target_class, self.tuning)
            if self.tuning.adaptive
            else DEFAULT_MAX_CONCURRENCY
        )

    def _target_now(self):
        """How many parts the controller wants in progress now: none during
        a cooldown."""
        if not self.session.parallel or self.controller is None:
            return 1
        return 0 if self.controller.pause_left() else self.controller.target

    def _limit(self):
        """How many parts may be in progress now: one at a time without a
        controller; with one, those in progress and as many more as it has
        permits for. A part waiting to be sent again holds no permit, so
        parts in progress can exceed the target, but never twice the
        upload's maximum, nor one for a file sending one part at a time."""
        if self.controller is None:
            return 1
        most = (
            2 * self.settings.max_concurrency if self.session.parallel else 1
        )
        return min(most, len(self.in_flight) + self.controller.room())

    def queued(self):
        """Parts ready to start that wait only for a permit, as a job's
        file admission counts them."""
        return len(self.ready) + (1 if self.waiting_for_permit else 0)

    def _note(self, shortfall):
        if self.controller is not None:
            self.controller.note_shortfall(shortfall)

    # Beginning or resuming.

    def _start(self):
        """Begin the upload, or resume the one its checkpoint records.
        Returns the grants to place new parts with, and the parts placed
        before that must be sent, or read again and checked, in order."""
        state = self.store.load() if self.store is not None else None
        if state is not None:
            resumed = self._resume(state)
            if resumed is not None:
                self.resumed = True
                return resumed
        first = self.session.begin(self.operation, size=self.source.size)[0]
        self._setup(first)
        self._save_state(final=True)
        return collections.deque([first]), collections.deque()

    def _resume(self, state):
        """Continue the upload a checkpoint recorded, or return None to start
        again when it no longer applies."""
        try:
            ref, plan, offsets = state["ref"], state["plan"], state["offsets"]
            rows = state["parts"]
            parts = [
                _Part(row[0], row[1], row[2], None, row[3], row[6])
                for row in rows
            ]
            etags = {row[0]: row[5] for row in rows if row[4]}
            number, offset, latest = state["next"]
            completion, source_state = state["completion"], state["source"]
            valid = (
                isinstance(ref, str)
                and plan in ("server", "variable")
                and all(
                    part.number == index + 1
                    for index, part in enumerate(parts)
                )
                and all(
                    later.offset == earlier.offset + earlier.length
                    for earlier, later in zip(parts, parts[1:])
                )
                and number == len(parts) + 1
                and offset
                == (parts[-1].offset + parts[-1].length if parts else 0)
            )
        except (KeyError, TypeError, ValueError, IndexError):
            valid = False
        if not valid:
            raise InvalidRequestError(
                "The checkpoint {} does not describe an upload. Remove it to "
                "upload again.".format(self.store.path)
            )
        if source_state != self.source.checkpoint_state():
            util.log_info(
                "Upload checkpoint not used",
                reason="the source changed",
                destination=self.destination,
            )
            return None
        if completion in ("completing", "uncertain"):
            raise APIConnectionError(
                "An earlier attempt to complete the upload to {0} may have "
                "succeeded, so it was not completed again. Check whether {0} is "
                "there; remove the checkpoint {1} to upload it again.".format(
                    self.destination, self.store.path
                ),
                remote_outcome_unknown=True,
            )
        self.placed = {part.number: part for part in parts}
        self.committed = set(etags)
        self.etags = dict(etags)
        self.progress.restore(
            sum(part.length for part in parts if part.number in etags),
            len(etags),
        )
        self.session.offsets = offsets
        incomplete = [part for part in parts if part.number not in etags]
        planned = number > 1 and offset >= self.source.size
        grants: collections.deque[_Grant] = collections.deque()
        if incomplete or not planned:
            wanted = incomplete[0].number if incomplete else number
            try:
                first = self.session.resume(self.operation, ref, wanted)
            except APIError as error:
                if error.http_status != 404:
                    raise
                util.log_info(
                    "Upload checkpoint not used",
                    reason="Files.com no longer has the upload",
                    destination=self.destination,
                )
                self._forget()
                return None
            self._setup(first, plan)
            if incomplete:
                if (
                    self.session.variable is None
                    and first.partsize != incomplete[0].partsize
                ):
                    raise self._cannot_resume(
                        "Files.com changed the size of part {}".format(wanted)
                    )
                incomplete[0].grant = first
            else:
                grants.append(first)
        else:
            self.session.resumed_ref = ref
            self._setup(None)
        self.planner.restore(number, offset, latest, parts)
        variable = self.session.variable
        first = self.session.first
        if (
            variable is not None
            and first is not None
            and not (
                first.variable_limits is not None
                and first.variable_limits.covers(variable)
            )
        ):
            raise self._cannot_resume(
                "Files.com narrowed the part sizes it chose"
            )
        replay = collections.deque(
            parts if self.source.check_on_resume else incomplete
        )
        return grants, replay

    def _cannot_resume(self, why):
        return InvalidRequestError(
            "The upload to {} cannot be resumed because {}, so nothing more was "
            "sent. Remove the checkpoint {} to upload it again.".format(
                self.destination, why, self.store.path
            )
        )

    def _forget(self):
        """Start again instead of resuming."""
        self.session = _Session(
            self.operation, self.destination, self.session.begin_params
        )
        self.placed, self.committed, self.etags = {}, set(), {}
        self.progress.restore(0, 0)

    # Sending parts.

    def _send_parts(self, executor):
        if self.pause is not None and self.pause.paused:
            raise _Paused()
        grants, replay = self._start()
        if self.tuning.observer is not None:
            # Only the waits this upload can have: the runway's for a stream
            # sent in parallel, the storage service's cooldown with a
            # controller.
            waits = ["limiter"]
            if self._has_runway():
                waits.append("runway")
            if self.controller is not None:
                waits.append("backpressure")
            self.observer = Observer(
                self.tuning.observer, self._observed_state, waits
            )
            self.observer.watch(self.controller)
            self.observer.knobs = knobs(self.settings)
            self.observer.start(self._observed_details())
        observer = self.observer
        planner = self.planner
        ready_bytes = 0
        # Since when the runway has been full with every worker busy.
        blocked_at = None
        # Whether a part was refused as it started, this round.
        refused = False

        def start_or_hold(part, prepared):
            """Start a part just prepared, or keep it ready to start first
            when backpressure or a smaller target came while it was being
            prepared. Returns whether it started."""
            nonlocal ready_bytes
            if self._start_part(executor, part, *prepared):
                return True
            self.ready.append((part, *prepared))
            ready_bytes += part.length
            return False

        while not planner.done or replay or self.ready or self.in_flight:
            if self.pause is not None and self.pause.paused:
                raise _Paused()
            # Read once a round to choose what to prepare; whether a part may
            # start is decided again as it starts. A part read but not
            # started holds room in the limiter that only starting it frees.
            # So while any is ready, room to read or check another is taken
            # only if the limiter grants it at once, before the part is
            # placed. Without that room, and after a refusal, the round goes
            # on to collect parts or wait out the cooldown, which is what
            # lets ready parts start.
            limit = self._limit()
            refused = False
            while self.ready and len(self.in_flight) < limit:
                part, reservation, data = self.ready.popleft()
                if not self._start_part(executor, part, reservation, data):
                    self.ready.appendleft((part, reservation, data))
                    refused = True
                    break
                ready_bytes -= part.length
            while replay and not refused:
                # Parts placed before the upload was resumed, in order.
                part = replay[0]
                if part.number in self.committed:
                    # Arrived already: its bytes are read again only to
                    # check they are the same.
                    if not self._check_committed(part, wait=not self.ready):
                        break
                    replay.popleft()
                    continue
                if len(self.in_flight) >= limit:
                    break
                reservation = self._admit(
                    self._charge(part.length), wait=not self.ready
                )
                if reservation is None:
                    break
                replay.popleft()
                refused = not start_or_hold(
                    part, self._prepare(part, reservation)
                )
            while not replay and not planner.done and not refused:
                if not grants:
                    if not self.session.parallel:
                        if self.in_flight:
                            break  # One at a time: the next part waits for this one.
                        grants.extend(
                            self.session.begin(
                                self.operation, number=planner.number
                            )
                        )
                    else:
                        # Grants for the free workers and the runway, in one request.
                        wanted = (
                            max(limit, 1)
                            - len(self.in_flight)
                            + self.settings.ready_parts
                        )
                        count = max(1, min(wanted, planner.parts_left()))
                        grants.extend(
                            self.session.begin(
                                self.operation,
                                number=planner.number,
                                count=count,
                            )
                        )
                length = planner.length(grants[0])
                if len(self.in_flight) < limit or self._runway_has_room(
                    length, ready_bytes
                ):
                    if blocked_at is not None and observer is not None:
                        observer.waited(
                            "runway", time.monotonic() - blocked_at
                        )
                    blocked_at = None
                if len(self.in_flight) < limit:
                    placed = self._read_next_part(
                        grants, length, wait=not self.ready
                    )
                    if placed is None:
                        break
                    part, prepared = placed
                    refused = not start_or_hold(part, prepared)
                elif self._runway_has_room(length, ready_bytes):
                    # Every worker is busy: read the next part ahead.
                    placed = self._read_next_part(
                        grants, length, wait=not self.ready
                    )
                    if placed is None:
                        break
                    part, prepared = placed
                    self.ready.append((part, *prepared))
                    ready_bytes += part.length
                else:
                    # Only a stream's read-ahead is a runway to wait for: a
                    # file's parts held ready were refused as they started.
                    if (
                        blocked_at is None
                        and self.ready
                        and self._has_runway()
                    ):
                        blocked_at = time.monotonic()
                    break
            controller = self.controller
            left = bool(self.ready or replay or not planner.done)
            self.waiting_for_permit = (
                controller is not None and left and controller.room() == 0
            )
            if (
                controller is not None
                and not self.session.parallel
                and self.in_flight
                and left
            ):
                # This file sends one part at a time, which is not the
                # network's capacity.
                self._note("serial parts")
            if self.in_flight:
                self._collect(timeout=_PROGRESS_INTERVAL)
                self.operation.lifetime.check("uploading")
                self.progress.report()
                self._save_state()
            elif controller is not None and controller.pause_left():
                # The storage service asked to wait before sending more.
                cooldown = min(controller.pause_left(), _PROGRESS_INTERVAL)
                self.operation.lifetime.sleep(cooldown, "waiting to upload")
                if observer is not None:
                    observer.waited("backpressure", cooldown)
            elif self.waiting_for_permit and controller is not None:
                # Other uploads of the job hold every permit.
                controller.wait_for_room(_PROGRESS_INTERVAL)
                self.operation.lifetime.check("uploading")
            if observer is not None:
                observer.poll()

    def _place(self, grant, length=None):
        part = self.planner.place(grant, length)
        self.placed[part.number] = part
        return part

    def _runway_has_room(self, length, ready_bytes):
        settings = self.settings
        return (
            self._has_runway()
            and len(self.ready) < settings.ready_parts
            and ready_bytes + length <= settings.ready_bytes
        )

    def _admit(self, size, wait=True):
        """A reservation of size bytes in the limiter, once there is room.
        While waiting, the parts in progress are collected and a pause is
        heard. With wait False, the reservation only if the limiter grants
        it now, otherwise None. Time without that room is the limiter's, not
        the network's: the controller hears so."""
        if not wait:
            reservation = _admitted_now(self.limiter, size)
            self._note(
                "no part ready" if reservation is not None else "limiter"
            )
            return reservation

        def while_waiting():
            if self.pause is not None and self.pause.paused:
                raise _Paused()
            self._collect(timeout=0)
            self.progress.report()

        reservation = _admitted(
            self.limiter,
            size,
            self.operation.lifetime,
            while_waiting,
            lambda: self._note("limiter"),
        )
        self._note("no part ready")
        return reservation

    def _charge(self, length):
        """The room in the limiter a part of length holds: a stream's part
        its whole length, since its bytes are held from before they are read
        until storage answers; a local file's part the copy buffer it is
        sent through, unless it is no larger, or DEBUG logging is on, which
        logs every byte of a part it reads whole, up to MAX_BUFFERED_PART."""
        if self.source.ordered or length <= _COPY_SIZE:
            return length
        if util.enabled(logging.DEBUG) and length <= MAX_BUFFERED_PART:
            return length
        return _COPY_SIZE

    def _check_committed(self, part, wait=True):
        """Read a part that arrived before the upload was resumed again, a
        piece at a time, to check it is the same, holding room in the
        limiter for the piece it reads while it does. Returns whether it
        did: with wait False, only if the limiter has that room now."""
        reservation = self._admit(min(part.length, _READ_SIZE), wait)
        if reservation is None:
            return False
        try:
            if self.observer is not None:
                self.observer.waited("limiter", reservation.waited)
            self.source.check(part, self.lifetime)
        finally:
            reservation.release()
        return True

    def _read_next_part(self, grants, length, wait):
        """The next part, of length, placed with the first of grants and
        read within room taken for it in the limiter: the part and what
        _prepare returns. With wait False, None, placing nothing, unless
        the limiter has the room now. The room goes back if placing or
        reading fails."""
        reservation = self._admit(self._charge(length), wait)
        if reservation is None:
            return None
        try:
            part = self._place(grants.popleft(), length)
        except BaseException:
            reservation.release()
            raise
        return part, self._prepare(part, reservation)

    def _prepare(self, part, reservation):
        """Within reservation, part's room in the limiter, read part now
        when the source must be read in order, or when a local file's part
        is held whole (no larger than its copy buffer, or for DEBUG
        logging): reading is preparation, done before the part may start,
        never within an attempt or its permit. Returns the reservation and
        the bytes, or None for a file's part read as it is sent."""
        try:
            # Within the reservation's cleanup: an observer can raise.
            if self.observer is not None:
                self.observer.waited("limiter", reservation.waited)
            data = None
            if self.source.ordered:
                data = self.source.read(part.length, self.lifetime)
            elif reservation.size >= part.length:
                data = self.source.read_part(part, self.lifetime)
        except BaseException:
            reservation.release()
            raise
        if data is not None and self.store is not None and self.source.ordered:
            part.digest = hashlib.sha256(data).hexdigest()
        return reservation, data

    def _start_part(self, executor, part, reservation, data):
        """Hand a prepared part to a worker if a new part may start now, and
        return whether it did. Preparing it can take a while, and a worker
        can report backpressure meanwhile; with a controller, the check, the
        permit for the part's first attempt and the hand-off are one step
        under its lock."""
        if not self.session.parallel:
            # One part at a time: Files.com asks for that, or the cap is one.
            if self.in_flight:
                return False
            if self.controller is None:
                self._submit(executor, part, reservation, data)
                return True
        if self.controller is None:
            return False
        return self.controller.admit(
            lambda permit: self._submit(
                executor, part, reservation, data, permit
            )
        )

    def _submit(self, executor, part, reservation, data, permit=None):
        if permit is not None:
            permit.sizer = self.sizer
        try:
            future = executor.submit(
                self._transfer, part, data, reservation, permit
            )
        except BaseException:
            # Controller.admit takes the permit back.
            reservation.release()
            raise
        self.in_flight[future] = (part, reservation)

    def _transfer(self, part, data, reservation, permit=None):
        # Runs in a worker thread. The part's room goes back as soon as it
        # is done, even while the coordinator is busy reading a stream, and
        # its permit as soon as each attempt ends.
        try:
            if data is None:
                data = self.source.body(part, self.lifetime)
            return self.session.send(
                self.workers, part, data, self.progress.add_sent, permit
            )
        finally:
            if permit is not None:
                permit.release()
            del data
            reservation.release()

    def _collect(self, timeout, keep_going=False):
        """Record the parts that have finished, raising the first failure
        unless keep_going."""
        done, _ = concurrent.futures.wait(
            list(self.in_flight),
            timeout=timeout,
            return_when=concurrent.futures.FIRST_COMPLETED,
        )
        arrived = False
        for future in done:
            part, reservation = self.in_flight.pop(future)
            reservation.release()
            error = future.exception()
            if error is not None:
                if keep_going:
                    continue
                raise error
            self.etags[part.number] = future.result()
            self.committed.add(part.number)
            self.progress.commit(part.length)
            arrived = True
        if arrived:
            self.dirty = True
            self._save_state()

    def _drain(self):
        """Let the parts in progress finish, keeping those that arrive and
        leaving those that fail to be sent again on resuming, and give back
        the room of parts read ahead."""
        while self.ready:
            _part, reservation, _data = self.ready.popleft()
            reservation.release()
        while self.in_flight:
            self._collect(timeout=_PROGRESS_INTERVAL, keep_going=True)
            self.operation.lifetime.check("pausing the upload")
            self.progress.report()
            self._save_state()

    def _settle(self):
        """Wait for the parts still in progress, keeping none of them, and
        give back the room of parts read ahead."""
        for future, (_part, reservation) in list(self.in_flight.items()):
            concurrent.futures.wait([future])
            reservation.release()
        self.in_flight.clear()
        while self.ready:
            _part, reservation, _data = self.ready.popleft()
            reservation.release()

    # Checkpoints.

    def _state(self):
        planner = self.planner
        parts = sorted(self.placed.values(), key=lambda part: part.number)
        return {
            "source": self.source.checkpoint_state(),
            "ref": self.session.ref,
            "plan": (
                "variable" if self.session.variable is not None else "server"
            ),
            "offsets": self.session.with_offsets,
            "parts": [
                [
                    part.number,
                    part.offset,
                    part.length,
                    part.partsize,
                    part.number in self.committed,
                    self.etags.get(part.number),
                    part.digest,
                ]
                for part in parts
            ],
            "next": [planner.number, planner.offset, planner.latest],
            "completion": self.completion,
        }

    def _save_state(self, final=False, durable=False):
        """Save the checkpoint: when final, or when parts arrived since the
        last save and a save is due, so progress is saved within about a
        second even while the parts in progress take longer. durable
        writes it to disk now, even as a job's slot. Nothing is saved once
        the source was seen to change, nor once the state was forgotten
        (_invalidate)."""
        if (
            self.store is None
            or self.session.ref is None
            or self.invalidated
            or self._source_changed()
        ):
            return
        if not final and not (self.dirty and self.store.due()):
            return
        self.dirty = False
        self.store.save(self._state(), final, durable=durable)

    def _save_quietly(self, error):
        """Save the checkpoint as the upload stops with error, noting on
        error if that fails rather than hiding it; or, for an upload whose
        source was seen to change, then or before, forget its state instead
        (_forget_if_changed)."""
        if self._forget_if_changed(error):
            return
        try:
            self._save_state(final=True)
        except OSError as problem:
            error.add_note(
                "The checkpoint {} could not be saved: {}".format(
                    self.store.path, problem
                )
            )

    def _forget_if_changed(self, error):
        """As the upload stops with error, its workers finished and its file
        still held, forget the checkpoint's state (_invalidate) if the file
        was seen to change, now or before, while a later call could still
        complete what the checkpoint records; and return whether it did. An
        upload this call began or resumed looks at a local file once more
        first, since a change after it was last checked, such as while a
        part read before was being sent, is seen no other way. Before the
        call takes up the upload its checkpoint records (_start), as when it
        was paused before it began, that upload is forgotten only if the
        checkpoint has it pending and the call has already seen the file
        change. One that may already have completed is left as it was,
        whatever the file did. error stands either way: a change found now
        is recorded, never raised."""
        source = self.source
        if self.session.ref is None:
            # Nothing of this call's own was begun or resumed: what the
            # checkpoint holds, if anything, an earlier call recorded.
            recorded = self.store.load() if self.store is not None else None
            if not (
                isinstance(recorded, dict)
                and recorded.get("completion") == "pending"
            ):
                return False
        elif (
            self.store is not None
            and self.completion == "pending"
            and isinstance(source, _PathSource)
            and not source.changed_seen
        ):
            with contextlib.suppress(InvalidRequestError, OSError):
                # Raises for a change, having recorded it; a file that
                # cannot be looked at now is not taken to have changed.
                source.check_unchanged()
        if not self._source_changed():
            return False
        self._invalidate(error)
        return True

    def _check_source(self):
        """Raise unless a local file is unchanged as far as can be seen
        (_PathSource.check_unchanged)."""
        if isinstance(self.source, _PathSource):
            self.source.check_unchanged()

    def _source_changed(self):
        """Whether the source was seen to change while a later call could
        still complete the upload (its completion pending): the parts that
        arrived may then hold bytes of the file as it was, which no
        checkpoint identity can tell apart from what it is now. An upload
        that may have completed keeps its state, so it is never completed
        again."""
        return self.completion == "pending" and getattr(
            self.source, "changed_seen", False
        )

    def _invalidate(self, error):
        """Forget, durably, the checkpoint's state of a pending upload whose
        source was seen to change (see _forget_if_changed), so that no later
        call resumes it, and save nothing more. If that fails, the checkpoint
        may still hold the state: error says so, and to remove it."""
        self.invalidated = True
        if self.store is None:
            return  # No checkpoint.
        try:
            self.store.invalidate()
        except OSError as problem:
            error.add_note(
                "The checkpoint {} could not be updated to forget this upload of a file that "
                "changed: {}. Remove it before uploading the file again.".format(
                    self.store.path, problem
                )
            )

    def _log_summary(self):
        controller = (
            self.controller.snapshot() if self.controller is not None else {}
        )
        util.log_info(
            "Upload finished",
            size=self.progress.committed,
            parts=self.progress.parts,
            bytes_sent=self.progress.sent,
            parallel=self.session.parallel,
            plan=self.plan,
            resumed=self.resumed,
            target_class=self.settings.target_class,
            adaptive=self.settings.adaptive,
            peak_concurrency=controller.get("peak", 1),
            shrinks=controller.get("shrink", 0),
            backpressure=controller.get("backpressure", 0),
            failures=controller.get("failures", 0),
            seconds=round(self.progress.elapsed(), 3),
        )


def _finish_observing(observer, details):
    """Deliver the final observation. The upload's outcome is settled by
    then, so an observer that fails here is logged rather than raised, and
    a log handler that fails as well is ignored."""
    try:
        observer.finish(details)
    except Exception as error:
        with contextlib.suppress(Exception):
            util.log_warning(
                "Upload observer failed", error=type(error).__name__
            )


def _admitted_now(limiter, size) -> _Reservation | None:
    """A reservation of size bytes in limiter if it grants one now, in its
    usual order behind anyone waiting; otherwise None, keeping no place."""
    reservation = limiter._request(size)
    if reservation.wait(0):
        return reservation
    reservation.release()
    return None


def _admitted(
    limiter, size, lifetime, while_waiting=None, on_wait=None, slot=True
) -> _Reservation:
    """A granted reservation of size bytes in limiter, and a slot unless
    slot is False, once there is room. Raises, giving up its place, if
    lifetime ends first. while_waiting, if given, runs every
    _PROGRESS_INTERVAL seconds of waiting; on_wait, once if it must wait."""
    reservation = limiter._request(size, slot)
    stop_waking = lifetime.watch(limiter._wake)
    try:
        if not reservation.wait(0):
            if on_wait is not None:
                on_wait()
            started = time.monotonic()
            while not reservation.wait(_PROGRESS_INTERVAL):
                lifetime.check("waiting to upload")
                if while_waiting is not None:
                    while_waiting()
            reservation.waited = time.monotonic() - started
        lifetime.check("waiting to upload")
    except BaseException:
        reservation.release()
        raise
    finally:
        stop_waking()
    return reservation


class _SerialUpload:
    """An upload whose size is not known in advance, sent one part at a
    time in order: the remote file a caller writes, and upload_chunks.
    Unknown sizes stay serial until the SDK plans them in parallel."""

    def __init__(self, operation, destination, params=None, previous=None):
        begin_params, self.finish_params = split_params(params)
        self.operation = operation
        self.session = _Session(operation, destination, begin_params)
        self.limiter = operation.context.transfer_limiter
        self.number = 1
        self.grant: _Grant | None = None
        self.last: _Grant | None = None
        self.etags: dict[int, str | None] = {}
        self.sent = 0
        # Where this call's first byte goes in the upload: part offsets are
        # the upload's, not this call's. None when continuing a part not
        # returned by upload_chunks, whose position is not known.
        self.base: int | None = 0
        if previous is not None:
            # Continue an upload that upload_chunks returned.
            self.session.first = self.last = _Grant.from_model(previous)
            self.number = self.last.number + 1
            self.base = getattr(previous, "_files_sdk_offset", None)
            offsets = getattr(previous, "_files_sdk_offsets", None)
            if offsets is not None:
                self.session.offsets = offsets

    def part_size(self):
        """The size of the next part, asking for its grant if needed."""
        if self.grant is None:
            self.grant = self.session.begin(
                self.operation, number=self.number
            )[0]
        return self.grant.partsize

    def reserve(self, size=None):
        """Room in the limiter for the next part's buffer."""
        return _admitted(
            self.limiter, size or self.part_size(), self.operation.lifetime
        )

    def send(self, data, sent=None):
        """Send data as the next part: a full part, or a shorter final one."""
        self.part_size()
        assert self.grant is not None
        if self.base is None and self.grant.offset_query:
            raise InvalidRequestError(
                "This upload sends each part's offset, so continuing it needs the "
                "FileUploadPart an earlier upload_chunks() call returned, which "
                "knows where the upload got to. Nothing more was sent."
            )
        # The grant's size, kept apart from a shorter final part's length, is
        # what a renewal of its URL must give again.
        part = _Part(
            self.number,
            (self.base or 0) + self.sent,
            len(data),
            self.grant,
            self.grant.partsize,
        )
        self.etags[part.number] = self.session.send(
            self.operation, part, data, sent or _ignore
        )
        self.last, self.grant = part.grant, None
        self.number += 1
        self.sent += len(data)

    def finish(self, extra=None):
        params = {**self.finish_params, **(extra or {})}
        return self.session.finish(self.sent, self.etags, params)


def _ignore(_count):
    pass


def upload_parts(
    operation, destination, stream, previous=None, etags=None, params=None
):
    """Upload stream from where it is to its end, in order, continuing the
    upload previous (the FileUploadPart upload_chunks returned) if given,
    without completing it. Returns the last part's FileUploadPart, the ETags
    of the parts sent, and the bytes sent."""
    from files_sdk.models.file_upload_part import FileUploadPart

    upload = _SerialUpload(operation, destination, params, previous)
    source = _StreamSource(stream, None, upload.limiter)
    try:
        while True:
            if upload.etags and source.ended(operation.lifetime):
                # It ended with a full part: no grant for a part never sent.
                break
            size = upload.part_size()
            reservation = upload.reserve()
            try:
                data = source.read(size, operation.lifetime, may_end=True)
                # Only an empty upload sends an empty part.
                if data or (
                    upload.sent == 0 and previous is None and not upload.etags
                ):
                    upload.send(data)
            finally:
                reservation.release()
            if len(data) < size:
                break
    finally:
        source.discard()
    tags = list(etags or [])
    tags.extend(
        {"etag": tag, "part": number}
        for number, tag in sorted(upload.etags.items())
        if tag
    )
    last = upload.last
    if upload.etags and last is not None:
        part = operation.adopt(FileUploadPart(last.record, operation.options))
        # For a later call continuing this upload: where it got to and
        # whether its parts carry offsets.
        if upload.base is not None:
            setattr(part, "_files_sdk_offset", upload.base + upload.sent)
        setattr(part, "_files_sdk_offsets", upload.session.with_offsets)
    else:
        part = previous
    return part, tags, upload.sent


class RemoteFileWriter:
    """The upload behind a File opened for writing: what is written goes to
    Files.com a part at a time as parts fill, and finish() sends the rest
    and completes the upload. The SDK holds at most one part of what was
    written, in buffer, until it is sent, and never more than
    MAX_BUFFERED_PART: a write that would, for a larger part, fails the
    upload.

    Once a write or finish fails, the writer refuses to go on: it cannot
    know which parts arrived, and a completion whose answer was lost must
    not be sent again.
    """

    def __init__(self, operation, destination, text, buffer):
        self.upload = _SerialUpload(operation, destination)
        self.text = text
        self.buffer = buffer
        self.reservation: _Reservation | None = None
        self.failure: BaseException | None = None

    def write(self, data):
        if self.text:
            if not isinstance(data, str):
                raise TypeError(
                    "write() argument must be str, not {}".format(
                        type(data).__name__
                    )
                )
            written = len(data)
            data = data.encode("utf-8")
        else:
            data = memoryview(data).cast("B")
            written = len(data)
        with self._guard():
            view = memoryview(data)
            while view:
                if self.reservation is None:
                    self.reservation = self.upload.reserve()
                room = self.upload.part_size() - self.buffer.tell()
                if (
                    self.buffer.tell() + min(room, len(view))
                    > MAX_BUFFERED_PART
                ):
                    raise _held_too_long()
                self.buffer.write(view[:room])
                view = view[room:]
                if self.buffer.tell() == self.upload.part_size():
                    self._send()
        return written

    def finish(self, extra):
        """Send what is left, as the final part, and complete the upload."""
        with self._guard():
            if self.buffer.tell() or not self.upload.etags:
                if self.reservation is None:
                    self.reservation = self.upload.reserve()
                self._send()
            return self.upload.finish(extra)

    def abandon(self):
        self._release()

    @contextlib.contextmanager
    def _guard(self):
        if self.failure is not None:
            raise InvalidRequestError(
                "This file's upload failed earlier ({}), so nothing more was "
                "sent. Open the file again to upload it.".format(
                    type(self.failure).__name__
                )
            ) from self.failure
        try:
            yield
        except BaseException as error:
            self.failure = error
            self._release()
            raise

    def _send(self):
        self.upload.send(self.buffer.getvalue())
        self.buffer.seek(0)
        self.buffer.truncate()
        self._release()

    def _release(self):
        if self.reservation is not None:
            self.reservation.release()
            self.reservation = None


class UploadScope:
    """What a job's uploads share: for each compatible kind of upload (its
    resolved settings: kind of storage, policy, startup, cap and tuning), one
    controller, and so one request budget, one target and what it learns,
    for the job's lifetime only. Its first file creates a controller and
    later files inherit its target, measurements, epoch and cooldown; a file
    finishing resets nothing. Another job, or a standalone upload, starts
    its own, even through the same TransferLimiter."""

    def __init__(self):
        self._lock = threading.Lock()
        self._controllers: dict[Any, Controller] = {}
        self._uploads: list[_Upload] = []

    def controller(self, settings) -> Controller:
        with self._lock:
            controller = self._controllers.get(settings)
            if controller is None:
                controller = self._controllers[settings] = Controller(
                    settings, shared=True
                )
            return controller

    def joined(self, upload):
        with self._lock:
            self._uploads.append(upload)

    def left(self, upload):
        with self._lock:
            self._uploads.remove(upload)

    def started(self) -> bool:
        """Whether any of the job's uploads has a shared controller yet."""
        with self._lock:
            return bool(self._controllers)

    def admission(self) -> tuple[int, bool, bool, int] | None:
        """For file admission, over the scaled S3 scopes: the lowest target,
        whether a scope at it is warming up and whether one started warm, and
        the part attempts waiting only for a permit, summed across scopes.
        None before such a scope exists."""
        with self._lock:
            controllers = [
                c
                for c in self._controllers.values()
                if c.settings.policy == SCALED_S3
            ]
            uploads = list(self._uploads)
        if not controllers:
            return None
        views = [controller.admission() for controller in controllers]
        lowest = min(view[0] for view in views)
        warming = any(view[1] for view in views if view[0] == lowest)
        started_warm = any(view[2] for view in views if view[0] == lowest)
        queued = sum(view[3] for view in views) + sum(
            upload.queued() for upload in uploads
        )
        return lowest, warming, started_warm, queued


def upload_path(
    operation,
    destination,
    path,
    params=None,
    *,
    max_concurrency=None,
    progress=None,
    tuning=None,
    checkpoint=None,
    pause_token=None,
    store=None,
    expected=None,
    scope=None,
):
    """Upload the local file at path to destination within operation and
    return the File created. With checkpoint (a local path), or store (a
    job's slot), the upload can be paused and resumed. expected, for a
    job's file, is the device, inode, size and modification time the file
    was found with, which it must still have; scope, the job's UploadScope.
    What the source holds is released once the upload is over, or fails
    before it begins."""
    source = _PathSource(path, expected=expected)
    try:
        upload = _Upload(
            operation,
            destination,
            source,
            params,
            max_concurrency,
            progress,
            tuning,
            pause_token,
            scope,
        )
        return _run(
            upload,
            checkpoint,
            store,
            os.path.realpath(source.path),
            params,
            [source.path],
        )
    finally:
        # _Upload.run returns only once its workers, and the part bodies
        # they read, have finished.
        source.close()


def upload_stream(
    operation,
    destination,
    stream,
    size=None,
    params=None,
    *,
    max_concurrency=None,
    progress=None,
    tuning=None,
    spool_limit=None,
    spool_directory=None,
    checkpoint=None,
    pause_token=None,
    store=None,
):
    """Upload stream, from where it is, to destination within operation and
    return the File created: size bytes of it, or, with size None, all of
    it. A stream of unknown size goes one part at a time, unless spool_limit
    says to copy it to a temporary file first, of at most that many bytes.
    A checkpoint needs the size, or the spool: resuming reads the same
    bytes again from the same start and checks the parts that arrived."""
    if size is None:
        if spool_limit is not None:
            if store is None:
                # Refused before the stream is copied.
                checked_checkpoint(checkpoint, checked_pause(pause_token))
            return _upload_spooled(
                operation,
                destination,
                stream,
                params,
                spool_limit,
                spool_directory,
                max_concurrency=max_concurrency,
                progress=progress,
                tuning=tuning,
                checkpoint=checkpoint,
                pause_token=pause_token,
                store=store,
            )
        if (
            checkpoint is not None
            or store is not None
            or pause_token is not None
        ):
            raise InvalidParameterError(
                "A stream of unknown size cannot be paused or resumed; give its size, or spool_limit"
            )
        return _upload_unknown(
            operation, destination, stream, params, progress, tuning
        )
    if isinstance(size, bool) or not isinstance(size, int) or size < 0:
        raise InvalidParameterError(
            "size must be an integer of 0 or more, or None"
        )
    if spool_limit is not None:
        raise InvalidParameterError(
            "spool_limit is for streams of unknown size; leave it out with size"
        )
    source = _StreamSource(stream, size, operation.context.transfer_limiter)
    upload = _Upload(
        operation,
        destination,
        source,
        params,
        max_concurrency,
        progress,
        tuning,
        pause_token,
    )
    return _run(upload, checkpoint, store, "stream", params, [])


def _run(upload, checkpoint, store, source_name, params, local_paths):
    """Run upload, with its checkpoint if it has one."""
    if store is not None:
        upload.store = store
        return upload.run()
    path = checked_checkpoint(checkpoint, upload.pause)
    if path is None:
        return upload.run()
    for local in local_paths:
        if same_file(path, local):
            raise InvalidParameterError(
                "The checkpoint must be a file of its own, not {}".format(
                    local
                )
            )
    key = {
        **scope(upload.operation.context),
        "destination": upload.destination,
        "source": source_name,
        "params": digest(params or {}),
    }
    handle, upload.store = file_store(path, "upload", key)
    try:
        return upload.run()
    finally:
        handle.close()


class _UnknownGrowth:
    """Part sizes for an upload of unknown size whose grant lets the SDK
    choose them (variable_part_limits): unknown_initial_part_size, doubled
    every unknown_grow_every parts up to unknown_max_part_size, within the
    grant's limits."""

    def __init__(self, limits, settings):
        self.limits = limits
        self.settings = settings
        self.number = 1
        self.size = 0
        self.largest = 0
        self.smallest_nonfinal = None

    def length(self):
        """The next part's size, or 0 when the grant allows no more."""
        settings, limits = self.settings, self.limits
        if (
            self.number > limits.max_parts
            or self.size >= limits.max_file_bytes
        ):
            return 0
        doublings = (self.number - 1) // settings.unknown_grow_every
        grown = settings.unknown_initial_part_size << min(doublings, 62)
        length = min(
            max(
                min(grown, settings.unknown_max_part_size),
                limits.min_nonfinal_bytes,
            ),
            limits.max_part_bytes,
        )
        return min(length, limits.max_file_bytes - self.size)

    def placed(self, length, final):
        self.number += 1
        self.size += length
        self.largest = max(self.largest, length)
        if not final:
            self.smallest_nonfinal = min(
                self.smallest_nonfinal or length, length
            )


def _too_long():
    return InvalidRequestError(
        "The upload stream is longer than Files.com allows for this upload, so "
        "the upload was not completed."
    )


def _upload_unknown(operation, destination, stream, params, progress, tuning):
    """Upload all of stream, one part at a time, and complete the upload.
    After a full part, the stream is read ahead by a byte before anything
    more is asked for: a stream that ended there completes with the parts
    sent, and one that goes on beyond what the grant allows fails without
    asking for a part it cannot have."""
    upload = _SerialUpload(operation, destination, params)
    source = _StreamSource(stream, None, upload.limiter)
    report = _Progress(destination, None, checked_progress(progress))
    tuning = checked_tuning(tuning, operation.context)
    # One part at a time, sending or not; there is no read-ahead runway.
    sending = [0]
    observer = None
    if tuning.observer is not None:
        observer = Observer(
            tuning.observer,
            lambda: (1, sending[0], None, None, None),
            waits=("limiter",),
        )
        observer.start(
            {
                "plan": "serial (unknown size)",
                "parallel": False,
                "size": None,
                "resumed": False,
            }
        )
    outcome = "failed"
    try:
        file = _send_unknown(
            operation, upload, source, report, tuning, observer, sending
        )
        outcome = "completed"
        return file
    finally:
        if observer is not None:
            plan = (
                "serial (variable part sizes)"
                if upload.session.variable is not None
                else "serial (unknown size)"
            )
            _finish_observing(
                observer,
                {
                    "plan": plan,
                    "parallel": False,
                    "size": None,
                    "resumed": False,
                    "outcome": outcome,
                    "parts": report.parts,
                    "bytes_committed": report.committed,
                    "bytes_sent": report.sent,
                },
            )


def _send_unknown(
    operation, upload, source, report, tuning, observer, sending
):
    """Send the parts of an upload of unknown size, then complete it,
    telling observer, if any, how it goes (sending[0] is 1 while a part
    goes)."""
    growth = None
    try:
        while True:
            first = upload.session.first
            if first is not None:
                if source.ended(operation.lifetime):
                    break
                if (
                    growth is None
                    and first.available_parts is not None
                    and upload.number > first.available_parts
                ):
                    raise _too_long()
            if growth is not None and not growth.length():
                raise _too_long()
            length = upload.part_size()
            first = upload.session.first
            if (
                growth is None
                and first is not None
                and first.variable_limits is not None
            ):
                growth = _UnknownGrowth(
                    first.variable_limits,
                    tuning.settings(first.target_class, 1),
                )
                upload.session.variable = growth  # type: ignore[assignment]
            if (
                observer is not None
                and observer.knobs is None
                and first is not None
            ):
                observer.knobs = (
                    knobs(growth.settings)
                    if growth is not None
                    else {"granted_part_size": first.partsize}
                )
            if growth is not None:
                length = growth.length()
                if not length:
                    # A grant that allows no bytes: only an empty stream fits.
                    if not source.ended(operation.lifetime):
                        raise _too_long()
                    length = 0
            reservation = upload.reserve(length)
            try:
                # Within the reservation's cleanup: an observer can raise.
                if observer is not None:
                    observer.waited("limiter", reservation.waited)
                data = source.read(length, operation.lifetime, may_end=True)
                if data or not upload.etags:
                    if observer is not None:
                        sending[0] = 1
                        observer.poll()
                    try:
                        upload.send(data, report.add_sent)
                    finally:
                        if observer is not None:
                            sending[0] = 0
                    if observer is not None:
                        observer.poll()
                    report.commit(len(data))
                    if growth is not None:
                        growth.placed(len(data), final=len(data) < length)
            finally:
                reservation.release()
            report.report()
            if len(data) < length:
                break
    finally:
        source.discard()
    report.report(force=True)
    return upload.finish()


def _upload_spooled(
    operation,
    destination,
    stream,
    params,
    spool_limit,
    spool_directory,
    **options,
):
    """Copy all of stream to a temporary file of the SDK's own, of at most
    spool_limit bytes, then upload that file as a file of known size. A
    longer stream fails before anything is sent."""
    if (
        isinstance(spool_limit, bool)
        or not isinstance(spool_limit, int)
        or spool_limit < 0
    ):
        raise InvalidParameterError(
            "spool_limit must be an integer of 0 or more"
        )
    if not callable(getattr(stream, "read", None)):
        raise InvalidParameterError(
            "The upload source must be a binary stream with a read() method"
        )
    handle, path = tempfile.mkstemp(
        prefix="files_sdk-upload-", dir=spool_directory
    )
    try:
        with os.fdopen(handle, "wb") as spool:
            total = 0
            while True:
                operation.lifetime.check("copying the stream")
                data = stream.read(_READ_SIZE)
                if data is None:
                    raise InvalidParameterError(
                        "The upload stream has no data ready but has not ended "
                        "(read() returned None). Uploads need a blocking stream."
                    )
                if isinstance(data, str):
                    raise InvalidParameterError(
                        "The upload stream returned text; open it in binary mode"
                    )
                if not data:
                    break
                total += len(data)
                if total > spool_limit:
                    raise InvalidRequestError(
                        "The upload stream is longer than its spool_limit of {} "
                        "bytes, so nothing was uploaded.".format(spool_limit)
                    )
                spool.write(data)
        source = _PathSource(path, send_mtime=False, owned=True)
        try:
            upload = _Upload(
                operation,
                destination,
                source,
                params,
                options["max_concurrency"],
                options["progress"],
                options["tuning"],
                options["pause_token"],
            )
            source.record_digests = (
                options["checkpoint"] is not None
                or options["store"] is not None
            )
            return _run(
                upload,
                options["checkpoint"],
                options["store"],
                "stream",
                params,
                [path],
            )
        finally:
            # Once the upload is over, as for upload_path, and before the
            # spool is removed.
            source.close()
    finally:
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass
