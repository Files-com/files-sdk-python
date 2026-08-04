# AgentNode

## Example AgentNode Object

```
{
  "node_id": "example",
  "name": "example",
  "hostname": "example",
  "availability_role": "example",
  "connection_status": "example",
  "is_default": True,
  "agent_version": "example",
  "direct_transfer_available": True,
  "last_seen_at": "2000-01-01T01:00:00Z"
}
```

* `node_id` (string): Stable Agent installation ID
* `name` (string): Customer-configured Agent node name
* `hostname` (string): Hostname reported by the Agent
* `availability_role` (string): Configured traffic preference
* `connection_status` (string): Whether this node is currently available for traffic
* `is_default` (boolean): Whether this node is the current default route for new unscoped work
* `agent_version` (string): Agent version reported by this node
* `direct_transfer_available` (boolean): Whether the proxy recently validated a direct connection to this Agent node. False means direct transfers are enabled but not currently available; null means disabled or unsupported.
* `last_seen_at` (date-time): Most recent successful node observation
