# Session

## Example Session Object

```
{
  "id": "60525f92e859c4c3d74cb02fd176b1525901b525",
  "language": "en",
  "aws_secret_key": "example",
  "ai_assistant_personality_id": 1,
  "ai_assistant_personality_system_prompt": "example",
  "login_token": "@tok-randomcode",
  "login_token_domain": "https://mysite.files.com",
  "default_workspace_id": 1,
  "max_dir_listing_size": 1,
  "multiple_regions": True,
  "read_only": True,
  "root_path": "example",
  "home_path": "example",
  "sftp_insecure_ciphers": True,
  "site_id": 1,
  "ssl_required": True,
  "timeout_at": "2000-01-01T01:00:00Z",
  "trusted": True,
  "two_factor_setup_needed": True,
  "allowed_2fa_method_sms": True,
  "allowed_2fa_method_totp": True,
  "allowed_2fa_method_webauthn": True,
  "allowed_2fa_method_yubi": True,
  "calculate_file_checksums_crc32": True,
  "calculate_file_checksums_md5": True,
  "calculate_file_checksums_sha1": True,
  "calculate_file_checksums_sha256": True,
  "legacy_checksums_mode": True,
  "finalize_partial_uploads": True,
  "use_provided_modified_at": True,
  "windows_mode_ftp": True,
  "user_belongs_to_parent_site": True,
  "impersonator_user_id": 1
}
```

* `id` (string): Session ID
* `language` (string): Session language
* `aws_secret_key` (string): AWS Secret Key for validating AWS-style signatures in the Inbound S3 endpoint.
* `ai_assistant_personality_id` (int64): AI Assistant Personality ID for the in-app AI Assistant.
* `ai_assistant_personality_system_prompt` (string): System prompt for the in-app AI Assistant.
* `login_token` (string): Login token. If set, this token will allow your user to log in via browser at the domain in `login_token_domain`.
* `login_token_domain` (string): Domain to use with `login_token`.
* `default_workspace_id` (int64): Workspace ID the user should land in by default when more than one Workspace is available.
* `max_dir_listing_size` (int64): Maximum number of files to retrieve per folder for a directory listing.  This is based on the user's plan.
* `multiple_regions` (boolean): Can access multiple regions?
* `read_only` (boolean): Is this session read only?
* `root_path` (string): Root path to restrict the user's session to.
* `home_path` (string): Initial path to start the user's session in.
* `sftp_insecure_ciphers` (boolean): Are insecure SFTP ciphers allowed for this user? (If this is set to true, the site administrator has signaled that it is ok to use less secure SSH ciphers for this user.)
* `site_id` (int64): Site ID
* `ssl_required` (boolean): Is SSL required for this user?  (If so, ensure all your communications with this user use SSL.)
* `timeout_at` (date-time): Session timeout datetime
* `trusted` (boolean): Can this session tolerate IP and User-Agent mismatches?
* `two_factor_setup_needed` (boolean): If true, this user needs to add a Two Factor Authentication method before performing any further actions.
* `allowed_2fa_method_sms` (boolean): Sent only if 2FA setup is needed. Is SMS two factor authentication allowed?
* `allowed_2fa_method_totp` (boolean): Sent only if 2FA setup is needed. Is TOTP two factor authentication allowed?
* `allowed_2fa_method_webauthn` (boolean): Sent only if 2FA setup is needed. Is WebAuthn two factor authentication allowed?
* `allowed_2fa_method_yubi` (boolean): Sent only if 2FA setup is needed. Is Yubikey two factor authentication allowed?
* `calculate_file_checksums_crc32` (boolean): Calculate CRC32 checksum for incoming files?
* `calculate_file_checksums_md5` (boolean): Calculate MD5 checksum for incoming files?
* `calculate_file_checksums_sha1` (boolean): Calculate SHA1 checksum for incoming files?
* `calculate_file_checksums_sha256` (boolean): Calculate SHA256 checksum for incoming files?
* `legacy_checksums_mode` (boolean): Use legacy checksums mode?
* `finalize_partial_uploads` (boolean): Finalize partial SFTP uploads?
* `use_provided_modified_at` (boolean): Allow the user to provide file/folder modified at dates?  If false, the server will always use the current date/time.
* `windows_mode_ftp` (boolean): Does this user want to use Windows line-ending emulation?  (CR vs CRLF)
* `user_belongs_to_parent_site` (boolean): 
* `impersonator_user_id` (int64): User ID of the Site Admin who initiated a Read-Only session impersonating this session's user
* `username` (string): Username to sign in as
* `password` (string): Password for sign in
* `aws_access_key_id` (string): AWS Access Key ID for signing in with AWS credentials
* `change_password` (string): 
* `change_password_confirmation` (string): 
* `interface` (string): 
* `ssh_client_identification` (string): 
* `locale` (string): 
* `no_cookie` (boolean): 
* `oauth_provider` (string): 
* `oauth_label` (string): 
* `oauth_code` (string): 
* `oauth_state` (string): 
* `otp` (string): If this user has a 2FA device, provide its OTP or code here.
* `partial_session_id` (string): Identifier for a partially-completed login


