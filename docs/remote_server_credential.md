# RemoteServerCredential

## Example RemoteServerCredential Object

```
{
  "id": 1,
  "workspace_id": 1,
  "name": "My Credential",
  "description": "More information or notes about this credential.",
  "server_type": "s3",
  "aws_access_key": "example",
  "google_cloud_storage_s3_compatible_access_key": "example",
  "wasabi_access_key": "example",
  "azure_blob_storage_account": "storage-account-name",
  "azure_files_storage_account": "storage-account-name",
  "s3_compatible_access_key": "example",
  "filebase_access_key": "example",
  "cloudflare_access_key": "example",
  "linode_access_key": "example",
  "username": "user"
}
```

* `id` (int64): Remote Server Credential ID
* `workspace_id` (int64): Workspace ID (0 for default workspace)
* `name` (string): Internal name for your reference
* `description` (string): Internal description for your reference
* `server_type` (string): Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
* `aws_access_key` (string): AWS Access Key.
* `google_cloud_storage_s3_compatible_access_key` (string): Google Cloud Storage: S3-compatible Access Key.
* `wasabi_access_key` (string): Wasabi: Access Key.
* `azure_blob_storage_account` (string): Azure Blob Storage: Account name
* `azure_files_storage_account` (string): Azure Files: Storage Account name
* `s3_compatible_access_key` (string): S3-compatible: Access Key
* `filebase_access_key` (string): Filebase: Access Key.
* `cloudflare_access_key` (string): Cloudflare: Access Key.
* `linode_access_key` (string): Linode: Access Key
* `username` (string): Remote server username.
* `password` (string): Password, if needed.
* `private_key` (string): Private key, if needed.
* `private_key_passphrase` (string): Passphrase for private key if needed.
* `aws_secret_key` (string): AWS: secret key.
* `azure_blob_storage_access_key` (string): Azure Blob Storage: Access Key
* `azure_blob_storage_sas_token` (string): Azure Blob Storage: Shared Access Signature (SAS) token
* `azure_files_storage_access_key` (string): Azure File Storage: Access Key
* `azure_files_storage_sas_token` (string): Azure File Storage: Shared Access Signature (SAS) token
* `backblaze_b2_application_key` (string): Backblaze B2 Cloud Storage: applicationKey
* `backblaze_b2_key_id` (string): Backblaze B2 Cloud Storage: keyID
* `cloudflare_secret_key` (string): Cloudflare: Secret Key
* `filebase_secret_key` (string): Filebase: Secret Key
* `google_cloud_storage_credentials_json` (string): Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
* `google_cloud_storage_s3_compatible_secret_key` (string): Google Cloud Storage: S3-compatible secret key
* `linode_secret_key` (string): Linode: Secret Key
* `s3_compatible_secret_key` (string): S3-compatible: Secret Key
* `wasabi_secret_key` (string): Wasabi: Secret Key


---

## List Remote Server Credentials

```
files_sdk.remote_server_credential.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id` and `name`. Valid field combinations are `[ workspace_id, name ]`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.


---

## Show Remote Server Credential

```
files_sdk.remote_server_credential.find(id)
```

### Parameters

* `id` (int64): Required - Remote Server Credential ID.


---

## Create Remote Server Credential

```
files_sdk.remote_server_credential.create({
  "name": "My Credential",
  "description": "More information or notes about this credential.",
  "server_type": "s3",
  "aws_access_key": "example",
  "azure_blob_storage_account": "storage-account-name",
  "azure_files_storage_account": "storage-account-name",
  "cloudflare_access_key": "example",
  "filebase_access_key": "example",
  "google_cloud_storage_s3_compatible_access_key": "example",
  "linode_access_key": "example",
  "s3_compatible_access_key": "example",
  "username": "user",
  "wasabi_access_key": "example",
  "workspace_id": 0
})
```

### Parameters

