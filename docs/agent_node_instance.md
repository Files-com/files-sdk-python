# AgentNodeInstance

## Example AgentNodeInstance Object

```
{
  "instance_id": "example",
  "process_state": "example",
  "status": "example",
  "is_default": True,
  "agent_version": "example",
  "last_seen_at": "2000-01-01T01:00:00Z",
  "connections": [
    {
      "mode": "example",
      "status": "example",
      "last_seen_at": "2000-01-01T01:00:00Z"
    }
  ]
}
```

* `instance_id` (string): Ephemeral ID for this running Agent process
* `process_state` (string): Role of this process during an Agent update
* `status` (string): Whether this process has an available proxy connection
* `is_default` (boolean): Whether this process receives new unscoped work for its node
* `agent_version` (string): Agent version reported by this process
* `last_seen_at` (date-time): Most recent successful observation for this process
* `connections` (array(object)): Proxy connections observed for this process
