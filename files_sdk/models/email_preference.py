import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class EmailPreference:
    default_attributes = {
        "email": None,  # email - Email address
        "notifications": None,  # array(object) - A list of notifications
        "bundle_notifications": None,  # array(object) - A list of bundle notifications
        "receive_admin_alerts": None,  # boolean - Deprecated. Use granular admin email preferences instead.
        "notify_on_all_site_warnings": None,  # boolean - Receive site warnings?
        "notify_on_all_sso_failures": None,  # boolean - Receive sso/scim/ldap configuration/sync failures?
        "notify_on_all_user_security_events": None,  # boolean - Receive user security events?
        "notify_on_all_pending_work_failures": None,  # boolean - Receive pending work failures?
        "notify_on_all_siem_http_destination_failures": None,  # boolean - Receive siem failures?
        "notify_on_all_sync_failures": None,  # boolean - Receive sync failures?
        "notify_on_all_automation_failures": None,  # boolean - Receive automation failures?
        "notify_on_all_expectation_failures": None,  # boolean - Receive expectation failures and misses?
        "receive_marketing_mail": None,  # boolean - Receive marketing mail?
        "receive_transactional_mail": None,  # boolean - Receive transactional (service-related) mail?
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
        ) in EmailPreference.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in EmailPreference.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


# Parameters:
#   token (required) - string - Email preferences token.
def get(token, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["token"] = token
    if "token" in params and not isinstance(params["token"], str):
        raise InvalidParameterError("Bad parameter: token must be an str")
    if "token" not in params:
        raise MissingParameterError("Parameter missing: token")
    response, options = Api.send_request(
        "GET",
        "/email_preferences/{token}".format(
            token=quote(str(params["token"]), safe="")
        ),
        params,
        options,
    )
    return EmailPreference(response.data, options)


# Parameters:
#   token (required) - string - Email preferences token.
#   user[receive_admin_alerts] - boolean
#   user[notify_on_all_site_warnings] - boolean
#   user[notify_on_all_sso_failures] - boolean
#   user[notify_on_all_user_security_events] - boolean
#   user[notify_on_all_pending_work_failures] - boolean
#   user[notify_on_all_siem_http_destination_failures] - boolean
#   user[notify_on_all_sync_failures] - boolean
#   user[notify_on_all_automation_failures] - boolean
#   user[notify_on_all_expectation_failures] - boolean
#   user[unsubscribe_marketing] - boolean
#   user[unsubscribe_transactional] - boolean
#   user[unsubscribe] - boolean
#   user[notifications][id] (required) - array(int64)
#   user[notifications][group] - array(boolean)
#   user[notifications][send_interval] - array(string)
#   user[notifications][unsubscribe] - array(boolean)
#   user[bundle_notifications][id] (required) - array(int64)
#   user[bundle_notifications][unsubscribe] - array(boolean)
def update(token, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["token"] = token
    if "token" in params and not isinstance(params["token"], str):
        raise InvalidParameterError("Bad parameter: token must be an str")
    if "token" not in params:
        raise MissingParameterError("Parameter missing: token")
    response, options = Api.send_request(
        "PATCH",
        "/email_preferences/{token}".format(
            token=quote(str(params["token"]), safe="")
        ),
        params,
        options,
    )
    return EmailPreference(response.data, options)


def new(*args, **kwargs):
    return EmailPreference(*args, **kwargs)