* `name` (string): Internal name for your reference
* `description` (string): Internal description for your reference
* `server_type` (string): Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
* `aws_access_key` (string): AWS Access Key.
* `azure_blob_storage_account` (string): Azure Blob Storage: Account name
* `azure_files_storage_account` (string): Azure Files: Storage Account name
* `cloudflare_access_key` (string): Cloudflare: Access Key.
* `filebase_access_key` (string): Filebase: Access Key.
* `google_cloud_storage_s3_compatible_access_key` (string): Google Cloud Storage: S3-compatible Access Key.
* `linode_access_key` (string): Linode: Access Key
* `s3_compatible_access_key` (string): S3-compatible: Access Key
* `username` (string): Remote server username.
* `wasabi_access_key` (string): Wasabi: Access Key.
* `password` (string): Password, if needed.
* `private_key` (string): Private key, if needed.
* `private_key_passphrase` (string): Passphrase for private key if needed.
* `aws_secret_key` (string): AWS: secret key.
* `azure_blob_storage_access_key` (string): Azure Blob Storage: Access Key
* `azure_blob_storage_sas_token` (string): Azure Blob Storage: Shared Access Signature (SAS) token
* `azure_files_storage_access_key` (string): Azure File Storage: Access Key
* `azure_files_storage_sas_token` (string): Azure File Storage: Shared Access Signature (SAS) token
* `backblaze_b2_application_key` (string): Backblaze B2 Cloud Storage: applicationKey
* `backblaze_b2_key_id` (string): Backblaze B2 Cloud Storage: keyID
* `cloudflare_secret_key` (string): Cloudflare: Secret Key
* `filebase_secret_key` (string): Filebase: Secret Key
* `google_cloud_storage_credentials_json` (string): Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
* `google_cloud_storage_s3_compatible_secret_key` (string): Google Cloud Storage: S3-compatible secret key
* `linode_secret_key` (string): Linode: Secret Key
* `s3_compatible_secret_key` (string): S3-compatible: Secret Key
* `wasabi_secret_key` (string): Wasabi: Secret Key
* `workspace_id` (int64): Workspace ID (0 for default workspace)


---

## Update Remote Server Credential

```
files_sdk.remote_server_credential.update(id, {
  "name": "My Credential",
  "description": "More information or notes about this credential.",
  "server_type": "s3",
  "aws_access_key": "example",
  "azure_blob_storage_account": "storage-account-name",
  "azure_files_storage_account": "storage-account-name",
  "cloudflare_access_key": "example",
  "filebase_access_key": "example",
  "google_cloud_storage_s3_compatible_access_key": "example",
  "linode_access_key": "example",
  "s3_compatible_access_key": "example",
  "username": "user",
  "wasabi_access_key": "example"
})
```

### Parameters

* `id` (int64): Required - Remote Server Credential ID.
* `name` (string): Internal name for your reference
* `description` (string): Internal description for your reference
* `server_type` (string): Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
* `aws_access_key` (string): AWS Access Key.
* `azure_blob_storage_account` (string): Azure Blob Storage: Account name
* `azure_files_storage_account` (string): Azure Files: Storage Account name
* `cloudflare_access_key` (string): Cloudflare: Access Key.
* `filebase_access_key` (string): Filebase: Access Key.
* `google_cloud_storage_s3_compatible_access_key` (string): Google Cloud Storage: S3-compatible Access Key.
* `linode_access_key` (string): Linode: Access Key
* `s3_compatible_access_key` (string): S3-compatible: Access Key
* `username` (string): Remote server username.
* `wasabi_access_key` (string): Wasabi: Access Key.
* `password` (string): Password, if needed.
* `private_key` (string): Private key, if needed.
* `private_key_passphrase` (string): Passphrase for private key if needed.
* `aws_secret_key` (string): AWS: secret key.
* `azure_blob_storage_access_key` (string): Azure Blob Storage: Access Key
* `azure_blob_storage_sas_token` (string): Azure Blob Storage: Shared Access Signature (SAS) token
* `azure_files_storage_access_key` (string): Azure File Storage: Access Key
* `azure_files_storage_sas_token` (string): Azure File Storage: Shared Access Signature (SAS) token
* `backblaze_b2_application_key` (string): Backblaze B2 Cloud Storage: applicationKey
* `backblaze_b2_key_id` (string): Backblaze B2 Cloud Storage: keyID
* `cloudflare_secret_key` (string): Cloudflare: Secret Key
* `filebase_secret_key` (string): Filebase: Secret Key
* `google_cloud_storage_credentials_json` (string): Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
* `google_cloud_storage_s3_compatible_secret_key` (string): Google Cloud Storage: S3-compatible secret key
* `linode_secret_key` (string): Linode: Secret Key
* `s3_compatible_secret_key` (string): S3-compatible: Secret Key
* `wasabi_secret_key` (string): Wasabi: Secret Key


