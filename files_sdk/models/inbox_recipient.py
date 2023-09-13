import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class InboxRecipient:
    default_attributes = {
        "company": None,  # string - The recipient's company.
        "name": None,  # string - The recipient's name.
        "note": None,  # string - A note sent to the recipient with the inbox.
        "recipient": None,  # string - The recipient's email address.
        "sent_at": None,  # date-time - When the Inbox was shared with this recipient.
        "inbox_id": None,  # int64 - Inbox to share.
        "share_after_create": None,  # boolean - Set to true to share the link with the recipient upon creation.
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
        ) in InboxRecipient.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in InboxRecipient.default_attributes
            if getattr(self, k, None) is not None
        }

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The InboxRecipient object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[has_registrations]=desc`). Valid fields are `has_registrations`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `has_registrations`.
#   inbox_id (required) - int64 - List recipients for the inbox with this ID.
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
    if "inbox_id" in params and not isinstance(params["inbox_id"], int):
        raise InvalidParameterError("Bad parameter: inbox_id must be an int")
    if "inbox_id" not in params:
        raise MissingParameterError("Parameter missing: inbox_id")
    return ListObj(InboxRecipient, "GET", "/inbox_recipients", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   inbox_id (required) - int64 - Inbox to share.
#   recipient (required) - string - Email address to share this inbox with.
#   name - string - Name of recipient.
#   company - string - Company of recipient.
#   note - string - Note to include in email.
#   share_after_create - boolean - Set to true to share the link with the recipient upon creation.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "inbox_id" in params and not isinstance(params["inbox_id"], int):
        raise InvalidParameterError("Bad parameter: inbox_id must be an int")
    if "recipient" in params and not isinstance(params["recipient"], str):
        raise InvalidParameterError("Bad parameter: recipient must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "company" in params and not isinstance(params["company"], str):
        raise InvalidParameterError("Bad parameter: company must be an str")
    if "note" in params and not isinstance(params["note"], str):
        raise InvalidParameterError("Bad parameter: note must be an str")
    if "inbox_id" not in params:
        raise MissingParameterError("Parameter missing: inbox_id")
    if "recipient" not in params:
        raise MissingParameterError("Parameter missing: recipient")
    response, options = Api.send_request(
        "POST", "/inbox_recipients", params, options
    )
    return InboxRecipient(response.data, options)


def new(*args, **kwargs):
    return InboxRecipient(*args, **kwargs)
