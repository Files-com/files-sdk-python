# GpgKey

## Example GpgKey Object

```
{
  "id": 1,
  "expires_at": "2000-01-01T01:00:00Z",
  "name": "key name",
  "user_id": 1,
  "public_key_md5": "7f8bc1210b09b9ddf469e6b6b8920e76",
  "private_key_md5": "ab236cfe4a195f0226bc2e674afdd6b0",
  "generated_public_key": "7f8bc1210b09b9ddf469e6b6b8920e76",
  "generated_private_key": "ab236cfe4a195f0226bc2e674afdd6b0",
  "private_key_password_md5": "[your GPG private key password]"
}
```

* `id` (int64): Your GPG key ID.
* `expires_at` (date-time): Your GPG key expiration date.
* `name` (string): Your GPG key name.
* `user_id` (int64): GPG owner's user id
* `public_key_md5` (string): MD5 hash of your GPG public key
* `private_key_md5` (string): MD5 hash of your GPG private key.
* `generated_public_key` (string): Your GPG public key
* `generated_private_key` (string): Your GPG private key.
* `private_key_password_md5` (string): Your GPG private key password. Only required for password protected keys.
* `public_key` (string): MD5 hash of your GPG public key
* `private_key` (string): MD5 hash of your GPG private key.
* `private_key_password` (string): Your GPG private key password. Only required for password protected keys.
* `generate_expires_at` (string): Expiration date of the key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
* `generate_keypair` (boolean): If true, generate a new GPG key pair. Can not be used with `public_key`/`private_key`
* `generate_full_name` (string): Full name of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
* `generate_email` (string): Email address of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.


---

## List GPG Keys

```
files_sdk.gpg_key.list({
  "user_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name` and `expires_at`.


---

## Show GPG Key

```
files_sdk.gpg_key.find(id)
```

### Parameters

* `id` (int64): Required - Gpg Key ID.


---

## Create GPG Key

```
files_sdk.gpg_key.create({
  "user_id": 1,
  "public_key": "7f8bc1210b09b9ddf469e6b6b8920e76",
  "private_key": "ab236cfe4a195f0226bc2e674afdd6b0",
  "private_key_password": "[your GPG private key password]",
  "name": "key name",
  "generate_expires_at": "2025-06-19 12:00:00",
  "generate_keypair": False,
  "generate_full_name": "John Doe",
  "generate_email": "jdoe@example.com"
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `public_key` (string): MD5 hash of your GPG public key
* `private_key` (string): MD5 hash of your GPG private key.
* `private_key_password` (string): Your GPG private key password. Only required for password protected keys.
* `name` (string): Required - Your GPG key name.
* `generate_expires_at` (string): Expiration date of the key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
* `generate_keypair` (boolean): If true, generate a new GPG key pair. Can not be used with `public_key`/`private_key`
* `generate_full_name` (string): Full name of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
* `generate_email` (string): Email address of the key owner. Used for the generation of the key. Will be ignored if `generate_keypair` is false.


---

## Update GPG Key

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
* `public_key` (string): MD5 hash of your GPG public key
* `private_key` (string): MD5 hash of your GPG private key.
* `private_key_password` (string): Your GPG private key password. Only required for password protected keys.
* `name` (string): Your GPG key name.


---

## Delete GPG Key

```
files_sdk.gpg_key.delete(id)
```

### Parameters

* `id` (int64): Required - Gpg Key ID.


---

## Update GPG Key

```
gpg_key = files_sdk.gpg_key.find(id)
gpg_key.update({
  "public_key": "7f8bc1210b09b9ddf469e6b6b8920e76",
  "private_key": "ab236cfe4a195f0226bc2e674afdd6b0",
  "private_key_password": "[your GPG private key password]",
  "name": "key name"
})
```

### Parameters

* `id` (int64): Required - Gpg Key ID.
* `public_key` (string): MD5 hash of your GPG public key
* `private_key` (string): MD5 hash of your GPG private key.
* `private_key_password` (string): Your GPG private key password. Only required for password protected keys.
* `name` (string): Your GPG key name.


---

## Delete GPG Key

```
gpg_key = files_sdk.gpg_key.find(id)
gpg_key.delete()
```

### Parameters

* `id` (int64): Required - Gpg Key ID.
