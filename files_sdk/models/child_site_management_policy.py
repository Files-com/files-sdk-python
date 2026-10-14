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


class ChildSiteManagementPolicy:
    """A child site management policy record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Policy ID.
        policy_type: string - Type of policy. Valid values: `settings`.
        name: string - Name for this policy.
        description: string - Description for this policy.
        value: object - Policy configuration data. On a Child Site, contains only managed setting names with null values. Settings policies accept site settings plus an optional `folder_behaviors` array for parent-managed root behaviors on child sites. For more information, refer to the Value Hash section of the developer documentation.
        applied_child_site_ids: array(int64) - IDs of child sites that this policy has been applied to. This field is read-only.
        skip_child_site_ids: array(int64) - IDs of child sites excluded from this default policy.
        child_site_ids: array(int64) - IDs of child sites explicitly assigned to this non-default policy.
        default_policy: boolean - Whether this policy applies to child sites not explicitly assigned to another policy.
        created_at: date-time - When this policy was created.
        updated_at: date-time - When this policy was last updated.
    """

    default_attributes = {
        "id": None,  # int64 - Policy ID.
        "policy_type": None,  # string - Type of policy.  Valid values: `settings`.
        "name": None,  # string - Name for this policy.
        "description": None,  # string - Description for this policy.
        "value": None,  # object - Policy configuration data. On a Child Site, contains only managed setting names with null values. Settings policies accept site settings plus an optional `folder_behaviors` array for parent-managed root behaviors on child sites. For more information, refer to the Value Hash section of the developer documentation.
        "applied_child_site_ids": None,  # array(int64) - IDs of child sites that this policy has been applied to. This field is read-only.
        "skip_child_site_ids": None,  # array(int64) - IDs of child sites excluded from this default policy.
        "child_site_ids": None,  # array(int64) - IDs of child sites explicitly assigned to this non-default policy.
        "default_policy": None,  # boolean - Whether this policy applies to child sites not explicitly assigned to another policy.
        "created_at": None,  # date-time - When this policy was created.
        "updated_at": None,  # date-time - When this policy was last updated.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    policy_type: str | None
    name: str | None
    description: str | None
    value: dict[str, Any] | None
    applied_child_site_ids: builtins.list[int] | None
    skip_child_site_ids: builtins.list[int] | None
    child_site_ids: builtins.list[int] | None
    default_policy: bool | None
    created_at: str | None
    updated_at: str | None

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
        ) in ChildSiteManagementPolicy.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ChildSiteManagementPolicy.default_attributes
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
          value - object - Policy configuration data. Attributes differ by policy type. For more information, refer to the Value Hash section of the developer documentation.
          skip_child_site_ids - array(int64) - IDs of child sites excluded from this default policy.
          child_site_ids - array(int64) - IDs of child sites explicitly assigned to this non-default policy.
          default_policy - boolean - Whether this policy applies to child sites not explicitly assigned to another policy.
          policy_type - string - Type of policy.  Valid values: `settings`.
          name - string - Name for this policy.
          description - string - Description for this policy.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "skip_child_site_ids" in params and not isinstance(
            params["skip_child_site_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_child_site_ids must be an list"
            )
        if "child_site_ids" in params and not isinstance(
            params["child_site_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: child_site_ids must be an list"
            )
        if "default_policy" in params and isinstance(
            params["default_policy"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: default_policy must be an bool"
            )
        if "policy_type" in params and not isinstance(
            params["policy_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: policy_type must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH",
            "/child_site_management_policies/" + path_value(params["id"]),
            params,
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

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
            "DELETE",
            "/child_site_management_policies/" + path_value(params["id"]),
            params,
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
            new_obj = ChildSiteManagementPolicyResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class ChildSiteManagementPolicyResource:
    """ChildSiteManagementPolicy operations that use one client's configuration.

    Get one from a client, such as ``client.child_site_management_policy``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[ChildSiteManagementPolicy]:
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
        return ListObj(
            ChildSiteManagementPolicy,
            "GET",
            "/child_site_management_policies",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[ChildSiteManagementPolicy]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ChildSiteManagementPolicy:
        """Parameters:
        id (required) - int64 - Child Site Management Policy ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ChildSiteManagementPolicy:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET",
            "/child_site_management_policies/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, ChildSiteManagementPolicy)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ChildSiteManagementPolicy:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ChildSiteManagementPolicy:
        """Parameters:
        value - object - Policy configuration data. Attributes differ by policy type. For more information, refer to the Value Hash section of the developer documentation.
        skip_child_site_ids - array(int64) - IDs of child sites excluded from this default policy.
        child_site_ids - array(int64) - IDs of child sites explicitly assigned to this non-default policy.
        default_policy - boolean - Whether this policy applies to child sites not explicitly assigned to another policy.
        policy_type (required) - string - Type of policy.  Valid values: `settings`.
        name - string - Name for this policy.
        description - string - Description for this policy.
        """
        params = copy_params(params)
        if "value" in params and not isinstance(params["value"], dict):
            raise InvalidParameterError("Bad parameter: value must be an dict")
        if "skip_child_site_ids" in params and not isinstance(
            params["skip_child_site_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_child_site_ids must be an list"
            )
        if "child_site_ids" in params and not isinstance(
            params["child_site_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: child_site_ids must be an list"
            )
        if "default_policy" in params and not isinstance(
            params["default_policy"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: default_policy must be an bool"
            )
        if "policy_type" in params and not isinstance(
            params["policy_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: policy_type must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "policy_type" not in params:
            raise MissingParameterError("Parameter missing: policy_type")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST", "/child_site_management_policies", params
        )
        return operation.decode_model(response, ChildSiteManagementPolicy)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ChildSiteManagementPolicy:
        """Parameters:
        value - object - Policy configuration data. Attributes differ by policy type. For more information, refer to the Value Hash section of the developer documentation.
        skip_child_site_ids - array(int64) - IDs of child sites excluded from this default policy.
        child_site_ids - array(int64) - IDs of child sites explicitly assigned to this non-default policy.
        default_policy - boolean - Whether this policy applies to child sites not explicitly assigned to another policy.
        policy_type - string - Type of policy.  Valid values: `settings`.
        name - string - Name for this policy.
        description - string - Description for this policy.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ChildSiteManagementPolicy:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "value" in params and not isinstance(params["value"], dict):
            raise InvalidParameterError("Bad parameter: value must be an dict")
        if "skip_child_site_ids" in params and not isinstance(
            params["skip_child_site_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_child_site_ids must be an list"
            )
        if "child_site_ids" in params and not isinstance(
            params["child_site_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: child_site_ids must be an list"
            )
        if "default_policy" in params and not isinstance(
            params["default_policy"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: default_policy must be an bool"
            )
        if "policy_type" in params and not isinstance(
            params["policy_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: policy_type must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH",
            "/child_site_management_policies/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, ChildSiteManagementPolicy)

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
            "DELETE",
            "/child_site_management_policies/" + path_value(params["id"]),
            params,
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
    ) -> ChildSiteManagementPolicy:
        """A new ChildSiteManagementPolicy with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = ChildSiteManagementPolicy(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = ChildSiteManagementPolicyResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[ChildSiteManagementPolicy]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[ChildSiteManagementPolicy]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ChildSiteManagementPolicy:
    """Parameters:
    id (required) - int64 - Child Site Management Policy ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ChildSiteManagementPolicy:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ChildSiteManagementPolicy:
    """Parameters:
    value - object - Policy configuration data. Attributes differ by policy type. For more information, refer to the Value Hash section of the developer documentation.
    skip_child_site_ids - array(int64) - IDs of child sites excluded from this default policy.
    child_site_ids - array(int64) - IDs of child sites explicitly assigned to this non-default policy.
    default_policy - boolean - Whether this policy applies to child sites not explicitly assigned to another policy.
    policy_type (required) - string - Type of policy.  Valid values: `settings`.
    name - string - Name for this policy.
    description - string - Description for this policy.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ChildSiteManagementPolicy:
    """Parameters:
    value - object - Policy configuration data. Attributes differ by policy type. For more information, refer to the Value Hash section of the developer documentation.
    skip_child_site_ids - array(int64) - IDs of child sites excluded from this default policy.
    child_site_ids - array(int64) - IDs of child sites explicitly assigned to this non-default policy.
    default_policy - boolean - Whether this policy applies to child sites not explicitly assigned to another policy.
    policy_type - string - Type of policy.  Valid values: `settings`.
    name - string - Name for this policy.
    description - string - Description for this policy.
    """
    return _legacy_resource.update(id, params, options)


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


def new(*args, **kwargs) -> ChildSiteManagementPolicy:
    return ChildSiteManagementPolicy(*args, **kwargs)
