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


class InvoiceLineItem:
    """A invoice line item record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Invoice Line item Id
        amount: decimal - Invoice line item amount
        created_at: date-time - Invoice line item created at date/time
        description: string - Invoice line item description
        type: string - Invoice line item type
        service_end_at: date-time - Invoice line item service end date/time
        service_start_at: date-time - Invoice line item service start date/time
        plan: string - Plan name
        site: string - Site name
        prepaid_bytes: int64 - Prepaid bytes purchased for this invoice line item
        prepaid_bytes_expire_at: date-time - When the prepaid bytes expire
        prepaid_bytes_used: int64 - Total prepaid bytes used for this invoice line item
        prepaid_bytes_available: int64 - Available prepaid bytes for this invoice line item
    """

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

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    amount: Decimal | None
    created_at: str | None
    description: str | None
    type: str | None
    service_end_at: str | None
    service_start_at: str | None
    plan: str | None
    site: str | None
    prepaid_bytes: int | None
    prepaid_bytes_expire_at: str | None
    prepaid_bytes_used: int | None
    prepaid_bytes_available: int | None

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
        ) in InvoiceLineItem.default_attributes.items():
            value = attributes.get(attribute, default_value)
            if value is None:
                values[attribute] = None
            elif attribute in InvoiceLineItem.__decimal_fields:
                values[attribute] = Decimal(str(value))
            elif attribute in InvoiceLineItem.__decimal_array_fields:
                values[attribute] = [Decimal(str(v)) for v in (value or [])]
            else:
                values[attribute] = value
        for attribute, value in values.items():
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in InvoiceLineItem.default_attributes
            if getattr(self, k, None) is not None
        }
        for k in InvoiceLineItem.__decimal_fields:
            if k in attrs:
                attrs[k] = str(attrs[k])
        for k in InvoiceLineItem.__decimal_array_fields:
            if k in attrs:
                attrs[k] = [str(v) for v in (attrs[k] or [])]
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


def new(*args, **kwargs) -> InvoiceLineItem:
    return InvoiceLineItem(*args, **kwargs)
