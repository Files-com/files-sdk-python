import builtins  # noqa: F401
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
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in InboxRegistration.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   folder_behavior_id - int64 - ID of the associated Inbox.
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


def new(*args, **kwargs):
    return InboxRegistration(*args, **kwargs)
