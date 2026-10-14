"""Files sent with API requests, such as a user's avatar or a site's logo.

An operation with a parameter of type file, such as ``avatar_file``, sends
file content in it as an attachment: in a multipart/form-data request when
form fields carry every parameter exactly, or else in a JSON request as the
API's {"encoded_content": ...} file object. A request without file content
is sent as JSON, as before.
"""

import base64
import errno
import io
import json
import math
import os
import re
import tempfile
import uuid
from contextlib import ExitStack
from decimal import Decimal

from requests_toolbelt import MultipartEncoder

from files_sdk.error import InvalidParameterError
import files_sdk.util as util

DEFAULT_SPOOL_LIMIT = 64 * 1024 * 1024
# A spool keeps this much in memory before moving to a temporary file.
_SPOOL_MEMORY = 1024 * 1024
_COPY_SIZE = 64 * 1024

_TOKEN = r"[!#$%&'*+.^_`|~0-9A-Za-z-]+"
_QUOTED = r'"(?:[^"\\\x00-\x1f\x7f]|\\[^\x00-\x1f\x7f])*"'
_MEDIA_TYPE = re.compile(
    rf"{_TOKEN}/{_TOKEN}(?:[ \t]*;[ \t]*{_TOKEN}=(?:{_TOKEN}|{_QUOTED}))*"
)
_CONTROL = re.compile(r"[\x00-\x1f\x7f]")
# Brackets structure form field names, and quotes cannot be sent in them.
_KEY_CHANGED_BY_FORMS = re.compile(r'[\[\]"\x00-\x1f\x7f]')
# The API's form parser percent-decodes an uploaded file's name, unescapes
# backslashes and keeps only the part after a slash. A quote reaches it
# percent-encoded, so it is decoded too. A name with any of these is sent in
# a JSON request, which keeps it exactly.
_FILENAME_CHANGED_BY_FORMS = re.compile(r'[%\\"/]')


class Attachment:
    """A file for an API parameter of type file, such as ``avatar_file``.

    ``content`` is bytes, or a binary stream opened for reading, such as a
    file from ``open(path, "rb")``. Bytes are copied if they can change. The
    SDK leaves a stream open and sends it from its position when the request
    starts to its end. If the request is retried, the SDK seeks back to that
    position and sends the same bytes again, so do not read, write or seek
    the stream until the request returns. A stream that cannot seek, such as
    a pipe, is first copied into a temporary buffer of at most
    ``spool_limit`` bytes, which the SDK deletes when the request ends. A
    request can buffer this much for each such attachment it sends.

    ``filename`` defaults to the base name of the stream's file, or else the
    parameter's name. ``content_type`` defaults to application/octet-stream.

    To send a local file, use :meth:`from_path`. Operations also accept bytes
    or a binary stream directly, as an attachment with these defaults.
    """

    def __init__(
        self,
        content,
        filename=None,
        content_type=None,
        *,
        spool_limit=DEFAULT_SPOOL_LIMIT,
    ):
        if isinstance(content, _Source):
            self._source = content
        elif isinstance(content, (bytes, bytearray, memoryview)):
            self._source = _BytesSource(bytes(content))
        elif _is_binary_stream(content):
            self._source = _StreamSource(content, _checked_limit(spool_limit))
        else:
            raise TypeError(_content_problem(content))
        self._filename = _checked_filename(filename) or self._source.filename
        self._content_type = _checked_content_type(content_type)

    @property
    def filename(self):
        """The file name sent, or None to send the parameter's name."""
        return self._filename

    @property
    def content_type(self):
        return self._content_type

    @classmethod
    def from_path(cls, path, filename=None, content_type=None):
        """An attachment of the local file at ``path``. The SDK opens the
        file when a request starts and closes it when the request ends. A
        retry sends the file again, unless its size or modification time has
        changed since the request started. ``filename`` defaults to the
        file's base name."""
        return cls(_PathSource(os.fspath(path)), filename, content_type)

    def __repr__(self):
        return "{}(filename={!r}, content_type={!r})".format(
            type(self).__name__, self.filename, self.content_type
        )


