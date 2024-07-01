# FileComment

## Example FileComment Object

```
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


---

## List File Comments by path

```
files_sdk.file_comment.list_for(path, {
  "per_page": 1,
  "page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): 
* `page` (int64): 
* `path` (string): Required - Path to operate on.


---

## Create File Comment

```
files_sdk.file_comment.create({
  "body": "body",
  "path": "path"
})
```

### Parameters

* `body` (string): Required - Comment body.
* `path` (string): Required - File path.


---

## Update File Comment

```
files_sdk.file_comment.update(id, {
  "body": "body"
})
```

### Parameters

* `id` (int64): Required - File Comment ID.
* `body` (string): Required - Comment body.


---

## Delete File Comment

```
files_sdk.file_comment.delete(id)
```

### Parameters

* `id` (int64): Required - File Comment ID.


---

## Update File Comment

```
file_comment = files_sdk.file_comment.list.first
file_comment.update({
  "body": "body"
})
```

### Parameters

* `id` (int64): Required - File Comment ID.
* `body` (string): Required - Comment body.


---

## Delete File Comment

```
file_comment = files_sdk.file_comment.list.first
file_comment.delete()
```

### Parameters

* `id` (int64): Required - File Comment ID.
