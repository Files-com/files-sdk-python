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


class Request:
    """A request record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Request ID
        path: string - Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        source: string - Source filename, if applicable
        destination: string - Destination filename
        automation_id: int64 - ID of automation that created request
        user_display_name: string - User making the request (if applicable)
        user_ids: string - A list of user IDs to request the file from. If sent as a string, it should be comma-delimited.
        group_ids: string - A list of group IDs to request the file from. If sent as a string, it should be comma-delimited.
    """

    default_attributes = {
        "id": None,  # int64 - Request ID
        "path": None,  # string - Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "source": None,  # string - Source filename, if applicable
        "destination": None,  # string - Destination filename
        "automation_id": None,  # int64 - ID of automation that created request
        "user_display_name": None,  # string - User making the request (if applicable)
        "user_ids": None,  # string - A list of user IDs to request the file from. If sent as a string, it should be comma-delimited.
        "group_ids": None,  # string - A list of group IDs to request the file from. If sent as a string, it should be comma-delimited.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    path: str | None
    source: str | None
    destination: str | None
    automation_id: int | None
    user_display_name: str | None
    user_ids: str | None
    group_ids: str | None

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
        for attribute, default_value in Request.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Request.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE", "/requests/" + path_value(params["id"]), params
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Create this object on the server, taking in place the record it
        returns. One that already has an id cannot be updated, and raises
        NotImplementedError."""
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The Request object doesn't support updates."
            )
        else:
            new_obj = RequestResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class RequestResource:
    """Request operations that use one client's configuration.

    Get one from a client, such as ``client.request``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Request]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
        mine - boolean - Only show requests of the current user?  (Defaults to true if current user is not a site admin.)
        path - string - Path to show requests for.  If omitted, shows all paths. Send `/` to represent the root directory.
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
        if "mine" in params and not isinstance(params["mine"], bool):
            raise InvalidParameterError("Bad parameter: mine must be an bool")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        operation = Operation.start(self._scope, options)
        return ListObj(Request, "GET", "/requests", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Request]:
        """The same as list()."""
        return self.list(params, options)

    def get_folder(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Request]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
        mine - boolean - Only show requests of the current user?  (Defaults to true if current user is not a site admin.)
        path (required) - string - Path to show requests for.  If omitted, shows all paths. Send `/` to represent the root directory.
        """
        return self.__get_folder({"path": path}, params, options)

    def __get_folder(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ListObj[Request]:
        params = copy_params(params, path_values)
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
        if "mine" in params and not isinstance(params["mine"], bool):
            raise InvalidParameterError("Bad parameter: mine must be an bool")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        return ListObj(
            Request,
            "GET",
            "/requests/folders/" + path_value(params["path"]),
            params,
            operation,
        )

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Request:
        """Parameters:
        path (required) - string - Folder path on which to request the file.
        destination (required) - string - Destination filename (without extension) to request.
        user_ids - string - A list of user IDs to request the file from. If sent as a string, it should be comma-delimited.
        group_ids - string - A list of group IDs to request the file from. If sent as a string, it should be comma-delimited.
        """
        params = copy_params(params)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "user_ids" in params and not isinstance(params["user_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: user_ids must be an str"
            )
        if "group_ids" in params and not isinstance(params["group_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an str"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/requests", params)
        return operation.decode_model(response, Request)

    def delete(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        return self.__delete({"id": id}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE", "/requests/" + path_value(params["id"]), params
        )

    def destroy(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Request:
        """A new Request with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Request(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = RequestResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Request]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
    mine - boolean - Only show requests of the current user?  (Defaults to true if current user is not a site admin.)
    path - string - Path to show requests for.  If omitted, shows all paths. Send `/` to represent the root directory.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Request]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def get_folder(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Request]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
    mine - boolean - Only show requests of the current user?  (Defaults to true if current user is not a site admin.)
    path (required) - string - Path to show requests for.  If omitted, shows all paths. Send `/` to represent the root directory.
    """
    return _legacy_resource.get_folder(path, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Request:
    """Parameters:
    path (required) - string - Folder path on which to request the file.
    destination (required) - string - Destination filename (without extension) to request.
    user_ids - string - A list of user IDs to request the file from. If sent as a string, it should be comma-delimited.
    group_ids - string - A list of group IDs to request the file from. If sent as a string, it should be comma-delimited.
    """
    return _legacy_resource.create(params, options)


def delete(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    _legacy_resource.delete(id, params, options)


def destroy(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(id, params, options)


def new(*args, **kwargs) -> Request:
    return Request(*args, **kwargs)
