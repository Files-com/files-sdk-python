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


class AgentPushUpdate:
    """A agent push update record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        version: string - Pushed agent version
        message: string - Update accepted or reason
        current_version: string - Installed agent version
        pending_version: string - Pending agent version or null
        last_error: string - Last error message or null
        error: string - Error code
    """

    default_attributes = {
        "version": None,  # string - Pushed agent version
        "message": None,  # string - Update accepted or reason
        "current_version": None,  # string - Installed agent version
        "pending_version": None,  # string - Pending agent version or null
        "last_error": None,  # string - Last error message or null
        "error": None,  # string - Error code
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    version: str | None
    message: str | None
    current_version: str | None
    pending_version: str | None
    last_error: str | None
    error: str | None

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
        ) in AgentPushUpdate.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in AgentPushUpdate.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> AgentPushUpdate:
    return AgentPushUpdate(*args, **kwargs)
