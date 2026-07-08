# Secret

## Example Secret Object

```
{
  "id": 1,
  "workspace_id": 1,
  "name": "Production API token",
  "description": "Used by production API integrations.",
  "secret_type": "token",
  "metadata": {
    "key": "example value"
  },
  "value_field_names": [
    "example"
  ],
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Secret ID.
* `workspace_id` (int64): Workspace ID. 0 means the default workspace.
* `name` (string): Secret name.
* `description` (string): Internal description for your reference.
* `secret_type` (string): Secret type.
* `metadata` (object): Non-secret metadata for the Secret type.
* `value_field_names` (array(string)): Names of configured secret value fields. Secret values are never returned.
* `created_at` (date-time): Secret create date/time.
* `updated_at` (date-time): Secret update date/time.


---

## List Secrets

```
files_sdk.secret.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `name` or `secret_type`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`, `name` or `secret_type`. Valid field combinations are `[ workspace_id, name ]`, `[ workspace_id, secret_type ]`, `[ secret_type, name ]` or `[ workspace_id, secret_type, name ]`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.


---

## Show Secret

```
files_sdk.secret.find(id)
```

### Parameters

* `id` (int64): Required - Secret ID.


---

## Create Secret

```
files_sdk.secret.create({
  "name": "Production API token",
  "description": "Used by production API integrations.",
  "secret_type": "token",
  "metadata": {"key":"example value"},
  "workspace_id": 0
})
```

### Parameters

* `name` (string): Required - Secret name.
* `description` (string): Internal description for your reference.
* `secret_type` (string): Required - Secret type.
* `metadata` (object): Non-secret metadata for the Secret type.
* `workspace_id` (int64): Workspace ID. 0 means the default workspace.


---

## Update Secret

```
files_sdk.secret.update(id, {
  "name": "Production API token",
  "description": "Used by production API integrations.",
  "secret_type": "token",
  "metadata": {"key":"example value"}
})
```

### Parameters

* `id` (int64): Required - Secret ID.
* `name` (string): Secret name.
* `description` (string): Internal description for your reference.
* `secret_type` (string): Secret type.
* `metadata` (object): Non-secret metadata for the Secret type.


---

## Delete Secret

```
files_sdk.secret.delete(id)
```

### Parameters

* `id` (int64): Required - Secret ID.


---

## Update Secret

```
secret = files_sdk.secret.find(id)
secret.update({
  "name": "Production API token",
  "description": "Used by production API integrations.",
  "secret_type": "token",
  "metadata": {"key":"example value"}
})
```

### Parameters

* `id` (int64): Required - Secret ID.
* `name` (string): Secret name.
* `description` (string): Internal description for your reference.
* `secret_type` (string): Secret type.
* `metadata` (object): Non-secret metadata for the Secret type.


---

## Delete Secret

```
secret = files_sdk.secret.find(id)
secret.delete()
```

### Parameters

* `id` (int64): Required - Secret ID.
