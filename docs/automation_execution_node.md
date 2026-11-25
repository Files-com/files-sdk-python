# AutomationExecutionNode

## Example AutomationExecutionNode Object

The API sends each `AutomationExecutionNode` record as JSON, such as:

```json
{
  "node_id": "example",
  "node_type": "example",
  "status": "example",
  "run_stage": "example",
  "reused": true,
  "successful_operations": 1,
  "failed_operations": 1,
  "started_at": "2000-01-01T01:00:00Z",
  "completed_at": "2000-01-01T01:00:00Z",
  "duration_ms": 1,
  "inputs": [
    "example"
  ],
  "outputs": "example",
  "input_items": "example",
  "output_items": "example",
  "item_refs": [
    "example"
  ],
  "item_values": [
    "example"
  ]
}
```

* `node_id` (string): Node ID from the pinned Automation definition.
* `node_type` (string): Node type.
* `status` (string): Node status.
* `run_stage` (string): Current node execution stage.
* `reused` (boolean): Whether this node reused persisted output from an earlier run.
* `successful_operations` (int64): Count of successful operations in this node.
* `failed_operations` (int64): Count of failed operations in this node.
* `started_at` (date-time): When this node started.
* `completed_at` (date-time): When this node completed.
* `duration_ms` (int64): Node runtime in milliseconds.
* `inputs` (array(object)): Ordered inbound edge references.
* `outputs` (object): Output counts, item kinds, and typed-error summaries by outlet.
* `input_items` (object): Available input items grouped by inlet. Resolve large values with item_refs and item_values.
* `output_items` (object): Output items grouped by outlet. Resolve large values with item_refs and item_values.
* `item_refs` (array(object)): References with a path from the response root and a digest. Replace the null at each path with the value for that digest. Path segments are literal object keys or zero-based array indexes.
* `item_values` (array(object)): Ordered entries with a digest, a value, and optional item_refs relative to that value. References inside entries point to earlier entries in this array.
