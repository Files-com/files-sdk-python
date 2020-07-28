import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class InvoiceLineItem:
    default_attributes = {
        'amount': None,     # double - Invoice line item amount
        'created_at': None,     # date-time - Invoice line item created at date/time
        'description': None,     # string - Invoice line item description
        'type': None,     # string - Invoice line item type
        'service_end_at': None,     # date-time - Invoice line item service end date/time
        'service_start_at': None,     # date-time - Invoice line item service start date/time
        'updated_at': None,     # date-time - Invoice line item updated date/time
        'plan': None,     # string - Plan name
        'site': None,     # string - Site name
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in InvoiceLineItem.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in InvoiceLineItem.default_attributes if getattr(self, k, None) is not None}


def new(*args, **kwargs):
    return InvoiceLineItem(*args, **kwargs)