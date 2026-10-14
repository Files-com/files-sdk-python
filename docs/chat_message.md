# ChatMessage

## Example ChatMessage Object

The API sends each `ChatMessage` record as JSON, such as:

```json
{
  "id": 1,
  "role": "example",
  "content": "example",
  "created_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Chat Message ID.
* `role` (string): Message role.
* `content` (string): Message content.
* `created_at` (date-time): Message creation date/time.
