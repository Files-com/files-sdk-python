# SftpHostKey

## Example SftpHostKey Object

```
{
  "id": 1,
  "name": "My Key",
  "fingerprint_md5": "12:7e:f8:61:78:a4:b2:c2:ee:12:51:92:25:a7:42:cc",
  "fingerprint_sha256": "SHA256:5ANRkDpXWA+PgOquzZAG9RtQ1Bt8KXYAH2hecr7LQk8"
}
```

* `id` (int64): SFTP Host Key ID
* `name` (string): The friendly name of this SFTP Host Key.
* `fingerprint_md5` (string): MD5 Fingerprint of the public key
* `fingerprint_sha256` (string): SHA256 Fingerprint of the public key
* `private_key` (string): The private key data.


---

## List SFTP Host Keys

```
files_sdk.sftp_host_key.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show SFTP Host Key

```
files_sdk.sftp_host_key.find(id)
```

### Parameters

* `id` (int64): Required - Sftp Host Key ID.


---

## Create SFTP Host Key

```
files_sdk.sftp_host_key.create({
  "name": "My Key"
})
```

### Parameters

* `name` (string): The friendly name of this SFTP Host Key.
* `private_key` (string): The private key data.


---

## Update SFTP Host Key

```
files_sdk.sftp_host_key.update(id, {
  "name": "My Key"
})
```

### Parameters

* `id` (int64): Required - Sftp Host Key ID.
* `name` (string): The friendly name of this SFTP Host Key.
* `private_key` (string): The private key data.


---

## Delete SFTP Host Key

```
files_sdk.sftp_host_key.delete(id)
```

### Parameters

* `id` (int64): Required - Sftp Host Key ID.


---

## Update SFTP Host Key

```
sftp_host_key = files_sdk.sftp_host_key.find(id)
sftp_host_key.update({
  "name": "My Key"
})
```

### Parameters

* `id` (int64): Required - Sftp Host Key ID.
* `name` (string): The friendly name of this SFTP Host Key.
* `private_key` (string): The private key data.


---

## Delete SFTP Host Key

```
sftp_host_key = files_sdk.sftp_host_key.find(id)
sftp_host_key.delete()
```

### Parameters

* `id` (int64): Required - Sftp Host Key ID.
