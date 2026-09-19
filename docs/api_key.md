# ApiKey

## Example ApiKey Object

```
{
  "id": 1,
  "descriptive_label": "Site-wide API key for https://site.files.com/ (key ID #1)",
  "description": "example",
  "created_at": "2000-01-01T01:00:00Z",
  "expires_at": "2000-01-01T01:00:00Z",
  "key": "[key]",
  "aws_style_credentials": True,
  "aws_access_key_id": "[aws_access_key_id]",
  "aws_secret_key": "[aws_secret_key]",
  "last_use_at": "2000-01-01T01:00:00Z",
  "name": "My Main API Key",
  "permission_set": "full",
  "platform": "win32",
  "site_id": 1,
  "site_name": "example",
  "url": "example",
  "user_id": 1,
  "workspace_id": 1
}
```

* `id` (int64): API Key ID
* `descriptive_label` (string): Unique label that describes this API key.  Useful for external systems where you may have API keys from multiple accounts and want a human-readable label for each key.
* `description` (string): User-supplied description of API key.
* `created_at` (date-time): Time which API Key was created
* `expires_at` (date-time): API Key expiration date
* `key` (string): API Key actual key string
* `aws_style_credentials` (boolean): If `true`, this API key will be usable with AWS-compatible endpoints, such as our Inbound S3-compatible endpoint.
* `aws_access_key_id` (string): AWS Access Key ID to use with AWS-compatible endpoints, such as our Inbound S3-compatible endpoint.
* `aws_secret_key` (string): AWS Secret Key to use with AWS-compatible endpoints, such as our Inbound S3-compatible endpoint.
* `last_use_at` (date-time): API Key last used - note this value is only updated once per 3 hour period, so the 'actual' time of last use may be up to 3 hours later than this timestamp.
* `name` (string): Internal name for the API Key.  For your use.
* `permission_set` (string): Permissions for this API Key. Keys with the `desktop_app` permission set only have the ability to do the functions provided in our Desktop App (File and Share Link operations). Keys with the `office_integration` permission set are auto generated, and automatically expire, to allow users to interact with office integration platforms. Keys with the `files_only` permission set can use only the files, folders, and file_actions endpoints, where they perform file operations as a full-access file user in the key's workspace scope, along with `GET /file_migrations/{id}` and `GET /api_key`. They cannot use site admin, workspace admin, folder admin, group admin, partner admin, or billing privileges from the owning user, and every other endpoint denies them with `not-authorized/api-key-only-for-file-operations`.
* `platform` (string): If this API key represents a Desktop app, what platform was it created on?
* `site_id` (int64): Site ID
* `site_name` (string): Site Name
* `url` (string): URL for API host.
* `user_id` (int64): User ID for the owner of this API Key.  May be blank for Site-wide API Keys.
* `workspace_id` (int64): Workspace ID for this API Key. `0` means the default workspace.
* `path` (string): Restricts the file and folder operations made with this key, meaning the files, folders, and file_actions endpoints, to the specified folder and its descendants, including copy and move destinations. Other endpoints do not apply the path restriction; use the `files_only` permission set to confine a key to the endpoints that do. Does not grant access beyond the owning user's permissions. Optional except for `office_integration` keys, which require a path the owning user can read.


---

## List API Keys

```
files_sdk.api_key.list({
  "user_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id` and `workspace_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `aws_style_credentials` and `expires_at`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `expires_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `expires_at`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `expires_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `expires_at`.


---

## Show information about current API key.  (Requires current API connection to be using an API key.)

```
files_sdk.api_key.find_current()
```


---

## Show API Key

```
files_sdk.api_key.find(id)
```

### Parameters

* `id` (int64): Required - Api Key ID.


---

## Create API Key

```
files_sdk.api_key.create({
  "user_id": 1,
  "description": "example",
  "expires_at": "2000-01-01T01:00:00Z",
  "name": "My Main API Key",
  "aws_style_credentials": True,
  "path": "shared/docs",
  "permission_set": "full",
  "workspace_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `description` (string): User-supplied description of API key.
* `expires_at` (string): API Key expiration date
* `name` (string): Required - Internal name for the API Key.  For your use.
* `aws_style_credentials` (boolean): If `true`, this API key will be usable with AWS-compatible endpoints, such as our Inbound S3-compatible endpoint.
* `path` (string): Restricts the file and folder operations made with this key, meaning the files, folders, and file_actions endpoints, to the specified folder and its descendants, including copy and move destinations. Other endpoints do not apply the path restriction; use the `files_only` permission set to confine a key to the endpoints that do. Does not grant access beyond the owning user's permissions. Optional except for `office_integration` keys, which require a path the owning user can read.
* `permission_set` (string): Permissions for this API Key. Keys with the `desktop_app` permission set only have the ability to do the functions provided in our Desktop App (File and Share Link operations). Keys with the `office_integration` permission set are auto generated, and automatically expire, to allow users to interact with office integration platforms. Keys with the `files_only` permission set can use only the files, folders, and file_actions endpoints, where they perform file operations as a full-access file user in the key's workspace scope, along with `GET /file_migrations/{id}` and `GET /api_key`. They cannot use site admin, workspace admin, folder admin, group admin, partner admin, or billing privileges from the owning user, and every other endpoint denies them with `not-authorized/api-key-only-for-file-operations`.
* `workspace_id` (int64): Workspace ID for this API Key. `0` means the default workspace.


---

## Update current API key.  (Requires current API connection to be using an API key.)

```
files_sdk.api_key.update_current({
  "expires_at": "2000-01-01T01:00:00Z",
  "name": "My Main API Key",
  "permission_set": "full"
})
```

### Parameters

* `expires_at` (string): API Key expiration date
* `name` (string): Internal name for the API Key.  For your use.
* `permission_set` (string): Permissions for this API Key. Keys with the `desktop_app` permission set only have the ability to do the functions provided in our Desktop App (File and Share Link operations). Keys with the `office_integration` permission set are auto generated, and automatically expire, to allow users to interact with office integration platforms. Keys with the `files_only` permission set can use only the files, folders, and file_actions endpoints, where they perform file operations as a full-access file user in the key's workspace scope, along with `GET /file_migrations/{id}` and `GET /api_key`. They cannot use site admin, workspace admin, folder admin, group admin, partner admin, or billing privileges from the owning user, and every other endpoint denies them with `not-authorized/api-key-only-for-file-operations`.


---

## Update API Key

```
files_sdk.api_key.update(id, {
  "description": "example",
  "expires_at": "2000-01-01T01:00:00Z",
  "name": "My Main API Key"
})
```

### Parameters

* `id` (int64): Required - Api Key ID.
* `description` (string): User-supplied description of API key.
* `expires_at` (string): API Key expiration date
* `name` (string): Internal name for the API Key.  For your use.


---

## Delete current API key.  (Requires current API connection to be using an API key.)

```
files_sdk.api_key.delete_current()
```


---

## Delete API Key

```
files_sdk.api_key.delete(id)
```

### Parameters

* `id` (int64): Required - Api Key ID.


---

## Update API Key

```
api_key = files_sdk.api_key.find(id)
api_key.update({
  "description": "example",
  "expires_at": "2000-01-01T01:00:00Z",
  "name": "My Main API Key"
})
```

### Parameters

* `id` (int64): Required - Api Key ID.
* `description` (string): User-supplied description of API key.
* `expires_at` (string): API Key expiration date
* `name` (string): Internal name for the API Key.  For your use.


---

## Delete API Key

```
api_key = files_sdk.api_key.find(id)
api_key.delete()
```

### Parameters

* `id` (int64): Required - Api Key ID.
