# RemoteServer

## Example RemoteServer Object

```
{
  "id": 1,
  "disabled": True,
  "authentication_method": "password",
  "hostname": "remote-server.com",
  "remote_home_path": "/home/user1",
  "name": "My Remote server",
  "port": 1,
  "max_connections": 1,
  "s3_bucket": "my-bucket",
  "s3_region": "us-east-1",
  "aws_access_key": "",
  "server_certificate": "require_match",
  "server_host_key": "[public key]",
  "server_type": "s3",
  "ssl": "if_available",
  "username": "user",
  "google_cloud_storage_bucket": "my-bucket",
  "google_cloud_storage_project_id": "my-project",
  "backblaze_b2_s3_endpoint": "s3.us-west-001.backblazeb2.com",
  "backblaze_b2_bucket": "my-bucket",
  "wasabi_bucket": "my-bucket",
  "wasabi_region": "us-west-1",
  "wasabi_access_key": "",
  "rackspace_username": "rackspaceuser",
  "rackspace_region": "dfw",
  "rackspace_container": "my-container",
  "auth_setup_link": "auth/:provider",
  "auth_status": "in_setup",
  "auth_account_name": "me@example.com",
  "one_drive_account_type": "personal",
  "azure_blob_storage_account": "storage-account-name",
  "azure_blob_storage_container": "container-name",
  "s3_compatible_bucket": "my-bucket",
  "s3_compatible_endpoint": "mys3platform.com",
  "s3_compatible_region": "us-east-1",
  "s3_compatible_access_key": "",
  "enable_dedicated_ips": True
}
```

* `id` (int64): Remote server ID
* `disabled` (boolean): If true, this server has been disabled due to failures.  Make any change or set disabled to false to clear this flag.
* `authentication_method` (string): Type of authentication method
* `hostname` (string): Hostname or IP address
* `remote_home_path` (string): Initial home folder on remote server
* `name` (string): Internal name for your reference
* `port` (int64): Port for remote server.  Not needed for S3.
* `max_connections` (int64): Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
* `s3_bucket` (string): S3 bucket name
* `s3_region` (string): S3 region
* `aws_access_key` (string): AWS Access Key.
* `server_certificate` (string): Remote server certificate
* `server_host_key` (string): Remote server SSH Host Key. If provided, we will require that the server host key matches the provided key. Uses OpenSSH format similar to what would go into ~/.ssh/known_hosts
* `server_type` (string): Remote server type.
* `ssl` (string): Should we require SSL?
* `username` (string): Remote server username.  Not needed for S3 buckets.
* `google_cloud_storage_bucket` (string): Google Cloud Storage bucket name
* `google_cloud_storage_project_id` (string): Google Cloud Project ID
* `backblaze_b2_s3_endpoint` (string): Backblaze B2 Cloud Storage S3 Endpoint
* `backblaze_b2_bucket` (string): Backblaze B2 Cloud Storage Bucket name
* `wasabi_bucket` (string): Wasabi Bucket name
* `wasabi_region` (string): Wasabi region
* `wasabi_access_key` (string): Wasabi access key.
* `rackspace_username` (string): Rackspace username used to login to the Rackspace Cloud Control Panel.
* `rackspace_region` (string): Three letter airport code for Rackspace region. See https://support.rackspace.com/how-to/about-regions/
* `rackspace_container` (string): The name of the container (top level directory) where files will sync.
* `auth_setup_link` (string): Returns link to login with an Oauth provider
* `auth_status` (string): Either `in_setup` or `complete`
* `auth_account_name` (string): Describes the authorized account
* `one_drive_account_type` (string): Either personal or business_other account types
* `azure_blob_storage_account` (string): Azure Blob Storage Account name
* `azure_blob_storage_container` (string): Azure Blob Storage Container name
* `s3_compatible_bucket` (string): S3-compatible Bucket name
* `s3_compatible_endpoint` (string): S3-compatible endpoint
* `s3_compatible_region` (string): S3-compatible endpoint
* `s3_compatible_access_key` (string): S3-compatible Access Key.
* `enable_dedicated_ips` (boolean): `true` if remote server only accepts connections from dedicated IPs
* `aws_secret_key` (string): AWS secret key.
* `password` (string): Password if needed.
* `private_key` (string): Private key if needed.
* `ssl_certificate` (string): SSL client certificate.
* `google_cloud_storage_credentials_json` (string): A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
* `wasabi_secret_key` (string): Wasabi secret key.
* `backblaze_b2_key_id` (string): Backblaze B2 Cloud Storage keyID.
* `backblaze_b2_application_key` (string): Backblaze B2 Cloud Storage applicationKey.
* `rackspace_api_key` (string): Rackspace API key from the Rackspace Cloud Control Panel.
* `reset_authentication` (boolean): Reset authenticated account
* `azure_blob_storage_access_key` (string): Azure Blob Storage secret key.
* `s3_compatible_secret_key` (string): S3-compatible secret key


