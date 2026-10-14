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


class UserLifecycleRule:
    """A user lifecycle rule record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - User Lifecycle Rule ID
        authentication_method: string - User authentication method for which the rule will apply. Use `all_non_sso` to target every non-SSO authentication method with one rule.
        group_ids: array(int64) - Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
        action: string - Action to take on inactive users (disable or delete)
        inactivity_days: int64 - Number of days of inactivity before the rule applies
        include_folder_admins: boolean - If true, the rule will apply to folder admins.
        include_site_admins: boolean - If true, the rule includes Site Administrators, who always belong to the Default Workspace. Can only be enabled when `workspace_id` is `0`.
        apply_to_all_workspaces: boolean - If true, a Default Workspace rule also applies to users in all Custom Workspaces. Can only be enabled when `workspace_id` is `0`.
        name: string - User Lifecycle Rule name
        notify_users: boolean - If true, users will be emailed before the rule disables or deletes them.
        partner_tag: string - If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
        site_id: int64 - Site ID
        workspace_id: int64 - Workspace whose users the rule applies to. `0` means the Default Workspace. A Custom Workspace rule applies only to users who belong to that Workspace, regardless of access granted to other users.
        user_state: string - State of the users to apply the rule to (inactive or disabled)
        user_tag: string - If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
    """

    default_attributes = {
        "id": None,  # int64 - User Lifecycle Rule ID
        "authentication_method": None,  # string - User authentication method for which the rule will apply. Use `all_non_sso` to target every non-SSO authentication method with one rule.
        "group_ids": None,  # array(int64) - Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
        "action": None,  # string - Action to take on inactive users (disable or delete)
        "inactivity_days": None,  # int64 - Number of days of inactivity before the rule applies
        "include_folder_admins": None,  # boolean - If true, the rule will apply to folder admins.
        "include_site_admins": None,  # boolean - If true, the rule includes Site Administrators, who always belong to the Default Workspace. Can only be enabled when `workspace_id` is `0`.
        "apply_to_all_workspaces": None,  # boolean - If true, a Default Workspace rule also applies to users in all Custom Workspaces. Can only be enabled when `workspace_id` is `0`.
        "name": None,  # string - User Lifecycle Rule name
        "notify_users": None,  # boolean - If true, users will be emailed before the rule disables or deletes them.
        "partner_tag": None,  # string - If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
        "site_id": None,  # int64 - Site ID
        "workspace_id": None,  # int64 - Workspace whose users the rule applies to. `0` means the Default Workspace. A Custom Workspace rule applies only to users who belong to that Workspace, regardless of access granted to other users.
        "user_state": None,  # string - State of the users to apply the rule to (inactive or disabled)
        "user_tag": None,  # string - If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    authentication_method: str | None
    group_ids: builtins.list[int] | None
    action: str | None
    inactivity_days: int | None
    include_folder_admins: bool | None
    include_site_admins: bool | None
    apply_to_all_workspaces: bool | None
    name: str | None
    notify_users: bool | None
    partner_tag: str | None
    site_id: int | None
    workspace_id: int | None
    user_state: str | None
    user_tag: str | None

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
        ) in UserLifecycleRule.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in UserLifecycleRule.default_attributes
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
          action - string - Action to take on inactive users (disable or delete)
          apply_to_all_workspaces - boolean - If true, a Default Workspace rule also applies to users in all Custom Workspaces. Can only be enabled when `workspace_id` is `0`.
          authentication_method - string - User authentication method for which the rule will apply. Use `all_non_sso` to target every non-SSO authentication method with one rule.
          group_ids - array(int64) - Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
          inactivity_days - int64 - Number of days of inactivity before the rule applies
          include_site_admins - boolean - If true, the rule includes Site Administrators, who always belong to the Default Workspace. Can only be enabled when `workspace_id` is `0`.
          include_folder_admins - boolean - If true, the rule will apply to folder admins.
          name - string - User Lifecycle Rule name
          notify_users - boolean - If true, users will be emailed before the rule disables or deletes them.
          partner_tag - string - If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
          user_state - string - State of the users to apply the rule to (inactive or disabled)
          user_tag - string - If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
          workspace_id - int64 - Workspace whose users the rule applies to. `0` means the Default Workspace. A Custom Workspace rule applies only to users who belong to that Workspace, regardless of access granted to other users.
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
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "apply_to_all_workspaces" in params and isinstance(
            params["apply_to_all_workspaces"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: apply_to_all_workspaces must be an bool"
            )
        if "authentication_method" in params and not isinstance(
            params["authentication_method"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: authentication_method must be an str"
            )
        if "group_ids" in params and not isinstance(
            params["group_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an list"
            )
        if "inactivity_days" in params and (
            not isinstance(params["inactivity_days"], int)
            or isinstance(params["inactivity_days"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inactivity_days must be an int"
            )
        if "include_site_admins" in params and isinstance(
            params["include_site_admins"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: include_site_admins must be an bool"
            )
        if "include_folder_admins" in params and isinstance(
            params["include_folder_admins"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: include_folder_admins must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "notify_users" in params and isinstance(
            params["notify_users"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_users must be an bool"
            )
        if "partner_tag" in params and not isinstance(
            params["partner_tag"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_tag must be an str"
            )
        if "user_state" in params and not isinstance(
            params["user_state"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: user_state must be an str"
            )
        if "user_tag" in params and not isinstance(params["user_tag"], str):
            raise InvalidParameterError(
                "Bad parameter: user_tag must be an str"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH",
            "/user_lifecycle_rules/" + path_value(params["id"]),
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
            "/user_lifecycle_rules/" + path_value(params["id"]),
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
            new_obj = UserLifecycleRuleResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class UserLifecycleRuleResource:
    """UserLifecycleRule operations that use one client's configuration.

    Get one from a client, such as ``client.user_lifecycle_rule``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[UserLifecycleRule]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id` and `workspace_id`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.
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
            UserLifecycleRule,
            "GET",
            "/user_lifecycle_rules",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[UserLifecycleRule]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> UserLifecycleRule:
        """Parameters:
        id (required) - int64 - User Lifecycle Rule ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> UserLifecycleRule:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/user_lifecycle_rules/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, UserLifecycleRule)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> UserLifecycleRule:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> UserLifecycleRule:
        """Parameters:
        action - string - Action to take on inactive users (disable or delete)
        apply_to_all_workspaces - boolean - If true, a Default Workspace rule also applies to users in all Custom Workspaces. Can only be enabled when `workspace_id` is `0`.
        authentication_method - string - User authentication method for which the rule will apply. Use `all_non_sso` to target every non-SSO authentication method with one rule.
        group_ids - array(int64) - Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
        inactivity_days - int64 - Number of days of inactivity before the rule applies
        include_site_admins - boolean - If true, the rule includes Site Administrators, who always belong to the Default Workspace. Can only be enabled when `workspace_id` is `0`.
        include_folder_admins - boolean - If true, the rule will apply to folder admins.
        name - string - User Lifecycle Rule name
        notify_users - boolean - If true, users will be emailed before the rule disables or deletes them.
        partner_tag - string - If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
        user_state - string - State of the users to apply the rule to (inactive or disabled)
        user_tag - string - If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
        workspace_id - int64 - Workspace whose users the rule applies to. `0` means the Default Workspace. A Custom Workspace rule applies only to users who belong to that Workspace, regardless of access granted to other users.
        """
        params = copy_params(params)
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "apply_to_all_workspaces" in params and not isinstance(
            params["apply_to_all_workspaces"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: apply_to_all_workspaces must be an bool"
            )
        if "authentication_method" in params and not isinstance(
            params["authentication_method"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: authentication_method must be an str"
            )
        if "group_ids" in params and not isinstance(
            params["group_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an list"
            )
        if "inactivity_days" in params and (
            not isinstance(params["inactivity_days"], int)
            or isinstance(params["inactivity_days"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inactivity_days must be an int"
            )
        if "include_site_admins" in params and not isinstance(
            params["include_site_admins"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: include_site_admins must be an bool"
            )
        if "include_folder_admins" in params and not isinstance(
            params["include_folder_admins"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: include_folder_admins must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "notify_users" in params and not isinstance(
            params["notify_users"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_users must be an bool"
            )
        if "partner_tag" in params and not isinstance(
            params["partner_tag"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_tag must be an str"
            )
        if "user_state" in params and not isinstance(
            params["user_state"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: user_state must be an str"
            )
        if "user_tag" in params and not isinstance(params["user_tag"], str):
            raise InvalidParameterError(
                "Bad parameter: user_tag must be an str"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/user_lifecycle_rules", params)
        return operation.decode_model(response, UserLifecycleRule)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> UserLifecycleRule:
        """Parameters:
        action - string - Action to take on inactive users (disable or delete)
        apply_to_all_workspaces - boolean - If true, a Default Workspace rule also applies to users in all Custom Workspaces. Can only be enabled when `workspace_id` is `0`.
        authentication_method - string - User authentication method for which the rule will apply. Use `all_non_sso` to target every non-SSO authentication method with one rule.
        group_ids - array(int64) - Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
        inactivity_days - int64 - Number of days of inactivity before the rule applies
        include_site_admins - boolean - If true, the rule includes Site Administrators, who always belong to the Default Workspace. Can only be enabled when `workspace_id` is `0`.
        include_folder_admins - boolean - If true, the rule will apply to folder admins.
        name - string - User Lifecycle Rule name
        notify_users - boolean - If true, users will be emailed before the rule disables or deletes them.
        partner_tag - string - If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
        user_state - string - State of the users to apply the rule to (inactive or disabled)
        user_tag - string - If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
        workspace_id - int64 - Workspace whose users the rule applies to. `0` means the Default Workspace. A Custom Workspace rule applies only to users who belong to that Workspace, regardless of access granted to other users.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> UserLifecycleRule:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "apply_to_all_workspaces" in params and not isinstance(
            params["apply_to_all_workspaces"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: apply_to_all_workspaces must be an bool"
            )
        if "authentication_method" in params and not isinstance(
            params["authentication_method"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: authentication_method must be an str"
            )
        if "group_ids" in params and not isinstance(
            params["group_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an list"
            )
        if "inactivity_days" in params and (
            not isinstance(params["inactivity_days"], int)
            or isinstance(params["inactivity_days"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inactivity_days must be an int"
            )
        if "include_site_admins" in params and not isinstance(
            params["include_site_admins"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: include_site_admins must be an bool"
            )
        if "include_folder_admins" in params and not isinstance(
            params["include_folder_admins"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: include_folder_admins must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "notify_users" in params and not isinstance(
            params["notify_users"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_users must be an bool"
            )
        if "partner_tag" in params and not isinstance(
            params["partner_tag"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_tag must be an str"
            )
        if "user_state" in params and not isinstance(
            params["user_state"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: user_state must be an str"
            )
        if "user_tag" in params and not isinstance(params["user_tag"], str):
            raise InvalidParameterError(
                "Bad parameter: user_tag must be an str"
            )
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
            "PATCH",
            "/user_lifecycle_rules/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, UserLifecycleRule)

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
            "/user_lifecycle_rules/" + path_value(params["id"]),
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
    ) -> UserLifecycleRule:
        """A new UserLifecycleRule with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = UserLifecycleRule(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = UserLifecycleRuleResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[UserLifecycleRule]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id` and `workspace_id`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[UserLifecycleRule]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> UserLifecycleRule:
    """Parameters:
    id (required) - int64 - User Lifecycle Rule ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> UserLifecycleRule:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> UserLifecycleRule:
    """Parameters:
    action - string - Action to take on inactive users (disable or delete)
    apply_to_all_workspaces - boolean - If true, a Default Workspace rule also applies to users in all Custom Workspaces. Can only be enabled when `workspace_id` is `0`.
    authentication_method - string - User authentication method for which the rule will apply. Use `all_non_sso` to target every non-SSO authentication method with one rule.
    group_ids - array(int64) - Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
    inactivity_days - int64 - Number of days of inactivity before the rule applies
    include_site_admins - boolean - If true, the rule includes Site Administrators, who always belong to the Default Workspace. Can only be enabled when `workspace_id` is `0`.
    include_folder_admins - boolean - If true, the rule will apply to folder admins.
    name - string - User Lifecycle Rule name
    notify_users - boolean - If true, users will be emailed before the rule disables or deletes them.
    partner_tag - string - If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
    user_state - string - State of the users to apply the rule to (inactive or disabled)
    user_tag - string - If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
    workspace_id - int64 - Workspace whose users the rule applies to. `0` means the Default Workspace. A Custom Workspace rule applies only to users who belong to that Workspace, regardless of access granted to other users.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> UserLifecycleRule:
    """Parameters:
    action - string - Action to take on inactive users (disable or delete)
    apply_to_all_workspaces - boolean - If true, a Default Workspace rule also applies to users in all Custom Workspaces. Can only be enabled when `workspace_id` is `0`.
    authentication_method - string - User authentication method for which the rule will apply. Use `all_non_sso` to target every non-SSO authentication method with one rule.
    group_ids - array(int64) - Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
    inactivity_days - int64 - Number of days of inactivity before the rule applies
    include_site_admins - boolean - If true, the rule includes Site Administrators, who always belong to the Default Workspace. Can only be enabled when `workspace_id` is `0`.
    include_folder_admins - boolean - If true, the rule will apply to folder admins.
    name - string - User Lifecycle Rule name
    notify_users - boolean - If true, users will be emailed before the rule disables or deletes them.
    partner_tag - string - If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
    user_state - string - State of the users to apply the rule to (inactive or disabled)
    user_tag - string - If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
    workspace_id - int64 - Workspace whose users the rule applies to. `0` means the Default Workspace. A Custom Workspace rule applies only to users who belong to that Workspace, regardless of access granted to other users.
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


def new(*args, **kwargs) -> UserLifecycleRule:
    return UserLifecycleRule(*args, **kwargs)
