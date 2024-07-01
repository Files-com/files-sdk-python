# MessageComment

## Example MessageComment Object

```
{
  "id": 1,
  "body": "What a great idea, thank you!",
  "reactions": [
    {
      "id": 1,
      "emoji": "👍"
    }
  ]
}
```

* `id` (int64): Message Comment ID
* `body` (string): Comment body.
* `reactions` (array(object)): Reactions to this comment.
* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.


---

## List Message Comments

```
files_sdk.message_comment.list({
  "user_id": 1,
  "per_page": 1,
  "page": 1,
  "message_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): 
* `page` (int64): 
* `message_id` (int64): Required - Message comment to return comments for.


---

## Show Message Comment

```
files_sdk.message_comment.find(id)
```

### Parameters

* `id` (int64): Required - Message Comment ID.


---

## Create Message Comment

```
files_sdk.message_comment.create({
  "user_id": 1,
  "body": "body"
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `body` (string): Required - Comment body.


---

## Update Message Comment

```
files_sdk.message_comment.update(id, {
  "body": "body"
})
```

### Parameters

* `id` (int64): Required - Message Comment ID.
* `body` (string): Required - Comment body.


---

## Delete Message Comment

```
files_sdk.message_comment.delete(id)
```

### Parameters

* `id` (int64): Required - Message Comment ID.


---

## Update Message Comment

```
message_comment = files_sdk.message_comment.find(id)
message_comment.update({
  "body": "body"
})
```

### Parameters

* `id` (int64): Required - Message Comment ID.
* `body` (string): Required - Comment body.


---

## Delete Message Comment

```
message_comment = files_sdk.message_comment.find(id)
message_comment.delete()
```

### Parameters

* `id` (int64): Required - Message Comment ID.
