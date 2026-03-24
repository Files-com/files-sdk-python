import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ExpectationIncident:
    default_attributes = {
        "id": None,  # int64 - Expectation Incident ID
        "workspace_id": None,  # int64 - Workspace ID. `0` means the default workspace.
        "expectation_id": None,  # int64 - Expectation ID.
        "status": None,  # string - Incident status.
        "opened_at": None,  # date-time - When the incident was opened.
        "last_failed_at": None,  # date-time - When the most recent failing evaluation contributing to the incident occurred.
        "acknowledged_at": None,  # date-time - When the incident was acknowledged.
        "snoozed_until": None,  # date-time - When the current snooze expires.
        "resolved_at": None,  # date-time - When the incident was resolved.
        "opened_by_evaluation_id": None,  # int64 - Evaluation that first opened the incident.
        "last_evaluation_id": None,  # int64 - Most recent evaluation linked to the incident.
        "resolved_by_evaluation_id": None,  # int64 - Evaluation that resolved the incident.
        "summary": None,  # object - Compact incident summary payload.
        "created_at": None,  # date-time - Creation time.
        "updated_at": None,  # date-time - Last update time.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (
            attribute,
            default_value,
        ) in ExpectationIncident.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ExpectationIncident.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    # Resolve an expectation incident
    def resolve(self, params=None):
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
        response, _options = Api.send_request(
            "POST",
            "/expectation_incidents/{id}/resolve".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    # Snooze an expectation incident until a specified time
    #
    # Parameters:
    #   snoozed_until (required) - string - Time until which the incident should remain snoozed.
    def snooze(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "snoozed_until" not in params:
            raise MissingParameterError("Parameter missing: snoozed_until")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "snoozed_until" in params and not isinstance(
            params["snoozed_until"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: snoozed_until must be an str"
            )
        response, _options = Api.send_request(
            "POST",
            "/expectation_incidents/{id}/snooze".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    # Acknowledge an expectation incident
    def acknowledge(self, params=None):
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
        response, _options = Api.send_request(
            "POST",
            "/expectation_incidents/{id}/acknowledge".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `created_at` or `expectation_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `expectation_id` and `workspace_id`. Valid field combinations are `[ workspace_id, expectation_id ]`.
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
    return ListObj(
        ExpectationIncident, "GET", "/expectation_incidents", params, options
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Expectation Incident ID.
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
        "GET",
        "/expectation_incidents/{id}".format(id=params["id"]),
        params,
        options,
    )
    return ExpectationIncident(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Resolve an expectation incident
def resolve(id, params=None, options=None):
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
        "POST",
        "/expectation_incidents/{id}/resolve".format(id=params["id"]),
        params,
        options,
    )
    return ExpectationIncident(response.data, options)


# Snooze an expectation incident until a specified time
#
# Parameters:
#   snoozed_until (required) - string - Time until which the incident should remain snoozed.
def snooze(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "snoozed_until" in params and not isinstance(
        params["snoozed_until"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: snoozed_until must be an str"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    if "snoozed_until" not in params:
        raise MissingParameterError("Parameter missing: snoozed_until")
    response, options = Api.send_request(
        "POST",
        "/expectation_incidents/{id}/snooze".format(id=params["id"]),
        params,
        options,
    )
    return ExpectationIncident(response.data, options)


# Acknowledge an expectation incident
def acknowledge(id, params=None, options=None):
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
        "POST",
        "/expectation_incidents/{id}/acknowledge".format(id=params["id"]),
        params,
        options,
    )
    return ExpectationIncident(response.data, options)


def new(*args, **kwargs):
    return ExpectationIncident(*args, **kwargs)
