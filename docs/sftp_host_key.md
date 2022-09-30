# SftpHostKey

## Example SftpHostKey Object

```
{
  "id": 1,
  "name": "example",
  "fingerprint_md5": "example",
  "fingerprint_sha256": "example"
}
```

* `id` (int64): Sftp Host Key ID
* `name` (string): The friendly name of this SFTP Host Key.
* `fingerprint_md5` (string): MD5 Fingerpint of the public key
* `fingerprint_sha256` (string): SHA256 Fingerpint of the public key
* `private_key` (string): The private key data.


---

## List Sftp Host Keys

```
files_sdk.sftp_host_key.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show Sftp Host Key

```
files_sdk.sftp_host_key.find(id)
```

### Parameters

* `id` (int64): Required - Sftp Host Key ID.


---

## Create Sftp Host Key

```
files_sdk.sftp_host_key.create({
  "name": "example"
})
```

### Parameters

* `name` (string): The friendly name of this SFTP Host Key.
* `private_key` (string): The private key data.


---

## Update Sftp Host Key

```
files_sdk.sftp_host_key.update(id, {
  "name": "example"
})
```

### Parameters

* `id` (int64): Required - Sftp Host Key ID.
* `name` (string): The friendly name of this SFTP Host Key.
* `private_key` (string): The private key data.


---

## Delete Sftp Host Key

```
files_sdk.sftp_host_key.delete(id)
```

### Parameters

* `id` (int64): Required - Sftp Host Key ID.


---

## Update Sftp Host Key

```
sftp_host_key = files_sdk.sftp_host_key.list.first
sftp_host_key.update({
  "name": "example"
})
```

### Parameters

* `id` (int64): Required - Sftp Host Key ID.
* `name` (string): The friendly name of this SFTP Host Key.
* `private_key` (string): The private key data.


---

## Delete Sftp Host Key

```
sftp_host_key = files_sdk.sftp_host_key.list.first
sftp_host_key.delete()
```

### Parameters

* `id` (int64): Required - Sftp Host Key ID.
