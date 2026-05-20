import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class EventTarget:
    default_attributes = {
        "id": None,  # int64 - Event Target ID
        "name": None,  # string - Event Target name.
        "target_type": None,  # string - Event Target type.
        "workspace_id": None,  # int64 - Workspace ID. 0 means the default workspace or site-wide.
        "apply_to_all_workspaces": None,  # boolean - If true, this default-workspace target can receive events from all workspaces.
        "enabled": None,  # boolean - Whether this Event Target can receive events.
        "config": None,  # object - Event Target configuration.
        "delivery_policy": None,  # object - Event Target delivery policy. Email targets support batch_interval in seconds, between 600 and 86400.
        "created_at": None,  # date-time - Event Target create date/time.
        "updated_at": None,  # date-time - Event Target update date/time.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

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

    # Parameters:
    #   name - string - Event Target name.
    #   workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
    #   apply_to_all_workspaces - boolean - If true, this default-workspace target can receive events from all workspaces.
    #   target_type - string - Event Target type.
    #   enabled - boolean - Whether this Event Target can receive events.
    #   config - object - Event Target configuration.
    #   delivery_policy - object - Event Target delivery policy. Email targets support batch_interval in seconds, between 600 and 86400.
    def update(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "workspace_id" in params and not isinstance(
            params["workspace_id"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "target_type" in params and not isinstance(
            params["target_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: target_type must be an str"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/event_targets/{id}".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    def delete(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        Api.send_request(
            "DELETE",
            "/event_targets/{id}".format(id=params["id"]),
            params,
            self.options,
        )

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            new_obj = self.update(self.get_attributes())
            self.set_attributes(new_obj.get_attributes())
            return True
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `enabled` and `workspace_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `enabled`, `target_type` or `workspace_id`. Valid field combinations are `[ enabled, target_type ]`, `[ workspace_id, enabled ]` or `[ workspace_id, enabled, target_type ]`.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    return ListObj(EventTarget, "GET", "/event_targets", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Event Target ID.
def find(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "GET", "/event_targets/{id}".format(id=params["id"]), params, options
    )
    return EventTarget(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   name (required) - string - Event Target name.
#   workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
#   apply_to_all_workspaces - boolean - If true, this default-workspace target can receive events from all workspaces.
#   target_type (required) - string - Event Target type.
#   enabled - boolean - Whether this Event Target can receive events.
#   config (required) - object - Event Target configuration.
#   delivery_policy - object - Event Target delivery policy. Email targets support batch_interval in seconds, between 600 and 86400.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "workspace_id" in params and not isinstance(
        params["workspace_id"], int
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
    if "target_type" in params and not isinstance(params["target_type"], str):
        raise InvalidParameterError(
            "Bad parameter: target_type must be an str"
        )
    if "enabled" in params and not isinstance(params["enabled"], bool):
        raise InvalidParameterError("Bad parameter: enabled must be an bool")
    if "config" in params and not isinstance(params["config"], dict):
        raise InvalidParameterError("Bad parameter: config must be an dict")
    if "delivery_policy" in params and not isinstance(
        params["delivery_policy"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: delivery_policy must be an dict"
        )
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    if "target_type" not in params:
        raise MissingParameterError("Parameter missing: target_type")
    if "config" not in params:
        raise MissingParameterError("Parameter missing: config")
    response, options = Api.send_request(
        "POST", "/event_targets", params, options
    )
    return EventTarget(response.data, options)


# Parameters:
#   name - string - Event Target name.
#   workspace_id - int64 - Workspace ID. 0 means the default workspace or site-wide.
#   apply_to_all_workspaces - boolean - If true, this default-workspace target can receive events from all workspaces.
#   target_type - string - Event Target type.
#   enabled - boolean - Whether this Event Target can receive events.
#   config - object - Event Target configuration.
#   delivery_policy - object - Event Target delivery policy. Email targets support batch_interval in seconds, between 600 and 86400.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "workspace_id" in params and not isinstance(
        params["workspace_id"], int
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
    if "target_type" in params and not isinstance(params["target_type"], str):
        raise InvalidParameterError(
            "Bad parameter: target_type must be an str"
        )
    if "enabled" in params and not isinstance(params["enabled"], bool):
        raise InvalidParameterError("Bad parameter: enabled must be an bool")
    if "config" in params and not isinstance(params["config"], dict):
        raise InvalidParameterError("Bad parameter: config must be an dict")
    if "delivery_policy" in params and not isinstance(
        params["delivery_policy"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: delivery_policy must be an dict"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH", "/event_targets/{id}".format(id=params["id"]), params, options
    )
    return EventTarget(response.data, options)


def delete(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    Api.send_request(
        "DELETE",
        "/event_targets/{id}".format(id=params["id"]),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return EventTarget(*args, **kwargs)
