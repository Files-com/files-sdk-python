# DatabaseDestination

## Example DatabaseDestination Object

The API sends each `DatabaseDestination` record as JSON, such as:

```json
{
  "id": 1,
  "workspace_id": 1,
  "name": "Orders",
  "provider": "snowflake",
  "config": "example",
  "secret_id": 1,
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Database Destination ID.
* `workspace_id` (int64): Workspace ID. 0 means the default workspace.
* `name` (string): Name of the destination.
* `provider` (string): Database provider.
* `config` (object): Provider settings for the destination. Use the schema matching provider. The connection address and table are fixed after creation.
* `secret_id` (int64): ID of a Secret in the same Workspace. Use a Token Secret for Snowflake, a service account Key/Value Secret for BigQuery, or a Username/Password Secret for a database login.
* `created_at` (date-time): When the destination was created.
* `updated_at` (date-time): When the destination was last updated.

The functions below use the module's settings. Each is also a method of a client's
`client.database_destination` resource, such as
`client.database_destination.list(...)`,
which uses that client's configuration instead.


---

## List Database Destinations

```python
files_sdk.database_destination.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id` and `name`. Valid field combinations are `[ workspace_id, name ]`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.


---

## Show Database Destination

```python
files_sdk.database_destination.find(id)
```

### Parameters

* `id` (int64): Required - Database Destination ID.


---

## Create Database Destination

```python
files_sdk.database_destination.create({
  "name": "Orders",
  "provider": "snowflake",
  "config": {"account_identifier": "value", "database_name": "value", "schema_name": "value", "table_name": "value"},
  "secret_id": 1,
  "workspace_id": 1
})
```

### Parameters

* `name` (string): Required - Name of the destination.
* `provider` (string): Required - Database provider.
* `config` (object): Required - Provider settings for the destination. Use the schema matching provider. The connection address and table are fixed after creation.
* `secret_id` (int64): Required - ID of a Secret in the same Workspace. Use a Token Secret for Snowflake, a service account Key/Value Secret for BigQuery, or a Username/Password Secret for a database login.
* `workspace_id` (int64): Workspace ID. 0 means the default workspace.


---

## Update Database Destination

```python
files_sdk.database_destination.update(id, {
  "name": "Orders",
  "secret_id": 1,
  "config": {"account_identifier": "value", "database_name": "value", "schema_name": "value", "table_name": "value"}
})
```

### Parameters

* `id` (int64): Required - Database Destination ID.
* `name` (string): Name of the destination.
* `secret_id` (int64): ID of a Secret in the same Workspace. Use a Token Secret for Snowflake, a service account Key/Value Secret for BigQuery, or a Username/Password Secret for a database login.
* `config` (object): Provider settings for the destination. Use the schema matching provider. The connection address and table are fixed after creation.


---

## Delete Database Destination

```python
files_sdk.database_destination.delete(id)
```

### Parameters

* `id` (int64): Required - Database Destination ID.


---

## Update Database Destination

```python
database_destination = files_sdk.database_destination.find(id)
database_destination.update({
  "name": "Orders",
  "secret_id": 1,
  "config": {"account_identifier": "value", "database_name": "value", "schema_name": "value", "table_name": "value"}
})
```

### Parameters

* `id` (int64): Required - Database Destination ID.
* `name` (string): Name of the destination.
* `secret_id` (int64): ID of a Secret in the same Workspace. Use a Token Secret for Snowflake, a service account Key/Value Secret for BigQuery, or a Username/Password Secret for a database login.
* `config` (object): Provider settings for the destination. Use the schema matching provider. The connection address and table are fixed after creation.


---

## Delete Database Destination

```python
database_destination = files_sdk.database_destination.find(id)
database_destination.delete()
```

### Parameters

* `id` (int64): Required - Database Destination ID.
