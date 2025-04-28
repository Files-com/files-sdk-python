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
  "pin_to_site_region": True,
  "pinned_region": "us-east-1",
  "s3_bucket": "my-bucket",
  "s3_region": "us-east-1",
  "aws_access_key": "example",
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
  "wasabi_access_key": "example",
  "rackspace_username": "rackspaceuser",
  "rackspace_region": "dfw",
  "rackspace_container": "my-container",
  "auth_status": "in_setup",
  "auth_account_name": "me@example.com",
  "one_drive_account_type": "personal",
  "azure_blob_storage_account": "storage-account-name",
  "azure_blob_storage_container": "container-name",
  "azure_blob_storage_hierarchical_namespace": True,
  "azure_blob_storage_dns_suffix": "usgovcloudapi.net",
  "azure_files_storage_account": "storage-account-name",
  "azure_files_storage_share_name": "share-name",
  "azure_files_storage_dns_suffix": "file.core.windows.net",
  "s3_compatible_bucket": "my-bucket",
  "s3_compatible_endpoint": "mys3platform.com",
  "s3_compatible_region": "us-east-1",
  "s3_compatible_access_key": "example",
  "enable_dedicated_ips": True,
  "files_agent_permission_set": "read_write",
  "files_agent_root": "example",
  "files_agent_api_token": "example",
  "files_agent_version": "example",
  "filebase_bucket": "my-bucket",
  "filebase_access_key": "example",
  "cloudflare_bucket": "my-bucket",
  "cloudflare_access_key": "example",
  "cloudflare_endpoint": "https://<ACCOUNT_ID>.r2.cloudflarestorage.com",
  "dropbox_teams": True,
  "linode_bucket": "my-bucket",
  "linode_access_key": "example",
  "linode_region": "us-east-1",
  "supports_versioning": True
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
* `pin_to_site_region` (boolean): If true, we will ensure that all communications with this remote server are made through the primary region of the site.  This setting can also be overridden by a site-wide setting which will force it to true.
* `pinned_region` (string): If set, all communications with this remote server are made through the provided region.
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
* `auth_status` (string): Either `in_setup` or `complete`
* `auth_account_name` (string): Describes the authorized account
* `one_drive_account_type` (string): Either personal or business_other account types
* `azure_blob_storage_account` (string): Azure Blob Storage Account name
* `azure_blob_storage_container` (string): Azure Blob Storage Container name
* `azure_blob_storage_hierarchical_namespace` (boolean): Enable when storage account has hierarchical namespace feature enabled
* `azure_blob_storage_dns_suffix` (string): Custom DNS suffix
* `azure_files_storage_account` (string): Azure File Storage Account name
* `azure_files_storage_share_name` (string): Azure File Storage Share name
* `azure_files_storage_dns_suffix` (string): Custom DNS suffix
* `s3_compatible_bucket` (string): S3-compatible Bucket name
* `s3_compatible_endpoint` (string): S3-compatible endpoint
* `s3_compatible_region` (string): S3-compatible endpoint
* `s3_compatible_access_key` (string): S3-compatible Access Key.
* `enable_dedicated_ips` (boolean): `true` if remote server only accepts connections from dedicated IPs
* `files_agent_permission_set` (string): Local permissions for files agent. read_only, write_only, or read_write
* `files_agent_root` (string): Agent local root path
* `files_agent_api_token` (string): Files Agent API Token
* `files_agent_version` (string): Files Agent version
* `filebase_bucket` (string): Filebase Bucket name
* `filebase_access_key` (string): Filebase Access Key.
* `cloudflare_bucket` (string): Cloudflare Bucket name
* `cloudflare_access_key` (string): Cloudflare Access Key.
* `cloudflare_endpoint` (string): Cloudflare endpoint
* `dropbox_teams` (boolean): List Team folders in root
* `linode_bucket` (string): Linode Bucket name
* `linode_access_key` (string): Linode Access Key.
* `linode_region` (string): Linode region
* `supports_versioning` (boolean): If true, this remote server supports file versioning. This value is determined automatically by Files.com.
* `aws_secret_key` (string): AWS secret key.
* `password` (string): Password if needed.
* `private_key` (string): Private key if needed.
* `private_key_passphrase` (string): Passphrase for private key if needed.
* `ssl_certificate` (string): SSL client certificate.
* `google_cloud_storage_credentials_json` (string): A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
* `wasabi_secret_key` (string): Wasabi secret key.
* `backblaze_b2_key_id` (string): Backblaze B2 Cloud Storage keyID.
* `backblaze_b2_application_key` (string): Backblaze B2 Cloud Storage applicationKey.
* `rackspace_api_key` (string): Rackspace API key from the Rackspace Cloud Control Panel.
* `reset_authentication` (boolean): Reset authenticated account
* `azure_blob_storage_access_key` (string): Azure Blob Storage secret key.
* `azure_files_storage_access_key` (string): Azure File Storage access key.
* `azure_blob_storage_sas_token` (string): Shared Access Signature (SAS) token
* `azure_files_storage_sas_token` (string): Shared Access Signature (SAS) token
* `s3_compatible_secret_key` (string): S3-compatible secret key
* `filebase_secret_key` (string): Filebase secret key
* `cloudflare_secret_key` (string): Cloudflare secret key
* `linode_secret_key` (string): Linode secret key