---

## Create user session (log in)

```
files_sdk.session.create({
  "username": "username",
  "password": "password",
  "aws_access_key_id": "AKIAIOSFODNN7EXAMPLE",
  "no_cookie": False,
  "otp": "123456"
})
```

### Parameters

* `username` (string): Username to sign in as
* `password` (string): Password for sign in
* `aws_access_key_id` (string): AWS Access Key ID for signing in with AWS credentials
* `change_password` (string): 
* `change_password_confirmation` (string): 
* `interface` (string): 
* `ssh_client_identification` (string): 
* `locale` (string): 
* `no_cookie` (boolean): 
* `oauth_provider` (string): 
* `oauth_label` (string): 
* `oauth_code` (string): 
* `oauth_state` (string): 
* `otp` (string): If this user has a 2FA device, provide its OTP or code here.
* `partial_session_id` (string): Identifier for a partially-completed login


---

## Login the current user to a child site

```
files_sdk.session.subdomain({
  "subdomain": "child_site"
})
```

### Parameters

* `subdomain` (string): Required - Site subdomain to login to


---

## Site Admins only: Create a read-only session representing another user

```
files_sdk.session.as_user({
  "user_id": "2"
})
```

### Parameters

* `user_id` (string): Required - User id to login as


---

## Create trusted session from an existing session

```
files_sdk.session.trusted({
  "session_id": "60525f92e859c4c3d74cb02fd176b1525901b525"
})
```

### Parameters

* `session_id` (string): Required - Session ID to convert to a trusted session


---

## Reset password given a password reset code

```
files_sdk.session.forgot_reset({
  "code": "abc123",
  "password": "password",
  "confirm_password": "password",
  "interface": "web",
  "locale": "en",
  "otp": "123456"
})
```

### Parameters

* `code` (string): Required - 
* `password` (string): Required - 
* `confirm_password` (string): 
* `interface` (string): 
* `locale` (string): 
* `otp` (string): 


---

## Validate password reset code

```
files_sdk.session.forgot_validate({
  "code": "abc123"
})
```

### Parameters

* `code` (string): Required - 


---

## Initiate a password reset process given an email address or username

```
files_sdk.session.forgot({
  "email": "johndoe@gmail.com"
})
```

### Parameters

* `email` (string): 
* `username` (string): 
* `username_or_email` (string): 


---

## Create Public Hosting session pairing key

```
files_sdk.session.public_hosting({
  "return_to": "return_to"
})
```

### Parameters

* `return_to` (string): Required - Public Hosting URL to return to after authentication


---

## Create long lived session (API Key) from Pairing Key

```
files_sdk.session.pairing_key(key)
```

### Parameters

* `key` (string): Required - The pairing key to reserve for login.  Cannot be reused


---

## Begin new session via Oauth

```
files_sdk.session.oauth({
  "provider": "okta",
  "label": "My Corporate SSO Provider"
})
```

### Parameters

* `provider` (string): Required - 
* `label` (string): 
* `state` (string): 
* `host` (string): 


---

## Delete user session (log out)

```
files_sdk.session.delete()
```
