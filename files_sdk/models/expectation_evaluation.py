import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ExpectationEvaluation:
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
        "criteria_errors": None,  # array(string) - Captured criteria failures for the window.
        "summary": None,  # object - Compact evaluator summary payload.
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
        ExpectationEvaluation,
        "GET",
        "/expectation_evaluations",
        params,
        options,
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Expectation Evaluation ID.
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
        "/expectation_evaluations/{id}".format(id=params["id"]),
        params,
        options,
    )
    return ExpectationEvaluation(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


def new(*args, **kwargs):
    return ExpectationEvaluation(*args, **kwargs)
