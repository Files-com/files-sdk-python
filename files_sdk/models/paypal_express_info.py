import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class PaypalExpressInfo:
    default_attributes = {
        "billing_email": None,  # email - Paypal billing email
        "billing_company_name": None,  # string - Paypal billing company name
        "billing_address": None,  # string - Paypal billing address
        "billing_address_2": None,  # string - Paypal billing address 2
        "billing_city": None,  # string - Paypal billing city
        "billing_state": None,  # string - Paypal billing state
        "billing_country": None,  # string - Paypal billing country
        "billing_zip": None,  # string - Paypal billing zipcode
        "billing_name": None,  # string - Paypal billing name
        "billing_phone": None,  # string - Paypal billing phone
        "paypal_payer_id": None,  # string - Paypal payer ID
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
        ) in PaypalExpressInfo.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in PaypalExpressInfo.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return PaypalExpressInfo(*args, **kwargs)
