# PublicKey

## Example PublicKey Object

```
{
  "id": 1,
  "title": "My public key",
  "created_at": "2000-01-01T01:00:00Z",
  "fingerprint": "43:51:43:a1:b5:fc:8b:b7:0a:3a:a9:b1:0f:66:73:a8",
  "fingerprint_sha256": "V5Q5t/ghT3R8Tol5GX9385bzmpygWVRnLuI9EXNrjCX",
  "status": "complete",
  "last_login_at": "2000-01-01T01:00:00Z",
  "private_key": "example",
  "public_key": "example",
  "username": "User",
  "user_id": 1
}
```

* `id` (int64): Public key ID
* `title` (string): Public key title
* `created_at` (date-time): Public key created at date/time
* `fingerprint` (string): Public key fingerprint (MD5)
* `fingerprint_sha256` (string): Public key fingerprint (SHA256)
* `status` (string): Can be invalid, not_generated, generating, complete
* `last_login_at` (date-time): Key's most recent login time via SFTP
* `private_key` (string): Private key generated for the user.
* `public_key` (string): Public key generated for the user.
* `username` (string): Username of the user this public key is associated with
* `user_id` (int64): User ID this public key is associated with
* `generate_keypair` (boolean): If true, generate a new SSH key pair. Can not be used with `public_key`
* `generate_private_key_password` (string): Password for the private key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
* `generate_algorithm` (string): Type of key to generate.  One of rsa, dsa, ecdsa, ed25519. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
* `generate_length` (int64): Length of key to generate. If algorithm is ecdsa, this is the signature size. Used for the generation of the key. Will be ignored if `generate_keypair` is false.


---

## List Public Keys

```
files_sdk.public_key.list({
  "user_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.


---

## Show Public Key

```
files_sdk.public_key.find(id)
```

### Parameters

* `id` (int64): Required - Public Key ID.


---

## Create Public Key

```
files_sdk.public_key.create({
  "user_id": 1,
  "title": "My Main Key",
  "public_key": "example",
  "generate_keypair": False,
  "generate_private_key_password": "[your private key password]",
  "generate_algorithm": "rsa",
  "generate_length": 4096
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `title` (string): Required - Internal reference for key.
* `public_key` (string): Actual contents of SSH key.
* `generate_keypair` (boolean): If true, generate a new SSH key pair. Can not be used with `public_key`
* `generate_private_key_password` (string): Password for the private key. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
* `generate_algorithm` (string): Type of key to generate.  One of rsa, dsa, ecdsa, ed25519. Used for the generation of the key. Will be ignored if `generate_keypair` is false.
* `generate_length` (int64): Length of key to generate. If algorithm is ecdsa, this is the signature size. Used for the generation of the key. Will be ignored if `generate_keypair` is false.


---

## Update Public Key

```
files_sdk.public_key.update(id, {
  "title": "My Main Key"
})
```

### Parameters

* `id` (int64): Required - Public Key ID.
* `title` (string): Required - Internal reference for key.


---

## Delete Public Key

```
files_sdk.public_key.delete(id)
```

### Parameters

* `id` (int64): Required - Public Key ID.


---

## Update Public Key

```
public_key = files_sdk.public_key.find(id)
public_key.update({
  "title": "My Main Key"
})
```

### Parameters

* `id` (int64): Required - Public Key ID.
* `title` (string): Required - Internal reference for key.


---

## Delete Public Key

```
public_key = files_sdk.public_key.find(id)
public_key.delete()
```

### Parameters

* `id` (int64): Required - Public Key ID.
