# Message

## Example Message Object

```
{
  "id": 1,
  "subject": "Files.com Account Upgrade",
  "body": "We should upgrade our Files.com account!",
  "comments": [
    null
  ]
}
```

* `id` (int64): Message ID
* `subject` (string): Message subject.
* `body` (string): Message body.
* `comments` (array): Comments.
* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `project_id` (int64): Project to which the message should be attached.


---

## List Messages

```
files_sdk.message.list({
  "user_id": 1,
  "per_page": 1,
  "project_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `project_id` (int64): Required - Project for which to return messages.


---

## Show Message

```
files_sdk.message.find(id)
```

### Parameters

* `id` (int64): Required - Message ID.


---

## Create Message

```
files_sdk.message.create({
  "user_id": 1,
  "project_id": 1,
  "subject": "Files.com Account Upgrade",
  "body": "We should upgrade our Files.com account!"
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `project_id` (int64): Required - Project to which the message should be attached.
* `subject` (string): Required - Message subject.
* `body` (string): Required - Message body.


---

## Update Message

```
files_sdk.message.update(id, {
  "project_id": 1,
  "subject": "Files.com Account Upgrade",
  "body": "We should upgrade our Files.com account!"
})
```

### Parameters

* `id` (int64): Required - Message ID.
* `project_id` (int64): Required - Project to which the message should be attached.
* `subject` (string): Required - Message subject.
* `body` (string): Required - Message body.


---

## Delete Message

```
files_sdk.message.delete(id)
```

### Parameters

* `id` (int64): Required - Message ID.


---

## Update Message

```
message = files_sdk.message.list.first
message.update({
  "project_id": 1,
  "subject": "Files.com Account Upgrade",
  "body": "We should upgrade our Files.com account!"
})
```

### Parameters

* `id` (int64): Required - Message ID.
* `project_id` (int64): Required - Project to which the message should be attached.
* `subject` (string): Required - Message subject.
* `body` (string): Required - Message body.


---

## Delete Message

```
message = files_sdk.message.list.first
message.delete()
```

### Parameters

* `id` (int64): Required - Message ID.
