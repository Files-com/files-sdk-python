import builtins  # noqa: F401
from files_sdk.models.file import File
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Folder:
    default_attributes = {
        "path": None,  # string - File/Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "created_by_id": None,  # int64 - User ID of the User who created the file/folder
        "created_by_api_key_id": None,  # int64 - ID of the API key that created the file/folder
        "created_by_as2_incoming_message_id": None,  # int64 - ID of the AS2 Incoming Message that created the file/folder
        "created_by_automation_id": None,  # int64 - ID of the Automation that created the file/folder
        "created_by_bundle_registration_id": None,  # int64 - ID of the Bundle Registration that created the file/folder
        "created_by_inbox_id": None,  # int64 - ID of the Inbox that created the file/folder
        "created_by_remote_server_id": None,  # int64 - ID of the Remote Server that created the file/folder
        "created_by_remote_server_sync_id": None,  # int64 - ID of the Remote Server Sync that created the file/folder
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
        "last_modified_by_remote_server_sync_id": None,  # int64 - ID of the Remote Server Sync that last modified the file/folder
        "mtime": None,  # date-time - File last modified date/time, according to the server.  This is the timestamp of the last Files.com operation of the file, regardless of what modified timestamp was sent.
        "provided_mtime": None,  # date-time - File last modified date/time, according to the client who set it.  Files.com allows desktop, FTP, SFTP, and WebDAV clients to set modified at times.  This allows Desktop<->Cloud syncing to preserve modified at times.
        "crc32": None,  # string - File CRC32 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        "md5": None,  # string - File MD5 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        "mime_type": None,  # string - MIME Type.  This is determined by the filename extension and is not stored separately internally.
        "region": None,  # string - Region location
        "permissions": None,  # string - A short string representing the current user's permissions.  Can be `r` (Read),`w` (Write),`d` (Delete), `l` (List) or any combination
        "subfolders_locked?": None,  # boolean - Are subfolders locked and unable to be modified?
        "is_locked": None,  # boolean - Is this folder locked and unable to be modified?
        "download_uri": None,  # string - Link to download file. Provided only in response to a download request.
        "priority_color": None,  # string - Bookmark/priority color of file/folder
        "preview_id": None,  # int64 - File preview ID
        "preview": None,  # Preview - File preview
        "mkdir_parents": None,  # boolean - Create parent directories if they do not exist?
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Folder.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Folder.default_attributes
            if getattr(self, k, None) is not None
        }

    def save(self):
        new_obj = create(self.path, self.get_attributes(), self.options)
        self.set_attributes(new_obj.get_attributes())
        return True


# Parameters:
#   cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   path (required) - string - Path to operate on.
#   filter - string - If specified, will filter folders/files list by name. Ignores text before last `/`. Wildcards of `*` and `?` are acceptable here.
#   preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
#   sort_by - object - Search by field and direction. Valid fields are `path`, `size`, `modified_at_datetime`, `provided_modified_at`.  Valid directions are `asc` and `desc`.  Defaults to `{"path":"asc"}`.
#   search - string - If `search_all` is `true`, provide the search string here.  Otherwise, this parameter acts like an alias of `filter`.
#   search_all - boolean - Search entire site?  If set, we will ignore the folder path provided and search the entire site.  This is the same API used by the search bar in the UI.  Search results are a best effort, not real time, and not guaranteed to match every file.  This field should only be used for ad-hoc (human) searching, and not as part of an automated process.
#   with_previews - boolean - Include file previews?
#   with_priority_color - boolean - Include file priority color information?
def list_for(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "filter" in params and not isinstance(params["filter"], str):
        raise InvalidParameterError("Bad parameter: filter must be an str")
    if "preview_size" in params and not isinstance(
        params["preview_size"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: preview_size must be an str"
        )
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "search" in params and not isinstance(params["search"], str):
        raise InvalidParameterError("Bad parameter: search must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    return ListObj(
        File,
        "GET",
        "/folders/{path}".format(path=params["path"]),
        params,
        options,
    )


# Parameters:
#   path (required) - string - Path to operate on.
#   mkdir_parents - boolean - Create parent directories if they do not exist?
#   provided_mtime - string - User provided modification time.
def create(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "provided_mtime" in params and not isinstance(
        params["provided_mtime"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provided_mtime must be an str"
        )
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request(
        "POST", "/folders/{path}".format(path=params["path"]), params, options
    )
    return File(response.data, options)


def new(*args, **kwargs):
    return Folder(*args, **kwargs)
