import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from datetime import datetime
import io
import os
from pathlib import Path
import files_sdk.path_util as path_util
from typing import BinaryIO, Callable, Iterable, NoReturn
import files_sdk.download as downloads
import files_sdk.jobs as jobs
import files_sdk.migration as migrations
import files_sdk.upload as uploads
from files_sdk.download import DownloadProgress
from files_sdk.adaptive import UploadTuning
from files_sdk.checkpoint import PauseToken
from files_sdk.jobs import TransferJobProgress, TransferResult
from files_sdk.models.file_migration import FileMigration
from files_sdk.upload import UploadProgress
from files_sdk.models.zip_list_entry import ZipListEntry
from files_sdk.models.file_action import FileAction
from files_sdk.models.file_upload_part import FileUploadPart
from files_sdk.api import (  # noqa: F401
    LEGACY,
    LegacyScope,
    Operation,
    copy_params,
    decode_record,
    path_value,
)
from files_sdk.api_client import unexpected_response_error  # noqa: F401
from files_sdk.context import RequestOptions  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class File:
    """A file record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        path: string - File/Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        created_by_id: int64 - User ID of the User who created the file/folder
        created_by_api_key_id: int64 - ID of the API key that created the file/folder
        created_by_as2_incoming_message_id: int64 - ID of the AS2 Incoming Message that created the file/folder
        created_by_automation_id: int64 - ID of the Automation that created the file/folder
        created_by_bundle_registration_id: int64 - ID of the Bundle Registration that created the file/folder
        created_by_inbox_id: int64 - ID of the Inbox that created the file/folder
        created_by_remote_server_id: int64 - ID of the Remote Server that created the file/folder
        created_by_sync_id: int64 - ID of the Sync that created the file/folder
        custom_metadata: object - Custom metadata map of keys and values. Limited to 32 keys, 256 characters per key and 1024 characters per value.
        display_name: string - File/Folder display name
        type: string - Type: `directory` or `file`.
        size: int64 - File/Folder size
        created_at: date-time - File created date/time
        last_modified_by_id: int64 - User ID of the User who last modified the file/folder
        last_modified_by_api_key_id: int64 - ID of the API key that last modified the file/folder
        last_modified_by_automation_id: int64 - ID of the Automation that last modified the file/folder
        last_modified_by_bundle_registration_id: int64 - ID of the Bundle Registration that last modified the file/folder
        last_modified_by_remote_server_id: int64 - ID of the Remote Server that last modified the file/folder
        last_modified_by_sync_id: int64 - ID of the Sync that last modified the file/folder
        mtime: date-time - File last modified date/time, according to the server. This is the timestamp of the last Files.com operation of the file, regardless of what modified timestamp was sent.
        provided_mtime: date-time - File last modified date/time, according to the client who set it. Files.com allows desktop, FTP, SFTP, and WebDAV clients to set modified at times. This allows Desktop<->Cloud syncing to preserve modified at times.
        crc32: string - File CRC32 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        md5: string - File MD5 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        sha1: string - File SHA1 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        sha256: string - File SHA256 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        mime_type: string - MIME Type. This is determined by the filename extension and is not stored separately internally.
        region: string - Region location
        permissions: string - A short string representing the current user's permissions. Can be `r` (Read),`w` (Write),`d` (Delete), `l` (List) or any combination
        subfolders_locked?: boolean - Are subfolders locked and unable to be modified?
        is_locked: boolean - Is this folder locked and unable to be modified?
        download_uri: string - Link to download file. Provided only in response to a download request.
        direct_connection_info: DirectConnectionInfo - Optional direct connection information for direct Agent transfer attempts
        priority_color: string - Bookmark/priority color of file/folder
        preview_id: int64 - File preview ID
        preview: Preview - File preview
        action: string - The action to perform. Can be `append`, `attachment`, `end`, `upload`, `put`, or may not exist
        length: int64 - Length of file.
        mkdir_parents: boolean - Create parent directories if they do not exist?
        part: int64 - Part if uploading a part.
        parts: int64 - How many parts to fetch?
        ref: string
        restart: int64 - File byte offset to restart from.
        copy_behaviors: boolean - If copying a folder, also copy supported behaviors, email notification subscriptions, and per-folder branding to the destination folder tree?
        structure: string - If copying folder, copy just the structure?
        with_rename: boolean - Allow file rename instead of overwrite?
        buffered_upload: boolean - If true, and the path refers to a destination not stored on Files.com (such as a remote server mount), the upload will be uploaded first to Files.com before being sent to the remote server mount. This can allow clients to upload using parallel parts to a remote server destination that does not offer parallel parts support natively.
        with_direct_connection_info: boolean - Include optional direct connection information for a direct Agent transfer attempt?
    """

    default_attributes = {
        "path": None,  # string - File/Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "created_by_id": None,  # int64 - User ID of the User who created the file/folder
        "created_by_api_key_id": None,  # int64 - ID of the API key that created the file/folder
        "created_by_as2_incoming_message_id": None,  # int64 - ID of the AS2 Incoming Message that created the file/folder
        "created_by_automation_id": None,  # int64 - ID of the Automation that created the file/folder
        "created_by_bundle_registration_id": None,  # int64 - ID of the Bundle Registration that created the file/folder
        "created_by_inbox_id": None,  # int64 - ID of the Inbox that created the file/folder
        "created_by_remote_server_id": None,  # int64 - ID of the Remote Server that created the file/folder
        "created_by_sync_id": None,  # int64 - ID of the Sync that created the file/folder
        "custom_metadata": None,  # object - Custom metadata map of keys and values. Limited to 32 keys, 256 characters per key and 1024 characters per value.
        "display_name": None,  # string - File/Folder display name
        "type": None,  # string - Type: `directory` or `file`.
        "size": None,  # int64 - File/Folder size
        "created_at": None,  # date-time - File created date/time
        "last_modified_by_id": None,  # int64 - User ID of the User who last modified the file/folder
        "last_modified_by_api_key_id": None,  # int64 - ID of the API key that last modified the file/folder
        "last_modified_by_automation_id": None,  # int64 - ID of the Automation that last modified the file/folder
        "last_modified_by_bundle_registration_id": None,  # int64 - ID of the Bundle Registration that last modified the file/folder
        "last_modified_by_remote_server_id": None,  # int64 - ID of the Remote Server that last modified the file/folder
        "last_modified_by_sync_id": None,  # int64 - ID of the Sync that last modified the file/folder
        "mtime": None,  # date-time - File last modified date/time, according to the server.  This is the timestamp of the last Files.com operation of the file, regardless of what modified timestamp was sent.
        "provided_mtime": None,  # date-time - File last modified date/time, according to the client who set it.  Files.com allows desktop, FTP, SFTP, and WebDAV clients to set modified at times.  This allows Desktop<->Cloud syncing to preserve modified at times.
        "crc32": None,  # string - File CRC32 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        "md5": None,  # string - File MD5 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        "sha1": None,  # string - File SHA1 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        "sha256": None,  # string - File SHA256 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        "mime_type": None,  # string - MIME Type.  This is determined by the filename extension and is not stored separately internally.
        "region": None,  # string - Region location
        "permissions": None,  # string - A short string representing the current user's permissions.  Can be `r` (Read),`w` (Write),`d` (Delete), `l` (List) or any combination
        "subfolders_locked?": None,  # boolean - Are subfolders locked and unable to be modified?
        "is_locked": None,  # boolean - Is this folder locked and unable to be modified?
        "download_uri": None,  # string - Link to download file. Provided only in response to a download request.
        "direct_connection_info": None,  # DirectConnectionInfo - Optional direct connection information for direct Agent transfer attempts
        "priority_color": None,  # string - Bookmark/priority color of file/folder
        "preview_id": None,  # int64 - File preview ID
        "preview": None,  # Preview - File preview
        "action": None,  # string - The action to perform.  Can be `append`, `attachment`, `end`, `upload`, `put`, or may not exist
        "length": None,  # int64 - Length of file.
        "mkdir_parents": None,  # boolean - Create parent directories if they do not exist?
        "part": None,  # int64 - Part if uploading a part.
        "parts": None,  # int64 - How many parts to fetch?
        "ref": None,  # string -
        "restart": None,  # int64 - File byte offset to restart from.
        "copy_behaviors": None,  # boolean - If copying a folder, also copy supported behaviors, email notification subscriptions, and per-folder branding to the destination folder tree?
        "structure": None,  # string - If copying folder, copy just the structure?
        "with_rename": None,  # boolean - Allow file rename instead of overwrite?
        "buffered_upload": None,  # boolean - If true, and the path refers to a destination not stored on Files.com (such as a remote server mount), the upload will be uploaded first to Files.com before being sent to the remote server mount. This can allow clients to upload using parallel parts to a remote server destination that does not offer parallel parts support natively.
        "with_direct_connection_info": None,  # boolean - Include optional direct connection information for a direct Agent transfer attempt?
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    path: str | None
    created_by_id: int | None
    created_by_api_key_id: int | None
    created_by_as2_incoming_message_id: int | None
    created_by_automation_id: int | None
    created_by_bundle_registration_id: int | None
    created_by_inbox_id: int | None
    created_by_remote_server_id: int | None
    created_by_sync_id: int | None
    custom_metadata: dict[str, Any] | None
    display_name: str | None
    type: str | None
    size: int | None
    created_at: str | None
    last_modified_by_id: int | None
    last_modified_by_api_key_id: int | None
    last_modified_by_automation_id: int | None
    last_modified_by_bundle_registration_id: int | None
    last_modified_by_remote_server_id: int | None
    last_modified_by_sync_id: int | None
    mtime: str | None
    provided_mtime: str | None
    crc32: str | None
    md5: str | None
    sha1: str | None
    sha256: str | None
    mime_type: str | None
    region: str | None
    permissions: str | None
    is_locked: bool | None
    download_uri: str | None
    direct_connection_info: dict[str, Any] | None
    priority_color: str | None
    preview_id: int | None
    preview: dict[str, Any] | None
    action: str | None
    length: int | None
    mkdir_parents: bool | None
    part: int | None
    parts: int | None
    ref: str | None
    restart: int | None
    copy_behaviors: bool | None
    structure: str | None
    with_rename: bool | None
    buffered_upload: bool | None
    with_direct_connection_info: bool | None

    # The client and settings this object's operations use: those of the
    # operation or client that made it, or the module's when it starts an
    # operation if neither did.
    _context: Any = None

    def __init__(self, *args):
        self.set_attributes({})
        self.options = {}
        self.mode = "r"
        self.upload = None
        self.etags = None
        self.io_obj: io.StringIO | io.BytesIO = io.StringIO()
        self.closed = True
        # The operation the file's reads and writes belong to: the one
        # open() starts, or, for a file written without open(), the one its
        # first write starts, until close().
        self._operation = None
        # The upload of what is written, from the first write until close().
        self._writer = None
        # What reads come from, from the first read until close(), and
        # whether open() opened the file.
        self._reader: Any = None
        self._opened = False

        self.bytes_written = 0
        if len(args) >= 1:
            if isinstance(args[0], dict):
                self.set_attributes(args[0])
            elif isinstance(args[0], str):
                self.set_attributes({"path": args[0]})
        if len(args) >= 2:
            if isinstance(args[1], dict):
                self.options = dict(args[1])
            elif isinstance(args[1], str):
                self.mode = args[1]
        if len(args) >= 3:
            if isinstance(args[2], dict):
                self.options = dict(args[2])

    def set_attributes(self, attributes):
        for attribute, default_value in File.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in File.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if (
            value is not None
            and self._writer is not None
            and self._writer.failure is not None
        ):
            # The upload failed already, and an exception, most often that
            # very failure, is leaving the with block: finishing would only
            # raise, in its place, that the upload failed. Nothing more is
            # sent; the file is closed.
            if not self.closed:
                self._writer.abandon()
                self._release()
            return
        # Otherwise closed as a local file is, completing the upload even
        # when the with block ends with an exception.
        self.close()

    def __del__(self):
        if self._writer is not None:
            self._writer.abandon()
        if self._reader is not None:
            self._reader.close()
        if not self.io_obj.closed:
            self.io_obj.close()

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line

    def close(self) -> None:
        """Finish with the file. For a file opened for writing, send what
        is left and complete the upload, then take the attributes of the
        File it became. Closing a closed file does nothing."""
        if self.closed:
            return
        try:
            if "w" in self.mode:
                file = self._writing().finish(
                    {"provided_mtime": datetime.now().isoformat()}
                )
                self.set_attributes(file.get_attributes())
                self._context = file._context
                self.mode = "r"
                self._writer = None
        finally:
            self._release()

    def _release(self):
        # The file's operation ends with it; later calls start their own.
        self._operation = None
        if self._reader is not None:
            self._reader.close()
            self._reader = None
        self.io_obj.close()
        self.closed = True

    def fileno(self) -> NoReturn:
        raise io.UnsupportedOperation("A remote file has no file descriptor")

    def flush(self, *_args) -> None:
        # Written data goes to Files.com a part at a time as parts fill, and
        # the last part when the file closes, so there is nothing to send
        # early: a shorter part in the middle would make the upload invalid.
        self._check_open()

    def _writing(self):
        if self._writer is None:
            if not isinstance(self.io_obj, io.BytesIO) or self.io_obj.closed:
                self.io_obj = io.BytesIO()
            self._writer = uploads.RemoteFileWriter(
                self._uploading(), self.path, "b" not in self.mode, self.io_obj
            )
        return self._writer

    def _uploading(self):
        if self._operation is None:
            operation = Operation.start(self._scope())
            operation.require_single_completion()
            self._operation = operation
        return self._operation

    def _reading(self) -> Any:
        self._check_open()
        if "r" not in self.mode:
            raise io.UnsupportedOperation(
                "The file was not opened for reading"
            )
        if self._reader is None:
            buffered = io.BufferedReader(
                downloads.RemoteReader(self._io_operation(), self)
            )
            # Text as UTF-8, with its line endings as they are.
            self._reader = (
                buffered
                if "b" in self.mode
                else io.TextIOWrapper(buffered, encoding="utf-8", newline="")
            )
        return self._reader

    def _check_open(self):
        if not self._opened:
            raise io.UnsupportedOperation(
                "Open the file with files_sdk.open() to read or write it, or "
                "use download_file() or download_content()"
            )
        if self.closed:
            # Both the ValueError io raises and the OSError version 1 did.
            raise io.UnsupportedOperation("I/O operation on closed file.")

    def isatty(self) -> bool:
        return False

    # Reads return str in text mode and bytes in binary mode, as the mode
    # given to open() says, so they are declared Any.
    def read(self, size: int | None = -1) -> Any:
        """Read up to size bytes (or characters, in text mode), or, by
        default, the rest of the file. Returns an empty value at the end."""
        return self._reading().read(size)

    def readable(self) -> bool:
        return "r" in self.mode and not self.closed

    def readall(self) -> Any:
        """The rest of the file."""
        return self._reading().read()

    def readinto(self, buffer: Any) -> int:
        """Read into buffer, a writable bytes-like object, in binary mode.
        Returns the number of bytes read, 0 at the end."""
        reader = self._reading()
        if not isinstance(reader, io.BufferedReader):
            raise io.UnsupportedOperation(
                "readinto() needs a file opened in binary mode"
            )
        return reader.readinto(buffer)

    def readline(self, size: int = -1) -> Any:
        """The next line, with its line ending, or an empty value at the
        end."""
        return self._reading().readline(size)

    def readlines(self, hint: int = -1) -> list[Any]:
        return self._reading().readlines(hint)

    def seek(self, *_args) -> NoReturn:
        raise io.UnsupportedOperation("A remote file cannot seek")

    def seekable(self) -> bool:
        return False

    def tell(self) -> NoReturn:
        raise io.UnsupportedOperation("A remote file has no position to tell")

    def truncate(self, *_args) -> NoReturn:
        raise io.UnsupportedOperation("A remote file cannot be truncated")

    def writable(self) -> bool:
        return "w" in self.mode and not self.closed

    def writeable(self) -> bool:
        """The same as writable(), as version 1 spelled it."""
        return self.writable()

    def write(self, data: Any) -> int:
        """Write data, bytes in binary mode or str in text mode, which is
        sent as UTF-8. Returns how many bytes (or characters) it took."""
        self._check_open()
        if not self.writable():
            raise io.UnsupportedOperation(
                "The file was not opened for writing"
            )
        return self._writing().write(data)

    def writelines(self, lines: Iterable[Any]) -> None:
        for line in lines:
            self.write(line)

    def _io_operation(self):
        # The operation open() started, until close(), for the file's
        # reads and downloads; otherwise each starts its own. Other model
        # actions, such as delete or copy, always start their own.
        return self._operation or Operation.start(self._scope())

    def download_uri_with_load(self) -> str | None:
        return self._download_uri(self._io_operation())

    def _download_uri(self, operation):
        if self.download_uri:
            return self.download_uri

        # The path as set, whatever its type: the operation checks it.
        f = FileResource(operation).download(getattr(self, "path"), {})
        self.set_attributes(f.get_attributes())
        return self.download_uri

    def download_content(self, io: Any, is_string_io: bool = False) -> None:
        """Write the file's content to io, a writable stream left open,
        as text if is_string_io. One operation finds the download URL, if
        the file does not have one yet, and downloads it."""
        downloads.download_stream(
            self._io_operation(), self, io, text=is_string_io
        )

    def download_file(self, output_file: str | Path) -> "File":
        """Download the file to the local path output_file, which is
        replaced only once the whole file has arrived."""
        return self._download_file(output_file, self._io_operation())

    def _download_file(self, output_file, operation, **options):
        return downloads.download_path(operation, self, output_file, **options)

    def copy_to_remote_server(
        self,
        remote_server_id: int,
        destination: str,
        params: dict[str, Any] | None = None,
    ) -> FileAction:
        return FileResource(self._scope()).copy_to_remote_server(
            getattr(self, "path"), remote_server_id, destination, params
        )

    def move_to_remote_server(
        self,
        remote_server_id: int,
        destination: str,
        params: dict[str, Any] | None = None,
    ) -> FileAction:
        return FileResource(self._scope()).move_to_remote_server(
            getattr(self, "path"), remote_server_id, destination, params
        )

    def copy_to_snapshot(
        self,
        snapshot_id: int,
        destination: str,
        params: dict[str, Any] | None = None,
    ) -> FileAction:
        return FileResource(self._scope()).copy_to_snapshot(
            getattr(self, "path"), snapshot_id, destination, params
        )

    def move_to_snapshot(
        self,
        snapshot_id: int,
        destination: str,
        params: dict[str, Any] | None = None,
    ) -> FileAction:
        return FileResource(self._scope()).move_to_snapshot(
            getattr(self, "path"), snapshot_id, destination, params
        )

    def copy_to_child_site(
        self,
        site_id: int,
        destination: str,
        params: dict[str, Any] | None = None,
    ) -> FileAction:
        return FileResource(self._scope()).copy_to_child_site(
            getattr(self, "path"), site_id, destination, params
        )

    def move_to_child_site(
        self,
        site_id: int,
        destination: str,
        params: dict[str, Any] | None = None,
    ) -> FileAction:
        return FileResource(self._scope()).move_to_child_site(
            getattr(self, "path"), site_id, destination, params
        )

    def download(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Download File

        Parameters:
          action - string - Can be blank, `redirect` or `stat`.  If set to `stat`, we will return file information but without a download URL, and without logging a download.  If set to `redirect` we will serve a 302 redirect directly to the file.  This is used for integrations with Zapier, and is not recommended for most integrations.
          preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
          with_previews - boolean - Include file preview information?
          with_priority_color - boolean - Include file priority color information?
          with_direct_connection_info - boolean - Include optional direct connection information for a direct Agent transfer attempt?
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "preview_size" in params and not isinstance(
            params["preview_size"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: preview_size must be an str"
            )
        if "with_previews" in params and isinstance(
            params["with_previews"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: with_previews must be an bool"
            )
        if "with_priority_color" in params and isinstance(
            params["with_priority_color"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: with_priority_color must be an bool"
            )
        if "with_direct_connection_info" in params and isinstance(
            params["with_direct_connection_info"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: with_direct_connection_info must be an bool"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "GET", "/files/" + path_value(params["path"]), params
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          custom_metadata - object - Custom metadata map of keys and values. Limited to 32 keys, 256 characters per key and 1024 characters per value.
          provided_mtime - string - Modified time of file.
          priority_color - string - Priority/Bookmark color of file.
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "provided_mtime" in params and not isinstance(
            params["provided_mtime"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provided_mtime must be an str"
            )
        if "priority_color" in params and not isinstance(
            params["priority_color"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: priority_color must be an str"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/files/" + path_value(params["path"]), params
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        """Parameters:
        recursive - boolean - If true, will recursively delete folders.  Otherwise, will error on non-empty folders.
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "recursive" in params and isinstance(
            params["recursive"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: recursive must be an bool"
            )
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE", "/files/" + path_value(params["path"]), params
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def zip_list_contents(
        self, params: dict[str, Any] | None = None
    ) -> builtins.list[Any]:
        """List the contents of a ZIP file"""
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        operation = Operation.start(self._scope())
        response = operation.request(
            "GET",
            "/file_actions/zip_list/" + path_value(params["path"]),
            params,
        )
        if not isinstance(response.data, builtins.list):
            raise unexpected_response_error(
                response, "a list was not a JSON array"
            )
        return response.data

    def begin_delete(
        self, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Delete File/Folder and return its File Action.  A pending or processing deletion continues in the background after this returns; check its File Migration for completion.  Waiting for the File Migration does not cancel the deletion

        Parameters:
          recursive - boolean - If true, will recursively delete folders.  Otherwise, will error on non-empty folders.
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "recursive" in params and isinstance(
            params["recursive"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: recursive must be an bool"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "POST",
            "/file_actions/delete/" + path_value(params["path"]),
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def copy(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Copy File/Folder

        Parameters:
          destination (required) - string - Copy destination path.
          copy_behaviors - boolean - If copying a folder, also copy supported behaviors, email notification subscriptions, and per-folder branding to the destination folder tree?
          structure - boolean - Copy structure only?
          overwrite - boolean - Overwrite existing file(s) in the destination?
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "copy_behaviors" in params and isinstance(
            params["copy_behaviors"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: copy_behaviors must be an bool"
            )
        if "structure" in params and isinstance(
            params["structure"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: structure must be an bool"
            )
        if "overwrite" in params and isinstance(
            params["overwrite"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "POST", "/file_actions/copy/" + path_value(params["path"]), params
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def move(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Move File/Folder

        Parameters:
          destination (required) - string - Move destination path.
          overwrite - boolean - Overwrite existing file(s) in the destination?
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "overwrite" in params and isinstance(
            params["overwrite"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "POST", "/file_actions/move/" + path_value(params["path"]), params
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def transform(
        self, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Transform a file and save the output to a destination path

        Parameters:
          destination (required) - string - Destination file path for the transformed output.
          transform_type (required) - string - Transform type. Supported values are `image_convert`, `document_convert`, and `files_transform_script_execute`.
          target_format (required) - string - Destination format to create.
          script - string - Files TransformScript source. Required when transform_type is `files_transform_script_execute`.
          width - int64 - Maximum output width for image_convert.
          height - int64 - Maximum output height for image_convert.
          overwrite - boolean - Overwrite existing file in the destination?
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        if "transform_type" not in params:
            raise MissingParameterError("Parameter missing: transform_type")
        if "target_format" not in params:
            raise MissingParameterError("Parameter missing: target_format")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "transform_type" in params and not isinstance(
            params["transform_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: transform_type must be an str"
            )
        if "target_format" in params and not isinstance(
            params["target_format"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: target_format must be an str"
            )
        if "script" in params and not isinstance(params["script"], str):
            raise InvalidParameterError("Bad parameter: script must be an str")
        if "width" in params and (
            not isinstance(params["width"], int)
            or isinstance(params["width"], bool)
        ):
            raise InvalidParameterError("Bad parameter: width must be an int")
        if "height" in params and (
            not isinstance(params["height"], int)
            or isinstance(params["height"], bool)
        ):
            raise InvalidParameterError("Bad parameter: height must be an int")
        if "overwrite" in params and isinstance(
            params["overwrite"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "POST",
            "/file_actions/transform/" + path_value(params["path"]),
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def gpg_decrypt(
        self, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Decrypt a GPG-encrypted file and save it to a destination path

        Parameters:
          destination (required) - string - Destination file path for the decrypted file.
          gpg_key_ids - array(int64) - GPG Key IDs to decrypt with. If omitted, every accessible private GPG key in the source workspace is used.
          gpg_key_partner_id - int64 - Partner ID whose GPG keys should be used for decryption.
          use_all_private_keys - boolean - Use every accessible private GPG key in the source workspace for decryption.
          ignore_mdc_error - boolean - Ignore errors from the MDC (modification detection code) check.
          overwrite - boolean - Overwrite existing file in the destination?
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "gpg_key_ids" in params and not isinstance(
            params["gpg_key_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: gpg_key_ids must be an list"
            )
        if "gpg_key_partner_id" in params and (
            not isinstance(params["gpg_key_partner_id"], int)
            or isinstance(params["gpg_key_partner_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: gpg_key_partner_id must be an int"
            )
        if "use_all_private_keys" in params and isinstance(
            params["use_all_private_keys"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: use_all_private_keys must be an bool"
            )
        if "ignore_mdc_error" in params and isinstance(
            params["ignore_mdc_error"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: ignore_mdc_error must be an bool"
            )
        if "overwrite" in params and isinstance(
            params["overwrite"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "POST",
            "/file_actions/gpg_decrypt/" + path_value(params["path"]),
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def gpg_encrypt(
        self, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Encrypt a file with GPG and save it to a destination path

        Parameters:
          destination (required) - string - Destination file path for the encrypted file.
          gpg_key_ids - array(int64) - GPG Key IDs to encrypt with.
          gpg_key_partner_id - int64 - Partner ID whose GPG keys should be used for encryption.
          signing_key_id - int64 - Optional GPG Key ID to sign with.
          armor - boolean - Output ASCII-armored encrypted data.
          overwrite - boolean - Overwrite existing file in the destination?
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "gpg_key_ids" in params and not isinstance(
            params["gpg_key_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: gpg_key_ids must be an list"
            )
        if "gpg_key_partner_id" in params and (
            not isinstance(params["gpg_key_partner_id"], int)
            or isinstance(params["gpg_key_partner_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: gpg_key_partner_id must be an int"
            )
        if "signing_key_id" in params and (
            not isinstance(params["signing_key_id"], int)
            or isinstance(params["signing_key_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: signing_key_id must be an int"
            )
        if "armor" in params and isinstance(
            params["armor"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError("Bad parameter: armor must be an bool")
        if "overwrite" in params and isinstance(
            params["overwrite"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "POST",
            "/file_actions/gpg_encrypt/" + path_value(params["path"]),
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def unzip(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Extract a ZIP file to a destination folder

        Parameters:
          destination (required) - string - Destination folder path for extracted files.
          filename - string - Optional single entry filename to extract.
          overwrite - boolean - Overwrite existing files in the destination?
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "filename" in params and not isinstance(params["filename"], str):
            raise InvalidParameterError(
                "Bad parameter: filename must be an str"
            )
        if "overwrite" in params and isinstance(
            params["overwrite"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        operation = Operation.start(self._scope())
        response = operation.request("POST", "/file_actions/unzip", params)
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def begin_upload(
        self, params: dict[str, Any] | None = None
    ) -> builtins.list[Any]:
        """Begin File Upload

        Parameters:
          mkdir_parents - boolean - Create parent directories if they do not exist?
          part - int64 - Part if uploading a part.
          parts - int64 - How many parts to fetch?
          ref - string -
          restart - int64 - File byte offset to restart from.
          size - int64 - Total bytes of file being uploaded (include bytes being retained if appending/restarting).
          with_rename - boolean - Allow file rename instead of overwrite?
          buffered_upload - boolean - If true, and the path refers to a destination not stored on Files.com (such as a remote server mount), the upload will be uploaded first to Files.com before being sent to the remote server mount. This can allow clients to upload using parallel parts to a remote server destination that does not offer parallel parts support natively.
          with_direct_connection_info - boolean - Include optional direct connection information for a direct Agent transfer attempt?
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "mkdir_parents" in params and isinstance(
            params["mkdir_parents"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: mkdir_parents must be an bool"
            )
        if "part" in params and (
            not isinstance(params["part"], int)
            or isinstance(params["part"], bool)
        ):
            raise InvalidParameterError("Bad parameter: part must be an int")
        if "parts" in params and (
            not isinstance(params["parts"], int)
            or isinstance(params["parts"], bool)
        ):
            raise InvalidParameterError("Bad parameter: parts must be an int")
        if "ref" in params and not isinstance(params["ref"], str):
            raise InvalidParameterError("Bad parameter: ref must be an str")
        if "restart" in params and (
            not isinstance(params["restart"], int)
            or isinstance(params["restart"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: restart must be an int"
            )
        if "size" in params and (
            not isinstance(params["size"], int)
            or isinstance(params["size"], bool)
        ):
            raise InvalidParameterError("Bad parameter: size must be an int")
        if "with_rename" in params and isinstance(
            params["with_rename"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: with_rename must be an bool"
            )
        if "buffered_upload" in params and isinstance(
            params["buffered_upload"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: buffered_upload must be an bool"
            )
        if "with_direct_connection_info" in params and isinstance(
            params["with_direct_connection_info"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: with_direct_connection_info must be an bool"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "POST",
            "/file_actions/begin_upload/" + path_value(params["path"]),
            params,
        )
        if not isinstance(response.data, builtins.list):
            raise unexpected_response_error(
                response, "a list was not a JSON array"
            )
        return response.data

    def save(self) -> None:
        """Create this object on the server, taking in place the record it
        returns."""
        new_obj = FileResource(self._scope()).create(
            getattr(self, "path"), self.get_attributes()
        )
        self.set_attributes(new_obj.get_attributes())
        self._context = new_obj._context


class FileResource:
    """File operations that use one client's configuration.

    Get one from a client, such as ``client.file``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def download(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> File:
        """Download File

        Parameters:
          action - string - Can be blank, `redirect` or `stat`.  If set to `stat`, we will return file information but without a download URL, and without logging a download.  If set to `redirect` we will serve a 302 redirect directly to the file.  This is used for integrations with Zapier, and is not recommended for most integrations.
          preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
          with_previews - boolean - Include file preview information?
          with_priority_color - boolean - Include file priority color information?
          with_direct_connection_info - boolean - Include optional direct connection information for a direct Agent transfer attempt?
        """
        return self.__download({"path": path}, params, options)

    def __download(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> File:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "preview_size" in params and not isinstance(
            params["preview_size"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: preview_size must be an str"
            )
        if "with_previews" in params and not isinstance(
            params["with_previews"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: with_previews must be an bool"
            )
        if "with_priority_color" in params and not isinstance(
            params["with_priority_color"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: with_priority_color must be an bool"
            )
        if "with_direct_connection_info" in params and not isinstance(
            params["with_direct_connection_info"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: with_direct_connection_info must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/files/" + path_value(params["path"]), params
        )
        return operation.decode_model(response, File)

    def create(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> File:
        """Parameters:
        path (required) - string - Path to operate on.
        action - string - The action to perform.  Can be `append`, `attachment`, `end`, `upload`, `put`, or may not exist
        custom_metadata - object - Custom metadata map to save when `action=end` completes the upload.  Replaces existing metadata; an empty map clears it.  No separate metadata-edit permission is required.  Supported on native files and configured remote mounts, excluding remote server automount paths.  Limited to 32 keys, 256 characters per key and 1024 characters per value.
        etags[etag] (required) - array(string) - etag identifier.
        etags[part] (required) - array(int64) - Part number.
        length - int64 - Length of file.
        mkdir_parents - boolean - Create parent directories if they do not exist?
        part - int64 - Part if uploading a part.
        parts - int64 - How many parts to fetch?
        provided_mtime - string - User provided modification time.
        ref - string -
        restart - int64 - File byte offset to restart from.
        size - int64 - Size of file.
        copy_behaviors - boolean - If copying a folder, also copy supported behaviors, email notification subscriptions, and per-folder branding to the destination folder tree?
        structure - string - If copying folder, copy just the structure?
        with_rename - boolean - Allow file rename instead of overwrite?
        buffered_upload - boolean - If true, and the path refers to a destination not stored on Files.com (such as a remote server mount), the upload will be uploaded first to Files.com before being sent to the remote server mount. This can allow clients to upload using parallel parts to a remote server destination that does not offer parallel parts support natively.
        with_direct_connection_info - boolean - Include optional direct connection information for a direct Agent transfer attempt?
        """
        return self.__create({"path": path}, params, options)

    def __create(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> File:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "custom_metadata" in params and not isinstance(
            params["custom_metadata"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: custom_metadata must be an dict"
            )
        if "length" in params and (
            not isinstance(params["length"], int)
            or isinstance(params["length"], bool)
        ):
            raise InvalidParameterError("Bad parameter: length must be an int")
        if "mkdir_parents" in params and not isinstance(
            params["mkdir_parents"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: mkdir_parents must be an bool"
            )
        if "part" in params and (
            not isinstance(params["part"], int)
            or isinstance(params["part"], bool)
        ):
            raise InvalidParameterError("Bad parameter: part must be an int")
        if "parts" in params and (
            not isinstance(params["parts"], int)
            or isinstance(params["parts"], bool)
        ):
            raise InvalidParameterError("Bad parameter: parts must be an int")
        if "provided_mtime" in params and not isinstance(
            params["provided_mtime"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provided_mtime must be an str"
            )
        if "ref" in params and not isinstance(params["ref"], str):
            raise InvalidParameterError("Bad parameter: ref must be an str")
        if "restart" in params and (
            not isinstance(params["restart"], int)
            or isinstance(params["restart"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: restart must be an int"
            )
        if "size" in params and (
            not isinstance(params["size"], int)
            or isinstance(params["size"], bool)
        ):
            raise InvalidParameterError("Bad parameter: size must be an int")
        if "copy_behaviors" in params and not isinstance(
            params["copy_behaviors"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: copy_behaviors must be an bool"
            )
        if "structure" in params and not isinstance(params["structure"], str):
            raise InvalidParameterError(
                "Bad parameter: structure must be an str"
            )
        if "with_rename" in params and not isinstance(
            params["with_rename"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: with_rename must be an bool"
            )
        if "buffered_upload" in params and not isinstance(
            params["buffered_upload"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: buffered_upload must be an bool"
            )
        if "with_direct_connection_info" in params and not isinstance(
            params["with_direct_connection_info"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: with_direct_connection_info must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST", "/files/" + path_value(params["path"]), params
        )
        return operation.decode_model(response, File)

    def update(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> File:
        """Parameters:
        custom_metadata - object - Custom metadata map of keys and values. Limited to 32 keys, 256 characters per key and 1024 characters per value.
        provided_mtime - string - Modified time of file.
        priority_color - string - Priority/Bookmark color of file.
        """
        return self.__update({"path": path}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> File:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "custom_metadata" in params and not isinstance(
            params["custom_metadata"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: custom_metadata must be an dict"
            )
        if "provided_mtime" in params and not isinstance(
            params["provided_mtime"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provided_mtime must be an str"
            )
        if "priority_color" in params and not isinstance(
            params["priority_color"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: priority_color must be an str"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/files/" + path_value(params["path"]), params
        )
        return operation.decode_model(response, File)

    def delete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Parameters:
        recursive - boolean - If true, will recursively delete folders.  Otherwise, will error on non-empty folders.
        """
        return self.__delete({"path": path}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "recursive" in params and not isinstance(params["recursive"], bool):
            raise InvalidParameterError(
                "Bad parameter: recursive must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE", "/files/" + path_value(params["path"]), params
        )

    def destroy(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(path, params, options)

    def find(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> File:
        """Parameters:
        path (required) - string - Path to operate on.
        preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
        with_previews - boolean - Include file preview information?
        with_priority_color - boolean - Include file priority color information?
        """
        return self.__find({"path": path}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> File:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "preview_size" in params and not isinstance(
            params["preview_size"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: preview_size must be an str"
            )
        if "with_previews" in params and not isinstance(
            params["with_previews"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: with_previews must be an bool"
            )
        if "with_priority_color" in params and not isinstance(
            params["with_priority_color"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: with_priority_color must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET",
            "/file_actions/metadata/" + path_value(params["path"]),
            params,
        )
        return operation.decode_model(response, File)

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> File:
        """The same as find()."""
        return self.find(path, params, options)

    def zip_list_contents(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> builtins.list[ZipListEntry]:
        """List the contents of a ZIP file"""
        return self.__zip_list_contents({"path": path}, params, options)

    def __zip_list_contents(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> builtins.list[ZipListEntry]:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET",
            "/file_actions/zip_list/" + path_value(params["path"]),
            params,
        )
        return operation.decode_models(response, ZipListEntry)

    def begin_delete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Delete File/Folder and return its File Action.  A pending or processing deletion continues in the background after this returns; check its File Migration for completion.  Waiting for the File Migration does not cancel the deletion

        Parameters:
          recursive - boolean - If true, will recursively delete folders.  Otherwise, will error on non-empty folders.
        """
        return self.__begin_delete({"path": path}, params, options)

    def __begin_delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> FileAction:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "recursive" in params and not isinstance(params["recursive"], bool):
            raise InvalidParameterError(
                "Bad parameter: recursive must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/file_actions/delete/" + path_value(params["path"]),
            params,
        )
        return operation.decode_model(response, FileAction)

    def copy(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Copy File/Folder

        Parameters:
          destination (required) - string - Copy destination path.
          copy_behaviors - boolean - If copying a folder, also copy supported behaviors, email notification subscriptions, and per-folder branding to the destination folder tree?
          structure - boolean - Copy structure only?
          overwrite - boolean - Overwrite existing file(s) in the destination?
        """
        return self.__copy({"path": path}, params, options)

    def __copy(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> FileAction:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "copy_behaviors" in params and not isinstance(
            params["copy_behaviors"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: copy_behaviors must be an bool"
            )
        if "structure" in params and not isinstance(params["structure"], bool):
            raise InvalidParameterError(
                "Bad parameter: structure must be an bool"
            )
        if "overwrite" in params and not isinstance(params["overwrite"], bool):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST", "/file_actions/copy/" + path_value(params["path"]), params
        )
        return operation.decode_model(response, FileAction)

    def move(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Move File/Folder

        Parameters:
          destination (required) - string - Move destination path.
          overwrite - boolean - Overwrite existing file(s) in the destination?
        """
        return self.__move({"path": path}, params, options)

    def __move(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> FileAction:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "overwrite" in params and not isinstance(params["overwrite"], bool):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST", "/file_actions/move/" + path_value(params["path"]), params
        )
        return operation.decode_model(response, FileAction)

    def transform(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Transform a file and save the output to a destination path

        Parameters:
          destination (required) - string - Destination file path for the transformed output.
          transform_type (required) - string - Transform type. Supported values are `image_convert`, `document_convert`, and `files_transform_script_execute`.
          target_format (required) - string - Destination format to create.
          script - string - Files TransformScript source. Required when transform_type is `files_transform_script_execute`.
          width - int64 - Maximum output width for image_convert.
          height - int64 - Maximum output height for image_convert.
          overwrite - boolean - Overwrite existing file in the destination?
        """
        return self.__transform({"path": path}, params, options)

    def __transform(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> FileAction:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "transform_type" in params and not isinstance(
            params["transform_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: transform_type must be an str"
            )
        if "target_format" in params and not isinstance(
            params["target_format"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: target_format must be an str"
            )
        if "script" in params and not isinstance(params["script"], str):
            raise InvalidParameterError("Bad parameter: script must be an str")
        if "width" in params and (
            not isinstance(params["width"], int)
            or isinstance(params["width"], bool)
        ):
            raise InvalidParameterError("Bad parameter: width must be an int")
        if "height" in params and (
            not isinstance(params["height"], int)
            or isinstance(params["height"], bool)
        ):
            raise InvalidParameterError("Bad parameter: height must be an int")
        if "overwrite" in params and not isinstance(params["overwrite"], bool):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        if "transform_type" not in params:
            raise MissingParameterError("Parameter missing: transform_type")
        if "target_format" not in params:
            raise MissingParameterError("Parameter missing: target_format")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/file_actions/transform/" + path_value(params["path"]),
            params,
        )
        return operation.decode_model(response, FileAction)

    def gpg_decrypt(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Decrypt a GPG-encrypted file and save it to a destination path

        Parameters:
          destination (required) - string - Destination file path for the decrypted file.
          gpg_key_ids - array(int64) - GPG Key IDs to decrypt with. If omitted, every accessible private GPG key in the source workspace is used.
          gpg_key_partner_id - int64 - Partner ID whose GPG keys should be used for decryption.
          use_all_private_keys - boolean - Use every accessible private GPG key in the source workspace for decryption.
          ignore_mdc_error - boolean - Ignore errors from the MDC (modification detection code) check.
          overwrite - boolean - Overwrite existing file in the destination?
        """
        return self.__gpg_decrypt({"path": path}, params, options)

    def __gpg_decrypt(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> FileAction:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "gpg_key_ids" in params and not isinstance(
            params["gpg_key_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: gpg_key_ids must be an list"
            )
        if "gpg_key_partner_id" in params and (
            not isinstance(params["gpg_key_partner_id"], int)
            or isinstance(params["gpg_key_partner_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: gpg_key_partner_id must be an int"
            )
        if "use_all_private_keys" in params and not isinstance(
            params["use_all_private_keys"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: use_all_private_keys must be an bool"
            )
        if "ignore_mdc_error" in params and not isinstance(
            params["ignore_mdc_error"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: ignore_mdc_error must be an bool"
            )
        if "overwrite" in params and not isinstance(params["overwrite"], bool):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/file_actions/gpg_decrypt/" + path_value(params["path"]),
            params,
        )
        return operation.decode_model(response, FileAction)

    def gpg_encrypt(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Encrypt a file with GPG and save it to a destination path

        Parameters:
          destination (required) - string - Destination file path for the encrypted file.
          gpg_key_ids - array(int64) - GPG Key IDs to encrypt with.
          gpg_key_partner_id - int64 - Partner ID whose GPG keys should be used for encryption.
          signing_key_id - int64 - Optional GPG Key ID to sign with.
          armor - boolean - Output ASCII-armored encrypted data.
          overwrite - boolean - Overwrite existing file in the destination?
        """
        return self.__gpg_encrypt({"path": path}, params, options)

    def __gpg_encrypt(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> FileAction:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "gpg_key_ids" in params and not isinstance(
            params["gpg_key_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: gpg_key_ids must be an list"
            )
        if "gpg_key_partner_id" in params and (
            not isinstance(params["gpg_key_partner_id"], int)
            or isinstance(params["gpg_key_partner_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: gpg_key_partner_id must be an int"
            )
        if "signing_key_id" in params and (
            not isinstance(params["signing_key_id"], int)
            or isinstance(params["signing_key_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: signing_key_id must be an int"
            )
        if "armor" in params and not isinstance(params["armor"], bool):
            raise InvalidParameterError("Bad parameter: armor must be an bool")
        if "overwrite" in params and not isinstance(params["overwrite"], bool):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/file_actions/gpg_encrypt/" + path_value(params["path"]),
            params,
        )
        return operation.decode_model(response, FileAction)

    def unzip(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Extract a ZIP file to a destination folder

        Parameters:
          destination (required) - string - Destination folder path for extracted files.
          filename - string - Optional single entry filename to extract.
          overwrite - boolean - Overwrite existing files in the destination?
        """
        return self.__unzip({"path": path}, params, options)

    def __unzip(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> FileAction:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "filename" in params and not isinstance(params["filename"], str):
            raise InvalidParameterError(
                "Bad parameter: filename must be an str"
            )
        if "overwrite" in params and not isinstance(params["overwrite"], bool):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/file_actions/unzip", params)
        return operation.decode_model(response, FileAction)

    def zip(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Parameters:
        paths (required) - array(string) - Paths to include in the ZIP.
        destination (required) - string - Destination file path for the ZIP.
        overwrite - boolean - Overwrite existing file in the destination?
        """
        params = copy_params(params)
        if "paths" in params and not isinstance(
            params["paths"], builtins.list
        ):
            raise InvalidParameterError("Bad parameter: paths must be an list")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "overwrite" in params and not isinstance(params["overwrite"], bool):
            raise InvalidParameterError(
                "Bad parameter: overwrite must be an bool"
            )
        if "paths" not in params:
            raise MissingParameterError("Parameter missing: paths")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/file_actions/zip", params)
        return operation.decode_model(response, FileAction)

    def begin_upload(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> builtins.list[FileUploadPart]:
        """Begin File Upload

        Parameters:
          mkdir_parents - boolean - Create parent directories if they do not exist?
          part - int64 - Part if uploading a part.
          parts - int64 - How many parts to fetch?
          ref - string -
          restart - int64 - File byte offset to restart from.
          size - int64 - Total bytes of file being uploaded (include bytes being retained if appending/restarting).
          with_rename - boolean - Allow file rename instead of overwrite?
          buffered_upload - boolean - If true, and the path refers to a destination not stored on Files.com (such as a remote server mount), the upload will be uploaded first to Files.com before being sent to the remote server mount. This can allow clients to upload using parallel parts to a remote server destination that does not offer parallel parts support natively.
          with_direct_connection_info - boolean - Include optional direct connection information for a direct Agent transfer attempt?
        """
        return self.__begin_upload({"path": path}, params, options)

    def __begin_upload(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> builtins.list[FileUploadPart]:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "mkdir_parents" in params and not isinstance(
            params["mkdir_parents"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: mkdir_parents must be an bool"
            )
        if "part" in params and (
            not isinstance(params["part"], int)
            or isinstance(params["part"], bool)
        ):
            raise InvalidParameterError("Bad parameter: part must be an int")
        if "parts" in params and (
            not isinstance(params["parts"], int)
            or isinstance(params["parts"], bool)
        ):
            raise InvalidParameterError("Bad parameter: parts must be an int")
        if "ref" in params and not isinstance(params["ref"], str):
            raise InvalidParameterError("Bad parameter: ref must be an str")
        if "restart" in params and (
            not isinstance(params["restart"], int)
            or isinstance(params["restart"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: restart must be an int"
            )
        if "size" in params and (
            not isinstance(params["size"], int)
            or isinstance(params["size"], bool)
        ):
            raise InvalidParameterError("Bad parameter: size must be an int")
        if "with_rename" in params and not isinstance(
            params["with_rename"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: with_rename must be an bool"
            )
        if "buffered_upload" in params and not isinstance(
            params["buffered_upload"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: buffered_upload must be an bool"
            )
        if "with_direct_connection_info" in params and not isinstance(
            params["with_direct_connection_info"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: with_direct_connection_info must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/file_actions/begin_upload/" + path_value(params["path"]),
            params,
        )
        return operation.decode_models(response, FileUploadPart)

    def open(
        self,
        path: str,
        mode: str = "r",
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> File:
        """A File for reading or writing path, like the built-in open(),
        with mode "r" or "w", and "b" for bytes (text is UTF-8).

        Reading streams the file a range at a time as reads need it, so
        the SDK holds at most a few MiB of it; the file cannot seek, and
        one that changes while it is read raises InvalidRequestError. Once
        a read fetches the remote file, size is the file's size in bytes as the
        storage service's answer states it (its Content-Length, or the
        version's size for ranges), or None if that answer states none the
        SDK can trust, such as an encoded one; not the size Files.com's
        record of the file states.
        Writing sends what is written a part at a time, and the rest when
        the file closes, which completes the upload. seek(), tell(),
        truncate() and fileno() raise io.UnsupportedOperation, as open()
        does for modes "a", "x" and "+". Reads, writes and close() are one
        operation, with the token and deadline options give."""
        text_mode = _checked_mode(mode)
        operation = Operation.start(self._scope, options)
        operation.lifetime.check("open")
        if "w" in mode:
            operation.require_single_completion()
        file = operation.adopt(File(path, mode, options))
        file._operation = operation
        file._opened = True
        if "w" in mode:
            # Holds what is written until it is sent, text as UTF-8.
            file.io_obj = io.BytesIO()
        else:
            file.io_obj = io.StringIO() if text_mode else io.BytesIO()
        file.closed = False
        return file

    def upload_chunks(self, io, path, upload=None, etags=None, params=None):
        """Upload io to path from where it is to its end, in the parts the
        API asks for, one at a time, continuing upload (the FileUploadPart
        an earlier call returned) if given, without completing the upload.
        Returns the last part sent, the ETags of the parts, and the bytes
        sent. Continue an upload with the part object the earlier call
        returned: it knows where the upload got to, which an upload that
        sends part offsets needs. Most callers want upload_stream or
        upload_file instead."""
        return uploads.upload_parts(
            Operation.start(self._scope), path, io, upload, etags, params
        )

    def upload_file(
        self,
        path: str | Path,
        destination: str | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        *,
        max_concurrency: int | None = None,
        progress: Callable[[UploadProgress], None] | None = None,
        tuning: UploadTuning | None = None,
        checkpoint: str | Path | None = None,
        pause_token: PauseToken | None = None,
    ) -> File:
        """Upload the local file at path to destination, by default its
        name in the root folder, and return the File it becomes.

        When Files.com allows it, several parts are sent at once, each read
        with its own handle; otherwise parts go one at a time. How many
        adapts to how the upload is going, up to max_concurrency; tuning
        (an UploadTuning) changes how, or turns adapting off. progress, if
        given, is called on this thread with an UploadProgress as parts
        arrive. The file must not change while it uploads. The SDK checks
        it as it reads it and before completing the upload, by its size,
        times and identity and, on Windows, by Windows' notice of a write
        to a file on a local disk where Windows gives one, and a change it
        finds fails the upload instead of completing it; but no check finds
        every change. One
        operation covers every request of the upload, and the client's
        transfer_limiter bounds its parts in progress. params can set
        mkdir_parents, with_rename, buffered_upload, custom_metadata and
        provided_mtime (the file's own modification time by default).

        checkpoint, a local path, keeps what the upload has done so far, so
        that calling upload_file again with it resumes the upload if it
        stopped, while the file's size, times and identity are as they were,
        which cannot prove its bytes are; an upload that found the file
        changed keeps nothing to resume. pause_token (a PauseToken) pauses
        it, raising TransferPausedError once its parts in progress have
        finished."""
        operation = Operation.start(self._scope, options)
        operation.require_single_completion()
        if destination is None:
            destination = Path(path).name
        return uploads.upload_path(
            operation,
            destination,
            path,
            params,
            max_concurrency=max_concurrency,
            progress=progress,
            tuning=tuning,
            checkpoint=checkpoint,
            pause_token=pause_token,
        )

    def upload_stream(
        self,
        stream: BinaryIO,
        destination: str,
        size: int | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        *,
        max_concurrency: int | None = None,
        progress: Callable[[UploadProgress], None] | None = None,
        tuning: UploadTuning | None = None,
        spool_limit: int | None = None,
        spool_directory: str | Path | None = None,
        checkpoint: str | Path | None = None,
        pause_token: PauseToken | None = None,
    ) -> File:
        """Upload a binary stream, read from where it is now, to
        destination, and return the File it becomes: exactly size bytes of
        it, or, with size None, all of it.

        The stream stays open and is read once, in order, never seeked; it
        is left just after the bytes uploaded. A short read is not the end,
        but a stream that ends before size bytes fails the upload, as does
        one with no data ready (read() returning None). Parts are buffered
        as they are read, within the client's transfer_limiter, and sent
        several at once when Files.com allows it, as for upload_file.

        A stream of unknown size (size None) goes one part at a time. Give
        spool_limit to copy it first to a temporary file of the SDK's own,
        in spool_directory (the system's temporary directory by default), of
        at most that many bytes, and upload that as a file of known size; a
        longer stream fails before anything is sent. progress, tuning and
        params work as for upload_file; provided_mtime is not sent unless
        params sets it.

        checkpoint and pause_token work as for upload_file, for a stream of
        known size or with spool_limit. To resume, give the same bytes from
        the same start: the parts that arrived before are read again and
        checked, not sent."""
        operation = Operation.start(self._scope, options)
        operation.require_single_completion()
        return uploads.upload_stream(
            operation,
            destination,
            stream,
            size,
            params,
            max_concurrency=max_concurrency,
            progress=progress,
            tuning=tuning,
            spool_limit=spool_limit,
            spool_directory=spool_directory,
            checkpoint=checkpoint,
            pause_token=pause_token,
        )

    def upload_to_remote_server(
        self,
        path: str | Path,
        remote_server_id: int,
        destination: str | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        *,
        max_concurrency: int | None = None,
        progress: Callable[[UploadProgress], None] | None = None,
        tuning: UploadTuning | None = None,
        checkpoint: str | Path | None = None,
        pause_token: PauseToken | None = None,
    ) -> File:
        """Upload the local file at path to destination, by default its
        name, in the Remote Server whose ID is remote_server_id, as upload_file does.
        """
        if destination is None:
            destination = Path(path).name
        return self.upload_file(
            path,
            _underscore_destination_path(
                "RemoteServers", remote_server_id, destination
            ),
            options,
            params,
            max_concurrency=max_concurrency,
            progress=progress,
            tuning=tuning,
            checkpoint=checkpoint,
            pause_token=pause_token,
        )

    def copy_to_remote_server(
        self,
        path: str,
        remote_server_id: int,
        destination: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Copy path to destination in the Remote Server whose ID is remote_server_id."""
        params = copy_params(params)
        params["destination"] = _underscore_destination_path(
            "RemoteServers", remote_server_id, destination
        )
        return self.copy(path, params, options)

    def move_to_remote_server(
        self,
        path: str,
        remote_server_id: int,
        destination: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Move path to destination in the Remote Server whose ID is remote_server_id."""
        params = copy_params(params)
        params["destination"] = _underscore_destination_path(
            "RemoteServers", remote_server_id, destination
        )
        return self.move(path, params, options)

    def upload_to_snapshot(
        self,
        path: str | Path,
        snapshot_id: int,
        destination: str | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        *,
        max_concurrency: int | None = None,
        progress: Callable[[UploadProgress], None] | None = None,
        tuning: UploadTuning | None = None,
        checkpoint: str | Path | None = None,
        pause_token: PauseToken | None = None,
    ) -> File:
        """Upload the local file at path to destination, by default its
        name, in the Snapshot whose ID is snapshot_id, as upload_file does."""
        if destination is None:
            destination = Path(path).name
        return self.upload_file(
            path,
            _underscore_destination_path(
                "Snapshots", snapshot_id, destination
            ),
            options,
            params,
            max_concurrency=max_concurrency,
            progress=progress,
            tuning=tuning,
            checkpoint=checkpoint,
            pause_token=pause_token,
        )

    def copy_to_snapshot(
        self,
        path: str,
        snapshot_id: int,
        destination: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Copy path to destination in the Snapshot whose ID is snapshot_id."""
        params = copy_params(params)
        params["destination"] = _underscore_destination_path(
            "Snapshots", snapshot_id, destination
        )
        return self.copy(path, params, options)

    def move_to_snapshot(
        self,
        path: str,
        snapshot_id: int,
        destination: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Move path to destination in the Snapshot whose ID is snapshot_id."""
        params = copy_params(params)
        params["destination"] = _underscore_destination_path(
            "Snapshots", snapshot_id, destination
        )
        return self.move(path, params, options)

    def upload_to_child_site(
        self,
        path: str | Path,
        site_id: int,
        destination: str | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        *,
        max_concurrency: int | None = None,
        progress: Callable[[UploadProgress], None] | None = None,
        tuning: UploadTuning | None = None,
        checkpoint: str | Path | None = None,
        pause_token: PauseToken | None = None,
    ) -> File:
        """Upload the local file at path to destination, by default its
        name, in the Child Site whose ID is site_id, as upload_file does."""
        if destination is None:
            destination = Path(path).name
        return self.upload_file(
            path,
            _underscore_destination_path("Sites", site_id, destination),
            options,
            params,
            max_concurrency=max_concurrency,
            progress=progress,
            tuning=tuning,
            checkpoint=checkpoint,
            pause_token=pause_token,
        )

    def copy_to_child_site(
        self,
        path: str,
        site_id: int,
        destination: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Copy path to destination in the Child Site whose ID is site_id."""
        params = copy_params(params)
        params["destination"] = _underscore_destination_path(
            "Sites", site_id, destination
        )
        return self.copy(path, params, options)

    def move_to_child_site(
        self,
        path: str,
        site_id: int,
        destination: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> FileAction:
        """Move path to destination in the Child Site whose ID is site_id."""
        params = copy_params(params)
        params["destination"] = _underscore_destination_path(
            "Sites", site_id, destination
        )
        return self.move(path, params, options)

    def download_file(
        self,
        path: str,
        local_path: str | Path | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
        *,
        max_concurrency: int | None = None,
        progress: Callable[[DownloadProgress], None] | None = None,
        tuning: UploadTuning | None = None,
        checkpoint: str | Path | None = None,
        pause_token: PauseToken | None = None,
    ) -> File:
        """Download path to the local file local_path, by default its name
        in the current directory, and return the File downloaded. On
        Windows, a name with a colon, which would be a drive-relative path
        or an NTFS stream, or a device name such as NUL, CON or COM1, which
        would write to the device, raises InvalidParameterError: give
        local_path. A device name with an extension, such as NUL.txt, raises
        only where that Windows version resolves it to the device.

        Where the download is bound to one version of the file, by Files.com's
        download identity or, from Amazon S3 without one, by storage's own
        answer to its first range, ranges of it are fetched at once into a
        temporary file beside
        local_path, which replaces local_path only once the whole file has
        arrived; a failed download leaves local_path as it was. From Amazon
        S3 the number adapts, starting at 150, as the Downloads page of the
        documentation describes; from other storage it is 4. max_concurrency
        (up to 1024) caps it, and tuning, a files_sdk.UploadTuning without
        settings only uploads use, chooses otherwise: adaptive=False fetches
        max_concurrency (or 4) at once. progress, if given, is called on
        this thread with a DownloadProgress. One operation covers every
        request.

        checkpoint, a local path, keeps the temporary file and what has
        arrived in it if the download stops, so that calling download_file
        again with it fetches only the rest, if the remote file is still
        the same; pause_token (a PauseToken) pauses it, raising
        TransferPausedError once its ranges in progress have finished."""
        if local_path is None:
            local_path = _default_local_path(path)
        operation = Operation.start(self._scope, options)
        file = operation.adopt(File(path, {}, options))
        return file._download_file(
            local_path,
            operation,
            max_concurrency=max_concurrency,
            progress=progress,
            tuning=tuning,
            checkpoint=checkpoint,
            pause_token=pause_token,
        )

    def download_stream(
        self,
        path: str,
        stream: BinaryIO,
        options: RequestOptions | Mapping[str, Any] | None = None,
        *,
        max_concurrency: int | None = None,
        progress: Callable[[DownloadProgress], None] | None = None,
        tuning: UploadTuning | None = None,
        checkpoint: str | Path | None = None,
        pause_token: PauseToken | None = None,
    ) -> File:
        """Download path into stream, a binary stream opened for writing,
        and return the File downloaded. The stream stays open and receives
        the content in order, though ranges are fetched at once as for
        download_file, max_concurrency and tuning included; each is held in
        memory, within the client's transfer_limiter, until the ranges
        before it are written. It is never rewound or truncated, so a
        failed download can leave part of the content in it.

        With checkpoint, a later call resumes into a stream just after the
        bytes the earlier one wrote (its tell() must say so), such as a
        file opened with "ab"; pause_token pauses it, as for
        download_file."""
        operation = Operation.start(self._scope, options)
        file = operation.adopt(File(path, {}, options))
        return downloads.download_stream(
            operation,
            file,
            stream,
            max_concurrency=max_concurrency,
            progress=progress,
            tuning=tuning,
            checkpoint=checkpoint,
            pause_token=pause_token,
        )

    def copy_and_wait(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
        *,
        interval: float = 1.0,
        progress: Callable[[FileMigration], None] | None = None,
    ) -> FileMigration | None:
        """Copy path as copy() does, then wait until Files.com has finished
        copying, as FileAction.wait() waits, and return the completed
        FileMigration, or None if the copy finished at once. A copy that
        fails raises FileMigrationError. One operation covers the copy and
        the wait, so its request_timeout or deadline option bounds both."""
        operation = Operation.start(self._scope, options)
        action = FileResource(operation).copy(path, params)
        return migrations.wait_for(operation, action, interval, progress)

    def move_and_wait(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
        *,
        interval: float = 1.0,
        progress: Callable[[FileMigration], None] | None = None,
    ) -> FileMigration | None:
        """Move path as move() does, then wait until Files.com has finished
        moving it, as copy_and_wait() does for a copy."""
        operation = Operation.start(self._scope, options)
        action = FileResource(operation).move(path, params)
        return migrations.wait_for(operation, action, interval, progress)

    def delete_and_wait(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
        *,
        interval: float = 1.0,
    ) -> None:
        """Delete path as delete() does, then wait until Files.com says it
        no longer exists, checking every interval seconds, so that a file
        can be uploaded in its place. One operation covers the deletion and
        the wait, so its request_timeout or deadline option bounds both."""
        operation = Operation.start(self._scope, options)
        FileResource(operation).delete(path, params)
        migrations.wait_until_gone(operation, path, interval)

    def upload_directory(
        self,
        local_path: str | Path,
        remote_path: str = "",
        options: RequestOptions | Mapping[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        *,
        max_files: int | None = None,
        max_concurrency: int | None = None,
        progress: Callable[[TransferJobProgress], None] | None = None,
        tuning: UploadTuning | None = None,
        checkpoint: str | Path | None = None,
        pause_token: PauseToken | None = None,
    ) -> TransferResult:
        """Upload the files and folders under the local directory local_path
        into remote_path (the root folder by default), keeping their
        relative paths, and return a TransferResult with each one's outcome.

        Up to max_files files (4 by default; without it, a job using the
        scaled S3 policy starts with six and prepares as many as its target
        needs, up to 128)
        upload at once, each as upload_file uploads one, all within the
        client's transfer_limiter. The job's adaptive uploads share one
        target, of up to max_concurrency parts, and what it learns, for
        this job only. A file that fails does not
        stop the others. Empty folders are created; symbolic links and
        special files are skipped, not followed. params apply to every
        file, with mkdir_parents on unless they turn it off. progress, if
        given, is called on this thread with a TransferJobProgress.
        checkpoint and pause_token work as for upload_file, for the whole
        job: calling it again with the checkpoint skips the files completed
        before that have not changed. Cancelling, closing the client or the
        deadline stops the whole job, and the error raised has the
        TransferResult so far as its result."""
        operation = Operation.start(self._scope, options)
        return jobs.upload_directory(
            operation,
            local_path,
            remote_path,
            params,
            max_files=max_files,
            max_concurrency=max_concurrency,
            progress=progress,
            tuning=tuning,
            checkpoint=checkpoint,
            pause_token=pause_token,
        )

    def download_directory(
        self,
        remote_path: str,
        local_path: str | Path,
        options: RequestOptions | Mapping[str, Any] | None = None,
        *,
        max_files: int | None = None,
        max_concurrency: int | None = None,
        progress: Callable[[TransferJobProgress], None] | None = None,
        tuning: UploadTuning | None = None,
        checkpoint: str | Path | None = None,
        pause_token: PauseToken | None = None,
    ) -> TransferResult:
        """Download the files and folders under remote_path into the local
        directory local_path, created if need be, keeping their relative
        paths, and return a TransferResult with each one's outcome.

        Up to max_files files (4 by default) download at once, each as
        download_file downloads one, all within the client's
        transfer_limiter. The job's adaptive downloads share one target, of
        up to max_concurrency ranges, and what it learns, for this job only.
        A remote name that cannot be a local file name, or that would lead
        outside local_path, fails for that file alone. progress, checkpoint
        and pause_token work as for upload_directory."""
        operation = Operation.start(self._scope, options)
        return jobs.download_directory(
            operation,
            remote_path,
            local_path,
            max_files=max_files,
            max_concurrency=max_concurrency,
            progress=progress,
            tuning=tuning,
            checkpoint=checkpoint,
            pause_token=pause_token,
        )

    def upload_files(
        self,
        files: Iterable[tuple[str | Path, str]],
        options: RequestOptions | Mapping[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        *,
        max_files: int | None = None,
        max_concurrency: int | None = None,
        progress: Callable[[TransferJobProgress], None] | None = None,
        tuning: UploadTuning | None = None,
        checkpoint: str | Path | None = None,
        pause_token: PauseToken | None = None,
    ) -> TransferResult:
        """Upload each (local path, remote path) pair in files, read as the
        job goes, as upload_directory uploads the files it finds."""
        operation = Operation.start(self._scope, options)
        return jobs.upload_files(
            operation,
            files,
            params,
            max_files=max_files,
            max_concurrency=max_concurrency,
            progress=progress,
            tuning=tuning,
            checkpoint=checkpoint,
            pause_token=pause_token,
        )

    def download_files(
        self,
        files: Iterable[tuple[str, str | Path]],
        options: RequestOptions | Mapping[str, Any] | None = None,
        *,
        max_files: int | None = None,
        max_concurrency: int | None = None,
        progress: Callable[[TransferJobProgress], None] | None = None,
        tuning: UploadTuning | None = None,
        checkpoint: str | Path | None = None,
        pause_token: PauseToken | None = None,
    ) -> TransferResult:
        """Download each (remote path, local path) pair in files, read as
        the job goes, as download_directory downloads the files it finds.
        With a checkpoint, a file completed before is skipped by its remote
        path."""
        operation = Operation.start(self._scope, options)
        return jobs.download_files(
            operation,
            files,
            max_files=max_files,
            max_concurrency=max_concurrency,
            progress=progress,
            tuning=tuning,
            checkpoint=checkpoint,
            pause_token=pause_token,
        )

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> File:
        """A new File with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = File(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = FileResource(LEGACY)


def download(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> File:
    """Download File

    Parameters:
      action - string - Can be blank, `redirect` or `stat`.  If set to `stat`, we will return file information but without a download URL, and without logging a download.  If set to `redirect` we will serve a 302 redirect directly to the file.  This is used for integrations with Zapier, and is not recommended for most integrations.
      preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
      with_previews - boolean - Include file preview information?
      with_priority_color - boolean - Include file priority color information?
      with_direct_connection_info - boolean - Include optional direct connection information for a direct Agent transfer attempt?
    """
    return _legacy_resource.download(path, params, options)


def create(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> File:
    """Parameters:
    path (required) - string - Path to operate on.
    action - string - The action to perform.  Can be `append`, `attachment`, `end`, `upload`, `put`, or may not exist
    custom_metadata - object - Custom metadata map to save when `action=end` completes the upload.  Replaces existing metadata; an empty map clears it.  No separate metadata-edit permission is required.  Supported on native files and configured remote mounts, excluding remote server automount paths.  Limited to 32 keys, 256 characters per key and 1024 characters per value.
    etags[etag] (required) - array(string) - etag identifier.
    etags[part] (required) - array(int64) - Part number.
    length - int64 - Length of file.
    mkdir_parents - boolean - Create parent directories if they do not exist?
    part - int64 - Part if uploading a part.
    parts - int64 - How many parts to fetch?
    provided_mtime - string - User provided modification time.
    ref - string -
    restart - int64 - File byte offset to restart from.
    size - int64 - Size of file.
    copy_behaviors - boolean - If copying a folder, also copy supported behaviors, email notification subscriptions, and per-folder branding to the destination folder tree?
    structure - string - If copying folder, copy just the structure?
    with_rename - boolean - Allow file rename instead of overwrite?
    buffered_upload - boolean - If true, and the path refers to a destination not stored on Files.com (such as a remote server mount), the upload will be uploaded first to Files.com before being sent to the remote server mount. This can allow clients to upload using parallel parts to a remote server destination that does not offer parallel parts support natively.
    with_direct_connection_info - boolean - Include optional direct connection information for a direct Agent transfer attempt?
    """
    return _legacy_resource.create(path, params, options)


def update(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> File:
    """Parameters:
    custom_metadata - object - Custom metadata map of keys and values. Limited to 32 keys, 256 characters per key and 1024 characters per value.
    provided_mtime - string - Modified time of file.
    priority_color - string - Priority/Bookmark color of file.
    """
    return _legacy_resource.update(path, params, options)


def delete(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Parameters:
    recursive - boolean - If true, will recursively delete folders.  Otherwise, will error on non-empty folders.
    """
    _legacy_resource.delete(path, params, options)


def destroy(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(path, params, options)


def find(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> File:
    """Parameters:
    path (required) - string - Path to operate on.
    preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
    with_previews - boolean - Include file preview information?
    with_priority_color - boolean - Include file priority color information?
    """
    return _legacy_resource.find(path, params, options)


def get(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> File:
    """The same as find()."""
    return _legacy_resource.find(path, params, options)


def zip_list_contents(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> builtins.list[ZipListEntry]:
    """List the contents of a ZIP file"""
    return _legacy_resource.zip_list_contents(path, params, options)


def begin_delete(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FileAction:
    """Delete File/Folder and return its File Action.  A pending or processing deletion continues in the background after this returns; check its File Migration for completion.  Waiting for the File Migration does not cancel the deletion

    Parameters:
      recursive - boolean - If true, will recursively delete folders.  Otherwise, will error on non-empty folders.
    """
    return _legacy_resource.begin_delete(path, params, options)


def copy(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FileAction:
    """Copy File/Folder

    Parameters:
      destination (required) - string - Copy destination path.
      copy_behaviors - boolean - If copying a folder, also copy supported behaviors, email notification subscriptions, and per-folder branding to the destination folder tree?
      structure - boolean - Copy structure only?
      overwrite - boolean - Overwrite existing file(s) in the destination?
    """
    return _legacy_resource.copy(path, params, options)


def move(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FileAction:
    """Move File/Folder

    Parameters:
      destination (required) - string - Move destination path.
      overwrite - boolean - Overwrite existing file(s) in the destination?
    """
    return _legacy_resource.move(path, params, options)


def transform(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FileAction:
    """Transform a file and save the output to a destination path

    Parameters:
      destination (required) - string - Destination file path for the transformed output.
      transform_type (required) - string - Transform type. Supported values are `image_convert`, `document_convert`, and `files_transform_script_execute`.
      target_format (required) - string - Destination format to create.
      script - string - Files TransformScript source. Required when transform_type is `files_transform_script_execute`.
      width - int64 - Maximum output width for image_convert.
      height - int64 - Maximum output height for image_convert.
      overwrite - boolean - Overwrite existing file in the destination?
    """
    return _legacy_resource.transform(path, params, options)


def gpg_decrypt(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FileAction:
    """Decrypt a GPG-encrypted file and save it to a destination path

    Parameters:
      destination (required) - string - Destination file path for the decrypted file.
      gpg_key_ids - array(int64) - GPG Key IDs to decrypt with. If omitted, every accessible private GPG key in the source workspace is used.
      gpg_key_partner_id - int64 - Partner ID whose GPG keys should be used for decryption.
      use_all_private_keys - boolean - Use every accessible private GPG key in the source workspace for decryption.
      ignore_mdc_error - boolean - Ignore errors from the MDC (modification detection code) check.
      overwrite - boolean - Overwrite existing file in the destination?
    """
    return _legacy_resource.gpg_decrypt(path, params, options)


def gpg_encrypt(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FileAction:
    """Encrypt a file with GPG and save it to a destination path

    Parameters:
      destination (required) - string - Destination file path for the encrypted file.
      gpg_key_ids - array(int64) - GPG Key IDs to encrypt with.
      gpg_key_partner_id - int64 - Partner ID whose GPG keys should be used for encryption.
      signing_key_id - int64 - Optional GPG Key ID to sign with.
      armor - boolean - Output ASCII-armored encrypted data.
      overwrite - boolean - Overwrite existing file in the destination?
    """
    return _legacy_resource.gpg_encrypt(path, params, options)


def unzip(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FileAction:
    """Extract a ZIP file to a destination folder

    Parameters:
      destination (required) - string - Destination folder path for extracted files.
      filename - string - Optional single entry filename to extract.
      overwrite - boolean - Overwrite existing files in the destination?
    """
    return _legacy_resource.unzip(path, params, options)


def zip(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> FileAction:
    """Parameters:
    paths (required) - array(string) - Paths to include in the ZIP.
    destination (required) - string - Destination file path for the ZIP.
    overwrite - boolean - Overwrite existing file in the destination?
    """
    return _legacy_resource.zip(params, options)


def begin_upload(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> builtins.list[FileUploadPart]:
    """Begin File Upload

    Parameters:
      mkdir_parents - boolean - Create parent directories if they do not exist?
      part - int64 - Part if uploading a part.
      parts - int64 - How many parts to fetch?
      ref - string -
      restart - int64 - File byte offset to restart from.
      size - int64 - Total bytes of file being uploaded (include bytes being retained if appending/restarting).
      with_rename - boolean - Allow file rename instead of overwrite?
      buffered_upload - boolean - If true, and the path refers to a destination not stored on Files.com (such as a remote server mount), the upload will be uploaded first to Files.com before being sent to the remote server mount. This can allow clients to upload using parallel parts to a remote server destination that does not offer parallel parts support natively.
      with_direct_connection_info - boolean - Include optional direct connection information for a direct Agent transfer attempt?
    """
    return _legacy_resource.begin_upload(path, params, options)


def _checked_mode(mode) -> bool:
    """Whether mode, a mode open() accepts, is a text mode."""
    if (
        not isinstance(mode, str)
        or not mode
        or set(mode) - set("rwaxbt+")
        or len(set(mode)) != len(mode)
    ):
        raise ValueError("invalid mode: {!r}".format(mode))
    kinds = [letter for letter in mode if letter in "rwax"]
    if len(kinds) != 1 or ("b" in mode and "t" in mode):
        raise ValueError("invalid mode: {!r}".format(mode))
    if kinds[0] in "ax" or "+" in mode:
        raise io.UnsupportedOperation(
            "A remote file can be opened for reading (r) or writing (w), not with mode {!r}".format(
                mode
            )
        )
    return "b" not in mode


_WINDOWS_DEVICE_NAMES = frozenset(
    [
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "CONIN$",
        "CONOUT$",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "COM\u00b9",
        "COM\u00b2",
        "COM\u00b3",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
        "LPT\u00b9",
        "LPT\u00b2",
        "LPT\u00b3",
    ]
)


def _underscore_destination_path(root, destination_id, relative_path=None):
    return path_util.normalize(
        f"_/{root}/{destination_id}/{relative_path or ''}"
    )


def _is_windows_device_name(name):
    # A bare device name is always a device. Anything after it, such as the
    # extension in NUL.txt, makes it a device on some Windows versions and a
    # file on others, so Windows decides those names: it resolves a device to
    # a \\.\ path.
    base = name.split(".", 1)[0].rstrip(" ")
    if base.upper() not in _WINDOWS_DEVICE_NAMES:
        return False
    return base == name or os.path.abspath(name).startswith("\\\\.\\")


def _default_local_path(path):
    name = path_util.normalize(path).split("/")[-1]
    # On Windows a colon makes the name a drive-relative path or an NTFS
    # stream, which can write outside the working directory or onto another
    # file, and a device name such as NUL writes to the device instead of a file.
    if os.name == "nt" and (":" in name or _is_windows_device_name(name)):
        raise InvalidParameterError(
            f"Bad parameter: local_path is required because {name!r} is not a valid local file name"
        )
    return name


_Options = RequestOptions | Mapping[str, Any] | None
_Params = dict[str, Any] | None


def open(path: str, mode: str = "r", options: _Options = None) -> File:
    return FileResource(LEGACY).open(path, mode, options)


def upload_chunks(
    io: Any,
    path: str,
    options: _Options,
    upload: Any = None,
    etags: list[Any] | None = None,
    params: _Params = None,
) -> tuple[Any, list[Any], int]:
    return FileResource(Operation.start(LEGACY, options)).upload_chunks(
        io, path, upload, etags, params
    )


def upload_file(
    path: str | Path,
    destination: str | None = None,
    options: _Options = None,
    params: _Params = None,
    *,
    max_concurrency: int | None = None,
    progress: Callable[[UploadProgress], None] | None = None,
    tuning: UploadTuning | None = None,
    checkpoint: str | Path | None = None,
    pause_token: PauseToken | None = None,
) -> File:
    return FileResource(LEGACY).upload_file(
        path,
        destination,
        options,
        params,
        max_concurrency=max_concurrency,
        progress=progress,
        tuning=tuning,
        checkpoint=checkpoint,
        pause_token=pause_token,
    )


def upload_stream(
    stream: BinaryIO,
    destination: str,
    size: int | None = None,
    options: _Options = None,
    params: _Params = None,
    *,
    max_concurrency: int | None = None,
    progress: Callable[[UploadProgress], None] | None = None,
    tuning: UploadTuning | None = None,
    spool_limit: int | None = None,
    spool_directory: str | Path | None = None,
    checkpoint: str | Path | None = None,
    pause_token: PauseToken | None = None,
) -> File:
    return FileResource(LEGACY).upload_stream(
        stream,
        destination,
        size,
        options,
        params,
        max_concurrency=max_concurrency,
        progress=progress,
        tuning=tuning,
        spool_limit=spool_limit,
        spool_directory=spool_directory,
        checkpoint=checkpoint,
        pause_token=pause_token,
    )


def upload_to_remote_server(
    path: str | Path,
    remote_server_id: int,
    destination: str | None = None,
    options: _Options = None,
    params: _Params = None,
    *,
    max_concurrency: int | None = None,
    progress: Callable[[UploadProgress], None] | None = None,
    tuning: UploadTuning | None = None,
    checkpoint: str | Path | None = None,
    pause_token: PauseToken | None = None,
) -> File:
    return FileResource(LEGACY).upload_to_remote_server(
        path,
        remote_server_id,
        destination,
        options,
        params,
        max_concurrency=max_concurrency,
        progress=progress,
        tuning=tuning,
        checkpoint=checkpoint,
        pause_token=pause_token,
    )


def copy_to_remote_server(
    path: str,
    remote_server_id: int,
    destination: str,
    params: _Params = None,
    options: _Options = None,
) -> FileAction:
    return FileResource(LEGACY).copy_to_remote_server(
        path, remote_server_id, destination, params, options
    )


def move_to_remote_server(
    path: str,
    remote_server_id: int,
    destination: str,
    params: _Params = None,
    options: _Options = None,
) -> FileAction:
    return FileResource(LEGACY).move_to_remote_server(
        path, remote_server_id, destination, params, options
    )


def upload_to_snapshot(
    path: str | Path,
    snapshot_id: int,
    destination: str | None = None,
    options: _Options = None,
    params: _Params = None,
    *,
    max_concurrency: int | None = None,
    progress: Callable[[UploadProgress], None] | None = None,
    tuning: UploadTuning | None = None,
    checkpoint: str | Path | None = None,
    pause_token: PauseToken | None = None,
) -> File:
    return FileResource(LEGACY).upload_to_snapshot(
        path,
        snapshot_id,
        destination,
        options,
        params,
        max_concurrency=max_concurrency,
        progress=progress,
        tuning=tuning,
        checkpoint=checkpoint,
        pause_token=pause_token,
    )


def copy_to_snapshot(
    path: str,
    snapshot_id: int,
    destination: str,
    params: _Params = None,
    options: _Options = None,
) -> FileAction:
    return FileResource(LEGACY).copy_to_snapshot(
        path, snapshot_id, destination, params, options
    )


def move_to_snapshot(
    path: str,
    snapshot_id: int,
    destination: str,
    params: _Params = None,
    options: _Options = None,
) -> FileAction:
    return FileResource(LEGACY).move_to_snapshot(
        path, snapshot_id, destination, params, options
    )


def upload_to_child_site(
    path: str | Path,
    site_id: int,
    destination: str | None = None,
    options: _Options = None,
    params: _Params = None,
    *,
    max_concurrency: int | None = None,
    progress: Callable[[UploadProgress], None] | None = None,
    tuning: UploadTuning | None = None,
    checkpoint: str | Path | None = None,
    pause_token: PauseToken | None = None,
) -> File:
    return FileResource(LEGACY).upload_to_child_site(
        path,
        site_id,
        destination,
        options,
        params,
        max_concurrency=max_concurrency,
        progress=progress,
        tuning=tuning,
        checkpoint=checkpoint,
        pause_token=pause_token,
    )


def copy_to_child_site(
    path: str,
    site_id: int,
    destination: str,
    params: _Params = None,
    options: _Options = None,
) -> FileAction:
    return FileResource(LEGACY).copy_to_child_site(
        path, site_id, destination, params, options
    )


def move_to_child_site(
    path: str,
    site_id: int,
    destination: str,
    params: _Params = None,
    options: _Options = None,
) -> FileAction:
    return FileResource(LEGACY).move_to_child_site(
        path, site_id, destination, params, options
    )


def download_file(
    path: str,
    local_path: str | Path | None = None,
    options: _Options = None,
    *,
    max_concurrency: int | None = None,
    progress: Callable[[DownloadProgress], None] | None = None,
    tuning: UploadTuning | None = None,
    checkpoint: str | Path | None = None,
    pause_token: PauseToken | None = None,
) -> File:
    return FileResource(LEGACY).download_file(
        path,
        local_path,
        options,
        max_concurrency=max_concurrency,
        progress=progress,
        tuning=tuning,
        checkpoint=checkpoint,
        pause_token=pause_token,
    )


def download_stream(
    path: str,
    stream: BinaryIO,
    options: _Options = None,
    *,
    max_concurrency: int | None = None,
    progress: Callable[[DownloadProgress], None] | None = None,
    tuning: UploadTuning | None = None,
    checkpoint: str | Path | None = None,
    pause_token: PauseToken | None = None,
) -> File:
    return FileResource(LEGACY).download_stream(
        path,
        stream,
        options,
        max_concurrency=max_concurrency,
        progress=progress,
        tuning=tuning,
        checkpoint=checkpoint,
        pause_token=pause_token,
    )


def copy_and_wait(
    path: str,
    params: _Params = None,
    options: _Options = None,
    *,
    interval: float = 1.0,
    progress: Callable[[FileMigration], None] | None = None,
) -> FileMigration | None:
    return FileResource(LEGACY).copy_and_wait(
        path, params, options, interval=interval, progress=progress
    )


def move_and_wait(
    path: str,
    params: _Params = None,
    options: _Options = None,
    *,
    interval: float = 1.0,
    progress: Callable[[FileMigration], None] | None = None,
) -> FileMigration | None:
    return FileResource(LEGACY).move_and_wait(
        path, params, options, interval=interval, progress=progress
    )


def delete_and_wait(
    path: str,
    params: _Params = None,
    options: _Options = None,
    *,
    interval: float = 1.0,
) -> None:
    FileResource(LEGACY).delete_and_wait(
        path, params, options, interval=interval
    )


def upload_directory(
    local_path: str | Path,
    remote_path: str = "",
    options: _Options = None,
    params: _Params = None,
    *,
    max_files: int | None = None,
    max_concurrency: int | None = None,
    progress: Callable[[TransferJobProgress], None] | None = None,
    tuning: UploadTuning | None = None,
    checkpoint: str | Path | None = None,
    pause_token: PauseToken | None = None,
) -> TransferResult:
    return FileResource(LEGACY).upload_directory(
        local_path,
        remote_path,
        options,
        params,
        max_files=max_files,
        max_concurrency=max_concurrency,
        progress=progress,
        tuning=tuning,
        checkpoint=checkpoint,
        pause_token=pause_token,
    )


def download_directory(
    remote_path: str,
    local_path: str | Path,
    options: _Options = None,
    *,
    max_files: int | None = None,
    max_concurrency: int | None = None,
    progress: Callable[[TransferJobProgress], None] | None = None,
    tuning: UploadTuning | None = None,
    checkpoint: str | Path | None = None,
    pause_token: PauseToken | None = None,
) -> TransferResult:
    return FileResource(LEGACY).download_directory(
        remote_path,
        local_path,
        options,
        max_files=max_files,
        max_concurrency=max_concurrency,
        progress=progress,
        tuning=tuning,
        checkpoint=checkpoint,
        pause_token=pause_token,
    )


def upload_files(
    files: Iterable[tuple[str | Path, str]],
    options: _Options = None,
    params: _Params = None,
    *,
    max_files: int | None = None,
    max_concurrency: int | None = None,
    progress: Callable[[TransferJobProgress], None] | None = None,
    tuning: UploadTuning | None = None,
    checkpoint: str | Path | None = None,
    pause_token: PauseToken | None = None,
) -> TransferResult:
    return FileResource(LEGACY).upload_files(
        files,
        options,
        params,
        max_files=max_files,
        max_concurrency=max_concurrency,
        progress=progress,
        tuning=tuning,
        checkpoint=checkpoint,
        pause_token=pause_token,
    )


def download_files(
    files: Iterable[tuple[str, str | Path]],
    options: _Options = None,
    *,
    max_files: int | None = None,
    max_concurrency: int | None = None,
    progress: Callable[[TransferJobProgress], None] | None = None,
    tuning: UploadTuning | None = None,
    checkpoint: str | Path | None = None,
    pause_token: PauseToken | None = None,
) -> TransferResult:
    return FileResource(LEGACY).download_files(
        files,
        options,
        max_files=max_files,
        max_concurrency=max_concurrency,
        progress=progress,
        tuning=tuning,
        checkpoint=checkpoint,
        pause_token=pause_token,
    )


def new(*args, **kwargs) -> File:
    return File(*args, **kwargs)
