import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class SupportRequest:
    default_attributes = {
        "id": None,  # int64 - ID
        "subject": None,  # string - Subject of the support request.
        "comment": None,  # string - Main body of the support request.
        "created_at": None,  # date - When this support request was made.
        "access_until": None,  # date - Customer Support can access your user account up through this date/time.
        "customer_success_access": None,  # string - Enable Customer Support access to your user account?
        "priority": None,  # string - Priority. Can be `low` (e.g. general or billing/account questions), `normal` (e.g. the system is impaired), `high` (e.g. a production workflow or business process is impaired), `urgent` (e.g. a production workflow or business process is down), `critical` (e.g. a business-critical workflow or business process is down)
        "name": None,  # string - Support Request name
        "phone_number": None,  # string - Support Request phone number
        "access_reset": None,  # boolean - If set to `true`, will reset the customer success access window.
        "email": None,  # string - Email address of the user requesting support.
        "attachments_files": None,  # array(file)
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
        ) in SupportRequest.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SupportRequest.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    # Parameters:
    #   customer_success_access - string - Enable Customer Support access to your user account?
    #   access_reset - boolean - If set to `true`, will reset the customer success access window.
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
        if "customer_success_access" in params and not isinstance(
            params["customer_success_access"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: customer_success_access must be an str"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/support_requests/{id}".format(
                id=quote(str(params["id"]), safe="")
            ),
            params,
            self.options,
        )
        return response.data

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
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
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
    return ListObj(SupportRequest, "GET", "/support_requests", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   customer_success_access - string - Enable Customer Support access to your user account?
#   access_reset - boolean - If set to `true`, will reset the customer success access window.
#   email (required) - string - Email address of the user requesting support.
#   subject (required) - string - Subject of the support request.
#   comment (required) - string - Main body of the support request.
#   priority - string - Priority. Can be `low` (e.g. general or billing/account questions), `normal` (e.g. the system is impaired), `high` (e.g. a production workflow or business process is impaired), `urgent` (e.g. a production workflow or business process is down), `critical` (e.g. a business-critical workflow or business process is down)
#   phone_number - string - Support Request phone number
#   name - string - Support Request name
#   attachments_files - array(file)
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "customer_success_access" in params and not isinstance(
        params["customer_success_access"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: customer_success_access must be an str"
        )
    if "access_reset" in params and not isinstance(
        params["access_reset"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: access_reset must be an bool"
        )
    if "email" in params and not isinstance(params["email"], str):
        raise InvalidParameterError("Bad parameter: email must be an str")
    if "subject" in params and not isinstance(params["subject"], str):
        raise InvalidParameterError("Bad parameter: subject must be an str")
    if "comment" in params and not isinstance(params["comment"], str):
        raise InvalidParameterError("Bad parameter: comment must be an str")
    if "priority" in params and not isinstance(params["priority"], str):
        raise InvalidParameterError("Bad parameter: priority must be an str")
    if "phone_number" in params and not isinstance(
        params["phone_number"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: phone_number must be an str"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "attachments_files" in params and not isinstance(
        params["attachments_files"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: attachments_files must be an list"
        )
    if "email" not in params:
        raise MissingParameterError("Parameter missing: email")
    if "subject" not in params:
        raise MissingParameterError("Parameter missing: subject")
    if "comment" not in params:
        raise MissingParameterError("Parameter missing: comment")
    response, options = Api.send_request(
        "POST", "/support_requests", params, options
    )
    return SupportRequest(response.data, options)


# Parameters:
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    response, options = Api.send_request(
        "POST", "/support_requests/create_export", params, options
    )
    return Export(response.data, options)


# Parameters:
#   customer_success_access - string - Enable Customer Support access to your user account?
#   access_reset - boolean - If set to `true`, will reset the customer success access window.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "customer_success_access" in params and not isinstance(
        params["customer_success_access"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: customer_success_access must be an str"
        )
    if "access_reset" in params and not isinstance(
        params["access_reset"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: access_reset must be an bool"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/support_requests/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return SupportRequest(response.data, options)


def new(*args, **kwargs):
    return SupportRequest(*args, **kwargs)
