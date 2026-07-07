# Revision

## Example Revision Object

```
{
  "current": "a1b2c3d4",
  "prior": "f9e8d7c6",
  "revision": "a1b2c3d4",
  "up_to_date": True
}
```

* `current` (string): The commit hash of the latest deployed revision.
* `prior` (string): The commit hash of the previously deployed revision.
* `revision` (string): The commit hash of the currently running revision.
* `up_to_date` (boolean): True if the currently running revision is the latest deployed revision.


---

## List Revisions

```
files_sdk.revision.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## Create an export CSV of Revision resources

```
files_sdk.revision.create_export()
```
