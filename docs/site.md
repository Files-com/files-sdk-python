# Site

## Example Site Object

```
{
  "id": 1,
  "name": "My Site",
  "additional_text_file_types": [
    "example"
  ],
  "allowed_2fa_method_sms": True,
  "allowed_2fa_method_totp": True,
  "allowed_2fa_method_webauthn": True,
  "allowed_2fa_method_yubi": True,
  "allowed_2fa_method_email": True,
  "allowed_2fa_method_static": True,
  "allowed_2fa_method_bypass_for_ftp_sftp_dav": True,
  "admin_user_id": 1,
  "admins_bypass_locked_subfolders": True,
  "allow_bundle_names": True,
  "allowed_countries": "US,DE",
  "allowed_ips": "example",
  "always_mkdir_parents": True,
  "ask_about_overwrites": True,
  "bundle_activity_notifications": "never",
  "bundle_expiration": 1,
  "bundle_not_found_message": "example",
  "bundle_password_required": True,
  "bundle_recipient_blacklist_domains": [
    "example"
  ],
  "bundle_recipient_blacklist_free_email_domains": True,
  "bundle_registration_notifications": "never",
  "bundle_require_registration": True,
  "bundle_require_share_recipient": True,
  "bundle_require_note": True,
  "bundle_send_shared_receipts": True,
  "bundle_upload_receipt_notifications": "never",
  "bundle_watermark_attachment": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "bundle_watermark_value": {
    "key": "example value"
  },
  "calculate_file_checksums_crc32": True,
  "calculate_file_checksums_md5": True,
  "calculate_file_checksums_sha1": True,
  "calculate_file_checksums_sha256": True,
  "uploads_via_email_authentication": True,
  "color2_left": "#0066a7",
  "color2_link": "#d34f5d",
  "color2_text": "#0066a7",
  "color2_top": "#000000",
  "color2_top_text": "#ffffff",
  "contact_name": "John Doe",
  "created_at": "2000-01-01T01:00:00Z",
  "currency": "USD",
  "custom_namespace": True,
  "dav_enabled": True,
  "dav_user_root_enabled": True,
  "days_before_deleting_disabled_users": 30,
  "days_to_retain_backups": 30,
  "document_edits_in_bundle_allowed": True,
  "default_time_zone": "Pacific Time (US & Canada)",
  "desktop_app": True,
  "desktop_app_session_ip_pinning": True,
  "desktop_app_session_lifetime": 1,
  "legacy_checksums_mode": True,
  "mobile_app": True,
  "mobile_app_session_ip_pinning": True,
  "mobile_app_session_lifetime": 1,
  "disallowed_countries": "US,DE",
  "disable_files_certificate_generation": True,
  "disable_notifications": True,
  "disable_password_reset": True,
  "domain": "my-custom-domain.com",
  "domain_hsts_header": True,
  "domain_letsencrypt_chain": "example",
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
  "ldap_base_dn": "example",
  "ldap_domain": "mysite.com",
  "ldap_enabled": True,
  "ldap_group_action": "disabled",
  "ldap_group_exclusion": "example",
  "ldap_group_inclusion": "example",
  "ldap_host": "ldap.site.com",
  "ldap_host_2": "ldap2.site.com",
  "ldap_host_3": "ldap3.site.com",
  "ldap_port": 1,
  "ldap_secure": True,
  "ldap_type": "open_ldap",
  "ldap_user_action": "disabled",
  "ldap_user_include_groups": "example",
  "ldap_username": "[ldap username]",
  "ldap_username_field": "sAMAccountName",
  "login_help_text": "Login page help text.",
  "logo": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "login_page_background_image": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "max_prior_passwords": 1,
  "motd_text": "example",
  "motd_use_for_ftp": True,
  "motd_use_for_sftp": True,
  "next_billing_amount": 1.0,
  "next_billing_date": "Apr 20",
  "office_integration_available": True,
  "office_integration_type": "example",
  "oncehub_link": "https://go.oncehub.com/files",
  "opt_out_global": True,
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
  "prevent_root_permissions_for_non_site_admins": True,
  "protocol_access_groups_only": True,
  "require_2fa": True,
  "require_2fa_stop_time": "2000-01-01T01:00:00Z",
  "revoke_bundle_access_on_disable_or_delete": True,
  "require_2fa_user_type": "`site_admins`",
  "require_logout_from_bundles_and_inboxes": True,
  "session": {
    "id": "60525f92e859c4c3d74cb02fd176b1525901b525",
    "language": "en",
    "login_token": "@tok-randomcode",
    "login_token_domain": "https://mysite.files.com",
    "max_dir_listing_size": 1,
    "multiple_regions": True,
    "read_only": True,
    "root_path": "example",
    "home_path": "example",
    "sftp_insecure_ciphers": False,
    "site_id": 1,
    "ssl_required": True,
    "timeout_at": "2000-01-01T01:00:00Z",
    "tls_disabled": False,
    "two_factor_setup_needed": False,
    "allowed_2fa_method_sms": True,
    "allowed_2fa_method_totp": True,
    "allowed_2fa_method_webauthn": True,
    "allowed_2fa_method_yubi": True,
    "calculate_file_checksums_crc32": True,
    "calculate_file_checksums_md5": True,
    "calculate_file_checksums_sha1": True,
    "calculate_file_checksums_sha256": True,
    "legacy_checksums_mode": True,
    "use_provided_modified_at": True,
    "windows_mode_ftp": False,
    "user_belongs_to_parent_site": False
  },
  "sftp_enabled": True,
  "sftp_host_key_type": "default",
  "active_sftp_host_key_id": 1,
  "sftp_insecure_ciphers": True,
  "sftp_insecure_diffie_hellman": True,
  "sftp_user_root_enabled": True,
  "sharing_enabled": True,
  "show_user_notifications_log_in_link": True,
  "show_request_access_link": True,
  "site_footer": "example",
  "site_header": "example",
  "smtp_address": "smtp.my-mail-server.com",
  "smtp_authentication": "plain",
  "smtp_from": "me@my-mail-server.com",
  "smtp_port": 25,
  "smtp_username": "mail",
  "session_expiry": 6.0,
  "session_expiry_minutes": 360,
  "snapshot_sharing_enabled": True,
  "ssl_required": True,
  "subdomain": "mysite",
  "switch_to_plan_date": "2000-01-01T01:00:00Z",
  "tls_disabled": True,
  "trial_days_left": 1,
  "trial_until": "2000-01-01T01:00:00Z",
  "use_dedicated_ips_for_smtp": True,
  "use_provided_modified_at": True,
  "user": {
    "id": 1,
    "username": "user",
    "admin_group_ids": [
      1
    ],
    "allowed_ips": "10.0.0.0/8\n127.0.0.1",
    "attachments_permission": True,
    "api_keys_count": 1,
    "authenticate_until": "2000-01-01T01:00:00Z",
    "authentication_method": "password",
    "avatar_url": "example",
    "billable": True,
    "billing_permission": False,
    "bypass_site_allowed_ips": False,
    "bypass_inactive_disable": False,
    "created_at": "2000-01-01T01:00:00Z",
    "dav_permission": True,
    "disabled": True,
    "disabled_expired_or_inactive": True,
    "email": "john.doe@files.com",
    "first_login_at": "2000-01-01T01:00:00Z",
    "ftp_permission": True,
    "group_ids": "example",
    "header_text": "User-specific message.",
    "language": "en",
    "last_login_at": "2000-01-01T01:00:00Z",
    "last_web_login_at": "2000-01-01T01:00:00Z",
    "last_ftp_login_at": "2000-01-01T01:00:00Z",
    "last_sftp_login_at": "2000-01-01T01:00:00Z",
    "last_dav_login_at": "2000-01-01T01:00:00Z",
    "last_desktop_login_at": "2000-01-01T01:00:00Z",
    "last_restapi_login_at": "2000-01-01T01:00:00Z",
    "last_api_use_at": "2000-01-01T01:00:00Z",
    "last_active_at": "2000-01-01T01:00:00Z",
    "last_protocol_cipher": "example",
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
    "require_login_by": "2000-01-01T01:00:00Z",
    "active_2fa": True,
    "require_password_change": True,
    "password_expired": True,
    "readonly_site_admin": True,
    "restapi_permission": True,
    "self_managed": True,
    "sftp_permission": True,
    "site_admin": True,
    "site_id": 1,
    "skip_welcome_screen": True,
    "ssl_required": "always_require",
    "sso_strategy_id": 1,
    "subscribe_to_newsletter": True,
    "externally_managed": True,
    "time_zone": "Pacific Time (US & Canada)",
    "type_of_2fa": "yubi",
    "type_of_2fa_for_display": "yubi",
    "updated_at": "2000-01-01T01:00:00Z",
    "user_root": "example",
    "user_home": "example",
    "days_remaining_until_password_expire": 1,
    "password_expire_at": "2000-01-01T01:00:00Z"
  },
  "user_lockout": True,
  "user_lockout_lock_period": 1,
  "user_lockout_tries": 1,
  "user_lockout_within": 6,
  "user_requests_enabled": True,
  "user_requests_notify_admins": True,
  "users_can_create_api_keys": True,
  "users_can_create_ssh_keys": True,
  "welcome_custom_text": "Welcome to my site!",
  "welcome_email_cc": "example",
  "welcome_email_subject": "example",
  "welcome_email_enabled": True,
  "welcome_screen": "user_controlled",
  "windows_mode_ftp": True,
  "disable_users_from_inactivity_period_days": 1,
  "group_admins_can_set_user_password": True
}
```

