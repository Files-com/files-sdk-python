# Session

## Example Session Object

```
{
  "id": "60525f92e859c4c3d74cb02fd176b1525901b525",
  "language": "en",
  "login_token": "@tok-randomcode",
  "login_token_domain": "https://mysite.files.com",
  "max_dir_listing_size": 1,
  "multiple_regions": True,
  "read_only": True,
  "root_path": "",
  "site_id": 1,
  "ssl_required": True,
  "tls_disabled": True,
  "two_factor_setup_needed": True,
  "allowed_2fa_method_sms": True,
  "allowed_2fa_method_totp": True,
  "allowed_2fa_method_u2f": True,
  "allowed_2fa_method_yubi": True,
  "use_provided_modified_at": True,
  "windows_mode_ftp": True
}
```

* `id` (string): Session ID
* `language` (string): Session language
* `login_token` (string): Login token. If set, this token will allow your user to log in via browser at the domain in `login_token_domain`.
* `login_token_domain` (string): Domain to use with `login_token`.
* `max_dir_listing_size` (int64): Maximum number of files to retrieve per folder for a directory listing.  This is based on the user's plan.
* `multiple_regions` (boolean): Can access multiple regions?
* `read_only` (boolean): Is this session read only?
* `root_path` (string): Initial root path to start the user's session in.
* `site_id` (int64): Site ID
* `ssl_required` (boolean): Is SSL required for this user?  (If so, ensure all your communications with this user use SSL.)
* `tls_disabled` (boolean): Is strong TLS disabled for this user? (If this is set to true, the site administrator has signaled that it is ok to use less secure TLS versions for this user.)
* `two_factor_setup_needed` (boolean): If true, this user needs to add a Two Factor Authentication method before performing any further actions.
* `allowed_2fa_method_sms` (boolean): Sent only if 2FA setup is needed. Is SMS two factor authentication allowed?
* `allowed_2fa_method_totp` (boolean): Sent only if 2FA setup is needed. Is TOTP two factor authentication allowed?
* `allowed_2fa_method_u2f` (boolean): Sent only if 2FA setup is needed. Is U2F two factor authentication allowed?
* `allowed_2fa_method_yubi` (boolean): Sent only if 2FA setup is needed. Is Yubikey two factor authentication allowed?
* `use_provided_modified_at` (boolean): Allow the user to provide file/folder modified at dates?  If false, the server will always use the current date/time.
* `windows_mode_ftp` (boolean): Does this user want to use Windows line-ending emulation?  (CR vs CRLF)
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
files_sdk.session.delete({
  "format": "",
  "session": ""
})
```

### Parameters

* `format` (string): 
* `session` (object): 
