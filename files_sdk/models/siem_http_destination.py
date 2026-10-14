import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
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


class SiemHttpDestination:
    """A siem http destination record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - SIEM HTTP Destination ID
        name: string - Name for this Destination
        destination_type: string - Destination Type
        destination_url: string - Destination Url
        file_destination_path: string - Applicable only for destination type: file. Destination folder path on Files.com.
        file_format: string - Applicable only for destination type: file. Generated file format.
        file_interval_minutes: int64 - Applicable only for destination type: file. Interval, in minutes, between file deliveries.
        additional_headers: object - Additional HTTP Headers included in calls to the destination URL
        sending_active: boolean - Whether this SIEM HTTP Destination is currently being sent to or not
        generic_payload_type: string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
        splunk_token_masked: string - Applicable only for destination types: splunk, splunk_compatible. Authentication token for the destination.
        crowdstrike_token_masked: string - Applicable only for destination type: crowdstrike. Authentication token provided by Crowdstrike.
        azure_dcr_immutable_id: string - Applicable only for destination types: azure, azure_legacy. Immutable ID of the Data Collection Rule.
        azure_stream_name: string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
        azure_oauth_client_credentials_tenant_id: string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Tenant ID.
        azure_oauth_client_credentials_client_id: string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Client ID.
        azure_oauth_client_credentials_client_secret_masked: string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Client Secret.
        qradar_username: string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
        qradar_password_masked: string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
        solar_winds_token_masked: string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
        new_relic_api_key_masked: string - Applicable only for destination type: new_relic. API key provided by New Relic.
        datadog_api_key_masked: string - Applicable only for destination type: datadog. API key provided by Datadog.
        action_send_enabled: boolean - Whether or not sending is enabled for action logs.
        action_entries_sent: int64 - Number of log entries sent for the lifetime of this destination.
        sftp_action_send_enabled: boolean - Whether or not sending is enabled for sftp_action logs.
        sftp_action_entries_sent: int64 - Number of log entries sent for the lifetime of this destination.
        ftp_action_send_enabled: boolean - Whether or not sending is enabled for ftp_action logs.
        ftp_action_entries_sent: int64 - Number of log entries sent for the lifetime of this destination.
        web_dav_action_send_enabled: boolean - Whether or not sending is enabled for web_dav_action logs.
        web_dav_action_entries_sent: int64 - Number of log entries sent for the lifetime of this destination.
        sync_send_enabled: boolean - Whether or not sending is enabled for sync logs.
        sync_entries_sent: int64 - Number of log entries sent for the lifetime of this destination.
        outbound_connection_send_enabled: boolean - Whether or not sending is enabled for outbound_connection logs.
        outbound_connection_entries_sent: int64 - Number of log entries sent for the lifetime of this destination.
        automation_send_enabled: boolean - Whether or not sending is enabled for automation logs.
        automation_entries_sent: int64 - Number of log entries sent for the lifetime of this destination.
        api_request_send_enabled: boolean - Whether or not sending is enabled for api_request logs.
        api_request_entries_sent: int64 - Number of log entries sent for the lifetime of this destination.
        public_hosting_request_send_enabled: boolean - Whether or not sending is enabled for public_hosting_request logs.
        public_hosting_request_entries_sent: int64 - Number of log entries sent for the lifetime of this destination.
        email_send_enabled: boolean - Whether or not sending is enabled for email logs.
        email_entries_sent: int64 - Number of log entries sent for the lifetime of this destination.
        exavault_api_request_send_enabled: boolean - Whether or not sending is enabled for exavault_api_request logs.
        exavault_api_request_entries_sent: int64 - Number of log entries sent for the lifetime of this destination.
        settings_change_send_enabled: boolean - Whether or not sending is enabled for settings_change logs.
        settings_change_entries_sent: int64 - Number of log entries sent for the lifetime of this destination.
        last_http_call_target_type: string - Type of URL that was last called. Can be `destination_url` or `azure_oauth_client_credentials_url`
        last_http_call_success: boolean - Was the last HTTP call made successful?
        last_http_call_response_code: int64 - Last HTTP Call Response Code
        last_http_call_response_body: string - Last HTTP Call Response Body. Large responses are truncated.
        last_http_call_error_message: string - Last HTTP Call Error Message if applicable
        last_http_call_time: string - Time of Last HTTP Call
        last_http_call_duration_ms: int64 - Duration of the last HTTP Call in milliseconds
        most_recent_http_call_success_time: string - Time of Most Recent Successful HTTP Call
        connection_test_entry: string - Connection Test Entry
        splunk_token: string - Applicable only for destination types: splunk, splunk_compatible. Authentication token for the destination.
        crowdstrike_token: string - Applicable only for destination type: crowdstrike. Authentication token provided by Crowdstrike.
        azure_oauth_client_credentials_client_secret: string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
        qradar_password: string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
        solar_winds_token: string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
        new_relic_api_key: string - Applicable only for destination type: new_relic. API key provided by New Relic.
        datadog_api_key: string - Applicable only for destination type: datadog. API key provided by Datadog.
    """

    default_attributes = {
        "id": None,  # int64 - SIEM HTTP Destination ID
        "name": None,  # string - Name for this Destination
        "destination_type": None,  # string - Destination Type
        "destination_url": None,  # string - Destination Url
        "file_destination_path": None,  # string - Applicable only for destination type: file. Destination folder path on Files.com.
        "file_format": None,  # string - Applicable only for destination type: file. Generated file format.
        "file_interval_minutes": None,  # int64 - Applicable only for destination type: file. Interval, in minutes, between file deliveries.
        "additional_headers": None,  # object - Additional HTTP Headers included in calls to the destination URL
        "sending_active": None,  # boolean - Whether this SIEM HTTP Destination is currently being sent to or not
        "generic_payload_type": None,  # string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
        "splunk_token_masked": None,  # string - Applicable only for destination types: splunk, splunk_compatible. Authentication token for the destination.
        "crowdstrike_token_masked": None,  # string - Applicable only for destination type: crowdstrike. Authentication token provided by Crowdstrike.
        "azure_dcr_immutable_id": None,  # string - Applicable only for destination types: azure, azure_legacy. Immutable ID of the Data Collection Rule.
        "azure_stream_name": None,  # string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
        "azure_oauth_client_credentials_tenant_id": None,  # string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Tenant ID.
        "azure_oauth_client_credentials_client_id": None,  # string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Client ID.
        "azure_oauth_client_credentials_client_secret_masked": None,  # string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Client Secret.
        "qradar_username": None,  # string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
        "qradar_password_masked": None,  # string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
        "solar_winds_token_masked": None,  # string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
        "new_relic_api_key_masked": None,  # string - Applicable only for destination type: new_relic. API key provided by New Relic.
        "datadog_api_key_masked": None,  # string - Applicable only for destination type: datadog. API key provided by Datadog.
        "action_send_enabled": None,  # boolean - Whether or not sending is enabled for action logs.
        "action_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "sftp_action_send_enabled": None,  # boolean - Whether or not sending is enabled for sftp_action logs.
        "sftp_action_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "ftp_action_send_enabled": None,  # boolean - Whether or not sending is enabled for ftp_action logs.
        "ftp_action_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "web_dav_action_send_enabled": None,  # boolean - Whether or not sending is enabled for web_dav_action logs.
        "web_dav_action_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "sync_send_enabled": None,  # boolean - Whether or not sending is enabled for sync logs.
        "sync_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "outbound_connection_send_enabled": None,  # boolean - Whether or not sending is enabled for outbound_connection logs.
        "outbound_connection_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "automation_send_enabled": None,  # boolean - Whether or not sending is enabled for automation logs.
        "automation_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "api_request_send_enabled": None,  # boolean - Whether or not sending is enabled for api_request logs.
        "api_request_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "public_hosting_request_send_enabled": None,  # boolean - Whether or not sending is enabled for public_hosting_request logs.
        "public_hosting_request_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "email_send_enabled": None,  # boolean - Whether or not sending is enabled for email logs.
        "email_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "exavault_api_request_send_enabled": None,  # boolean - Whether or not sending is enabled for exavault_api_request logs.
        "exavault_api_request_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "settings_change_send_enabled": None,  # boolean - Whether or not sending is enabled for settings_change logs.
        "settings_change_entries_sent": None,  # int64 - Number of log entries sent for the lifetime of this destination.
        "last_http_call_target_type": None,  # string - Type of URL that was last called. Can be `destination_url` or `azure_oauth_client_credentials_url`
        "last_http_call_success": None,  # boolean - Was the last HTTP call made successful?
        "last_http_call_response_code": None,  # int64 - Last HTTP Call Response Code
        "last_http_call_response_body": None,  # string - Last HTTP Call Response Body. Large responses are truncated.
        "last_http_call_error_message": None,  # string - Last HTTP Call Error Message if applicable
        "last_http_call_time": None,  # string - Time of Last HTTP Call
        "last_http_call_duration_ms": None,  # int64 - Duration of the last HTTP Call in milliseconds
        "most_recent_http_call_success_time": None,  # string - Time of Most Recent Successful HTTP Call
        "connection_test_entry": None,  # string - Connection Test Entry
        "splunk_token": None,  # string - Applicable only for destination types: splunk, splunk_compatible. Authentication token for the destination.
        "crowdstrike_token": None,  # string - Applicable only for destination type: crowdstrike. Authentication token provided by Crowdstrike.
        "azure_oauth_client_credentials_client_secret": None,  # string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
        "qradar_password": None,  # string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
        "solar_winds_token": None,  # string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
        "new_relic_api_key": None,  # string - Applicable only for destination type: new_relic. API key provided by New Relic.
        "datadog_api_key": None,  # string - Applicable only for destination type: datadog. API key provided by Datadog.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    name: str | None
    destination_type: str | None
    destination_url: str | None
    file_destination_path: str | None
    file_format: str | None
    file_interval_minutes: int | None
    additional_headers: dict[str, Any] | None
    sending_active: bool | None
    generic_payload_type: str | None
    splunk_token_masked: str | None
    crowdstrike_token_masked: str | None
    azure_dcr_immutable_id: str | None
    azure_stream_name: str | None
    azure_oauth_client_credentials_tenant_id: str | None
    azure_oauth_client_credentials_client_id: str | None
    azure_oauth_client_credentials_client_secret_masked: str | None
    qradar_username: str | None
    qradar_password_masked: str | None
    solar_winds_token_masked: str | None
    new_relic_api_key_masked: str | None
    datadog_api_key_masked: str | None
    action_send_enabled: bool | None
    action_entries_sent: int | None
    sftp_action_send_enabled: bool | None
    sftp_action_entries_sent: int | None
    ftp_action_send_enabled: bool | None
    ftp_action_entries_sent: int | None
    web_dav_action_send_enabled: bool | None
    web_dav_action_entries_sent: int | None
    sync_send_enabled: bool | None
    sync_entries_sent: int | None
    outbound_connection_send_enabled: bool | None
    outbound_connection_entries_sent: int | None
    automation_send_enabled: bool | None
    automation_entries_sent: int | None
    api_request_send_enabled: bool | None
    api_request_entries_sent: int | None
    public_hosting_request_send_enabled: bool | None
    public_hosting_request_entries_sent: int | None
    email_send_enabled: bool | None
    email_entries_sent: int | None
    exavault_api_request_send_enabled: bool | None
    exavault_api_request_entries_sent: int | None
    settings_change_send_enabled: bool | None
    settings_change_entries_sent: int | None
    last_http_call_target_type: str | None
    last_http_call_success: bool | None
    last_http_call_response_code: int | None
    last_http_call_response_body: str | None
    last_http_call_error_message: str | None
    last_http_call_time: str | None
    last_http_call_duration_ms: int | None
    most_recent_http_call_success_time: str | None
    connection_test_entry: str | None
    splunk_token: str | None
    crowdstrike_token: str | None
    azure_oauth_client_credentials_client_secret: str | None
    qradar_password: str | None
    solar_winds_token: str | None
    new_relic_api_key: str | None
    datadog_api_key: str | None

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
        for (
            attribute,
            default_value,
        ) in SiemHttpDestination.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SiemHttpDestination.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          name - string - Name for this Destination
          additional_headers - object - Additional HTTP Headers included in calls to the destination URL
          sending_active - boolean - Whether this SIEM HTTP Destination is currently being sent to or not
          generic_payload_type - string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
          file_destination_path - string - Applicable only for destination type: file. Destination folder path on Files.com.
          file_format - string - Applicable only for destination type: file. Generated file format.
          file_interval_minutes - int64 - Applicable only for destination type: file. Interval, in minutes, between file deliveries. Valid values are 5, 10, 15, 20, 30, 60, 90, 180, 240, 360.
          splunk_token - string - Applicable only for destination types: splunk, splunk_compatible. Authentication token for the destination.
          crowdstrike_token - string - Applicable only for destination type: crowdstrike. Authentication token provided by Crowdstrike.
          azure_dcr_immutable_id - string - Applicable only for destination types: azure, azure_legacy. Immutable ID of the Data Collection Rule.
          azure_stream_name - string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
          azure_oauth_client_credentials_tenant_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Tenant ID.
          azure_oauth_client_credentials_client_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Client ID.
          azure_oauth_client_credentials_client_secret - string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
          qradar_username - string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
          qradar_password - string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
          solar_winds_token - string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
          new_relic_api_key - string - Applicable only for destination type: new_relic. API key provided by New Relic.
          datadog_api_key - string - Applicable only for destination type: datadog. API key provided by Datadog.
          action_send_enabled - boolean - Whether or not sending is enabled for action logs.
          sftp_action_send_enabled - boolean - Whether or not sending is enabled for sftp_action logs.
          ftp_action_send_enabled - boolean - Whether or not sending is enabled for ftp_action logs.
          web_dav_action_send_enabled - boolean - Whether or not sending is enabled for web_dav_action logs.
          sync_send_enabled - boolean - Whether or not sending is enabled for sync logs.
          outbound_connection_send_enabled - boolean - Whether or not sending is enabled for outbound_connection logs.
          automation_send_enabled - boolean - Whether or not sending is enabled for automation logs.
          api_request_send_enabled - boolean - Whether or not sending is enabled for api_request logs.
          public_hosting_request_send_enabled - boolean - Whether or not sending is enabled for public_hosting_request logs.
          email_send_enabled - boolean - Whether or not sending is enabled for email logs.
          exavault_api_request_send_enabled - boolean - Whether or not sending is enabled for exavault_api_request logs.
          settings_change_send_enabled - boolean - Whether or not sending is enabled for settings_change logs.
          destination_type - string - Destination Type
          destination_url - string - Destination Url
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "sending_active" in params and isinstance(
            params["sending_active"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: sending_active must be an bool"
            )
        if "generic_payload_type" in params and not isinstance(
            params["generic_payload_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: generic_payload_type must be an str"
            )
        if "file_destination_path" in params and not isinstance(
            params["file_destination_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: file_destination_path must be an str"
            )
        if "file_format" in params and not isinstance(
            params["file_format"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: file_format must be an str"
            )
        if "file_interval_minutes" in params and (
            not isinstance(params["file_interval_minutes"], int)
            or isinstance(params["file_interval_minutes"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: file_interval_minutes must be an int"
            )
        if "splunk_token" in params and not isinstance(
            params["splunk_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: splunk_token must be an str"
            )
        if "crowdstrike_token" in params and not isinstance(
            params["crowdstrike_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: crowdstrike_token must be an str"
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
        if "action_send_enabled" in params and isinstance(
            params["action_send_enabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: action_send_enabled must be an bool"
            )
        if "sftp_action_send_enabled" in params and isinstance(
            params["sftp_action_send_enabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: sftp_action_send_enabled must be an bool"
            )
        if "ftp_action_send_enabled" in params and isinstance(
            params["ftp_action_send_enabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: ftp_action_send_enabled must be an bool"
            )
        if "web_dav_action_send_enabled" in params and isinstance(
            params["web_dav_action_send_enabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: web_dav_action_send_enabled must be an bool"
            )
        if "sync_send_enabled" in params and isinstance(
            params["sync_send_enabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: sync_send_enabled must be an bool"
            )
        if "outbound_connection_send_enabled" in params and isinstance(
            params["outbound_connection_send_enabled"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: outbound_connection_send_enabled must be an bool"
            )
        if "automation_send_enabled" in params and isinstance(
            params["automation_send_enabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: automation_send_enabled must be an bool"
            )
        if "api_request_send_enabled" in params and isinstance(
            params["api_request_send_enabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: api_request_send_enabled must be an bool"
            )
        if "public_hosting_request_send_enabled" in params and isinstance(
            params["public_hosting_request_send_enabled"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: public_hosting_request_send_enabled must be an bool"
            )
        if "email_send_enabled" in params and isinstance(
            params["email_send_enabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: email_send_enabled must be an bool"
            )
        if "exavault_api_request_send_enabled" in params and isinstance(
            params["exavault_api_request_send_enabled"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: exavault_api_request_send_enabled must be an bool"
            )
        if "settings_change_send_enabled" in params and isinstance(
            params["settings_change_send_enabled"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: settings_change_send_enabled must be an bool"
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
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH",
            "/siem_http_destinations/" + path_value(params["id"]),
            params,
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE",
            "/siem_http_destinations/" + path_value(params["id"]),
            params,
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Update this object on the server if it has an id, or else create
        it, taking in place the record the server returns."""
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = SiemHttpDestinationResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class SiemHttpDestinationResource:
    """SiemHttpDestination operations that use one client's configuration.

    Get one from a client, such as ``client.siem_http_destination``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SiemHttpDestination]:
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
        return ListObj(
            SiemHttpDestination,
            "GET",
            "/siem_http_destinations",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SiemHttpDestination]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SiemHttpDestination:
        """Parameters:
        id (required) - int64 - Siem Http Destination ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> SiemHttpDestination:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET",
            "/siem_http_destinations/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, SiemHttpDestination)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SiemHttpDestination:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SiemHttpDestination:
        """Parameters:
        name - string - Name for this Destination
        additional_headers - object - Additional HTTP Headers included in calls to the destination URL
        sending_active - boolean - Whether this SIEM HTTP Destination is currently being sent to or not
        generic_payload_type - string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
        file_destination_path - string - Applicable only for destination type: file. Destination folder path on Files.com.
        file_format - string - Applicable only for destination type: file. Generated file format.
        file_interval_minutes - int64 - Applicable only for destination type: file. Interval, in minutes, between file deliveries. Valid values are 5, 10, 15, 20, 30, 60, 90, 180, 240, 360.
        splunk_token - string - Applicable only for destination types: splunk, splunk_compatible. Authentication token for the destination.
        crowdstrike_token - string - Applicable only for destination type: crowdstrike. Authentication token provided by Crowdstrike.
        azure_dcr_immutable_id - string - Applicable only for destination types: azure, azure_legacy. Immutable ID of the Data Collection Rule.
        azure_stream_name - string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
        azure_oauth_client_credentials_tenant_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Tenant ID.
        azure_oauth_client_credentials_client_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Client ID.
        azure_oauth_client_credentials_client_secret - string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
        qradar_username - string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
        qradar_password - string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
        solar_winds_token - string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
        new_relic_api_key - string - Applicable only for destination type: new_relic. API key provided by New Relic.
        datadog_api_key - string - Applicable only for destination type: datadog. API key provided by Datadog.
        action_send_enabled - boolean - Whether or not sending is enabled for action logs.
        sftp_action_send_enabled - boolean - Whether or not sending is enabled for sftp_action logs.
        ftp_action_send_enabled - boolean - Whether or not sending is enabled for ftp_action logs.
        web_dav_action_send_enabled - boolean - Whether or not sending is enabled for web_dav_action logs.
        sync_send_enabled - boolean - Whether or not sending is enabled for sync logs.
        outbound_connection_send_enabled - boolean - Whether or not sending is enabled for outbound_connection logs.
        automation_send_enabled - boolean - Whether or not sending is enabled for automation logs.
        api_request_send_enabled - boolean - Whether or not sending is enabled for api_request logs.
        public_hosting_request_send_enabled - boolean - Whether or not sending is enabled for public_hosting_request logs.
        email_send_enabled - boolean - Whether or not sending is enabled for email logs.
        exavault_api_request_send_enabled - boolean - Whether or not sending is enabled for exavault_api_request logs.
        settings_change_send_enabled - boolean - Whether or not sending is enabled for settings_change logs.
        destination_type (required) - string - Destination Type
        destination_url - string - Destination Url
        """
        params = copy_params(params)
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "additional_headers" in params and not isinstance(
            params["additional_headers"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: additional_headers must be an dict"
            )
        if "sending_active" in params and not isinstance(
            params["sending_active"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sending_active must be an bool"
            )
        if "generic_payload_type" in params and not isinstance(
            params["generic_payload_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: generic_payload_type must be an str"
            )
        if "file_destination_path" in params and not isinstance(
            params["file_destination_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: file_destination_path must be an str"
            )
        if "file_format" in params and not isinstance(
            params["file_format"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: file_format must be an str"
            )
        if "file_interval_minutes" in params and (
            not isinstance(params["file_interval_minutes"], int)
            or isinstance(params["file_interval_minutes"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: file_interval_minutes must be an int"
            )
        if "splunk_token" in params and not isinstance(
            params["splunk_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: splunk_token must be an str"
            )
        if "crowdstrike_token" in params and not isinstance(
            params["crowdstrike_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: crowdstrike_token must be an str"
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
        if "action_send_enabled" in params and not isinstance(
            params["action_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: action_send_enabled must be an bool"
            )
        if "sftp_action_send_enabled" in params and not isinstance(
            params["sftp_action_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sftp_action_send_enabled must be an bool"
            )
        if "ftp_action_send_enabled" in params and not isinstance(
            params["ftp_action_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: ftp_action_send_enabled must be an bool"
            )
        if "web_dav_action_send_enabled" in params and not isinstance(
            params["web_dav_action_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: web_dav_action_send_enabled must be an bool"
            )
        if "sync_send_enabled" in params and not isinstance(
            params["sync_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sync_send_enabled must be an bool"
            )
        if "outbound_connection_send_enabled" in params and not isinstance(
            params["outbound_connection_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: outbound_connection_send_enabled must be an bool"
            )
        if "automation_send_enabled" in params and not isinstance(
            params["automation_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: automation_send_enabled must be an bool"
            )
        if "api_request_send_enabled" in params and not isinstance(
            params["api_request_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: api_request_send_enabled must be an bool"
            )
        if "public_hosting_request_send_enabled" in params and not isinstance(
            params["public_hosting_request_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: public_hosting_request_send_enabled must be an bool"
            )
        if "email_send_enabled" in params and not isinstance(
            params["email_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: email_send_enabled must be an bool"
            )
        if "exavault_api_request_send_enabled" in params and not isinstance(
            params["exavault_api_request_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: exavault_api_request_send_enabled must be an bool"
            )
        if "settings_change_send_enabled" in params and not isinstance(
            params["settings_change_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: settings_change_send_enabled must be an bool"
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
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/siem_http_destinations", params)
        return operation.decode_model(response, SiemHttpDestination)

    def send_test_entry(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Parameters:
        siem_http_destination_id - int64 - SIEM HTTP Destination ID
        destination_type - string - Destination Type
        destination_url - string - Destination Url
        name - string - Name for this Destination
        additional_headers - object - Additional HTTP Headers included in calls to the destination URL
        sending_active - boolean - Whether this SIEM HTTP Destination is currently being sent to or not
        generic_payload_type - string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
        file_destination_path - string - Applicable only for destination type: file. Destination folder path on Files.com.
        file_format - string - Applicable only for destination type: file. Generated file format.
        file_interval_minutes - int64 - Applicable only for destination type: file. Interval, in minutes, between file deliveries. Valid values are 5, 10, 15, 20, 30, 60, 90, 180, 240, 360.
        splunk_token - string - Applicable only for destination types: splunk, splunk_compatible. Authentication token for the destination.
        crowdstrike_token - string - Applicable only for destination type: crowdstrike. Authentication token provided by Crowdstrike.
        azure_dcr_immutable_id - string - Applicable only for destination types: azure, azure_legacy. Immutable ID of the Data Collection Rule.
        azure_stream_name - string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
        azure_oauth_client_credentials_tenant_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Tenant ID.
        azure_oauth_client_credentials_client_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Client ID.
        azure_oauth_client_credentials_client_secret - string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
        qradar_username - string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
        qradar_password - string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
        solar_winds_token - string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
        new_relic_api_key - string - Applicable only for destination type: new_relic. API key provided by New Relic.
        datadog_api_key - string - Applicable only for destination type: datadog. API key provided by Datadog.
        action_send_enabled - boolean - Whether or not sending is enabled for action logs.
        sftp_action_send_enabled - boolean - Whether or not sending is enabled for sftp_action logs.
        ftp_action_send_enabled - boolean - Whether or not sending is enabled for ftp_action logs.
        web_dav_action_send_enabled - boolean - Whether or not sending is enabled for web_dav_action logs.
        sync_send_enabled - boolean - Whether or not sending is enabled for sync logs.
        outbound_connection_send_enabled - boolean - Whether or not sending is enabled for outbound_connection logs.
        automation_send_enabled - boolean - Whether or not sending is enabled for automation logs.
        api_request_send_enabled - boolean - Whether or not sending is enabled for api_request logs.
        public_hosting_request_send_enabled - boolean - Whether or not sending is enabled for public_hosting_request logs.
        email_send_enabled - boolean - Whether or not sending is enabled for email logs.
        exavault_api_request_send_enabled - boolean - Whether or not sending is enabled for exavault_api_request logs.
        settings_change_send_enabled - boolean - Whether or not sending is enabled for settings_change logs.
        """
        params = copy_params(params)
        if "siem_http_destination_id" in params and (
            not isinstance(params["siem_http_destination_id"], int)
            or isinstance(params["siem_http_destination_id"], bool)
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
        if "sending_active" in params and not isinstance(
            params["sending_active"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sending_active must be an bool"
            )
        if "generic_payload_type" in params and not isinstance(
            params["generic_payload_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: generic_payload_type must be an str"
            )
        if "file_destination_path" in params and not isinstance(
            params["file_destination_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: file_destination_path must be an str"
            )
        if "file_format" in params and not isinstance(
            params["file_format"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: file_format must be an str"
            )
        if "file_interval_minutes" in params and (
            not isinstance(params["file_interval_minutes"], int)
            or isinstance(params["file_interval_minutes"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: file_interval_minutes must be an int"
            )
        if "splunk_token" in params and not isinstance(
            params["splunk_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: splunk_token must be an str"
            )
        if "crowdstrike_token" in params and not isinstance(
            params["crowdstrike_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: crowdstrike_token must be an str"
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
        if "action_send_enabled" in params and not isinstance(
            params["action_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: action_send_enabled must be an bool"
            )
        if "sftp_action_send_enabled" in params and not isinstance(
            params["sftp_action_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sftp_action_send_enabled must be an bool"
            )
        if "ftp_action_send_enabled" in params and not isinstance(
            params["ftp_action_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: ftp_action_send_enabled must be an bool"
            )
        if "web_dav_action_send_enabled" in params and not isinstance(
            params["web_dav_action_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: web_dav_action_send_enabled must be an bool"
            )
        if "sync_send_enabled" in params and not isinstance(
            params["sync_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sync_send_enabled must be an bool"
            )
        if "outbound_connection_send_enabled" in params and not isinstance(
            params["outbound_connection_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: outbound_connection_send_enabled must be an bool"
            )
        if "automation_send_enabled" in params and not isinstance(
            params["automation_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: automation_send_enabled must be an bool"
            )
        if "api_request_send_enabled" in params and not isinstance(
            params["api_request_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: api_request_send_enabled must be an bool"
            )
        if "public_hosting_request_send_enabled" in params and not isinstance(
            params["public_hosting_request_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: public_hosting_request_send_enabled must be an bool"
            )
        if "email_send_enabled" in params and not isinstance(
            params["email_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: email_send_enabled must be an bool"
            )
        if "exavault_api_request_send_enabled" in params and not isinstance(
            params["exavault_api_request_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: exavault_api_request_send_enabled must be an bool"
            )
        if "settings_change_send_enabled" in params and not isinstance(
            params["settings_change_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: settings_change_send_enabled must be an bool"
            )
        operation = Operation.start(self._scope, options)
        operation.request(
            "POST", "/siem_http_destinations/send_test_entry", params
        )

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SiemHttpDestination:
        """Parameters:
        name - string - Name for this Destination
        additional_headers - object - Additional HTTP Headers included in calls to the destination URL
        sending_active - boolean - Whether this SIEM HTTP Destination is currently being sent to or not
        generic_payload_type - string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
        file_destination_path - string - Applicable only for destination type: file. Destination folder path on Files.com.
        file_format - string - Applicable only for destination type: file. Generated file format.
        file_interval_minutes - int64 - Applicable only for destination type: file. Interval, in minutes, between file deliveries. Valid values are 5, 10, 15, 20, 30, 60, 90, 180, 240, 360.
        splunk_token - string - Applicable only for destination types: splunk, splunk_compatible. Authentication token for the destination.
        crowdstrike_token - string - Applicable only for destination type: crowdstrike. Authentication token provided by Crowdstrike.
        azure_dcr_immutable_id - string - Applicable only for destination types: azure, azure_legacy. Immutable ID of the Data Collection Rule.
        azure_stream_name - string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
        azure_oauth_client_credentials_tenant_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Tenant ID.
        azure_oauth_client_credentials_client_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Client ID.
        azure_oauth_client_credentials_client_secret - string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
        qradar_username - string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
        qradar_password - string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
        solar_winds_token - string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
        new_relic_api_key - string - Applicable only for destination type: new_relic. API key provided by New Relic.
        datadog_api_key - string - Applicable only for destination type: datadog. API key provided by Datadog.
        action_send_enabled - boolean - Whether or not sending is enabled for action logs.
        sftp_action_send_enabled - boolean - Whether or not sending is enabled for sftp_action logs.
        ftp_action_send_enabled - boolean - Whether or not sending is enabled for ftp_action logs.
        web_dav_action_send_enabled - boolean - Whether or not sending is enabled for web_dav_action logs.
        sync_send_enabled - boolean - Whether or not sending is enabled for sync logs.
        outbound_connection_send_enabled - boolean - Whether or not sending is enabled for outbound_connection logs.
        automation_send_enabled - boolean - Whether or not sending is enabled for automation logs.
        api_request_send_enabled - boolean - Whether or not sending is enabled for api_request logs.
        public_hosting_request_send_enabled - boolean - Whether or not sending is enabled for public_hosting_request logs.
        email_send_enabled - boolean - Whether or not sending is enabled for email logs.
        exavault_api_request_send_enabled - boolean - Whether or not sending is enabled for exavault_api_request logs.
        settings_change_send_enabled - boolean - Whether or not sending is enabled for settings_change logs.
        destination_type - string - Destination Type
        destination_url - string - Destination Url
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> SiemHttpDestination:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "additional_headers" in params and not isinstance(
            params["additional_headers"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: additional_headers must be an dict"
            )
        if "sending_active" in params and not isinstance(
            params["sending_active"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sending_active must be an bool"
            )
        if "generic_payload_type" in params and not isinstance(
            params["generic_payload_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: generic_payload_type must be an str"
            )
        if "file_destination_path" in params and not isinstance(
            params["file_destination_path"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: file_destination_path must be an str"
            )
        if "file_format" in params and not isinstance(
            params["file_format"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: file_format must be an str"
            )
        if "file_interval_minutes" in params and (
            not isinstance(params["file_interval_minutes"], int)
            or isinstance(params["file_interval_minutes"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: file_interval_minutes must be an int"
            )
        if "splunk_token" in params and not isinstance(
            params["splunk_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: splunk_token must be an str"
            )
        if "crowdstrike_token" in params and not isinstance(
            params["crowdstrike_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: crowdstrike_token must be an str"
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
        if "action_send_enabled" in params and not isinstance(
            params["action_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: action_send_enabled must be an bool"
            )
        if "sftp_action_send_enabled" in params and not isinstance(
            params["sftp_action_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sftp_action_send_enabled must be an bool"
            )
        if "ftp_action_send_enabled" in params and not isinstance(
            params["ftp_action_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: ftp_action_send_enabled must be an bool"
            )
        if "web_dav_action_send_enabled" in params and not isinstance(
            params["web_dav_action_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: web_dav_action_send_enabled must be an bool"
            )
        if "sync_send_enabled" in params and not isinstance(
            params["sync_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sync_send_enabled must be an bool"
            )
        if "outbound_connection_send_enabled" in params and not isinstance(
            params["outbound_connection_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: outbound_connection_send_enabled must be an bool"
            )
        if "automation_send_enabled" in params and not isinstance(
            params["automation_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: automation_send_enabled must be an bool"
            )
        if "api_request_send_enabled" in params and not isinstance(
            params["api_request_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: api_request_send_enabled must be an bool"
            )
        if "public_hosting_request_send_enabled" in params and not isinstance(
            params["public_hosting_request_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: public_hosting_request_send_enabled must be an bool"
            )
        if "email_send_enabled" in params and not isinstance(
            params["email_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: email_send_enabled must be an bool"
            )
        if "exavault_api_request_send_enabled" in params and not isinstance(
            params["exavault_api_request_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: exavault_api_request_send_enabled must be an bool"
            )
        if "settings_change_send_enabled" in params and not isinstance(
            params["settings_change_send_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: settings_change_send_enabled must be an bool"
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
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH",
            "/siem_http_destinations/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, SiemHttpDestination)

    def delete(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        return self.__delete({"id": id}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE",
            "/siem_http_destinations/" + path_value(params["id"]),
            params,
        )

    def destroy(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SiemHttpDestination:
        """A new SiemHttpDestination with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = SiemHttpDestination(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = SiemHttpDestinationResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SiemHttpDestination]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SiemHttpDestination]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SiemHttpDestination:
    """Parameters:
    id (required) - int64 - Siem Http Destination ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SiemHttpDestination:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SiemHttpDestination:
    """Parameters:
    name - string - Name for this Destination
    additional_headers - object - Additional HTTP Headers included in calls to the destination URL
    sending_active - boolean - Whether this SIEM HTTP Destination is currently being sent to or not
    generic_payload_type - string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
    file_destination_path - string - Applicable only for destination type: file. Destination folder path on Files.com.
    file_format - string - Applicable only for destination type: file. Generated file format.
    file_interval_minutes - int64 - Applicable only for destination type: file. Interval, in minutes, between file deliveries. Valid values are 5, 10, 15, 20, 30, 60, 90, 180, 240, 360.
    splunk_token - string - Applicable only for destination types: splunk, splunk_compatible. Authentication token for the destination.
    crowdstrike_token - string - Applicable only for destination type: crowdstrike. Authentication token provided by Crowdstrike.
    azure_dcr_immutable_id - string - Applicable only for destination types: azure, azure_legacy. Immutable ID of the Data Collection Rule.
    azure_stream_name - string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
    azure_oauth_client_credentials_tenant_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Tenant ID.
    azure_oauth_client_credentials_client_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Client ID.
    azure_oauth_client_credentials_client_secret - string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
    qradar_username - string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
    qradar_password - string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
    solar_winds_token - string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
    new_relic_api_key - string - Applicable only for destination type: new_relic. API key provided by New Relic.
    datadog_api_key - string - Applicable only for destination type: datadog. API key provided by Datadog.
    action_send_enabled - boolean - Whether or not sending is enabled for action logs.
    sftp_action_send_enabled - boolean - Whether or not sending is enabled for sftp_action logs.
    ftp_action_send_enabled - boolean - Whether or not sending is enabled for ftp_action logs.
    web_dav_action_send_enabled - boolean - Whether or not sending is enabled for web_dav_action logs.
    sync_send_enabled - boolean - Whether or not sending is enabled for sync logs.
    outbound_connection_send_enabled - boolean - Whether or not sending is enabled for outbound_connection logs.
    automation_send_enabled - boolean - Whether or not sending is enabled for automation logs.
    api_request_send_enabled - boolean - Whether or not sending is enabled for api_request logs.
    public_hosting_request_send_enabled - boolean - Whether or not sending is enabled for public_hosting_request logs.
    email_send_enabled - boolean - Whether or not sending is enabled for email logs.
    exavault_api_request_send_enabled - boolean - Whether or not sending is enabled for exavault_api_request logs.
    settings_change_send_enabled - boolean - Whether or not sending is enabled for settings_change logs.
    destination_type (required) - string - Destination Type
    destination_url - string - Destination Url
    """
    return _legacy_resource.create(params, options)


def send_test_entry(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Parameters:
    siem_http_destination_id - int64 - SIEM HTTP Destination ID
    destination_type - string - Destination Type
    destination_url - string - Destination Url
    name - string - Name for this Destination
    additional_headers - object - Additional HTTP Headers included in calls to the destination URL
    sending_active - boolean - Whether this SIEM HTTP Destination is currently being sent to or not
    generic_payload_type - string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
    file_destination_path - string - Applicable only for destination type: file. Destination folder path on Files.com.
    file_format - string - Applicable only for destination type: file. Generated file format.
    file_interval_minutes - int64 - Applicable only for destination type: file. Interval, in minutes, between file deliveries. Valid values are 5, 10, 15, 20, 30, 60, 90, 180, 240, 360.
    splunk_token - string - Applicable only for destination types: splunk, splunk_compatible. Authentication token for the destination.
    crowdstrike_token - string - Applicable only for destination type: crowdstrike. Authentication token provided by Crowdstrike.
    azure_dcr_immutable_id - string - Applicable only for destination types: azure, azure_legacy. Immutable ID of the Data Collection Rule.
    azure_stream_name - string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
    azure_oauth_client_credentials_tenant_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Tenant ID.
    azure_oauth_client_credentials_client_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Client ID.
    azure_oauth_client_credentials_client_secret - string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
    qradar_username - string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
    qradar_password - string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
    solar_winds_token - string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
    new_relic_api_key - string - Applicable only for destination type: new_relic. API key provided by New Relic.
    datadog_api_key - string - Applicable only for destination type: datadog. API key provided by Datadog.
    action_send_enabled - boolean - Whether or not sending is enabled for action logs.
    sftp_action_send_enabled - boolean - Whether or not sending is enabled for sftp_action logs.
    ftp_action_send_enabled - boolean - Whether or not sending is enabled for ftp_action logs.
    web_dav_action_send_enabled - boolean - Whether or not sending is enabled for web_dav_action logs.
    sync_send_enabled - boolean - Whether or not sending is enabled for sync logs.
    outbound_connection_send_enabled - boolean - Whether or not sending is enabled for outbound_connection logs.
    automation_send_enabled - boolean - Whether or not sending is enabled for automation logs.
    api_request_send_enabled - boolean - Whether or not sending is enabled for api_request logs.
    public_hosting_request_send_enabled - boolean - Whether or not sending is enabled for public_hosting_request logs.
    email_send_enabled - boolean - Whether or not sending is enabled for email logs.
    exavault_api_request_send_enabled - boolean - Whether or not sending is enabled for exavault_api_request logs.
    settings_change_send_enabled - boolean - Whether or not sending is enabled for settings_change logs.
    """
    _legacy_resource.send_test_entry(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SiemHttpDestination:
    """Parameters:
    name - string - Name for this Destination
    additional_headers - object - Additional HTTP Headers included in calls to the destination URL
    sending_active - boolean - Whether this SIEM HTTP Destination is currently being sent to or not
    generic_payload_type - string - Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
    file_destination_path - string - Applicable only for destination type: file. Destination folder path on Files.com.
    file_format - string - Applicable only for destination type: file. Generated file format.
    file_interval_minutes - int64 - Applicable only for destination type: file. Interval, in minutes, between file deliveries. Valid values are 5, 10, 15, 20, 30, 60, 90, 180, 240, 360.
    splunk_token - string - Applicable only for destination types: splunk, splunk_compatible. Authentication token for the destination.
    crowdstrike_token - string - Applicable only for destination type: crowdstrike. Authentication token provided by Crowdstrike.
    azure_dcr_immutable_id - string - Applicable only for destination types: azure, azure_legacy. Immutable ID of the Data Collection Rule.
    azure_stream_name - string - Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
    azure_oauth_client_credentials_tenant_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Tenant ID.
    azure_oauth_client_credentials_client_id - string - Applicable only for destination types: azure, azure_legacy. Client Credentials OAuth Client ID.
    azure_oauth_client_credentials_client_secret - string - Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
    qradar_username - string - Applicable only for destination type: qradar. Basic auth username provided by QRadar.
    qradar_password - string - Applicable only for destination type: qradar. Basic auth password provided by QRadar.
    solar_winds_token - string - Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
    new_relic_api_key - string - Applicable only for destination type: new_relic. API key provided by New Relic.
    datadog_api_key - string - Applicable only for destination type: datadog. API key provided by Datadog.
    action_send_enabled - boolean - Whether or not sending is enabled for action logs.
    sftp_action_send_enabled - boolean - Whether or not sending is enabled for sftp_action logs.
    ftp_action_send_enabled - boolean - Whether or not sending is enabled for ftp_action logs.
    web_dav_action_send_enabled - boolean - Whether or not sending is enabled for web_dav_action logs.
    sync_send_enabled - boolean - Whether or not sending is enabled for sync logs.
    outbound_connection_send_enabled - boolean - Whether or not sending is enabled for outbound_connection logs.
    automation_send_enabled - boolean - Whether or not sending is enabled for automation logs.
    api_request_send_enabled - boolean - Whether or not sending is enabled for api_request logs.
    public_hosting_request_send_enabled - boolean - Whether or not sending is enabled for public_hosting_request logs.
    email_send_enabled - boolean - Whether or not sending is enabled for email logs.
    exavault_api_request_send_enabled - boolean - Whether or not sending is enabled for exavault_api_request logs.
    settings_change_send_enabled - boolean - Whether or not sending is enabled for settings_change logs.
    destination_type - string - Destination Type
    destination_url - string - Destination Url
    """
    return _legacy_resource.update(id, params, options)


def delete(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    _legacy_resource.delete(id, params, options)


def destroy(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(id, params, options)


def new(*args, **kwargs) -> SiemHttpDestination:
    return SiemHttpDestination(*args, **kwargs)
