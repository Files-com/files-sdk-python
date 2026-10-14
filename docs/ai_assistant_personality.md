# AiAssistantPersonality

## Example AiAssistantPersonality Object

The API sends each `AiAssistantPersonality` record as JSON, such as:

```json
{
  "id": 1,
  "workspace_id": 1,
  "name": "Concise Assistant",
  "system_prompt": "Respond as a concise operations assistant.",
  "use_by_default": false,
  "apply_to_all_workspaces": false,
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): AI Assistant Personality ID.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.
* `name` (string): AI Assistant Personality name.
* `system_prompt` (string): System prompt injected into the in-app AI Assistant.
* `use_by_default` (boolean): Whether this personality is the default personality for the Workspace.
* `apply_to_all_workspaces` (boolean): If true, this default-workspace personality can apply to users in all workspaces.
* `created_at` (date-time): Creation time.
* `updated_at` (date-time): Last update time.

The functions below use the module's settings. Each is also a method of a client's
`client.ai_assistant_personality` resource, such as
`client.ai_assistant_personality.list(...)`,
which uses that client's configuration instead.


---

## List Ai Assistant Personalities

```python
files_sdk.ai_assistant_personality.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.


---

## Show Ai Assistant Personality

```python
files_sdk.ai_assistant_personality.find(id)
```

### Parameters

* `id` (int64): Required - Ai Assistant Personality ID.


---

## Create Ai Assistant Personality

```python
files_sdk.ai_assistant_personality.create({
  "apply_to_all_workspaces": False,
  "name": "Concise Assistant",
  "system_prompt": "Respond as a concise operations assistant.",
  "use_by_default": False,
  "workspace_id": 0
})
```

### Parameters

* `apply_to_all_workspaces` (boolean): If true, this default-workspace personality can apply to users in all workspaces.
* `name` (string): Required - AI Assistant Personality name.
* `system_prompt` (string): Required - System prompt injected into the in-app AI Assistant.
* `use_by_default` (boolean): Whether this personality is the default personality for the Workspace.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Update Ai Assistant Personality

```python
files_sdk.ai_assistant_personality.update(id, {
  "apply_to_all_workspaces": False,
  "name": "Concise Assistant",
  "system_prompt": "Respond as a concise operations assistant.",
  "use_by_default": False,
  "workspace_id": 0
})
```

### Parameters

* `id` (int64): Required - Ai Assistant Personality ID.
* `apply_to_all_workspaces` (boolean): If true, this default-workspace personality can apply to users in all workspaces.
* `name` (string): AI Assistant Personality name.
* `system_prompt` (string): System prompt injected into the in-app AI Assistant.
* `use_by_default` (boolean): Whether this personality is the default personality for the Workspace.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Delete Ai Assistant Personality

```python
files_sdk.ai_assistant_personality.delete(id)
```

### Parameters

* `id` (int64): Required - Ai Assistant Personality ID.


---

## Update Ai Assistant Personality

```python
ai_assistant_personality = files_sdk.ai_assistant_personality.find(id)
ai_assistant_personality.update({
  "apply_to_all_workspaces": False,
  "name": "Concise Assistant",
  "system_prompt": "Respond as a concise operations assistant.",
  "use_by_default": False,
  "workspace_id": 0
})
```

### Parameters

* `id` (int64): Required - Ai Assistant Personality ID.
* `apply_to_all_workspaces` (boolean): If true, this default-workspace personality can apply to users in all workspaces.
* `name` (string): AI Assistant Personality name.
* `system_prompt` (string): System prompt injected into the in-app AI Assistant.
* `use_by_default` (boolean): Whether this personality is the default personality for the Workspace.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Delete Ai Assistant Personality

```python
ai_assistant_personality = files_sdk.ai_assistant_personality.find(id)
ai_assistant_personality.delete()
```

### Parameters

* `id` (int64): Required - Ai Assistant Personality ID.
