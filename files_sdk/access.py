"""Who besides this process's user can change a local file or folder.

A checkpoint is used only where no other principal can have written it (see
files_sdk.checkpoint). These checks decide that, on each system, from what
it actually enforces:

- POSIX: the owner, and whether the group or others may write. On Linux an
  access control list that lets a named user or group write shows in the
  group permissions (its mask), so the same check covers it.
- macOS: also its extended access control list, which the permissions do
  not show: an entry that allows anyone but this user to write, append,
  delete, change attributes or extended attributes, change the list or take
  ownership. A deny entry takes nothing away from the owner, and an entry
  that is only inherited by new items does not apply to the item itself.
- Windows: the owner and the discretionary access control list, read with
  GetFileSecurityW (a folder, by path) or GetKernelObjectSecurity (a file
  the SDK holds open) and read here: an entry that allows anyone but this
  user, the system or administrators to change the item, or, for a folder,
  to delete or replace what is in it.

A download's temporary file and its private directory are made private,
and checked to be still private when resumed, with the same helpers (see
files_sdk.localfs).

Anything that cannot be read is refused rather than taken for no access.
Code running as the same user, or as the system or an administrator, is
trusted like the SDK itself.
"""

import ctypes
import ctypes.util
import errno
import os
import stat
import struct
import sys

WINDOWS = sys.platform == "win32"
_DARWIN = sys.platform == "darwin"

# The most symbolic links followed on the way to a folder, as the operating
# system itself allows.
_MAX_LINKS = 40


def namespace_problem(directory) -> str | None:
    """Why a file in directory could be written or replaced by a principal
    other than this process's user, or None when it could not.

    Walks the path from its root as the operating system resolves it. On
    POSIX every folder on the way must belong to this user or to root and
    must not let its group or other users write (unless it is sticky, as
    /tmp is, where others can add entries but not remove or replace this
    user's), nor, on macOS, let anyone else change it through its access
    control list; every symbolic link on the way must belong to this user
    or to root, and on macOS let no one else change it, so no one else can
    point it elsewhere. On Windows every folder must belong to this user,
    the system or administrators and let no one else delete, replace or
    re-permission it or what is in it; a link or junction on the way is
    refused."""
    if sys.platform == "win32":
        return _windows_namespace_problem(directory)
    user = os.geteuid()
    current = os.sep
    pending = [
        part for part in os.path.abspath(directory).split(os.sep) if part
    ]
    links = 0
    problem = _directory_problem(current, os.stat(current), user)
    while problem is None and pending:
        part = pending.pop(0)
        if part == ".":
            continue
        if part == "..":
            current = os.path.dirname(current)
            continue
        path = os.path.join(current, part)
        found = os.lstat(path)
        if stat.S_ISLNK(found.st_mode):
            links += 1
            if found.st_uid not in (user, 0):
                return "{} is a symbolic link that belongs to another user".format(
                    path
                )
            if links > _MAX_LINKS:
                return "its path has too many symbolic links"
            problem = _darwin_path_problem(path) if _DARWIN else None
            if problem is not None:
                return problem
            target = os.readlink(path)
            if os.path.isabs(target):
                current = os.sep
            pending[:0] = [piece for piece in target.split(os.sep) if piece]
            continue
        if not stat.S_ISDIR(found.st_mode):
            raise NotADirectoryError(
                errno.ENOTDIR, os.strerror(errno.ENOTDIR), path
            )
        problem = _directory_problem(path, found, user)
        current = path
    return problem


def _directory_problem(path, found, user):
    if found.st_uid not in (user, 0):
        return "{} belongs to another user".format(path)
    if (
        found.st_mode & (stat.S_IWGRP | stat.S_IWOTH)
        and not found.st_mode & stat.S_ISVTX
    ):
        return (
            "{} can be changed by other users (its permissions are {})".format(
                path, stat.filemode(found.st_mode)
            )
        )
    return _darwin_path_problem(path) if _DARWIN else None


