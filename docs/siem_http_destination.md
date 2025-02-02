# SiemHttpDestination

## Example SiemHttpDestination Object

```
{
  "id": 1,
  "name": "example",
  "destination_type": "example",
  "destination_url": "example",
  "additional_headers": {
    "key": "example value"
  },
  "sending_active": True,
  "generic_payload_type": "example",
  "splunk_token_masked": "example",
  "azure_dcr_immutable_id": "example",
  "azure_stream_name": "example",
  "azure_oauth_client_credentials_tenant_id": "example",
  "azure_oauth_client_credentials_client_id": "example",
  "azure_oauth_client_credentials_client_secret_masked": "example",
  "qradar_username": "example",
  "qradar_password_masked": "example",
  "solar_winds_token_masked": "example",
  "new_relic_api_key_masked": "example",
  "datadog_api_key_masked": "example",
  "sftp_action_send_enabled": True,
  "sftp_action_entries_sent": 1,
  "ftp_action_send_enabled": True,
  "ftp_action_entries_sent": 1,
  "web_dav_action_send_enabled": True,
  "web_dav_action_entries_sent": 1,
  "sync_send_enabled": True,
  "sync_entries_sent": 1,
  "outbound_connection_send_enabled": True,
  "outbound_connection_entries_sent": 1,
  "automation_send_enabled": True,
  "automation_entries_sent": 1,
  "api_request_send_enabled": True,
  "api_request_entries_sent": 1,
  "public_hosting_request_send_enabled": True,
  "public_hosting_request_entries_sent": 1,
  "email_send_enabled": True,
  "email_entries_sent": 1,
  "exavault_api_request_send_enabled": True,
  "exavault_api_request_entries_sent": 1,
  "last_http_call_target_type": "destination_url",
  "last_http_call_success": True,
  "last_http_call_response_code": 1,
  "last_http_call_response_body": "example",
  "last_http_call_error_message": "example",
  "last_http_call_time": "example",
  "last_http_call_duration_ms": 1,
  "most_recent_http_call_success_time": "example",
  "connection_test_entry": "example"
}
```