* `id` (int64): Site Id
* `name` (string): Site name
* `additional_text_file_types` (array(string)): Additional extensions that are considered text files
* `allowed_2fa_method_sms` (boolean): Is SMS two factor authentication allowed?
* `allowed_2fa_method_totp` (boolean): Is TOTP two factor authentication allowed?
* `allowed_2fa_method_webauthn` (boolean): Is WebAuthn two factor authentication allowed?
* `allowed_2fa_method_yubi` (boolean): Is yubikey two factor authentication allowed?
* `allowed_2fa_method_email` (boolean): Is OTP via email two factor authentication allowed?
* `allowed_2fa_method_static` (boolean): Is OTP via static codes for two factor authentication allowed?
* `allowed_2fa_method_bypass_for_ftp_sftp_dav` (boolean): Are users allowed to configure their two factor authentication to be bypassed for FTP/SFTP/WebDAV?
* `admin_user_id` (int64): User ID for the main site administrator
* `admins_bypass_locked_subfolders` (boolean): Allow admins to bypass the locked subfolders setting.
* `allow_bundle_names` (boolean): Are manual Bundle names allowed?
* `allowed_countries` (string): Comma separated list of allowed Country codes
* `allowed_ips` (string): List of allowed IP addresses
* `always_mkdir_parents` (boolean): Create parent directories if they do not exist during uploads?  This is primarily used to work around broken upload clients that assume servers will perform this step.
* `ask_about_overwrites` (boolean): If false, rename conflicting files instead of asking for overwrite confirmation.  Only applies to web interface.
* `bundle_activity_notifications` (string): Do Bundle owners receive activity notifications?
* `bundle_expiration` (int64): Site-wide Bundle expiration in days
* `bundle_not_found_message` (string): Custom error message to show when bundle is not found.
* `bundle_password_required` (boolean): Do Bundles require password protection?
* `bundle_recipient_blacklist_domains` (array(string)): List of email domains to disallow when entering a Bundle/Inbox recipients
* `bundle_recipient_blacklist_free_email_domains` (boolean): Disallow free email domains for Bundle/Inbox recipients?
* `bundle_registration_notifications` (string): Do Bundle owners receive registration notification?
* `bundle_require_registration` (boolean): Do Bundles require registration?
* `bundle_require_share_recipient` (boolean): Do Bundles require recipients for sharing?
* `bundle_require_note` (boolean): Do Bundles require internal notes?
* `bundle_send_shared_receipts` (boolean): Do Bundle creators receive receipts of invitations?
* `bundle_upload_receipt_notifications` (string): Do Bundle uploaders receive upload confirmation notifications?
* `bundle_watermark_attachment` (Image): Preview watermark image applied to all bundle items.
* `bundle_watermark_value` (object): Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
* `calculate_file_checksums_crc32` (boolean): Calculate CRC32 checksums for files?
* `calculate_file_checksums_md5` (boolean): Calculate MD5 checksums for files?
* `calculate_file_checksums_sha1` (boolean): Calculate SHA1 checksums for files?
* `calculate_file_checksums_sha256` (boolean): Calculate SHA256 checksums for files?
* `uploads_via_email_authentication` (boolean): Do incoming emails in the Inboxes require checking for SPF/DKIM/DMARC?
* `color2_left` (string): Page link and button color
* `color2_link` (string): Top bar link color
* `color2_text` (string): Page link and button color
* `color2_top` (string): Top bar background color
* `color2_top_text` (string): Top bar text color
* `contact_name` (string): Site main contact name
* `created_at` (date-time): Time this site was created
* `currency` (string): Preferred currency
* `custom_namespace` (boolean): Is this site using a custom namespace for users?
* `dav_enabled` (boolean): Is WebDAV enabled?
* `dav_user_root_enabled` (boolean): Use user FTP roots also for WebDAV?
* `days_before_deleting_disabled_users` (int64): Number of days to keep disabled users before deleting them. If set to 0, disabled users will not be deleted.
* `days_to_retain_backups` (int64): Number of days to keep deleted files
* `document_edits_in_bundle_allowed` (boolean): If true, allow public viewers of Bundles with full permissions to use document editing integrations.
* `default_time_zone` (string): Site default time zone
* `desktop_app` (boolean): Is the desktop app enabled?
* `desktop_app_session_ip_pinning` (boolean): Is desktop app session IP pinning enabled?
* `desktop_app_session_lifetime` (int64): Desktop app session lifetime (in hours)
* `legacy_checksums_mode` (boolean): Use legacy checksums mode?
* `mobile_app` (boolean): Is the mobile app enabled?
* `mobile_app_session_ip_pinning` (boolean): Is mobile app session IP pinning enabled?
* `mobile_app_session_lifetime` (int64): Mobile app session lifetime (in hours)
* `disallowed_countries` (string): Comma separated list of disallowed Country codes
* `disable_files_certificate_generation` (boolean): If set, Files.com will not set the CAA records required to generate future SSL certificates for this domain.
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
* `folder_permissions_groups_only` (boolean): If true, permissions for this site must be bound to a group (not a user).
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
* `login_page_background_image` (Image): Branded login page background
* `max_prior_passwords` (int64): Number of prior passwords to disallow
* `motd_text` (string): A message to show users when they connect via FTP or SFTP.
* `motd_use_for_ftp` (boolean): Show message to users connecting via FTP
* `motd_use_for_sftp` (boolean): Show message to users connecting via SFTP
* `next_billing_amount` (double): Next billing amount
* `next_billing_date` (string): Next billing date
* `office_integration_available` (boolean): If true, allows users to use a document editing integration.
* `office_integration_type` (string): Which document editing integration to support. Files.com Editor or Microsoft Office for the Web.
* `oncehub_link` (string): Link to scheduling a meeting with our Sales team
* `opt_out_global` (boolean): Use servers in the USA only?
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
* `prevent_root_permissions_for_non_site_admins` (boolean): If true, we will prevent non-administrators from receiving any permissions directly on the root folder.  This is commonly used to prevent the accidental application of permissions.
* `protocol_access_groups_only` (boolean): If true, protocol access permissions on users will be ignored, and only protocol access permissions set on Groups will be honored.  Make sure that your current user is a member of a group with API permission when changing this value to avoid locking yourself out of your site.
* `require_2fa` (boolean): Require two-factor authentication for all users?
* `require_2fa_stop_time` (date-time): If set, requirement for two-factor authentication has been scheduled to end on this date-time.
* `revoke_bundle_access_on_disable_or_delete` (boolean): Auto-removes bundles for disabled/deleted users and enforces bundle expiry within user access period.
* `require_2fa_user_type` (string): What type of user is required to use two-factor authentication (when require_2fa is set to `true` for this site)?
* `require_logout_from_bundles_and_inboxes` (boolean): If true, we will hide the 'Remember Me' box on Inbox and Bundle registration pages, requiring that the user logout and log back in every time they visit the page.
* `session` (Session): Current session
* `sftp_enabled` (boolean): Is SFTP enabled?
* `sftp_host_key_type` (string): Sftp Host Key Type
* `active_sftp_host_key_id` (int64): Id of the currently selected custom SFTP Host Key
* `sftp_insecure_ciphers` (boolean): If true, we will allow weak and known insecure ciphers to be used for SFTP connections.  Enabling this setting severely weakens the security of your site and it is not recommend, except as a last resort for compatibility.
* `sftp_insecure_diffie_hellman` (boolean): If true, we will allow weak Diffie Hellman parameters to be used within ciphers for SFTP that are otherwise on our secure list.  This has the effect of making the cipher weaker than our normal threshold for security, but is required to support certain legacy or broken SSH and MFT clients.  Enabling this weakens security, but not nearly as much as enabling the full `sftp_insecure_ciphers` option.
* `sftp_user_root_enabled` (boolean): Use user FTP roots also for SFTP?
* `sharing_enabled` (boolean): Allow bundle creation
* `show_user_notifications_log_in_link` (boolean): Show log in link in user notifications?
* `show_request_access_link` (boolean): Show request access link for users without access?  Currently unused.
* `site_footer` (string): Custom site footer text
* `site_header` (string): Custom site header text
* `smtp_address` (string): SMTP server hostname or IP
* `smtp_authentication` (string): SMTP server authentication type
* `smtp_from` (string): From address to use when mailing through custom SMTP
* `smtp_port` (int64): SMTP server port
* `smtp_username` (string): SMTP server username
* `session_expiry` (double): Session expiry in hours
* `session_expiry_minutes` (int64): Session expiry in minutes
* `snapshot_sharing_enabled` (boolean): Allow snapshot share links creation
* `ssl_required` (boolean): Is SSL required?  Disabling this is insecure.
* `subdomain` (string): Site subdomain
* `switch_to_plan_date` (date-time): If switching plans, when does the new plan take effect?
* `tls_disabled` (boolean): DO NOT ENABLE. This setting allows TLSv1.0 and TLSv1.1 to be used on your site.  We intend to remove this capability entirely in early 2024.  If set, the `sftp_insecure_ciphers` flag will be automatically set to true.
* `trial_days_left` (int64): Number of days left in trial
* `trial_until` (date-time): When does this Site trial expire?
* `use_dedicated_ips_for_smtp` (boolean): If using custom SMTP, should we use dedicated IPs to deliver emails?
* `use_provided_modified_at` (boolean): Allow uploaders to set `provided_modified_at` for uploaded files?
* `user` (User): User of current session
* `user_lockout` (boolean): Will users be locked out after incorrect login attempts?
* `user_lockout_lock_period` (int64): How many hours to lock user out for failed password?
* `user_lockout_tries` (int64): Number of login tries within `user_lockout_within` hours before users are locked out
* `user_lockout_within` (int64): Number of hours for user lockout window
* `user_requests_enabled` (boolean): Enable User Requests feature
* `user_requests_notify_admins` (boolean): Send email to site admins when a user request is received?
* `users_can_create_api_keys` (boolean): Allow users to create their own API keys?
* `users_can_create_ssh_keys` (boolean): Allow users to create their own SSH keys?
* `welcome_custom_text` (string): Custom text send in user welcome email
* `welcome_email_cc` (email): Include this email in welcome emails if enabled
* `welcome_email_subject` (string): Include this email subject in welcome emails if enabled
* `welcome_email_enabled` (boolean): Will the welcome email be sent to new users?
* `welcome_screen` (string): Does the welcome screen appear?
* `windows_mode_ftp` (boolean): Does FTP user Windows emulation mode?
* `disable_users_from_inactivity_period_days` (int64): If greater than zero, users will unable to login if they do not show activity within this number of days.
* `group_admins_can_set_user_password` (boolean): Allow group admins set password authentication method