def file_problem(fd, what) -> str | None:
    """Why the file open as fd (the checkpoint or its lock file) could have
    been written by a principal other than this process's user, or None.
    What is checked is the file held open, not whatever a path now names."""
    found = os.fstat(fd)
    if not stat.S_ISREG(found.st_mode):
        return "its {} is not a regular file".format(what)
    if sys.platform == "win32":
        return _windows_problem(
            _windows_fd_descriptor(fd),
            _windows_user(),
            "its " + what,
            _FILE_WRITES,
            _FILE_OWNERS,
        )
    if found.st_uid != os.geteuid():
        return "its {} belongs to another user".format(what)
    if found.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        return "its {} can be changed by other users (its permissions are {})".format(
            what, stat.filemode(found.st_mode)
        )
    if _DARWIN:
        return _darwin_acl_problem(
            _darwin().acl_get_fd_np(fd, _ACL_TYPE_EXTENDED), "its " + what
        )
    return None


def new_file_problem(fd, what) -> str | None:
    """Make a file the SDK has just created (open as fd, with owner-only
    permissions) private before anything is written to it, or say why it
    cannot be: on macOS its extended access control list, which it may have
    inherited from its folder, is removed; on Windows it must not have
    inherited access for anyone but this user, the system or
    administrators. Elsewhere its permissions suffice (on Linux an
    inherited list is limited by them)."""
    if sys.platform == "win32":
        return _windows_problem(
            _windows_fd_descriptor(fd),
            _windows_user(),
            "a new " + what,
            _NEW_FILE_ACCESS,
            _FILE_OWNERS,
        )
    if _DARWIN:
        libc = _darwin()
        empty = libc.acl_init(0)
        if not empty:
            raise MemoryError("acl_init")
        try:
            if libc.acl_set_fd_np(fd, empty, _ACL_TYPE_EXTENDED) != 0:
                code = ctypes.get_errno()
                if code not in _NO_ACL_SUPPORT:
                    return "the access control list of a new {} could not be removed ({})".format(
                        what, os.strerror(code)
                    )
        finally:
            libc.acl_free(empty)
        return _darwin_acl_problem(
            libc.acl_get_fd_np(fd, _ACL_TYPE_EXTENDED),
            "a new " + what,
            any_allow=True,
        )
    return None


def private_folder_problem(fd) -> str | None:
    """Make a folder the SDK has just made (open as fd) private before any
    file is made in it, or say why it cannot be: it must be this user's own
    and owner-only, and on macOS its access control list, which it may have
    inherited, is removed. From then on no one else can look anything up in
    it, whatever they opened before: each lookup is checked when it is
    made."""
    found = os.fstat(fd)
    if not stat.S_ISDIR(found.st_mode):
        return "a new staging folder is not a folder"
    if sys.platform != "win32":
        if found.st_uid != os.geteuid():
            return "a new staging folder belongs to another user"
        if stat.S_IMODE(found.st_mode) != 0o700:
            # The umask can only remove permissions; one that removed the
            # owner's own is corrected.
            os.fchmod(fd, 0o700)
    return new_file_problem(fd, "staging folder")


def exposed_problem(fd, what) -> str | None:
    """Why an item the SDK made private (open as fd; see
    private_folder_problem and new_file_problem) no longer is, or None: on
    macOS, any entry in its access control list that allows anything. The
    list is only read: removing it now would not take back what anyone
    opened while it was there."""
    if _DARWIN:
        return _darwin_acl_problem(
            _darwin().acl_get_fd_np(fd, _ACL_TYPE_EXTENDED),
            what,
            any_allow=True,
        )
    return None


def acl_supported(fd) -> bool:
    """Whether the file system of fd (open) keeps extended access control
    lists, which a new file could inherit: on macOS, as it reports; never
    elsewhere (Linux limits an inherited list by the permissions a file is
    made with)."""
    if not _DARWIN:
        return False
    acl = _darwin().acl_get_fd_np(fd, _ACL_TYPE_EXTENDED)
    if acl:
        _darwin().acl_free(acl)
        return True
    return ctypes.get_errno() not in _NO_ACL_SUPPORT - {errno.ENOENT}


def inheritance_problem(directory) -> str | None:
    """Why a new file made in directory would, from the moment it exists, let
    a principal other than this user use it, or None. On Windows a new file
    gets the entries its folder marks for files to inherit, so such an entry
    that gives anyone but this user, the system or administrators any access
    refuses the folder. Elsewhere the SDK makes new checkpoint files where no
    one else can reach them (see files_sdk.checkpoint), so nothing is
    refused here."""
    if sys.platform == "win32":
        return _windows_inheritance_problem(
            _windows_path_descriptor(directory), _windows_user(), directory
        )
    return None


