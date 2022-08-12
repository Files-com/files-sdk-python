# Site

## Example Site Object

```
{
  "name": "My Site",
  "allowed_2fa_method_sms": True,
  "allowed_2fa_method_totp": True,
  "allowed_2fa_method_u2f": True,
  "allowed_2fa_method_webauthn": True,
  "allowed_2fa_method_yubi": True,
  "allowed_2fa_method_bypass_for_ftp_sftp_dav": True,
  "admin_user_id": 1,
  "allow_bundle_names": True,
  "allowed_countries": "US,DE",
  "allowed_ips": "",
  "ask_about_overwrites": True,
  "bundle_expiration": 1,
  "bundle_password_required": True,
  "bundle_require_share_recipient": True,
  "bundle_watermark_attachment": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "bundle_watermark_value": "",
  "color2_left": "#0066a7",
  "color2_link": "#d34f5d",
  "color2_text": "#0066a7",
  "color2_top": "#000000",
  "color2_top_text": "#ffffff",
  "contact_name": "John Doe",
  "created_at": "2000-01-01T01:00:00Z",
  "currency": "USD",
  "custom_namespace": True,
  "days_to_retain_backups": 30,
  "default_time_zone": "Pacific Time (US & Canada)",
  "desktop_app": True,
  "desktop_app_session_ip_pinning": True,
  "desktop_app_session_lifetime": 1,
  "mobile_app": True,
  "mobile_app_session_ip_pinning": True,
  "mobile_app_session_lifetime": 1,
  "disallowed_countries": "US,DE",
  "disable_notifications": True,
  "disable_password_reset": True,
  "domain": "my-custom-domain.com",
  "domain_hsts_header": True,
  "domain_letsencrypt_chain": "",
  "email": "john.doe@files.com",
  "ftp_enabled": True,
  "reply_to_email": "jane.doe@files.com",
  "non_sso_groups_allowed": True,
  "non_sso_users_allowed": True,
  "folder_permissions_groups_only": True,
  "hipaa": True,
  "icon128": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "icon16": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "icon32": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "icon48": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "immutable_files_set_at": "2000-01-01T01:00:00Z",
  "include_password_in_welcome_email": True,
  "language": "en",
  "ldap_base_dn": "",
  "ldap_domain": "mysite.com",
  "ldap_enabled": True,
  "ldap_group_action": "disabled",
  "ldap_group_exclusion": "",
  "ldap_group_inclusion": "",
  "ldap_host": "ldap.site.com",
  "ldap_host_2": "ldap2.site.com",
  "ldap_host_3": "ldap3.site.com",
  "ldap_port": 1,
  "ldap_secure": True,
  "ldap_type": "open_ldap",
  "ldap_user_action": "disabled",
  "ldap_user_include_groups": "",
  "ldap_username": "[ldap username]",
  "ldap_username_field": "sAMAccountName",
  "login_help_text": "Login page help text.",
  "logo": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "max_prior_passwords": 1,
  "next_billing_amount": 1.0,
  "next_billing_date": "Apr 20",
  "office_integration_available": True,
  "oncehub_link": "https://go.oncehub.com/files",
  "opt_out_global": True,
  "overage_notified_at": "2000-01-01T01:00:00Z",
  "overage_notify": True,
  "overdue": True,
  "password_min_length": 1,
  "password_require_letter": True,
  "password_require_mixed": True,
  "password_require_number": True,
  "password_require_special": True,
  "password_require_unbreached": True,
  "password_requirements_apply_to_bundles": True,
  "password_validity_days": 1,
  "phone": "555-555-5555",
  "pin_all_remote_servers_to_site_region": True,
  "require_2fa": True,
  "require_2fa_stop_time": "2000-01-01T01:00:00Z",
  "require_2fa_user_type": "`site_admins`",
  "session": {
    "id": "60525f92e859c4c3d74cb02fd176b1525901b525",
    "language": "en",
    "login_token": "@tok-randomcode",
    "login_token_domain": "https://mysite.files.com",
    "max_dir_listing_size": False,
    "multiple_regions": True,
    "read_only": True,
    "root_path": "",
    "sftp_insecure_ciphers": False,
    "site_id": 1,
    "ssl_required": True,
    "tls_disabled": False,
    "two_factor_setup_needed": False,
    "allowed_2fa_method_sms": True,
    "allowed_2fa_method_totp": True,
    "allowed_2fa_method_u2f": True,
    "allowed_2fa_method_webauthn": True,
    "allowed_2fa_method_yubi": True,
    "use_provided_modified_at": True,
    "windows_mode_ftp": False
  },
  "session_pinned_by_ip": True,
  "sftp_enabled": True,
  "sftp_insecure_ciphers": True,
  "sftp_user_root_enabled": True,
  "sharing_enabled": True,
  "show_request_access_link": True,
  "site_footer": "",
  "site_header": "",
  "smtp_address": "smtp.my-mail-server.com",
  "smtp_authentication": "plain",
  "smtp_from": "me@my-mail-server.com",
  "smtp_port": 25,
  "smtp_username": "mail",
  "session_expiry": 6.0,
  "ssl_required": True,
  "subdomain": "mysite",
  "switch_to_plan_date": "2000-01-01T01:00:00Z",
  "tls_disabled": True,
  "trial_days_left": 1,
  "trial_until": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z",
  "use_provided_modified_at": True,
  "user": {
    "id": 1,
    "username": "user",
    "admin_group_ids": [
      1
    ],
    "allowed_ips": "127.0.0.1",
    "attachments_permission": True,
    "api_keys_count": 1,
    "authenticate_until": "2000-01-01T01:00:00Z",
    "authentication_method": "password",
    "avatar_url": "",
    "billing_permission": False,
    "bypass_site_allowed_ips": False,
    "bypass_inactive_disable": False,
    "created_at": "2000-01-01T01:00:00Z",
    "dav_permission": True,
    "disabled": True,
    "email": "john.doe@files.com",
    "first_login_at": "2000-01-01T01:00:00Z",
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
    "password_expired": True,
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
    "type_of_2fa": "yubi",
    "updated_at": "2000-01-01T01:00:00Z",
    "user_root": ""
  },
  "user_lockout": True,
  "user_lockout_lock_period": 1,
  "user_lockout_tries": 1,
  "user_lockout_within": 6,
  "user_requests_enabled": True,
  "user_requests_notify_admins": True,
  "welcome_custom_text": "Welcome to my site!",
  "welcome_email_cc": "",
  "welcome_email_subject": "",
  "welcome_email_enabled": True,
  "welcome_screen": "user_controlled",
  "windows_mode_ftp": True,
  "disable_users_from_inactivity_period_days": 1
}
```

