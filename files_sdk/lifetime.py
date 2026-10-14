"""Cancellation and deadlines for SDK operations.

Each logical operation, such as one API call, one list with all the pages
it goes on to fetch, or one upload from its first request to its last, has
one Lifetime. It stops when the caller's CancellationToken is cancelled,
when the client that runs it is closed, or when its deadline passes.
"""

import heapq
import itertools
import math
import threading
import time
from typing import Any, Callable

from files_sdk.error import (
    ClientClosedError,
    DeadlineExceededError,
    OperationCancelledError,
)


class CancellationToken:
    """A one-way signal that stops the operations it is given to.

    Pass it as the cancel_token option. cancel() can be called from any
    thread, and the token stays cancelled. An operation stops at once while
    it waits for a connection to Files.com or the storage service to send
    or receive data, or between retries and pages. It cannot interrupt a
    host name lookup or the caller's own code, such as a stream it reads an
    upload from, and stops once they return.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._cancelled = False
        self._callbacks: dict[int, Callable[[], None]] = {}
        self._keys = itertools.count()

    @property
    def cancelled(self) -> bool:
        return self._cancelled

    def cancel(self) -> None:
        with self._lock:
            if self._cancelled:
                return
            self._cancelled = True
            callbacks = list(self._callbacks.values())
            self._callbacks.clear()
        for callback in callbacks:
            callback()

    def _subscribe(self, callback: Callable[[], None]) -> Callable[[], None]:
        """Call callback when the token is cancelled, now if it already
        is. Returns the function that cancels the subscription."""
        with self._lock:
            if not self._cancelled:
                key = next(self._keys)
                self._callbacks[key] = callback
                return lambda: self._unsubscribe(key)
        callback()
        return _nothing

    def _unsubscribe(self, key):
        with self._lock:
            self._callbacks.pop(key, None)

    def __repr__(self):
        state = "cancelled" if self._cancelled else "active"
        return f"<CancellationToken {state}>"


def _nothing():
    pass


class _DeadlineTimer:
    """Calls functions at monotonic deadlines from one background thread.

    The thread starts when a deadline is scheduled and ends when none is
    left, so operations without a deadline never start it.
    """

    def __init__(self):
        self._condition = threading.Condition()
        self._entries: list[list[Any]] = []
        self._order = itertools.count()
        self._running = False

    def schedule(self, deadline, callback) -> Callable[[], None]:
        entry = [deadline, next(self._order), callback]
        with self._condition:
            heapq.heappush(self._entries, entry)
            if self._running:
                self._condition.notify()
            else:
                self._running = True
                threading.Thread(
                    target=self._run, name="files_sdk deadlines", daemon=True
                ).start()
        return lambda: self._cancel(entry)

    def _cancel(self, entry):
        with self._condition:
            entry[2] = None
            # Wake the thread, so it ends if no other deadline is pending.
            self._condition.notify()

    def _run(self):
        with self._condition:
            while True:
                entries = self._entries
                while entries and entries[0][2] is None:
                    heapq.heappop(entries)
                if not entries:
                    self._running = False
                    return
                wait = entries[0][0] - time.monotonic()
                if wait > 0:
                    self._condition.wait(wait)
                    continue
                callback = heapq.heappop(entries)[2]
                self._condition.release()
                try:
                    callback()
                finally:
                    self._condition.acquire()


_timer = _DeadlineTimer()


class Lifetime:
    """When one logical operation must stop.

    closing is the token its client cancels when it closes; cancel_token
    is the caller's. deadline is a time.monotonic() value, or None.
    """

    def __init__(self, closing, cancel_token=None, deadline=None):
        self.closing = closing
        self.cancel_token = cancel_token
        self.deadline = deadline

    @classmethod
    def start(cls, closing, cancel_token, request_timeout, deadline):
        """The lifetime of an operation starting now. It ends at the
        earlier of deadline and request_timeout seconds from now."""
        if request_timeout is not None:
            timeout_deadline = time.monotonic() + request_timeout
            if deadline is None or timeout_deadline < deadline:
                deadline = timeout_deadline
        return cls(closing, cancel_token, deadline)

    def remaining(self) -> float | None:
        """Seconds left before the deadline, or None without one."""
        if self.deadline is None:
            return None
        return max(0.0, self.deadline - time.monotonic())

    def bound(self, seconds):
        """seconds, or the time left if that is less. Raises once the
        deadline has passed."""
        remaining = self.remaining()
        if remaining is None:
            return seconds
        if remaining <= 0:
            raise self.stopped_error("waiting")
        return min(seconds, remaining)

    @property
    def stopped(self) -> bool:
        return self.stop_reason() is not None

    def stop_reason(self):
        if self.closing.cancelled:
            return "closed"
        if self.cancel_token is not None and self.cancel_token.cancelled:
            return "cancelled"
        if self.deadline is not None and time.monotonic() >= self.deadline:
            return "deadline"
        return None

    def check(self, phase):
        """Raise if the operation must stop before its next step."""
        if self.stopped:
            raise self.stopped_error(phase)

    def stopped_error(self, phase, remote_outcome_unknown=False):
        """The error for this operation having stopped during phase."""
        reason = self.stop_reason() or "deadline"
        if reason == "closed":
            error_class, what = ClientClosedError, "its client was closed"
        elif reason == "cancelled":
            error_class, what = OperationCancelledError, "it was cancelled"
        else:
            error_class, what = DeadlineExceededError, "it ran out of time"
        message = "The operation stopped because {}".format(what)
        if phase:
            message += " ({})".format(phase)
        message += "."
        if remote_outcome_unknown:
            message += (
                " The request may already have reached the server, so "
                "check whether it took effect before repeating it."
            )
        return error_class(
            message, phase=phase, remote_outcome_unknown=remote_outcome_unknown
        )

    def watch(self, callback) -> Callable[[], None]:
        """Call callback once when the operation must stop, from whichever
        thread notices. Returns the function that stops watching."""
        fired = threading.Event()

        def fire():
            if not fired.is_set():
                fired.set()
                callback()

        stops = [self.closing._subscribe(fire)]
        if self.cancel_token is not None:
            stops.append(self.cancel_token._subscribe(fire))
        if self.deadline is not None:
            stops.append(_timer.schedule(self.deadline, fire))

        def stop_watching():
            for stop in stops:
                stop()

        return stop_watching

    def sleep(self, seconds, phase):
        """Wait seconds, raising at once if the operation must stop."""
        self.check(phase)
        if seconds <= 0:
            return
        woken = threading.Event()
        stop_watching = self.watch(woken.set)
        try:
            woken.wait(seconds)
        finally:
            stop_watching()
        self.check(phase)


def checked_duration(name, value):
    """value as a positive, finite number of seconds, or raise ValueError."""
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
    ):
        raise ValueError(
            "{} must be a positive number of seconds, not {!r}".format(
                name, value
            )
        )
    return value
