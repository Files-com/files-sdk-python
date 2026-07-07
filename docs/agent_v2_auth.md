# AgentV2Auth

## Example AgentV2Auth Object

```
{
  "id": 1,
  "nonce": "example",
  "status": "example",
  "site_id": 1
}
```

* `id` (int64): Agent ID
* `nonce` (string): authentication nonce
* `status` (string): in_setup: waiting for signed_nonce, complete: authorization approved
* `site_id` (int64): Agent's site ID
