# FileComment

## Example FileComment Object

```
{
  "id": 1,
  "body": "What a great file!",
  "reactions": {
    "id": 1,
    "emoji": "👍"
  }
}
```

* `id` (int64): File Comment ID
* `body` (string): Comment body.
* `reactions`: Reactions to this comment.
* `path` (string): File path.


---

## List File Comments by path

```
files_sdk.file_comment.list_for(path, {
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
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
file_comment = files_sdk.file_comment.list_for(path).first

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
file_comment = files_sdk.file_comment.list_for(path).first

file_comment.delete()
```

### Parameters

* `id` (int64): Required - File Comment ID.
