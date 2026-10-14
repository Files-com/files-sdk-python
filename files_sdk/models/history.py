import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.models.action import Action
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


class History:
    """A history record from the Files.com API.

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
        for attribute, default_value in History.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in History.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class HistoryResource:
    """History operations that use one client's configuration.

    Get one from a client, such as ``client.history``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list_for_file(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Action]:
        """Parameters:
        start_at - string - Leave blank or set to a date/time to filter earlier entries.
        end_at - string - Leave blank or set to a date/time to filter later entries.
        display - string - Display format. Leave blank or set to `full` or `parent`.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
        path (required) - string - Path to operate on.
        """
        return self.__list_for_file({"path": path}, params, options)

    def __list_for_file(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ListObj[Action]:
        params = copy_params(params, path_values)
        if "start_at" in params and not isinstance(params["start_at"], str):
            raise InvalidParameterError(
                "Bad parameter: start_at must be an str"
            )
        if "end_at" in params and not isinstance(params["end_at"], str):
            raise InvalidParameterError("Bad parameter: end_at must be an str")
        if "display" in params and not isinstance(params["display"], str):
            raise InvalidParameterError(
                "Bad parameter: display must be an str"
            )
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
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        return ListObj(
            Action,
            "GET",
            "/history/files/" + path_value(params["path"]),
            params,
            operation,
        )

    def list_for_folder(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Action]:
        """Parameters:
        start_at - string - Leave blank or set to a date/time to filter earlier entries.
        end_at - string - Leave blank or set to a date/time to filter later entries.
        display - string - Display format. Leave blank or set to `full` or `parent`.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
        path (required) - string - Path to operate on.
        """
        return self.__list_for_folder({"path": path}, params, options)

    def __list_for_folder(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ListObj[Action]:
        params = copy_params(params, path_values)
        if "start_at" in params and not isinstance(params["start_at"], str):
            raise InvalidParameterError(
                "Bad parameter: start_at must be an str"
            )
        if "end_at" in params and not isinstance(params["end_at"], str):
            raise InvalidParameterError("Bad parameter: end_at must be an str")
        if "display" in params and not isinstance(params["display"], str):
            raise InvalidParameterError(
                "Bad parameter: display must be an str"
            )
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
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        return ListObj(
            Action,
            "GET",
            "/history/folders/" + path_value(params["path"]),
            params,
            operation,
        )

    def list_for_user(
        self,
        user_id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Action]:
        """Parameters:
        start_at - string - Leave blank or set to a date/time to filter earlier entries.
        end_at - string - Leave blank or set to a date/time to filter later entries.
        display - string - Display format. Leave blank or set to `full` or `parent`.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
        user_id (required) - int64 - User ID.
        """
        return self.__list_for_user({"user_id": user_id}, params, options)

    def __list_for_user(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ListObj[Action]:
        params = copy_params(params, path_values)
        if "start_at" in params and not isinstance(params["start_at"], str):
            raise InvalidParameterError(
                "Bad parameter: start_at must be an str"
            )
        if "end_at" in params and not isinstance(params["end_at"], str):
            raise InvalidParameterError("Bad parameter: end_at must be an str")
        if "display" in params and not isinstance(params["display"], str):
            raise InvalidParameterError(
                "Bad parameter: display must be an str"
            )
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
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "user_id" not in params:
            raise MissingParameterError("Parameter missing: user_id")
        operation = Operation.start(self._scope, options)
        return ListObj(
            Action,
            "GET",
            "/history/users/" + path_value(params["user_id"]),
            params,
            operation,
        )

    def list_logins(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Action]:
        """Parameters:
        start_at - string - Leave blank or set to a date/time to filter earlier entries.
        end_at - string - Leave blank or set to a date/time to filter later entries.
        display - string - Display format. Leave blank or set to `full` or `parent`.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
        """
        params = copy_params(params)
        if "start_at" in params and not isinstance(params["start_at"], str):
            raise InvalidParameterError(
                "Bad parameter: start_at must be an str"
            )
        if "end_at" in params and not isinstance(params["end_at"], str):
            raise InvalidParameterError("Bad parameter: end_at must be an str")
        if "display" in params and not isinstance(params["display"], str):
            raise InvalidParameterError(
                "Bad parameter: display must be an str"
            )
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
        operation = Operation.start(self._scope, options)
        return ListObj(Action, "GET", "/history/login", params, operation)

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Action]:
        """Parameters:
        start_at - string - Leave blank or set to a date/time to filter earlier entries.
        end_at - string - Leave blank or set to a date/time to filter later entries.
        display - string - Display format. Leave blank or set to `full` or `parent`.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `user_id`, `folder` or `path`. Valid field combinations are `[  ]`, `[ path ]`, `[ path ]` or `[ path ]`.
        filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.
        """
        params = copy_params(params)
        if "start_at" in params and not isinstance(params["start_at"], str):
            raise InvalidParameterError(
                "Bad parameter: start_at must be an str"
            )
        if "end_at" in params and not isinstance(params["end_at"], str):
            raise InvalidParameterError("Bad parameter: end_at must be an str")
        if "display" in params and not isinstance(params["display"], str):
            raise InvalidParameterError(
                "Bad parameter: display must be an str"
            )
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
        if "filter_prefix" in params and not isinstance(
            params["filter_prefix"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_prefix must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(Action, "GET", "/history", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Action]:
        """The same as list()."""
        return self.list(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> History:
        """A new History with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = History(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = HistoryResource(LEGACY)


def list_for_file(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Action]:
    """Parameters:
    start_at - string - Leave blank or set to a date/time to filter earlier entries.
    end_at - string - Leave blank or set to a date/time to filter later entries.
    display - string - Display format. Leave blank or set to `full` or `parent`.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
    path (required) - string - Path to operate on.
    """
    return _legacy_resource.list_for_file(path, params, options)


def list_for_folder(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Action]:
    """Parameters:
    start_at - string - Leave blank or set to a date/time to filter earlier entries.
    end_at - string - Leave blank or set to a date/time to filter later entries.
    display - string - Display format. Leave blank or set to `full` or `parent`.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
    path (required) - string - Path to operate on.
    """
    return _legacy_resource.list_for_folder(path, params, options)


def list_for_user(
    user_id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Action]:
    """Parameters:
    start_at - string - Leave blank or set to a date/time to filter earlier entries.
    end_at - string - Leave blank or set to a date/time to filter later entries.
    display - string - Display format. Leave blank or set to `full` or `parent`.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
    user_id (required) - int64 - User ID.
    """
    return _legacy_resource.list_for_user(user_id, params, options)


def list_logins(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Action]:
    """Parameters:
    start_at - string - Leave blank or set to a date/time to filter earlier entries.
    end_at - string - Leave blank or set to a date/time to filter later entries.
    display - string - Display format. Leave blank or set to `full` or `parent`.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
    """
    return _legacy_resource.list_logins(params, options)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Action]:
    """Parameters:
    start_at - string - Leave blank or set to a date/time to filter earlier entries.
    end_at - string - Leave blank or set to a date/time to filter later entries.
    display - string - Display format. Leave blank or set to `full` or `parent`.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `user_id`, `folder` or `path`. Valid field combinations are `[  ]`, `[ path ]`, `[ path ]` or `[ path ]`.
    filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Action]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def new(*args, **kwargs) -> History:
    return History(*args, **kwargs)
