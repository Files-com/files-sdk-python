import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class InvoiceLineItem:
    default_attributes = {
        "amount": None,  # double - Invoice line item amount
        "created_at": None,  # date-time - Invoice line item created at date/time
        "description": None,  # string - Invoice line item description
        "type": None,  # string - Invoice line item type
        "service_end_at": None,  # date-time - Invoice line item service end date/time
        "service_start_at": None,  # date-time - Invoice line item service start date/time
        "updated_at": None,  # date-time - Invoice line item updated date/time
        "plan": None,  # string - Plan name
        "site": None,  # string - Site name
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
