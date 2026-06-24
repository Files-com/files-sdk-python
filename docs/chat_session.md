# ChatSession

## Example ChatSession Object

```
{
  "id": "example",
  "user_id": 1,
  "workspace_id": 1,
  "last_active_at": "2000-01-01T01:00:00Z",
  "created_at": "2000-01-01T01:00:00Z",
  "messages": [
    {
      "id": 1,
      "role": "example",
      "content": "example",
      "created_at": "2000-01-01T01:00:00Z"
    }
  ]
}
```

* `id` (string): Chat Session ID.
* `user_id` (int64): User ID.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.
* `last_active_at` (date-time): Most recent chat activity date/time.
* `created_at` (date-time): Chat session creation date/time.
* `messages` (array(object)): Visible conversation messages in this chat session. For performance reasons, this is not provided when listing chat sessions.


---

## List Chat Sessions

```
files_sdk.chat_session.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## Show Chat Session

```
files_sdk.chat_session.find(id)
```

### Parameters

* `id` (string): Required - Chat Session ID.