---

## List Remote Servers

```
files_sdk.remote_server.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `server_type`, `backblaze_b2_bucket`, `google_cloud_storage_bucket`, `wasabi_bucket`, `s3_bucket`, `rackspace_container`, `azure_blob_storage_container`, `azure_files_storage_share_name`, `s3_compatible_bucket`, `filebase_bucket`, `cloudflare_bucket` or `linode_bucket`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `name`, `server_type`, `backblaze_b2_bucket`, `google_cloud_storage_bucket`, `wasabi_bucket`, `s3_bucket`, `rackspace_container`, `azure_blob_storage_container`, `azure_files_storage_share_name`, `s3_compatible_bucket`, `filebase_bucket`, `cloudflare_bucket` or `linode_bucket`. Valid field combinations are `[ server_type, name ]`, `[ backblaze_b2_bucket, name ]`, `[ google_cloud_storage_bucket, name ]`, `[ wasabi_bucket, name ]`, `[ s3_bucket, name ]`, `[ rackspace_container, name ]`, `[ azure_blob_storage_container, name ]`, `[ azure_files_storage_share_name, name ]`, `[ s3_compatible_bucket, name ]`, `[ filebase_bucket, name ]`, `[ cloudflare_bucket, name ]` or `[ linode_bucket, name ]`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`, `backblaze_b2_bucket`, `google_cloud_storage_bucket`, `wasabi_bucket`, `s3_bucket`, `rackspace_container`, `azure_blob_storage_container`, `azure_files_storage_share_name`, `s3_compatible_bucket`, `filebase_bucket`, `cloudflare_bucket` or `linode_bucket`. Valid field combinations are `[ backblaze_b2_bucket, name ]`, `[ google_cloud_storage_bucket, name ]`, `[ wasabi_bucket, name ]`, `[ s3_bucket, name ]`, `[ rackspace_container, name ]`, `[ azure_blob_storage_container, name ]`, `[ azure_files_storage_share_name, name ]`, `[ s3_compatible_bucket, name ]`, `[ filebase_bucket, name ]`, `[ cloudflare_bucket, name ]` or `[ linode_bucket, name ]`.


---

## Show Remote Server

```
files_sdk.remote_server.find(id)
```

### Parameters

* `id` (int64): Required - Remote Server ID.


---

## Download configuration file (required for some Remote Server integrations, such as the Files.com Agent)

```
files_sdk.remote_server.find_configuration_file(id)
```

### Parameters

* `id` (int64): Required - Remote Server ID.


---

## Create Remote Server

