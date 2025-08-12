import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class InvoiceLineItem:
    default_attributes = {
        "id": None,  # int64 - Invoice Line item Id
        "amount": None,  # double - Invoice line item amount
        "created_at": None,  # date-time - Invoice line item created at date/time
        "description": None,  # string - Invoice line item description
        "type": None,  # string - Invoice line item type
        "service_end_at": None,  # date-time - Invoice line item service end date/time
        "service_start_at": None,  # date-time - Invoice line item service start date/time
        "plan": None,  # string - Plan name
        "site": None,  # string - Site name
        "prepaid_bytes": None,  # int64 - Prepaid bytes purchased for this invoice line item
        "prepaid_bytes_expire_at": None,  # date-time - When the prepaid bytes expire
        "prepaid_bytes_used": None,  # int64 - Total prepaid bytes used for this invoice line item
        "prepaid_bytes_available": None,  # int64 - Available prepaid bytes for this invoice line item
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
        ) in InvoiceLineItem.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in InvoiceLineItem.default_attributes
            if getattr(self, k, None) is not None
        }


def new(*args, **kwargs):
    return InvoiceLineItem(*args, **kwargs)