---

## Delete Remote Server Credential

```
files_sdk.remote_server_credential.delete(id)
```

### Parameters

* `id` (int64): Required - Remote Server Credential ID.


---

## Update Remote Server Credential

```
remote_server_credential = files_sdk.remote_server_credential.find(id)
remote_server_credential.update({
  "name": "My Credential",
  "description": "More information or notes about this credential.",
  "server_type": "s3",
  "aws_access_key": "example",
  "azure_blob_storage_account": "storage-account-name",
  "azure_files_storage_account": "storage-account-name",
  "cloudflare_access_key": "example",
  "filebase_access_key": "example",
  "google_cloud_storage_s3_compatible_access_key": "example",
  "linode_access_key": "example",
  "s3_compatible_access_key": "example",
  "username": "user",
  "wasabi_access_key": "example"
})
```

### Parameters

* `id` (int64): Required - Remote Server Credential ID.
* `name` (string): Internal name for your reference
* `description` (string): Internal description for your reference
* `server_type` (string): Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
* `aws_access_key` (string): AWS Access Key.
* `azure_blob_storage_account` (string): Azure Blob Storage: Account name
* `azure_files_storage_account` (string): Azure Files: Storage Account name
* `cloudflare_access_key` (string): Cloudflare: Access Key.
* `filebase_access_key` (string): Filebase: Access Key.
* `google_cloud_storage_s3_compatible_access_key` (string): Google Cloud Storage: S3-compatible Access Key.
* `linode_access_key` (string): Linode: Access Key
* `s3_compatible_access_key` (string): S3-compatible: Access Key
* `username` (string): Remote server username.
* `wasabi_access_key` (string): Wasabi: Access Key.
* `password` (string): Password, if needed.
* `private_key` (string): Private key, if needed.
* `private_key_passphrase` (string): Passphrase for private key if needed.
* `aws_secret_key` (string): AWS: secret key.
* `azure_blob_storage_access_key` (string): Azure Blob Storage: Access Key
* `azure_blob_storage_sas_token` (string): Azure Blob Storage: Shared Access Signature (SAS) token
* `azure_files_storage_access_key` (string): Azure File Storage: Access Key
* `azure_files_storage_sas_token` (string): Azure File Storage: Shared Access Signature (SAS) token
* `backblaze_b2_application_key` (string): Backblaze B2 Cloud Storage: applicationKey
* `backblaze_b2_key_id` (string): Backblaze B2 Cloud Storage: keyID
* `cloudflare_secret_key` (string): Cloudflare: Secret Key
* `filebase_secret_key` (string): Filebase: Secret Key
* `google_cloud_storage_credentials_json` (string): Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
* `google_cloud_storage_s3_compatible_secret_key` (string): Google Cloud Storage: S3-compatible secret key
* `linode_secret_key` (string): Linode: Secret Key
* `s3_compatible_secret_key` (string): S3-compatible: Secret Key
* `wasabi_secret_key` (string): Wasabi: Secret Key


---

## Delete Remote Server Credential

```
remote_server_credential = files_sdk.remote_server_credential.find(id)
remote_server_credential.delete()
```

### Parameters

* `id` (int64): Required - Remote Server Credential ID.