# macOS extended access control lists (sys/acl.h, membership.h).

_ACL_TYPE_EXTENDED = 0x00000100
_ACL_EXTENDED_ALLOW = 1
_ACL_FIRST_ENTRY = 0
_ACL_NEXT_ENTRY = -1
_ACL_ENTRY_ONLY_INHERIT = 1 << 8
# Rights that let a principal change an item or what is in it: write or add
# a file, delete, append or add a folder, delete a child, write attributes
# or extended attributes, change the list, take ownership.
_ACL_WRITES = (
    (1 << 2)
    | (1 << 4)
    | (1 << 5)
    | (1 << 6)
    | (1 << 8)
    | (1 << 10)
    | (1 << 12)
    | (1 << 13)
)
# What a file system without extended lists answers.
_NO_ACL_SUPPORT = frozenset(
    code
    for code in (
        errno.ENOENT,
        getattr(errno, "ENOTSUP", None),
        getattr(errno, "EOPNOTSUPP", None),
    )
    if code is not None
)
_libc = None
_user_uuid: bytes | None = None


def _darwin():
    global _libc
    if _libc is None:
        libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
        pointer = ctypes.c_void_p
        libc.acl_get_fd_np.restype = pointer
        libc.acl_get_fd_np.argtypes = [ctypes.c_int, ctypes.c_int]
        libc.acl_get_link_np.restype = pointer
        libc.acl_get_link_np.argtypes = [ctypes.c_char_p, ctypes.c_int]
        libc.acl_get_entry.argtypes = [
            pointer,
            ctypes.c_int,
            ctypes.POINTER(pointer),
        ]
        libc.acl_get_tag_type.argtypes = [
            pointer,
            ctypes.POINTER(ctypes.c_int),
        ]
        libc.acl_get_permset_mask_np.argtypes = [
            pointer,
            ctypes.POINTER(ctypes.c_uint64),
        ]
        libc.acl_get_flagset_np.argtypes = [pointer, ctypes.POINTER(pointer)]
        libc.acl_get_flag_np.argtypes = [pointer, ctypes.c_int]
        libc.acl_get_qualifier.restype = pointer
        libc.acl_get_qualifier.argtypes = [pointer]
        libc.acl_init.restype = pointer
        libc.acl_init.argtypes = [ctypes.c_int]
        libc.acl_set_fd_np.argtypes = [ctypes.c_int, pointer, ctypes.c_int]
        libc.acl_free.argtypes = [pointer]
        libc.mbr_uid_to_uuid.argtypes = [ctypes.c_uint32, ctypes.c_char_p]
        _libc = libc
    return _libc


def _darwin_user_uuid():
    """This user's UUID, as access control list entries name principals, or
    None if it cannot be told (then every entry is taken for another's)."""
    global _user_uuid
    if sys.platform == "win32":
        return None
    if _user_uuid is None:
        buffer = ctypes.create_string_buffer(16)
        _user_uuid = (
            buffer.raw
            if _darwin().mbr_uid_to_uuid(os.geteuid(), buffer) == 0
            else b""
        )
    return _user_uuid or None


def _darwin_path_problem(path):
    """The access control list problem of path itself (a folder or a link,
    never followed)."""
    return _darwin_acl_problem(
        _darwin().acl_get_link_np(os.fsencode(path), _ACL_TYPE_EXTENDED), path
    )


