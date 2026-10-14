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


class UserRequest:
    """A user request record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - ID
        name: string - User's full name
        email: email - User email address
        details: string - Details of the user's request
        company: string - User's company name
    """

    default_attributes = {
        "id": None,  # int64 - ID
        "name": None,  # string - User's full name
        "email": None,  # email - User email address
        "details": None,  # string - Details of the user's request
        "company": None,  # string - User's company name
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    name: str | None
    email: str | None
    details: str | None
    company: str | None

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
        for attribute, default_value in UserRequest.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in UserRequest.default_attributes
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
            "DELETE", "/user_requests/" + path_value(params["id"]), params
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
                "The UserRequest object doesn't support updates."
            )
        else:
            new_obj = UserRequestResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class UserRequestResource:
    """UserRequest operations that use one client's configuration.

    Get one from a client, such as ``client.user_request``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[UserRequest]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
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
        operation = Operation.start(self._scope, options)
        return ListObj(UserRequest, "GET", "/user_requests", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[UserRequest]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> UserRequest:
        """Parameters:
        id (required) - int64 - User Request ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> UserRequest:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/user_requests/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, UserRequest)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> UserRequest:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> UserRequest:
        """Parameters:
        name (required) - string - Name of user requested
        email (required) - string - Email of user requested
        details (required) - string - Details of the user request
        company - string - Company of the user requested
        """
        params = copy_params(params)
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "email" in params and not isinstance(params["email"], str):
            raise InvalidParameterError("Bad parameter: email must be an str")
        if "details" in params and not isinstance(params["details"], str):
            raise InvalidParameterError(
                "Bad parameter: details must be an str"
            )
        if "company" in params and not isinstance(params["company"], str):
            raise InvalidParameterError(
                "Bad parameter: company must be an str"
            )
        if "name" not in params:
            raise MissingParameterError("Parameter missing: name")
        if "email" not in params:
            raise MissingParameterError("Parameter missing: email")
        if "details" not in params:
            raise MissingParameterError("Parameter missing: details")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/user_requests", params)
        return operation.decode_model(response, UserRequest)

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
            "DELETE", "/user_requests/" + path_value(params["id"]), params
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
    ) -> UserRequest:
        """A new UserRequest with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = UserRequest(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = UserRequestResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[UserRequest]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[UserRequest]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> UserRequest:
    """Parameters:
    id (required) - int64 - User Request ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> UserRequest:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> UserRequest:
    """Parameters:
    name (required) - string - Name of user requested
    email (required) - string - Email of user requested
    details (required) - string - Details of the user request
    company - string - Company of the user requested
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


def new(*args, **kwargs) -> UserRequest:
    return UserRequest(*args, **kwargs)