def with_attachments(params, *names):
    """``params``, with file content in each named parameter made an
    Attachment. Other values, such as an {"encoded_content": ...} file
    object, are sent as given, and the API decides whether they are valid.
    Operations with file parameters call this after checking their other
    parameters. It never changes ``params``: if it converts a value, it
    returns a new dict."""
    attachments = {}
    for name in names:
        if name in params:
            value = params[name]
            attachment = _as_attachment(name, value)
            if attachment is not value:
                attachments[name] = attachment
    return {**params, **attachments} if attachments else params


def has_attachment(params):
    """Whether params hold an attachment to stream."""
    return any(isinstance(value, Attachment) for value in params.values())


def _as_attachment(name, value):
    if isinstance(value, (bytes, bytearray, memoryview)) or _is_binary_stream(
        value
    ):
        return Attachment(value)
    # A path, or a stream that is not binary and readable, can never be
    # sent; say how to send the file instead of failing to encode it.
    if isinstance(value, os.PathLike) or callable(
        getattr(value, "read", None)
    ):
        raise InvalidParameterError(
            "Bad parameter: {} must be bytes, a binary stream or a "
            "files_sdk.Attachment. {}".format(name, _content_problem(value))
        )
    return value


def _is_binary_stream(value):
    if isinstance(value, (str, bytes, io.TextIOBase)):
        return False
    if not callable(getattr(value, "read", None)):
        return False
    readable = getattr(value, "readable", None)
    try:
        return readable is None or readable()
    except ValueError:  # A closed file.
        return False


def _content_problem(value):
    if isinstance(value, (str, os.PathLike)):
        return (
            "To send the local file at a path, use "
            "files_sdk.Attachment.from_path(path)."
        )
    if isinstance(value, io.TextIOBase):
        return "Open the file in binary mode, such as open(path, 'rb')."
    if callable(getattr(value, "read", None)):
        return "The stream is not open for reading."
    return "Attachments are bytes or binary streams, not {}.".format(
        type(value).__name__
    )


def _checked_filename(filename):
    if filename is None:
        return None
    if not isinstance(filename, str) or not filename:
        raise ValueError("An attachment's filename must be a non-empty str")
    if _CONTROL.search(filename):
        raise ValueError(
            "An attachment's filename cannot contain control characters, "
            "such as a line break"
        )
    return filename


def _checked_content_type(content_type):
    if content_type is None:
        return "application/octet-stream"
    if not isinstance(content_type, str) or not _MEDIA_TYPE.fullmatch(
        content_type
    ):
        raise ValueError(
            "An attachment's content_type must be a media type such as "
            "'image/png', not {!r}".format(content_type)
        )
    return content_type


def _checked_limit(spool_limit):
    if (
        isinstance(spool_limit, bool)
        or not isinstance(spool_limit, int)
        or spool_limit <= 0
    ):
        raise ValueError(
            "spool_limit must be a positive number of bytes, not {!r}".format(
                spool_limit
            )
        )
    return spool_limit


# Sources. Each request opens an attachment's source once, into content that
# every attempt, and every redirect, reads again from the start.


def _no_check():
    pass


class _Source:
    filename = None

    def open(self, stack, name, check=_no_check):
        """The _Content to send. Resources it needs are entered into stack,
        which the request closes when it ends. check() raises once the
        request's operation has stopped; it runs before each read the SDK
        makes from the source."""
        raise NotImplementedError


class _BytesSource(_Source):
    def __init__(self, data):
        self.data = data

    def open(self, stack, name, check=_no_check):
        return _Content(
            name, io.BytesIO(self.data), 0, len(self.data), check=check
        )


