# Workspace

## Example Workspace Object

```
{
  "id": 1,
  "name": "Project Alpha"
}
```

* `id` (int64): Workspace ID
* `name` (string): Workspace name


---

## List Workspaces

```
files_sdk.workspace.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `name`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.


---

## Show Workspace

```
files_sdk.workspace.find(id)
```

### Parameters

* `id` (int64): Required - Workspace ID.


---

## Create Workspace

```
files_sdk.workspace.create({
  "name": "Project Alpha"
})
```

### Parameters

* `name` (string): Workspace name


---

## Update Workspace

```
files_sdk.workspace.update(id, {
  "name": "Project Alpha"
})
```

### Parameters

* `id` (int64): Required - Workspace ID.
* `name` (string): Workspace name


---

## Delete Workspace

```
files_sdk.workspace.delete(id)
```

### Parameters

* `id` (int64): Required - Workspace ID.


---

## Update Workspace

```
workspace = files_sdk.workspace.find(id)
workspace.update({
  "name": "Project Alpha"
})
```

### Parameters

* `id` (int64): Required - Workspace ID.
* `name` (string): Workspace name


---

## Delete Workspace

```
workspace = files_sdk.workspace.find(id)
workspace.delete()
```

### Parameters

* `id` (int64): Required - Workspace ID.
