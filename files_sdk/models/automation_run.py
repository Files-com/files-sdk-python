import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.models.automation_execution_node import AutomationExecutionNode
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


class AutomationRun:
    """A automation run record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - ID.
        automation_id: int64 - ID of the associated Automation.
        automation_version_id: int64 - ID of the immutable Automation version pinned by this run.
        version: int64 - Pinned Automation v2 definition version.
        workspace_id: int64 - Workspace ID.
        cancel_requested_at: date-time - Date/time at which cancellation was requested.
        completed_at: date-time - Automation run completion/failure date/time.
        created_at: date-time - Automation run start date/time.
        retry_at: date-time - If set, this automation will be retried at this date/time due to `failure` or `partial_failure`.
        retried_at: date-time - If set, this Automation run was retried due to `failure` or `partial_failure`.
        retried_in_run_id: int64 - ID of the run that is or will be retrying this run.
        retry_of_run_id: int64 - ID of the original run that this run is retrying.
        rerun_of_run_id: int64 - ID of the run whose persisted node outputs this run reused.
        rerun_from_node_id: string - Node at which this run resumed execution.
        runtime: double - Automation run runtime.
        status: string - The status of the AutomationRun. One of `queued`, `running`, `success`, `partial_failure`, `failure`, `skipped`, or `canceled`.
        successful_operations: int64 - Count of successful operations.
        failed_operations: int64 - Count of failed operations.
        definition: object - Automation definition snapshot pinned by this run. For performance reasons, this is not provided when listing Automation runs.
        node_states: object - Status and execution stage for each node in this run. For performance reasons, this is not provided when listing Automation runs.
        execution_nodes: array(object) - Execution status, timing, and bounded output summaries for each node. For performance reasons, this is not provided when listing Automation runs.
        journal_url: string - Link to the run journal artifact.
        status_messages_url: string - Link to status messages log file.
    """

    default_attributes = {
        "id": None,  # int64 - ID.
        "automation_id": None,  # int64 - ID of the associated Automation.
        "automation_version_id": None,  # int64 - ID of the immutable Automation version pinned by this run.
        "version": None,  # int64 - Pinned Automation v2 definition version.
        "workspace_id": None,  # int64 - Workspace ID.
        "cancel_requested_at": None,  # date-time - Date/time at which cancellation was requested.
        "completed_at": None,  # date-time - Automation run completion/failure date/time.
        "created_at": None,  # date-time - Automation run start date/time.
        "retry_at": None,  # date-time - If set, this automation will be retried at this date/time due to `failure` or `partial_failure`.
        "retried_at": None,  # date-time - If set, this Automation run was retried due to `failure` or `partial_failure`.
        "retried_in_run_id": None,  # int64 - ID of the run that is or will be retrying this run.
        "retry_of_run_id": None,  # int64 - ID of the original run that this run is retrying.
        "rerun_of_run_id": None,  # int64 - ID of the run whose persisted node outputs this run reused.
        "rerun_from_node_id": None,  # string - Node at which this run resumed execution.
        "runtime": None,  # double - Automation run runtime.
        "status": None,  # string - The status of the AutomationRun. One of `queued`, `running`, `success`, `partial_failure`, `failure`, `skipped`, or `canceled`.
        "successful_operations": None,  # int64 - Count of successful operations.
        "failed_operations": None,  # int64 - Count of failed operations.
        "definition": None,  # object - Automation definition snapshot pinned by this run. For performance reasons, this is not provided when listing Automation runs.
        "node_states": None,  # object - Status and execution stage for each node in this run. For performance reasons, this is not provided when listing Automation runs.
        "execution_nodes": None,  # array(object) - Execution status, timing, and bounded output summaries for each node. For performance reasons, this is not provided when listing Automation runs.
        "journal_url": None,  # string - Link to the run journal artifact.
        "status_messages_url": None,  # string - Link to status messages log file.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    automation_id: int | None
    automation_version_id: int | None
    version: int | None
    workspace_id: int | None
    cancel_requested_at: str | None
    completed_at: str | None
    created_at: str | None
    retry_at: str | None
    retried_at: str | None
    retried_in_run_id: int | None
    retry_of_run_id: int | None
    rerun_of_run_id: int | None
    rerun_from_node_id: str | None
    runtime: float | None
    status: str | None
    successful_operations: int | None
    failed_operations: int | None
    definition: dict[str, Any] | None
    node_states: dict[str, Any] | None
    execution_nodes: builtins.list[dict[str, Any]] | None
    journal_url: str | None
    status_messages_url: str | None

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
        ) in AutomationRun.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in AutomationRun.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def cancel(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Cancel Automation Run"""
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
            "/automation_runs/" + path_value(params["id"]) + "/cancel",
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def rerun(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Re-run Automation from Node

        Parameters:
          node_id (required) - string - Node ID at which execution should resume.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "node_id" not in params:
            raise MissingParameterError("Parameter missing: node_id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "node_id" in params and not isinstance(params["node_id"], str):
            raise InvalidParameterError(
                "Bad parameter: node_id must be an str"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "POST",
            "/automation_runs/" + path_value(params["id"]) + "/rerun",
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data


class AutomationRunResource:
    """AutomationRun operations that use one client's configuration.

    Get one from a client, such as ``client.automation_run``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[AutomationRun]:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `automation_id`, `created_at` or `status`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `status`, `workspace_id` or `automation_id`. Valid field combinations are `[ workspace_id, status ]`, `[ automation_id, status ]`, `[ workspace_id, automation_id ]` or `[ workspace_id, automation_id, status ]`.
        automation_id (required) - int64 - ID of the associated Automation.
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
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
        if "automation_id" in params and (
            not isinstance(params["automation_id"], int)
            or isinstance(params["automation_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: automation_id must be an int"
            )
        if "automation_id" not in params:
            raise MissingParameterError("Parameter missing: automation_id")
        operation = Operation.start(self._scope, options)
        return ListObj(
            AutomationRun, "GET", "/automation_runs", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[AutomationRun]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AutomationRun:
        """Parameters:
        id (required) - int64 - Automation Run ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> AutomationRun:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/automation_runs/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, AutomationRun)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AutomationRun:
        """The same as find()."""
        return self.find(id, params, options)

    def find_node(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AutomationExecutionNode:
        """Parameters:
        id (required) - int64 - Automation Run ID.
        node_id (required) - string - Node ID from the pinned Automation definition.
        """
        return self.__find_node({"id": id}, params, options)

    def __find_node(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> AutomationExecutionNode:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "node_id" in params and not isinstance(params["node_id"], str):
            raise InvalidParameterError(
                "Bad parameter: node_id must be an str"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "node_id" not in params:
            raise MissingParameterError("Parameter missing: node_id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET",
            "/automation_runs/" + path_value(params["id"]) + "/node",
            params,
        )
        return operation.decode_model(response, AutomationExecutionNode)

    def cancel(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AutomationRun:
        """Cancel Automation Run"""
        return self.__cancel({"id": id}, params, options)

    def __cancel(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> AutomationRun:
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
            "/automation_runs/" + path_value(params["id"]) + "/cancel",
            params,
        )
        return operation.decode_model(response, AutomationRun)

    def rerun(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AutomationRun:
        """Re-run Automation from Node

        Parameters:
          node_id (required) - string - Node ID at which execution should resume.
        """
        return self.__rerun({"id": id}, params, options)

    def __rerun(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> AutomationRun:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "node_id" in params and not isinstance(params["node_id"], str):
            raise InvalidParameterError(
                "Bad parameter: node_id must be an str"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "node_id" not in params:
            raise MissingParameterError("Parameter missing: node_id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/automation_runs/" + path_value(params["id"]) + "/rerun",
            params,
        )
        return operation.decode_model(response, AutomationRun)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AutomationRun:
        """A new AutomationRun with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = AutomationRun(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = AutomationRunResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[AutomationRun]:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `automation_id`, `created_at` or `status`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `status`, `workspace_id` or `automation_id`. Valid field combinations are `[ workspace_id, status ]`, `[ automation_id, status ]`, `[ workspace_id, automation_id ]` or `[ workspace_id, automation_id, status ]`.
    automation_id (required) - int64 - ID of the associated Automation.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[AutomationRun]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AutomationRun:
    """Parameters:
    id (required) - int64 - Automation Run ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AutomationRun:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def find_node(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AutomationExecutionNode:
    """Parameters:
    id (required) - int64 - Automation Run ID.
    node_id (required) - string - Node ID from the pinned Automation definition.
    """
    return _legacy_resource.find_node(id, params, options)


def cancel(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AutomationRun:
    """Cancel Automation Run"""
    return _legacy_resource.cancel(id, params, options)


def rerun(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AutomationRun:
    """Re-run Automation from Node

    Parameters:
      node_id (required) - string - Node ID at which execution should resume.
    """
    return _legacy_resource.rerun(id, params, options)


def new(*args, **kwargs) -> AutomationRun:
    return AutomationRun(*args, **kwargs)
