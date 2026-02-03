import builtins  # noqa: F401
from decimal import Decimal
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class PaymentLineItem:
    __decimal_fields = {
        "amount",
    }
    __decimal_array_fields = {}
    default_attributes = {
        "amount": None,  # decimal - Payment line item amount
        "created_at": None,  # date-time - Payment line item created at date/time
        "invoice_id": None,  # int64 - Invoice ID
        "payment_id": None,  # int64 - Payment ID
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
        ) in PaymentLineItem.default_attributes.items():
            value = attributes.get(attribute, default_value)
            if (
                attribute in PaymentLineItem.__decimal_fields
                and value is not None
            ):
                value = Decimal(str(value))
            if (
                attribute in PaymentLineItem.__decimal_array_fields
                and value is not None
            ):
                value = [Decimal(str(v)) for v in (value or [])]
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in PaymentLineItem.default_attributes
            if getattr(self, k, None) is not None
        }
        for k in list(attrs.keys()):
            if k in PaymentLineItem.__decimal_fields and attrs[k] is not None:
                attrs[k] = str(attrs[k])
            if (
                k in PaymentLineItem.__decimal_array_fields
                and attrs[k] is not None
            ):
                attrs[k] = [str(v) for v in (attrs[k] or [])]
        return attrs


def new(*args, **kwargs):
    return PaymentLineItem(*args, **kwargs)