```
files_sdk.remote_server.create({
  "aws_access_key": "example",
  "wasabi_access_key": "example",
  "reset_authentication": False,
  "hostname": "remote-server.com",
  "name": "My Remote server",
  "max_connections": 1,
  "pin_to_site_region": True,
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
  "azure_blob_storage_hierarchical_namespace": True,
  "azure_blob_storage_dns_suffix": "usgovcloudapi.net",
  "azure_files_storage_account": "storage-account-name",
  "azure_files_storage_share_name": "share-name",
  "azure_files_storage_dns_suffix": "file.core.windows.net",
  "s3_compatible_bucket": "my-bucket",
  "s3_compatible_endpoint": "mys3platform.com",
  "s3_compatible_region": "us-east-1",
  "enable_dedicated_ips": True,
  "s3_compatible_access_key": "example",
  "files_agent_root": "example",
  "files_agent_permission_set": "read_write",
  "files_agent_version": "example",
  "filebase_access_key": "example",
  "filebase_bucket": "my-bucket",
  "cloudflare_access_key": "example",
  "cloudflare_bucket": "my-bucket",
  "cloudflare_endpoint": "https://<ACCOUNT_ID>.r2.cloudflarestorage.com",
  "dropbox_teams": True,
  "linode_access_key": "example",
  "linode_bucket": "my-bucket",
  "linode_region": "us-east-1"
})
```

### Parameters

* `aws_access_key` (string): AWS Access Key.
* `aws_secret_key` (string): AWS secret key.
* `password` (string): Password if needed.
* `private_key` (string): Private key if needed.
* `private_key_passphrase` (string): Passphrase for private key if needed.
* `ssl_certificate` (string): SSL client certificate.
* `google_cloud_storage_credentials_json` (string): A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
* `wasabi_access_key` (string): Wasabi access key.
* `wasabi_secret_key` (string): Wasabi secret key.
* `backblaze_b2_key_id` (string): Backblaze B2 Cloud Storage keyID.
* `backblaze_b2_application_key` (string): Backblaze B2 Cloud Storage applicationKey.
* `rackspace_api_key` (string): Rackspace API key from the Rackspace Cloud Control Panel.
* `reset_authentication` (boolean): Reset authenticated account
* `azure_blob_storage_access_key` (string): Azure Blob Storage secret key.
* `azure_files_storage_access_key` (string): Azure File Storage access key.
* `hostname` (string): Hostname or IP address
* `name` (string): Internal name for your reference
* `max_connections` (int64): Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
* `pin_to_site_region` (boolean): If true, we will ensure that all communications with this remote server are made through the primary region of the site.  This setting can also be overridden by a site-wide setting which will force it to true.
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
* `azure_blob_storage_hierarchical_namespace` (boolean): Enable when storage account has hierarchical namespace feature enabled
* `azure_blob_storage_sas_token` (string): Shared Access Signature (SAS) token
* `azure_blob_storage_dns_suffix` (string): Custom DNS suffix
* `azure_files_storage_account` (string): Azure File Storage Account name
* `azure_files_storage_share_name` (string): Azure File Storage Share name
* `azure_files_storage_dns_suffix` (string): Custom DNS suffix
* `azure_files_storage_sas_token` (string): Shared Access Signature (SAS) token
* `s3_compatible_bucket` (string): S3-compatible Bucket name
* `s3_compatible_endpoint` (string): S3-compatible endpoint
* `s3_compatible_region` (string): S3-compatible endpoint
* `enable_dedicated_ips` (boolean): `true` if remote server only accepts connections from dedicated IPs
* `s3_compatible_access_key` (string): S3-compatible Access Key.
* `s3_compatible_secret_key` (string): S3-compatible secret key
* `files_agent_root` (string): Agent local root path
* `files_agent_permission_set` (string): Local permissions for files agent. read_only, write_only, or read_write
* `files_agent_version` (string): Files Agent version
* `filebase_access_key` (string): Filebase Access Key.
* `filebase_secret_key` (string): Filebase secret key
* `filebase_bucket` (string): Filebase Bucket name
* `cloudflare_access_key` (string): Cloudflare Access Key.
* `cloudflare_secret_key` (string): Cloudflare secret key
* `cloudflare_bucket` (string): Cloudflare Bucket name
* `cloudflare_endpoint` (string): Cloudflare endpoint
* `dropbox_teams` (boolean): List Team folders in root
* `linode_access_key` (string): Linode Access Key.
* `linode_secret_key` (string): Linode secret key
* `linode_bucket` (string): Linode Bucket name
* `linode_region` (string): Linode region


