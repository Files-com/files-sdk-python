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


class Group:
    """A group record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Group ID
        name: string - Group name
        allowed_ips: string - A list of allowed IPs if applicable. Newline delimited
        admin_ids: string - Comma-delimited list of user IDs who are group administrators (separated by commas)
        notes: string - Notes about this group
        user_ids: string - Comma-delimited list of user IDs who belong to this group (separated by commas)
        usernames: string - Comma-delimited list of usernames who belong to this group (separated by commas)
        ai_assistant_personality_id: int64 - AI Assistant Personality ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user or Partner assignment overrides it.
        ftp_permission: boolean - If true, users in this group can use FTP to login. This will override a false value of `ftp_permission` on the user level.
        sftp_permission: boolean - If true, users in this group can use SFTP to login. This will override a false value of `sftp_permission` on the user level.
        dav_permission: boolean - If true, users in this group can use WebDAV to login. This will override a false value of `dav_permission` on the user level.
        restapi_permission: boolean - If true, users in this group can use the REST API to login. This will override a false value of `restapi_permission` on the user level.
        s3_compatible_endpoint_permission: boolean - If true, users in this group can access the S3-compatible endpoint. This will override a false value of `s3_compatible_endpoint_permission` on the user level. Defaults to false.
        desktop_configuration_profile_id: int64 - Desktop Configuration Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
        integration_centric_profile_id: int64 - Integration Centric Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
        site_id: int64 - Site ID
        workspace_id: int64 - Workspace ID
    """

    default_attributes = {
        "id": None,  # int64 - Group ID
        "name": None,  # string - Group name
        "allowed_ips": None,  # string - A list of allowed IPs if applicable.  Newline delimited
        "admin_ids": None,  # string - Comma-delimited list of user IDs who are group administrators (separated by commas)
        "notes": None,  # string - Notes about this group
        "user_ids": None,  # string - Comma-delimited list of user IDs who belong to this group (separated by commas)
        "usernames": None,  # string - Comma-delimited list of usernames who belong to this group (separated by commas)
        "ai_assistant_personality_id": None,  # int64 - AI Assistant Personality ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user or Partner assignment overrides it.
        "ftp_permission": None,  # boolean - If true, users in this group can use FTP to login.  This will override a false value of `ftp_permission` on the user level.
        "sftp_permission": None,  # boolean - If true, users in this group can use SFTP to login.  This will override a false value of `sftp_permission` on the user level.
        "dav_permission": None,  # boolean - If true, users in this group can use WebDAV to login.  This will override a false value of `dav_permission` on the user level.
        "restapi_permission": None,  # boolean - If true, users in this group can use the REST API to login.  This will override a false value of `restapi_permission` on the user level.
        "s3_compatible_endpoint_permission": None,  # boolean - If true, users in this group can access the S3-compatible endpoint. This will override a false value of `s3_compatible_endpoint_permission` on the user level. Defaults to false.
        "desktop_configuration_profile_id": None,  # int64 - Desktop Configuration Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
        "integration_centric_profile_id": None,  # int64 - Integration Centric Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
        "site_id": None,  # int64 - Site ID
        "workspace_id": None,  # int64 - Workspace ID
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    name: str | None
    allowed_ips: str | None
    admin_ids: str | None
    notes: str | None
    user_ids: str | None
    usernames: str | None
    ai_assistant_personality_id: int | None
    ftp_permission: bool | None
    sftp_permission: bool | None
    dav_permission: bool | None
    restapi_permission: bool | None
    s3_compatible_endpoint_permission: bool | None
    desktop_configuration_profile_id: int | None
    integration_centric_profile_id: int | None
    site_id: int | None
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
        for attribute, default_value in Group.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Group.default_attributes
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
          notes - string - Group notes.
          user_ids - string - A list of user ids. If sent as a string, should be comma-delimited.
          admin_ids - string - A list of group admin user ids. If sent as a string, should be comma-delimited.
          ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user or Partner assignment overrides it.
          ftp_permission - boolean - If true, users in this group can use FTP to login.  This will override a false value of `ftp_permission` on the user level.
          sftp_permission - boolean - If true, users in this group can use SFTP to login.  This will override a false value of `sftp_permission` on the user level.
          dav_permission - boolean - If true, users in this group can use WebDAV to login.  This will override a false value of `dav_permission` on the user level.
          restapi_permission - boolean - If true, users in this group can use the REST API to login.  This will override a false value of `restapi_permission` on the user level.
          s3_compatible_endpoint_permission - boolean - If true, users in this group can access the S3-compatible endpoint. This will override a false value of `s3_compatible_endpoint_permission` on the user level. Defaults to false.
          desktop_configuration_profile_id - int64 - Desktop Configuration Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
          integration_centric_profile_id - int64 - Integration Centric Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
          allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
          name - string - Group name.
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
        if "notes" in params and not isinstance(params["notes"], str):
            raise InvalidParameterError("Bad parameter: notes must be an str")
        if "user_ids" in params and not isinstance(params["user_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: user_ids must be an str"
            )
        if "admin_ids" in params and not isinstance(params["admin_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: admin_ids must be an str"
            )
        if "ai_assistant_personality_id" in params and (
            not isinstance(params["ai_assistant_personality_id"], int)
            or isinstance(params["ai_assistant_personality_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: ai_assistant_personality_id must be an int"
            )
        if "ftp_permission" in params and isinstance(
            params["ftp_permission"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: ftp_permission must be an bool"
            )
        if "sftp_permission" in params and isinstance(
            params["sftp_permission"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: sftp_permission must be an bool"
            )
        if "dav_permission" in params and isinstance(
            params["dav_permission"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: dav_permission must be an bool"
            )
        if "restapi_permission" in params and isinstance(
            params["restapi_permission"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: restapi_permission must be an bool"
            )
        if "s3_compatible_endpoint_permission" in params and isinstance(
            params["s3_compatible_endpoint_permission"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_compatible_endpoint_permission must be an bool"
            )
        if "desktop_configuration_profile_id" in params and (
            not isinstance(params["desktop_configuration_profile_id"], int)
            or isinstance(params["desktop_configuration_profile_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: desktop_configuration_profile_id must be an int"
            )
        if "integration_centric_profile_id" in params and (
            not isinstance(params["integration_centric_profile_id"], int)
            or isinstance(params["integration_centric_profile_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: integration_centric_profile_id must be an int"
            )
        if "allowed_ips" in params and not isinstance(
            params["allowed_ips"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: allowed_ips must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/groups/" + path_value(params["id"]), params
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
            "DELETE", "/groups/" + path_value(params["id"]), params
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
            new_obj = GroupResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class GroupResource:
    """Group operations that use one client's configuration.

    Get one from a client, such as ``client.group``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Group]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `workspace_id` or `name`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `name` and `workspace_id`. Valid field combinations are `[ workspace_id, name ]`.
        filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.
        ids - string - Comma-separated list of group ids to include in results.
        include_parent_site_groups - boolean - Include groups from the parent site.
        include_default_workspace_groups - boolean - When scoped to a Custom Workspace, include Default Workspace groups that have permissions in that Workspace. Available to Site Administrators, and to Workspace Administrators and Folder Admins in that Workspace when the site shares its Default Workspace directory with Workspaces.
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
        if "ids" in params and not isinstance(params["ids"], str):
            raise InvalidParameterError("Bad parameter: ids must be an str")
        if "include_parent_site_groups" in params and not isinstance(
            params["include_parent_site_groups"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: include_parent_site_groups must be an bool"
            )
        if "include_default_workspace_groups" in params and not isinstance(
            params["include_default_workspace_groups"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: include_default_workspace_groups must be an bool"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(Group, "GET", "/groups", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Group]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Group:
        """Parameters:
        id (required) - int64 - Group ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Group:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/groups/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Group)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Group:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Group:
        """Parameters:
        notes - string - Group notes.
        user_ids - string - A list of user ids. If sent as a string, should be comma-delimited.
        admin_ids - string - A list of group admin user ids. If sent as a string, should be comma-delimited.
        ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user or Partner assignment overrides it.
        ftp_permission - boolean - If true, users in this group can use FTP to login.  This will override a false value of `ftp_permission` on the user level.
        sftp_permission - boolean - If true, users in this group can use SFTP to login.  This will override a false value of `sftp_permission` on the user level.
        dav_permission - boolean - If true, users in this group can use WebDAV to login.  This will override a false value of `dav_permission` on the user level.
        restapi_permission - boolean - If true, users in this group can use the REST API to login.  This will override a false value of `restapi_permission` on the user level.
        s3_compatible_endpoint_permission - boolean - If true, users in this group can access the S3-compatible endpoint. This will override a false value of `s3_compatible_endpoint_permission` on the user level. Defaults to false.
        desktop_configuration_profile_id - int64 - Desktop Configuration Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
        integration_centric_profile_id - int64 - Integration Centric Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
        allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
        name (required) - string - Group name.
        workspace_id - int64 - Workspace ID
        """
        params = copy_params(params)
        if "notes" in params and not isinstance(params["notes"], str):
            raise InvalidParameterError("Bad parameter: notes must be an str")
        if "user_ids" in params and not isinstance(params["user_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: user_ids must be an str"
            )
        if "admin_ids" in params and not isinstance(params["admin_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: admin_ids must be an str"
            )
        if "ai_assistant_personality_id" in params and (
            not isinstance(params["ai_assistant_personality_id"], int)
            or isinstance(params["ai_assistant_personality_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: ai_assistant_personality_id must be an int"
            )
        if "ftp_permission" in params and not isinstance(
            params["ftp_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: ftp_permission must be an bool"
            )
        if "sftp_permission" in params and not isinstance(
            params["sftp_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sftp_permission must be an bool"
            )
        if "dav_permission" in params and not isinstance(
            params["dav_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: dav_permission must be an bool"
            )
        if "restapi_permission" in params and not isinstance(
            params["restapi_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: restapi_permission must be an bool"
            )
        if "s3_compatible_endpoint_permission" in params and not isinstance(
            params["s3_compatible_endpoint_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_compatible_endpoint_permission must be an bool"
            )
        if "desktop_configuration_profile_id" in params and (
            not isinstance(params["desktop_configuration_profile_id"], int)
            or isinstance(params["desktop_configuration_profile_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: desktop_configuration_profile_id must be an int"
            )
        if "integration_centric_profile_id" in params and (
            not isinstance(params["integration_centric_profile_id"], int)
            or isinstance(params["integration_centric_profile_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: integration_centric_profile_id must be an int"
            )
        if "allowed_ips" in params and not isinstance(
            params["allowed_ips"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: allowed_ips must be an str"
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
        if "name" not in params:
            raise MissingParameterError("Parameter missing: name")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/groups", params)
        return operation.decode_model(response, Group)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Group:
        """Parameters:
        notes - string - Group notes.
        user_ids - string - A list of user ids. If sent as a string, should be comma-delimited.
        admin_ids - string - A list of group admin user ids. If sent as a string, should be comma-delimited.
        ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user or Partner assignment overrides it.
        ftp_permission - boolean - If true, users in this group can use FTP to login.  This will override a false value of `ftp_permission` on the user level.
        sftp_permission - boolean - If true, users in this group can use SFTP to login.  This will override a false value of `sftp_permission` on the user level.
        dav_permission - boolean - If true, users in this group can use WebDAV to login.  This will override a false value of `dav_permission` on the user level.
        restapi_permission - boolean - If true, users in this group can use the REST API to login.  This will override a false value of `restapi_permission` on the user level.
        s3_compatible_endpoint_permission - boolean - If true, users in this group can access the S3-compatible endpoint. This will override a false value of `s3_compatible_endpoint_permission` on the user level. Defaults to false.
        desktop_configuration_profile_id - int64 - Desktop Configuration Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
        integration_centric_profile_id - int64 - Integration Centric Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
        allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
        name - string - Group name.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Group:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "notes" in params and not isinstance(params["notes"], str):
            raise InvalidParameterError("Bad parameter: notes must be an str")
        if "user_ids" in params and not isinstance(params["user_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: user_ids must be an str"
            )
        if "admin_ids" in params and not isinstance(params["admin_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: admin_ids must be an str"
            )
        if "ai_assistant_personality_id" in params and (
            not isinstance(params["ai_assistant_personality_id"], int)
            or isinstance(params["ai_assistant_personality_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: ai_assistant_personality_id must be an int"
            )
        if "ftp_permission" in params and not isinstance(
            params["ftp_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: ftp_permission must be an bool"
            )
        if "sftp_permission" in params and not isinstance(
            params["sftp_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sftp_permission must be an bool"
            )
        if "dav_permission" in params and not isinstance(
            params["dav_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: dav_permission must be an bool"
            )
        if "restapi_permission" in params and not isinstance(
            params["restapi_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: restapi_permission must be an bool"
            )
        if "s3_compatible_endpoint_permission" in params and not isinstance(
            params["s3_compatible_endpoint_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_compatible_endpoint_permission must be an bool"
            )
        if "desktop_configuration_profile_id" in params and (
            not isinstance(params["desktop_configuration_profile_id"], int)
            or isinstance(params["desktop_configuration_profile_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: desktop_configuration_profile_id must be an int"
            )
        if "integration_centric_profile_id" in params and (
            not isinstance(params["integration_centric_profile_id"], int)
            or isinstance(params["integration_centric_profile_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: integration_centric_profile_id must be an int"
            )
        if "allowed_ips" in params and not isinstance(
            params["allowed_ips"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: allowed_ips must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/groups/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Group)

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
            "DELETE", "/groups/" + path_value(params["id"]), params
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
    ) -> Group:
        """A new Group with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Group(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = GroupResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Group]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `workspace_id` or `name`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `name` and `workspace_id`. Valid field combinations are `[ workspace_id, name ]`.
    filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.
    ids - string - Comma-separated list of group ids to include in results.
    include_parent_site_groups - boolean - Include groups from the parent site.
    include_default_workspace_groups - boolean - When scoped to a Custom Workspace, include Default Workspace groups that have permissions in that Workspace. Available to Site Administrators, and to Workspace Administrators and Folder Admins in that Workspace when the site shares its Default Workspace directory with Workspaces.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Group]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Group:
    """Parameters:
    id (required) - int64 - Group ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Group:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Group:
    """Parameters:
    notes - string - Group notes.
    user_ids - string - A list of user ids. If sent as a string, should be comma-delimited.
    admin_ids - string - A list of group admin user ids. If sent as a string, should be comma-delimited.
    ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user or Partner assignment overrides it.
    ftp_permission - boolean - If true, users in this group can use FTP to login.  This will override a false value of `ftp_permission` on the user level.
    sftp_permission - boolean - If true, users in this group can use SFTP to login.  This will override a false value of `sftp_permission` on the user level.
    dav_permission - boolean - If true, users in this group can use WebDAV to login.  This will override a false value of `dav_permission` on the user level.
    restapi_permission - boolean - If true, users in this group can use the REST API to login.  This will override a false value of `restapi_permission` on the user level.
    s3_compatible_endpoint_permission - boolean - If true, users in this group can access the S3-compatible endpoint. This will override a false value of `s3_compatible_endpoint_permission` on the user level. Defaults to false.
    desktop_configuration_profile_id - int64 - Desktop Configuration Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
    integration_centric_profile_id - int64 - Integration Centric Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
    allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
    name (required) - string - Group name.
    workspace_id - int64 - Workspace ID
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Group:
    """Parameters:
    notes - string - Group notes.
    user_ids - string - A list of user ids. If sent as a string, should be comma-delimited.
    admin_ids - string - A list of group admin user ids. If sent as a string, should be comma-delimited.
    ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user or Partner assignment overrides it.
    ftp_permission - boolean - If true, users in this group can use FTP to login.  This will override a false value of `ftp_permission` on the user level.
    sftp_permission - boolean - If true, users in this group can use SFTP to login.  This will override a false value of `sftp_permission` on the user level.
    dav_permission - boolean - If true, users in this group can use WebDAV to login.  This will override a false value of `dav_permission` on the user level.
    restapi_permission - boolean - If true, users in this group can use the REST API to login.  This will override a false value of `restapi_permission` on the user level.
    s3_compatible_endpoint_permission - boolean - If true, users in this group can access the S3-compatible endpoint. This will override a false value of `s3_compatible_endpoint_permission` on the user level. Defaults to false.
    desktop_configuration_profile_id - int64 - Desktop Configuration Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
    integration_centric_profile_id - int64 - Integration Centric Profile ID assigned to this Group, if any. Users in the Group inherit it unless a direct per-user assignment overrides it.
    allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
    name - string - Group name.
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


def new(*args, **kwargs) -> Group:
    return Group(*args, **kwargs)
