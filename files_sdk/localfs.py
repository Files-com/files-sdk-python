"""Local files the SDK writes, reached through directories it has open.

A download to a path, and each file of a folder download, is written into
a temporary file in a private directory of the SDK's own, made inside the
destination's directory, and renamed into place only once it is complete.
Where the operating system supports it (POSIX), every step goes through
open directory descriptors rather than path names:

- A folder download opens its local folder once, and each folder below it
  one step at a time without following links, so a link put in place of a
  folder, before or during the download, cannot lead a file outside.
- The private directory is created with owner-only permissions, and on
  macOS the access control list it inherits is removed before anything is
  made in it; the temporary file has owner-only permissions (and no list)
  from the moment it exists, so no other user can open it or replace it
  while it fills. A checkpoint's temporary file that has since become open
  to others is not resumed.
- The finished file is renamed from the private directory into the
  destination's directory by descriptor, so what is published is the file
  the SDK wrote, into the directory it opened.

This protects against other users and against links, not against code
running as the same user, which can do anything the SDK can, and a
directory that is moved while the download runs is still the one written
to. The permissions of the destination's directory are left as they are.
A file the SDK replaces keeps who can use it: the new file gets its
permissions, owner and group, and its access control list on Linux and
macOS (none, if it has none), or it is not replaced (AccessNotKept). A new
file gets the permissions a new file there would, and on macOS the access
control list its directory passes on to new files, given to it only as it
is renamed into place. Where descriptors cannot be
used (Windows), the same steps use path names, without these protections,
and a replaced file's own access control entries are not carried over.
"""

import ctypes
import ctypes.util
import errno
import os
import stat
import struct
import sys
import threading
import uuid

from files_sdk import access

ANCHORED = (
    os.open in os.supports_dir_fd
    and os.mkdir in os.supports_dir_fd
    and os.rename in os.supports_dir_fd
    and os.unlink in os.supports_dir_fd
    and os.rmdir in os.supports_dir_fd
    and os.stat in os.supports_dir_fd
    and hasattr(os, "O_DIRECTORY")
    and hasattr(os, "O_NOFOLLOW")
)
"""Whether local files are reached through directory descriptors here."""

_BINARY = getattr(os, "O_BINARY", 0)
_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)
_DIRECTORY = getattr(os, "O_DIRECTORY", 0)
_CLOEXEC = getattr(os, "O_CLOEXEC", 0)

PRIVATE_PREFIX = ".files_sdk-"
"""How the SDK's private directories are named: this, then 32 hex digits."""


class LinkRefused(OSError):
    """A link was found where the SDK does not follow one."""


class AccessNotKept(OSError):
    """A file to replace has an owner, group or access control list that
    the SDK cannot give the new file, so it was not replaced: the new file
    would have let other principals use it differently. Also raised when a
    new file cannot be given the access control list its directory passes
    on to new files, so it is not made."""


def identity_of(found):
    return (found.st_dev, found.st_ino)


