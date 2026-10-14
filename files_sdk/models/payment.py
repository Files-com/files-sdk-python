import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from decimal import Decimal
from files_sdk.models.account_line_item import AccountLineItem
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
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Payment:
    """A payment record from the Files.com API.

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
        for attribute, default_value in Payment.default_attributes.items():
            value = attributes.get(attribute, default_value)
            if value is None:
                values[attribute] = None
            elif attribute in Payment.__decimal_fields:
                values[attribute] = Decimal(str(value))
            elif attribute in Payment.__decimal_array_fields:
                values[attribute] = [Decimal(str(v)) for v in (value or [])]
            else:
                values[attribute] = value
        for attribute, value in values.items():
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Payment.default_attributes
            if getattr(self, k, None) is not None
        }
        for k in Payment.__decimal_fields:
            if k in attrs:
                attrs[k] = str(attrs[k])
        for k in Payment.__decimal_array_fields:
            if k in attrs:
                attrs[k] = [str(v) for v in (attrs[k] or [])]
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class PaymentResource:
    """Payment operations that use one client's configuration.

    Get one from a client, such as ``client.payment``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[AccountLineItem]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        """
        params = copy_params(params)
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(AccountLineItem, "GET", "/payments", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[AccountLineItem]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AccountLineItem:
        """Parameters:
        id (required) - int64 - Payment ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> AccountLineItem:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/payments/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, AccountLineItem)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AccountLineItem:
        """The same as find()."""
        return self.find(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Payment:
        """A new Payment with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Payment(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = PaymentResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[AccountLineItem]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[AccountLineItem]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AccountLineItem:
    """Parameters:
    id (required) - int64 - Payment ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AccountLineItem:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def new(*args, **kwargs) -> Payment:
    return Payment(*args, **kwargs)