---

## List Remote Servers

```
files_sdk.remote_server.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show Remote Server

```
files_sdk.remote_server.find(id)
```

### Parameters

* `id` (int64): Required - Remote Server ID.


---

## Create Remote Server

```
files_sdk.remote_server.create({
  "reset_authentication": True,
  "hostname": "remote-server.com",
  "name": "My Remote server",
  "max_connections": 1,
  "port": 1,
  "s3_bucket": "my-bucket",
  "s3_region": "us-east-1",
  "server_certificate": "require_match",
  "server_host_key": "[public key]",
  "server_type": "s3",
  "ssl": "if_available",
  "username": "user",
  "google_cloud_storage_bucket": "my-bucket",
  "google_cloud_storage_project_id": "my-project",
  "backblaze_b2_bucket": "my-bucket",
  "backblaze_b2_s3_endpoint": "s3.us-west-001.backblazeb2.com",
  "wasabi_bucket": "my-bucket",
  "wasabi_region": "us-west-1",
  "rackspace_username": "rackspaceuser",
  "rackspace_region": "dfw",
  "rackspace_container": "my-container",
  "one_drive_account_type": "personal",
  "azure_blob_storage_account": "storage-account-name",
  "azure_blob_storage_container": "container-name",
  "s3_compatible_bucket": "my-bucket",
  "s3_compatible_endpoint": "mys3platform.com",
  "s3_compatible_region": "us-east-1",
  "enable_dedicated_ips": True
})
```

### Parameters

* `aws_access_key` (string): AWS Access Key.
* `aws_secret_key` (string): AWS secret key.
* `password` (string): Password if needed.
* `private_key` (string): Private key if needed.
* `ssl_certificate` (string): SSL client certificate.
* `google_cloud_storage_credentials_json` (string): A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
* `wasabi_access_key` (string): Wasabi access key.
* `wasabi_secret_key` (string): Wasabi secret key.
* `backblaze_b2_key_id` (string): Backblaze B2 Cloud Storage keyID.
* `backblaze_b2_application_key` (string): Backblaze B2 Cloud Storage applicationKey.
* `rackspace_api_key` (string): Rackspace API key from the Rackspace Cloud Control Panel.
* `reset_authentication` (boolean): Reset authenticated account
* `azure_blob_storage_access_key` (string): Azure Blob Storage secret key.
* `hostname` (string): Hostname or IP address
* `name` (string): Internal name for your reference
* `max_connections` (int64): Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
* `port` (int64): Port for remote server.  Not needed for S3.
* `s3_bucket` (string): S3 bucket name
* `s3_region` (string): S3 region
* `server_certificate` (string): Remote server certificate
* `server_host_key` (string): Remote server SSH Host Key. If provided, we will require that the server host key matches the provided key. Uses OpenSSH format similar to what would go into ~/.ssh/known_hosts
* `server_type` (string): Remote server type.
* `ssl` (string): Should we require SSL?
* `username` (string): Remote server username.  Not needed for S3 buckets.
* `google_cloud_storage_bucket` (string): Google Cloud Storage bucket name
* `google_cloud_storage_project_id` (string): Google Cloud Project ID
* `backblaze_b2_bucket` (string): Backblaze B2 Cloud Storage Bucket name
* `backblaze_b2_s3_endpoint` (string): Backblaze B2 Cloud Storage S3 Endpoint
* `wasabi_bucket` (string): Wasabi Bucket name
* `wasabi_region` (string): Wasabi region
* `rackspace_username` (string): Rackspace username used to login to the Rackspace Cloud Control Panel.
* `rackspace_region` (string): Three letter airport code for Rackspace region. See https://support.rackspace.com/how-to/about-regions/
* `rackspace_container` (string): The name of the container (top level directory) where files will sync.
* `one_drive_account_type` (string): Either personal or business_other account types
* `azure_blob_storage_account` (string): Azure Blob Storage Account name
* `azure_blob_storage_container` (string): Azure Blob Storage Container name
* `s3_compatible_bucket` (string): S3-compatible Bucket name
* `s3_compatible_endpoint` (string): S3-compatible endpoint
* `s3_compatible_region` (string): S3-compatible endpoint
* `enable_dedicated_ips` (boolean): `true` if remote server only accepts connections from dedicated IPs
* `s3_compatible_access_key` (string): S3-compatible Access Key.
* `s3_compatible_secret_key` (string): S3-compatible secret key


---

## Update Remote Server

```
files_sdk.remote_server.update(id, {
  "reset_authentication": True,
  "hostname": "remote-server.com",
  "name": "My Remote server",
  "max_connections": 1,
  "port": 1,
  "s3_bucket": "my-bucket",
  "s3_region": "us-east-1",
  "server_certificate": "require_match",
  "server_host_key": "[public key]",
  "server_type": "s3",
  "ssl": "if_available",
  "username": "user",
  "google_cloud_storage_bucket": "my-bucket",
  "google_cloud_storage_project_id": "my-project",
  "backblaze_b2_bucket": "my-bucket",
  "backblaze_b2_s3_endpoint": "s3.us-west-001.backblazeb2.com",
  "wasabi_bucket": "my-bucket",
  "wasabi_region": "us-west-1",
  "rackspace_username": "rackspaceuser",
  "rackspace_region": "dfw",
  "rackspace_container": "my-container",
  "one_drive_account_type": "personal",
  "azure_blob_storage_account": "storage-account-name",
  "azure_blob_storage_container": "container-name",
  "s3_compatible_bucket": "my-bucket",
  "s3_compatible_endpoint": "mys3platform.com",
  "s3_compatible_region": "us-east-1",
  "enable_dedicated_ips": True
})
```

### Parameters

* `id` (int64): Required - Remote Server ID.
* `aws_access_key` (string): AWS Access Key.
* `aws_secret_key` (string): AWS secret key.
* `password` (string): Password if needed.
* `private_key` (string): Private key if needed.
* `ssl_certificate` (string): SSL client certificate.
* `google_cloud_storage_credentials_json` (string): A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
* `wasabi_access_key` (string): Wasabi access key.
* `wasabi_secret_key` (string): Wasabi secret key.
* `backblaze_b2_key_id` (string): Backblaze B2 Cloud Storage keyID.
* `backblaze_b2_application_key` (string): Backblaze B2 Cloud Storage applicationKey.
* `rackspace_api_key` (string): Rackspace API key from the Rackspace Cloud Control Panel.
* `reset_authentication` (boolean): Reset authenticated account
* `azure_blob_storage_access_key` (string): Azure Blob Storage secret key.
* `hostname` (string): Hostname or IP address
* `name` (string): Internal name for your reference
* `max_connections` (int64): Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
* `port` (int64): Port for remote server.  Not needed for S3.
* `s3_bucket` (string): S3 bucket name
* `s3_region` (string): S3 region
* `server_certificate` (string): Remote server certificate
* `server_host_key` (string): Remote server SSH Host Key. If provided, we will require that the server host key matches the provided key. Uses OpenSSH format similar to what would go into ~/.ssh/known_hosts
* `server_type` (string): Remote server type.
* `ssl` (string): Should we require SSL?
* `username` (string): Remote server username.  Not needed for S3 buckets.
* `google_cloud_storage_bucket` (string): Google Cloud Storage bucket name
* `google_cloud_storage_project_id` (string): Google Cloud Project ID
* `backblaze_b2_bucket` (string): Backblaze B2 Cloud Storage Bucket name
* `backblaze_b2_s3_endpoint` (string): Backblaze B2 Cloud Storage S3 Endpoint
* `wasabi_bucket` (string): Wasabi Bucket name
* `wasabi_region` (string): Wasabi region
* `rackspace_username` (string): Rackspace username used to login to the Rackspace Cloud Control Panel.
* `rackspace_region` (string): Three letter airport code for Rackspace region. See https://support.rackspace.com/how-to/about-regions/
* `rackspace_container` (string): The name of the container (top level directory) where files will sync.
* `one_drive_account_type` (string): Either personal or business_other account types
* `azure_blob_storage_account` (string): Azure Blob Storage Account name
* `azure_blob_storage_container` (string): Azure Blob Storage Container name
* `s3_compatible_bucket` (string): S3-compatible Bucket name
* `s3_compatible_endpoint` (string): S3-compatible endpoint
* `s3_compatible_region` (string): S3-compatible endpoint
* `enable_dedicated_ips` (boolean): `true` if remote server only accepts connections from dedicated IPs
* `s3_compatible_access_key` (string): S3-compatible Access Key.
* `s3_compatible_secret_key` (string): S3-compatible secret key


---

## Delete Remote Server

```
files_sdk.remote_server.delete(id)
```

### Parameters

* `id` (int64): Required - Remote Server ID.


---

## Update Remote Server

```
remote_server = files_sdk.remote_server.list.first
remote_server.update({
  "reset_authentication": True,
  "hostname": "remote-server.com",
  "name": "My Remote server",
  "max_connections": 1,
  "port": 1,
  "s3_bucket": "my-bucket",
  "s3_region": "us-east-1",
  "server_certificate": "require_match",
  "server_host_key": "[public key]",
  "server_type": "s3",
  "ssl": "if_available",
  "username": "user",
  "google_cloud_storage_bucket": "my-bucket",
  "google_cloud_storage_project_id": "my-project",
  "backblaze_b2_bucket": "my-bucket",
  "backblaze_b2_s3_endpoint": "s3.us-west-001.backblazeb2.com",
  "wasabi_bucket": "my-bucket",
  "wasabi_region": "us-west-1",
  "rackspace_username": "rackspaceuser",
  "rackspace_region": "dfw",
  "rackspace_container": "my-container",
  "one_drive_account_type": "personal",
  "azure_blob_storage_account": "storage-account-name",
  "azure_blob_storage_container": "container-name",
  "s3_compatible_bucket": "my-bucket",
  "s3_compatible_endpoint": "mys3platform.com",
  "s3_compatible_region": "us-east-1",
  "enable_dedicated_ips": True
})
```

### Parameters

* `id` (int64): Required - Remote Server ID.
* `aws_access_key` (string): AWS Access Key.
* `aws_secret_key` (string): AWS secret key.
* `password` (string): Password if needed.
* `private_key` (string): Private key if needed.
* `ssl_certificate` (string): SSL client certificate.
* `google_cloud_storage_credentials_json` (string): A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
* `wasabi_access_key` (string): Wasabi access key.
* `wasabi_secret_key` (string): Wasabi secret key.
* `backblaze_b2_key_id` (string): Backblaze B2 Cloud Storage keyID.
* `backblaze_b2_application_key` (string): Backblaze B2 Cloud Storage applicationKey.
* `rackspace_api_key` (string): Rackspace API key from the Rackspace Cloud Control Panel.
* `reset_authentication` (boolean): Reset authenticated account
* `azure_blob_storage_access_key` (string): Azure Blob Storage secret key.
* `hostname` (string): Hostname or IP address
* `name` (string): Internal name for your reference
* `max_connections` (int64): Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
* `port` (int64): Port for remote server.  Not needed for S3.
* `s3_bucket` (string): S3 bucket name
* `s3_region` (string): S3 region
* `server_certificate` (string): Remote server certificate
* `server_host_key` (string): Remote server SSH Host Key. If provided, we will require that the server host key matches the provided key. Uses OpenSSH format similar to what would go into ~/.ssh/known_hosts
* `server_type` (string): Remote server type.
* `ssl` (string): Should we require SSL?
* `username` (string): Remote server username.  Not needed for S3 buckets.
* `google_cloud_storage_bucket` (string): Google Cloud Storage bucket name
* `google_cloud_storage_project_id` (string): Google Cloud Project ID
* `backblaze_b2_bucket` (string): Backblaze B2 Cloud Storage Bucket name
* `backblaze_b2_s3_endpoint` (string): Backblaze B2 Cloud Storage S3 Endpoint
* `wasabi_bucket` (string): Wasabi Bucket name
* `wasabi_region` (string): Wasabi region
* `rackspace_username` (string): Rackspace username used to login to the Rackspace Cloud Control Panel.
* `rackspace_region` (string): Three letter airport code for Rackspace region. See https://support.rackspace.com/how-to/about-regions/
* `rackspace_container` (string): The name of the container (top level directory) where files will sync.
* `one_drive_account_type` (string): Either personal or business_other account types
* `azure_blob_storage_account` (string): Azure Blob Storage Account name
* `azure_blob_storage_container` (string): Azure Blob Storage Container name
* `s3_compatible_bucket` (string): S3-compatible Bucket name
* `s3_compatible_endpoint` (string): S3-compatible endpoint
* `s3_compatible_region` (string): S3-compatible endpoint
* `enable_dedicated_ips` (boolean): `true` if remote server only accepts connections from dedicated IPs
* `s3_compatible_access_key` (string): S3-compatible Access Key.
* `s3_compatible_secret_key` (string): S3-compatible secret key


---

## Delete Remote Server

```
remote_server = files_sdk.remote_server.list.first
remote_server.delete()
```

### Parameters

* `id` (int64): Required - Remote Server ID.