* `id` (int64): SIEM HTTP Destination ID
* `name` (string): Name for this Destination
* `destination_type` (string): Destination Type
* `destination_url` (string): Destination Url
* `additional_headers` (object): Additional HTTP Headers included in calls to the destination URL
* `sending_active` (boolean): Whether this SIEM HTTP Destination is currently being sent to or not
* `generic_payload_type` (string): Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
* `splunk_token_masked` (string): Applicable only for destination type: splunk. Authentication token provided by Splunk.
* `azure_dcr_immutable_id` (string): Applicable only for destination type: azure. Immutable ID of the Data Collection Rule.
* `azure_stream_name` (string): Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
* `azure_oauth_client_credentials_tenant_id` (string): Applicable only for destination type: azure. Client Credentials OAuth Tenant ID.
* `azure_oauth_client_credentials_client_id` (string): Applicable only for destination type: azure. Client Credentials OAuth Client ID.
* `azure_oauth_client_credentials_client_secret_masked` (string): Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
* `qradar_username` (string): Applicable only for destination type: qradar. Basic auth username provided by QRadar.
* `qradar_password_masked` (string): Applicable only for destination type: qradar. Basic auth password provided by QRadar.
* `solar_winds_token_masked` (string): Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
* `new_relic_api_key_masked` (string): Applicable only for destination type: new_relic. API key provided by New Relic.
* `datadog_api_key_masked` (string): Applicable only for destination type: datadog. API key provided by Datadog.
* `sftp_action_send_enabled` (boolean): Whether or not sending is enabled for sftp_action logs.
* `sftp_action_entries_sent` (int64): Number of log entries sent for the lifetime of this destination.
* `ftp_action_send_enabled` (boolean): Whether or not sending is enabled for ftp_action logs.
* `ftp_action_entries_sent` (int64): Number of log entries sent for the lifetime of this destination.
* `web_dav_action_send_enabled` (boolean): Whether or not sending is enabled for web_dav_action logs.
* `web_dav_action_entries_sent` (int64): Number of log entries sent for the lifetime of this destination.
* `sync_send_enabled` (boolean): Whether or not sending is enabled for sync logs.
* `sync_entries_sent` (int64): Number of log entries sent for the lifetime of this destination.
* `outbound_connection_send_enabled` (boolean): Whether or not sending is enabled for outbound_connection logs.
* `outbound_connection_entries_sent` (int64): Number of log entries sent for the lifetime of this destination.
* `automation_send_enabled` (boolean): Whether or not sending is enabled for automation logs.
* `automation_entries_sent` (int64): Number of log entries sent for the lifetime of this destination.
* `api_request_send_enabled` (boolean): Whether or not sending is enabled for api_request logs.
* `api_request_entries_sent` (int64): Number of log entries sent for the lifetime of this destination.
* `public_hosting_request_send_enabled` (boolean): Whether or not sending is enabled for public_hosting_request logs.
* `public_hosting_request_entries_sent` (int64): Number of log entries sent for the lifetime of this destination.
* `email_send_enabled` (boolean): Whether or not sending is enabled for email logs.
* `email_entries_sent` (int64): Number of log entries sent for the lifetime of this destination.
* `exavault_api_request_send_enabled` (boolean): Whether or not sending is enabled for exavault_api_request logs.
* `exavault_api_request_entries_sent` (int64): Number of log entries sent for the lifetime of this destination.
* `last_http_call_target_type` (string): Type of URL that was last called. Can be `destination_url` or `azure_oauth_client_credentials_url`
* `last_http_call_success` (boolean): Was the last HTTP call made successful?
* `last_http_call_response_code` (int64): Last HTTP Call Response Code
* `last_http_call_response_body` (string): Last HTTP Call Response Body. Large responses are truncated.
* `last_http_call_error_message` (string): Last HTTP Call Error Message if applicable
* `last_http_call_time` (string): Time of Last HTTP Call
* `last_http_call_duration_ms` (int64): Duration of the last HTTP Call in milliseconds
* `most_recent_http_call_success_time` (string): Time of Most Recent Successful HTTP Call
* `connection_test_entry` (string): Connection Test Entry
* `splunk_token` (string): Applicable only for destination type: splunk. Authentication token provided by Splunk.
* `azure_oauth_client_credentials_client_secret` (string): Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
* `qradar_password` (string): Applicable only for destination type: qradar. Basic auth password provided by QRadar.
* `solar_winds_token` (string): Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
* `new_relic_api_key` (string): Applicable only for destination type: new_relic. API key provided by New Relic.
* `datadog_api_key` (string): Applicable only for destination type: datadog. API key provided by Datadog.


---

## List SIEM HTTP Destinations