class Directory:
    """An open directory: by descriptor where ANCHORED, else by path."""

    def __init__(self, path, fd=None):
        self.path = path
        self.fd = fd

    @classmethod
    def open(cls, path):
        """The directory at path, following links in path, as the caller
        chose it."""
        path = os.fspath(path)
        if not ANCHORED:
            if not os.path.isdir(path):
                raise NotADirectoryError(path)
            return cls(path)
        return cls(path, os.open(path, os.O_RDONLY | _DIRECTORY | _CLOEXEC))

    def close(self):
        fd, self.fd = self.fd, None
        if fd is not None:
            os.close(fd)

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.close()

    def join(self, name):
        return os.path.join(self.path, name)

    def _at(self, name):
        # (path, dir_fd) for a call about name in this directory.
        return (
            (name, self.fd) if self.fd is not None else (self.join(name), None)
        )

    def child(self, name, create=False):
        """The directory name in this one, made if create and missing. A
        link there is refused, not followed."""
        path, dir_fd = self._at(name)
        if create:
            try:
                os.mkdir(path, 0o777, dir_fd=dir_fd)
            except FileExistsError:
                pass
        if self.fd is None:
            if os.path.islink(path):
                raise LinkRefused("{} is a symbolic link".format(path))
            if not os.path.isdir(path):
                raise NotADirectoryError(path)
            return Directory(path)
        try:
            fd = os.open(
                path,
                os.O_RDONLY | _DIRECTORY | _NOFOLLOW | _CLOEXEC,
                dir_fd=dir_fd,
            )
        except OSError as error:
            if self.is_link(name):
                raise LinkRefused(
                    "{} is a symbolic link".format(self.join(name))
                ) from None
            raise error
        return Directory(self.join(name), fd)

    def lstat(self, name):
        path, dir_fd = self._at(name)
        return os.stat(path, dir_fd=dir_fd, follow_symlinks=False)

    def is_link(self, name):
        try:
            return stat.S_ISLNK(self.lstat(name).st_mode)
        except FileNotFoundError:
            return False

    def open_file(self, name, flags, mode=0o600):
        """A descriptor for name here, never through a link."""
        path, dir_fd = self._at(name)
        return os.open(
            path, flags | _BINARY | _NOFOLLOW | _CLOEXEC, mode, dir_fd=dir_fd
        )

    def mkdir(self, name, mode):
        path, dir_fd = self._at(name)
        os.mkdir(path, mode, dir_fd=dir_fd)

    def unlink(self, name):
        path, dir_fd = self._at(name)
        os.unlink(path, dir_fd=dir_fd)

    def rmdir(self, name):
        path, dir_fd = self._at(name)
        os.rmdir(path, dir_fd=dir_fd)

    def renames_by_path(self, target):
        """Whether rename_into goes by path names, where directories are not
        held open (Windows)."""
        return self.fd is None or target.fd is None

    def rename_into(self, name, target, target_name):
        """Rename name here to target_name in the directory target,
        replacing what is there."""
        if self.renames_by_path(target):
            os.replace(self.join(name), target.join(target_name))
            return
        os.rename(name, target_name, src_dir_fd=self.fd, dst_dir_fd=target.fd)


