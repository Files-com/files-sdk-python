"""Writing to a stream the caller owns, exactly.

A download into a caller's stream, and a remote file read into one, write
through write_all: every byte (or, for a text stream, character) is
written, however few a single write() takes, and only what the stream has
taken counts as delivered. The stream must be blocking, as the SDK
documents: a raw stream that answers None (it would block) or a stream
that takes nothing is refused rather than retried forever. A write()
that returns None from any other object, as simple file-like classes
often do, is taken to have written everything, as version 1 took every
write. Before each write after the first, check(), when given, raises if
the operation has stopped, so a cancelled download starts no more writes.
The caller's own exceptions pass through unchanged.
"""

import io

from files_sdk.error import InvalidParameterError


def write_all(stream, data, check=None, delivered=None, write=None):
    """Write all of data (bytes-like or str) to stream. delivered, when
    given, hears the count of each write's accepted units as it happens,
    so a failure part way leaves an exact count behind. write, when given,
    is called in place of stream.write."""
    write = write or stream.write
    if not isinstance(data, (str, bytes)):
        # Plain bytes, as a stream would get them from a response.
        data = bytes(data)
    total = len(data)
    done = 0
    while done < total:
        if done and check is not None:
            check()
        piece = data if not done else data[done:]
        accepted = write(piece)
        if accepted is None:
            if isinstance(stream, io.RawIOBase):
                raise InvalidParameterError(
                    "The download's stream took no bytes because it would block "
                    "(write() returned None). Downloads need a blocking stream."
                )
            accepted = len(piece)
        if (
            isinstance(accepted, bool)
            or not isinstance(accepted, int)
            or accepted < 0
            or accepted > len(piece)
        ):
            raise InvalidParameterError(
                "The download's stream reported writing {!r} of {} {}".format(
                    accepted,
                    len(piece),
                    "characters" if isinstance(data, str) else "bytes",
                )
            )
        if accepted == 0:
            raise InvalidParameterError(
                "The download's stream took nothing (write() returned 0)"
            )
        done += accepted
        if delivered is not None:
            delivered(accepted)
    return done
