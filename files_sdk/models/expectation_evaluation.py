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


class ExpectationEvaluation:
    """A expectation evaluation record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - ExpectationEvaluation ID
        workspace_id: int64 - Workspace ID. `0` means the default workspace.
        expectation_id: int64 - Expectation ID.
        status: string - Evaluation status.
        opened_via: string - How the evaluation window was opened.
        opened_at: date-time - When the evaluation row was opened.
        window_start_at: date-time - Logical start of the candidate window.
        window_end_at: date-time - Actual candidate cutoff boundary for the window.
        deadline_at: date-time - Logical due boundary for schedule-driven windows.
        late_acceptance_cutoff_at: date-time - Logical cutoff for late acceptance, when present.
        hard_close_at: date-time - Hard stop after which the window may not remain open.
        closed_at: date-time - When the evaluation row was finalized.
        matched_files: array(object) - Captured evidence for files that matched the window.
        missing_files: array(object) - Captured evidence for required files that were missing.
        criteria_errors: array(string) - Captured criteria failures for the window, including file-scoped FTS errors and returned validation details.
        summary: object - Compact evaluator summary payload.
        created_at: date-time - Creation time.
        updated_at: date-time - Last update time.
    """

    default_attributes = {
        "id": None,  # int64 - ExpectationEvaluation ID
        "workspace_id": None,  # int64 - Workspace ID. `0` means the default workspace.
        "expectation_id": None,  # int64 - Expectation ID.
        "status": None,  # string - Evaluation status.
        "opened_via": None,  # string - How the evaluation window was opened.
        "opened_at": None,  # date-time - When the evaluation row was opened.
        "window_start_at": None,  # date-time - Logical start of the candidate window.
        "window_end_at": None,  # date-time - Actual candidate cutoff boundary for the window.
        "deadline_at": None,  # date-time - Logical due boundary for schedule-driven windows.
        "late_acceptance_cutoff_at": None,  # date-time - Logical cutoff for late acceptance, when present.
        "hard_close_at": None,  # date-time - Hard stop after which the window may not remain open.
        "closed_at": None,  # date-time - When the evaluation row was finalized.
        "matched_files": None,  # array(object) - Captured evidence for files that matched the window.
        "missing_files": None,  # array(object) - Captured evidence for required files that were missing.
        "criteria_errors": None,  # array(string) - Captured criteria failures for the window, including file-scoped FTS errors and returned validation details.
        "summary": None,  # object - Compact evaluator summary payload.
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
    opened_via: str | None
    opened_at: str | None
    window_start_at: str | None
    window_end_at: str | None
    deadline_at: str | None
    late_acceptance_cutoff_at: str | None
    hard_close_at: str | None
    closed_at: str | None
    matched_files: builtins.list[dict[str, Any]] | None
    missing_files: builtins.list[dict[str, Any]] | None
    criteria_errors: builtins.list[str] | None
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
        ) in ExpectationEvaluation.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ExpectationEvaluation.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class ExpectationEvaluationResource:
    """ExpectationEvaluation operations that use one client's configuration.

    Get one from a client, such as ``client.expectation_evaluation``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[ExpectationEvaluation]:
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
            ExpectationEvaluation,
            "GET",
            "/expectation_evaluations",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[ExpectationEvaluation]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ExpectationEvaluation:
        """Parameters:
        id (required) - int64 - Expectation Evaluation ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ExpectationEvaluation:
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
            "/expectation_evaluations/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, ExpectationEvaluation)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ExpectationEvaluation:
        """The same as find()."""
        return self.find(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ExpectationEvaluation:
        """A new ExpectationEvaluation with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = ExpectationEvaluation(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = ExpectationEvaluationResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[ExpectationEvaluation]:
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
) -> ListObj[ExpectationEvaluation]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ExpectationEvaluation:
    """Parameters:
    id (required) - int64 - Expectation Evaluation ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ExpectationEvaluation:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def new(*args, **kwargs) -> ExpectationEvaluation:
    return ExpectationEvaluation(*args, **kwargs)
