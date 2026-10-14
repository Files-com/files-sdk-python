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


class KeyLifecycleRule:
    """A key lifecycle rule record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Key Lifecycle Rule ID
        key_type: string - Key type for which the rule will apply (gpg, ssh, or api).
        inactivity_days: int64 - Number of days of inactivity before the rule applies.
        expiration_days: int64 - Number of days after creation before an SSH key expires. Applies only to SSH keys.
        apply_to_all_workspaces: boolean - If true, a default-workspace rule also applies to keys in all workspaces.
        name: string - Key Lifecycle Rule name
        workspace_id: int64 - Workspace ID. `0` means the default workspace.
    """

    default_attributes = {
        "id": None,  # int64 - Key Lifecycle Rule ID
        "key_type": None,  # string - Key type for which the rule will apply (gpg, ssh, or api).
        "inactivity_days": None,  # int64 - Number of days of inactivity before the rule applies.
        "expiration_days": None,  # int64 - Number of days after creation before an SSH key expires. Applies only to SSH keys.
        "apply_to_all_workspaces": None,  # boolean - If true, a default-workspace rule also applies to keys in all workspaces.
        "name": None,  # string - Key Lifecycle Rule name
        "workspace_id": None,  # int64 - Workspace ID. `0` means the default workspace.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    key_type: str | None
    inactivity_days: int | None
    expiration_days: int | None
    apply_to_all_workspaces: bool | None
    name: str | None
    workspace_id: int | None

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
        ) in KeyLifecycleRule.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in KeyLifecycleRule.default_attributes
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
          apply_to_all_workspaces - boolean - If true, a default-workspace rule also applies to keys in all workspaces.
          expiration_days - int64 - Number of days after creation before an SSH key expires. Applies only to SSH keys.
          key_type - string - Key type for which the rule will apply (gpg, ssh, or api).
          inactivity_days - int64 - Number of days of inactivity before the rule applies.
          name - string - Key Lifecycle Rule name
          workspace_id - int64 - Workspace ID. `0` means the default workspace.
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
        if "apply_to_all_workspaces" in params and isinstance(
            params["apply_to_all_workspaces"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: apply_to_all_workspaces must be an bool"
            )
        if "expiration_days" in params and (
            not isinstance(params["expiration_days"], int)
            or isinstance(params["expiration_days"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: expiration_days must be an int"
            )
        if "key_type" in params and not isinstance(params["key_type"], str):
            raise InvalidParameterError(
                "Bad parameter: key_type must be an str"
            )
        if "inactivity_days" in params and (
            not isinstance(params["inactivity_days"], int)
            or isinstance(params["inactivity_days"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inactivity_days must be an int"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/key_lifecycle_rules/" + path_value(params["id"]), params
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
            "/key_lifecycle_rules/" + path_value(params["id"]),
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
            new_obj = KeyLifecycleRuleResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class KeyLifecycleRuleResource:
    """KeyLifecycleRule operations that use one client's configuration.

    Get one from a client, such as ``client.key_lifecycle_rule``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[KeyLifecycleRule]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `key_type`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `key_type` and `workspace_id`. Valid field combinations are `[ workspace_id, key_type ]`.
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
            KeyLifecycleRule, "GET", "/key_lifecycle_rules", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[KeyLifecycleRule]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> KeyLifecycleRule:
        """Parameters:
        id (required) - int64 - Key Lifecycle Rule ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> KeyLifecycleRule:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/key_lifecycle_rules/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, KeyLifecycleRule)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> KeyLifecycleRule:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> KeyLifecycleRule:
        """Parameters:
        apply_to_all_workspaces - boolean - If true, a default-workspace rule also applies to keys in all workspaces.
        expiration_days - int64 - Number of days after creation before an SSH key expires. Applies only to SSH keys.
        key_type - string - Key type for which the rule will apply (gpg, ssh, or api).
        inactivity_days - int64 - Number of days of inactivity before the rule applies.
        name - string - Key Lifecycle Rule name
        workspace_id - int64 - Workspace ID. `0` means the default workspace.
        """
        params = copy_params(params)
        if "apply_to_all_workspaces" in params and not isinstance(
            params["apply_to_all_workspaces"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: apply_to_all_workspaces must be an bool"
            )
        if "expiration_days" in params and (
            not isinstance(params["expiration_days"], int)
            or isinstance(params["expiration_days"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: expiration_days must be an int"
            )
        if "key_type" in params and not isinstance(params["key_type"], str):
            raise InvalidParameterError(
                "Bad parameter: key_type must be an str"
            )
        if "inactivity_days" in params and (
            not isinstance(params["inactivity_days"], int)
            or isinstance(params["inactivity_days"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inactivity_days must be an int"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/key_lifecycle_rules", params)
        return operation.decode_model(response, KeyLifecycleRule)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> KeyLifecycleRule:
        """Parameters:
        apply_to_all_workspaces - boolean - If true, a default-workspace rule also applies to keys in all workspaces.
        expiration_days - int64 - Number of days after creation before an SSH key expires. Applies only to SSH keys.
        key_type - string - Key type for which the rule will apply (gpg, ssh, or api).
        inactivity_days - int64 - Number of days of inactivity before the rule applies.
        name - string - Key Lifecycle Rule name
        workspace_id - int64 - Workspace ID. `0` means the default workspace.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> KeyLifecycleRule:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "apply_to_all_workspaces" in params and not isinstance(
            params["apply_to_all_workspaces"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: apply_to_all_workspaces must be an bool"
            )
        if "expiration_days" in params and (
            not isinstance(params["expiration_days"], int)
            or isinstance(params["expiration_days"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: expiration_days must be an int"
            )
        if "key_type" in params and not isinstance(params["key_type"], str):
            raise InvalidParameterError(
                "Bad parameter: key_type must be an str"
            )
        if "inactivity_days" in params and (
            not isinstance(params["inactivity_days"], int)
            or isinstance(params["inactivity_days"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inactivity_days must be an int"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/key_lifecycle_rules/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, KeyLifecycleRule)

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
            "/key_lifecycle_rules/" + path_value(params["id"]),
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
    ) -> KeyLifecycleRule:
        """A new KeyLifecycleRule with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = KeyLifecycleRule(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = KeyLifecycleRuleResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[KeyLifecycleRule]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `key_type`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `key_type` and `workspace_id`. Valid field combinations are `[ workspace_id, key_type ]`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[KeyLifecycleRule]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> KeyLifecycleRule:
    """Parameters:
    id (required) - int64 - Key Lifecycle Rule ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> KeyLifecycleRule:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> KeyLifecycleRule:
    """Parameters:
    apply_to_all_workspaces - boolean - If true, a default-workspace rule also applies to keys in all workspaces.
    expiration_days - int64 - Number of days after creation before an SSH key expires. Applies only to SSH keys.
    key_type - string - Key type for which the rule will apply (gpg, ssh, or api).
    inactivity_days - int64 - Number of days of inactivity before the rule applies.
    name - string - Key Lifecycle Rule name
    workspace_id - int64 - Workspace ID. `0` means the default workspace.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> KeyLifecycleRule:
    """Parameters:
    apply_to_all_workspaces - boolean - If true, a default-workspace rule also applies to keys in all workspaces.
    expiration_days - int64 - Number of days after creation before an SSH key expires. Applies only to SSH keys.
    key_type - string - Key type for which the rule will apply (gpg, ssh, or api).
    inactivity_days - int64 - Number of days of inactivity before the rule applies.
    name - string - Key Lifecycle Rule name
    workspace_id - int64 - Workspace ID. `0` means the default workspace.
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


def new(*args, **kwargs) -> KeyLifecycleRule:
    return KeyLifecycleRule(*args, **kwargs)