class Stage:
    """A private directory of the SDK's own inside a destination's
    directory, holding one temporary file, open for reading and writing
    by position until it is published or discarded."""

    def __init__(
        self,
        parent,
        private_name,
        private,
        private_identity,
        file_name,
        fd,
        file_identity,
        new_file_mode,
    ):
        self.parent = parent
        self.private_name = private_name
        self.private = private
        self.private_identity = private_identity
        self.file_name = file_name
        self.fd = fd
        self.file_identity = file_identity
        self.new_file_mode = new_file_mode
        # Without positional writes, a seek and the write after it go
        # together, whichever thread writes.
        self._seeking = threading.Lock()

    @classmethod
    def create(cls, parent, stem):
        """A new stage in parent, for a file called stem."""
        private_name = PRIVATE_PREFIX + uuid.uuid4().hex
        parent.mkdir(private_name, 0o700)
        private = None
        try:
            private = parent.child(private_name)
            if private.fd is not None:
                # Owner-only, and on macOS without the access control list
                # it inherited, before anything is made in it: from then on
                # no one else can look anything up in it, whatever they
                # opened before.
                _check_private(
                    access.private_folder_problem(private.fd), parent
                )
            elif stat.S_IMODE(parent.lstat(private_name).st_mode) != 0o700:
                # The umask can only remove permissions, so the directory is
                # owner-only; one that removes the owner's own is corrected.
                os.chmod(private.path, 0o700)
            new_file_mode = _new_file_mode(private)
            file_name = _stage_name(stem)
            fd = private.open_file(
                file_name, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600
            )
            try:
                if sys.platform == "darwin":
                    _check_private(
                        access.new_file_problem(fd, "temporary file"), parent
                    )
                return cls(
                    parent,
                    private_name,
                    private,
                    identity_of(parent.lstat(private_name)),
                    file_name,
                    fd,
                    identity_of(os.fstat(fd)),
                    new_file_mode,
                )
            except BaseException:
                os.close(fd)
                try:
                    private.unlink(file_name)
                except OSError:
                    pass
                raise
        except BaseException:
            if private is not None:
                _remove_quietly(private, parent, private_name)
            else:
                try:
                    parent.rmdir(private_name)
                except OSError:
                    pass
            raise

    @classmethod
    def adopt(cls, parent, state, size):
        """The stage a checkpoint recorded, if it is still the SDK's own,
        unchanged and private, else None. It is the SDK's own when its
        private directory, this user's, and its file are the ones recorded
        (not links or replacements), found through the directory held open;
        it is unchanged when the file has size bytes, and private unless
        _exposed. One that is the SDK's own but no longer private is removed
        rather than resumed, where the directory can be held open; anything
        else is left as it is. A new file's permissions come from this
        process, as for a new stage, never from the checkpoint."""
        try:
            private_name, private_identity = state["directory"], tuple(
                state["directory_identity"]
            )
            file_name, file_identity = state["name"], tuple(state["identity"])
            if not (
                isinstance(private_name, str)
                and private_name.startswith(PRIVATE_PREFIX)
                and len(private_name) == len(PRIVATE_PREFIX) + 32
                and isinstance(file_name, str)
                and not any(
                    sep and sep in file_name for sep in (os.sep, os.altsep)
                )
                and file_name not in ("", ".", "..")
            ):
                return None
            found = parent.lstat(private_name)
            if (
                not stat.S_ISDIR(found.st_mode)
                or identity_of(found) != private_identity
                or (
                    sys.platform != "win32"
                    and hasattr(os, "geteuid")
                    and found.st_uid != os.geteuid()
                )
            ):
                return None
            private = parent.child(private_name)
        except (KeyError, TypeError, ValueError, OSError):
            return None
        try:
            if private.fd is not None:
                directory = os.fstat(private.fd)
                if identity_of(directory) != private_identity:
                    private.close()
                    return None
            else:
                directory = found
            fd = private.open_file(file_name, os.O_RDWR)
        except OSError:
            private.close()
            return None
        found = os.fstat(fd)
        if (
            not stat.S_ISREG(found.st_mode)
            or identity_of(found) != file_identity
            or found.st_size != size
        ):
            os.close(fd)
            private.close()
            return None
        try:
            exposed = _exposed(private, directory, fd, found)
        except BaseException:
            os.close(fd)
            private.close()
            raise
        if exposed:
            if private.fd is not None:
                # Unlinking cannot close what others opened, but ends access
                # by name and leaves no partial file behind; only the file
                # and directory just verified are removed, the directory
                # only if empty.
                cls(
                    parent,
                    private_name,
                    private,
                    private_identity,
                    file_name,
                    fd,
                    file_identity,
                    None,
                ).discard()
            else:
                os.close(fd)
                private.close()
            return None
        try:
            new_file_mode = _new_file_mode(private)
        except BaseException:
            os.close(fd)
            private.close()
            raise
        return cls(
            parent,
            private_name,
            private,
            private_identity,
            file_name,
            fd,
            file_identity,
            new_file_mode,
        )

    def state(self):
        return {
            "directory": self.private_name,
            "directory_identity": list(self.private_identity),
            "name": self.file_name,
            "identity": list(self.file_identity),
        }

    def truncate(self, size):
        os.ftruncate(self.fd, size)

    def write_at(self, offset, data):
        """Write all of data at offset."""
        with memoryview(data) as view:
            done = 0
            while done < len(view):
                # The platform check lets type checkers see where os.pwrite
                # exists; the attribute check keeps the fallback wherever it
                # does not.
                if sys.platform != "win32" and hasattr(os, "pwrite"):
                    written = os.pwrite(self.fd, view[done:], offset + done)
                else:  # Windows: ranges written by several threads take turns.
                    with self._seeking:
                        os.lseek(self.fd, offset + done, os.SEEK_SET)
                        written = os.write(self.fd, view[done:])
                if written <= 0:
                    raise OSError("the temporary file took no bytes")
                done += written

    def sync(self):
        os.fsync(self.fd)

    def _is_ours(self):
        try:
            found = self.private.lstat(self.file_name)
        except FileNotFoundError:
            return False
        return (
            stat.S_ISREG(found.st_mode)
            and identity_of(found) == self.file_identity
        )

    def publish(self, target_name, confined):
        """Rename the file to target_name in the parent directory, with a
        new file's permissions, or the access of the file it replaces: its
        permissions (without set-user-ID, set-group-ID or sticky bits),
        owner, group and access control list (see _keep_access). A confined
        destination that is a link is refused rather than replaced."""
        try:
            found = self.parent.lstat(target_name)
        except FileNotFoundError:
            mode = self.new_file_mode
            _inherit_access(self.parent, self.fd)
        else:
            if stat.S_ISLNK(found.st_mode):
                if confined:
                    raise LinkRefused(
                        "{} is a symbolic link; a folder download does not write through links".format(
                            self.parent.join(target_name)
                        )
                    )
                # A single file's link was followed when its path was
                # resolved, so it is not here.
            else:
                _keep_access(self.parent, target_name, found, self.fd)
            mode = stat.S_IMODE(found.st_mode) & 0o777
        # Windows has fchmod from Python 3.13.
        if (
            sys.platform != "win32" or sys.version_info >= (3, 13)
        ) and hasattr(os, "fchmod"):
            os.fchmod(self.fd, mode)
        else:
            os.chmod(self.private.join(self.file_name), mode)
        if not self._is_ours():
            raise ReplacedStage(self.private.join(self.file_name))
        if self.private.renames_by_path(self.parent):
            # Windows does not rename a file this process holds open: os.open
            # does not share deletion. The file is closed first, and opened
            # again if it is not renamed, so that a checkpoint can still sync
            # and keep it.
            self.close()
            try:
                self.private.rename_into(
                    self.file_name, self.parent, target_name
                )
            except BaseException as error:
                self._reopen(error)
                raise
        else:
            self.private.rename_into(self.file_name, self.parent, target_name)
            self.close()
        self._remove_private()

    def _reopen(self, error):
        """Open the file again after it was closed to be renamed and was not
        (error is why), if it is still the SDK's own; otherwise it stays
        closed, with a note on error saying why. Nothing here is raised in
        place of error."""
        path = self.private.join(self.file_name)
        try:
            fd = self.private.open_file(self.file_name, os.O_RDWR)
        except OSError as problem:
            error.add_note(
                "The temporary file {} could not be opened again: {}".format(
                    path, problem
                )
            )
            return
        try:
            mine = identity_of(os.fstat(fd)) == self.file_identity
        except OSError:
            mine = False
        if mine:
            self.fd = fd
            return
        try:
            os.close(fd)
        except OSError:
            pass
        error.add_note(
            "The temporary file {} is no longer the SDK's own".format(path)
        )

    def close(self):
        fd, self.fd = self.fd, -1
        if fd >= 0:
            os.close(fd)

    def discard(self):
        """Remove the file and the private directory, if they are still
        the SDK's own; never a file put in their place."""
        self.close()
        try:
            if self._is_ours():
                self.private.unlink(self.file_name)
        except OSError:
            pass
        self._remove_private()

    def keep(self):
        """Close the file, leaving it and its directory for a checkpoint."""
        self.close()
        self.private.close()

    def _remove_private(self):
        _remove_quietly(
            self.private, self.parent, self.private_name, self.private_identity
        )


