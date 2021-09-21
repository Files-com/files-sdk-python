import builtins
import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class AutomationRun:
    default_attributes = {
        'automation_id': None,     # int64 - ID of the associated Automation.
        'status': None,     # string - The success status of the AutomationRun. One of `running`, `success`, `partial_failure`, or `failure`.
        'status_messages_url': None,     # string - Link to status messages log file.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in AutomationRun.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in AutomationRun.default_attributes if getattr(self, k, None) is not None}


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   automation_id (required) - int64 - ID of the associated Automation.
def list(params = None, options = None):
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
    if "automation_id" in params and not isinstance(params["automation_id"], int):
        raise InvalidParameterError("Bad parameter: automation_id must be an int")
    if "automation_id" not in params:
        raise MissingParameterError("Parameter missing: automation_id")
    return ListObj(AutomationRun,"GET", "/automation_runs", params, options)

def all(params = None, options = None):
    list(params, options)

def new(*args, **kwargs):
    return AutomationRun(*args, **kwargs)