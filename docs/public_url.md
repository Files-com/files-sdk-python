# PublicUrl

## Example PublicUrl Object

```
{
  "http-code": 1,
  "type": "not-found/file-not-found",
  "http_headers": "example",
  "body": "example",
  "download_uri": "example",
  "internal_download_uri": "example",
  "redirect": "example",
  "mime_type": "example",
  "site_id": 1,
  "remote_server_id": 1,
  "headers": {
    "key": "example value"
  },
  "socks_ips": [
    "example"
  ],
  "True_path": "example",
  "cache_for_seconds": 1
}
```

* `http-code` (int64): Response HTTP code
* `type` (string): A short string representing which error happened, if any
* `http_headers` (object): Headers to include with the response
* `body` (string): Body of the response, if a folder listing was requested
* `download_uri` (string): Signed URL allowing access to the requested file
* `internal_download_uri` (string): For use with internal services and should also be with headers and socks_ips
* `redirect` (string): URL where this request should be redirected, if necessary
* `mime_type` (string): Used for response content-type
* `site_id` (int64): Site id
* `remote_server_id` (int64): Used for internal bandwidth tracking
* `headers` (object): Used for internal url management
* `socks_ips` (array(string)): Used for internal url management
* `true_path` (string): The actual path of the file or folder being accessed. Used for caching.
* `cache_for_seconds` (int64): Indicates how long the response should be cached, in seconds.
* `hostname` (string): Hostname used to request the publicly shared resource.
* `path` (string): Path of the resource being requested.


---

## Fetch a public download URL for a publicly hosted resource

```
files_sdk.public_url.create(path, {
  "hostname": "hostname"
})
```

### Parameters

* `hostname` (string): Required - Hostname used to request the publicly shared resource.
* `path` (string): Required - Path of the resource being requested.