---

## Post local changes, check in, and download configuration file (used by some Remote Server integrations, such as the Files.com Agent)

```
files_sdk.remote_server.configuration_file(id, {
  "api_token": "example",
  "permission_set": "example",
  "root": "C:\\Users\\",
  "hostname": "example",
  "port": 1,
  "status": "example",
  "config_version": "example",
  "private_key": "example",
  "public_key": "example",
  "server_host_key": "example",
  "subdomain": "example"
})
```

### Parameters

* `id` (int64): Required - Remote Server ID.
* `api_token` (string): Files Agent API Token
* `permission_set` (string): The permission set for the agent ['read_write', 'read_only', 'write_only']
* `root` (string): The root directory for the agent
* `hostname` (string): 
* `port` (int64): Incoming port for files agent connections
* `status` (string): either running or shutdown
* `config_version` (string): agent config version
* `private_key` (string): The private key for the agent
* `public_key` (string): public key
* `server_host_key` (string): 
* `subdomain` (string): Files.com subdomain site name


---

## Update Remote Server

```
files_sdk.remote_server.update(id, {
  "aws_access_key": "example",
  "wasabi_access_key": "example",
  "reset_authentication": False,
  "hostname": "remote-server.com",
  "name": "My Remote server",
  "max_connections": 1,
  "pin_to_site_region": True,
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
  "azure_blob_storage_hierarchical_namespace": True,
  "azure_blob_storage_dns_suffix": "usgovcloudapi.net",
  "azure_files_storage_account": "storage-account-name",
  "azure_files_storage_share_name": "share-name",
  "azure_files_storage_dns_suffix": "file.core.windows.net",
  "s3_compatible_bucket": "my-bucket",
  "s3_compatible_endpoint": "mys3platform.com",
  "s3_compatible_region": "us-east-1",
  "enable_dedicated_ips": True,
  "s3_compatible_access_key": "example",
  "files_agent_root": "example",
  "files_agent_permission_set": "read_write",
  "files_agent_version": "example",
  "filebase_access_key": "example",
  "filebase_bucket": "my-bucket",
  "cloudflare_access_key": "example",
  "cloudflare_bucket": "my-bucket",
  "cloudflare_endpoint": "https://<ACCOUNT_ID>.r2.cloudflarestorage.com",
  "dropbox_teams": True,
  "linode_access_key": "example",
  "linode_bucket": "my-bucket",
  "linode_region": "us-east-1"
})
```

### Parameters

