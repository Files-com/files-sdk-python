import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.models.automation_run import AutomationRun
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


class SharedWorkflow:
    """A shared workflow record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Shared Workflow ID.
        name: string - Name displayed to recipients.
        description: string - Description displayed to recipients.
        submission_revision: string - Revision required when submitting a Shared Workflow run.
        form_fields: array(object) - Current custom questions in display order.
    """

    default_attributes = {
        "id": None,  # int64 - Shared Workflow ID.
        "name": None,  # string - Name displayed to recipients.
        "description": None,  # string - Description displayed to recipients.
        "submission_revision": None,  # string - Revision required when submitting a Shared Workflow run.
        "form_fields": None,  # array(object) - Current custom questions in display order.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    name: str | None
    description: str | None
    submission_revision: str | None
    form_fields: builtins.list[dict[str, Any]] | None

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
        ) in SharedWorkflow.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SharedWorkflow.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def run_workflow(
        self, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Run a Shared Workflow

        Parameters:
          submission_revision (required) - string - Revision returned when opening the Shared Workflow.
          submission_id (required) - string - Client-generated UUID used to retry the same submission without starting another run.
          file_path (required) - string - Path of a file the recipient can read, including a file uploaded to a Snapshot created for this workflow.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "submission_revision" not in params:
            raise MissingParameterError(
                "Parameter missing: submission_revision"
            )
        if "submission_id" not in params:
            raise MissingParameterError("Parameter missing: submission_id")
        if "file_path" not in params:
            raise MissingParameterError("Parameter missing: file_path")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "submission_revision" in params and not isinstance(
            params["submission_revision"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: submission_revision must be an str"
            )
        if "submission_id" in params and not isinstance(
            params["submission_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: submission_id must be an str"
            )
        if "file_path" in params and not isinstance(params["file_path"], str):
            raise InvalidParameterError(
                "Bad parameter: file_path must be an str"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "POST",
            "/shared_workflows/" + path_value(params["id"]) + "/run_workflow",
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data


class SharedWorkflowResource:
    """SharedWorkflow operations that use one client's configuration.

    Get one from a client, such as ``client.shared_workflow``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SharedWorkflow]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
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
        operation = Operation.start(self._scope, options)
        return ListObj(
            SharedWorkflow, "GET", "/shared_workflows", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SharedWorkflow]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SharedWorkflow:
        """Parameters:
        id (required) - int64 - Shared Workflow ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> SharedWorkflow:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/shared_workflows/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, SharedWorkflow)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SharedWorkflow:
        """The same as find()."""
        return self.find(id, params, options)

    def find_run(
        self,
        id: int,
        run_id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AutomationRun:
        """Parameters:
        id (required) - int64 - Shared Workflow ID.
        run_id (required) - int64 - ID of the run returned by the Shared Workflow submission.
        """
        return self.__find_run({"id": id, "run_id": run_id}, params, options)

    def __find_run(
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
        if "run_id" in params and (
            not isinstance(params["run_id"], int)
            or isinstance(params["run_id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: run_id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "run_id" not in params:
            raise MissingParameterError("Parameter missing: run_id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET",
            "/shared_workflows/"
            + path_value(params["id"])
            + "/runs/"
            + path_value(params["run_id"]),
            params,
        )
        return operation.decode_model(response, AutomationRun)

    def run_workflow(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AutomationRun:
        """Run a Shared Workflow

        Parameters:
          submission_revision (required) - string - Revision returned when opening the Shared Workflow.
          submission_id (required) - string - Client-generated UUID used to retry the same submission without starting another run.
          file_path (required) - string - Path of a file the recipient can read, including a file uploaded to a Snapshot created for this workflow.
        """
        return self.__run_workflow({"id": id}, params, options)

    def __run_workflow(
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
        if "submission_revision" in params and not isinstance(
            params["submission_revision"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: submission_revision must be an str"
            )
        if "submission_id" in params and not isinstance(
            params["submission_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: submission_id must be an str"
            )
        if "file_path" in params and not isinstance(params["file_path"], str):
            raise InvalidParameterError(
                "Bad parameter: file_path must be an str"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "submission_revision" not in params:
            raise MissingParameterError(
                "Parameter missing: submission_revision"
            )
        if "submission_id" not in params:
            raise MissingParameterError("Parameter missing: submission_id")
        if "file_path" not in params:
            raise MissingParameterError("Parameter missing: file_path")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/shared_workflows/" + path_value(params["id"]) + "/run_workflow",
            params,
        )
        return operation.decode_model(response, AutomationRun)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SharedWorkflow:
        """A new SharedWorkflow with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = SharedWorkflow(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = SharedWorkflowResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SharedWorkflow]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SharedWorkflow]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SharedWorkflow:
    """Parameters:
    id (required) - int64 - Shared Workflow ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SharedWorkflow:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def find_run(
    id: int,
    run_id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AutomationRun:
    """Parameters:
    id (required) - int64 - Shared Workflow ID.
    run_id (required) - int64 - ID of the run returned by the Shared Workflow submission.
    """
    return _legacy_resource.find_run(id, run_id, params, options)


def run_workflow(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AutomationRun:
    """Run a Shared Workflow

    Parameters:
      submission_revision (required) - string - Revision returned when opening the Shared Workflow.
      submission_id (required) - string - Client-generated UUID used to retry the same submission without starting another run.
      file_path (required) - string - Path of a file the recipient can read, including a file uploaded to a Snapshot created for this workflow.
    """
    return _legacy_resource.run_workflow(id, params, options)


def new(*args, **kwargs) -> SharedWorkflow:
    return SharedWorkflow(*args, **kwargs)