def _darwin_acl_problem(acl, what, any_allow=False):
    """Why the list acl (from acl_get_*_np, freed here) lets a principal
    other than this user change what, or None. With any_allow, any allow
    entry at all is a problem (a list the SDK meant to remove)."""
    libc = _darwin()
    if not acl:
        code = ctypes.get_errno()
        if code in _NO_ACL_SUPPORT:
            return None
        return "the access control list of {} could not be read ({})".format(
            what, os.strerror(code)
        )
    try:
        own = _darwin_user_uuid()
        entry = ctypes.c_void_p()
        which = _ACL_FIRST_ENTRY
        while libc.acl_get_entry(acl, which, ctypes.byref(entry)) == 0:
            which = _ACL_NEXT_ENTRY
            tag = ctypes.c_int()
            flags = ctypes.c_void_p()
            mask = ctypes.c_uint64()
            if (
                libc.acl_get_tag_type(entry, ctypes.byref(tag)) != 0
                or libc.acl_get_flagset_np(entry, ctypes.byref(flags)) != 0
                or libc.acl_get_permset_mask_np(entry, ctypes.byref(mask)) != 0
            ):
                return (
                    "the access control list of {} could not be read".format(
                        what
                    )
                )
            if (
                tag.value != _ACL_EXTENDED_ALLOW
                or libc.acl_get_flag_np(flags, _ACL_ENTRY_ONLY_INHERIT) == 1
            ):
                continue
            if any_allow:
                return "{} still has an access control list".format(what)
            if not mask.value & _ACL_WRITES:
                continue
            qualifier = libc.acl_get_qualifier(entry)
            try:
                mine = (
                    bool(qualifier)
                    and own is not None
                    and ctypes.string_at(qualifier, 16) == own
                )
            finally:
                if qualifier:
                    libc.acl_free(qualifier)
            if not mine:
                return "{} has an access control list entry that lets another user or group change it".format(
                    what
                )
        return None
    finally:
        libc.acl_free(acl)


# Windows security descriptors (winnt.h), read here from their
# self-relative form.

_DELETE = 0x00010000
_WRITE_DAC = 0x00040000
_WRITE_OWNER = 0x00080000
_GENERIC_ALL = 0x10000000
_GENERIC_WRITE = 0x40000000
_GENERIC_READ = 0x80000000
_FILE_READ_DATA = 0x0001
_FILE_WRITE_DATA = 0x0002
_FILE_APPEND_DATA = 0x0004
_FILE_READ_EA = 0x0008
_FILE_WRITE_EA = 0x0010
_FILE_DELETE_CHILD = 0x0040
_FILE_WRITE_ATTRIBUTES = 0x0100
# A folder: deleting, replacing or re-permissioning it or what is in it.
# (Adding entries, as FILE_ADD_FILE allows, cannot replace this user's.)
_FOLDER_WRITES = (
    _DELETE
    | _WRITE_DAC
    | _WRITE_OWNER
    | _FILE_DELETE_CHILD
    | _GENERIC_ALL
    | _GENERIC_WRITE
)
# A file: changing its contents, attributes, permissions or owner, or
# deleting it.
_FILE_WRITES = (
    _FILE_WRITE_DATA
    | _FILE_APPEND_DATA
    | _FILE_WRITE_EA
    | _FILE_WRITE_ATTRIBUTES
    | _DELETE
    | _WRITE_DAC
    | _WRITE_OWNER
    | _GENERIC_ALL
    | _GENERIC_WRITE
)
# A new checkpoint file, before anything is written to it: nor reading it.
_NEW_FILE_ACCESS = (
    _FILE_WRITES | _FILE_READ_DATA | _FILE_READ_EA | _GENERIC_READ
)
_SE_DACL_PRESENT = 0x0004
_OBJECT_INHERIT_ACE = 0x01
_INHERIT_ONLY_ACE = 0x08
_ACCESS_ALLOWED_ACE = 0x00
# Allow entries of other forms (object and callback entries), which the
# SDK does not read: any of them is refused.
_OTHER_ALLOW_ACES = frozenset({0x05, 0x09, 0x0B})
_SYSTEM = "S-1-5-18"
_ADMINISTRATORS = "S-1-5-32-544"
_TRUSTED_INSTALLER = (
    "S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464"
)
_CREATOR_OWNER = "S-1-3-0"
_OWNER_RIGHTS = "S-1-3-4"
_FOLDER_OWNERS = frozenset({_SYSTEM, _ADMINISTRATORS, _TRUSTED_INSTALLER})
_FILE_OWNERS = frozenset({_SYSTEM, _ADMINISTRATORS})
_TRUSTED_ENTRIES = frozenset(
    {
        _SYSTEM,
        _ADMINISTRATORS,
        _TRUSTED_INSTALLER,
        _CREATOR_OWNER,
        _OWNER_RIGHTS,
    }
)
_FILE_ATTRIBUTE_REPARSE_POINT = 0x400
# A reparse point that stands for another name: a symbolic link or junction.
_NAME_SURROGATE = 0x20000000


