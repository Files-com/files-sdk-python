# DirectConnectionInfo

## Example DirectConnectionInfo Object

```
{
  "version": 1,
  "server_name": "example",
  "addresses": [
    "example"
  ],
  "direct_uri": "example",
  "ca_pem": "example"
}
```

* `version` (int64): Direct connection information schema version.
* `server_name` (string): TLS server name (SNI and Host header) for the Agent's direct transfer listener.
* `addresses` (array(string)): Validated ip:port candidates that may be dialed over TCP+TLS for this transfer.
* `direct_uri` (string): Signed HTTPS URI for direct Agent transfer traffic.
* `ca_pem` (string): PEM-encoded CA certificate used to verify the Agent's direct transfer TLS certificate.
