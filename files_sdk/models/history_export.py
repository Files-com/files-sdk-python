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
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class HistoryExport:
    """A history export record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        workspace_id: int64 - Workspace of the export. 0 represents the default workspace. A null value means a site-wide export.
        id: int64 - History Export ID
        history_version: string - Version of the history for the export.
        start_at: date-time - Start date/time of export range.
        end_at: date-time - End date/time of export range.
        status: string - Status of export. Will be: `building`, `ready`, or `failed`
        query_action: string - Filter results by this this action type. Valid values: `create`, `read`, `update`, `destroy`, `move`, `login`, `failedlogin`, `copy`, `user_create`, `user_update`, `user_destroy`, `group_create`, `group_update`, `group_destroy`, `permission_create`, `permission_destroy`, `api_key_create`, `api_key_update`, `api_key_destroy`, `archived_delete`
        query_interface: string - Filter results by this this interface type. Valid values: `web`, `ftp`, `robot`, `jsapi`, `webdesktopapi`, `sftp`, `dav`, `desktop`, `restapi`, `scim`, `office`, `mobile`, `as2`, `inbound_email`, `remote`, `inbound_s3`
        query_user_id: string - Return results that are actions performed by the user indicated by this User ID
        query_file_id: string - Return results that are file actions related to the file indicated by this File ID
        query_parent_id: string - Return results that are file actions inside the parent folder specified by this folder ID
        query_path: string - Return results that are file actions related to paths matching this pattern.
        query_folder: string - Return results that are file actions related to files or folders inside folder paths matching this pattern.
        query_src: string - Return results that are file moves originating from paths matching this pattern.
        query_destination: string - Return results that are file moves with paths matching this pattern as destination.
        query_ip: string - Filter results by this IP address.
        query_username: string - Filter results by this username.
        query_failure_type: string - If searching for Histories about login failures, this parameter restricts results to failures of this specific type. Valid values: `expired_trial`, `account_overdue`, `locked_out`, `ip_mismatch`, `password_mismatch`, `site_mismatch`, `username_not_found`, `none`, `no_ftp_permission`, `no_web_permission`, `no_directory`, `errno_enoent`, `no_sftp_permission`, `no_dav_permission`, `no_restapi_permission`, `key_mismatch`, `region_mismatch`, `expired_access`, `desktop_ip_mismatch`, `desktop_api_key_not_used_quickly_enough`, `disabled`, `country_mismatch`, `insecure_ftp`, `insecure_cipher`, `rate_limited`, `no_s3_compatible_endpoint_permission`, `mobile_ip_mismatch`, `mobile_api_key_not_used_quickly_enough`, `desktop_app_disabled`, `mobile_app_disabled`
        query_target_id: string - If searching for Histories about specific objects (such as Users, or API Keys), this parameter restricts results to objects that match this ID.
        query_target_name: string - If searching for Histories about Users, Groups or other objects with names, this parameter restricts results to objects with this name/username.
        query_target_permission: string - If searching for Histories about Permissions, this parameter restricts results to permissions of this level.
        query_target_user_id: string - If searching for Histories about API keys, this parameter restricts results to API keys created by/for this user ID.
        query_target_username: string - If searching for Histories about API keys, this parameter restricts results to API keys created by/for this username.
        query_target_platform: string - If searching for Histories about API keys, this parameter restricts results to API keys associated with this platform.
        query_target_permission_set: string - If searching for Histories about API keys, this parameter restricts results to API keys with this permission set.
        results_url: string - If `status` is `ready`, this will be a URL where all the results can be downloaded at once as a CSV.
        user_id: int64 - User ID. Provide a value of `0` to operate the current session's user.
    """

    default_attributes = {
        "workspace_id": None,  # int64 - Workspace of the export. 0 represents the default workspace. A null value means a site-wide export.
        "id": None,  # int64 - History Export ID
        "history_version": None,  # string - Version of the history for the export.
        "start_at": None,  # date-time - Start date/time of export range.
        "end_at": None,  # date-time - End date/time of export range.
        "status": None,  # string - Status of export.  Will be: `building`, `ready`, or `failed`
        "query_action": None,  # string - Filter results by this this action type. Valid values: `create`, `read`, `update`, `destroy`, `move`, `login`, `failedlogin`, `copy`, `user_create`, `user_update`, `user_destroy`, `group_create`, `group_update`, `group_destroy`, `permission_create`, `permission_destroy`, `api_key_create`, `api_key_update`, `api_key_destroy`, `archived_delete`
        "query_interface": None,  # string - Filter results by this this interface type. Valid values: `web`, `ftp`, `robot`, `jsapi`, `webdesktopapi`, `sftp`, `dav`, `desktop`, `restapi`, `scim`, `office`, `mobile`, `as2`, `inbound_email`, `remote`, `inbound_s3`
        "query_user_id": None,  # string - Return results that are actions performed by the user indicated by this User ID
        "query_file_id": None,  # string - Return results that are file actions related to the file indicated by this File ID
        "query_parent_id": None,  # string - Return results that are file actions inside the parent folder specified by this folder ID
        "query_path": None,  # string - Return results that are file actions related to paths matching this pattern.
        "query_folder": None,  # string - Return results that are file actions related to files or folders inside folder paths matching this pattern.
        "query_src": None,  # string - Return results that are file moves originating from paths matching this pattern.
        "query_destination": None,  # string - Return results that are file moves with paths matching this pattern as destination.
        "query_ip": None,  # string - Filter results by this IP address.
        "query_username": None,  # string - Filter results by this username.
        "query_failure_type": None,  # string - If searching for Histories about login failures, this parameter restricts results to failures of this specific type.  Valid values: `expired_trial`, `account_overdue`, `locked_out`, `ip_mismatch`, `password_mismatch`, `site_mismatch`, `username_not_found`, `none`, `no_ftp_permission`, `no_web_permission`, `no_directory`, `errno_enoent`, `no_sftp_permission`, `no_dav_permission`, `no_restapi_permission`, `key_mismatch`, `region_mismatch`, `expired_access`, `desktop_ip_mismatch`, `desktop_api_key_not_used_quickly_enough`, `disabled`, `country_mismatch`, `insecure_ftp`, `insecure_cipher`, `rate_limited`, `no_s3_compatible_endpoint_permission`, `mobile_ip_mismatch`, `mobile_api_key_not_used_quickly_enough`, `desktop_app_disabled`, `mobile_app_disabled`
        "query_target_id": None,  # string - If searching for Histories about specific objects (such as Users, or API Keys), this parameter restricts results to objects that match this ID.
        "query_target_name": None,  # string - If searching for Histories about Users, Groups or other objects with names, this parameter restricts results to objects with this name/username.
        "query_target_permission": None,  # string - If searching for Histories about Permissions, this parameter restricts results to permissions of this level.
        "query_target_user_id": None,  # string - If searching for Histories about API keys, this parameter restricts results to API keys created by/for this user ID.
        "query_target_username": None,  # string - If searching for Histories about API keys, this parameter restricts results to API keys created by/for this username.
        "query_target_platform": None,  # string - If searching for Histories about API keys, this parameter restricts results to API keys associated with this platform.
        "query_target_permission_set": None,  # string - If searching for Histories about API keys, this parameter restricts results to API keys with this permission set.
        "results_url": None,  # string - If `status` is `ready`, this will be a URL where all the results can be downloaded at once as a CSV.
        "user_id": None,  # int64 - User ID.  Provide a value of `0` to operate the current session's user.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    workspace_id: int | None
    id: int | None
    history_version: str | None
    start_at: str | None
    end_at: str | None
    status: str | None
    query_action: str | None
    query_interface: str | None
    query_user_id: str | None
    query_file_id: str | None
    query_parent_id: str | None
    query_path: str | None
    query_folder: str | None
    query_src: str | None
    query_destination: str | None
    query_ip: str | None
    query_username: str | None
    query_failure_type: str | None
    query_target_id: str | None
    query_target_name: str | None
    query_target_permission: str | None
    query_target_user_id: str | None
    query_target_username: str | None
    query_target_platform: str | None
    query_target_permission_set: str | None
    results_url: str | None
    user_id: int | None

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
        ) in HistoryExport.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in HistoryExport.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def save(self) -> None:
        """Create this object on the server, taking in place the record it
        returns. One that already has an id cannot be updated, and raises
        NotImplementedError."""
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The HistoryExport object doesn't support updates."
            )
        else:
            new_obj = HistoryExportResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class HistoryExportResource:
    """HistoryExport operations that use one client's configuration.

    Get one from a client, such as ``client.history_export``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> HistoryExport:
        """Parameters:
        id (required) - int64 - History Export ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> HistoryExport:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/history_exports/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, HistoryExport)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> HistoryExport:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> HistoryExport:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        start_at - string - Start date/time of export range.
        end_at - string - End date/time of export range.
        query_action - string - Filter results by this this action type. Valid values: `create`, `read`, `update`, `destroy`, `move`, `login`, `failedlogin`, `copy`, `user_create`, `user_update`, `user_destroy`, `group_create`, `group_update`, `group_destroy`, `permission_create`, `permission_destroy`, `api_key_create`, `api_key_update`, `api_key_destroy`, `archived_delete`
        query_interface - string - Filter results by this this interface type. Valid values: `web`, `ftp`, `robot`, `jsapi`, `webdesktopapi`, `sftp`, `dav`, `desktop`, `restapi`, `scim`, `office`, `mobile`, `as2`, `inbound_email`, `remote`, `inbound_s3`
        query_user_id - string - Return results that are actions performed by the user indicated by this User ID
        query_file_id - string - Return results that are file actions related to the file indicated by this File ID
        query_parent_id - string - Return results that are file actions inside the parent folder specified by this folder ID
        query_path - string - Return results that are file actions related to paths matching this pattern.
        query_folder - string - Return results that are file actions related to files or folders inside folder paths matching this pattern.
        query_src - string - Return results that are file moves originating from paths matching this pattern.
        query_destination - string - Return results that are file moves with paths matching this pattern as destination.
        query_ip - string - Filter results by this IP address.
        query_username - string - Filter results by this username.
        query_failure_type - string - If searching for Histories about login failures, this parameter restricts results to failures of this specific type.  Valid values: `expired_trial`, `account_overdue`, `locked_out`, `ip_mismatch`, `password_mismatch`, `site_mismatch`, `username_not_found`, `none`, `no_ftp_permission`, `no_web_permission`, `no_directory`, `errno_enoent`, `no_sftp_permission`, `no_dav_permission`, `no_restapi_permission`, `key_mismatch`, `region_mismatch`, `expired_access`, `desktop_ip_mismatch`, `desktop_api_key_not_used_quickly_enough`, `disabled`, `country_mismatch`, `insecure_ftp`, `insecure_cipher`, `rate_limited`, `no_s3_compatible_endpoint_permission`, `mobile_ip_mismatch`, `mobile_api_key_not_used_quickly_enough`, `desktop_app_disabled`, `mobile_app_disabled`
        query_target_id - string - If searching for Histories about specific objects (such as Users, or API Keys), this parameter restricts results to objects that match this ID.
        query_target_name - string - If searching for Histories about Users, Groups or other objects with names, this parameter restricts results to objects with this name/username.
        query_target_permission - string - If searching for Histories about Permissions, this parameter restricts results to permissions of this level.
        query_target_user_id - string - If searching for Histories about API keys, this parameter restricts results to API keys created by/for this user ID.
        query_target_username - string - If searching for Histories about API keys, this parameter restricts results to API keys created by/for this username.
        query_target_platform - string - If searching for Histories about API keys, this parameter restricts results to API keys associated with this platform.
        query_target_permission_set - string - If searching for Histories about API keys, this parameter restricts results to API keys with this permission set.
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "start_at" in params and not isinstance(params["start_at"], str):
            raise InvalidParameterError(
                "Bad parameter: start_at must be an str"
            )
        if "end_at" in params and not isinstance(params["end_at"], str):
            raise InvalidParameterError("Bad parameter: end_at must be an str")
        if "query_action" in params and not isinstance(
            params["query_action"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_action must be an str"
            )
        if "query_interface" in params and not isinstance(
            params["query_interface"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_interface must be an str"
            )
        if "query_user_id" in params and not isinstance(
            params["query_user_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_user_id must be an str"
            )
        if "query_file_id" in params and not isinstance(
            params["query_file_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_file_id must be an str"
            )
        if "query_parent_id" in params and not isinstance(
            params["query_parent_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_parent_id must be an str"
            )
        if "query_path" in params and not isinstance(
            params["query_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_path must be an str"
            )
        if "query_folder" in params and not isinstance(
            params["query_folder"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_folder must be an str"
            )
        if "query_src" in params and not isinstance(params["query_src"], str):
            raise InvalidParameterError(
                "Bad parameter: query_src must be an str"
            )
        if "query_destination" in params and not isinstance(
            params["query_destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_destination must be an str"
            )
        if "query_ip" in params and not isinstance(params["query_ip"], str):
            raise InvalidParameterError(
                "Bad parameter: query_ip must be an str"
            )
        if "query_username" in params and not isinstance(
            params["query_username"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_username must be an str"
            )
        if "query_failure_type" in params and not isinstance(
            params["query_failure_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_failure_type must be an str"
            )
        if "query_target_id" in params and not isinstance(
            params["query_target_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_target_id must be an str"
            )
        if "query_target_name" in params and not isinstance(
            params["query_target_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_target_name must be an str"
            )
        if "query_target_permission" in params and not isinstance(
            params["query_target_permission"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_target_permission must be an str"
            )
        if "query_target_user_id" in params and not isinstance(
            params["query_target_user_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_target_user_id must be an str"
            )
        if "query_target_username" in params and not isinstance(
            params["query_target_username"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_target_username must be an str"
            )
        if "query_target_platform" in params and not isinstance(
            params["query_target_platform"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_target_platform must be an str"
            )
        if "query_target_permission_set" in params and not isinstance(
            params["query_target_permission_set"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_target_permission_set must be an str"
            )
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/history_exports", params)
        return operation.decode_model(response, HistoryExport)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> HistoryExport:
        """A new HistoryExport with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = HistoryExport(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = HistoryExportResource(LEGACY)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> HistoryExport:
    """Parameters:
    id (required) - int64 - History Export ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> HistoryExport:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> HistoryExport:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    start_at - string - Start date/time of export range.
    end_at - string - End date/time of export range.
    query_action - string - Filter results by this this action type. Valid values: `create`, `read`, `update`, `destroy`, `move`, `login`, `failedlogin`, `copy`, `user_create`, `user_update`, `user_destroy`, `group_create`, `group_update`, `group_destroy`, `permission_create`, `permission_destroy`, `api_key_create`, `api_key_update`, `api_key_destroy`, `archived_delete`
    query_interface - string - Filter results by this this interface type. Valid values: `web`, `ftp`, `robot`, `jsapi`, `webdesktopapi`, `sftp`, `dav`, `desktop`, `restapi`, `scim`, `office`, `mobile`, `as2`, `inbound_email`, `remote`, `inbound_s3`
    query_user_id - string - Return results that are actions performed by the user indicated by this User ID
    query_file_id - string - Return results that are file actions related to the file indicated by this File ID
    query_parent_id - string - Return results that are file actions inside the parent folder specified by this folder ID
    query_path - string - Return results that are file actions related to paths matching this pattern.
    query_folder - string - Return results that are file actions related to files or folders inside folder paths matching this pattern.
    query_src - string - Return results that are file moves originating from paths matching this pattern.
    query_destination - string - Return results that are file moves with paths matching this pattern as destination.
    query_ip - string - Filter results by this IP address.
    query_username - string - Filter results by this username.
    query_failure_type - string - If searching for Histories about login failures, this parameter restricts results to failures of this specific type.  Valid values: `expired_trial`, `account_overdue`, `locked_out`, `ip_mismatch`, `password_mismatch`, `site_mismatch`, `username_not_found`, `none`, `no_ftp_permission`, `no_web_permission`, `no_directory`, `errno_enoent`, `no_sftp_permission`, `no_dav_permission`, `no_restapi_permission`, `key_mismatch`, `region_mismatch`, `expired_access`, `desktop_ip_mismatch`, `desktop_api_key_not_used_quickly_enough`, `disabled`, `country_mismatch`, `insecure_ftp`, `insecure_cipher`, `rate_limited`, `no_s3_compatible_endpoint_permission`, `mobile_ip_mismatch`, `mobile_api_key_not_used_quickly_enough`, `desktop_app_disabled`, `mobile_app_disabled`
    query_target_id - string - If searching for Histories about specific objects (such as Users, or API Keys), this parameter restricts results to objects that match this ID.
    query_target_name - string - If searching for Histories about Users, Groups or other objects with names, this parameter restricts results to objects with this name/username.
    query_target_permission - string - If searching for Histories about Permissions, this parameter restricts results to permissions of this level.
    query_target_user_id - string - If searching for Histories about API keys, this parameter restricts results to API keys created by/for this user ID.
    query_target_username - string - If searching for Histories about API keys, this parameter restricts results to API keys created by/for this username.
    query_target_platform - string - If searching for Histories about API keys, this parameter restricts results to API keys associated with this platform.
    query_target_permission_set - string - If searching for Histories about API keys, this parameter restricts results to API keys with this permission set.
    """
    return _legacy_resource.create(params, options)


def new(*args, **kwargs) -> HistoryExport:
    return HistoryExport(*args, **kwargs)
