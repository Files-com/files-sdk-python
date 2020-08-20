import datetime
from files_sdk.models.file import File
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Folder:
    default_attributes = {
        'id': None,     # int64 - File/Folder ID
        'path': None,     # string - File/Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'display_name': None,     # string - File/Folder display name
        'type': None,     # string - Type: `directory` or `file`.
        'size': None,     # int64 - File/Folder size
        'mtime': None,     # date-time - File last modified date/time, according to the server.  This is the timestamp of the last Files.com operation of the file, regardless of what modified timestamp was sent.
        'provided_mtime': None,     # date-time - File last modified date/time, according to the client who set it.  Files.com allows desktop, FTP, SFTP, and WebDAV clients to set modified at times.  This allows Desktop<->Cloud syncing to preserve modified at times.
        'crc32': None,     # string - File CRC32 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        'md5': None,     # string - File MD5 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        'mime_type': None,     # string - MIME Type.  This is determined by the filename extension and is not stored separately internally.
        'region': None,     # string - Region location
        'permissions': None,     # string - A short string representing the current user's permissions.  Can be `r`,`w`,`p`, or any combination
        'subfolders_locked?': None,     # boolean - Are subfolders locked and unable to be modified?
        'download_uri': None,     # string - Link to download file. Provided only in response to a download request.
        'priority_color': None,     # string - Bookmark/priority color of file/folder
        'preview_id': None,     # int64 - File preview ID
        'preview': None,     # File preview
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Folder.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Folder.default_attributes if getattr(self, k, None) is not None}


    def save(self):
        new_obj = create(self.path, self.get_attributes(), self.options)
        self.set_attributes(new_obj.get_attributes())

# Parameters:
#   page - int64 - Current page number.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   action - string - Action to take.  Can be `count`, `size`, `permissions`, or blank.
#   cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor header.
#   path (required) - string - Path to operate on.
#   filter - string - If specified, will to filter folders/files list by this string.  Wildcards of `*` and `?` are acceptable here.
#   preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
#   search - string - If `search_all` is `true`, provide the search string here.  Otherwise, this parameter acts like an alias of `filter`.
#   search_all - boolean - Search entire site?
#   with_previews - boolean - Include file previews?
#   with_priority_color - boolean - Include file priority color information?
def list_for(path, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["path"] = path
    if "page" in params and not isinstance(params["page"], int):
        raise InvalidParameterError("Bad parameter: page must be an int")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "filter" in params and not isinstance(params["filter"], str):
        raise InvalidParameterError("Bad parameter: filter must be an str")
    if "preview_size" in params and not isinstance(params["preview_size"], str):
        raise InvalidParameterError("Bad parameter: preview_size must be an str")
    if "search" in params and not isinstance(params["search"], str):
        raise InvalidParameterError("Bad parameter: search must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    return ListObj(File,"GET", "/folders/{path}".format(path=params['path']), params, options)

# Parameters:
#   path (required) - string - Path to operate on.
def create(path, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request("POST", "/folders/{path}".format(path=params['path']), params, options)
    return File(response.data, options)

def new(*args, **kwargs):
    return Folder(*args, **kwargs)