import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class SiemHttpDestination:
    default_attributes = {
        "id": None,  # int64 - SIEM HTTP Destination ID
        "name": None,  # string - Name for this Destination
        "destination_type": None,  # string - Destination Type
        "destination_url": None,  # string - Destination Url
        "additional_headers": None,  # object - Additional HTTP Headers included in calls to the destination URL
        "sending_active": None,  # boolean - Whether this SIEM HTTP Destination is currently being sent to or not
        "generic_payload_type": None,  # string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
        "splunk_token_masked": None,  # string - Applicable only for destination type: splunk. Authentication token provided by Splunk.
        "azure_dcr_immutable_id": None,  # string - Applicable only for destination type: azure. Immutable ID of the Data Collection Rule.
        "azure_stream_name": None,  # string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
        "azure_oauth_client_credentials_tenant_id": None,  # string - Applicable only for destination type: azure. Client Credentials OAuth Tenant ID.
        "azure_oauth_client_credentials_client_id": None,  # string - Applicable only for destination type: azure. Client Credentials OAuth Client ID.
        "azure_oauth_client_credentials_client_secret_masked": None,  # string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
        "qradar_username": None,  # string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
        "qradar_password_masked": None,  # string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
        "solar_winds_token_masked": None,  # string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
        "new_relic_api_key_masked": None,  # string - Applicable only for destination type: new_relic. API key provided by New Relic.
        "datadog_api_key_masked": None,  # string - Applicable only for destination type: datadog. API key provided by Datadog.
        "sftp_action_send_enabled": None,  # boolean - Whether or not sending is enabled for sftp_action logs.
        "sftp_action_records_sent_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "ftp_action_send_enabled": None,  # boolean - Whether or not sending is enabled for ftp_action logs.
        "ftp_action_records_sent_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "web_dav_action_send_enabled": None,  # boolean - Whether or not sending is enabled for web_dav_action logs.
        "web_dav_action_records_sent_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "sync_send_enabled": None,  # boolean - Whether or not sending is enabled for sync logs.
        "sync_records_sent_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "outbound_connection_send_enabled": None,  # boolean - Whether or not sending is enabled for outbound_connection logs.
        "outbound_connection_records_sent_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "automation_send_enabled": None,  # boolean - Whether or not sending is enabled for automation logs.
        "automation_records_sent_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "api_request_send_enabled": None,  # boolean - Whether or not sending is enabled for api_request logs.
        "api_request_records_sent_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "public_hosting_request_send_enabled": None,  # boolean - Whether or not sending is enabled for public_hosting_request logs.
        "public_hosting_request_records_sent_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "email_send_enabled": None,  # boolean - Whether or not sending is enabled for email logs.
        "email_records_sent_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "exavault_api_request_send_enabled": None,  # boolean - Whether or not sending is enabled for exavault_api_request logs.
        "exavault_api_request_records_sent_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "last_http_call_target_type": None,  # string - Type of URL that was last called. Can be `destination_url` or `azure_oauth_client_credentials_url`
        "last_http_call_success": None,  # boolean - Was the last HTTP call made successful?
        "last_http_call_response_code": None,  # int64 - Last HTTP Call Response Code
        "last_http_call_response_body": None,  # string - Last HTTP Call Response Body. Large responses are truncated.
        "last_http_call_error_message": None,  # string - Last HTTP Call Error Message if applicable
        "last_http_call_time": None,  # string - Time of Last HTTP Call
        "last_http_call_duration_ms": None,  # int64 - Duration of the last HTTP Call in milliseconds
        "most_recent_http_call_success_time": None,  # string - Time of Most Recent Successful HTTP Call
        "connection_test_entry": None,  # string - Connection Test Entry
        "splunk_token": None,  # string - Applicable only for destination type: splunk. Authentication token provided by Splunk.
        "azure_oauth_client_credentials_client_secret": None,  # string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
        "qradar_password": None,  # string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
        "solar_winds_token": None,  # string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
        "new_relic_api_key": None,  # string - Applicable only for destination type: new_relic. API key provided by New Relic.
        "datadog_api_key": None,  # string - Applicable only for destination type: datadog. API key provided by Datadog.
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
        ) in SiemHttpDestination.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in SiemHttpDestination.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   name - string - Name for this Destination
    #   additional_headers - object - Additional HTTP Headers included in calls to the destination URL
    #   sending_active - boolean - Whether this SIEM HTTP Destination is currently being sent to or not
    #   generic_payload_type - string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
    #   splunk_token - string - Applicable only for destination type: splunk. Authentication token provided by Splunk.
    #   azure_dcr_immutable_id - string - Applicable only for destination type: azure. Immutable ID of the Data Collection Rule.
    #   azure_stream_name - string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
    #   azure_oauth_client_credentials_tenant_id - string - Applicable only for destination type: azure. Client Credentials OAuth Tenant ID.
    #   azure_oauth_client_credentials_client_id - string - Applicable only for destination type: azure. Client Credentials OAuth Client ID.
    #   azure_oauth_client_credentials_client_secret - string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
    #   qradar_username - string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
    #   qradar_password - string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
    #   solar_winds_token - string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
    #   new_relic_api_key - string - Applicable only for destination type: new_relic. API key provided by New Relic.
    #   datadog_api_key - string - Applicable only for destination type: datadog. API key provided by Datadog.
    #   sftp_action_send_enabled - boolean - Whether or not sending is enabled for sftp_action logs.
    #   ftp_action_send_enabled - boolean - Whether or not sending is enabled for ftp_action logs.
    #   web_dav_action_send_enabled - boolean - Whether or not sending is enabled for web_dav_action logs.
    #   sync_send_enabled - boolean - Whether or not sending is enabled for sync logs.
    #   outbound_connection_send_enabled - boolean - Whether or not sending is enabled for outbound_connection logs.
    #   automation_send_enabled - boolean - Whether or not sending is enabled for automation logs.
    #   api_request_send_enabled - boolean - Whether or not sending is enabled for api_request logs.
    #   public_hosting_request_send_enabled - boolean - Whether or not sending is enabled for public_hosting_request logs.
    #   email_send_enabled - boolean - Whether or not sending is enabled for email logs.
    #   exavault_api_request_send_enabled - boolean - Whether or not sending is enabled for exavault_api_request logs.
    #   destination_type - string - Destination Type
    #   destination_url - string - Destination Url
    def update(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "generic_payload_type" in params and not isinstance(
            params["generic_payload_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: generic_payload_type must be an str"
            )
        if "splunk_token" in params and not isinstance(
            params["splunk_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: splunk_token must be an str"
            )
        if "azure_dcr_immutable_id" in params and not isinstance(
            params["azure_dcr_immutable_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_dcr_immutable_id must be an str"
            )
        if "azure_stream_name" in params and not isinstance(
            params["azure_stream_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_stream_name must be an str"
            )
        if (
            "azure_oauth_client_credentials_tenant_id" in params
            and not isinstance(
                params["azure_oauth_client_credentials_tenant_id"], str
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_oauth_client_credentials_tenant_id must be an str"
            )
        if (
            "azure_oauth_client_credentials_client_id" in params
            and not isinstance(
                params["azure_oauth_client_credentials_client_id"], str
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_oauth_client_credentials_client_id must be an str"
            )
        if (
            "azure_oauth_client_credentials_client_secret" in params
            and not isinstance(
                params["azure_oauth_client_credentials_client_secret"], str
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_oauth_client_credentials_client_secret must be an str"
            )
        if "qradar_username" in params and not isinstance(
            params["qradar_username"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: qradar_username must be an str"
            )
        if "qradar_password" in params and not isinstance(
            params["qradar_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: qradar_password must be an str"
            )
        if "solar_winds_token" in params and not isinstance(
            params["solar_winds_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: solar_winds_token must be an str"
            )
        if "new_relic_api_key" in params and not isinstance(
            params["new_relic_api_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: new_relic_api_key must be an str"
            )
        if "datadog_api_key" in params and not isinstance(
            params["datadog_api_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: datadog_api_key must be an str"
            )
        if "destination_type" in params and not isinstance(
            params["destination_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination_type must be an str"
            )
        if "destination_url" in params and not isinstance(
            params["destination_url"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination_url must be an str"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/siem_http_destinations/{id}".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    def delete(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        Api.send_request(
            "DELETE",
            "/siem_http_destinations/{id}".format(id=params["id"]),
            params,
            self.options,
        )

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            new_obj = self.update(self.get_attributes())
            self.set_attributes(new_obj.get_attributes())
            return True
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(
        SiemHttpDestination, "GET", "/siem_http_destinations", params, options
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Siem Http Destination ID.
def find(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "GET",
        "/siem_http_destinations/{id}".format(id=params["id"]),
        params,
        options,
    )
    return SiemHttpDestination(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   name - string - Name for this Destination
#   additional_headers - object - Additional HTTP Headers included in calls to the destination URL
#   sending_active - boolean - Whether this SIEM HTTP Destination is currently being sent to or not
#   generic_payload_type - string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
#   splunk_token - string - Applicable only for destination type: splunk. Authentication token provided by Splunk.
#   azure_dcr_immutable_id - string - Applicable only for destination type: azure. Immutable ID of the Data Collection Rule.
#   azure_stream_name - string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
#   azure_oauth_client_credentials_tenant_id - string - Applicable only for destination type: azure. Client Credentials OAuth Tenant ID.
#   azure_oauth_client_credentials_client_id - string - Applicable only for destination type: azure. Client Credentials OAuth Client ID.
#   azure_oauth_client_credentials_client_secret - string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
#   qradar_username - string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
#   qradar_password - string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
#   solar_winds_token - string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
#   new_relic_api_key - string - Applicable only for destination type: new_relic. API key provided by New Relic.
#   datadog_api_key - string - Applicable only for destination type: datadog. API key provided by Datadog.
#   sftp_action_send_enabled - boolean - Whether or not sending is enabled for sftp_action logs.
#   ftp_action_send_enabled - boolean - Whether or not sending is enabled for ftp_action logs.
#   web_dav_action_send_enabled - boolean - Whether or not sending is enabled for web_dav_action logs.
#   sync_send_enabled - boolean - Whether or not sending is enabled for sync logs.
#   outbound_connection_send_enabled - boolean - Whether or not sending is enabled for outbound_connection logs.
#   automation_send_enabled - boolean - Whether or not sending is enabled for automation logs.
#   api_request_send_enabled - boolean - Whether or not sending is enabled for api_request logs.
#   public_hosting_request_send_enabled - boolean - Whether or not sending is enabled for public_hosting_request logs.
#   email_send_enabled - boolean - Whether or not sending is enabled for email logs.
#   exavault_api_request_send_enabled - boolean - Whether or not sending is enabled for exavault_api_request logs.
#   destination_type (required) - string - Destination Type
#   destination_url (required) - string - Destination Url
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "additional_headers" in params and not isinstance(
        params["additional_headers"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: additional_headers must be an dict"
        )
    if "generic_payload_type" in params and not isinstance(
        params["generic_payload_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: generic_payload_type must be an str"
        )
    if "splunk_token" in params and not isinstance(
        params["splunk_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: splunk_token must be an str"
        )
    if "azure_dcr_immutable_id" in params and not isinstance(
        params["azure_dcr_immutable_id"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_dcr_immutable_id must be an str"
        )
    if "azure_stream_name" in params and not isinstance(
        params["azure_stream_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_stream_name must be an str"
        )
    if (
        "azure_oauth_client_credentials_tenant_id" in params
        and not isinstance(
            params["azure_oauth_client_credentials_tenant_id"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_oauth_client_credentials_tenant_id must be an str"
        )
    if (
        "azure_oauth_client_credentials_client_id" in params
        and not isinstance(
            params["azure_oauth_client_credentials_client_id"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_oauth_client_credentials_client_id must be an str"
        )
    if (
        "azure_oauth_client_credentials_client_secret" in params
        and not isinstance(
            params["azure_oauth_client_credentials_client_secret"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_oauth_client_credentials_client_secret must be an str"
        )
    if "qradar_username" in params and not isinstance(
        params["qradar_username"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: qradar_username must be an str"
        )
    if "qradar_password" in params and not isinstance(
        params["qradar_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: qradar_password must be an str"
        )
    if "solar_winds_token" in params and not isinstance(
        params["solar_winds_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: solar_winds_token must be an str"
        )
    if "new_relic_api_key" in params and not isinstance(
        params["new_relic_api_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: new_relic_api_key must be an str"
        )
    if "datadog_api_key" in params and not isinstance(
        params["datadog_api_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: datadog_api_key must be an str"
        )
    if "destination_type" in params and not isinstance(
        params["destination_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: destination_type must be an str"
        )
    if "destination_url" in params and not isinstance(
        params["destination_url"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: destination_url must be an str"
        )
    if "destination_type" not in params:
        raise MissingParameterError("Parameter missing: destination_type")
    if "destination_url" not in params:
        raise MissingParameterError("Parameter missing: destination_url")
    response, options = Api.send_request(
        "POST", "/siem_http_destinations", params, options
    )
    return SiemHttpDestination(response.data, options)


# Parameters:
#   siem_http_destination_id - int64 - SIEM HTTP Destination ID
#   destination_type - string - Destination Type
#   destination_url - string - Destination Url
#   name - string - Name for this Destination
#   additional_headers - object - Additional HTTP Headers included in calls to the destination URL
#   sending_active - boolean - Whether this SIEM HTTP Destination is currently being sent to or not
#   generic_payload_type - string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
#   splunk_token - string - Applicable only for destination type: splunk. Authentication token provided by Splunk.
#   azure_dcr_immutable_id - string - Applicable only for destination type: azure. Immutable ID of the Data Collection Rule.
#   azure_stream_name - string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
#   azure_oauth_client_credentials_tenant_id - string - Applicable only for destination type: azure. Client Credentials OAuth Tenant ID.
#   azure_oauth_client_credentials_client_id - string - Applicable only for destination type: azure. Client Credentials OAuth Client ID.
#   azure_oauth_client_credentials_client_secret - string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
#   qradar_username - string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
#   qradar_password - string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
#   solar_winds_token - string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
#   new_relic_api_key - string - Applicable only for destination type: new_relic. API key provided by New Relic.
#   datadog_api_key - string - Applicable only for destination type: datadog. API key provided by Datadog.
#   sftp_action_send_enabled - boolean - Whether or not sending is enabled for sftp_action logs.
#   ftp_action_send_enabled - boolean - Whether or not sending is enabled for ftp_action logs.
#   web_dav_action_send_enabled - boolean - Whether or not sending is enabled for web_dav_action logs.
#   sync_send_enabled - boolean - Whether or not sending is enabled for sync logs.
#   outbound_connection_send_enabled - boolean - Whether or not sending is enabled for outbound_connection logs.
#   automation_send_enabled - boolean - Whether or not sending is enabled for automation logs.
#   api_request_send_enabled - boolean - Whether or not sending is enabled for api_request logs.
#   public_hosting_request_send_enabled - boolean - Whether or not sending is enabled for public_hosting_request logs.
#   email_send_enabled - boolean - Whether or not sending is enabled for email logs.
#   exavault_api_request_send_enabled - boolean - Whether or not sending is enabled for exavault_api_request logs.
def send_test_entry(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "siem_http_destination_id" in params and not isinstance(
        params["siem_http_destination_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: siem_http_destination_id must be an int"
        )
    if "destination_type" in params and not isinstance(
        params["destination_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: destination_type must be an str"
        )
    if "destination_url" in params and not isinstance(
        params["destination_url"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: destination_url must be an str"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "additional_headers" in params and not isinstance(
        params["additional_headers"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: additional_headers must be an dict"
        )
    if "generic_payload_type" in params and not isinstance(
        params["generic_payload_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: generic_payload_type must be an str"
        )
    if "splunk_token" in params and not isinstance(
        params["splunk_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: splunk_token must be an str"
        )
    if "azure_dcr_immutable_id" in params and not isinstance(
        params["azure_dcr_immutable_id"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_dcr_immutable_id must be an str"
        )
    if "azure_stream_name" in params and not isinstance(
        params["azure_stream_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_stream_name must be an str"
        )
    if (
        "azure_oauth_client_credentials_tenant_id" in params
        and not isinstance(
            params["azure_oauth_client_credentials_tenant_id"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_oauth_client_credentials_tenant_id must be an str"
        )
    if (
        "azure_oauth_client_credentials_client_id" in params
        and not isinstance(
            params["azure_oauth_client_credentials_client_id"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_oauth_client_credentials_client_id must be an str"
        )
    if (
        "azure_oauth_client_credentials_client_secret" in params
        and not isinstance(
            params["azure_oauth_client_credentials_client_secret"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_oauth_client_credentials_client_secret must be an str"
        )
    if "qradar_username" in params and not isinstance(
        params["qradar_username"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: qradar_username must be an str"
        )
    if "qradar_password" in params and not isinstance(
        params["qradar_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: qradar_password must be an str"
        )
    if "solar_winds_token" in params and not isinstance(
        params["solar_winds_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: solar_winds_token must be an str"
        )
    if "new_relic_api_key" in params and not isinstance(
        params["new_relic_api_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: new_relic_api_key must be an str"
        )
    if "datadog_api_key" in params and not isinstance(
        params["datadog_api_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: datadog_api_key must be an str"
        )
    Api.send_request(
        "POST", "/siem_http_destinations/send_test_entry", params, options
    )


# Parameters:
#   name - string - Name for this Destination
#   additional_headers - object - Additional HTTP Headers included in calls to the destination URL
#   sending_active - boolean - Whether this SIEM HTTP Destination is currently being sent to or not
#   generic_payload_type - string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
#   splunk_token - string - Applicable only for destination type: splunk. Authentication token provided by Splunk.
#   azure_dcr_immutable_id - string - Applicable only for destination type: azure. Immutable ID of the Data Collection Rule.
#   azure_stream_name - string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
#   azure_oauth_client_credentials_tenant_id - string - Applicable only for destination type: azure. Client Credentials OAuth Tenant ID.
#   azure_oauth_client_credentials_client_id - string - Applicable only for destination type: azure. Client Credentials OAuth Client ID.
#   azure_oauth_client_credentials_client_secret - string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
#   qradar_username - string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
#   qradar_password - string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
#   solar_winds_token - string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
#   new_relic_api_key - string - Applicable only for destination type: new_relic. API key provided by New Relic.
#   datadog_api_key - string - Applicable only for destination type: datadog. API key provided by Datadog.
#   sftp_action_send_enabled - boolean - Whether or not sending is enabled for sftp_action logs.
#   ftp_action_send_enabled - boolean - Whether or not sending is enabled for ftp_action logs.
#   web_dav_action_send_enabled - boolean - Whether or not sending is enabled for web_dav_action logs.
#   sync_send_enabled - boolean - Whether or not sending is enabled for sync logs.
#   outbound_connection_send_enabled - boolean - Whether or not sending is enabled for outbound_connection logs.
#   automation_send_enabled - boolean - Whether or not sending is enabled for automation logs.
#   api_request_send_enabled - boolean - Whether or not sending is enabled for api_request logs.
#   public_hosting_request_send_enabled - boolean - Whether or not sending is enabled for public_hosting_request logs.
#   email_send_enabled - boolean - Whether or not sending is enabled for email logs.
#   exavault_api_request_send_enabled - boolean - Whether or not sending is enabled for exavault_api_request logs.
#   destination_type - string - Destination Type
#   destination_url - string - Destination Url
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "additional_headers" in params and not isinstance(
        params["additional_headers"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: additional_headers must be an dict"
        )
    if "generic_payload_type" in params and not isinstance(
        params["generic_payload_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: generic_payload_type must be an str"
        )
    if "splunk_token" in params and not isinstance(
        params["splunk_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: splunk_token must be an str"
        )
    if "azure_dcr_immutable_id" in params and not isinstance(
        params["azure_dcr_immutable_id"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_dcr_immutable_id must be an str"
        )
    if "azure_stream_name" in params and not isinstance(
        params["azure_stream_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_stream_name must be an str"
        )
    if (
        "azure_oauth_client_credentials_tenant_id" in params
        and not isinstance(
            params["azure_oauth_client_credentials_tenant_id"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_oauth_client_credentials_tenant_id must be an str"
        )
    if (
        "azure_oauth_client_credentials_client_id" in params
        and not isinstance(
            params["azure_oauth_client_credentials_client_id"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_oauth_client_credentials_client_id must be an str"
        )
    if (
        "azure_oauth_client_credentials_client_secret" in params
        and not isinstance(
            params["azure_oauth_client_credentials_client_secret"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_oauth_client_credentials_client_secret must be an str"
        )
    if "qradar_username" in params and not isinstance(
        params["qradar_username"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: qradar_username must be an str"
        )
    if "qradar_password" in params and not isinstance(
        params["qradar_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: qradar_password must be an str"
        )
    if "solar_winds_token" in params and not isinstance(
        params["solar_winds_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: solar_winds_token must be an str"
        )
    if "new_relic_api_key" in params and not isinstance(
        params["new_relic_api_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: new_relic_api_key must be an str"
        )
    if "datadog_api_key" in params and not isinstance(
        params["datadog_api_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: datadog_api_key must be an str"
        )
    if "destination_type" in params and not isinstance(
        params["destination_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: destination_type must be an str"
        )
    if "destination_url" in params and not isinstance(
        params["destination_url"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: destination_url must be an str"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/siem_http_destinations/{id}".format(id=params["id"]),
        params,
        options,
    )
    return SiemHttpDestination(response.data, options)


def delete(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    Api.send_request(
        "DELETE",
        "/siem_http_destinations/{id}".format(id=params["id"]),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return SiemHttpDestination(*args, **kwargs)
