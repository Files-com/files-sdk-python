# Warning

## Example Warning Object

```
{
  "warnings": [
    "Warning"
  ]
}
```

* `warnings` (array(object)): A list of warnings


---

## List warnings that apply to the current site

```
files_sdk.warning.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## List warnings that apply to the current site

```
files_sdk.warning.create_export()
```