class _PathSource(_Source):
    def __init__(self, path):
        self.path = path
        self.filename = _base_name(path)

    def open(self, stack, name, check=_no_check):
        check()
        try:
            file = stack.enter_context(open(self.path, "rb"))
            opened = os.fstat(file.fileno())
        except OSError as error:
            raise _source_error(name, "open the file", error) from error

        def check_unchanged():
            now = os.fstat(file.fileno())
            if (now.st_size, now.st_mtime_ns) != (
                opened.st_size,
                opened.st_mtime_ns,
            ):
                raise InvalidParameterError(
                    "The file for {} changed while it was being sent, so the "
                    "request was stopped. Send it again once the file is "
                    "complete.".format(name)
                )

        return _Content(name, file, 0, opened.st_size, check_unchanged, check)


class _StreamSource(_Source):
    def __init__(self, stream, spool_limit):
        self.stream = stream
        self.spool_limit = spool_limit
        # The rule Requests uses for its files= uploads: a file's base name,
        # but not a pseudo-name such as "<stdin>".
        stream_name = getattr(stream, "name", None)
        if isinstance(stream_name, (str, bytes)):
            stream_name = os.fsdecode(stream_name)
            if stream_name[:1] != "<" and stream_name[-1:] != ">":
                self.filename = _base_name(stream_name)

    def open(self, stack, name, check=_no_check):
        check()
        try:
            seekable = getattr(self.stream, "seekable", None)
            if seekable is None or not seekable():
                return self._spooled(stack, name, check)
            start = self.stream.tell()
            end = self.stream.seek(0, io.SEEK_END)
            self.stream.seek(start)
        except (OSError, ValueError) as error:
            raise _source_error(
                name, "find the length of the stream", error
            ) from error
        return _Content(
            name, self.stream, start, max(0, end - start), check=check
        )

    def _spooled(self, stack, name, check):
        """Copy a stream that cannot seek, so each attempt can resend it.
        It stops, leaving the stream open, before any further read once the
        operation has stopped."""
        spool = stack.enter_context(
            tempfile.SpooledTemporaryFile(max_size=_SPOOL_MEMORY)
        )
        size = 0
        try:
            while True:
                check()
                # Read at most one byte past the limit, to detect exceeding it.
                chunk = self.stream.read(
                    min(_COPY_SIZE, self.spool_limit - size + 1)
                )
                _check_chunk(name, chunk, size)
                if not chunk:
                    break
                size += len(chunk)
                if size > self.spool_limit:
                    raise InvalidParameterError(
                        "The stream for {} holds more than the {} bytes the "
                        "SDK buffers for a stream it cannot seek. Send a "
                        "seekable file, or pass a larger spool_limit to "
                        "files_sdk.Attachment.".format(name, self.spool_limit)
                    )
                spool.write(chunk)
        except (OSError, ValueError) as error:
            raise _source_error(name, "read the stream", error) from error
        return _Content(name, spool, 0, size, check=check)


class _Content:
    """An opened attachment: length bytes of file, starting at start."""

    def __init__(
        self, name, file, start, length, check_unchanged=None, check=_no_check
    ):
        self.name = name
        self.file = file
        self.start = start
        self.length = length
        self.check_unchanged = check_unchanged or (lambda: None)
        self.check = check

    def reader(self):
        """A reader of the content from its start, for one attempt. It
        fails now, before the attempt sends anything, if the content cannot
        be sent again."""
        self.check()
        self.check_unchanged()
        self.rewind()
        return _Reader(self)

    def rewind(self):
        try:
            self.file.seek(self.start)
        except (OSError, ValueError) as error:
            raise _source_error(
                self.name, "return to the start of the stream", error
            ) from error


