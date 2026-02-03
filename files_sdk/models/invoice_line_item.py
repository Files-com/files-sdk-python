import builtins  # noqa: F401
from decimal import Decimal
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class InvoiceLineItem:
    __decimal_fields = {
        "amount",
    }
    __decimal_array_fields = {}
    default_attributes = {
        "id": None,  # int64 - Invoice Line item Id
        "amount": None,  # decimal - Invoice line item amount
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
            value = attributes.get(attribute, default_value)
            if (
                attribute in InvoiceLineItem.__decimal_fields
                and value is not None
            ):
                value = Decimal(str(value))
            if (
                attribute in InvoiceLineItem.__decimal_array_fields
                and value is not None
            ):
                value = [Decimal(str(v)) for v in (value or [])]
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in InvoiceLineItem.default_attributes
            if getattr(self, k, None) is not None
        }
        for k in list(attrs.keys()):
            if k in InvoiceLineItem.__decimal_fields and attrs[k] is not None:
                attrs[k] = str(attrs[k])
            if (
                k in InvoiceLineItem.__decimal_array_fields
                and attrs[k] is not None
            ):
                attrs[k] = [str(v) for v in (attrs[k] or [])]
        return attrs


def new(*args, **kwargs):
    return InvoiceLineItem(*args, **kwargs)
