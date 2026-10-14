import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from decimal import Decimal
from files_sdk.api import (  # noqa: F401
    LEGACY,
    LegacyScope,
    Operation,
    copy_params,
    decode_record,
    path_value,
)
from files_sdk.api_client import unexpected_response_error  # noqa: F401
from files_sdk.context import RequestOptions  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class PaymentLineItem:
    """A payment line item record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        amount: decimal - Payment line item amount
        created_at: date-time - Payment line item created at date/time
        invoice_id: int64 - Invoice ID
        payment_id: int64 - Payment ID
    """

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

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    amount: Decimal | None
    created_at: str | None
    invoice_id: int | None
    payment_id: int | None

    # The client and settings this object's operations use: those of the
    # operation or client that made it, or the module's when it starts an
    # operation if neither did.
    _context: Any = None

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = dict(options)

    def set_attributes(self, attributes):
        # Convert every value before assigning any, so a malformed decimal
        # cannot leave the object partly updated.
        values = {}
        for (
            attribute,
            default_value,
        ) in PaymentLineItem.default_attributes.items():
            value = attributes.get(attribute, default_value)
            if value is None:
                values[attribute] = None
            elif attribute in PaymentLineItem.__decimal_fields:
                values[attribute] = Decimal(str(value))
            elif attribute in PaymentLineItem.__decimal_array_fields:
                values[attribute] = [Decimal(str(v)) for v in (value or [])]
            else:
                values[attribute] = value
        for attribute, value in values.items():
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in PaymentLineItem.default_attributes
            if getattr(self, k, None) is not None
        }
        for k in PaymentLineItem.__decimal_fields:
            if k in attrs:
                attrs[k] = str(attrs[k])
        for k in PaymentLineItem.__decimal_array_fields:
            if k in attrs:
                attrs[k] = [str(v) for v in (attrs[k] or [])]
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> PaymentLineItem:
    return PaymentLineItem(*args, **kwargs)
