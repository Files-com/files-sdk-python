# Session

## Example Session Object

```
{
  "id": "60525f92e859c4c3d74cb02fd176b1525901b525",
  "language": "en",
  "read_only": True,
  "sftp_insecure_ciphers": True
}
```

* `id` (string): Session ID
* `language` (string): Session language
* `read_only` (boolean): Is this session read only?
* `sftp_insecure_ciphers` (boolean): Are insecure SFTP ciphers allowed for this user? (If this is set to true, the site administrator has signaled that it is ok to use less secure SSH ciphers for this user.)
* `username` (string): Username to sign in as
* `password` (string): Password for sign in
* `otp` (string): If this user has a 2FA device, provide its OTP or code here.
* `partial_session_id` (string): Identifier for a partially-completed login


---

## Create user session (log in)

```
files_sdk.session.create({
  "username": "username",
  "password": "password",
  "otp": "123456"
})
```

### Parameters

* `username` (string): Username to sign in as
* `password` (string): Password for sign in
* `otp` (string): If this user has a 2FA device, provide its OTP or code here.
* `partial_session_id` (string): Identifier for a partially-completed login


---

## Delete user session (log out)

```
files_sdk.session.delete()
```
