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


class EventTarget:
    """A event target record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Event Target ID
        name: string - Event Target name.
        target_type: string - Event Target type.
        workspace_id: int64 - Workspace ID. 0 means the default workspace or site-wide.
        apply_to_all_workspaces: boolean - If true, this default-workspace target can receive events from all workspaces.
        enabled: boolean - Whether this Event Target can receive events.
        config: object - Event Target configuration. Folder targets accept path and format (json or csv).
        delivery_policy: object - Event Target delivery policy. Email and folder targets support batch_interval in seconds, between 600 and 86400. Slack and Teams support delivery_mode (immediate or subfolder_summary), summary_path (empty string means root), and summary_delay (15–300 seconds, default 60). The summary applies to matching file activity under summary_path; other matching events retain immediate delivery.
        created_at: date-time - Event Target create date/time.
        updated_at: date-time - Event Target update date/time.
    """

    default_attributes = {
        "id": None,  # int64 - Event Target ID
        "name": None,  # string - Event Target name.
        "target_type": None,  # string - Event Target type.
        "workspace_id": None,  # int64 - Workspace ID. 0 means the default workspace or site-wide.
        "apply_to_all_workspaces": None,  # boolean - If true, this default-workspace target can receive events from all workspaces.
        "enabled": None,  # boolean - Whether this Event Target can receive events.
        "config": None,  # object - Event Target configuration. Folder targets accept path and format (json or csv).
        "delivery_policy": None,  # object - Event Target delivery policy. Email and folder targets support batch_interval in seconds, between 600 and 86400. Slack and Teams support delivery_mode (immediate or subfolder_summary), summary_path (empty string means root), and summary_delay (15–300 seconds, default 60). The summary applies to matching file activity under summary_path; other matching events retain immediate delivery.
        "created_at": None,  # date-time - Event Target create date/time.
        "updated_at": None,  # date-time - Event Target update date/time.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    name: str | None
    target_type: str | None
    workspace_id: int | None
    apply_to_all_workspaces: bool | None
    enabled: bool | None
    config: dict[str, Any] | None
    delivery_policy: dict[str, Any] | None
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
        for attribute, default_value in EventTarget.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in EventTarget.default_attributes
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
          name - string - Event Target name.
          workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
          apply_to_all_workspaces - boolean - If true, this default-workspace target can receive events from all workspaces.
          enabled - boolean - Whether this Event Target can receive events.
          config - object - Event Target configuration. Folder targets accept path and format (json or csv).
          delivery_policy - object - Event Target delivery policy. Email and folder targets support batch_interval in seconds, between 600 and 86400. Slack and Teams support delivery_mode (immediate or subfolder_summary), summary_path (empty string means root), and summary_delay (15–300 seconds, default 60). The summary applies to matching file activity under summary_path; other matching events retain immediate delivery.
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
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "apply_to_all_workspaces" in params and isinstance(
            params["apply_to_all_workspaces"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: apply_to_all_workspaces must be an bool"
            )
        if "enabled" in params and isinstance(
            params["enabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: enabled must be an bool"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/event_targets/" + path_value(params["id"]), params
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
            "DELETE", "/event_targets/" + path_value(params["id"]), params
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
            new_obj = EventTargetResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class EventTargetResource:
    """EventTarget operations that use one client's configuration.

    Get one from a client, such as ``client.event_target``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[EventTarget]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `enabled` or `workspace_id`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `enabled`, `target_type` or `workspace_id`. Valid field combinations are `[ enabled, target_type ]`, `[ workspace_id, enabled ]` or `[ workspace_id, enabled, target_type ]`.
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
        return ListObj(EventTarget, "GET", "/event_targets", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[EventTarget]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> EventTarget:
        """Parameters:
        id (required) - int64 - Event Target ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> EventTarget:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/event_targets/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, EventTarget)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> EventTarget:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> EventTarget:
        """Parameters:
        name (required) - string - Event Target name.
        workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
        apply_to_all_workspaces - boolean - If true, this default-workspace target can receive events from all workspaces.
        enabled - boolean - Whether this Event Target can receive events.
        config (required) - object - Event Target configuration. Folder targets accept path and format (json or csv).
        delivery_policy - object - Event Target delivery policy. Email and folder targets support batch_interval in seconds, between 600 and 86400. Slack and Teams support delivery_mode (immediate or subfolder_summary), summary_path (empty string means root), and summary_delay (15–300 seconds, default 60). The summary applies to matching file activity under summary_path; other matching events retain immediate delivery.
        target_type (required) - string - Event Target type.
        """
        params = copy_params(params)
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "apply_to_all_workspaces" in params and not isinstance(
            params["apply_to_all_workspaces"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: apply_to_all_workspaces must be an bool"
            )
        if "enabled" in params and not isinstance(params["enabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: enabled must be an bool"
            )
        if "config" in params and not isinstance(params["config"], dict):
            raise InvalidParameterError(
                "Bad parameter: config must be an dict"
            )
        if "delivery_policy" in params and not isinstance(
            params["delivery_policy"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: delivery_policy must be an dict"
            )
        if "target_type" in params and not isinstance(
            params["target_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: target_type must be an str"
            )
        if "name" not in params:
            raise MissingParameterError("Parameter missing: name")
        if "config" not in params:
            raise MissingParameterError("Parameter missing: config")
        if "target_type" not in params:
            raise MissingParameterError("Parameter missing: target_type")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/event_targets", params)
        return operation.decode_model(response, EventTarget)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> EventTarget:
        """Parameters:
        name - string - Event Target name.
        workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
        apply_to_all_workspaces - boolean - If true, this default-workspace target can receive events from all workspaces.
        enabled - boolean - Whether this Event Target can receive events.
        config - object - Event Target configuration. Folder targets accept path and format (json or csv).
        delivery_policy - object - Event Target delivery policy. Email and folder targets support batch_interval in seconds, between 600 and 86400. Slack and Teams support delivery_mode (immediate or subfolder_summary), summary_path (empty string means root), and summary_delay (15–300 seconds, default 60). The summary applies to matching file activity under summary_path; other matching events retain immediate delivery.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> EventTarget:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "apply_to_all_workspaces" in params and not isinstance(
            params["apply_to_all_workspaces"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: apply_to_all_workspaces must be an bool"
            )
        if "enabled" in params and not isinstance(params["enabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: enabled must be an bool"
            )
        if "config" in params and not isinstance(params["config"], dict):
            raise InvalidParameterError(
                "Bad parameter: config must be an dict"
            )
        if "delivery_policy" in params and not isinstance(
            params["delivery_policy"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: delivery_policy must be an dict"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/event_targets/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, EventTarget)

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
            "DELETE", "/event_targets/" + path_value(params["id"]), params
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
    ) -> EventTarget:
        """A new EventTarget with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = EventTarget(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = EventTargetResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[EventTarget]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `enabled` or `workspace_id`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `enabled`, `target_type` or `workspace_id`. Valid field combinations are `[ enabled, target_type ]`, `[ workspace_id, enabled ]` or `[ workspace_id, enabled, target_type ]`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[EventTarget]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> EventTarget:
    """Parameters:
    id (required) - int64 - Event Target ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> EventTarget:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> EventTarget:
    """Parameters:
    name (required) - string - Event Target name.
    workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
    apply_to_all_workspaces - boolean - If true, this default-workspace target can receive events from all workspaces.
    enabled - boolean - Whether this Event Target can receive events.
    config (required) - object - Event Target configuration. Folder targets accept path and format (json or csv).
    delivery_policy - object - Event Target delivery policy. Email and folder targets support batch_interval in seconds, between 600 and 86400. Slack and Teams support delivery_mode (immediate or subfolder_summary), summary_path (empty string means root), and summary_delay (15–300 seconds, default 60). The summary applies to matching file activity under summary_path; other matching events retain immediate delivery.
    target_type (required) - string - Event Target type.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> EventTarget:
    """Parameters:
    name - string - Event Target name.
    workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
    apply_to_all_workspaces - boolean - If true, this default-workspace target can receive events from all workspaces.
    enabled - boolean - Whether this Event Target can receive events.
    config - object - Event Target configuration. Folder targets accept path and format (json or csv).
    delivery_policy - object - Event Target delivery policy. Email and folder targets support batch_interval in seconds, between 600 and 86400. Slack and Teams support delivery_mode (immediate or subfolder_summary), summary_path (empty string means root), and summary_delay (15–300 seconds, default 60). The summary applies to matching file activity under summary_path; other matching events retain immediate delivery.
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


def new(*args, **kwargs) -> EventTarget:
    return EventTarget(*args, **kwargs)
