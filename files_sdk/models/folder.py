import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from typing import Iterator
import files_sdk.path_util as path_util
from files_sdk.models.file import File
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
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Folder:
    """A folder record from the Files.com API.

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
        mkdir_parents: boolean - Create parent directories if they do not exist?
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
        "mkdir_parents": None,  # boolean - Create parent directories if they do not exist?
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
    mkdir_parents: bool | None

    # The client and settings this object's operations use: those of the
    # operation or client that made it, or the module's when it starts an
    # operation if neither did.
    _context: Any = None

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = dict(options)

    def set_attributes(self, attributes):
        for attribute, default_value in Folder.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Folder.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def save(self) -> None:
        """Create this object on the server, taking in place the record it
        returns."""
        new_obj = FolderResource(self._scope()).create(
            getattr(self, "path"), self.get_attributes()
        )
        self.set_attributes(new_obj.get_attributes())
        self._context = new_obj._context


class FolderResource:
    """Folder operations that use one client's configuration.

    Get one from a client, such as ``client.folder``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list_for(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[File]:
        """Parameters:
        cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        path (required) - string - Path to operate on.
        preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
        sort_by - object - Search by field and direction. Valid fields are `path`, `size`, `modified_at_datetime`, `provided_modified_at`.  Valid directions are `asc` and `desc`.  Defaults to `{"path":"asc"}`.
        search - string - If specified, will search the folders/files list by name. Ignores text before last `/`. This is the same API used by the search bar in the web UI when running 'Search This Folder'.  Search results are a best effort, not real time, and not guaranteed to perfectly match the latest folder listing.  Results may be truncated if more than 1,000 possible matches exist.  This field should only be used for ad-hoc (human) searching, and not as part of an automated process.
        search_custom_metadata_key - string - If provided, the search string in `search` will search for files where this custom metadata key matches the value sent in `search`.  Set this to `*` to allow any metadata key to match the value sent in `search`.
        search_all - boolean - Search entire site?  If true, we will search the entire site.  Do not provide a path when using this parameter.  This is the same API used by the search bar in the web UI when running 'Search All Files'.  Search results are a best effort, not real time, and not guaranteed to match every file.  This field should only be used for ad-hoc (human) searching, and not as part of an automated process.
        with_previews - boolean - Include file previews?
        with_priority_color - boolean - Include file priority color information?
        type - string - Type of objects to return.  Can be `folder` or `file`.
        modified_at_datetime - string - If provided, will only return files/folders modified after this time. Can be used only in combination with `type` filter.
        """
        return self.__list_for({"path": path}, params, options)

    def __list_for(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ListObj[File]:
        params = copy_params(params, path_values)
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "preview_size" in params and not isinstance(
            params["preview_size"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: preview_size must be an str"
            )
        if "sort_by" in params and not isinstance(params["sort_by"], dict):
            raise InvalidParameterError(
                "Bad parameter: sort_by must be an dict"
            )
        if "search" in params and not isinstance(params["search"], str):
            raise InvalidParameterError("Bad parameter: search must be an str")
        if "search_custom_metadata_key" in params and not isinstance(
            params["search_custom_metadata_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: search_custom_metadata_key must be an str"
            )
        if "search_all" in params and not isinstance(
            params["search_all"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: search_all must be an bool"
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
        if "type" in params and not isinstance(params["type"], str):
            raise InvalidParameterError("Bad parameter: type must be an str")
        if "modified_at_datetime" in params and not isinstance(
            params["modified_at_datetime"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: modified_at_datetime must be an str"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        return ListObj(
            File,
            "GET",
            "/folders/" + path_value(params["path"]),
            params,
            operation,
        )

    def create(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> File:
        """Parameters:
        path (required) - string - Path to operate on.
        mkdir_parents - boolean - Create parent directories if they do not exist?
        provided_mtime - string - User provided modification time.
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
        if "mkdir_parents" in params and not isinstance(
            params["mkdir_parents"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: mkdir_parents must be an bool"
            )
        if "provided_mtime" in params and not isinstance(
            params["provided_mtime"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provided_mtime must be an str"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST", "/folders/" + path_value(params["path"]), params
        )
        return operation.decode_model(response, File)

    def walk(
        self,
        path: str = "",
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Iterator[tuple[str, builtins.list[File], builtins.list[File]]]:
        """Walk the folder tree under path (the root folder by default),
        top down, as os.walk() walks a local one: for each folder, yield its
        path, the folders in it and the files in it, as File objects.

        Each folder is listed, a page at a time, when the walk reaches it,
        and its subfolders are walked in the order of its folders list,
        which can be changed in place to skip some. One operation covers
        the whole walk, so its cancel_token and deadline options apply to
        all of it."""
        operation = Operation.start(self._scope, options)
        return _walk(operation, path)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Folder:
        """A new Folder with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Folder(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = FolderResource(LEGACY)


def list_for(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[File]:
    """Parameters:
    cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    path (required) - string - Path to operate on.
    preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
    sort_by - object - Search by field and direction. Valid fields are `path`, `size`, `modified_at_datetime`, `provided_modified_at`.  Valid directions are `asc` and `desc`.  Defaults to `{"path":"asc"}`.
    search - string - If specified, will search the folders/files list by name. Ignores text before last `/`. This is the same API used by the search bar in the web UI when running 'Search This Folder'.  Search results are a best effort, not real time, and not guaranteed to perfectly match the latest folder listing.  Results may be truncated if more than 1,000 possible matches exist.  This field should only be used for ad-hoc (human) searching, and not as part of an automated process.
    search_custom_metadata_key - string - If provided, the search string in `search` will search for files where this custom metadata key matches the value sent in `search`.  Set this to `*` to allow any metadata key to match the value sent in `search`.
    search_all - boolean - Search entire site?  If true, we will search the entire site.  Do not provide a path when using this parameter.  This is the same API used by the search bar in the web UI when running 'Search All Files'.  Search results are a best effort, not real time, and not guaranteed to match every file.  This field should only be used for ad-hoc (human) searching, and not as part of an automated process.
    with_previews - boolean - Include file previews?
    with_priority_color - boolean - Include file priority color information?
    type - string - Type of objects to return.  Can be `folder` or `file`.
    modified_at_datetime - string - If provided, will only return files/folders modified after this time. Can be used only in combination with `type` filter.
    """
    return _legacy_resource.list_for(path, params, options)


def create(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> File:
    """Parameters:
    path (required) - string - Path to operate on.
    mkdir_parents - boolean - Create parent directories if they do not exist?
    provided_mtime - string - User provided modification time.
    """
    return _legacy_resource.create(path, params, options)


def _walk(operation, path):
    stack = [path_util.normalize(path or "")]
    while stack:
        folder = stack.pop()
        folders: builtins.list[File] = []
        files: builtins.list[File] = []
        for entry in (
            FolderResource(operation)
            .list_for(folder, {"per_page": 1000})
            .auto_paging_iter()
        ):
            (folders if entry.type == "directory" else files).append(entry)
        yield folder, folders, files
        # After the caller has seen, and may have pruned, the folders.
        stack.extend(
            reversed(
                [path_util.normalize(entry.path or "") for entry in folders]
            )
        )


def walk(
    path: str = "", options: RequestOptions | Mapping[str, Any] | None = None
) -> Iterator[tuple[str, builtins.list[File], builtins.list[File]]]:
    return FolderResource(LEGACY).walk(path, options)


def new(*args, **kwargs) -> Folder:
    return Folder(*args, **kwargs)
