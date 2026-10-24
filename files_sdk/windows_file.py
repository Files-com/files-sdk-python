"""Windows' notice of a write to a local file while it uploads.

The SDK checks a local file being uploaded for changes by its identity,
size and times, which Windows does not always update when a file is
written: writes through a handle that stays open can leave all of them as
they were. So on Windows an upload of a local file also asks Windows to tell
it of any write, with a read oplock (FSCTL_REQUEST_OPLOCK at level R alone)
on a handle of its own. That handle shares reading, writing and deleting
with every other, and the oplock needs no acknowledgment: it makes no writer
wait and keeps no one from the file. It is a notice, not a lock.

It is opportunistic. It is asked for only for a file on a local disk (a
request to a file Windows reaches over the network is not allowed), and
Windows grants it only when nothing prevents it, such as another handle's
byte-range lock or a writable mapping of the file. Without it, an upload
relies on the file's metadata alone, as on other systems, which cannot
reveal every change; the log says so, and why, never naming the file. Once
granted, it lasts the whole upload: Windows ending it for any reason, a
write above all, fails the upload as any change does, and it is never asked
for again during that upload.

A request Windows has not finished keeps its handle, event, OVERLAPPED and
buffers until it has. Closing a guard asks Windows to cancel its request
(CancelIoEx only asks); if that has not finished at once, one thread of the
SDK's own, which runs only while there are such requests, keeps them until
it has, then releases them. It looks at all of them again after every wait,
however many there are, and no wait lasts more than a second; that bounds
each wait, not when a release happens, which also depends on that thread
being scheduled, and a wait that fails stops it (see _Settler). A guard is
never freed while Windows may still write to it, even by an owner that
forgets to close it.
"""

import contextlib
import ctypes
import errno
import os
import sys
import threading

import files_sdk.util as util

