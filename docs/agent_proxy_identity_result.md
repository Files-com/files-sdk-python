# AgentProxyIdentityResult

## Example AgentProxyIdentityResult Object

```
{
  "ip": "example",
  "status": "example",
  "identities": [
    {
      "peer_id": "example",
      "endpoints": [
        {
          "multiaddr": "example"
        }
      ]
    }
  ]
}
```

* `ip` (string): Requested public IPv4 address.
* `status` (string): Lookup status for the requested IP.
* `identities` (array(object)): Ordered identity candidates for this IP during rotation.
