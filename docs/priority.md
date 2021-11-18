# Priority

## Example Priority Object

```
{
  "path": "foo/bar",
  "color": "pink"
}
```

* `path` (string): The path corresponding to the priority color This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `color` (string): The priority color


---

## List Priorities

```
files_sdk.priority.list(path, {
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `path` (string): Required - The path to query for priorities
