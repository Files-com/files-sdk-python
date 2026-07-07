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


class PublicInbox:
    default_attributes = {
        "color_left": None,  # string - Page link and button color
        "color_link": None,  # string - Top bar link color
        "color_text": None,  # string - Page link and button color
        "color_top": None,  # string - Top bar background color
        "color_top_text": None,  # string - Top bar text color
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
        "require_logout": None,  # boolean - If true, we will hide the 'Remember Me' box on the Inbox registration page, requiring that the user logout and log back in every time they visit the page.
        "logo": None,  # Image - Custom logo for Inbox folder
        "logo_click_href": None,  # string - URL to open when a public visitor clicks the custom logo
        "thumbnail": None,  # Image - Custom logo thumbnail for Inbox folder
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in PublicInbox.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in PublicInbox.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(PublicInbox, "GET", "/public_inboxes", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   key (required) - string - Unique key for inbox
#   recipient_code - string - Inbox recipient code
def get_key(key, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["key"] = key
    if "key" in params and not isinstance(params["key"], str):
        raise InvalidParameterError("Bad parameter: key must be an str")
    if "recipient_code" in params and not isinstance(
        params["recipient_code"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: recipient_code must be an str"
        )
    if "key" not in params:
        raise MissingParameterError("Parameter missing: key")
    response, options = Api.send_request(
        "GET",
        "/public_inboxes/key/{key}".format(
            key=quote(str(params["key"]), safe="")
        ),
        params,
        options,
    )
    return PublicInbox(response.data, options)


def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, options = Api.send_request(
        "POST", "/public_inboxes/create_export", params, options
    )
    return Export(response.data, options)


def new(*args, **kwargs):
    return PublicInbox(*args, **kwargs)
