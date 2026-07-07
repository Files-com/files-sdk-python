# AgentProxyIdentity

## Example AgentProxyIdentity Object

```
{
  "peer_id": "example",
  "endpoints": [
    {
      "multiaddr": "example"
    }
  ]
}
```

* `peer_id` (string): Libp2p peer ID for this identity candidate.
* `endpoints` (array(object)): Protocol-specific endpoints for this peer ID.


---

## Resolve Files Agent Proxy identities by public IPv4 address

```
files_sdk.agent_proxy_identity.lookup({
  "ips": "ips"
})
```

### Parameters

* `ips` (array(string)): Required - One or more public IPv4 addresses to resolve


---

## Report the currently active agent proxy peer ID for a proxy private IP

```
files_sdk.agent_proxy_identity.report({
  "private_ip": "private_ip",
  "peer_id": "peer_id"
})
```

### Parameters

* `private_ip` (string): Required - Proxy private IPv4 address
* `peer_id` (string): Required - Libp2p peer ID currently served by the proxy
