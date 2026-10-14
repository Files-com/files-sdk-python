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


class Action:
    """A action record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Action ID
        path: string - Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        when: date-time - Action occurrence date/time
        destination: string - The destination path for this action, if applicable
        display: string - Friendly displayed output
        ip: string - IP Address that performed this action
        source: string - The source path for this action, if applicable
        targets: object - Targets
        user_id: int64 - User ID
        username: string - Username
        user_is_from_parent_site: boolean - true if this change was performed by a user on a parent site.
        action: string - Type of action
        failure_type: string - Failure type. If action was a user login or session failure, why did it fail?
        interface: string - Interface on which this action occurred.
    """

    default_attributes = {
        "id": None,  # int64 - Action ID
        "path": None,  # string - Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "when": None,  # date-time - Action occurrence date/time
        "destination": None,  # string - The destination path for this action, if applicable
        "display": None,  # string - Friendly displayed output
        "ip": None,  # string - IP Address that performed this action
        "source": None,  # string - The source path for this action, if applicable
        "targets": None,  # object - Targets
        "user_id": None,  # int64 - User ID
        "username": None,  # string - Username
        "user_is_from_parent_site": None,  # boolean - true if this change was performed by a user on a parent site.
        "action": None,  # string - Type of action
        "failure_type": None,  # string - Failure type.  If action was a user login or session failure, why did it fail?
        "interface": None,  # string - Interface on which this action occurred.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    path: str | None
    when: str | None
    destination: str | None
    display: str | None
    ip: str | None
    source: str | None
    targets: dict[str, Any] | None
    user_id: int | None
    username: str | None
    user_is_from_parent_site: bool | None
    action: str | None
    failure_type: str | None
    interface: str | None

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
        for attribute, default_value in Action.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Action.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> Action:
    return Action(*args, **kwargs)
