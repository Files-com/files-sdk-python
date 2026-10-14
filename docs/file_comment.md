# FileComment

## Example FileComment Object

The API sends each `FileComment` record as JSON, such as:

```json
{
  "id": 1,
  "body": "What a great file!",
  "reactions": [
    {
      "id": 1,
      "emoji": "👍"
    }
  ]
}
```

* `id` (int64): File Comment ID
* `body` (string): Comment body.
* `reactions` (array(object)): Reactions to this comment.
* `path` (string): File path.

The functions below use the module's settings. Each is also a method of a client's
`client.file_comment` resource, such as
`client.file_comment.list_for(...)`,
which uses that client's configuration instead.


---

## List File Comments by Path

```python
files_sdk.file_comment.list_for(path)
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `path` (string): Required - Path to operate on.


---

## Create File Comment

```python
files_sdk.file_comment.create({
  "body": "What a great file!",
  "path": "path"
})
```

### Parameters

* `body` (string): Required - Comment body.
* `path` (string): Required - File path.


---

## Update File Comment

```python
files_sdk.file_comment.update(id, {
  "body": "What a great file!"
})
```

### Parameters

* `id` (int64): Required - File Comment ID.
* `body` (string): Required - Comment body.


---

## Delete File Comment

```python
files_sdk.file_comment.delete(id)
```

### Parameters

* `id` (int64): Required - File Comment ID.


---

## Update File Comment

```python
file_comment = next(files_sdk.file_comment.list_for(path).auto_paging_iter(), None)
if file_comment is not None:
    file_comment.update({
      "body": "What a great file!"
    })
```

### Parameters

* `id` (int64): Required - File Comment ID.
* `body` (string): Required - Comment body.


---

## Delete File Comment

```python
file_comment = next(files_sdk.file_comment.list_for(path).auto_paging_iter(), None)
if file_comment is not None:
    file_comment.delete()
```

### Parameters

* `id` (int64): Required - File Comment ID.
