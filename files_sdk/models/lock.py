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


class Lock:
    """A lock record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        path: string - Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        timeout: int64 - Lock timeout in seconds
        depth: string
        recursive: boolean - Does lock apply to subfolders?
        owner: string - Arbitrary descriptive label for the lock. Does not change the lock creator or permissions.
        scope: string
        exclusive: boolean - Is lock exclusive?
        token: string - Lock token. Use to release lock.
        type: string
        allow_access_by_any_user: boolean - Can lock be modified by users other than its creator?
        user_id: int64 - Lock creator user ID
        username: string - Lock creator username
        expected_token: string - Require this existing, unexpired token before refreshing or replacing a lock. Set token to the same value to refresh, or a different value to replace.
    """

    default_attributes = {
        "path": None,  # string - Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "timeout": None,  # int64 - Lock timeout in seconds
        "depth": None,  # string
        "recursive": None,  # boolean - Does lock apply to subfolders?
        "owner": None,  # string - Arbitrary descriptive label for the lock. Does not change the lock creator or permissions.
        "scope": None,  # string
        "exclusive": None,  # boolean - Is lock exclusive?
        "token": None,  # string - Lock token.  Use to release lock.
        "type": None,  # string
        "allow_access_by_any_user": None,  # boolean - Can lock be modified by users other than its creator?
        "user_id": None,  # int64 - Lock creator user ID
        "username": None,  # string - Lock creator username
        "expected_token": None,  # string - Require this existing, unexpired token before refreshing or replacing a lock. Set token to the same value to refresh, or a different value to replace.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    path: str | None
    timeout: int | None
    depth: str | None
    recursive: bool | None
    owner: str | None
    scope: str | None
    exclusive: bool | None
    token: str | None
    type: str | None
    allow_access_by_any_user: bool | None
    user_id: int | None
    username: str | None
    expected_token: str | None

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
        for attribute, default_value in Lock.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Lock.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        """Parameters:
        token (required) - string - Lock token
        """
        if not (hasattr(self, "path") and self.path):
            raise MissingParameterError("Current object doesn't have a path")
        params = copy_params(params, {"path": self.path})
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "token" not in params:
            raise MissingParameterError("Parameter missing: token")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "token" in params and not isinstance(params["token"], str):
            raise InvalidParameterError("Bad parameter: token must be an str")
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE", "/locks/" + path_value(params["path"]), params
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Create this object on the server, taking in place the record it
        returns."""
        new_obj = LockResource(self._scope()).create(
            getattr(self, "path"), self.get_attributes()
        )
        self.set_attributes(new_obj.get_attributes())
        self._context = new_obj._context


class LockResource:
    """Lock operations that use one client's configuration.

    Get one from a client, such as ``client.lock``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list_for(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Lock]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        path (required) - string - Path to operate on.
        include_children - boolean - Include locks from children objects?
        """
        return self.__list_for({"path": path}, params, options)

    def __list_for(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ListObj[Lock]:
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
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "include_children" in params and not isinstance(
            params["include_children"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: include_children must be an bool"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        return ListObj(
            Lock,
            "GET",
            "/locks/" + path_value(params["path"]),
            params,
            operation,
        )

    def create(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Lock:
        """Parameters:
        path (required) - string - Path
        token - string - Lock token. With expected_token, use the same value to refresh or a different value to replace the existing token.
        expected_token - string - Require this existing, unexpired token before refreshing or replacing a lock. Set token to the same value to refresh, or a different value to replace.
        allow_access_by_any_user - boolean - Can lock be modified by users other than its creator?
        exclusive - boolean - Is lock exclusive?
        recursive - boolean - Does lock apply to subfolders?
        owner - string - Arbitrary descriptive label for the lock. Does not change the lock creator or permissions.
        timeout - int64 - Lock timeout in seconds
        """
        return self.__create({"path": path}, params, options)

    def __create(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Lock:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "token" in params and not isinstance(params["token"], str):
            raise InvalidParameterError("Bad parameter: token must be an str")
        if "expected_token" in params and not isinstance(
            params["expected_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: expected_token must be an str"
            )
        if "allow_access_by_any_user" in params and not isinstance(
            params["allow_access_by_any_user"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: allow_access_by_any_user must be an bool"
            )
        if "exclusive" in params and not isinstance(params["exclusive"], bool):
            raise InvalidParameterError(
                "Bad parameter: exclusive must be an bool"
            )
        if "recursive" in params and not isinstance(params["recursive"], bool):
            raise InvalidParameterError(
                "Bad parameter: recursive must be an bool"
            )
        if "owner" in params and not isinstance(params["owner"], str):
            raise InvalidParameterError("Bad parameter: owner must be an str")
        if "timeout" in params and (
            not isinstance(params["timeout"], int)
            or isinstance(params["timeout"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: timeout must be an int"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST", "/locks/" + path_value(params["path"]), params
        )
        return operation.decode_model(response, Lock)

    def delete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Parameters:
        token (required) - string - Lock token
        """
        return self.__delete({"path": path}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "token" in params and not isinstance(params["token"], str):
            raise InvalidParameterError("Bad parameter: token must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "token" not in params:
            raise MissingParameterError("Parameter missing: token")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE", "/locks/" + path_value(params["path"]), params
        )

    def destroy(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(path, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Lock:
        """A new Lock with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Lock(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = LockResource(LEGACY)


def list_for(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Lock]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    path (required) - string - Path to operate on.
    include_children - boolean - Include locks from children objects?
    """
    return _legacy_resource.list_for(path, params, options)


def create(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Lock:
    """Parameters:
    path (required) - string - Path
    token - string - Lock token. With expected_token, use the same value to refresh or a different value to replace the existing token.
    expected_token - string - Require this existing, unexpired token before refreshing or replacing a lock. Set token to the same value to refresh, or a different value to replace.
    allow_access_by_any_user - boolean - Can lock be modified by users other than its creator?
    exclusive - boolean - Is lock exclusive?
    recursive - boolean - Does lock apply to subfolders?
    owner - string - Arbitrary descriptive label for the lock. Does not change the lock creator or permissions.
    timeout - int64 - Lock timeout in seconds
    """
    return _legacy_resource.create(path, params, options)


def delete(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Parameters:
    token (required) - string - Lock token
    """
    _legacy_resource.delete(path, params, options)


def destroy(
    path: str,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(path, params, options)


def new(*args, **kwargs) -> Lock:
    return Lock(*args, **kwargs)