class _Reader:
    """Reads an attachment's bytes for MultipartEncoder, which sizes the part
    from len and reads until len reaches 0. It has no getvalue or fileno, so
    the encoder cannot measure or read the file past the content."""

    def __init__(self, content):
        self._content = content
        self.len = content.length

    def read(self, size: int | None = -1):
        wanted = self.len if size is None or size < 0 else min(size, self.len)
        if wanted == 0:
            return b""
        content = self._content
        sent = content.length - self.len
        if sent == 0:
            # Parameters can share one stream; each part reads it from the
            # start.
            content.rewind()
        content.check()
        try:
            chunk = content.file.read(wanted)
        except (OSError, ValueError) as error:
            raise _source_error(
                content.name, "read the stream", error
            ) from error
        _check_chunk(content.name, chunk, sent)
        chunk = bytes(chunk)
        if not chunk:
            raise InvalidParameterError(
                "The stream for {} ended after {} of its {} bytes, so the "
                "request was stopped.".format(
                    content.name, sent, content.length
                )
            )
        if len(chunk) > wanted:
            raise InvalidParameterError(
                "The stream for {} returned more bytes than were asked "
                "for.".format(content.name)
            )
        self.len -= len(chunk)
        if self.len == 0:
            content.check_unchanged()
        return chunk


def _check_chunk(name, chunk, offset):
    if chunk is None:
        raise InvalidParameterError(
            "The stream for {} has no data ready but has not ended (read() "
            "returned None after {} bytes). Attachments need a blocking "
            "stream.".format(name, offset)
        )
    if not isinstance(chunk, (bytes, bytearray, memoryview)):
        raise InvalidParameterError(
            "The stream for {} returned {} instead of bytes. Open the file "
            "in binary mode, such as open(path, 'rb').".format(
                name, type(chunk).__name__
            )
        )


def _base_name(path):
    """A path's base name as a filename to send, or None if it has none."""
    name = os.path.basename(os.fsdecode(path))
    return name if name and not _CONTROL.search(name) else None


def _source_error(name, action, error):
    """The InvalidParameterError for an attachment source that failed while
    the SDK tried to action. The source's own error text can hold anything,
    such as a signed URL, so the message gives only the parameter, the kind
    of error and its errno. The error itself is the cause, and its text is
    logged at DEBUG."""
    util.log_debug(
        "Attachment source error details", parameter=name, error_message=error
    )
    return InvalidParameterError(
        "Could not {} for {} ({}).".format(action, name, _error_kind(error))
    )


def _error_kind(error):
    """An exception's class name, with its errno if it has one, such as
    "FileNotFoundError, errno 2 ENOENT"."""
    kind = type(error).__name__
    code = getattr(error, "errno", None)
    if isinstance(code, int):
        kind += ", errno {} {}".format(
            code, errno.errorcode.get(code, "")
        ).rstrip()
    return kind


# The request body.


class AttachmentBody:
    """The body of a request whose params hold attachments.

    It is multipart/form-data when form fields carry every parameter exactly
    as JSON would. Otherwise it is the JSON the request would send without
    attachments, with each attachment as the API's JSON file object:
    {"encoded_content": <base64>, "filename": ..., "type": ...}. Either way
    it streams each attachment from its source, so memory stays bounded.

    Requests sends it like a file of len bytes. seek(0) starts it over with
    the same bytes, from each attachment's start: the SDK calls it before
    each retry, and Requests calls it before following a 307 or 308 redirect.

    Making the body opens the attachments, before anything is sent, and
    close() closes what it opened. Streams the caller passed in stay open.
    check() raises once the request's operation has stopped; the body calls
    it before each read it makes from a source, so a stopped operation reads
    no further.
    """

    def __init__(self, params, check=_no_check):
        fields = _exact_form_fields(params)
        document = None if fields is not None else _JsonDocument(params)
        self._stack = ExitStack()
        try:
            parts = {
                name: _FilePart(self._stack, name, value, check)
                for name, value in params.items()
                if isinstance(value, Attachment)
            }
            self._encoding = (
                _MultipartEncoding(fields, parts)
                if document is None
                else _JsonEncoding(document, parts)
            )
            self.seek(0)
        except BaseException as error:
            _close_keeping(self._stack, error)
            raise

    @property
    def content_type(self):
        return self._encoding.content_type

    def seek(self, offset, whence=io.SEEK_SET):
        if (offset, whence) != (0, io.SEEK_SET):
            raise io.UnsupportedOperation(
                "A request body can only return to its start"
            )
        self._chunks = self._encoding.attempt()
        self._buffer = bytearray()
        self._position = 0
        return 0

    def tell(self):
        return self._position

    @property
    def len(self):
        return self._encoding.length

    def read(self, size: int | None = -1):
        buffer = self._buffer
        while size is None or size < 0 or len(buffer) < size:
            chunk = next(self._chunks, None)
            if chunk is None:
                break
            buffer += chunk
        count = len(buffer) if size is None or size < 0 else size
        data = bytes(buffer[:count])
        del buffer[:count]
        self._position += len(data)
        return data

    # Iterable, so Requests treats the body as a stream: it records the
    # start with tell() and can seek back to it for a 307 or 308 redirect.
    def __iter__(self):
        return iter(lambda: self.read(_COPY_SIZE), b"")

    def close(self):
        self._stack.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        if exc is None:
            self.close()
        else:
            _close_keeping(self._stack, exc)

    def __repr__(self):
        # Logged at DEBUG: the parameter names and attachment details, never
        # the values, which can hold passwords.
        return "<{} {}>".format(
            self.content_type.split(";")[0],
            ", ".join(
                (
                    "{}={}".format(name, value)
                    if isinstance(value, _FilePart)
                    else name
                )
                for name, value in self._encoding.named_values()
            ),
        )


