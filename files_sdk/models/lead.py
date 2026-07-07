import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Lead:
    default_attributes = {
        "id": None,  # int64 - Lead ID
        "code": None,  # string - Lead Cookie Code
        "name": None,  # string - Lead name
        "address": None,  # string - Lead address
        "address_2": None,  # string - Lead address 2
        "city": None,  # string - Lead city
        "company_name": None,  # string - Lead company name
        "contact_name": None,  # string - Contact name at the company
        "country": None,  # string - Lead country
        "currency": None,  # string - Lead preferred currency
        "email": None,  # string - Lead email address
        "language": None,  # string - Lead preferred language
        "phone_number": None,  # string - Lead phone number
        "state": None,  # string - Lead state
        "zip": None,  # string - Lead zipcode
        "lead_level": None,  # string - Quality score of the lead
        "signup_page_split_test_group": None,  # string - Signup page split test group
        "recaptcha_token": None,  # string
        "form_name": None,  # string - Signup form name
        "lead_source": None,  # string - Source of the lead
        "opportunity_comment": None,  # string - Opportunity comment
        "opportunity_type": None,  # string - Type of opportunity to create
        "gclid": None,  # string - Google Adwords Click ID
        "original_brand": None,  # string - Brand: `files`, `exavault` or `mover`
        "utm_campaign": None,  # string - Marketing tracking - campaign
        "utm_content": None,  # string - Marketing tracking - content
        "utm_domain": None,  # string - Marketing tracking - domain
        "utm_medium": None,  # string - Marketing tracking - medium
        "utm_source": None,  # string - Marketing tracking - source
        "utm_term": None,  # string - Marketing tracking - term
        "time_zone": None,  # string - Time zone, as returned by Javascript
        "time_zone_offset": None,  # int64 - Time zone offset (integer from -12 to 12)
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Lead.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Lead.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The Lead object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   recaptcha_token - string
#   name - string - Lead name
#   address - string - Lead address
#   address_2 - string - Lead address 2
#   city - string - Lead city
#   contact_name - string - Contact name at the company
#   currency - string - Lead preferred currency
#   email - string - Lead email address
#   language - string - Lead preferred language
#   phone_number - string - Lead phone number
#   state - string - Lead state
#   zip - string - Lead zipcode
#   form_name - string - Signup form name
#   lead_source - string - Source of the lead
#   opportunity_comment - string - Opportunity comment
#   opportunity_type - string - Type of opportunity to create
#   gclid - string - Google Adwords Click ID
#   original_brand - string - Brand: `files`, `exavault` or `mover`
#   utm_campaign - string - Marketing tracking - campaign
#   utm_content - string - Marketing tracking - content
#   utm_domain - string - Marketing tracking - domain
#   utm_medium - string - Marketing tracking - medium
#   utm_source - string - Marketing tracking - source
#   utm_term - string - Marketing tracking - term
#   time_zone - string - Time zone, as returned by Javascript
#   time_zone_offset - int64 - Time zone offset (integer from -12 to 12)
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "recaptcha_token" in params and not isinstance(
        params["recaptcha_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: recaptcha_token must be an str"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "address" in params and not isinstance(params["address"], str):
        raise InvalidParameterError("Bad parameter: address must be an str")
    if "address_2" in params and not isinstance(params["address_2"], str):
        raise InvalidParameterError("Bad parameter: address_2 must be an str")
    if "city" in params and not isinstance(params["city"], str):
        raise InvalidParameterError("Bad parameter: city must be an str")
    if "contact_name" in params and not isinstance(
        params["contact_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: contact_name must be an str"
        )
    if "currency" in params and not isinstance(params["currency"], str):
        raise InvalidParameterError("Bad parameter: currency must be an str")
    if "email" in params and not isinstance(params["email"], str):
        raise InvalidParameterError("Bad parameter: email must be an str")
    if "language" in params and not isinstance(params["language"], str):
        raise InvalidParameterError("Bad parameter: language must be an str")
    if "phone_number" in params and not isinstance(
        params["phone_number"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: phone_number must be an str"
        )
    if "state" in params and not isinstance(params["state"], str):
        raise InvalidParameterError("Bad parameter: state must be an str")
    if "zip" in params and not isinstance(params["zip"], str):
        raise InvalidParameterError("Bad parameter: zip must be an str")
    if "form_name" in params and not isinstance(params["form_name"], str):
        raise InvalidParameterError("Bad parameter: form_name must be an str")
    if "lead_source" in params and not isinstance(params["lead_source"], str):
        raise InvalidParameterError(
            "Bad parameter: lead_source must be an str"
        )
    if "opportunity_comment" in params and not isinstance(
        params["opportunity_comment"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: opportunity_comment must be an str"
        )
    if "opportunity_type" in params and not isinstance(
        params["opportunity_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: opportunity_type must be an str"
        )
    if "gclid" in params and not isinstance(params["gclid"], str):
        raise InvalidParameterError("Bad parameter: gclid must be an str")
    if "original_brand" in params and not isinstance(
        params["original_brand"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: original_brand must be an str"
        )
    if "utm_campaign" in params and not isinstance(
        params["utm_campaign"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: utm_campaign must be an str"
        )
    if "utm_content" in params and not isinstance(params["utm_content"], str):
        raise InvalidParameterError(
            "Bad parameter: utm_content must be an str"
        )
    if "utm_domain" in params and not isinstance(params["utm_domain"], str):
        raise InvalidParameterError("Bad parameter: utm_domain must be an str")
    if "utm_medium" in params and not isinstance(params["utm_medium"], str):
        raise InvalidParameterError("Bad parameter: utm_medium must be an str")
    if "utm_source" in params and not isinstance(params["utm_source"], str):
        raise InvalidParameterError("Bad parameter: utm_source must be an str")
    if "utm_term" in params and not isinstance(params["utm_term"], str):
        raise InvalidParameterError("Bad parameter: utm_term must be an str")
    if "time_zone" in params and not isinstance(params["time_zone"], str):
        raise InvalidParameterError("Bad parameter: time_zone must be an str")
    if "time_zone_offset" in params and not isinstance(
        params["time_zone_offset"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: time_zone_offset must be an int"
        )
    response, options = Api.send_request("POST", "/leads", params, options)
    return Lead(response.data, options)


# Parameters:
#   code (required) - string - Lead lookup code.
#   recaptcha_token - string
#   name - string - Lead name
#   address - string - Lead address
#   address_2 - string - Lead address 2
#   city - string - Lead city
#   contact_name - string - Contact name at the company
#   currency - string - Lead preferred currency
#   email - string - Lead email address
#   language - string - Lead preferred language
#   phone_number - string - Lead phone number
#   state - string - Lead state
#   zip - string - Lead zipcode
#   form_name - string - Signup form name
#   lead_source - string - Source of the lead
#   opportunity_comment - string - Opportunity comment
#   opportunity_type - string - Type of opportunity to create
#   gclid - string - Google Adwords Click ID
#   original_brand - string - Brand: `files`, `exavault` or `mover`
#   utm_campaign - string - Marketing tracking - campaign
#   utm_content - string - Marketing tracking - content
#   utm_domain - string - Marketing tracking - domain
#   utm_medium - string - Marketing tracking - medium
#   utm_source - string - Marketing tracking - source
#   utm_term - string - Marketing tracking - term
#   time_zone - string - Time zone, as returned by Javascript
#   time_zone_offset - int64 - Time zone offset (integer from -12 to 12)
def update(code, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["code"] = code
    if "code" in params and not isinstance(params["code"], str):
        raise InvalidParameterError("Bad parameter: code must be an str")
    if "recaptcha_token" in params and not isinstance(
        params["recaptcha_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: recaptcha_token must be an str"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "address" in params and not isinstance(params["address"], str):
        raise InvalidParameterError("Bad parameter: address must be an str")
    if "address_2" in params and not isinstance(params["address_2"], str):
        raise InvalidParameterError("Bad parameter: address_2 must be an str")
    if "city" in params and not isinstance(params["city"], str):
        raise InvalidParameterError("Bad parameter: city must be an str")
    if "contact_name" in params and not isinstance(
        params["contact_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: contact_name must be an str"
        )
    if "currency" in params and not isinstance(params["currency"], str):
        raise InvalidParameterError("Bad parameter: currency must be an str")
    if "email" in params and not isinstance(params["email"], str):
        raise InvalidParameterError("Bad parameter: email must be an str")
    if "language" in params and not isinstance(params["language"], str):
        raise InvalidParameterError("Bad parameter: language must be an str")
    if "phone_number" in params and not isinstance(
        params["phone_number"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: phone_number must be an str"
        )
    if "state" in params and not isinstance(params["state"], str):
        raise InvalidParameterError("Bad parameter: state must be an str")
    if "zip" in params and not isinstance(params["zip"], str):
        raise InvalidParameterError("Bad parameter: zip must be an str")
    if "form_name" in params and not isinstance(params["form_name"], str):
        raise InvalidParameterError("Bad parameter: form_name must be an str")
    if "lead_source" in params and not isinstance(params["lead_source"], str):
        raise InvalidParameterError(
            "Bad parameter: lead_source must be an str"
        )
    if "opportunity_comment" in params and not isinstance(
        params["opportunity_comment"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: opportunity_comment must be an str"
        )
    if "opportunity_type" in params and not isinstance(
        params["opportunity_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: opportunity_type must be an str"
        )
    if "gclid" in params and not isinstance(params["gclid"], str):
        raise InvalidParameterError("Bad parameter: gclid must be an str")
    if "original_brand" in params and not isinstance(
        params["original_brand"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: original_brand must be an str"
        )
    if "utm_campaign" in params and not isinstance(
        params["utm_campaign"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: utm_campaign must be an str"
        )
    if "utm_content" in params and not isinstance(params["utm_content"], str):
        raise InvalidParameterError(
            "Bad parameter: utm_content must be an str"
        )
    if "utm_domain" in params and not isinstance(params["utm_domain"], str):
        raise InvalidParameterError("Bad parameter: utm_domain must be an str")
    if "utm_medium" in params and not isinstance(params["utm_medium"], str):
        raise InvalidParameterError("Bad parameter: utm_medium must be an str")
    if "utm_source" in params and not isinstance(params["utm_source"], str):
        raise InvalidParameterError("Bad parameter: utm_source must be an str")
    if "utm_term" in params and not isinstance(params["utm_term"], str):
        raise InvalidParameterError("Bad parameter: utm_term must be an str")
    if "time_zone" in params and not isinstance(params["time_zone"], str):
        raise InvalidParameterError("Bad parameter: time_zone must be an str")
    if "time_zone_offset" in params and not isinstance(
        params["time_zone_offset"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: time_zone_offset must be an int"
        )
    if "code" not in params:
        raise MissingParameterError("Parameter missing: code")
    response, options = Api.send_request(
        "PATCH",
        "/leads/{code}".format(code=quote(str(params["code"]), safe="")),
        params,
        options,
    )
    return Lead(response.data, options)


def new(*args, **kwargs):
    return Lead(*args, **kwargs)
