import builtins  # noqa: F401
from decimal import Decimal
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AccountLineItem:
    __decimal_fields = {
        "amount",
        "balance",
    }
    __decimal_array_fields = {}
    default_attributes = {
        "id": None,  # int64 - Line item Id
        "amount": None,  # decimal - Line item amount
        "balance": None,  # decimal - Line item balance
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
            value = attributes.get(attribute, default_value)
            if (
                attribute in AccountLineItem.__decimal_fields
                and value is not None
            ):
                value = Decimal(str(value))
            if (
                attribute in AccountLineItem.__decimal_array_fields
                and value is not None
            ):
                value = [Decimal(str(v)) for v in (value or [])]
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in AccountLineItem.default_attributes
            if getattr(self, k, None) is not None
        }
        for k in list(attrs.keys()):
            if k in AccountLineItem.__decimal_fields and attrs[k] is not None:
                attrs[k] = str(attrs[k])
            if (
                k in AccountLineItem.__decimal_array_fields
                and attrs[k] is not None
            ):
                attrs[k] = [str(v) for v in (attrs[k] or [])]
        return attrs


def new(*args, **kwargs):
    return AccountLineItem(*args, **kwargs)
