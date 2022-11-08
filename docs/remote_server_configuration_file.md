# RemoteServerConfigurationFile

## Example RemoteServerConfigurationFile Object

```
{
  "id": 1,
  "permission_set": "full",
  "api_token": "example",
  "root": "example",
  "port": 1,
  "hostname": "example",
  "public_key": "example",
  "private_key": "example",
  "status": "example",
  "config_version": "example"
}
```

* `id` (int64): Agent ID
* `permission_set` (string): 
* `api_token` (string): Files Agent API Token
* `root` (string): Agent local root path
* `port` (int64): Incoming port for files agent connections
* `hostname` (string): 
* `public_key` (string): public key
* `private_key` (string): private key
* `status` (string): either running or shutdown
* `config_version` (string): agent config version
