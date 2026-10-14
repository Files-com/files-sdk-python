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


class Permission:
    """A permission record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Permission ID
        path: string - Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        user_id: int64 - User ID
        username: string - Username (if applicable)
        group_id: int64 - Group ID
        group_name: string - Group name (if applicable)
        group_ids: array(int64) - Group IDs when this Permission requires membership in every listed group.
        group_names: array(string) - Group names when this permission requires multiple groups
        partner_id: int64 - Partner ID (if applicable)
        partner_name: string - Partner name (if applicable)
        permission: string - Permission type. See the table referenced in the documentation for an explanation of each permission.
        recursive: boolean - Whether this Permission applies to subfolders. Must be true for `admin` Permissions.
        site_id: int64 - Site ID
    """

    default_attributes = {
        "id": None,  # int64 - Permission ID
        "path": None,  # string - Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "user_id": None,  # int64 - User ID
        "username": None,  # string - Username (if applicable)
        "group_id": None,  # int64 - Group ID
        "group_name": None,  # string - Group name (if applicable)
        "group_ids": None,  # array(int64) - Group IDs when this Permission requires membership in every listed group.
        "group_names": None,  # array(string) - Group names when this permission requires multiple groups
        "partner_id": None,  # int64 - Partner ID (if applicable)
        "partner_name": None,  # string - Partner name (if applicable)
        "permission": None,  # string - Permission type.  See the table referenced in the documentation for an explanation of each permission.
        "recursive": None,  # boolean - Whether this Permission applies to subfolders. Must be true for `admin` Permissions.
        "site_id": None,  # int64 - Site ID
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    path: str | None
    user_id: int | None
    username: str | None
    group_id: int | None
    group_name: str | None
    group_ids: builtins.list[int] | None
    group_names: builtins.list[str] | None
    partner_id: int | None
    partner_name: str | None
    permission: str | None
    recursive: bool | None
    site_id: int | None

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
        for attribute, default_value in Permission.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Permission.default_attributes
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
            "DELETE", "/permissions/" + path_value(params["id"]), params
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
                "The Permission object doesn't support updates."
            )
        else:
            new_obj = PermissionResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class PermissionResource:
    """Permission operations that use one client's configuration.

    Get one from a client, such as ``client.permission``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Permission]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `group_id`, `path`, `user_id`, `partner_id` or `id`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `path`, `group_id`, `partner_id` or `user_id`. Valid field combinations are `[ group_id, path ]`, `[ partner_id, path ]`, `[ user_id, path ]`, `[ user_id, group_id ]`, `[ user_id, group_id, path ]`, `[ user_id, group_id, partner_id ]` or `[ user_id, group_id, partner_id, path ]`.
        filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.
        path - string - Permission path.  If provided, will scope all permissions(including upward) to this path.
        include_groups - boolean - If searching by user or group, also include user's permissions that are inherited from its groups?
        group_id - string
        partner_id - string
        user_id - string
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
        if "filter_prefix" in params and not isinstance(
            params["filter_prefix"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_prefix must be an dict"
            )
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "include_groups" in params and not isinstance(
            params["include_groups"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: include_groups must be an bool"
            )
        if "group_id" in params and not isinstance(params["group_id"], str):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an str"
            )
        if "partner_id" in params and not isinstance(
            params["partner_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_id must be an str"
            )
        if "user_id" in params and not isinstance(params["user_id"], str):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an str"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(Permission, "GET", "/permissions", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Permission]:
        """The same as list()."""
        return self.list(params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Permission:
        """Parameters:
        path (required) - string - Folder path
        group_id - int64 - Group ID. Provide `group_name` or `group_id`
        group_ids - string - Group IDs when the Permission requires membership in every listed group. If sent as a string, it should be comma-delimited.
        permission - string - Permission type.  Can be `admin`, `full`, `readonly`, `writeonly`, `list`, or `history`
        recursive - boolean - Apply to subfolders recursively? Must be true for `admin` Permissions.
        partner_id - int64 - Partner ID if this Permission belongs to a partner.
        user_id - int64 - User ID.  Provide `username` or `user_id`
        username - string - User username.  Provide `username` or `user_id`
        group_name - string - Group name.  Provide `group_name` or `group_id`
        site_id - int64 - Site ID. If not provided, will default to current site. Used when creating a permission for a child site.
        """
        params = copy_params(params)
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "group_ids" in params and not isinstance(params["group_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an str"
            )
        if "permission" in params and not isinstance(
            params["permission"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: permission must be an str"
            )
        if "recursive" in params and not isinstance(params["recursive"], bool):
            raise InvalidParameterError(
                "Bad parameter: recursive must be an bool"
            )
        if "partner_id" in params and (
            not isinstance(params["partner_id"], int)
            or isinstance(params["partner_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_id must be an int"
            )
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "username" in params and not isinstance(params["username"], str):
            raise InvalidParameterError(
                "Bad parameter: username must be an str"
            )
        if "group_name" in params and not isinstance(
            params["group_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: group_name must be an str"
            )
        if "site_id" in params and (
            not isinstance(params["site_id"], int)
            or isinstance(params["site_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: site_id must be an int"
            )
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/permissions", params)
        return operation.decode_model(response, Permission)

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
            "DELETE", "/permissions/" + path_value(params["id"]), params
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
    ) -> Permission:
        """A new Permission with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Permission(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = PermissionResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Permission]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `group_id`, `path`, `user_id`, `partner_id` or `id`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `path`, `group_id`, `partner_id` or `user_id`. Valid field combinations are `[ group_id, path ]`, `[ partner_id, path ]`, `[ user_id, path ]`, `[ user_id, group_id ]`, `[ user_id, group_id, path ]`, `[ user_id, group_id, partner_id ]` or `[ user_id, group_id, partner_id, path ]`.
    filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.
    path - string - Permission path.  If provided, will scope all permissions(including upward) to this path.
    include_groups - boolean - If searching by user or group, also include user's permissions that are inherited from its groups?
    group_id - string
    partner_id - string
    user_id - string
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Permission]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Permission:
    """Parameters:
    path (required) - string - Folder path
    group_id - int64 - Group ID. Provide `group_name` or `group_id`
    group_ids - string - Group IDs when the Permission requires membership in every listed group. If sent as a string, it should be comma-delimited.
    permission - string - Permission type.  Can be `admin`, `full`, `readonly`, `writeonly`, `list`, or `history`
    recursive - boolean - Apply to subfolders recursively? Must be true for `admin` Permissions.
    partner_id - int64 - Partner ID if this Permission belongs to a partner.
    user_id - int64 - User ID.  Provide `username` or `user_id`
    username - string - User username.  Provide `username` or `user_id`
    group_name - string - Group name.  Provide `group_name` or `group_id`
    site_id - int64 - Site ID. If not provided, will default to current site. Used when creating a permission for a child site.
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


def new(*args, **kwargs) -> Permission:
    return Permission(*args, **kwargs)
