# User

## Example User Object

```
{
  "id": 1,
  "username": "user",
  "admin_group_ids": [

  ],
  "allowed_ips": "127.0.0.1",
  "attachments_permission": True,
  "api_keys_count": 1,
  "authenticate_until": "2000-01-01T01:00:00Z",
  "authentication_method": "password",
  "avatar_url": "",
  "billing_permission": True,
  "bypass_site_allowed_ips": True,
  "bypass_inactive_disable": True,
  "created_at": "2000-01-01T01:00:00Z",
  "dav_permission": True,
  "disabled": True,
  "email": "john.doe@files.com",
  "ftp_permission": True,
  "group_ids": "",
  "header_text": "User-specific message.",
  "language": "en",
  "last_login_at": "2000-01-01T01:00:00Z",
  "last_protocol_cipher": "",
  "lockout_expires": "2000-01-01T01:00:00Z",
  "name": "John Doe",
  "company": "ACME Corp.",
  "notes": "Internal notes on this user.",
  "notification_daily_send_time": 18,
  "office_integration_enabled": True,
  "password_set_at": "2000-01-01T01:00:00Z",
  "password_validity_days": 1,
  "public_keys_count": 1,
  "receive_admin_alerts": True,
  "require_2fa": "always_require",
  "active_2fa": True,
  "require_password_change": True,
  "restapi_permission": True,
  "self_managed": True,
  "sftp_permission": True,
  "site_admin": True,
  "skip_welcome_screen": True,
  "ssl_required": "always_require",
  "sso_strategy_id": 1,
  "subscribe_to_newsletter": True,
  "externally_managed": True,
  "time_zone": "Pacific Time (US & Canada)",
  "type_of_2fa": "",
  "user_root": ""
}
```

* `id` (int64): User ID
* `username` (string): User's username
* `admin_group_ids` (array): List of group IDs of which this user is an administrator
* `allowed_ips` (string): A list of allowed IPs if applicable.  Newline delimited
* `attachments_permission` (boolean): Can the user create Bundles (aka Share Links)?  This field will be aliased or renamed in the future to `bundles_permission`.
* `api_keys_count` (int64): Number of api keys associated with this user
* `authenticate_until` (date-time): Scheduled Date/Time at which user will be deactivated
* `authentication_method` (string): How is this user authenticated?
* `avatar_url` (string): URL holding the user's avatar
* `billing_permission` (boolean): Allow this user to perform operations on the account, payments, and invoices?
* `bypass_site_allowed_ips` (boolean): Allow this user to skip site-wide IP blacklists?
* `bypass_inactive_disable` (boolean): Exempt this user from being disabled based on inactivity?
* `created_at` (date-time): When this user was created
* `dav_permission` (boolean): Can the user connect with WebDAV?
* `disabled` (boolean): Is user disabled? Disabled users cannot log in, and do not count for billing purposes.  Users can be automatically disabled after an inactivity period via a Site setting.
* `email` (email): User email address
* `ftp_permission` (boolean): Can the user access with FTP/FTPS?
* `group_ids` (string): Comma-separated list of group IDs of which this user is a member
* `header_text` (string): Text to display to the user in the header of the UI
* `language` (string): Preferred language
* `last_login_at` (date-time): User's last login time
* `last_protocol_cipher` (string): The last protocol and cipher used
* `lockout_expires` (date-time): Time in the future that the user will no longer be locked out if applicable
* `name` (string): User's full name
* `company` (string): User's company
* `notes` (string): Any internal notes on the user
* `notification_daily_send_time` (int64): Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
* `office_integration_enabled` (boolean): Enable integration with Office for the web?
* `password_set_at` (date-time): Last time the user's password was set
* `password_validity_days` (int64): Number of days to allow user to use the same password
* `public_keys_count` (int64): Number of public keys associated with this user
* `receive_admin_alerts` (boolean): Should the user receive admin alerts such a certificate expiration notifications and overages?
* `require_2fa` (string): 2FA required setting
* `active_2fa` (boolean): Is 2fa active for the user?
* `require_password_change` (boolean): Is a password change required upon next user login?
* `restapi_permission` (boolean): Can this user access the REST API?
* `self_managed` (boolean): Does this user manage it's own credentials or is it a shared/bot user?
* `sftp_permission` (boolean): Can the user access with SFTP?
* `site_admin` (boolean): Is the user an administrator for this site?
* `skip_welcome_screen` (boolean): Skip Welcome page in the UI?
* `ssl_required` (string): SSL required setting
* `sso_strategy_id` (int64): SSO (Single Sign On) strategy ID for the user, if applicable.
* `subscribe_to_newsletter` (boolean): Is the user subscribed to the newsletter?
* `externally_managed` (boolean): Is this user managed by a SsoStrategy?
* `time_zone` (string): User time zone
* `type_of_2fa` (string): Type(s) of 2FA methods in use.  Will be either `sms`, `totp`, `u2f`, `yubi`, or multiple values sorted alphabetically and joined by an underscore.
* `user_root` (string): Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set.)  Note that this is not used for API, Desktop, or Web interface.
* `avatar_file` (file): An image file for your user avatar.
* `avatar_delete` (boolean): If true, the avatar will be deleted.
* `change_password` (string): Used for changing a password on an existing user.
* `change_password_confirmation` (string): Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
* `grant_permission` (string): Permission to grant on the user root.  Can be blank or `full`, `read`, `write`, `list`, or `history`.
* `group_id` (int64): Group ID to associate this user with.
* `password` (string): User password.
* `password_confirmation` (string): Optional, but if provided, we will ensure that it matches the value sent in `password`.
* `announcements_read` (boolean): Signifies that the user has read all the announcements in the UI.


