# AutomationAuthoringSchema

## Example AutomationAuthoringSchema Object

The API sends each `AutomationAuthoringSchema` record as JSON, such as:

```json
{
  "definition_schema": "example",
  "error_families": [
    "example"
  ],
  "nodes": [
    "example"
  ],
  "schema_url": "example"
}
```

* `definition_schema` (object): JSON Schema for active Automation v2 graph definitions.
* `error_families` (array(object)): Typed error families accepted by Automation v2 on_error rules.
* `nodes` (array(object)): Active Automation v2 node authoring metadata.
* `schema_url` (string): Stable public URL for the Automation v2 graph definition JSON Schema.