* `id` (int64): Required - Remote Server ID.
* `aws_access_key` (string): AWS Access Key.
* `aws_secret_key` (string): AWS secret key.
* `password` (string): Password if needed.
* `private_key` (string): Private key if needed.
* `private_key_passphrase` (string): Passphrase for private key if needed.
* `ssl_certificate` (string): SSL client certificate.
* `google_cloud_storage_credentials_json` (string): A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
* `wasabi_access_key` (string): Wasabi access key.
* `wasabi_secret_key` (string): Wasabi secret key.
* `backblaze_b2_key_id` (string): Backblaze B2 Cloud Storage keyID.
* `backblaze_b2_application_key` (string): Backblaze B2 Cloud Storage applicationKey.
* `rackspace_api_key` (string): Rackspace API key from the Rackspace Cloud Control Panel.
* `reset_authentication` (boolean): Reset authenticated account
* `azure_blob_storage_access_key` (string): Azure Blob Storage secret key.
* `azure_files_storage_access_key` (string): Azure File Storage access key.
* `hostname` (string): Hostname or IP address
* `name` (string): Internal name for your reference
* `max_connections` (int64): Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
* `pin_to_site_region` (boolean): If true, we will ensure that all communications with this remote server are made through the primary region of the site.  This setting can also be overridden by a site-wide setting which will force it to true.
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
* `azure_blob_storage_hierarchical_namespace` (boolean): Enable when storage account has hierarchical namespace feature enabled
* `azure_blob_storage_sas_token` (string): Shared Access Signature (SAS) token
* `azure_blob_storage_dns_suffix` (string): Custom DNS suffix
* `azure_files_storage_account` (string): Azure File Storage Account name
* `azure_files_storage_share_name` (string): Azure File Storage Share name
* `azure_files_storage_dns_suffix` (string): Custom DNS suffix
* `azure_files_storage_sas_token` (string): Shared Access Signature (SAS) token
* `s3_compatible_bucket` (string): S3-compatible Bucket name
* `s3_compatible_endpoint` (string): S3-compatible endpoint
* `s3_compatible_region` (string): S3-compatible endpoint
* `enable_dedicated_ips` (boolean): `true` if remote server only accepts connections from dedicated IPs
* `s3_compatible_access_key` (string): S3-compatible Access Key.
* `s3_compatible_secret_key` (string): S3-compatible secret key
* `files_agent_root` (string): Agent local root path
* `files_agent_permission_set` (string): Local permissions for files agent. read_only, write_only, or read_write
* `files_agent_version` (string): Files Agent version
* `filebase_access_key` (string): Filebase Access Key.
* `filebase_secret_key` (string): Filebase secret key
* `filebase_bucket` (string): Filebase Bucket name
* `cloudflare_access_key` (string): Cloudflare Access Key.
* `cloudflare_secret_key` (string): Cloudflare secret key
* `cloudflare_bucket` (string): Cloudflare Bucket name
* `cloudflare_endpoint` (string): Cloudflare endpoint
* `dropbox_teams` (boolean): List Team folders in root
* `linode_access_key` (string): Linode Access Key.
* `linode_secret_key` (string): Linode secret key
* `linode_bucket` (string): Linode Bucket name
* `linode_region` (string): Linode region


---

## Delete Remote Server

```
files_sdk.remote_server.delete(id)
```

### Parameters

* `id` (int64): Required - Remote Server ID.


---

## Post local changes, check in, and download configuration file (used by some Remote Server integrations, such as the Files.com Agent)

```
remote_server = files_sdk.remote_server.find(id)
remote_server.configuration_file({
  "api_token": "example",
  "permission_set": "example",
  "root": "C:\\Users\\",
  "hostname": "example",
  "port": 1,
  "status": "example",
  "config_version": "example",
  "private_key": "example",
  "public_key": "example",
  "server_host_key": "example",
  "subdomain": "example"
})
```

### Parameters

* `id` (int64): Required - Remote Server ID.
* `api_token` (string): Files Agent API Token
* `permission_set` (string): The permission set for the agent ['read_write', 'read_only', 'write_only']
* `root` (string): The root directory for the agent
* `hostname` (string): 
* `port` (int64): Incoming port for files agent connections
* `status` (string): either running or shutdown
* `config_version` (string): agent config version
* `private_key` (string): The private key for the agent
* `public_key` (string): public key
* `server_host_key` (string): 
* `subdomain` (string): Files.com subdomain site name


---

## Update Remote Server

```
remote_server = files_sdk.remote_server.find(id)
remote_server.update({
  "aws_access_key": "example",
  "wasabi_access_key": "example",
  "reset_authentication": False,
  "hostname": "remote-server.com",
  "name": "My Remote server",
  "max_connections": 1,
  "pin_to_site_region": True,
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
  "azure_blob_storage_hierarchical_namespace": True,
  "azure_blob_storage_dns_suffix": "usgovcloudapi.net",
  "azure_files_storage_account": "storage-account-name",
  "azure_files_storage_share_name": "share-name",
  "azure_files_storage_dns_suffix": "file.core.windows.net",
  "s3_compatible_bucket": "my-bucket",
  "s3_compatible_endpoint": "mys3platform.com",
  "s3_compatible_region": "us-east-1",
  "enable_dedicated_ips": True,
  "s3_compatible_access_key": "example",
  "files_agent_root": "example",
  "files_agent_permission_set": "read_write",
  "files_agent_version": "example",
  "filebase_access_key": "example",
  "filebase_bucket": "my-bucket",
  "cloudflare_access_key": "example",
  "cloudflare_bucket": "my-bucket",
  "cloudflare_endpoint": "https://<ACCOUNT_ID>.r2.cloudflarestorage.com",
  "dropbox_teams": True,
  "linode_access_key": "example",
  "linode_bucket": "my-bucket",
  "linode_region": "us-east-1"
})
```

