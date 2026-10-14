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


class ExpectationIncident:
    """A expectation incident record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Expectation Incident ID
        workspace_id: int64 - Workspace ID. `0` means the default workspace.
        expectation_id: int64 - Expectation ID.
        status: string - Incident status.
        opened_at: date-time - When the incident was opened.
        last_failed_at: date-time - When the most recent failing evaluation contributing to the incident occurred.
        acknowledged_at: date-time - When the incident was acknowledged.
        snoozed_until: date-time - When the current snooze expires.
        resolved_at: date-time - When the incident was resolved.
        opened_by_evaluation_id: int64 - Evaluation that first opened the incident.
        last_evaluation_id: int64 - Most recent evaluation linked to the incident.
        resolved_by_evaluation_id: int64 - Evaluation that resolved the incident.
        summary: object - Compact incident summary payload.
        created_at: date-time - Creation time.
        updated_at: date-time - Last update time.
    """

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

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    workspace_id: int | None
    expectation_id: int | None
    status: str | None
    opened_at: str | None
    last_failed_at: str | None
    acknowledged_at: str | None
    snoozed_until: str | None
    resolved_at: str | None
    opened_by_evaluation_id: int | None
    last_evaluation_id: int | None
    resolved_by_evaluation_id: int | None
    summary: dict[str, Any] | None
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

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def resolve(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Resolve an expectation incident"""
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
        response = operation.request(
            "POST",
            "/expectation_incidents/" + path_value(params["id"]) + "/resolve",
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def snooze(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Snooze an expectation incident until a specified time

        Parameters:
          snoozed_until (required) - string - Time until which the incident should remain snoozed.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "snoozed_until" not in params:
            raise MissingParameterError("Parameter missing: snoozed_until")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "snoozed_until" in params and not isinstance(
            params["snoozed_until"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: snoozed_until must be an str"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "POST",
            "/expectation_incidents/" + path_value(params["id"]) + "/snooze",
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def acknowledge(
        self, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Acknowledge an expectation incident"""
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
        response = operation.request(
            "POST",
            "/expectation_incidents/"
            + path_value(params["id"])
            + "/acknowledge",
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data


class ExpectationIncidentResource:
    """ExpectationIncident operations that use one client's configuration.

    Get one from a client, such as ``client.expectation_incident``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[ExpectationIncident]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `created_at` or `expectation_id`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `expectation_id` and `workspace_id`. Valid field combinations are `[ workspace_id, expectation_id ]`.
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
            ExpectationIncident,
            "GET",
            "/expectation_incidents",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[ExpectationIncident]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ExpectationIncident:
        """Parameters:
        id (required) - int64 - Expectation Incident ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ExpectationIncident:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/expectation_incidents/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, ExpectationIncident)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ExpectationIncident:
        """The same as find()."""
        return self.find(id, params, options)

    def resolve(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ExpectationIncident:
        """Resolve an expectation incident"""
        return self.__resolve({"id": id}, params, options)

    def __resolve(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ExpectationIncident:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/expectation_incidents/" + path_value(params["id"]) + "/resolve",
            params,
        )
        return operation.decode_model(response, ExpectationIncident)

    def snooze(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ExpectationIncident:
        """Snooze an expectation incident until a specified time

        Parameters:
          snoozed_until (required) - string - Time until which the incident should remain snoozed.
        """
        return self.__snooze({"id": id}, params, options)

    def __snooze(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ExpectationIncident:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
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
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/expectation_incidents/" + path_value(params["id"]) + "/snooze",
            params,
        )
        return operation.decode_model(response, ExpectationIncident)

    def acknowledge(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ExpectationIncident:
        """Acknowledge an expectation incident"""
        return self.__acknowledge({"id": id}, params, options)

    def __acknowledge(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ExpectationIncident:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/expectation_incidents/"
            + path_value(params["id"])
            + "/acknowledge",
            params,
        )
        return operation.decode_model(response, ExpectationIncident)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ExpectationIncident:
        """A new ExpectationIncident with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = ExpectationIncident(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = ExpectationIncidentResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[ExpectationIncident]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `created_at` or `expectation_id`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `expectation_id` and `workspace_id`. Valid field combinations are `[ workspace_id, expectation_id ]`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[ExpectationIncident]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ExpectationIncident:
    """Parameters:
    id (required) - int64 - Expectation Incident ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ExpectationIncident:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def resolve(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ExpectationIncident:
    """Resolve an expectation incident"""
    return _legacy_resource.resolve(id, params, options)


def snooze(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ExpectationIncident:
    """Snooze an expectation incident until a specified time

    Parameters:
      snoozed_until (required) - string - Time until which the incident should remain snoozed.
    """
    return _legacy_resource.snooze(id, params, options)


def acknowledge(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ExpectationIncident:
    """Acknowledge an expectation incident"""
    return _legacy_resource.acknowledge(id, params, options)


def new(*args, **kwargs) -> ExpectationIncident:
    return ExpectationIncident(*args, **kwargs)
