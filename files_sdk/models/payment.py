import builtins  # noqa: F401
from files_sdk.models.account_line_item import AccountLineItem
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Payment:
    default_attributes = {
        "id": None,  # int64 - Line item Id
        "amount": None,  # double - Line item amount
        "balance": None,  # double - Line item balance
        "created_at": None,  # date-time - Line item created at
        "currency": None,  # string - Line item currency
        "download_uri": None,  # string - Line item download uri
        "invoice_line_items": None,  # array(object) - Associated invoice line items
        "method": None,  # string - Line item payment method
        "payment_line_items": None,  # array(object) - Associated payment line items
        "payment_reversed_at": None,  # date-time - Date/time payment was reversed if applicable
        "payment_type": None,  # string - Type of payment if applicable
        "site_name": None,  # string - Site name this line item is for
        "type": None,  # string - Type of line item, either payment or invoice
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Payment.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Payment.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(AccountLineItem, "GET", "/payments", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Payment ID.
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
        "GET", "/payments/{id}".format(id=params["id"]), params, options
    )
    return AccountLineItem(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


def new(*args, **kwargs):
    return Payment(*args, **kwargs)
