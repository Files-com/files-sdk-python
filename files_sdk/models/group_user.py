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


class GroupUser:
    """A group user record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        group_name: string - Group name
        group_id: int64 - Group ID
        user_id: int64 - User ID
        admin: boolean - Is this user an administrator of this group?
        username: string - Username of the user
        id: int64 - Group User ID.
    """

    default_attributes = {
        "group_name": None,  # string - Group name
        "group_id": None,  # int64 - Group ID
        "user_id": None,  # int64 - User ID
        "admin": None,  # boolean - Is this user an administrator of this group?
        "username": None,  # string - Username of the user
        "id": None,  # int64 - Group User ID.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    group_name: str | None
    group_id: int | None
    user_id: int | None
    admin: bool | None
    username: str | None
    id: int | None

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
        for attribute, default_value in GroupUser.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in GroupUser.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          group_id (required) - int64 - Group ID to add user to.
          user_id (required) - int64 - User ID to add to group.
          admin - boolean - Is the user a group administrator?
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "group_id" not in params:
            raise MissingParameterError("Parameter missing: group_id")
        if "user_id" not in params:
            raise MissingParameterError("Parameter missing: user_id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "admin" in params and isinstance(
            params["admin"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError("Bad parameter: admin must be an bool")
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/group_users/" + path_value(params["id"]), params
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        """Parameters:
        group_id (required) - int64 - Group ID from which to remove user.
        user_id (required) - int64 - User ID to remove from group.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "group_id" not in params:
            raise MissingParameterError("Parameter missing: group_id")
        if "user_id" not in params:
            raise MissingParameterError("Parameter missing: user_id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE", "/group_users/" + path_value(params["id"]), params
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Update this object on the server if it has an id, or else create
        it, taking in place the record the server returns."""
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = GroupUserResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class GroupUserResource:
    """GroupUser operations that use one client's configuration.

    Get one from a client, such as ``client.group_user``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[GroupUser]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        group_id - int64 - Group ID. If provided, returns memberships of this group. Requires a Site Administrator, a Read-only Administrator, a Workspace Administrator for the group's workspace, or a Group Administrator of this group.
        user_id - int64 - User ID.  If provided, will return group_users of this user.
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
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(GroupUser, "GET", "/group_users", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[GroupUser]:
        """The same as list()."""
        return self.list(params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> GroupUser:
        """Parameters:
        group_id (required) - int64 - Group ID to add user to.
        user_id (required) - int64 - User ID to add to group.
        admin - boolean - Is the user a group administrator?
        """
        params = copy_params(params)
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "admin" in params and not isinstance(params["admin"], bool):
            raise InvalidParameterError("Bad parameter: admin must be an bool")
        if "group_id" not in params:
            raise MissingParameterError("Parameter missing: group_id")
        if "user_id" not in params:
            raise MissingParameterError("Parameter missing: user_id")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/group_users", params)
        return operation.decode_model(response, GroupUser)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> GroupUser:
        """Parameters:
        group_id (required) - int64 - Group ID to add user to.
        user_id (required) - int64 - User ID to add to group.
        admin - boolean - Is the user a group administrator?
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> GroupUser:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "admin" in params and not isinstance(params["admin"], bool):
            raise InvalidParameterError("Bad parameter: admin must be an bool")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "group_id" not in params:
            raise MissingParameterError("Parameter missing: group_id")
        if "user_id" not in params:
            raise MissingParameterError("Parameter missing: user_id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/group_users/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, GroupUser)

    def delete(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Parameters:
        group_id (required) - int64 - Group ID from which to remove user.
        user_id (required) - int64 - User ID to remove from group.
        """
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
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "group_id" not in params:
            raise MissingParameterError("Parameter missing: group_id")
        if "user_id" not in params:
            raise MissingParameterError("Parameter missing: user_id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE", "/group_users/" + path_value(params["id"]), params
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
    ) -> GroupUser:
        """A new GroupUser with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = GroupUser(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = GroupUserResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[GroupUser]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    group_id - int64 - Group ID. If provided, returns memberships of this group. Requires a Site Administrator, a Read-only Administrator, a Workspace Administrator for the group's workspace, or a Group Administrator of this group.
    user_id - int64 - User ID.  If provided, will return group_users of this user.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[GroupUser]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> GroupUser:
    """Parameters:
    group_id (required) - int64 - Group ID to add user to.
    user_id (required) - int64 - User ID to add to group.
    admin - boolean - Is the user a group administrator?
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> GroupUser:
    """Parameters:
    group_id (required) - int64 - Group ID to add user to.
    user_id (required) - int64 - User ID to add to group.
    admin - boolean - Is the user a group administrator?
    """
    return _legacy_resource.update(id, params, options)


def delete(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Parameters:
    group_id (required) - int64 - Group ID from which to remove user.
    user_id (required) - int64 - User ID to remove from group.
    """
    _legacy_resource.delete(id, params, options)


def destroy(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(id, params, options)


def new(*args, **kwargs) -> GroupUser:
    return GroupUser(*args, **kwargs)
