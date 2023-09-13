import builtins  # noqa: F401
from builtins import open as builtin_open
from datetime import datetime
import io
from pathlib import Path
from files_sdk.models.file_action import FileAction
from files_sdk.models.file_upload_part import FileUploadPart
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class File:
    default_attributes = {
        "path": None,  # string - File/Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "display_name": None,  # string - File/Folder display name
        "type": None,  # string - Type: `directory` or `file`.
        "size": None,  # int64 - File/Folder size
        "created_at": None,  # date-time - File created date/time
        "mtime": None,  # date-time - File last modified date/time, according to the server.  This is the timestamp of the last Files.com operation of the file, regardless of what modified timestamp was sent.
        "provided_mtime": None,  # date-time - File last modified date/time, according to the client who set it.  Files.com allows desktop, FTP, SFTP, and WebDAV clients to set modified at times.  This allows Desktop<->Cloud syncing to preserve modified at times.
        "crc32": None,  # string - File CRC32 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        "md5": None,  # string - File MD5 checksum. This is sometimes delayed, so if you get a blank response, wait and try again.
        "mime_type": None,  # string - MIME Type.  This is determined by the filename extension and is not stored separately internally.
        "region": None,  # string - Region location
        "permissions": None,  # string - A short string representing the current user's permissions.  Can be `r`,`w`,`d`, `l` or any combination
        "subfolders_locked?": None,  # boolean - Are subfolders locked and unable to be modified?
        "is_locked": None,  # boolean - Is this folder locked and unable to be modified?
        "download_uri": None,  # string - Link to download file. Provided only in response to a download request.
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
        "structure": None,  # string - If copying folder, copy just the structure?
        "with_rename": None,  # boolean - Allow file rename instead of overwrite?
    }

    def __init__(self, *args):
        self.set_attributes({})
        self.options = {}
        self.mode = "r"
        self.upload = None
        self.etags = None
        self.io_obj = io.StringIO()
        self.closed = True

        self.bytes_written = 0
        if len(args) >= 1:
            if isinstance(args[0], dict):
                self.set_attributes(args[0])
            elif isinstance(args[0], str):
                self.set_attributes({"path": args[0]})
        if len(args) >= 2:
            if isinstance(args[1], dict):
                self.options = args[1]
            elif isinstance(args[1], str):
                self.mode = args[1]
        if len(args) >= 3:
            if isinstance(args[2], dict):
                self.options = args[2]

    def set_attributes(self, attributes):
        for attribute, default_value in File.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in File.default_attributes
            if getattr(self, k, None) is not None
        }

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __del__(self):
        if not self.io_obj.closed:
            self.io_obj.close()

    def close(self):
        self.flush()

        if self.upload:
            end_options = {
                "action": "end",
                "etags": self.etags,
                "provided_mtime": datetime.now().isoformat(),
                "ref": self.upload.ref,
                "size": self.bytes_written,
            }

            file = create(self.path, end_options, self.options)
            self.set_attributes(file.get_attributes())
            self.mode = "r"
            self.upload = None
            self.etags = None
            self.io_obj = io.StringIO()
        self.io_obj.close
        self.closed = True

    def fileno(self):
        raise OSError

    def flush(self, *_args):
        if "w" in self.mode:
            if self.io_obj.seekable():
                self.io_obj.seek(0)

            self.upload, self.etags, bytes_written = upload_chunks(
                self.io_obj, self.path, self.options, self.upload, self.etags
            )
            self.bytes_written += bytes_written
        elif "a" in self.mode:
            raise io.UnsupportedOperation("Append is not a supported mode")

    def isatty(self):
        return False

    def read(self):
        if self.readable():
            self.download_content(
                self.io_obj, False if "b" in self.mode else True
            )
            self.io_obj.seek(0)
            return self.io_obj.read()
        else:
            raise OSError("read mode not indicated")

    def readable(self):
        if "r" in self.mode and not self.closed:
            return True
        return False

    def readall(self):
        self.read()

    def readinto(self):
        return NotImplementedError

    def readline(self):
        return NotImplementedError

    def seek(self):
        raise OSError

    def seekable(self):
        return False

    def tell(self):
        raise OSError

    def truncate(self):
        raise OSError

    def writeable(self):
        if "w" in self.mode and not self.closed:
            return True
        return False

    def write(self, *args):
        if self.writeable():
            self.io_obj.write(*args)
        else:
            raise OSError("write mode not indicated")

    def download_uri_with_load(self):
        if self.download_uri:
            return self.download_uri

        f = download(self.path, {}, self.options)
        self.set_attributes(f.get_attributes())
        return self.download_uri

    def download_content(self, io, is_string_io=False):
        Api.api_client().stream_download(
            self.download_uri_with_load(), io, is_string_io
        )

    def download_file(self, output_file):
        with builtin_open(output_file, "wb") as file:
            self.download_content(file)

    # Download file
    #
    # Parameters:
    #   action - string - Can be blank, `redirect` or `stat`.  If set to `stat`, we will return file information but without a download URL, and without logging a download.  If set to `redirect` we will serve a 302 redirect directly to the file.  This is used for integrations with Zapier, and is not recommended for most integrations.
    #   preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
    #   with_previews - boolean - Include file preview information?
    #   with_priority_color - boolean - Include file priority color information?
    def download(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params["path"] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
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
        response, _options = Api.send_request(
            "GET",
            "/files/{path}".format(path=params["path"]),
            params,
            self.options,
        )
        return response.data

    # Parameters:
    #   provided_mtime - string - Modified time of file.
    #   priority_color - string - Priority/Bookmark color of file.
    def update(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params["path"] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
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
        response, _options = Api.send_request(
            "PATCH",
            "/files/{path}".format(path=params["path"]),
            params,
            self.options,
        )
        return response.data

    # Parameters:
    #   recursive - boolean - If true, will recursively delete folers.  Otherwise, will error on non-empty folders.
    def delete(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params["path"] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        response, _options = Api.send_request(
            "DELETE",
            "/files/{path}".format(path=params["path"]),
            params,
            self.options,
        )
        return response.data

    def destroy(self, params=None):
        self.delete(params)

    # Copy file/folder
    #
    # Parameters:
    #   destination (required) - string - Copy destination path.
    #   structure - boolean - Copy structure only?
    def copy(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params["path"] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
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
        response, _options = Api.send_request(
            "POST",
            "/file_actions/copy/{path}".format(path=params["path"]),
            params,
            self.options,
        )
        return response.data

    # Move file/folder
    #
    # Parameters:
    #   destination (required) - string - Move destination path.
    def move(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params["path"] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
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
        response, _options = Api.send_request(
            "POST",
            "/file_actions/move/{path}".format(path=params["path"]),
            params,
            self.options,
        )
        return response.data

    # Begin file upload
    #
    # Parameters:
    #   mkdir_parents - boolean - Create parent directories if they do not exist?
    #   part - int64 - Part if uploading a part.
    #   parts - int64 - How many parts to fetch?
    #   ref - string -
    #   restart - int64 - File byte offset to restart from.
    #   size - int64 - Total bytes of file being uploaded (include bytes being retained if appending/restarting).
    #   with_rename - boolean - Allow file rename instead of overwrite?
    def begin_upload(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params["path"] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "part" in params and not isinstance(params["part"], int):
            raise InvalidParameterError("Bad parameter: part must be an int")
        if "parts" in params and not isinstance(params["parts"], int):
            raise InvalidParameterError("Bad parameter: parts must be an int")
        if "ref" in params and not isinstance(params["ref"], str):
            raise InvalidParameterError("Bad parameter: ref must be an str")
        if "restart" in params and not isinstance(params["restart"], int):
            raise InvalidParameterError(
                "Bad parameter: restart must be an int"
            )
        if "size" in params and not isinstance(params["size"], int):
            raise InvalidParameterError("Bad parameter: size must be an int")
        response, _options = Api.send_request(
            "POST",
            "/file_actions/begin_upload/{path}".format(path=params["path"]),
            params,
            self.options,
        )
        return response.data

    def save(self):
        new_obj = create(self.path, self.get_attributes(), self.options)
        self.set_attributes(new_obj.get_attributes())


# Download file
#
# Parameters:
#   action - string - Can be blank, `redirect` or `stat`.  If set to `stat`, we will return file information but without a download URL, and without logging a download.  If set to `redirect` we will serve a 302 redirect directly to the file.  This is used for integrations with Zapier, and is not recommended for most integrations.
#   preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
#   with_previews - boolean - Include file preview information?
#   with_priority_color - boolean - Include file priority color information?
def download(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
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
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request(
        "GET", "/files/{path}".format(path=params["path"]), params, options
    )
    return File(response.data, options)


# Parameters:
#   path (required) - string - Path to operate on.
#   action - string - The action to perform.  Can be `append`, `attachment`, `end`, `upload`, `put`, or may not exist
#   etags[etag] (required) - array(string) - etag identifier.
#   etags[part] (required) - array(int64) - Part number.
#   length - int64 - Length of file.
#   mkdir_parents - boolean - Create parent directories if they do not exist?
#   part - int64 - Part if uploading a part.
#   parts - int64 - How many parts to fetch?
#   provided_mtime - string - User provided modification time.
#   ref - string -
#   restart - int64 - File byte offset to restart from.
#   size - int64 - Size of file.
#   structure - string - If copying folder, copy just the structure?
#   with_rename - boolean - Allow file rename instead of overwrite?
def create(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "length" in params and not isinstance(params["length"], int):
        raise InvalidParameterError("Bad parameter: length must be an int")
    if "part" in params and not isinstance(params["part"], int):
        raise InvalidParameterError("Bad parameter: part must be an int")
    if "parts" in params and not isinstance(params["parts"], int):
        raise InvalidParameterError("Bad parameter: parts must be an int")
    if "provided_mtime" in params and not isinstance(
        params["provided_mtime"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provided_mtime must be an str"
        )
    if "ref" in params and not isinstance(params["ref"], str):
        raise InvalidParameterError("Bad parameter: ref must be an str")
    if "restart" in params and not isinstance(params["restart"], int):
        raise InvalidParameterError("Bad parameter: restart must be an int")
    if "size" in params and not isinstance(params["size"], int):
        raise InvalidParameterError("Bad parameter: size must be an int")
    if "structure" in params and not isinstance(params["structure"], str):
        raise InvalidParameterError("Bad parameter: structure must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request(
        "POST", "/files/{path}".format(path=params["path"]), params, options
    )
    return File(response.data, options)


# Parameters:
#   provided_mtime - string - Modified time of file.
#   priority_color - string - Priority/Bookmark color of file.
def update(path, params=None, options=None):
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
    if "priority_color" in params and not isinstance(
        params["priority_color"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: priority_color must be an str"
        )
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request(
        "PATCH", "/files/{path}".format(path=params["path"]), params, options
    )
    return File(response.data, options)


# Parameters:
#   recursive - boolean - If true, will recursively delete folers.  Otherwise, will error on non-empty folders.
def delete(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, _options = Api.send_request(
        "DELETE", "/files/{path}".format(path=params["path"]), params, options
    )
    return response.data


def destroy(path, params=None, options=None):
    delete(path, params, options)


# Parameters:
#   path (required) - string - Path to operate on.
#   preview_size - string - Request a preview size.  Can be `small` (default), `large`, `xlarge`, or `pdf`.
#   with_previews - boolean - Include file preview information?
#   with_priority_color - boolean - Include file priority color information?
def find(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "preview_size" in params and not isinstance(
        params["preview_size"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: preview_size must be an str"
        )
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request(
        "GET",
        "/file_actions/metadata/{path}".format(path=params["path"]),
        params,
        options,
    )
    return File(response.data, options)


def get(path, params=None, options=None):
    find(path, params, options)


# Copy file/folder
#
# Parameters:
#   destination (required) - string - Copy destination path.
#   structure - boolean - Copy structure only?
def copy(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "destination" in params and not isinstance(params["destination"], str):
        raise InvalidParameterError(
            "Bad parameter: destination must be an str"
        )
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    if "destination" not in params:
        raise MissingParameterError("Parameter missing: destination")
    response, options = Api.send_request(
        "POST",
        "/file_actions/copy/{path}".format(path=params["path"]),
        params,
        options,
    )
    return FileAction(response.data, options)


# Move file/folder
#
# Parameters:
#   destination (required) - string - Move destination path.
def move(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "destination" in params and not isinstance(params["destination"], str):
        raise InvalidParameterError(
            "Bad parameter: destination must be an str"
        )
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    if "destination" not in params:
        raise MissingParameterError("Parameter missing: destination")
    response, options = Api.send_request(
        "POST",
        "/file_actions/move/{path}".format(path=params["path"]),
        params,
        options,
    )
    return FileAction(response.data, options)


# Begin file upload
#
# Parameters:
#   mkdir_parents - boolean - Create parent directories if they do not exist?
#   part - int64 - Part if uploading a part.
#   parts - int64 - How many parts to fetch?
#   ref - string -
#   restart - int64 - File byte offset to restart from.
#   size - int64 - Total bytes of file being uploaded (include bytes being retained if appending/restarting).
#   with_rename - boolean - Allow file rename instead of overwrite?
def begin_upload(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "part" in params and not isinstance(params["part"], int):
        raise InvalidParameterError("Bad parameter: part must be an int")
    if "parts" in params and not isinstance(params["parts"], int):
        raise InvalidParameterError("Bad parameter: parts must be an int")
    if "ref" in params and not isinstance(params["ref"], str):
        raise InvalidParameterError("Bad parameter: ref must be an str")
    if "restart" in params and not isinstance(params["restart"], int):
        raise InvalidParameterError("Bad parameter: restart must be an int")
    if "size" in params and not isinstance(params["size"], int):
        raise InvalidParameterError("Bad parameter: size must be an int")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request(
        "POST",
        "/file_actions/begin_upload/{path}".format(path=params["path"]),
        params,
        options,
    )
    return [
        FileUploadPart(entity_data, options) for entity_data in response.data
    ]


def open(path, mode="r", options=None):
    if not isinstance(options, dict):
        options = {}
    file = File(path, mode, options)

    if "w" in mode:
        if "b" in mode:
            file.io_obj = io.BytesIO()
        else:
            file.io_obj = io.StringIO()

    if "r" in mode:
        if "b" in mode:
            file.io_obj = io.BytesIO()
        else:
            file.io_obj = io.StringIO()
    file.closed = False
    return file


def upload_chunks(io, path, options, upload=None, etags=None, params=None):
    if not etags:
        etags = []
    if not params:
        params = {}
    bytes_written = 0
    while True:
        chunk_params = (
            {"part": 1}
            if not upload
            else {"ref": upload.ref, "part": upload.part_number + 1}
        )
        params.update(chunk_params)
        upload = begin_upload(path, params, options)[0]
        buf = io.read(upload.partsize)
        if (buf == b"" or buf == "") and len(
            etags
        ) > 0:  # Empty bytearray means EOF for BytesIO, Empty String means EOF for StringIO
            return (upload, etags, bytes_written)
        if buf is not None:  # None means no data but io still open
            bytes_written += len(buf)
            response = Api.api_client().send_remote_request(
                upload.http_method,
                upload.upload_uri,
                {"Content-Length": str(len(buf))},
                buf,
            )
            if "ETag" in response.headers:
                etags.append(
                    {
                        "etag": response.headers["ETag"].strip('"'),
                        "part": upload.part_number,
                    }
                )


def upload_file(path, destination=None, options=None, params=None):
    if not isinstance(options, dict):
        options = {}
    pth = Path(path)
    stat = pth.stat()
    with builtin_open(path, "rb") as local_file:
        if destination is None:
            destination = pth.name
        upload, etags, _bytes_written = upload_chunks(
            local_file, destination, options, params=params
        )

        final_params = {
            "action": "end",
            "etags": etags,
            "provided_mtime": datetime.utcfromtimestamp(
                stat.st_mtime
            ).isoformat(),
            "ref": upload.ref,
            "size": stat.st_size,
        }

        create(destination, final_params, options)


def download_file(path, local_path=None, options=None):
    if not isinstance(options, dict):
        options = {}
    if local_path is None:
        local_path = Path(path).name
    return File(path, {}, options).download_file(local_path)


def new(*args, **kwargs):
    return File(*args, **kwargs)