def sid_string(data, offset=0) -> str:
    """The S-1-... form of the binary SID at offset in data."""
    revision, count = data[offset], data[offset + 1]
    authority = int.from_bytes(data[offset + 2 : offset + 8], "big")
    parts = struct.unpack_from("<{}I".format(count), data, offset + 8)
    return "S-{}-{}".format(revision, authority) + "".join(
        "-{}".format(part) for part in parts
    )


def _windows_problem(descriptor, user, what, rights, owners):
    """Why the self-relative security descriptor lets a principal other
    than user (a S-1-... string), the system or administrators change what,
    or None. rights are the access rights that count as changing it; owners
    are who may own it besides user."""
    try:
        _revision, _sbz, control, owner_at, _group, _sacl, dacl_at = (
            struct.unpack_from("<BBHIIII", descriptor, 0)
        )
        if not owner_at:
            return "{} has no owner the SDK can read".format(what)
        if sid_string(descriptor, owner_at) not in owners | {user}:
            return "{} belongs to another user".format(what)
        if not control & _SE_DACL_PRESENT or not dacl_at:
            return "{} lets everyone change it (it has no access control list)".format(
                what
            )
        _acl_revision, _sbz1, _size, count, _sbz2 = struct.unpack_from(
            "<BBHHH", descriptor, dacl_at
        )
        at = dacl_at + 8
        for _ in range(count):
            kind, flags, size = struct.unpack_from("<BBH", descriptor, at)
            if size < 4:
                return (
                    "the access control list of {} could not be read".format(
                        what
                    )
                )
            if not flags & _INHERIT_ONLY_ACE:
                if kind in _OTHER_ALLOW_ACES:
                    return "{} has an access control entry the SDK cannot read".format(
                        what
                    )
                if kind == _ACCESS_ALLOWED_ACE:
                    (mask,) = struct.unpack_from("<I", descriptor, at + 4)
                    principal = sid_string(descriptor, at + 8)
                    if (
                        mask & rights
                        and principal != user
                        and principal not in _TRUSTED_ENTRIES
                    ):
                        return "{} has an access control entry that lets {} change it".format(
                            what, principal
                        )
            at += size
    except (struct.error, IndexError):
        return "the security descriptor of {} could not be read".format(what)
    return None


def redirects(found) -> bool:
    """Whether found (from os.lstat) is, on Windows, a symbolic link or
    junction: a reparse point that stands for another name."""
    return bool(
        WINDOWS
        and getattr(found, "st_file_attributes", 0)
        & _FILE_ATTRIBUTE_REPARSE_POINT
        and getattr(found, "st_reparse_tag", 0) & _NAME_SURROGATE
    )


def _windows_inheritance_problem(descriptor, user, what):
    """Why the self-relative security descriptor of the folder what passes
    to new files an entry that gives anyone but user, the system or
    administrators any access, or None. CREATOR OWNER stands for whoever
    makes the file, here this user."""
    try:
        _revision, _sbz, control, _owner, _group, _sacl, dacl_at = (
            struct.unpack_from("<BBHIIII", descriptor, 0)
        )
        if not control & _SE_DACL_PRESENT or not dacl_at:
            return "{} lets everyone change it (it has no access control list)".format(
                what
            )
        _acl_revision, _sbz1, _size, count, _sbz2 = struct.unpack_from(
            "<BBHHH", descriptor, dacl_at
        )
        at = dacl_at + 8
        for _ in range(count):
            kind, flags, size = struct.unpack_from("<BBH", descriptor, at)
            if size < 4:
                return (
                    "the access control list of {} could not be read".format(
                        what
                    )
                )
            if flags & _OBJECT_INHERIT_ACE:
                if kind in _OTHER_ALLOW_ACES:
                    return "{} passes new files an access control entry the SDK cannot read".format(
                        what
                    )
                if kind == _ACCESS_ALLOWED_ACE:
                    (mask,) = struct.unpack_from("<I", descriptor, at + 4)
                    principal = sid_string(descriptor, at + 8)
                    if (
                        mask & _NEW_FILE_ACCESS
                        and principal != user
                        and principal not in _TRUSTED_ENTRIES
                    ):
                        return "{} gives {} access to every new file made in it".format(
                            what, principal
                        )
            at += size
    except (struct.error, IndexError):
        return "the security descriptor of {} could not be read".format(what)
    return None