---

## Show Site Settings

```
files_sdk.site.get()
```


---

## Get the most recent usage snapshot (usage data for billing purposes) for a Site

```
files_sdk.site.get_usage()
```


---

## Update Site Settings

```
files_sdk.site.update({
  "name": "My Site",
  "subdomain": "mysite",
  "domain": "my-custom-domain.com",
  "domain_hsts_header": False,
  "domain_letsencrypt_chain": "example",
  "email": "john.doe@files.com",
  "reply_to_email": "jane.doe@files.com",
  "allow_bundle_names": False,
  "bundle_expiration": 1,
  "welcome_email_enabled": False,
  "ask_about_overwrites": False,
  "show_request_access_link": False,
  "always_mkdir_parents": False,
  "welcome_email_cc": "example",
  "welcome_email_subject": "example",
  "welcome_custom_text": "Welcome to my site!",
  "language": "en",
  "windows_mode_ftp": False,
  "default_time_zone": "Pacific Time (US & Canada)",
  "desktop_app": False,
  "desktop_app_session_ip_pinning": False,
  "desktop_app_session_lifetime": 1,
  "mobile_app": False,
  "mobile_app_session_ip_pinning": False,
  "mobile_app_session_lifetime": 1,
  "folder_permissions_groups_only": False,
  "welcome_screen": "user_controlled",
  "office_integration_available": False,
  "office_integration_type": "example",
  "pin_all_remote_servers_to_site_region": False,
  "motd_text": "example",
  "motd_use_for_ftp": False,
  "motd_use_for_sftp": False,
  "additional_text_file_types": ["example"],
  "bundle_require_note": False,
  "bundle_send_shared_receipts": False,
  "calculate_file_checksums_crc32": False,
  "calculate_file_checksums_md5": False,
  "calculate_file_checksums_sha1": False,
  "calculate_file_checksums_sha256": False,
  "legacy_checksums_mode": False,
  "session_expiry": 1.0,
  "ssl_required": False,
  "tls_disabled": False,
  "sftp_insecure_ciphers": False,
  "sftp_insecure_diffie_hellman": False,
  "disable_files_certificate_generation": False,
  "user_lockout": False,
  "user_lockout_tries": 1,
  "user_lockout_within": 1,
  "user_lockout_lock_period": 1,
  "include_password_in_welcome_email": False,
  "allowed_countries": "US,DE",
  "allowed_ips": "example",
  "disallowed_countries": "US,DE",
  "days_before_deleting_disabled_users": 1,
  "days_to_retain_backups": 1,
  "max_prior_passwords": 1,
  "password_validity_days": 1,
  "password_min_length": 1,
  "password_require_letter": False,
  "password_require_mixed": False,
  "password_require_special": False,
  "password_require_number": False,
  "password_require_unbreached": False,
  "require_logout_from_bundles_and_inboxes": False,
  "dav_user_root_enabled": False,
  "sftp_user_root_enabled": False,
  "disable_password_reset": False,
  "immutable_files": False,
  "bundle_not_found_message": "example",
  "bundle_password_required": False,
  "bundle_require_registration": False,
  "bundle_require_share_recipient": False,
  "bundle_registration_notifications": "never",
  "bundle_activity_notifications": "never",
  "bundle_upload_receipt_notifications": "never",
  "document_edits_in_bundle_allowed": False,
  "password_requirements_apply_to_bundles": False,
  "prevent_root_permissions_for_non_site_admins": False,
  "opt_out_global": False,
  "use_provided_modified_at": False,
  "custom_namespace": False,
  "disable_users_from_inactivity_period_days": 1,
  "non_sso_groups_allowed": False,
  "non_sso_users_allowed": False,
  "sharing_enabled": False,
  "snapshot_sharing_enabled": False,
  "user_requests_enabled": False,
  "user_requests_notify_admins": False,
  "dav_enabled": False,
  "ftp_enabled": False,
  "sftp_enabled": False,
  "users_can_create_api_keys": False,
  "users_can_create_ssh_keys": False,
  "show_user_notifications_log_in_link": False,
  "sftp_host_key_type": "default",
  "active_sftp_host_key_id": 1,
  "protocol_access_groups_only": False,
  "revoke_bundle_access_on_disable_or_delete": False,
  "bundle_watermark_value": {"key":"example value"},
  "group_admins_can_set_user_password": False,
  "bundle_recipient_blacklist_free_email_domains": False,
  "bundle_recipient_blacklist_domains": ["example"],
  "admins_bypass_locked_subfolders": False,
  "allowed_2fa_method_sms": False,
  "allowed_2fa_method_totp": False,
  "allowed_2fa_method_webauthn": False,
  "allowed_2fa_method_yubi": False,
  "allowed_2fa_method_email": False,
  "allowed_2fa_method_static": False,
  "allowed_2fa_method_bypass_for_ftp_sftp_dav": False,
  "require_2fa": False,
  "require_2fa_user_type": "`site_admins`",
  "color2_top": "#000000",
  "color2_left": "#0066a7",
  "color2_link": "#d34f5d",
  "color2_text": "#0066a7",
  "color2_top_text": "#ffffff",
  "site_header": "example",
  "site_footer": "example",
  "login_help_text": "Login page help text.",
  "use_dedicated_ips_for_smtp": False,
  "smtp_address": "smtp.my-mail-server.com",
  "smtp_authentication": "plain",
  "smtp_from": "me@my-mail-server.com",
  "smtp_username": "mail",
  "smtp_port": 1,
  "ldap_enabled": False,
  "ldap_type": "open_ldap",
  "ldap_host": "ldap.site.com",
  "ldap_host_2": "ldap2.site.com",
  "ldap_host_3": "ldap3.site.com",
  "ldap_port": 1,
  "ldap_secure": False,
  "ldap_username": "[ldap username]",
  "ldap_username_field": "sAMAccountName",
  "ldap_domain": "mysite.com",
  "ldap_user_action": "disabled",
  "ldap_group_action": "disabled",
  "ldap_user_include_groups": "example",
  "ldap_group_exclusion": "example",
  "ldap_group_inclusion": "example",
  "ldap_base_dn": "example",
  "uploads_via_email_authentication": False,
  "icon16_delete": False,
  "icon32_delete": False,
  "icon48_delete": False,
  "icon128_delete": False,
  "logo_delete": False,
  "bundle_watermark_attachment_delete": False,
  "login_page_background_image_delete": False,
  "disable_2fa_with_delay": False,
  "session_expiry_minutes": 1
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
* `welcome_email_enabled` (boolean): Will the welcome email be sent to new users?
* `ask_about_overwrites` (boolean): If false, rename conflicting files instead of asking for overwrite confirmation.  Only applies to web interface.
* `show_request_access_link` (boolean): Show request access link for users without access?  Currently unused.
* `always_mkdir_parents` (boolean): Create parent directories if they do not exist during uploads?  This is primarily used to work around broken upload clients that assume servers will perform this step.
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
* `folder_permissions_groups_only` (boolean): If true, permissions for this site must be bound to a group (not a user).
* `welcome_screen` (string): Does the welcome screen appear?
* `office_integration_available` (boolean): If true, allows users to use a document editing integration.
* `office_integration_type` (string): Which document editing integration to support. Files.com Editor or Microsoft Office for the Web.
* `pin_all_remote_servers_to_site_region` (boolean): If true, we will ensure that all internal communications with any remote server are made through the primary region of the site. This setting overrides individual remote server settings.
* `motd_text` (string): A message to show users when they connect via FTP or SFTP.
* `motd_use_for_ftp` (boolean): Show message to users connecting via FTP
* `motd_use_for_sftp` (boolean): Show message to users connecting via SFTP
* `left_navigation_visibility` (object): Visibility settings for account navigation
* `additional_text_file_types` (array(string)): Additional extensions that are considered text files
* `bundle_require_note` (boolean): Do Bundles require internal notes?
* `bundle_send_shared_receipts` (boolean): Do Bundle creators receive receipts of invitations?
* `calculate_file_checksums_crc32` (boolean): Calculate CRC32 checksums for files?
* `calculate_file_checksums_md5` (boolean): Calculate MD5 checksums for files?
* `calculate_file_checksums_sha1` (boolean): Calculate SHA1 checksums for files?
* `calculate_file_checksums_sha256` (boolean): Calculate SHA256 checksums for files?
* `legacy_checksums_mode` (boolean): Use legacy checksums mode?
* `session_expiry` (double): Session expiry in hours
* `ssl_required` (boolean): Is SSL required?  Disabling this is insecure.
* `tls_disabled` (boolean): DO NOT ENABLE. This setting allows TLSv1.0 and TLSv1.1 to be used on your site.  We intend to remove this capability entirely in early 2024.  If set, the `sftp_insecure_ciphers` flag will be automatically set to true.
* `sftp_insecure_ciphers` (boolean): If true, we will allow weak and known insecure ciphers to be used for SFTP connections.  Enabling this setting severely weakens the security of your site and it is not recommend, except as a last resort for compatibility.
* `sftp_insecure_diffie_hellman` (boolean): If true, we will allow weak Diffie Hellman parameters to be used within ciphers for SFTP that are otherwise on our secure list.  This has the effect of making the cipher weaker than our normal threshold for security, but is required to support certain legacy or broken SSH and MFT clients.  Enabling this weakens security, but not nearly as much as enabling the full `sftp_insecure_ciphers` option.
* `disable_files_certificate_generation` (boolean): If set, Files.com will not set the CAA records required to generate future SSL certificates for this domain.
* `user_lockout` (boolean): Will users be locked out after incorrect login attempts?
* `user_lockout_tries` (int64): Number of login tries within `user_lockout_within` hours before users are locked out
* `user_lockout_within` (int64): Number of hours for user lockout window
* `user_lockout_lock_period` (int64): How many hours to lock user out for failed password?
* `include_password_in_welcome_email` (boolean): Include password in emails to new users?
* `allowed_countries` (string): Comma separated list of allowed Country codes
* `allowed_ips` (string): List of allowed IP addresses
* `disallowed_countries` (string): Comma separated list of disallowed Country codes
* `days_before_deleting_disabled_users` (int64): Number of days to keep disabled users before deleting them. If set to 0, disabled users will not be deleted.
* `days_to_retain_backups` (int64): Number of days to keep deleted files
* `max_prior_passwords` (int64): Number of prior passwords to disallow
* `password_validity_days` (int64): Number of days password is valid
* `password_min_length` (int64): Shortest password length for users
* `password_require_letter` (boolean): Require a letter in passwords?
* `password_require_mixed` (boolean): Require lower and upper case letters in passwords?
* `password_require_special` (boolean): Require special characters in password?
* `password_require_number` (boolean): Require a number in passwords?
* `password_require_unbreached` (boolean): Require passwords that have not been previously breached? (see https://haveibeenpwned.com/)
* `require_logout_from_bundles_and_inboxes` (boolean): If true, we will hide the 'Remember Me' box on Inbox and Bundle registration pages, requiring that the user logout and log back in every time they visit the page.
* `dav_user_root_enabled` (boolean): Use user FTP roots also for WebDAV?
* `sftp_user_root_enabled` (boolean): Use user FTP roots also for SFTP?
* `disable_password_reset` (boolean): Is password reset disabled?
* `immutable_files` (boolean): Are files protected from modification?
* `bundle_not_found_message` (string): Custom error message to show when bundle is not found.
* `bundle_password_required` (boolean): Do Bundles require password protection?
* `bundle_require_registration` (boolean): Do Bundles require registration?
* `bundle_require_share_recipient` (boolean): Do Bundles require recipients for sharing?
* `bundle_registration_notifications` (string): Do Bundle owners receive registration notification?
* `bundle_activity_notifications` (string): Do Bundle owners receive activity notifications?
* `bundle_upload_receipt_notifications` (string): Do Bundle uploaders receive upload confirmation notifications?
* `document_edits_in_bundle_allowed` (boolean): If true, allow public viewers of Bundles with full permissions to use document editing integrations.
* `password_requirements_apply_to_bundles` (boolean): Require bundles' passwords, and passwords for other items (inboxes, public shares, etc.) to conform to the same requirements as users' passwords?
* `prevent_root_permissions_for_non_site_admins` (boolean): If true, we will prevent non-administrators from receiving any permissions directly on the root folder.  This is commonly used to prevent the accidental application of permissions.
* `opt_out_global` (boolean): Use servers in the USA only?
* `use_provided_modified_at` (boolean): Allow uploaders to set `provided_modified_at` for uploaded files?
* `custom_namespace` (boolean): Is this site using a custom namespace for users?
* `disable_users_from_inactivity_period_days` (int64): If greater than zero, users will unable to login if they do not show activity within this number of days.
* `non_sso_groups_allowed` (boolean): If true, groups can be manually created / modified / deleted by Site Admins. Otherwise, groups can only be managed via your SSO provider.
* `non_sso_users_allowed` (boolean): If true, users can be manually created / modified / deleted by Site Admins. Otherwise, users can only be managed via your SSO provider.
* `sharing_enabled` (boolean): Allow bundle creation
* `snapshot_sharing_enabled` (boolean): Allow snapshot share links creation
* `user_requests_enabled` (boolean): Enable User Requests feature
* `user_requests_notify_admins` (boolean): Send email to site admins when a user request is received?
* `dav_enabled` (boolean): Is WebDAV enabled?
* `ftp_enabled` (boolean): Is FTP enabled?
* `sftp_enabled` (boolean): Is SFTP enabled?
* `users_can_create_api_keys` (boolean): Allow users to create their own API keys?
* `users_can_create_ssh_keys` (boolean): Allow users to create their own SSH keys?
* `show_user_notifications_log_in_link` (boolean): Show log in link in user notifications?
* `sftp_host_key_type` (string): Sftp Host Key Type
* `active_sftp_host_key_id` (int64): Id of the currently selected custom SFTP Host Key
* `protocol_access_groups_only` (boolean): If true, protocol access permissions on users will be ignored, and only protocol access permissions set on Groups will be honored.  Make sure that your current user is a member of a group with API permission when changing this value to avoid locking yourself out of your site.
* `revoke_bundle_access_on_disable_or_delete` (boolean): Auto-removes bundles for disabled/deleted users and enforces bundle expiry within user access period.
* `bundle_watermark_value` (object): Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
* `group_admins_can_set_user_password` (boolean): Allow group admins set password authentication method
* `bundle_recipient_blacklist_free_email_domains` (boolean): Disallow free email domains for Bundle/Inbox recipients?
* `bundle_recipient_blacklist_domains` (array(string)): List of email domains to disallow when entering a Bundle/Inbox recipients
* `admins_bypass_locked_subfolders` (boolean): Allow admins to bypass the locked subfolders setting.
* `allowed_2fa_method_sms` (boolean): Is SMS two factor authentication allowed?
* `allowed_2fa_method_totp` (boolean): Is TOTP two factor authentication allowed?
* `allowed_2fa_method_webauthn` (boolean): Is WebAuthn two factor authentication allowed?
* `allowed_2fa_method_yubi` (boolean): Is yubikey two factor authentication allowed?
* `allowed_2fa_method_email` (boolean): Is OTP via email two factor authentication allowed?
* `allowed_2fa_method_static` (boolean): Is OTP via static codes for two factor authentication allowed?
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
* `use_dedicated_ips_for_smtp` (boolean): If using custom SMTP, should we use dedicated IPs to deliver emails?
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
* `uploads_via_email_authentication` (boolean): Do incoming emails in the Inboxes require checking for SPF/DKIM/DMARC?
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
* `login_page_background_image_file` (file): 
* `login_page_background_image_delete` (boolean): If true, will delete the file stored in login_page_background_image
* `disable_2fa_with_delay` (boolean): If set to true, we will begin the process of disabling 2FA on this site.
* `ldap_password_change` (string): New LDAP password.
* `ldap_password_change_confirmation` (string): Confirm new LDAP password.
* `smtp_password` (string): Password for SMTP server.
* `session_expiry_minutes` (int64): Session expiry in minutes