def _close_keeping(stack, error):
    """Close stack's resources after error, which stays the error raised. A
    failure to close is noted on it."""
    try:
        stack.close()
    except Exception as cleanup_error:
        # The stack holds only what the SDK opened, never the caller's
        # streams, so this is the SDK's own file or spool failing.
        error.add_note(
            "Closing an attachment afterwards also failed: {!r}".format(
                cleanup_error
            )
        )


class _FilePart:
    """An attachment opened for one request."""

    def __init__(self, stack, name, attachment, check=_no_check):
        self.filename = attachment.filename or name
        self.content_type = attachment.content_type
        self.content = attachment._source.open(stack, name, check)

    def __str__(self):
        return "({}, {}, {} bytes)".format(
            self.filename, self.content_type, self.content.length
        )


class _MultipartEncoding:
    def __init__(self, fields, parts):
        self._fields = [
            (name, parts[name] if isinstance(value, Attachment) else value)
            for name, value in fields
        ]
        self._boundary = uuid.uuid4().hex
        self.content_type = "multipart/form-data; boundary={}".format(
            self._boundary
        )

    def attempt(self):
        """The body's bytes for one attempt, in chunks."""
        # A new encoder for each attempt: one that has been read cannot be
        # read again. Every attempt has the same length.
        encoder = MultipartEncoder(
            [
                (
                    name,
                    (
                        (
                            value.filename,
                            value.content.reader(),
                            value.content_type,
                        )
                        if isinstance(value, _FilePart)
                        else value
                    ),
                )
                for name, value in self._fields
            ],
            boundary=self._boundary,
        )
        self.length = encoder.len
        return iter(lambda: encoder.read(_COPY_SIZE), b"")

    def named_values(self):
        return self._fields


