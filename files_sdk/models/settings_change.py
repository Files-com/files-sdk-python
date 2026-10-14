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
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class SettingsChange:
    """A settings change record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        api_key_id: int64 - The API key id responsible for this change.
        changes: array(string) - Markdown-formatted change messages.
        created_at: date-time - The time this change was made.
        user_id: int64 - The user id responsible for this change.
        user_is_files_support: boolean - true if this change was performed by Files.com support.
        user_is_from_parent_site: boolean - true if this change was performed by a user on a parent site.
        username: string - The username of the user responsible for this change.
    """

    default_attributes = {
        "api_key_id": None,  # int64 - The API key id responsible for this change.
        "changes": None,  # array(string) - Markdown-formatted change messages.
        "created_at": None,  # date-time - The time this change was made.
        "user_id": None,  # int64 - The user id responsible for this change.
        "user_is_files_support": None,  # boolean - true if this change was performed by Files.com support.
        "user_is_from_parent_site": None,  # boolean - true if this change was performed by a user on a parent site.
        "username": None,  # string - The username of the user responsible for this change.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    api_key_id: int | None
    changes: builtins.list[str] | None
    created_at: str | None
    user_id: int | None
    user_is_files_support: bool | None
    user_is_from_parent_site: bool | None
    username: str | None

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
        ) in SettingsChange.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SettingsChange.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class SettingsChangeResource:
    """SettingsChange operations that use one client's configuration.

    Get one from a client, such as ``client.settings_change``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SettingsChange]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`, `api_key_id` or `user_id`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `api_key_id` and `user_id`.
        """
        params = copy_params(params)
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        if "sort_by" in params and not isinstance(params["sort_by"], dict):
            raise InvalidParameterError(
                "Bad parameter: sort_by must be an dict"
            )
        if "filter" in params and not isinstance(params["filter"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(
            SettingsChange, "GET", "/settings_changes", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SettingsChange]:
        """The same as list()."""
        return self.list(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SettingsChange:
        """A new SettingsChange with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = SettingsChange(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = SettingsChangeResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SettingsChange]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`, `api_key_id` or `user_id`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `api_key_id` and `user_id`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SettingsChange]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def new(*args, **kwargs) -> SettingsChange:
    return SettingsChange(*args, **kwargs)
