import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Account:
    default_attributes = {
        "name": None,  # string - Account name
        "address": None,  # string - Account address
        "address_2": None,  # string - Account address 2
        "card_number": None,  # string - Account payment card number
        "card_type": None,  # string - Account payment card type
        "city": None,  # string - Account city
        "company_name": None,  # string - Account company name
        "country": None,  # string - Account country
        "created_at": None,  # date-time - Account creation date/time
        "currency": None,  # string - Account preferred currency
        "email": None,  # email - Account email address
        "phone_number": None,  # string - Account phone number
        "processor_type": None,  # string - Type of billing processor.  Can be PayPal, Credit Card, or Manual
        "state": None,  # string - Account state
        "zip": None,  # string - Account zipcode
        "billing_frequency": None,  # int64 - Number of usage periods billed at once.  This value will either be 12 representing an annual account of 12 usage periods or 1 representing a monthly account.
        "expiration_year": None,  # string - Expiration year(4 digits).
        "expiration_month": None,  # string - Expiration month(2 digits).
        "start_year": None,  # string - Required for some cards(Switch / Solo).
        "start_month": None,  # string - Required for some cards(Switch / Solo).
        "cvv": None,  # string - 3 digit code on the back of the card.
        "paypal_token": None,  # string - Token for paying with paypal.
        "paypal_payer_id": None,  # string - Paypal payer ID for paying with paypal.
        "plan_id": None,  # int64 - Plan ID to switch to immediately.
        "create_account": None,  # boolean - Create account without immediately charging the customer.  (i.e. let the trial complete first.)
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Account.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Account.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The Account object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


def get(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, options = Api.send_request("GET", "/account", params, options)
    return Account(response.data, options)


# Parameters:
#   name - string - Internal name.
#   company_name - string - Company name.
#   address - string - Address line 1.
#   address_2 - string - Address line 2.
#   city - string - City.
#   state - string - State.
#   zip - string - Zipcode.
#   country - string - Country.
#   email - string - Email.
#   phone_number - string - Primary phone number.
#   card_number - string - Credit card number.
#   card_type - string - Credit card type.  Can be visa, master, maestro, solo, switch, american_express, or discover.
#   expiration_year - string - Expiration year(4 digits).
#   expiration_month - string - Expiration month(2 digits).
#   start_year - string - Required for some cards(Switch / Solo).
#   start_month - string - Required for some cards(Switch / Solo).
#   cvv - string - 3 digit code on the back of the card.
#   paypal_token - string - Token for paying with paypal.
#   paypal_payer_id - string - Paypal payer ID for paying with paypal.
#   plan_id - int64 - Plan ID to switch to immediately.
#   billing_frequency - int64 - The billing frequency, in months, for the site.  Must be 1 (monthly) or 12 (annual).
#   currency - string - Preferred currency for this account.
#   create_account - boolean - Create account without immediately charging the customer.  (i.e. let the trial complete first.)
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "company_name" in params and not isinstance(
        params["company_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: company_name must be an str"
        )
    if "address" in params and not isinstance(params["address"], str):
        raise InvalidParameterError("Bad parameter: address must be an str")
    if "address_2" in params and not isinstance(params["address_2"], str):
        raise InvalidParameterError("Bad parameter: address_2 must be an str")
    if "city" in params and not isinstance(params["city"], str):
        raise InvalidParameterError("Bad parameter: city must be an str")
    if "state" in params and not isinstance(params["state"], str):
        raise InvalidParameterError("Bad parameter: state must be an str")
    if "zip" in params and not isinstance(params["zip"], str):
        raise InvalidParameterError("Bad parameter: zip must be an str")
    if "country" in params and not isinstance(params["country"], str):
        raise InvalidParameterError("Bad parameter: country must be an str")
    if "email" in params and not isinstance(params["email"], str):
        raise InvalidParameterError("Bad parameter: email must be an str")
    if "phone_number" in params and not isinstance(
        params["phone_number"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: phone_number must be an str"
        )
    if "card_number" in params and not isinstance(params["card_number"], str):
        raise InvalidParameterError(
            "Bad parameter: card_number must be an str"
        )
    if "card_type" in params and not isinstance(params["card_type"], str):
        raise InvalidParameterError("Bad parameter: card_type must be an str")
    if "expiration_year" in params and not isinstance(
        params["expiration_year"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: expiration_year must be an str"
        )
    if "expiration_month" in params and not isinstance(
        params["expiration_month"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: expiration_month must be an str"
        )
    if "start_year" in params and not isinstance(params["start_year"], str):
        raise InvalidParameterError("Bad parameter: start_year must be an str")
    if "start_month" in params and not isinstance(params["start_month"], str):
        raise InvalidParameterError(
            "Bad parameter: start_month must be an str"
        )
    if "cvv" in params and not isinstance(params["cvv"], str):
        raise InvalidParameterError("Bad parameter: cvv must be an str")
    if "paypal_token" in params and not isinstance(
        params["paypal_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: paypal_token must be an str"
        )
    if "paypal_payer_id" in params and not isinstance(
        params["paypal_payer_id"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: paypal_payer_id must be an str"
        )
    if "plan_id" in params and not isinstance(params["plan_id"], int):
        raise InvalidParameterError("Bad parameter: plan_id must be an int")
    if "billing_frequency" in params and not isinstance(
        params["billing_frequency"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: billing_frequency must be an int"
        )
    if "currency" in params and not isinstance(params["currency"], str):
        raise InvalidParameterError("Bad parameter: currency must be an str")
    if "create_account" in params and not isinstance(
        params["create_account"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: create_account must be an bool"
        )
    response, options = Api.send_request("POST", "/account", params, options)
    return Account(response.data, options)


# Parameters:
#   name - string - Internal name.
#   company_name - string - Company name.
#   address - string - Address line 1.
#   address_2 - string - Address line 2.
#   city - string - City.
#   state - string - State.
#   zip - string - Zipcode.
#   country - string - Country.
#   email - string - Email.
#   phone_number - string - Primary phone number.
#   card_number - string - Credit card number.
#   card_type - string - Credit card type.  Can be visa, master, maestro, solo, switch, american_express, or discover.
#   expiration_year - string - Expiration year(4 digits).
#   expiration_month - string - Expiration month(2 digits).
#   start_year - string - Required for some cards(Switch / Solo).
#   start_month - string - Required for some cards(Switch / Solo).
#   cvv - string - 3 digit code on the back of the card.
#   paypal_token - string - Token for paying with paypal.
#   paypal_payer_id - string - Paypal payer ID for paying with paypal.
def update(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "company_name" in params and not isinstance(
        params["company_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: company_name must be an str"
        )
    if "address" in params and not isinstance(params["address"], str):
        raise InvalidParameterError("Bad parameter: address must be an str")
    if "address_2" in params and not isinstance(params["address_2"], str):
        raise InvalidParameterError("Bad parameter: address_2 must be an str")
    if "city" in params and not isinstance(params["city"], str):
        raise InvalidParameterError("Bad parameter: city must be an str")
    if "state" in params and not isinstance(params["state"], str):
        raise InvalidParameterError("Bad parameter: state must be an str")
    if "zip" in params and not isinstance(params["zip"], str):
        raise InvalidParameterError("Bad parameter: zip must be an str")
    if "country" in params and not isinstance(params["country"], str):
        raise InvalidParameterError("Bad parameter: country must be an str")
    if "email" in params and not isinstance(params["email"], str):
        raise InvalidParameterError("Bad parameter: email must be an str")
    if "phone_number" in params and not isinstance(
        params["phone_number"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: phone_number must be an str"
        )
    if "card_number" in params and not isinstance(params["card_number"], str):
        raise InvalidParameterError(
            "Bad parameter: card_number must be an str"
        )
    if "card_type" in params and not isinstance(params["card_type"], str):
        raise InvalidParameterError("Bad parameter: card_type must be an str")
    if "expiration_year" in params and not isinstance(
        params["expiration_year"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: expiration_year must be an str"
        )
    if "expiration_month" in params and not isinstance(
        params["expiration_month"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: expiration_month must be an str"
        )
    if "start_year" in params and not isinstance(params["start_year"], str):
        raise InvalidParameterError("Bad parameter: start_year must be an str")
    if "start_month" in params and not isinstance(params["start_month"], str):
        raise InvalidParameterError(
            "Bad parameter: start_month must be an str"
        )
    if "cvv" in params and not isinstance(params["cvv"], str):
        raise InvalidParameterError("Bad parameter: cvv must be an str")
    if "paypal_token" in params and not isinstance(
        params["paypal_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: paypal_token must be an str"
        )
    if "paypal_payer_id" in params and not isinstance(
        params["paypal_payer_id"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: paypal_payer_id must be an str"
        )
    response, options = Api.send_request("PATCH", "/account", params, options)
    return Account(response.data, options)


def new(*args, **kwargs):
    return Account(*args, **kwargs)
