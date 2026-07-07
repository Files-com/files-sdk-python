import builtins  # noqa: F401
from decimal import Decimal
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Plan:
    __decimal_fields = {
        "activation_cost",
    }
    __decimal_array_fields = {}
    default_attributes = {
        "id": None,  # int64 - Plan ID
        "activation_cost": None,  # decimal - Activation cost (upfront)
        "addon_description": None,  # string - Description of add on charges
        "annually": None,  # string - Price annually
        "annually_addon": None,  # string - Addons price annually
        "automation_and_sync_flow_overage_cost": None,  # string - Cost per additional automation and sync flow
        "automation_and_sync_flows": None,  # int64 - Number of automation and sync flows included. 0 means unlimited.
        "child_sites": None,  # int64 - Number of child sites available
        "currency": None,  # string - Currency
        "dedicated_ip": None,  # boolean - Offers dedicated ip?
        "dedicated_ips": None,  # int64 - Number of dedicated IPs
        "domain_count": None,  # int64 - Number of custom domains
        "feature_bundle_eca": None,  # boolean - Does this plan include the ECA feature bundle?
        "feature_bundle_power": None,  # boolean - Does this plan include the Power feature bundle?
        "feature_bundle_premier": None,  # boolean - Does this plan include the Enterprise feature bundle?
        "feature_bundle_starter": None,  # boolean - Does this plan include the Starter feature bundle?
        "monthly": None,  # string - Price monthly
        "monthly_addon": None,  # string - Addons price monthly
        "name": None,  # string - Plan name
        "outbound_connections": None,  # int64 - Number of outbound connections
        "preview_page_limit": None,  # int64 - Number of previews available
        "regions_included": None,  # int64 - Number of storage regions included
        "remote_sync_interval": None,  # int64 - Number of minutes between remote sync
        "signup_page_marketing_text": None,  # string - Additional marketing text to show on signup page
        "system_users": None,  # int64 - # of System Users included.  0 means that system users are included in the normal user quota.
        "staging_sites": None,  # int64 - Number of child sites available
        "transformation_and_ai_credit_overage_cost_per_million": None,  # string - Cost per million additional transformation and AI credits
        "transformation_and_ai_credits": None,  # int64 - Transformation and AI credits included
        "trial_days": None,  # int64 - # of trial days included. Values of 0 or less mean no trial is offered.
        "user_cost": None,  # string - Cost per additional user
        "usage_cost": None,  # string - Usage cost per GB of overage
        "usage_included": None,  # int64 - Usage included per month, in GB
        "users": None,  # int64 - # of users included.  0 or -1 mean unlimited.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Plan.default_attributes.items():
            value = attributes.get(attribute, default_value)
            if attribute in Plan.__decimal_fields and value is not None:
                value = Decimal(str(value))
            if attribute in Plan.__decimal_array_fields and value is not None:
                value = [Decimal(str(v)) for v in (value or [])]
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Plan.default_attributes
            if getattr(self, k, None) is not None
        }
        for k in list(attrs.keys()):
            if k in Plan.__decimal_fields and attrs[k] is not None:
                attrs[k] = str(attrs[k])
            if k in Plan.__decimal_array_fields and attrs[k] is not None:
                attrs[k] = [str(v) for v in (attrs[k] or [])]
        return attrs


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
#   currency - string - Currency.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "currency" in params and not isinstance(params["currency"], str):
        raise InvalidParameterError("Bad parameter: currency must be an str")
    return ListObj(Plan, "GET", "/plans", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   currency - string - Currency.
def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "currency" in params and not isinstance(params["currency"], str):
        raise InvalidParameterError("Bad parameter: currency must be an str")
    response, options = Api.send_request(
        "POST", "/plans/create_export", params, options
    )
    return Export(response.data, options)


def new(*args, **kwargs):
    return Plan(*args, **kwargs)
