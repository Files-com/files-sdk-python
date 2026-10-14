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


class Preview:
    """A preview record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Preview ID
        status: string - Preview status. Can be invalid, not_generated, generating, complete, or file_too_large
        download_uri: string - Link to download preview
        type: string - Preview type. Can be image, pdf, pdf_native, video, audio, or text
        size: string - Preview size
    """

    default_attributes = {
        "id": None,  # int64 - Preview ID
        "status": None,  # string - Preview status.  Can be invalid, not_generated, generating, complete, or file_too_large
        "download_uri": None,  # string - Link to download preview
        "type": None,  # string - Preview type. Can be image, pdf, pdf_native, video, audio, or text
        "size": None,  # string - Preview size
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    status: str | None
    download_uri: str | None
    type: str | None
    size: str | None

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
        for attribute, default_value in Preview.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Preview.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> Preview:
    return Preview(*args, **kwargs)
