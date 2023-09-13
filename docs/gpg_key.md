# GpgKey

## Example GpgKey Object

```
{
  "id": 1,
  "expires_at": "2000-01-01T01:00:00Z",
  "name": "key name",
  "user_id": 1,
  "public_key": "7f8bc1210b09b9ddf469e6b6b8920e76",
  "private_key": "ab236cfe4a195f0226bc2e674afdd6b0",
  "private_key_password": "[your GPG private key password]"
}
```

* `id` (int64): Your GPG key ID.
* `expires_at` (date-time): Your GPG key expiration date.
* `name` (string): Your GPG key name.
* `user_id` (int64): GPG owner's user id
* `public_key` (string): Your GPG public key
* `private_key` (string): Your GPG private key.
* `private_key_password` (string): Your GPG private key password. Only required for password protected keys.


---

## List Gpg Keys

```
files_sdk.gpg_key.list({
  "user_id": 1,
  "per_page": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[name]=desc`). Valid fields are `name` and `expires_at`.


---

## Show Gpg Key

```
files_sdk.gpg_key.find(id)
```

### Parameters

* `id` (int64): Required - Gpg Key ID.


---

## Create Gpg Key

```
files_sdk.gpg_key.create({
  "user_id": 1,
  "public_key": "7f8bc1210b09b9ddf469e6b6b8920e76",
  "private_key": "ab236cfe4a195f0226bc2e674afdd6b0",
  "private_key_password": "[your GPG private key password]",
  "name": "key name"
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `public_key` (string): Your GPG public key
* `private_key` (string): Your GPG private key.
* `private_key_password` (string): Your GPG private key password. Only required for password protected keys.
* `name` (string): Required - Your GPG key name.


---

## Update Gpg Key

```
files_sdk.gpg_key.update(id, {
  "public_key": "7f8bc1210b09b9ddf469e6b6b8920e76",
  "private_key": "ab236cfe4a195f0226bc2e674afdd6b0",
  "private_key_password": "[your GPG private key password]",
  "name": "key name"
})
```

### Parameters

* `id` (int64): Required - Gpg Key ID.
* `public_key` (string): Your GPG public key
* `private_key` (string): Your GPG private key.
* `private_key_password` (string): Your GPG private key password. Only required for password protected keys.
* `name` (string): Your GPG key name.


---

## Delete Gpg Key

```
files_sdk.gpg_key.delete(id)
```

### Parameters

* `id` (int64): Required - Gpg Key ID.


---

## Update Gpg Key

```
gpg_key = files_sdk.gpg_key.list.first
gpg_key.update({
  "public_key": "7f8bc1210b09b9ddf469e6b6b8920e76",
  "private_key": "ab236cfe4a195f0226bc2e674afdd6b0",
  "private_key_password": "[your GPG private key password]",
  "name": "key name"
})
```

### Parameters

* `id` (int64): Required - Gpg Key ID.
* `public_key` (string): Your GPG public key
* `private_key` (string): Your GPG private key.
* `private_key_password` (string): Your GPG private key password. Only required for password protected keys.
* `name` (string): Your GPG key name.


---

## Delete Gpg Key

```
gpg_key = files_sdk.gpg_key.list.first
gpg_key.delete()
```

### Parameters

* `id` (int64): Required - Gpg Key ID.
