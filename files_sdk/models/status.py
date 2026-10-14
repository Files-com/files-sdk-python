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


class Status:
    """A status record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        code: int64 - Status HTTP code
        message: string - Error message
        status: string - Status message
        data: Auto - Additional data
        errors: array(object) - A list of api errors
        clickwrap_id: int64 - Required Clickwrap id
        clickwrap_body: string - Required Clickwrap body
    """

    default_attributes = {
        "code": None,  # int64 - Status HTTP code
        "message": None,  # string - Error message
        "status": None,  # string - Status message
        "data": None,  # Auto - Additional data
        "errors": None,  # array(object) - A list of api errors
        "clickwrap_id": None,  # int64 - Required Clickwrap id
        "clickwrap_body": None,  # string - Required Clickwrap body
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    code: int | None
    message: str | None
    status: str | None
    data: Any
    errors: builtins.list[dict[str, Any]] | None
    clickwrap_id: int | None
    clickwrap_body: str | None

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
        for attribute, default_value in Status.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Status.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> Status:
    return Status(*args, **kwargs)