```
files_sdk.siem_http_destination.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show SIEM HTTP Destination

```
files_sdk.siem_http_destination.find(id)
```

### Parameters

* `id` (int64): Required - Siem Http Destination ID.


---

## Create SIEM HTTP Destination

```
files_sdk.siem_http_destination.create({
  "name": "example",
  "additional_headers": {"key":"example value"},
  "sending_active": True,
  "generic_payload_type": "example",
  "azure_dcr_immutable_id": "example",
  "azure_stream_name": "example",
  "azure_oauth_client_credentials_tenant_id": "example",
  "azure_oauth_client_credentials_client_id": "example",
  "qradar_username": "example",
  "sftp_action_send_enabled": True,
  "ftp_action_send_enabled": True,
  "web_dav_action_send_enabled": True,
  "sync_send_enabled": True,
  "outbound_connection_send_enabled": True,
  "automation_send_enabled": True,
  "api_request_send_enabled": True,
  "public_hosting_request_send_enabled": True,
  "email_send_enabled": True,
  "exavault_api_request_send_enabled": True,
  "destination_type": "example",
  "destination_url": "example"
})
```

### Parameters

* `name` (string): Name for this Destination
* `additional_headers` (object): Additional HTTP Headers included in calls to the destination URL
* `sending_active` (boolean): Whether this SIEM HTTP Destination is currently being sent to or not
* `generic_payload_type` (string): Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
* `splunk_token` (string): Applicable only for destination type: splunk. Authentication token provided by Splunk.
* `azure_dcr_immutable_id` (string): Applicable only for destination type: azure. Immutable ID of the Data Collection Rule.
* `azure_stream_name` (string): Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
* `azure_oauth_client_credentials_tenant_id` (string): Applicable only for destination type: azure. Client Credentials OAuth Tenant ID.
* `azure_oauth_client_credentials_client_id` (string): Applicable only for destination type: azure. Client Credentials OAuth Client ID.
* `azure_oauth_client_credentials_client_secret` (string): Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
* `qradar_username` (string): Applicable only for destination type: qradar. Basic auth username provided by QRadar.
* `qradar_password` (string): Applicable only for destination type: qradar. Basic auth password provided by QRadar.
* `solar_winds_token` (string): Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
* `new_relic_api_key` (string): Applicable only for destination type: new_relic. API key provided by New Relic.
* `datadog_api_key` (string): Applicable only for destination type: datadog. API key provided by Datadog.
* `sftp_action_send_enabled` (boolean): Whether or not sending is enabled for sftp_action logs.
* `ftp_action_send_enabled` (boolean): Whether or not sending is enabled for ftp_action logs.
* `web_dav_action_send_enabled` (boolean): Whether or not sending is enabled for web_dav_action logs.
* `sync_send_enabled` (boolean): Whether or not sending is enabled for sync logs.
* `outbound_connection_send_enabled` (boolean): Whether or not sending is enabled for outbound_connection logs.
* `automation_send_enabled` (boolean): Whether or not sending is enabled for automation logs.
* `api_request_send_enabled` (boolean): Whether or not sending is enabled for api_request logs.
* `public_hosting_request_send_enabled` (boolean): Whether or not sending is enabled for public_hosting_request logs.
* `email_send_enabled` (boolean): Whether or not sending is enabled for email logs.
* `exavault_api_request_send_enabled` (boolean): Whether or not sending is enabled for exavault_api_request logs.
* `destination_type` (string): Required - Destination Type
* `destination_url` (string): Required - Destination Url


---

## send_test_entry SIEM HTTP Destination

```
files_sdk.siem_http_destination.send_test_entry({
  "siem_http_destination_id": 1,
  "destination_type": "example",
  "destination_url": "example",
  "name": "example",
  "additional_headers": {"key":"example value"},
  "sending_active": True,
  "generic_payload_type": "example",
  "azure_dcr_immutable_id": "example",
  "azure_stream_name": "example",
  "azure_oauth_client_credentials_tenant_id": "example",
  "azure_oauth_client_credentials_client_id": "example",
  "qradar_username": "example",
  "sftp_action_send_enabled": True,
  "ftp_action_send_enabled": True,
  "web_dav_action_send_enabled": True,
  "sync_send_enabled": True,
  "outbound_connection_send_enabled": True,
  "automation_send_enabled": True,
  "api_request_send_enabled": True,
  "public_hosting_request_send_enabled": True,
  "email_send_enabled": True,
  "exavault_api_request_send_enabled": True
})
```

### Parameters

* `siem_http_destination_id` (int64): SIEM HTTP Destination ID
* `destination_type` (string): Destination Type
* `destination_url` (string): Destination Url
* `name` (string): Name for this Destination
* `additional_headers` (object): Additional HTTP Headers included in calls to the destination URL
* `sending_active` (boolean): Whether this SIEM HTTP Destination is currently being sent to or not
* `generic_payload_type` (string): Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
* `splunk_token` (string): Applicable only for destination type: splunk. Authentication token provided by Splunk.
* `azure_dcr_immutable_id` (string): Applicable only for destination type: azure. Immutable ID of the Data Collection Rule.
* `azure_stream_name` (string): Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
* `azure_oauth_client_credentials_tenant_id` (string): Applicable only for destination type: azure. Client Credentials OAuth Tenant ID.
* `azure_oauth_client_credentials_client_id` (string): Applicable only for destination type: azure. Client Credentials OAuth Client ID.
* `azure_oauth_client_credentials_client_secret` (string): Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
* `qradar_username` (string): Applicable only for destination type: qradar. Basic auth username provided by QRadar.
* `qradar_password` (string): Applicable only for destination type: qradar. Basic auth password provided by QRadar.
* `solar_winds_token` (string): Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
* `new_relic_api_key` (string): Applicable only for destination type: new_relic. API key provided by New Relic.
* `datadog_api_key` (string): Applicable only for destination type: datadog. API key provided by Datadog.
* `sftp_action_send_enabled` (boolean): Whether or not sending is enabled for sftp_action logs.
* `ftp_action_send_enabled` (boolean): Whether or not sending is enabled for ftp_action logs.
* `web_dav_action_send_enabled` (boolean): Whether or not sending is enabled for web_dav_action logs.
* `sync_send_enabled` (boolean): Whether or not sending is enabled for sync logs.
* `outbound_connection_send_enabled` (boolean): Whether or not sending is enabled for outbound_connection logs.
* `automation_send_enabled` (boolean): Whether or not sending is enabled for automation logs.
* `api_request_send_enabled` (boolean): Whether or not sending is enabled for api_request logs.
* `public_hosting_request_send_enabled` (boolean): Whether or not sending is enabled for public_hosting_request logs.
* `email_send_enabled` (boolean): Whether or not sending is enabled for email logs.
* `exavault_api_request_send_enabled` (boolean): Whether or not sending is enabled for exavault_api_request logs.


---

## Update SIEM HTTP Destination

```
files_sdk.siem_http_destination.update(id, {
  "name": "example",
  "additional_headers": {"key":"example value"},
  "sending_active": True,
  "generic_payload_type": "example",
  "azure_dcr_immutable_id": "example",
  "azure_stream_name": "example",
  "azure_oauth_client_credentials_tenant_id": "example",
  "azure_oauth_client_credentials_client_id": "example",
  "qradar_username": "example",
  "sftp_action_send_enabled": True,
  "ftp_action_send_enabled": True,
  "web_dav_action_send_enabled": True,
  "sync_send_enabled": True,
  "outbound_connection_send_enabled": True,
  "automation_send_enabled": True,
  "api_request_send_enabled": True,
  "public_hosting_request_send_enabled": True,
  "email_send_enabled": True,
  "exavault_api_request_send_enabled": True,
  "destination_type": "example",
  "destination_url": "example"
})
```

### Parameters

* `id` (int64): Required - Siem Http Destination ID.
* `name` (string): Name for this Destination
* `additional_headers` (object): Additional HTTP Headers included in calls to the destination URL
* `sending_active` (boolean): Whether this SIEM HTTP Destination is currently being sent to or not
* `generic_payload_type` (string): Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
* `splunk_token` (string): Applicable only for destination type: splunk. Authentication token provided by Splunk.
* `azure_dcr_immutable_id` (string): Applicable only for destination type: azure. Immutable ID of the Data Collection Rule.
* `azure_stream_name` (string): Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
* `azure_oauth_client_credentials_tenant_id` (string): Applicable only for destination type: azure. Client Credentials OAuth Tenant ID.
* `azure_oauth_client_credentials_client_id` (string): Applicable only for destination type: azure. Client Credentials OAuth Client ID.
* `azure_oauth_client_credentials_client_secret` (string): Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
* `qradar_username` (string): Applicable only for destination type: qradar. Basic auth username provided by QRadar.
* `qradar_password` (string): Applicable only for destination type: qradar. Basic auth password provided by QRadar.
* `solar_winds_token` (string): Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
* `new_relic_api_key` (string): Applicable only for destination type: new_relic. API key provided by New Relic.
* `datadog_api_key` (string): Applicable only for destination type: datadog. API key provided by Datadog.
* `sftp_action_send_enabled` (boolean): Whether or not sending is enabled for sftp_action logs.
* `ftp_action_send_enabled` (boolean): Whether or not sending is enabled for ftp_action logs.
* `web_dav_action_send_enabled` (boolean): Whether or not sending is enabled for web_dav_action logs.
* `sync_send_enabled` (boolean): Whether or not sending is enabled for sync logs.
* `outbound_connection_send_enabled` (boolean): Whether or not sending is enabled for outbound_connection logs.
* `automation_send_enabled` (boolean): Whether or not sending is enabled for automation logs.
* `api_request_send_enabled` (boolean): Whether or not sending is enabled for api_request logs.
* `public_hosting_request_send_enabled` (boolean): Whether or not sending is enabled for public_hosting_request logs.
* `email_send_enabled` (boolean): Whether or not sending is enabled for email logs.
* `exavault_api_request_send_enabled` (boolean): Whether or not sending is enabled for exavault_api_request logs.
* `destination_type` (string): Destination Type
* `destination_url` (string): Destination Url


---

## Delete SIEM HTTP Destination

```
files_sdk.siem_http_destination.delete(id)
```

### Parameters

* `id` (int64): Required - Siem Http Destination ID.


---

## Update SIEM HTTP Destination

```
siem_http_destination = files_sdk.siem_http_destination.find(id)
siem_http_destination.update({
  "name": "example",
  "additional_headers": {"key":"example value"},
  "sending_active": True,
  "generic_payload_type": "example",
  "azure_dcr_immutable_id": "example",
  "azure_stream_name": "example",
  "azure_oauth_client_credentials_tenant_id": "example",
  "azure_oauth_client_credentials_client_id": "example",
  "qradar_username": "example",
  "sftp_action_send_enabled": True,
  "ftp_action_send_enabled": True,
  "web_dav_action_send_enabled": True,
  "sync_send_enabled": True,
  "outbound_connection_send_enabled": True,
  "automation_send_enabled": True,
  "api_request_send_enabled": True,
  "public_hosting_request_send_enabled": True,
  "email_send_enabled": True,
  "exavault_api_request_send_enabled": True,
  "destination_type": "example",
  "destination_url": "example"
})
```

### Parameters

* `id` (int64): Required - Siem Http Destination ID.
* `name` (string): Name for this Destination
* `additional_headers` (object): Additional HTTP Headers included in calls to the destination URL
* `sending_active` (boolean): Whether this SIEM HTTP Destination is currently being sent to or not
* `generic_payload_type` (string): Applicable only for destination type: generic. Indicates the type of HTTP body. Can be json_newline or json_array. json_newline is multiple log entries as JSON separated by newlines. json_array is a single JSON array containing multiple log entries as JSON.
* `splunk_token` (string): Applicable only for destination type: splunk. Authentication token provided by Splunk.
* `azure_dcr_immutable_id` (string): Applicable only for destination type: azure. Immutable ID of the Data Collection Rule.
* `azure_stream_name` (string): Applicable only for destination type: azure. Name of the stream in the DCR that represents the destination table.
* `azure_oauth_client_credentials_tenant_id` (string): Applicable only for destination type: azure. Client Credentials OAuth Tenant ID.
* `azure_oauth_client_credentials_client_id` (string): Applicable only for destination type: azure. Client Credentials OAuth Client ID.
* `azure_oauth_client_credentials_client_secret` (string): Applicable only for destination type: azure. Client Credentials OAuth Client Secret.
* `qradar_username` (string): Applicable only for destination type: qradar. Basic auth username provided by QRadar.
* `qradar_password` (string): Applicable only for destination type: qradar. Basic auth password provided by QRadar.
* `solar_winds_token` (string): Applicable only for destination type: solar_winds. Authentication token provided by Solar Winds.
* `new_relic_api_key` (string): Applicable only for destination type: new_relic. API key provided by New Relic.
* `datadog_api_key` (string): Applicable only for destination type: datadog. API key provided by Datadog.
* `sftp_action_send_enabled` (boolean): Whether or not sending is enabled for sftp_action logs.
* `ftp_action_send_enabled` (boolean): Whether or not sending is enabled for ftp_action logs.
* `web_dav_action_send_enabled` (boolean): Whether or not sending is enabled for web_dav_action logs.
* `sync_send_enabled` (boolean): Whether or not sending is enabled for sync logs.
* `outbound_connection_send_enabled` (boolean): Whether or not sending is enabled for outbound_connection logs.
* `automation_send_enabled` (boolean): Whether or not sending is enabled for automation logs.
* `api_request_send_enabled` (boolean): Whether or not sending is enabled for api_request logs.
* `public_hosting_request_send_enabled` (boolean): Whether or not sending is enabled for public_hosting_request logs.
* `email_send_enabled` (boolean): Whether or not sending is enabled for email logs.
* `exavault_api_request_send_enabled` (boolean): Whether or not sending is enabled for exavault_api_request logs.
* `destination_type` (string): Destination Type
* `destination_url` (string): Destination Url


---

## Delete SIEM HTTP Destination

```
siem_http_destination = files_sdk.siem_http_destination.find(id)
siem_http_destination.delete()
```

### Parameters

* `id` (int64): Required - Siem Http Destination ID.