class ReplacedStage(OSError):
    """The temporary file is no longer the SDK's own."""


def _check_private(problem, parent):
    if problem is not None:
        raise PermissionError(
            errno.EACCES,
            "The SDK's temporary file in {} could not be made private: {}".format(
                parent.path, problem
            ),
        )


def _exposed(private, directory, fd, found):
    """Whether a temporary file the SDK made private (open as fd; found is
    its status) or its private directory (directory is its status) has
    since become usable by others: by the directory's or the file's
    permissions, the file's owner, or on macOS an access control list on
    either. Windows permissions show only whether an item is read-only, so
    there it is by owners and access control lists (see files_sdk.access):
    the file's must let no one but this user, the system or administrators
    use it, and the private directory and every folder above it must let no
    one else delete, replace or re-permission them or what is in them, nor
    be a link or junction; what cannot be read counts as usable by others.
    Whoever opened it meanwhile keeps what they opened, however the
    permissions are changed back, so such a file is never resumed."""
    if sys.platform == "win32":
        try:
            return (
                access.namespace_problem(private.path) is not None
                or access.new_file_problem(fd, "temporary file") is not None
            )
        except OSError:
            return True
    if stat.S_IMODE(directory.st_mode) & 0o077:
        return True
    if stat.S_IMODE(found.st_mode) & 0o077 or found.st_uid != os.geteuid():
        return True
    return private.fd is not None and (
        access.exposed_problem(private.fd, "a temporary directory") is not None
        or access.exposed_problem(fd, "a temporary file") is not None
    )