* `name` (string): Site name
* `allowed_2fa_method_sms` (boolean): Is SMS two factor authentication allowed?
* `allowed_2fa_method_totp` (boolean): Is TOTP two factor authentication allowed?
* `allowed_2fa_method_u2f` (boolean): Is U2F two factor authentication allowed?
* `allowed_2fa_method_webauthn` (boolean): Is WebAuthn two factor authentication allowed?
* `allowed_2fa_method_yubi` (boolean): Is yubikey two factor authentication allowed?
* `allowed_2fa_method_bypass_for_ftp_sftp_dav` (boolean): Are users allowed to configure their two factor authentication to be bypassed for FTP/SFTP/WebDAV?
* `admin_user_id` (int64): User ID for the main site administrator
* `allow_bundle_names` (boolean): Are manual Bundle names allowed?
* `allowed_countries` (string): Comma seperated list of allowed Country codes
* `allowed_ips` (string): List of allowed IP addresses
* `ask_about_overwrites` (boolean): If false, rename conflicting files instead of asking for overwrite confirmation.  Only applies to web interface.
* `bundle_expiration` (int64): Site-wide Bundle expiration in days
* `bundle_password_required` (boolean): Do Bundles require password protection?
* `bundle_require_share_recipient` (boolean): Do Bundles require recipients for sharing?
* `bundle_watermark_attachment` (Image): Preview watermark image applied to all bundle items.
* `bundle_watermark_value` (object): Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
* `color2_left` (string): Page link and button color
* `color2_link` (string): Top bar link color
* `color2_text` (string): Page link and button color
* `color2_top` (string): Top bar background color
* `color2_top_text` (string): Top bar text color
* `contact_name` (string): Site main contact name
* `created_at` (date-time): Time this site was created
* `currency` (string): Preferred currency
* `custom_namespace` (boolean): Is this site using a custom namespace for users?
* `days_to_retain_backups` (int64): Number of days to keep deleted files
* `default_time_zone` (string): Site default time zone
* `desktop_app` (boolean): Is the desktop app enabled?
* `desktop_app_session_ip_pinning` (boolean): Is desktop app session IP pinning enabled?
* `desktop_app_session_lifetime` (int64): Desktop app session lifetime (in hours)
* `mobile_app` (boolean): Is the mobile app enabled?
* `mobile_app_session_ip_pinning` (boolean): Is mobile app session IP pinning enabled?
* `mobile_app_session_lifetime` (int64): Mobile app session lifetime (in hours)
* `disallowed_countries` (string): Comma seperated list of disallowed Country codes
* `disable_notifications` (boolean): Are notifications disabled?
* `disable_password_reset` (boolean): Is password reset disabled?
* `domain` (string): Custom domain
* `domain_hsts_header` (boolean): Send HSTS (HTTP Strict Transport Security) header when visitors access the site via a custom domain?
* `domain_letsencrypt_chain` (string): Letsencrypt chain to use when registering SSL Certificate for domain.
* `email` (email): Main email for this site
* `ftp_enabled` (boolean): Is FTP enabled?
* `reply_to_email` (email): Reply-to email for this site
* `non_sso_groups_allowed` (boolean): If true, groups can be manually created / modified / deleted by Site Admins. Otherwise, groups can only be managed via your SSO provider.
* `non_sso_users_allowed` (boolean): If true, users can be manually created / modified / deleted by Site Admins. Otherwise, users can only be managed via your SSO provider.
* `folder_permissions_groups_only` (boolean): If true, permissions for this site must be bound to a group (not a user). Otherwise, permissions must be bound to a user.
* `hipaa` (boolean): Is there a signed HIPAA BAA between Files.com and this site?
* `icon128` (Image): Branded icon 128x128
* `icon16` (Image): Branded icon 16x16
* `icon32` (Image): Branded icon 32x32
* `icon48` (Image): Branded icon 48x48
* `immutable_files_set_at` (date-time): Can files be modified?
* `include_password_in_welcome_email` (boolean): Include password in emails to new users?
* `language` (string): Site default language
* `ldap_base_dn` (string): Base DN for looking up users in LDAP server
* `ldap_domain` (string): Domain name that will be appended to usernames
* `ldap_enabled` (boolean): Main LDAP setting: is LDAP enabled?
* `ldap_group_action` (string): Should we sync groups from LDAP server?
* `ldap_group_exclusion` (string): Comma or newline separated list of group names (with optional wildcards) to exclude when syncing.
* `ldap_group_inclusion` (string): Comma or newline separated list of group names (with optional wildcards) to include when syncing.
* `ldap_host` (string): LDAP host
* `ldap_host_2` (string): LDAP backup host
* `ldap_host_3` (string): LDAP backup host
* `ldap_port` (int64): LDAP port
* `ldap_secure` (boolean): Use secure LDAP?
* `ldap_type` (string): LDAP type
* `ldap_user_action` (string): Should we sync users from LDAP server?
* `ldap_user_include_groups` (string): Comma or newline separated list of group names (with optional wildcards) - if provided, only users in these groups will be added or synced.
* `ldap_username` (string): Username for signing in to LDAP server.
* `ldap_username_field` (string): LDAP username field
* `login_help_text` (string): Login help text
* `logo` (Image): Branded logo
* `max_prior_passwords` (int64): Number of prior passwords to disallow
* `next_billing_amount` (double): Next billing amount
* `next_billing_date` (string): Next billing date
* `office_integration_available` (boolean): Allow users to use Office for the web?
* `oncehub_link` (string): Link to scheduling a meeting with our Sales team
* `opt_out_global` (boolean): Use servers in the USA only?
* `overage_notified_at` (date-time): Last time the site was notified about an overage
* `overage_notify` (boolean): Notify site email of overages?
* `overdue` (boolean): Is this site's billing overdue?
* `password_min_length` (int64): Shortest password length for users
* `password_require_letter` (boolean): Require a letter in passwords?
* `password_require_mixed` (boolean): Require lower and upper case letters in passwords?
* `password_require_number` (boolean): Require a number in passwords?
* `password_require_special` (boolean): Require special characters in password?
* `password_require_unbreached` (boolean): Require passwords that have not been previously breached? (see https://haveibeenpwned.com/)
* `password_requirements_apply_to_bundles` (boolean): Require bundles' passwords, and passwords for other items (inboxes, public shares, etc.) to conform to the same requirements as users' passwords?
* `password_validity_days` (int64): Number of days password is valid
* `phone` (string): Site phone number
* `pin_all_remote_servers_to_site_region` (boolean): If true, we will ensure that all internal communications with any remote server are made through the primary region of the site. This setting overrides individual remote server settings.
* `require_2fa` (boolean): Require two-factor authentication for all users?
* `require_2fa_stop_time` (date-time): If set, requirement for two-factor authentication has been scheduled to end on this date-time.
* `require_2fa_user_type` (string): What type of user is required to use two-factor authentication (when require_2fa is set to `true` for this site)?
* `session` (Session): Current session
* `session_pinned_by_ip` (boolean): Are sessions locked to the same IP? (i.e. do users need to log in again if they change IPs?)
* `sftp_enabled` (boolean): Is SFTP enabled?
* `sftp_insecure_ciphers` (boolean): Are Insecure Ciphers allowed for SFTP?  Note:  Settting TLS Disabled -> True will always allow insecure ciphers for SFTP as well.  Enabling this is insecure.
* `sftp_user_root_enabled` (boolean): Use user FTP roots also for SFTP?
* `sharing_enabled` (boolean): Allow bundle creation
* `show_request_access_link` (boolean): Show request access link for users without access?  Currently unused.
* `site_footer` (string): Custom site footer text
* `site_header` (string): Custom site header text
* `smtp_address` (string): SMTP server hostname or IP
* `smtp_authentication` (string): SMTP server authentication type
* `smtp_from` (string): From address to use when mailing through custom SMTP
* `smtp_port` (int64): SMTP server port
* `smtp_username` (string): SMTP server username
* `session_expiry` (double): Session expiry in hours
* `ssl_required` (boolean): Is SSL required?  Disabling this is insecure.
* `subdomain` (string): Site subdomain
* `switch_to_plan_date` (date-time): If switching plans, when does the new plan take effect?
* `tls_disabled` (boolean): Are Insecure TLS and SFTP Ciphers allowed?  Enabling this is insecure.
* `trial_days_left` (int64): Number of days left in trial
* `trial_until` (date-time): When does this Site trial expire?
* `updated_at` (date-time): Last time this Site was updated
* `use_provided_modified_at` (boolean): Allow uploaders to set `provided_modified_at` for uploaded files?
* `user` (User): User of current session
* `user_lockout` (boolean): Will users be locked out after incorrect login attempts?
* `user_lockout_lock_period` (int64): How many hours to lock user out for failed password?
* `user_lockout_tries` (int64): Number of login tries within `user_lockout_within` hours before users are locked out
* `user_lockout_within` (int64): Number of hours for user lockout window
* `user_requests_enabled` (boolean): Enable User Requests feature
* `user_requests_notify_admins` (boolean): Send email to site admins when a user request is received?
* `welcome_custom_text` (string): Custom text send in user welcome email
* `welcome_email_cc` (email): Include this email in welcome emails if enabled
* `welcome_email_subject` (string): Include this email subject in welcome emails if enabled
* `welcome_email_enabled` (boolean): Will the welcome email be sent to new users?
* `welcome_screen` (string): Does the welcome screen appear?
* `windows_mode_ftp` (boolean): Does FTP user Windows emulation mode?
* `disable_users_from_inactivity_period_days` (int64): If greater than zero, users will unable to login if they do not show activity within this number of days.


---

## Show site settings

```
files_sdk.site.get()
```


---

## Get the most recent usage snapshot (usage data for billing purposes) for a Site

```
files_sdk.site.get_usage()
```


---

## Update site settings

```
files_sdk.site.update({
  "name": "My Site",
  "subdomain": "mysite",
  "domain": "my-custom-domain.com",
  "domain_hsts_header": True,
  "email": "john.doe@files.com",
  "reply_to_email": "jane.doe@files.com",
  "allow_bundle_names": True,
  "bundle_expiration": 1,
  "overage_notify": True,
  "welcome_email_enabled": True,
  "ask_about_overwrites": True,
  "show_request_access_link": True,
  "welcome_custom_text": "Welcome to my site!",
  "language": "en",
  "windows_mode_ftp": True,
  "default_time_zone": "Pacific Time (US & Canada)",
  "desktop_app": True,
  "desktop_app_session_ip_pinning": True,
  "desktop_app_session_lifetime": 1,
  "mobile_app": True,
  "mobile_app_session_ip_pinning": True,
  "mobile_app_session_lifetime": 1,
  "folder_permissions_groups_only": True,
  "welcome_screen": "user_controlled",
  "office_integration_available": True,
  "pin_all_remote_servers_to_site_region": True,
  "session_expiry": 1.0,
  "ssl_required": True,
  "tls_disabled": True,
  "sftp_insecure_ciphers": True,
  "user_lockout": True,
  "user_lockout_tries": 1,
  "user_lockout_within": 1,
  "user_lockout_lock_period": 1,
  "include_password_in_welcome_email": True,
  "allowed_countries": "US,DE",
  "disallowed_countries": "US,DE",
  "days_to_retain_backups": 1,
  "max_prior_passwords": 1,
  "password_validity_days": 1,
  "password_min_length": 1,
  "password_require_letter": True,
  "password_require_mixed": True,
  "password_require_special": True,
  "password_require_number": True,
  "password_require_unbreached": True,
  "sftp_user_root_enabled": True,
  "disable_password_reset": True,
  "immutable_files": True,
  "session_pinned_by_ip": True,
  "bundle_password_required": True,
  "bundle_require_share_recipient": True,
  "password_requirements_apply_to_bundles": True,
  "opt_out_global": True,
  "use_provided_modified_at": True,
  "custom_namespace": True,
  "disable_users_from_inactivity_period_days": 1,
  "non_sso_groups_allowed": True,
  "non_sso_users_allowed": True,
  "sharing_enabled": True,
  "user_requests_enabled": True,
  "user_requests_notify_admins": True,
  "ftp_enabled": True,
  "sftp_enabled": True,
  "allowed_2fa_method_sms": True,
  "allowed_2fa_method_u2f": True,
  "allowed_2fa_method_totp": True,
  "allowed_2fa_method_webauthn": True,
  "allowed_2fa_method_yubi": True,
  "allowed_2fa_method_bypass_for_ftp_sftp_dav": True,
  "require_2fa": True,
  "require_2fa_user_type": "`site_admins`",
  "color2_top": "#000000",
  "color2_left": "#0066a7",
  "color2_link": "#d34f5d",
  "color2_text": "#0066a7",
  "color2_top_text": "#ffffff",
  "login_help_text": "Login page help text.",
  "smtp_address": "smtp.my-mail-server.com",
  "smtp_authentication": "plain",
  "smtp_from": "me@my-mail-server.com",
  "smtp_username": "mail",
  "smtp_port": 1,
  "ldap_enabled": True,
  "ldap_type": "open_ldap",
  "ldap_host": "ldap.site.com",
  "ldap_host_2": "ldap2.site.com",
  "ldap_host_3": "ldap3.site.com",
  "ldap_port": 1,
  "ldap_secure": True,
  "ldap_username": "[ldap username]",
  "ldap_username_field": "sAMAccountName",
  "ldap_domain": "mysite.com",
  "ldap_user_action": "disabled",
  "ldap_group_action": "disabled",
  "icon16_delete": True,
  "icon32_delete": True,
  "icon48_delete": True,
  "icon128_delete": True,
  "logo_delete": True,
  "bundle_watermark_attachment_delete": True,
  "disable_2fa_with_delay": True
})
```

### Parameters

* `name` (string): Site name
* `subdomain` (string): Site subdomain
* `domain` (string): Custom domain
* `domain_hsts_header` (boolean): Send HSTS (HTTP Strict Transport Security) header when visitors access the site via a custom domain?
* `domain_letsencrypt_chain` (string): Letsencrypt chain to use when registering SSL Certificate for domain.
* `email` (string): Main email for this site
* `reply_to_email` (string): Reply-to email for this site
* `allow_bundle_names` (boolean): Are manual Bundle names allowed?
* `bundle_expiration` (int64): Site-wide Bundle expiration in days
* `overage_notify` (boolean): Notify site email of overages?
* `welcome_email_enabled` (boolean): Will the welcome email be sent to new users?
* `ask_about_overwrites` (boolean): If false, rename conflicting files instead of asking for overwrite confirmation.  Only applies to web interface.
* `show_request_access_link` (boolean): Show request access link for users without access?  Currently unused.
* `welcome_email_cc` (string): Include this email in welcome emails if enabled
* `welcome_email_subject` (string): Include this email subject in welcome emails if enabled
* `welcome_custom_text` (string): Custom text send in user welcome email
* `language` (string): Site default language
* `windows_mode_ftp` (boolean): Does FTP user Windows emulation mode?
* `default_time_zone` (string): Site default time zone
* `desktop_app` (boolean): Is the desktop app enabled?
* `desktop_app_session_ip_pinning` (boolean): Is desktop app session IP pinning enabled?
* `desktop_app_session_lifetime` (int64): Desktop app session lifetime (in hours)
* `mobile_app` (boolean): Is the mobile app enabled?
* `mobile_app_session_ip_pinning` (boolean): Is mobile app session IP pinning enabled?
* `mobile_app_session_lifetime` (int64): Mobile app session lifetime (in hours)
* `folder_permissions_groups_only` (boolean): If true, permissions for this site must be bound to a group (not a user). Otherwise, permissions must be bound to a user.
* `welcome_screen` (string): Does the welcome screen appear?
* `office_integration_available` (boolean): Allow users to use Office for the web?
* `pin_all_remote_servers_to_site_region` (boolean): If true, we will ensure that all internal communications with any remote server are made through the primary region of the site. This setting overrides individual remote server settings.
* `session_expiry` (double): Session expiry in hours
* `ssl_required` (boolean): Is SSL required?  Disabling this is insecure.
* `tls_disabled` (boolean): Are Insecure TLS and SFTP Ciphers allowed?  Enabling this is insecure.
* `sftp_insecure_ciphers` (boolean): Are Insecure Ciphers allowed for SFTP?  Note:  Settting TLS Disabled -> True will always allow insecure ciphers for SFTP as well.  Enabling this is insecure.
* `user_lockout` (boolean): Will users be locked out after incorrect login attempts?
* `user_lockout_tries` (int64): Number of login tries within `user_lockout_within` hours before users are locked out
* `user_lockout_within` (int64): Number of hours for user lockout window
* `user_lockout_lock_period` (int64): How many hours to lock user out for failed password?
* `include_password_in_welcome_email` (boolean): Include password in emails to new users?
* `allowed_countries` (string): Comma seperated list of allowed Country codes
* `allowed_ips` (string): List of allowed IP addresses
* `disallowed_countries` (string): Comma seperated list of disallowed Country codes
* `days_to_retain_backups` (int64): Number of days to keep deleted files
* `max_prior_passwords` (int64): Number of prior passwords to disallow
* `password_validity_days` (int64): Number of days password is valid
* `password_min_length` (int64): Shortest password length for users
* `password_require_letter` (boolean): Require a letter in passwords?
* `password_require_mixed` (boolean): Require lower and upper case letters in passwords?
* `password_require_special` (boolean): Require special characters in password?
* `password_require_number` (boolean): Require a number in passwords?
* `password_require_unbreached` (boolean): Require passwords that have not been previously breached? (see https://haveibeenpwned.com/)
* `sftp_user_root_enabled` (boolean): Use user FTP roots also for SFTP?
* `disable_password_reset` (boolean): Is password reset disabled?
* `immutable_files` (boolean): Are files protected from modification?
* `session_pinned_by_ip` (boolean): Are sessions locked to the same IP? (i.e. do users need to log in again if they change IPs?)
* `bundle_password_required` (boolean): Do Bundles require password protection?
* `bundle_require_share_recipient` (boolean): Do Bundles require recipients for sharing?
* `password_requirements_apply_to_bundles` (boolean): Require bundles' passwords, and passwords for other items (inboxes, public shares, etc.) to conform to the same requirements as users' passwords?
* `opt_out_global` (boolean): Use servers in the USA only?
* `use_provided_modified_at` (boolean): Allow uploaders to set `provided_modified_at` for uploaded files?
* `custom_namespace` (boolean): Is this site using a custom namespace for users?
* `disable_users_from_inactivity_period_days` (int64): If greater than zero, users will unable to login if they do not show activity within this number of days.
* `non_sso_groups_allowed` (boolean): If true, groups can be manually created / modified / deleted by Site Admins. Otherwise, groups can only be managed via your SSO provider.
* `non_sso_users_allowed` (boolean): If true, users can be manually created / modified / deleted by Site Admins. Otherwise, users can only be managed via your SSO provider.
* `sharing_enabled` (boolean): Allow bundle creation
* `user_requests_enabled` (boolean): Enable User Requests feature
* `user_requests_notify_admins` (boolean): Send email to site admins when a user request is received?
* `ftp_enabled` (boolean): Is FTP enabled?
* `sftp_enabled` (boolean): Is SFTP enabled?
* `allowed_2fa_method_sms` (boolean): Is SMS two factor authentication allowed?
* `allowed_2fa_method_u2f` (boolean): Is U2F two factor authentication allowed?
* `allowed_2fa_method_totp` (boolean): Is TOTP two factor authentication allowed?
* `allowed_2fa_method_webauthn` (boolean): Is WebAuthn two factor authentication allowed?
* `allowed_2fa_method_yubi` (boolean): Is yubikey two factor authentication allowed?
* `allowed_2fa_method_bypass_for_ftp_sftp_dav` (boolean): Are users allowed to configure their two factor authentication to be bypassed for FTP/SFTP/WebDAV?
* `require_2fa` (boolean): Require two-factor authentication for all users?
* `require_2fa_user_type` (string): What type of user is required to use two-factor authentication (when require_2fa is set to `true` for this site)?
* `color2_top` (string): Top bar background color
* `color2_left` (string): Page link and button color
* `color2_link` (string): Top bar link color
* `color2_text` (string): Page link and button color
* `color2_top_text` (string): Top bar text color
* `site_header` (string): Custom site header text
* `site_footer` (string): Custom site footer text
* `login_help_text` (string): Login help text
* `smtp_address` (string): SMTP server hostname or IP
* `smtp_authentication` (string): SMTP server authentication type
* `smtp_from` (string): From address to use when mailing through custom SMTP
* `smtp_username` (string): SMTP server username
* `smtp_port` (int64): SMTP server port
* `ldap_enabled` (boolean): Main LDAP setting: is LDAP enabled?
* `ldap_type` (string): LDAP type
* `ldap_host` (string): LDAP host
* `ldap_host_2` (string): LDAP backup host
* `ldap_host_3` (string): LDAP backup host
* `ldap_port` (int64): LDAP port
* `ldap_secure` (boolean): Use secure LDAP?
* `ldap_username` (string): Username for signing in to LDAP server.
* `ldap_username_field` (string): LDAP username field
* `ldap_domain` (string): Domain name that will be appended to usernames
* `ldap_user_action` (string): Should we sync users from LDAP server?
* `ldap_group_action` (string): Should we sync groups from LDAP server?
* `ldap_user_include_groups` (string): Comma or newline separated list of group names (with optional wildcards) - if provided, only users in these groups will be added or synced.
* `ldap_group_exclusion` (string): Comma or newline separated list of group names (with optional wildcards) to exclude when syncing.
* `ldap_group_inclusion` (string): Comma or newline separated list of group names (with optional wildcards) to include when syncing.
* `ldap_base_dn` (string): Base DN for looking up users in LDAP server
* `icon16_file` (file): 
* `icon16_delete` (boolean): If true, will delete the file stored in icon16
* `icon32_file` (file): 
* `icon32_delete` (boolean): If true, will delete the file stored in icon32
* `icon48_file` (file): 
* `icon48_delete` (boolean): If true, will delete the file stored in icon48
* `icon128_file` (file): 
* `icon128_delete` (boolean): If true, will delete the file stored in icon128
* `logo_file` (file): 
* `logo_delete` (boolean): If true, will delete the file stored in logo
* `bundle_watermark_attachment_file` (file): 
* `bundle_watermark_attachment_delete` (boolean): If true, will delete the file stored in bundle_watermark_attachment
* `disable_2fa_with_delay` (boolean): If set to true, we will begin the process of disabling 2FA on this site.
* `ldap_password_change` (string): New LDAP password.
* `ldap_password_change_confirmation` (string): Confirm new LDAP password.
* `smtp_password` (string): Password for SMTP server.