---

## List Users

```
files_sdk.user.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `active`, `master_admin`, `site_id`, `authenticate_until`, `email`, `last_desktop_login_at`, `last_login_at`, `username`, `company`, `name`, `notes`, `site_admin`, `receive_admin_alerts`, `allowed_ips`, `password_validity_days`, `ssl_required` or `not_site_admin`.
* `filter` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `username`, `email`, `company`, `notes`, `site_admin`, `allowed_ips`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until` or `not_site_admin`.
* `filter_gt` (object): If set, return records where the specifiied field is greater than the supplied value. Valid fields are `username`, `email`, `company`, `notes`, `site_admin`, `allowed_ips`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until` or `not_site_admin`.
* `filter_gteq` (object): If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `username`, `email`, `company`, `notes`, `site_admin`, `allowed_ips`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until` or `not_site_admin`.
* `filter_like` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `username`, `email`, `company`, `notes`, `site_admin`, `allowed_ips`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until` or `not_site_admin`.
* `filter_lt` (object): If set, return records where the specifiied field is less than the supplied value. Valid fields are `username`, `email`, `company`, `notes`, `site_admin`, `allowed_ips`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until` or `not_site_admin`.
* `filter_lteq` (object): If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `username`, `email`, `company`, `notes`, `site_admin`, `allowed_ips`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until` or `not_site_admin`.
* `ids` (string): comma-separated list of User IDs
* `q[username]` (string): List users matching username.
* `q[email]` (string): List users matching email.
* `q[notes]` (string): List users matching notes field.
* `q[admin]` (string): If `true`, list only admin users.
* `q[allowed_ips]` (string): If set, list only users with overridden allowed IP setting.
* `q[password_validity_days]` (string): If set, list only users with overridden password validity days setting.
* `q[ssl_required]` (string): If set, list only users with overridden SSL required setting.
* `search` (string): Searches for partial matches of name, username, or email.


---

## Show User

```
files_sdk.user.find(id)
```

### Parameters

* `id` (int64): Required - User ID.


---

## Create User

```
files_sdk.user.create({
  "avatar_delete": True,
  "email": "john.doe@files.com",
  "group_id": 1,
  "announcements_read": True,
  "allowed_ips": "127.0.0.1",
  "attachments_permission": True,
  "authenticate_until": "2000-01-01T01:00:00Z",
  "authentication_method": "password",
  "billing_permission": True,
  "bypass_inactive_disable": True,
  "bypass_site_allowed_ips": True,
  "dav_permission": True,
  "disabled": True,
  "ftp_permission": True,
  "header_text": "User-specific message.",
  "language": "en",
  "notification_daily_send_time": 18,
  "name": "John Doe",
  "company": "ACME Corp.",
  "notes": "Internal notes on this user.",
  "office_integration_enabled": True,
  "password_validity_days": 1,
  "receive_admin_alerts": True,
  "require_password_change": True,
  "restapi_permission": True,
  "self_managed": True,
  "sftp_permission": True,
  "site_admin": True,
  "skip_welcome_screen": True,
  "ssl_required": "always_require",
  "sso_strategy_id": 1,
  "subscribe_to_newsletter": True,
  "require_2fa": "always_require",
  "time_zone": "Pacific Time (US & Canada)",
  "username": "user"
})
```

### Parameters

* `avatar_file` (file): An image file for your user avatar.
* `avatar_delete` (boolean): If true, the avatar will be deleted.
* `change_password` (string): Used for changing a password on an existing user.
* `change_password_confirmation` (string): Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
* `email` (string): User's email.
* `grant_permission` (string): Permission to grant on the user root.  Can be blank or `full`, `read`, `write`, `list`, or `history`.
* `group_id` (int64): Group ID to associate this user with.
* `group_ids` (string): A list of group ids to associate this user with.  Comma delimited.
* `password` (string): User password.
* `password_confirmation` (string): Optional, but if provided, we will ensure that it matches the value sent in `password`.
* `announcements_read` (boolean): Signifies that the user has read all the announcements in the UI.
* `allowed_ips` (string): A list of allowed IPs if applicable.  Newline delimited
* `attachments_permission` (boolean): Can the user create Bundles (aka Share Links)?  This field will be aliased or renamed in the future to `bundles_permission`.
* `authenticate_until` (string): Scheduled Date/Time at which user will be deactivated
* `authentication_method` (string): How is this user authenticated?
* `billing_permission` (boolean): Allow this user to perform operations on the account, payments, and invoices?
* `bypass_inactive_disable` (boolean): Exempt this user from being disabled based on inactivity?
* `bypass_site_allowed_ips` (boolean): Allow this user to skip site-wide IP blacklists?
* `dav_permission` (boolean): Can the user connect with WebDAV?
* `disabled` (boolean): Is user disabled? Disabled users cannot log in, and do not count for billing purposes.  Users can be automatically disabled after an inactivity period via a Site setting.
* `ftp_permission` (boolean): Can the user access with FTP/FTPS?
* `header_text` (string): Text to display to the user in the header of the UI
* `language` (string): Preferred language
* `notification_daily_send_time` (int64): Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
* `name` (string): User's full name
* `company` (string): User's company
* `notes` (string): Any internal notes on the user
* `office_integration_enabled` (boolean): Enable integration with Office for the web?
* `password_validity_days` (int64): Number of days to allow user to use the same password
* `receive_admin_alerts` (boolean): Should the user receive admin alerts such a certificate expiration notifications and overages?
* `require_password_change` (boolean): Is a password change required upon next user login?
* `restapi_permission` (boolean): Can this user access the REST API?
* `self_managed` (boolean): Does this user manage it's own credentials or is it a shared/bot user?
* `sftp_permission` (boolean): Can the user access with SFTP?
* `site_admin` (boolean): Is the user an administrator for this site?
* `skip_welcome_screen` (boolean): Skip Welcome page in the UI?
* `ssl_required` (string): SSL required setting
* `sso_strategy_id` (int64): SSO (Single Sign On) strategy ID for the user, if applicable.
* `subscribe_to_newsletter` (boolean): Is the user subscribed to the newsletter?
* `require_2fa` (string): 2FA required setting
* `time_zone` (string): User time zone
* `user_root` (string): Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set.)  Note that this is not used for API, Desktop, or Web interface.
* `username` (string): User's username


---

## Unlock user who has been locked out due to failed logins

```
files_sdk.user.unlock(id)
```

### Parameters

* `id` (int64): Required - User ID.


---

## Resend user welcome email

```
files_sdk.user.resend_welcome_email(id)
```

### Parameters

* `id` (int64): Required - User ID.


---

## Trigger 2FA Reset process for user who has lost access to their existing 2FA methods

```
files_sdk.user.user_2fa_reset(id)
```

### Parameters

* `id` (int64): Required - User ID.


---

## Update User

```
files_sdk.user.update(id, {
  "avatar_delete": True,
  "email": "john.doe@files.com",
  "group_id": 1,
  "announcements_read": True,
  "allowed_ips": "127.0.0.1",
  "attachments_permission": True,
  "authenticate_until": "2000-01-01T01:00:00Z",
  "authentication_method": "password",
  "billing_permission": True,
  "bypass_inactive_disable": True,
  "bypass_site_allowed_ips": True,
  "dav_permission": True,
  "disabled": True,
  "ftp_permission": True,
  "header_text": "User-specific message.",
  "language": "en",
  "notification_daily_send_time": 18,
  "name": "John Doe",
  "company": "ACME Corp.",
  "notes": "Internal notes on this user.",
  "office_integration_enabled": True,
  "password_validity_days": 1,
  "receive_admin_alerts": True,
  "require_password_change": True,
  "restapi_permission": True,
  "self_managed": True,
  "sftp_permission": True,
  "site_admin": True,
  "skip_welcome_screen": True,
  "ssl_required": "always_require",
  "sso_strategy_id": 1,
  "subscribe_to_newsletter": True,
  "require_2fa": "always_require",
  "time_zone": "Pacific Time (US & Canada)",
  "username": "user"
})
```

### Parameters

* `id` (int64): Required - User ID.
* `avatar_file` (file): An image file for your user avatar.
* `avatar_delete` (boolean): If true, the avatar will be deleted.
* `change_password` (string): Used for changing a password on an existing user.
* `change_password_confirmation` (string): Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
* `email` (string): User's email.
* `grant_permission` (string): Permission to grant on the user root.  Can be blank or `full`, `read`, `write`, `list`, or `history`.
* `group_id` (int64): Group ID to associate this user with.
* `group_ids` (string): A list of group ids to associate this user with.  Comma delimited.
* `password` (string): User password.
* `password_confirmation` (string): Optional, but if provided, we will ensure that it matches the value sent in `password`.
* `announcements_read` (boolean): Signifies that the user has read all the announcements in the UI.
* `allowed_ips` (string): A list of allowed IPs if applicable.  Newline delimited
* `attachments_permission` (boolean): Can the user create Bundles (aka Share Links)?  This field will be aliased or renamed in the future to `bundles_permission`.
* `authenticate_until` (string): Scheduled Date/Time at which user will be deactivated
* `authentication_method` (string): How is this user authenticated?
* `billing_permission` (boolean): Allow this user to perform operations on the account, payments, and invoices?
* `bypass_inactive_disable` (boolean): Exempt this user from being disabled based on inactivity?
* `bypass_site_allowed_ips` (boolean): Allow this user to skip site-wide IP blacklists?
* `dav_permission` (boolean): Can the user connect with WebDAV?
* `disabled` (boolean): Is user disabled? Disabled users cannot log in, and do not count for billing purposes.  Users can be automatically disabled after an inactivity period via a Site setting.
* `ftp_permission` (boolean): Can the user access with FTP/FTPS?
* `header_text` (string): Text to display to the user in the header of the UI
* `language` (string): Preferred language
* `notification_daily_send_time` (int64): Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
* `name` (string): User's full name
* `company` (string): User's company
* `notes` (string): Any internal notes on the user
* `office_integration_enabled` (boolean): Enable integration with Office for the web?
* `password_validity_days` (int64): Number of days to allow user to use the same password
* `receive_admin_alerts` (boolean): Should the user receive admin alerts such a certificate expiration notifications and overages?
* `require_password_change` (boolean): Is a password change required upon next user login?
* `restapi_permission` (boolean): Can this user access the REST API?
* `self_managed` (boolean): Does this user manage it's own credentials or is it a shared/bot user?
* `sftp_permission` (boolean): Can the user access with SFTP?
* `site_admin` (boolean): Is the user an administrator for this site?
* `skip_welcome_screen` (boolean): Skip Welcome page in the UI?
* `ssl_required` (string): SSL required setting
* `sso_strategy_id` (int64): SSO (Single Sign On) strategy ID for the user, if applicable.
* `subscribe_to_newsletter` (boolean): Is the user subscribed to the newsletter?
* `require_2fa` (string): 2FA required setting
* `time_zone` (string): User time zone
* `user_root` (string): Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set.)  Note that this is not used for API, Desktop, or Web interface.
* `username` (string): User's username


---

## Delete User

```
files_sdk.user.delete(id)
```

### Parameters

* `id` (int64): Required - User ID.


---

## Unlock user who has been locked out due to failed logins

```
user = files_sdk.user.find(1)

