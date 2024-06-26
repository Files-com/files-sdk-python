import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AccountLineItem:
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
        for (
            attribute,
            default_value,
        ) in AccountLineItem.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in AccountLineItem.default_attributes
            if getattr(self, k, None) is not None
        }


def new(*args, **kwargs):
    return AccountLineItem(*args, **kwargs)
