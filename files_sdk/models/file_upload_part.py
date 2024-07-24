import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class FileUploadPart:
    default_attributes = {
        "send": None,  # object - Content-Type and File to send
        "action": None,  # string - Type of upload
        "ask_about_overwrites": None,  # boolean - If `true`, this file exists and you may wish to ask the user for overwrite confirmation
        "available_parts": None,  # int64 - Number of parts in the upload
        "expires": None,  # string - Date/time of when this Upload part expires and the URL cannot be used any more
        "headers": None,  # object - Additional upload headers to provide as part of the upload
        "http_method": None,  # string - HTTP Method to use for uploading the part, usually `PUT`
        "next_partsize": None,  # int64 - Size in bytes for this part
        "parallel_parts": None,  # boolean - If `true`, multiple parts may be uploaded in parallel.  If `false`, be sure to only upload one part at a time, in order.
        "retry_parts": None,  # boolean - If `true`, parts may be retried. If `false`, a part cannot be retried and the upload should be restarted.
        "parameters": None,  # object - Additional HTTP parameters to send with the upload
        "part_number": None,  # int64 - Number of this upload part
        "partsize": None,  # int64 - Size in bytes for the next upload part
        "path": None,  # string - New file path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "ref": None,  # string - Reference name for this upload part
        "upload_uri": None,  # string - URI to upload this part to
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (
            attribute,
            default_value,
        ) in FileUploadPart.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in FileUploadPart.default_attributes
            if getattr(self, k, None) is not None
        }


def new(*args, **kwargs):
    return FileUploadPart(*args, **kwargs)