def _keep_access(parent, name, found, fd):
    """Give fd's file the owner, group and access control list of found,
    the file name in parent that it is about to replace, or raise
    AccessNotKept before anything is replaced. Changing a file to another
    owner takes privileges, and to another group membership of it, so a
    file of another user or of a group the process is not in is not
    replaced. Access control lists are copied on Linux and macOS; other
    systems have none the SDK can read, and Windows keeps its own."""
    path = parent.join(name)
    mine = os.fstat(fd)
    uid = found.st_uid if found.st_uid != mine.st_uid else -1
    gid = found.st_gid if found.st_gid != mine.st_gid else -1
    if (
        (uid, gid) != (-1, -1)
        and sys.platform != "win32"
        and hasattr(os, "fchown")
    ):
        try:
            os.fchown(fd, uid, gid)
        except PermissionError:
            whose = "user" if uid != -1 else "group"
            raise AccessNotKept(
                errno.EPERM,
                "{} belongs to another {}, which the new file cannot be given, so "
                "it was not replaced".format(path, whose),
            ) from None
    _copy_acl(parent, name, found, fd, path)


def _unreadable_acl(path, error=None):
    reason = ": {}".format(os.strerror(error)) if error else ""
    return AccessNotKept(
        error or errno.EACCES,
        "The access control list of {} could not be copied{}, so it was not replaced".format(
            path, reason
        ),
    )


def _changed(path):
    return AccessNotKept(
        errno.EAGAIN,
        "{} changed or moved while it was being replaced, so it was not replaced".format(
            path
        ),
    )


def _check_same(parent, name, found, path, by_path):
    """Raise unless name in parent, and path too when what was read came by
    path, is still found's file, so what was read belongs to the file being
    replaced."""
    try:
        same = identity_of(parent.lstat(name)) == identity_of(found) and (
            not by_path or identity_of(os.lstat(path)) == identity_of(found)
        )
    except FileNotFoundError:
        same = False
    if not same:
        raise _changed(path)


_LINUX_ACL = "system.posix_acl_access"


