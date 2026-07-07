# TwoFactorAuthenticationMethod

## Example TwoFactorAuthenticationMethod Object

```
{
  "id": 1,
  "name": "My Verizon Phone",
  "method_type": "sms",
  "phone_number": "+15555555555",
  "phone_number_country": "US",
  "phone_number_national_format": "+15555555555",
  "secret_tokens": [
    "example"
  ],
  "setup_expired": True,
  "setup_complete": True,
  "setup_expires_at": "2000-01-01T01:00:00Z",
  "totp_provisioning_uri": "https://...",
  "webauthn_registration_options": {
    "key": "example value"
  },
  "bypass_for_ftp_sftp_dav": True
}
```

* `id` (int64): 2fa ID
* `name` (string): 2fa method name
* `method_type` (string): Type of 2fa
* `phone_number` (string): 2fa phone number (if SMS)
* `phone_number_country` (string): 2fa phone number country (if SMS)
* `phone_number_national_format` (string): 2fa phone number national format (if SMS)
* `secret_tokens` (array(string)): For the Static method type, this is the list of tokens which can be used
* `setup_expired` (boolean): 2fa setup expired?
* `setup_complete` (boolean): 2fa setup complete?
* `setup_expires_at` (date-time): 2fa setup expires at this date/time (typically 10 minutes after a new method is created)
* `totp_provisioning_uri` (string): TOTP provisioning URI (if TOTP)
* `webauthn_registration_options` (object): WebAuthn / FIDO 2 registration options (if WebAuthn)
* `bypass_for_ftp_sftp_dav` (boolean): Set true to skip checking this 2FA method when using FTP, SFTP, and DAV
* `otp` (string): Current value of OTP, Yubikey string, or Webauthn response value.


---

## List current user's 2FA methods

```
files_sdk.two_factor_authentication_method.get()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## Create 2FA method on current user

```
files_sdk.two_factor_authentication_method.create({
  "method_type": "sms",
  "name": "My Verizon Phone",
  "phone_number": "+15555555555",
  "bypass_for_ftp_sftp_dav": False
})
```

### Parameters

* `method_type` (string): Required - Type of 2fa
* `name` (string): 2fa method name
* `phone_number` (string): 2fa phone number (if SMS)
* `bypass_for_ftp_sftp_dav` (boolean): Set true to skip checking this 2FA method when using FTP, SFTP, and DAV


---

## Generate (and send if applicable) a one time password for current user's primary 2FA method

```
files_sdk.two_factor_authentication_method.send_code({
  "webauthn_only": False
})
```

### Parameters

* `webauthn_only` (boolean): Set to `true` to only generate an OTP for Webauthn keys and skip things like SMS.


---

## List current user's 2FA methods

```
files_sdk.two_factor_authentication_method.create_export()
```


---

## Update 2fa

```
files_sdk.two_factor_authentication_method.update(id, {
  "otp": "123456",
  "name": "My Verizon Phone",
  "bypass_for_ftp_sftp_dav": False
})
```

### Parameters

* `id` (int64): Required - 2fa ID.
* `otp` (string): Current value of OTP, Yubikey string, or Webauthn response value.
* `name` (string): 2fa method name
* `bypass_for_ftp_sftp_dav` (boolean): Set true to skip checking this 2FA method when using FTP, SFTP, and DAV


---

## Delete 2fa

```
files_sdk.two_factor_authentication_method.delete(id)
```

### Parameters

* `id` (int64): Required - 2fa ID.


---

## Update 2fa

```
two_factor_authentication_method = files_sdk.two_factor_authentication_method.find(id)
two_factor_authentication_method.update({
  "otp": "123456",
  "name": "My Verizon Phone",
  "bypass_for_ftp_sftp_dav": False
})
```

### Parameters

* `id` (int64): Required - 2fa ID.
* `otp` (string): Current value of OTP, Yubikey string, or Webauthn response value.
* `name` (string): 2fa method name
* `bypass_for_ftp_sftp_dav` (boolean): Set true to skip checking this 2FA method when using FTP, SFTP, and DAV


---

## Delete 2fa

```
two_factor_authentication_method = files_sdk.two_factor_authentication_method.find(id)
two_factor_authentication_method.delete()
```

### Parameters

* `id` (int64): Required - 2fa ID.