### Parameters

* `id` (int64): Required - Remote Server ID.
* `aws_access_key` (string): AWS Access Key.
* `aws_secret_key` (string): AWS secret key.
* `password` (string): Password if needed.
* `private_key` (string): Private key if needed.
* `private_key_passphrase` (string): Passphrase for private key if needed.
* `ssl_certificate` (string): SSL client certificate.
* `google_cloud_storage_credentials_json` (string): A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
* `wasabi_access_key` (string): Wasabi access key.
* `wasabi_secret_key` (string): Wasabi secret key.
* `backblaze_b2_key_id` (string): Backblaze B2 Cloud Storage keyID.
* `backblaze_b2_application_key` (string): Backblaze B2 Cloud Storage applicationKey.
* `rackspace_api_key` (string): Rackspace API key from the Rackspace Cloud Control Panel.
* `reset_authentication` (boolean): Reset authenticated account
* `azure_blob_storage_access_key` (string): Azure Blob Storage secret key.
* `azure_files_storage_access_key` (string): Azure File Storage access key.
* `hostname` (string): Hostname or IP address
* `name` (string): Internal name for your reference
* `max_connections` (int64): Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
* `pin_to_site_region` (boolean): If true, we will ensure that all communications with this remote server are made through the primary region of the site.  This setting can also be overridden by a site-wide setting which will force it to true.
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
* `azure_blob_storage_hierarchical_namespace` (boolean): Enable when storage account has hierarchical namespace feature enabled
* `azure_blob_storage_sas_token` (string): Shared Access Signature (SAS) token
* `azure_blob_storage_dns_suffix` (string): Custom DNS suffix
* `azure_files_storage_account` (string): Azure File Storage Account name
* `azure_files_storage_share_name` (string): Azure File Storage Share name
* `azure_files_storage_dns_suffix` (string): Custom DNS suffix
* `azure_files_storage_sas_token` (string): Shared Access Signature (SAS) token
* `s3_compatible_bucket` (string): S3-compatible Bucket name
* `s3_compatible_endpoint` (string): S3-compatible endpoint
* `s3_compatible_region` (string): S3-compatible endpoint
* `enable_dedicated_ips` (boolean): `true` if remote server only accepts connections from dedicated IPs
* `s3_compatible_access_key` (string): S3-compatible Access Key.
* `s3_compatible_secret_key` (string): S3-compatible secret key
* `files_agent_root` (string): Agent local root path
* `files_agent_permission_set` (string): Local permissions for files agent. read_only, write_only, or read_write
* `files_agent_version` (string): Files Agent version
* `filebase_access_key` (string): Filebase Access Key.
* `filebase_secret_key` (string): Filebase secret key
* `filebase_bucket` (string): Filebase Bucket name
* `cloudflare_access_key` (string): Cloudflare Access Key.
* `cloudflare_secret_key` (string): Cloudflare secret key
* `cloudflare_bucket` (string): Cloudflare Bucket name
* `cloudflare_endpoint` (string): Cloudflare endpoint
* `dropbox_teams` (boolean): List Team folders in root
* `linode_access_key` (string): Linode Access Key.
* `linode_secret_key` (string): Linode secret key
* `linode_bucket` (string): Linode Bucket name
* `linode_region` (string): Linode region


---

## Delete Remote Server

```
remote_server = files_sdk.remote_server.find(id)
remote_server.delete()
```

### Parameters

* `id` (int64): Required - Remote Server ID.
