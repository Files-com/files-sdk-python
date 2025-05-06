import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AutomationRun:
    default_attributes = {
        "id": None,  # int64 - ID.
        "automation_id": None,  # int64 - ID of the associated Automation.
        "completed_at": None,  # date-time - Automation run completion/failure date/time.
        "created_at": None,  # date-time - Automation run start date/time.
        "retry_at": None,  # date-time - If set, this automation will be retried at this date/time due to `failure` or `partial_failure`.
        "retried_at": None,  # date-time - If set, this Automation run was retried due to `failure` or `partial_failure`.
        "retried_in_run_id": None,  # int64 - ID of the run that is or will be retrying this run.
        "retry_of_run_id": None,  # int64 - ID of the original run that this run is retrying.
        "runtime": None,  # double - Automation run runtime.
        "status": None,  # string - The success status of the AutomationRun. One of `running`, `success`, `partial_failure`, or `failure`.
        "successful_operations": None,  # int64 - Count of successful operations.
        "failed_operations": None,  # int64 - Count of failed operations.
        "status_messages_url": None,  # string - Link to status messages log file.
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
        ) in AutomationRun.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in AutomationRun.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `automation_id`, `created_at` or `status`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `status` and `automation_id`. Valid field combinations are `[ automation_id, status ]`.
#   automation_id (required) - int64 - ID of the associated Automation.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "automation_id" in params and not isinstance(
        params["automation_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: automation_id must be an int"
        )
    if "automation_id" not in params:
        raise MissingParameterError("Parameter missing: automation_id")
    return ListObj(AutomationRun, "GET", "/automation_runs", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Automation Run ID.
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
        "GET", "/automation_runs/{id}".format(id=params["id"]), params, options
    )
    return AutomationRun(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


def new(*args, **kwargs):
    return AutomationRun(*args, **kwargs)
