import builtins  # noqa: F401
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Inbox:
    default_attributes = {
        "title": None,  # string - Inbox title
        "description": None,  # string - User description
        "help_text": None,  # string - Text that will be shown to the users on the Inbox.  Use this field to provide custom instructions.
        "key": None,  # string - Unique key for inbox
        "show_on_login_page": None,  # boolean - Show this inbox on site login page?
        "has_password": None,  # boolean - Is this inbox password protected?
        "require_registration": None,  # boolean - Does this inbox require registration?
        "dont_allow_folders_in_uploads": None,  # boolean - Should folder uploads be prevented?
        "clickwrap_body": None,  # string - Legal text that must be agreed to prior to accessing Inbox.
        "form_field_set": None,  # FormFieldSet - Custom Form to use
        "notify_senders_on_successful_uploads_via_email": None,  # boolean - Notify senders on successful uploads via email
        "notify_senders_on_successful_uploads_via_web": None,  # boolean - Notify senders on successful uploads via web
        "allow_whitelisting": None,  # boolean - allow/disallow whitelist
        "whitelist": None,  # array(string) - A list of emails and domain names for whitelisting
        "disable_web_upload": None,  # boolean - This will disable the upload URL and can only be done if uploads via email are enabled
        "inbound_email_address": None,  # string - inbound email address to the inbox
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Inbox.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Inbox.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `allow_whitelisting`.
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
    return ListObj(Inbox, "GET", "/inboxes", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `allow_whitelisting`.
def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    response, options = Api.send_request(
        "POST", "/inboxes/create_export", params, options
    )
    return Export(response.data, options)


def new(*args, **kwargs):
    return Inbox(*args, **kwargs)