if sys.platform == "win32":
    import msvcrt
    from ctypes import wintypes

    _GENERIC_READ = 0x80000000
    # FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE.
    _SHARE_ALL = 0x7
    _OPEN_EXISTING = 3
    _FILE_FLAG_OVERLAPPED = 0x40000000
    _INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
    # CTL_CODE(FILE_DEVICE_FILE_SYSTEM, 144, METHOD_BUFFERED, FILE_ANY_ACCESS).
    _FSCTL_REQUEST_OPLOCK = (9 << 16) | (144 << 2)
    _REQUEST_OPLOCK_CURRENT_VERSION = 1
    _OPLOCK_LEVEL_CACHE_READ = 1
    _REQUEST_OPLOCK_INPUT_FLAG_REQUEST = 1
    # What OVERLAPPED.Internal holds while a request is in Windows' hands
    # (HasOverlappedIoCompleted).
    _STATUS_PENDING = 0x103
    _ERROR_IO_PENDING = 997
    _ERROR_NOT_FOUND = 1168
    _VOLUME_NAME_GUID = 0x1
    _PATH_LENGTH = 32768
    # DRIVE_REMOVABLE, DRIVE_FIXED and DRIVE_RAMDISK: local disks.
    _LOCAL_DRIVES = frozenset({2, 3, 6})
    # Answers to a request the SDK itself got wrong, rather than refusals:
    # ERROR_INVALID_HANDLE, ERROR_BAD_LENGTH, ERROR_INVALID_PARAMETER,
    # ERROR_INSUFFICIENT_BUFFER, ERROR_NOACCESS and ERROR_INVALID_USER_BUFFER.
    # Raised, never taken for a refusal.
    _MISTAKES = frozenset({6, 24, 87, 122, 998, 1784})
    _WAIT_FAILED = 0xFFFFFFFF
    _MAXIMUM_WAIT_OBJECTS = 64
    # The longest, in milliseconds, the settler waits before it looks at
    # every guard it keeps again (_Settler).
    _SWEEP_INTERVAL = 1000

    class _Offsets(ctypes.Structure):
        _fields_ = [("Offset", wintypes.DWORD), ("OffsetHigh", wintypes.DWORD)]

    class _OffsetOrPointer(ctypes.Union):
        _fields_ = [("Offsets", _Offsets), ("Pointer", ctypes.c_void_p)]

    class _Overlapped(ctypes.Structure):
        """OVERLAPPED."""

        _fields_ = [
            ("Internal", ctypes.c_size_t),
            ("InternalHigh", ctypes.c_size_t),
            ("Position", _OffsetOrPointer),
            ("hEvent", wintypes.HANDLE),
        ]

    class _OplockInput(ctypes.Structure):
        """REQUEST_OPLOCK_INPUT_BUFFER."""

        _fields_ = [
            ("StructureVersion", wintypes.WORD),
            ("StructureLength", wintypes.WORD),
            ("RequestedOplockLevel", wintypes.DWORD),
            ("Flags", wintypes.DWORD),
        ]

    class _OplockOutput(ctypes.Structure):
        """REQUEST_OPLOCK_OUTPUT_BUFFER."""

        _fields_ = [
            ("StructureVersion", wintypes.WORD),
            ("StructureLength", wintypes.WORD),
            ("OriginalOplockLevel", wintypes.DWORD),
            ("NewOplockLevel", wintypes.DWORD),
            ("Flags", wintypes.DWORD),
            ("AccessMode", wintypes.DWORD),
            ("ShareMode", wintypes.WORD),
        ]

    def _checked_layout():
        """Raise unless the native structures have the sizes Windows gives
        them: a mistake of the SDK's own, never a reason to go on unguarded."""
        pointer = ctypes.sizeof(ctypes.c_void_p)
        expected = {8: (12, 24, 32, 24), 4: (12, 24, 20, 16)}.get(pointer)
        actual = (
            ctypes.sizeof(_OplockInput),
            ctypes.sizeof(_OplockOutput),
            ctypes.sizeof(_Overlapped),
            _Overlapped.hEvent.offset,
        )
        if (
            actual != expected
            or ctypes.sizeof(wintypes.DWORD) != 4
            or _Overlapped.Internal.offset != 0
        ):
            raise RuntimeError(
                "The SDK does not know this Windows layout (sizes {} with {}-byte pointers), "
                "so it cannot ask Windows for notice of writes to a file it uploads".format(
                    actual, pointer
                )
            )

    class _Api:
        """kernel32's functions a guard calls, from a kernel32 of its own so
        that their argument types are set for it alone."""

        def __init__(self):
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            HANDLE, DWORD, BOOL = (
                wintypes.HANDLE,
                wintypes.DWORD,
                wintypes.BOOL,
            )

            def bind(name, restype, *argtypes):
                function = getattr(kernel32, name)
                function.restype, function.argtypes = restype, argtypes
                return function

            self.CreateFileW = bind(
                "CreateFileW",
                HANDLE,
                wintypes.LPCWSTR,
                DWORD,
                DWORD,
                ctypes.c_void_p,
                DWORD,
                DWORD,
                HANDLE,
            )
            self.CloseHandle = bind("CloseHandle", BOOL, HANDLE)
            self.CreateEventW = bind(
                "CreateEventW",
                HANDLE,
                ctypes.c_void_p,
                BOOL,
                BOOL,
                wintypes.LPCWSTR,
            )
            self.SetEvent = bind("SetEvent", BOOL, HANDLE)
            self.DeviceIoControl = bind(
                "DeviceIoControl",
                BOOL,
                HANDLE,
                DWORD,
                ctypes.c_void_p,
                DWORD,
                ctypes.c_void_p,
                DWORD,
                ctypes.POINTER(DWORD),
                ctypes.POINTER(_Overlapped),
            )
            self.CancelIoEx = bind(
                "CancelIoEx", BOOL, HANDLE, ctypes.POINTER(_Overlapped)
            )
            self.WaitForMultipleObjects = bind(
                "WaitForMultipleObjects",
                DWORD,
                DWORD,
                ctypes.POINTER(HANDLE),
                BOOL,
                DWORD,
            )
            self.GetFinalPathNameByHandleW = bind(
                "GetFinalPathNameByHandleW",
                DWORD,
                HANDLE,
                wintypes.LPWSTR,
                DWORD,
                DWORD,
            )
            self.GetDriveTypeW = bind(
                "GetDriveTypeW", wintypes.UINT, wintypes.LPCWSTR
            )

    _api_lock = threading.Lock()
    _bound: "list[_Api | None]" = []

    def _api():
        """The functions a guard calls, bound once; None where this Windows
        lacks one, which leaves the notice unavailable."""
        with _api_lock:
            if not _bound:
                _checked_layout()
                try:
                    _bound.append(_Api())
                except AttributeError:
                    _bound.append(None)
            return _bound[0]

    def acquire(path):
        """A guard on the file at path, its read oplock granted; or None
        where Windows gives none, which is logged by why, never with the
        path. Raises OSError, as opening the file would, if it cannot be
        opened; and for an answer to a request the SDK got wrong."""
        api = _api()
        if api is None:
            _unguarded("unavailable")
            return None
        handle = api.CreateFileW(
            path,
            _GENERIC_READ,
            _SHARE_ALL,
            None,
            _OPEN_EXISTING,
            _FILE_FLAG_OVERLAPPED,
            None,
        )
        if handle is None or handle == _INVALID_HANDLE_VALUE:
            code = ctypes.get_last_error()
            raise OSError(None, ctypes.FormatError(code), path, code)
        try:
            local = _on_local_disk(api, handle)
            # The descriptor owns the handle from here on: closing it closes
            # the handle, once and only once.
            fd = msvcrt.open_osfhandle(handle, os.O_RDONLY) if local else None
        except BaseException:
            _close_handle(api, handle)
            raise
        if fd is None:
            _close_handle(api, handle)
            _unguarded("not on a local disk")
            return None
        try:
            guard = ChangeGuard(api, fd, handle)
        except BaseException:
            # Nothing was asked of Windows yet: the descriptor, and with it
            # the handle, is closed now.
            _close_descriptor(fd)
            raise
        try:
            refusal = guard._request()
        except BaseException:
            guard.close()
            raise
        if refusal is None:
            return guard
        guard.close()
        if refusal in _MISTAKES:
            raise OSError(None, ctypes.FormatError(refusal), path, refusal)
        # Refused at once, or finished at once (0), which grants nothing.
        _unguarded("not granted", error=refusal)
        return None

    def _on_local_disk(api, handle):
        """Whether the file open as handle is on a local disk: one Windows
        names by a volume GUID path, which a file reached over the network
        has none of, on a drive of a local kind. Asked of the file actually
        opened, wherever links led; one this cannot tell is not asked."""
        name = ctypes.create_unicode_buffer(_PATH_LENGTH)
        length = api.GetFinalPathNameByHandleW(
            handle, name, _PATH_LENGTH, _VOLUME_NAME_GUID
        )
        if (
            not length
            or length >= _PATH_LENGTH
            or not name.value.startswith("\\\\?\\Volume{")
        ):
            return False
        end = name.value.find("\\", len("\\\\?\\"))
        return (
            end > 0
            and api.GetDriveTypeW(name.value[: end + 1]) in _LOCAL_DRIVES
        )

    def _close_handle(api, handle):
        if not api.CloseHandle(handle):
            _log_problem("close file", ctypes.get_last_error())

    def _close_descriptor(fd):
        # Closes the handle the descriptor owns too.
        try:
            os.close(fd)
        except OSError as error:
            _log_problem("close file", error.winerror or error.errno)

    def _unguarded(reason, **details):
        util.log_info(
            "Upload checks its file by its metadata alone",
            reason=reason,
            **details,
        )

    def _log_problem(step, error):
        # Cleanup goes on, and the upload's own outcome stands.
        with contextlib.suppress(Exception):
            util.log_warning(
                "Windows notice of file writes not released cleanly",
                step=step,
                error=error,
            )

    # Guards whose request may be in Windows' hands: kept from just before it
    # is sent until it has finished and they are released, whatever their
    # owners do.
    _held: "set[ChangeGuard]" = set()
    _held_lock = threading.Lock()

    class ChangeGuard:
        """One read oplock on a local file, granted to a handle of its own:
        see the module's documentation. intact() says whether Windows has
        told of nothing since it was granted; close() releases it."""

        def __init__(self, api, fd, handle):
            self._api = api
            self._fd: int | None = fd
            self._handle = handle
            # Held while the oplock's state is read or ended, so that neither
            # races a close.
            self._lock = threading.Lock()
            # What the request uses, written by Windows until it finishes.
            self._overlapped = _Overlapped()
            self._input = _OplockInput(
                _REQUEST_OPLOCK_CURRENT_VERSION,
                ctypes.sizeof(_OplockInput),
                _OPLOCK_LEVEL_CACHE_READ,
                _REQUEST_OPLOCK_INPUT_FLAG_REQUEST,
            )
            self._output = _OplockOutput()
            self._event = None
            # Whether the request may be in Windows' hands.
            self._sent = False
            # Whether the oplock ended, or the guard was closed: never intact
            # again.
            self._ended = False
            self._closed = False

        def _request(self):
            """Ask for the oplock. Returns None once it is granted, Windows
            holding the request until the oplock ends; otherwise the error
            that refused it, or 0 for a request finished at once."""
            event = self._api.CreateEventW(None, True, False, None)
            if not event:
                raise ctypes.WinError(ctypes.get_last_error())
            self._event = event
            self._overlapped.hEvent = event
            with _held_lock:
                _held.add(self)
            self._sent = True
            done = self._api.DeviceIoControl(
                self._handle,
                _FSCTL_REQUEST_OPLOCK,
                ctypes.byref(self._input),
                ctypes.sizeof(self._input),
                ctypes.byref(self._output),
                ctypes.sizeof(self._output),
                None,
                ctypes.byref(self._overlapped),
            )
            error = 0 if done else ctypes.get_last_error()
            if error == _ERROR_IO_PENDING:
                return None
            # Finished, granting nothing: nothing of it is in Windows' hands.
            self._sent = False
            return error

        def stat(self):
            """os.fstat of the guard's own handle: the file it is on. A guard
            that has let its handle go (closed, or its notice ended) has none
            to look at, and raises OSError (EBADF). Under the lock, so the
            handle cannot be released while it is looked at."""
            with self._lock:
                fd = self._fd
                if fd is None:
                    raise OSError(errno.EBADF, os.strerror(errno.EBADF))
                return os.fstat(fd)

        def intact(self) -> bool:
            """Whether Windows has told of nothing since the oplock was
            granted: no write, nor anything else that ended it. Once false,
            always false, and false once the guard is closed."""
            with self._lock:
                if self._ended:
                    return False
                if self._overlapped.Internal == _STATUS_PENDING:
                    return True
                # The request has finished: the oplock broke, above all for
                # a write, or Windows ended it otherwise. Either way the
                # notice is gone. With nothing in Windows' hands, the handle
                # is closed at once, which would also release a writer
                # waiting for an acknowledgment, though level R asks none.
                self._ended = True
                self._sent = False
                self._release()
                return False

        def close(self):
            """Release the oplock, its handle and what its request uses: now,
            or, if Windows has not finished the request even once asked to
            cancel it, once it has (_Settler). A failure to release is
            logged, never raised. Safe to repeat."""
            with self._lock:
                if self._closed:
                    return
                self._closed = self._ended = True
                deferred = False
                if self._sent and self._overlapped.Internal == _STATUS_PENDING:
                    # Only asks: the request finishes when Windows says, and
                    # keeps everything it uses until then.
                    if not self._api.CancelIoEx(
                        self._handle, ctypes.byref(self._overlapped)
                    ):
                        error = ctypes.get_last_error()
                        if error != _ERROR_NOT_FOUND:
                            _log_problem("cancel", error)
                    deferred = self._overlapped.Internal == _STATUS_PENDING
                if not deferred:
                    self._sent = False
                    self._release()
            if deferred:
                _settler.keep(self)

        def _release(self):
            # With the lock held, once nothing of the request is in Windows'
            # hands, or it was never sent.
            event, self._event = self._event, None
            fd, self._fd = self._fd, None
            if event is not None and not self._api.CloseHandle(event):
                _log_problem("close event", ctypes.get_last_error())
            if fd is not None:
                _close_descriptor(fd)
            with _held_lock:
                _held.discard(self)

    class _Settler:
        """Keeps closed guards whose request Windows has not finished, even
        once asked to cancel it, and releases each once it has: from one
        thread, which runs only while it keeps any. It waits on the events
        of the first guards, as many as one wait can watch, and on its own
        for a guard kept meanwhile; no wait lasts longer than
        _SWEEP_INTERVAL, and after each it looks at every guard again. So a
        guard that has finished is looked at again within one wait, wherever
        it is among them and even if that event could not be made: a bound
        on each wait, not on when the release happens, which also depends on
        the thread being scheduled. If waiting itself fails, the thread
        stops: its guards stay kept, never freed, until another guard is
        kept and starts it again."""

        def __init__(self):
            self._lock = threading.Lock()
            self._guards: list[ChangeGuard] = []
            # Wakes the thread for a guard kept while it waits.
            self._wake = None
            self._running = False

        def keep(self, guard):
            with self._lock:
                self._guards.append(guard)
                if self._wake is None:
                    self._wake = (
                        guard._api.CreateEventW(None, False, False, None)
                        or None
                    )
                if self._running:
                    if self._wake is not None:
                        guard._api.SetEvent(self._wake)
                    return
                self._running = True
            try:
                threading.Thread(
                    target=self._run,
                    name="files_sdk file notices",
                    daemon=True,
                ).start()
            except Exception as error:
                with self._lock:
                    self._running = False
                _log_problem("keep", type(error).__name__)

        def _run(self):
            while True:
                with self._lock:
                    waiting = []
                    for guard in self._guards:
                        if guard._overlapped.Internal == _STATUS_PENDING:
                            waiting.append(guard)
                            continue
                        with guard._lock:
                            guard._sent = False
                            guard._release()
                    self._guards = waiting
                    if not waiting:
                        self._running = False
                        return
                    # Woken when one of these finishes or a guard is kept,
                    # and at the latest after _SWEEP_INTERVAL, when the
                    # guards beyond these are looked at as well.
                    events = [
                        guard._event
                        for guard in waiting[: _MAXIMUM_WAIT_OBJECTS - 1]
                    ]
                    if self._wake is not None:
                        events.append(self._wake)
                    api = waiting[0]._api
                handles = (wintypes.HANDLE * len(events))(*events)
                if (
                    api.WaitForMultipleObjects(
                        len(events), handles, False, _SWEEP_INTERVAL
                    )
                    == _WAIT_FAILED
                ):
                    _log_problem("wait", ctypes.get_last_error())
                    with self._lock:
                        self._running = False
                    return

    _settler = _Settler()
