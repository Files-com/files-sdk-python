import builtins  # noqa: F401
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class InboxRegistration:
    default_attributes = {
        "code": None,  # string - Registration cookie code
        "name": None,  # string - Registrant name
        "company": None,  # string - Registrant company name
        "email": None,  # string - Registrant email address
        "ip": None,  # string - Registrant IP Address
        "clickwrap_body": None,  # string - Clickwrap text that was shown to the registrant
        "form_field_set_id": None,  # int64 - Id of associated form field set
        "form_field_data": None,  # object - Data for form field set with form field ids as keys and user data as values
        "inbox_id": None,  # int64 - Id of associated inbox
        "inbox_recipient_id": None,  # int64 - Id of associated inbox recipient
        "inbox_title": None,  # string - Title of associated inbox
        "created_at": None,  # date-time - Registration creation date/time
        "inbox_code": None,  # string - Inbox URL code
        "inbox_recipient_registration_code": None,  # string - Inbox recipient registration code
        "password": None,  # string - Inbox password
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
        ) in InboxRegistration.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in InboxRegistration.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The InboxRegistration object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
#   folder_behavior_id - int64 - ID of the associated Inbox. This is required if the user is not a site admin.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "folder_behavior_id" in params and not isinstance(
        params["folder_behavior_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: folder_behavior_id must be an int"
        )
    return ListObj(
        InboxRegistration, "GET", "/inbox_registrations", params, options
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   inbox_code (required) - string - Inbox URL code
#   inbox_recipient_registration_code - string - Inbox recipient registration code
#   password - string - Inbox password
#   name - string - Registrant name
#   company - string - Registrant company name
#   email - string - Registrant email address
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "inbox_code" in params and not isinstance(params["inbox_code"], str):
        raise InvalidParameterError("Bad parameter: inbox_code must be an str")
    if "inbox_recipient_registration_code" in params and not isinstance(
        params["inbox_recipient_registration_code"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: inbox_recipient_registration_code must be an str"
        )
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "company" in params and not isinstance(params["company"], str):
        raise InvalidParameterError("Bad parameter: company must be an str")
    if "email" in params and not isinstance(params["email"], str):
        raise InvalidParameterError("Bad parameter: email must be an str")
    if "inbox_code" not in params:
        raise MissingParameterError("Parameter missing: inbox_code")
    response, options = Api.send_request(
        "POST", "/inbox_registrations", params, options
    )
    return InboxRegistration(response.data, options)


# Parameters:
#   inbox_registration_code (required) - string - Inbox registration cookie code
def last_activity(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "inbox_registration_code" in params and not isinstance(
        params["inbox_registration_code"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: inbox_registration_code must be an str"
        )
    if "inbox_registration_code" not in params:
        raise MissingParameterError(
            "Parameter missing: inbox_registration_code"
        )
    Api.send_request(
        "POST", "/inbox_registrations/last_activity", params, options
    )


# Parameters:
#   folder_behavior_id - int64 - ID of the associated Inbox. This is required if the user is not a site admin.
def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "folder_behavior_id" in params and not isinstance(
        params["folder_behavior_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: folder_behavior_id must be an int"
        )
    response, options = Api.send_request(
        "POST", "/inbox_registrations/create_export", params, options
    )
    return Export(response.data, options)


def new(*args, **kwargs):
    return InboxRegistration(*args, **kwargs)
