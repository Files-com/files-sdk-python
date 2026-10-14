# AgentPushUpdate

## Example AgentPushUpdate Object

The API sends each `AgentPushUpdate` record as JSON, such as:

```json
{
  "version": "example",
  "message": "example",
  "current_version": "example",
  "pending_version": "example",
  "last_error": "example",
  "error": "example"
}
```

* `version` (string): Pushed agent version
* `message` (string): Update accepted or reason
* `current_version` (string): Installed agent version
* `pending_version` (string): Pending agent version or null
* `last_error` (string): Last error message or null
* `error` (string): Error code
