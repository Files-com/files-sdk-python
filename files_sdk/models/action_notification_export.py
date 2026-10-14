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


class ActionNotificationExport:
    """A action notification export record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - History Export ID
        workspace_id: int64 - Workspace whose logs are exported. Set to `0` for the default workspace. A null value means a site-wide export.
        export_version: string - Version of the underlying records for the export.
        start_at: date-time - Start date/time of export range.
        end_at: date-time - End date/time of export range.
        status: string - Status of export. Valid values: `building`, `ready`, or `failed`
        query_path: string - Return notifications that were triggered by actions on this specific path.
        query_folder: string - Return notifications that were triggered by actions in this folder.
        query_message: string - Error message associated with the request, if any.
        query_request_method: string - The HTTP request method used by the webhook.
        query_request_url: string - The target webhook URL.
        query_status: string - The HTTP status returned from the server in response to the webhook request.
        query_success: boolean - true if the webhook request succeeded (i.e. returned a 200 or 204 response status). false otherwise.
        results_url: string - If `status` is `ready`, this will be a URL where all the results can be downloaded at once as a CSV.
        user_id: int64 - User ID. Provide a value of `0` to operate the current session's user.
    """

    default_attributes = {
        "id": None,  # int64 - History Export ID
        "workspace_id": None,  # int64 - Workspace whose logs are exported. Set to `0` for the default workspace. A null value means a site-wide export.
        "export_version": None,  # string - Version of the underlying records for the export.
        "start_at": None,  # date-time - Start date/time of export range.
        "end_at": None,  # date-time - End date/time of export range.
        "status": None,  # string - Status of export.  Valid values: `building`, `ready`, or `failed`
        "query_path": None,  # string - Return notifications that were triggered by actions on this specific path.
        "query_folder": None,  # string - Return notifications that were triggered by actions in this folder.
        "query_message": None,  # string - Error message associated with the request, if any.
        "query_request_method": None,  # string - The HTTP request method used by the webhook.
        "query_request_url": None,  # string - The target webhook URL.
        "query_status": None,  # string - The HTTP status returned from the server in response to the webhook request.
        "query_success": None,  # boolean - true if the webhook request succeeded (i.e. returned a 200 or 204 response status). false otherwise.
        "results_url": None,  # string - If `status` is `ready`, this will be a URL where all the results can be downloaded at once as a CSV.
        "user_id": None,  # int64 - User ID.  Provide a value of `0` to operate the current session's user.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    workspace_id: int | None
    export_version: str | None
    start_at: str | None
    end_at: str | None
    status: str | None
    query_path: str | None
    query_folder: str | None
    query_message: str | None
    query_request_method: str | None
    query_request_url: str | None
    query_status: str | None
    query_success: bool | None
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
        ) in ActionNotificationExport.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ActionNotificationExport.default_attributes
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
                "The ActionNotificationExport object doesn't support updates."
            )
        else:
            new_obj = ActionNotificationExportResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class ActionNotificationExportResource:
    """ActionNotificationExport operations that use one client's configuration.

    Get one from a client, such as ``client.action_notification_export``. Each operation
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
    ) -> ActionNotificationExport:
        """Parameters:
        id (required) - int64 - Action Notification Export ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ActionNotificationExport:
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
            "/action_notification_exports/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, ActionNotificationExport)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ActionNotificationExport:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ActionNotificationExport:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        workspace_id - int64 - Workspace whose logs are exported. Set to `0` for the default workspace. A null value means a site-wide export.
        start_at - string - Start date/time of export range.
        end_at - string - End date/time of export range.
        query_message - string - Error message associated with the request, if any.
        query_request_method - string - The HTTP request method used by the webhook.
        query_request_url - string - The target webhook URL.
        query_status - string - The HTTP status returned from the server in response to the webhook request.
        query_success - boolean - true if the webhook request succeeded (i.e. returned a 200 or 204 response status). false otherwise.
        query_path - string - Return notifications that were triggered by actions on this specific path.
        query_folder - string - Return notifications that were triggered by actions in this folder.
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "start_at" in params and not isinstance(params["start_at"], str):
            raise InvalidParameterError(
                "Bad parameter: start_at must be an str"
            )
        if "end_at" in params and not isinstance(params["end_at"], str):
            raise InvalidParameterError("Bad parameter: end_at must be an str")
        if "query_message" in params and not isinstance(
            params["query_message"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_message must be an str"
            )
        if "query_request_method" in params and not isinstance(
            params["query_request_method"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_request_method must be an str"
            )
        if "query_request_url" in params and not isinstance(
            params["query_request_url"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_request_url must be an str"
            )
        if "query_status" in params and not isinstance(
            params["query_status"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: query_status must be an str"
            )
        if "query_success" in params and not isinstance(
            params["query_success"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: query_success must be an bool"
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
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST", "/action_notification_exports", params
        )
        return operation.decode_model(response, ActionNotificationExport)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ActionNotificationExport:
        """A new ActionNotificationExport with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = ActionNotificationExport(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = ActionNotificationExportResource(LEGACY)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ActionNotificationExport:
    """Parameters:
    id (required) - int64 - Action Notification Export ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ActionNotificationExport:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ActionNotificationExport:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    workspace_id - int64 - Workspace whose logs are exported. Set to `0` for the default workspace. A null value means a site-wide export.
    start_at - string - Start date/time of export range.
    end_at - string - End date/time of export range.
    query_message - string - Error message associated with the request, if any.
    query_request_method - string - The HTTP request method used by the webhook.
    query_request_url - string - The target webhook URL.
    query_status - string - The HTTP status returned from the server in response to the webhook request.
    query_success - boolean - true if the webhook request succeeded (i.e. returned a 200 or 204 response status). false otherwise.
    query_path - string - Return notifications that were triggered by actions on this specific path.
    query_folder - string - Return notifications that were triggered by actions in this folder.
    """
    return _legacy_resource.create(params, options)


def new(*args, **kwargs) -> ActionNotificationExport:
    return ActionNotificationExport(*args, **kwargs)