class _JsonEncoding:
    content_type = "application/json"

    def __init__(self, document, parts):
        self._document = document
        self._parts = [parts[name] for name in document.attachment_names]
        self.length = sum(len(text) for text in document.texts) + sum(
            4 * ((part.content.length + 2) // 3) for part in self._parts
        )

    def attempt(self):
        """The body's bytes for one attempt, in chunks."""
        # Make the readers now, so a source that cannot be sent again fails
        # before the attempt sends anything.
        readers = [part.content.reader() for part in self._parts]
        return self._chunks(readers)

    def _chunks(self, readers):
        texts = self._document.texts
        yield texts[0]
        for reader, text in zip(readers, texts[1:]):
            yield from _base64_chunks(reader)
            yield text

    def named_values(self):
        return self._document.named_values(self._parts)


class _JsonDocument:
    """The JSON text of params, encoded as the SDK's JSON requests are, with
    each attachment as a file object. texts are the encoded pieces around each
    attachment's encoded_content string, in attachment_names order."""

    def __init__(self, params):
        document = {}
        markers = {}
        for name, value in params.items():
            if isinstance(value, Attachment):
                markers[name] = "files-sdk-attachment-" + uuid.uuid4().hex
                value = {
                    "encoded_content": markers[name],
                    "filename": value.filename or name,
                    "type": value.content_type,
                }
            document[name] = value
        try:
            # Requests encodes a json= body the same way.
            text = json.dumps(document, allow_nan=False)
        except (TypeError, ValueError) as error:
            raise InvalidParameterError(
                "Bad parameter: the request's parameters cannot be sent as "
                "JSON: {}".format(error)
            ) from error
        texts = []
        for marker in markers.values():
            before, text = text.split('"{}"'.format(marker))
            texts.append(before + '"')
            text = '"' + text
        texts.append(text)
        self.texts = [text.encode("utf-8") for text in texts]
        self.attachment_names = list(markers)
        self._names = list(params)

    def named_values(self, parts):
        by_name = dict(zip(self.attachment_names, parts))
        return [(name, by_name.get(name)) for name in self._names]


def _base64_chunks(reader):
    """The base64 of a reader's bytes, in chunks. Each chunk but the last
    encodes a multiple of 3 bytes, so the chunks join into one encoding."""
    pending = b""
    while reader.len:
        pending += reader.read(_COPY_SIZE)
        whole = len(pending) if reader.len == 0 else len(pending) // 3 * 3
        if whole:
            yield base64.b64encode(pending[:whole])
            pending = pending[whole:]


# Form fields. The Files.com API reads multipart form fields with Rack's
# bracketed names: "paths[]" appends to a list and "value[gravity]" sets a
# key of an object. It converts a top-level field's text to that
# parameter's type, such as a boolean, but keeps the values inside an object
# as text. Form fields have no way to send None, an empty list or object, or
# a list of objects, and the API percent-decodes and unescapes some
# characters of an uploaded file's name. A request with any of those is sent
# as JSON instead.


class _NotExact(Exception):
    pass


def _exact_form_fields(params):
    """The (name, text or Attachment) form fields that carry params exactly,
    or None if form fields would change a value."""
    fields = []
    try:
        for key, value in params.items():
            name = _field_name(None, key)
            if isinstance(value, Attachment):
                if _FILENAME_CHANGED_BY_FORMS.search(value.filename or name):
                    raise _NotExact
                fields.append((name, value))
            else:
                _add_value(fields, name, value, in_object=False)
    except _NotExact:
        return None
    return fields


def _add_value(fields, name, value, in_object):
    if isinstance(value, dict) and value:
        for key, item in value.items():
            _add_value(fields, _field_name(name, key), item, in_object=True)
    elif isinstance(value, (list, tuple)) and value:
        for item in value:
            if isinstance(item, (dict, list, tuple)):
                raise _NotExact
            _add_value(fields, name + "[]", item, in_object)
    else:
        fields.append((name, _text(value, in_object)))


def _text(value, in_object):
    """The form text that carries value exactly."""
    if isinstance(value, (str, Decimal)):
        # JSON requests send a Decimal as a string too.
        return str(value)
    # The API converts top-level text to the parameter's type, so there a
    # boolean or number reads back as itself; inside an object it would stay
    # text.
    if in_object or isinstance(value, Attachment):
        raise _NotExact
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float) and math.isfinite(value):
        return repr(value)
    raise _NotExact


def _field_name(parent, key):
    """The form field name for key in parent, or for the parameter key."""
    if (
        not isinstance(key, str)
        or not key
        or _KEY_CHANGED_BY_FORMS.search(key)
    ):
        raise _NotExact
    return key if parent is None else "{}[{}]".format(parent, key)
