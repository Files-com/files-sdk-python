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


class AccountLineItem:
    """A account line item record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Line item Id
        amount: decimal - Line item amount
        balance: decimal - Line item balance
        created_at: date-time - Line item created at
        currency: string - Line item currency
        download_uri: string - Line item download uri
        invoice_line_items: array(object) - Associated invoice line items
        method: string - Line item payment method
        payment_line_items: array(object) - Associated payment line items
        payment_reversed_at: date-time - Date/time payment was reversed if applicable
        payment_type: string - Type of payment if applicable
        site_name: string - Site name this line item is for
        type: string - Type of line item, either payment or invoice
    """

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

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    amount: Decimal | None
    balance: Decimal | None
    created_at: str | None
    currency: str | None
    download_uri: str | None
    invoice_line_items: builtins.list[dict[str, Any]] | None
    method: str | None
    payment_line_items: builtins.list[dict[str, Any]] | None
    payment_reversed_at: str | None
    payment_type: str | None
    site_name: str | None
    type: str | None

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
        ) in AccountLineItem.default_attributes.items():
            value = attributes.get(attribute, default_value)
            if value is None:
                values[attribute] = None
            elif attribute in AccountLineItem.__decimal_fields:
                values[attribute] = Decimal(str(value))
            elif attribute in AccountLineItem.__decimal_array_fields:
                values[attribute] = [Decimal(str(v)) for v in (value or [])]
            else:
                values[attribute] = value
        for attribute, value in values.items():
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in AccountLineItem.default_attributes
            if getattr(self, k, None) is not None
        }
        for k in AccountLineItem.__decimal_fields:
            if k in attrs:
                attrs[k] = str(attrs[k])
        for k in AccountLineItem.__decimal_array_fields:
            if k in attrs:
                attrs[k] = [str(v) for v in (attrs[k] or [])]
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> AccountLineItem:
    return AccountLineItem(*args, **kwargs)
