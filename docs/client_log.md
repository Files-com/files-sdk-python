

---

## Append client log records

```
files_sdk.client_log.log({
  "identifier": "identifier",
  "body": "body"
})
```

### Parameters

* `identifier` (string): Required - Client log stream identifier
* `body` (string): Required - NDJSON log records