def _copy_acl(parent, name, found, fd, path):
    """Give fd's file the access control list of found, the file name in
    parent (at path) that it replaces, on Linux and macOS. The list is read
    through the directory the SDK holds open, which still leads to the file
    if the directory has moved, and checked to be found's; a list that
    cannot be read, or a file that cannot be found again, is not taken for
    no list."""
    if sys.platform == "linux":
        # Through the held directory where /proc allows it, else by path,
        # checked to lead to the same file.
        by_path = parent.fd is None or not os.path.isdir("/proc/self/fd")
        target = (
            path if by_path else "/proc/self/fd/{}/{}".format(parent.fd, name)
        )
        try:
            acl = os.getxattr(target, _LINUX_ACL, follow_symlinks=False)
        except OSError as error:
            if error.errno not in (
                errno.ENODATA,
                errno.ENOTSUP,
                errno.EOPNOTSUPP,
            ):
                raise _unreadable_acl(path, error.errno) from None
            acl = None  # No list, or none possible on this file system.
        _check_same(parent, name, found, path, by_path)
        try:
            if acl is not None:
                os.setxattr(fd, _LINUX_ACL, acl)
            else:
                # Nor for the new file, whatever it inherited.
                os.removexattr(fd, _LINUX_ACL)
        except OSError as error:
            if acl is not None or error.errno not in (
                errno.ENODATA,
                errno.ENOTSUP,
                errno.EOPNOTSUPP,
            ):
                raise _unreadable_acl(path, error.errno) from None
    elif sys.platform == "darwin":
        _copy_darwin_acl(parent, name, found, fd, path)


class _AttrList(ctypes.Structure):
    """struct attrlist, which asks getattrlistat(2) for attributes."""

    _fields_ = [
        ("bitmapcount", ctypes.c_ushort),
        ("reserved", ctypes.c_uint16),
        ("commonattr", ctypes.c_uint32),
        ("volattr", ctypes.c_uint32),
        ("dirattr", ctypes.c_uint32),
        ("fileattr", ctypes.c_uint32),
        ("forkattr", ctypes.c_uint32),
    ]


_ATTR_CMN_RETURNED_ATTRS = 0x80000000
_ATTR_CMN_DEVID = 0x00000002
_ATTR_CMN_EXTENDED_SECURITY = 0x00400000
_ATTR_CMN_FILEID = 0x02000000
_FSOPT_NOFOLLOW = 0x00000001
_FSOPT_PACK_INVAL_ATTRS = 0x00000008
_AT_FDCWD = -2
_ACL_TYPE_EXTENDED = 0x00000100
# What getattrlistat returns for those attributes: its length, the common
# attributes it returned, the device, the list's reference (an offset from
# the reference itself, and a length), the file ID, then the list.
_ATTRIBUTES = struct.Struct("=II16xiiIQ")
_LIST_REFERENCE = 28
# Room for the largest list: 128 entries of 24 bytes and its 44-byte header.
_ATTRIBUTE_BUFFER = 8192
_libc = None


def _darwin_libc():
    global _libc
    if _libc is None:
        libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
        libc.getattrlistat.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.POINTER(_AttrList),
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.c_ulong,
        ]
        libc.acl_get_fd_np.restype = ctypes.c_void_p
        libc.acl_get_fd_np.argtypes = [ctypes.c_int, ctypes.c_int]
        libc.acl_copy_int_native.restype = ctypes.c_void_p
        libc.acl_copy_int_native.argtypes = [ctypes.c_void_p]
        libc.acl_set_fd_np.argtypes = [
            ctypes.c_int,
            ctypes.c_void_p,
            ctypes.c_int,
        ]
        libc.acl_free.argtypes = [ctypes.c_void_p]
        _libc = libc
    return _libc