user.unlock()
```

### Parameters

* `id` (int64): Required - User ID.


---

## Resend user welcome email

```
user = files_sdk.user.find(1)

user.resend_welcome_email()
```

### Parameters

* `id` (int64): Required - User ID.


---

## Trigger 2FA Reset process for user who has lost access to their existing 2FA methods

```
user = files_sdk.user.find(1)

user.user_2fa_reset()
```

### Parameters

* `id` (int64): Required - User ID.


---

## Update User

```
user = files_sdk.user.find(1)

user.update({
  "avatar_delete": True,
  "email": "john.doe@files.com",
  "group_id": 1,
  "announcements_read": True,
  "allowed_ips": "127.0.0.1",
  "attachments_permission": True,
  "authenticate_until": "2000-01-01T01:00:00Z",
  "authentication_method": "password",
  "billing_permission": True,
  "bypass_inactive_disable": True,
  "bypass_site_allowed_ips": True,
  "dav_permission": True,
  "disabled": True,
  "ftp_permission": True,
  "header_text": "User-specific message.",
  "language": "en",
  "notification_daily_send_time": 18,
  "name": "John Doe",
  "company": "ACME Corp.",
  "notes": "Internal notes on this user.",
  "office_integration_enabled": True,
  "password_validity_days": 1,
  "receive_admin_alerts": True,
  "require_password_change": True,
  "restapi_permission": True,
  "self_managed": True,
  "sftp_permission": True,
  "site_admin": True,
  "skip_welcome_screen": True,
  "ssl_required": "always_require",
  "sso_strategy_id": 1,
  "subscribe_to_newsletter": True,
  "require_2fa": "always_require",
  "time_zone": "Pacific Time (US & Canada)",
  "username": "user"
})
```

### Parameters

* `id` (int64): Required - User ID.
* `avatar_file` (file): An image file for your user avatar.
* `avatar_delete` (boolean): If true, the avatar will be deleted.
* `change_password` (string): Used for changing a password on an existing user.
* `change_password_confirmation` (string): Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
* `email` (string): User's email.
* `grant_permission` (string): Permission to grant on the user root.  Can be blank or `full`, `read`, `write`, `list`, or `history`.
* `group_id` (int64): Group ID to associate this user with.
* `group_ids` (string): A list of group ids to associate this user with.  Comma delimited.
* `password` (string): User password.
* `password_confirmation` (string): Optional, but if provided, we will ensure that it matches the value sent in `password`.
* `announcements_read` (boolean): Signifies that the user has read all the announcements in the UI.
* `allowed_ips` (string): A list of allowed IPs if applicable.  Newline delimited
* `attachments_permission` (boolean): Can the user create Bundles (aka Share Links)?  This field will be aliased or renamed in the future to `bundles_permission`.
* `authenticate_until` (string): Scheduled Date/Time at which user will be deactivated
* `authentication_method` (string): How is this user authenticated?
* `billing_permission` (boolean): Allow this user to perform operations on the account, payments, and invoices?
* `bypass_inactive_disable` (boolean): Exempt this user from being disabled based on inactivity?
* `bypass_site_allowed_ips` (boolean): Allow this user to skip site-wide IP blacklists?
* `dav_permission` (boolean): Can the user connect with WebDAV?
* `disabled` (boolean): Is user disabled? Disabled users cannot log in, and do not count for billing purposes.  Users can be automatically disabled after an inactivity period via a Site setting.
* `ftp_permission` (boolean): Can the user access with FTP/FTPS?
* `header_text` (string): Text to display to the user in the header of the UI
* `language` (string): Preferred language
* `notification_daily_send_time` (int64): Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
* `name` (string): User's full name
* `company` (string): User's company
* `notes` (string): Any internal notes on the user
* `office_integration_enabled` (boolean): Enable integration with Office for the web?
* `password_validity_days` (int64): Number of days to allow user to use the same password
* `receive_admin_alerts` (boolean): Should the user receive admin alerts such a certificate expiration notifications and overages?
* `require_password_change` (boolean): Is a password change required upon next user login?
* `restapi_permission` (boolean): Can this user access the REST API?
* `self_managed` (boolean): Does this user manage it's own credentials or is it a shared/bot user?
* `sftp_permission` (boolean): Can the user access with SFTP?
* `site_admin` (boolean): Is the user an administrator for this site?
* `skip_welcome_screen` (boolean): Skip Welcome page in the UI?
* `ssl_required` (string): SSL required setting
* `sso_strategy_id` (int64): SSO (Single Sign On) strategy ID for the user, if applicable.
* `subscribe_to_newsletter` (boolean): Is the user subscribed to the newsletter?
* `require_2fa` (string): 2FA required setting
* `time_zone` (string): User time zone
* `user_root` (string): Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set.)  Note that this is not used for API, Desktop, or Web interface.
* `username` (string): User's username


---

## Delete User

```
user = files_sdk.user.find(1)

user.delete()
```

### Parameters

* `id` (int64): Required - User ID.