def _windows_namespace_problem(directory):
    path = os.path.abspath(directory)
    drive, rest = os.path.splitdrive(path)
    current = drive + os.sep
    user = _windows_user()
    for part in [None] + [piece for piece in rest.split(os.sep) if piece]:
        if part is not None:
            current = os.path.join(current, part)
        if redirects(os.lstat(current)):
            return "{} is a link or junction".format(current)
        problem = _windows_problem(
            _windows_path_descriptor(current),
            user,
            current,
            _FOLDER_WRITES,
            _FOLDER_OWNERS,
        )
        if problem is not None:
            return problem
    return None


_OWNER_SECURITY_INFORMATION = 0x1
_DACL_SECURITY_INFORMATION = 0x4
_windows_user_sid: str | None = None

if sys.platform == "win32":

    def _windows_call(function, *arguments):
        """Call a Windows function that fills a security descriptor buffer,
        first to learn its size, and return the descriptor's bytes."""
        needed = ctypes.c_ulong(0)
        function(*arguments, None, 0, ctypes.byref(needed))
        if not needed.value:
            raise ctypes.WinError(ctypes.get_last_error())
        buffer = ctypes.create_string_buffer(needed.value)
        if not function(
            *arguments, buffer, needed.value, ctypes.byref(needed)
        ):
            raise ctypes.WinError(ctypes.get_last_error())
        return buffer.raw

    def _windows_path_descriptor(path):
        advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
        return _windows_call(
            advapi32.GetFileSecurityW,
            ctypes.c_wchar_p(path),
            _OWNER_SECURITY_INFORMATION | _DACL_SECURITY_INFORMATION,
        )

    def _windows_fd_descriptor(fd):
        import msvcrt

        advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
        handle = ctypes.c_void_p(msvcrt.get_osfhandle(fd))
        return _windows_call(
            advapi32.GetKernelObjectSecurity,
            handle,
            _OWNER_SECURITY_INFORMATION | _DACL_SECURITY_INFORMATION,
        )

    def _windows_user():
        """This process's user, as a S-1-... string, from its access token."""
        global _windows_user_sid
        if _windows_user_sid is None:
            advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.GetCurrentProcess.restype = ctypes.c_void_p
            advapi32.GetLengthSid.argtypes = [ctypes.c_void_p]
            token = ctypes.c_void_p()
            if not advapi32.OpenProcessToken(
                ctypes.c_void_p(kernel32.GetCurrentProcess()),
                0x0008,
                ctypes.byref(token),
            ):
                raise ctypes.WinError(ctypes.get_last_error())
            try:
                needed = ctypes.c_ulong(0)
                advapi32.GetTokenInformation(
                    token, 1, None, 0, ctypes.byref(needed)
                )
                buffer = ctypes.create_string_buffer(needed.value)
                if not advapi32.GetTokenInformation(
                    token, 1, buffer, needed.value, ctypes.byref(needed)
                ):
                    raise ctypes.WinError(ctypes.get_last_error())
                # TOKEN_USER begins with a pointer to the user's SID.
                sid = ctypes.c_void_p.from_buffer(buffer).value
                if not sid:
                    raise OSError("the process's access token names no user")
                _windows_user_sid = sid_string(
                    ctypes.string_at(sid, advapi32.GetLengthSid(sid))
                )
            finally:
                kernel32.CloseHandle(token)
        return _windows_user_sid

else:

    def _windows_path_descriptor(path):
        raise NotImplementedError(
            "Windows security descriptors are read only on Windows"
        )

    def _windows_fd_descriptor(fd):
        raise NotImplementedError(
            "Windows security descriptors are read only on Windows"
        )

    def _windows_user():
        raise NotImplementedError(
            "Windows access tokens are read only on Windows"
        )