def _copy_darwin_acl(parent, name, found, fd, path):
    # getattrlistat describes name in the held directory without opening
    # it or following a link, so a file no one may read is described too,
    # and says which file it described.
    libc = _darwin_libc()
    request = _AttrList(
        5,
        0,
        _ATTR_CMN_RETURNED_ATTRS
        | _ATTR_CMN_DEVID
        | _ATTR_CMN_EXTENDED_SECURITY
        | _ATTR_CMN_FILEID,
        0,
        0,
        0,
        0,
    )
    buffer = ctypes.create_string_buffer(_ATTRIBUTE_BUFFER)
    directory, relative = (
        (parent.fd, name) if parent.fd is not None else (_AT_FDCWD, path)
    )
    ctypes.set_errno(0)
    options = _FSOPT_NOFOLLOW | _FSOPT_PACK_INVAL_ATTRS
    if (
        libc.getattrlistat(
            directory,
            os.fsencode(relative),
            ctypes.byref(request),
            buffer,
            len(buffer),
            options,
        )
        != 0
    ):
        raise _unreadable_acl(path, ctypes.get_errno())
    length, returned, device, offset, size, file_id = _ATTRIBUTES.unpack_from(
        buffer
    )
    if (device & 0xFFFFFFFF, file_id) != (
        found.st_dev & 0xFFFFFFFF,
        found.st_ino,
    ):
        raise _changed(path)
    if not returned & _ATTR_CMN_EXTENDED_SECURITY or not size:
        # No list, or none possible on this file system: nor for the new file.
        problem = access.new_file_problem(fd, "temporary file")
        if problem is not None:
            raise AccessNotKept(
                errno.EACCES,
                "{}, so {} was not replaced".format(problem, path),
            )
        return
    if length > len(buffer) or _LIST_REFERENCE + offset + size > length:
        raise _unreadable_acl(path, errno.ERANGE)
    acl = libc.acl_copy_int_native(
        ctypes.addressof(buffer) + _LIST_REFERENCE + offset
    )
    if not acl:
        raise _unreadable_acl(path, ctypes.get_errno())
    try:
        if libc.acl_set_fd_np(fd, acl, _ACL_TYPE_EXTENDED) != 0:
            raise _unreadable_acl(path, ctypes.get_errno())
    finally:
        libc.acl_free(acl)


def _inherit_access(parent, fd):
    """Give fd's file, about to become a new file in parent, the access
    control list a file made there gets, on macOS, where a new file takes
    the entries its directory passes on. The temporary file was made
    without them, so that no one else could use it while it filled. What
    parent passes on is observed by making an empty file in it, as only the
    system decides that, and removing it."""
    if sys.platform != "darwin" or parent.fd is None:
        return
    libc = _darwin_libc()
    name = PRIVATE_PREFIX + uuid.uuid4().hex + ".new"
    probe = parent.open_file(name, os.O_CREAT | os.O_EXCL | os.O_RDONLY, 0o600)
    try:
        ctypes.set_errno(0)
        acl = libc.acl_get_fd_np(probe, _ACL_TYPE_EXTENDED)
        code = ctypes.get_errno()
    finally:
        os.close(probe)
        try:
            parent.unlink(name)
        except OSError:
            pass
    if not acl:
        if code in (errno.ENOENT, errno.ENOTSUP, errno.EOPNOTSUPP):
            return  # None passed on, or none possible on this file system.
        raise _not_inherited(parent, code)
    try:
        if libc.acl_set_fd_np(fd, acl, _ACL_TYPE_EXTENDED) != 0:
            raise _not_inherited(parent, ctypes.get_errno())
    finally:
        libc.acl_free(acl)


def _not_inherited(parent, error):
    return AccessNotKept(
        error or errno.EACCES,
        "The access control list {} passes on to new files could not be given to the new file ({}), so it "
        "was not made".format(parent.path, os.strerror(error or errno.EACCES)),
    )


def _stage_name(stem):
    # Bounded, whatever the destination's name.
    return (stem[:64] or "file") + ".files_sdk-download"


def _new_file_mode(private):
    """The permissions a new file gets under the process's umask, observed
    by creating an empty file in the private directory (reading the umask
    would mean setting it, for every thread at once)."""
    name = ".mode-" + uuid.uuid4().hex
    fd = private.open_file(name, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o666)
    try:
        return stat.S_IMODE(os.fstat(fd).st_mode) & 0o777
    finally:
        os.close(fd)
        private.unlink(name)


def _remove_quietly(private, parent, private_name, private_identity=None):
    """Remove the private directory if it is empty and still the SDK's."""
    private.close()
    try:
        found = parent.lstat(private_name)
        if stat.S_ISDIR(found.st_mode) and (
            private_identity is None or identity_of(found) == private_identity
        ):
            parent.rmdir(private_name)
    except OSError:
        pass
