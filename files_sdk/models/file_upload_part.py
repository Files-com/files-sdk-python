import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
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


class FileUploadPart:
    """A file upload part record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        send: object - Content-Type and File to send
        action: string - Type of upload
        ask_about_overwrites: boolean - If `true`, this file exists and you may wish to ask the user for overwrite confirmation
        available_parts: int64 - Number of parts in the upload
        expires: string - Date/time of when this Upload part expires and the URL cannot be used any more
        headers: object - Additional upload headers to provide as part of the upload
        http_method: string - HTTP Method to use for uploading the part, usually `PUT`
        next_partsize: int64 - Size in bytes for this part
        parallel_parts: boolean - If `true`, multiple parts may be uploaded in parallel. If `false`, be sure to only upload one part at a time, in order.
        retry_parts: boolean - If `true`, parts may be retried. If `false`, a part cannot be retried and the upload should be restarted.
        parameters: object - Additional HTTP parameters to send with the upload
        part_number: int64 - Number of this upload part
        partsize: int64 - Size in bytes for the next upload part
        path: string - New file path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        ref: string - Reference name for this upload part
        upload_uri: string - URI to upload this part to
        direct_connection_info: DirectConnectionInfo - Optional direct connection information for direct Agent transfer attempts
    """

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
        "direct_connection_info": None,  # DirectConnectionInfo - Optional direct connection information for direct Agent transfer attempts
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    send: dict[str, Any] | None
    action: str | None
    ask_about_overwrites: bool | None
    available_parts: int | None
    expires: str | None
    headers: dict[str, Any] | None
    http_method: str | None
    next_partsize: int | None
    parallel_parts: bool | None
    retry_parts: bool | None
    parameters: dict[str, Any] | None
    part_number: int | None
    partsize: int | None
    path: str | None
    ref: str | None
    upload_uri: str | None
    direct_connection_info: dict[str, Any] | None

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
        for (
            attribute,
            default_value,
        ) in FileUploadPart.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in FileUploadPart.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> FileUploadPart:
    return FileUploadPart(*args, **kwargs)
