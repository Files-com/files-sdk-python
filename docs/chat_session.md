# ChatSession

## Example ChatSession Object

```
{
  "id": "example",
  "user_id": 1,
  "ai_task_id": 1,
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
* `ai_task_id` (int64): AI Task ID. Present when the conversation was started by an AI Task.
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
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `ai_task_id`, `user_id` or `workspace_id`.


---

## Show Chat Session

```
files_sdk.chat_session.find(id)
```

### Parameters

* `id` (string): Required - Chat Session ID.


---

## Create an export CSV of Chat Session resources

```
files_sdk.chat_session.create_export()
```

### Parameters

* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `ai_task_id`, `user_id` or `workspace_id`.
