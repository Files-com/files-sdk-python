# MetadataCategory

## Example MetadataCategory Object

The API sends each `MetadataCategory` record as JSON, such as:

```json
{
  "id": 1,
  "name": "Approval Workflow",
  "definitions": {
    "Approval Status": [
      "Under Review",
      "Approved",
      "Rejected"
    ],
    "Reviewer": [

    ]
  },
  "default_columns": [
    "Approval Status"
  ]
}
```

* `id` (int64): Metadata Category ID
* `name` (string): Name of the metadata category.
* `definitions` (hash(string,array(string))): Map of key names to arrays of allowed values. An empty array means free-form text.
* `default_columns` (array(string)): Metadata keys that should appear as columns in the UI by default.

The functions below use the module's settings. Each is also a method of a client's
`client.metadata_category` resource, such as
`client.metadata_category.list(...)`,
which uses that client's configuration instead.


---

## List Metadata Categories

```python
files_sdk.metadata_category.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .


---

## Show Metadata Category

```python
files_sdk.metadata_category.find(id)
```

### Parameters

* `id` (int64): Required - Metadata Category ID.


---

## List Metadata Categories by Path

```python
files_sdk.metadata_category.list_for(path)
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `path` (string): Required - Path to operate on.


---

## Create Metadata Category

```python
files_sdk.metadata_category.create({
  "name": "Approval Workflow",
  "default_columns": ["Approval Status"]
})
```

### Parameters

* `name` (string): Required - Name of the metadata category.
* `default_columns` (array(string)): Metadata keys that should appear as columns in the UI by default.


---

## Update Metadata Category

```python
files_sdk.metadata_category.update(id, {
  "name": "Approval Workflow",
  "default_columns": ["Approval Status"]
})
```

### Parameters

* `id` (int64): Required - Metadata Category ID.
* `name` (string): Name of the metadata category.
* `default_columns` (array(string)): Metadata keys that should appear as columns in the UI by default.


---

## Delete Metadata Category

```python
files_sdk.metadata_category.delete(id)
```

### Parameters

* `id` (int64): Required - Metadata Category ID.


---

## Update Metadata Category

```python
metadata_category = files_sdk.metadata_category.find(id)
metadata_category.update({
  "name": "Approval Workflow",
  "default_columns": ["Approval Status"]
})
```

### Parameters

* `id` (int64): Required - Metadata Category ID.
* `name` (string): Name of the metadata category.
* `default_columns` (array(string)): Metadata keys that should appear as columns in the UI by default.


---

## Delete Metadata Category

```python
metadata_category = files_sdk.metadata_category.find(id)
metadata_category.delete()
```

### Parameters

* `id` (int64): Required - Metadata Category ID.
