# Settings

## Example Settings Object

```
{
  "image_regex": ".(png|...)",
  "video_regex": ".(avi|...)",
  "audio_regex": ".(mp3|...)",
  "pdf_regex": ".(pdf|...)",
  "current_language": "en",
  "current_time": "2000-01-01T01:00:00Z",
  "linode_regions": [
    "example"
  ],
  "wasabi_regions": [
    "example"
  ],
  "primary_sub_domain_base": "files.com",
  "read_only": True,
  "reauth": True,
  "regions": [
    "example"
  ],
  "s3_regions": [
    "example"
  ],
  "sales_tax_regions": [
    "example"
  ],
  "session_language": "en",
  "tab_config": "example",
  "allow_bypassing_2fa_policies": True,
  "allow_credential_changes": True,
  "allow_providing_gpg_keys": True,
  "allow_user_creation": True,
  "bundle_not_found_message": "example",
  "beta_features": True,
  "beta_feature2": True,
  "beta_feature3": True,
  "calculate_file_checksums_crc32": True,
  "calculate_file_checksums_md5": True,
  "calculate_file_checksums_sha1": True,
  "calculate_file_checksums_sha256": True,
  "color2_left": "#0066a7",
  "color2_link": "#d34f5d",
  "color2_text": "#0066a7",
  "color2_top": "#000000",
  "color2_top_text": "#ffffff",
  "document_edits_in_bundle_allowed": True,
  "domain": "my-custom-domain.com",
  "disable_password_reset": True,
  "login_clickwrap_body": "example",
  "pending_clickwrap_id": 1,
  "pending_clickwrap_body": "example",
  "disable_drive_mounting": True,
  "desktop_drive_mappings": {
    "key": "example value"
  },
  "remote_desktop_debug_logging_enabled": True,
  "remote_desktop_debug_logging_expires_at": "2000-01-01T01:00:00Z",
  "has_workspaces": True,
  "has_accessible_gpg_keys": True,
  "default_workspace_id": 1,
  "legacy_checksums_mode": True,
  "login_help_text": "Text shown on login page.",
  "login_help_text_markdown": "Text shown on login page.",
  "site_name": "My Great Site",
  "office_integration_type": "office_365",
  "office_integration_enabled": True,
  "office_integration_host": "wopi.files.com",
  "oncehub_link": "https://go.oncehub.com/files",
  "office_integration_available": True,
  "require_logout_from_bundles_and_inboxes": True,
  "self_signup_eligible": True,
  "show_request_access_link": True,
  "site_footer_markdown": "example",
  "site_header_markdown": "example",
  "email_footer_custom_text_markdown": "example",
  "site_public_header_markdown": "example",
  "site_public_footer_markdown": "example",
  "site_language": "en",
  "site_id": 1,
  "sso_strategies": [
    "google"
  ],
  "subdomain": "mysite",
  "use_provided_modified_at": True,
  "user_requests_enabled": True,
  "welcome_screen": "user_controlled",
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
  "logo": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "login_page_background_image": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "logo_thumbnail": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "login_page_background_image_thumbnail": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "attachments_permission": True,
  "authentication_method": "password",
  "avatar_url": "example",
  "billing_permission": True,
  "cached_permissions": [
    False
  ],
  "can_admin_somewhere": True,
  "can_bundle_somewhere": True,
  "can_write_somewhere": True,
  "dav_permission": True,
  "days_remaining_until_password_expire": 1,
  "email": "example",
  "ftp_permission": True,
  "group_admin": True,
  "header_text": "example",
  "in_app_ai_assistant_available": True,
  "ai_assistant_personality_id": 1,
  "ai_assistant_personality_system_prompt": "example",
  "file_transform_capabilities": null,
  "id": 1,
  "last_read_announcements_at": "2000-01-01T01:00:00Z",
  "name": "user",
  "notification_daily_send_time": 18,
  "notify_on_all_site_warnings": True,
  "notify_on_all_sso_failures": True,
  "notify_on_all_user_security_events": True,
  "notify_on_all_pending_work_failures": True,
  "notify_on_all_siem_http_destination_failures": True,
  "notify_on_all_sync_failures": True,
  "notify_on_all_automation_failures": True,
  "notify_on_all_expectation_failures": True,
  "partner_admin": True,
  "primary_group_id": 1,
  "partner_id": 1,
  "root_folder_restricted": True,
  "self_managed": True,
  "sftp_permission": True,
  "site_admin": True,
  "readonly_site_admin": True,
  "skip_welcome_screen": True,
  "externally_managed": True,
  "time_zone": "Pacific Time (US & Canada)",
  "type_of_2fa": "totp",
  "reauth_2fa": "totp",
  "user_id": 1,
  "user_language": "en",
  "user_login_url": "example",
  "user_root": "example",
  "username": "user",
  "web_root": "",
  "workspace_admin": True,
  "workspace_scoped": True,
  "nps_response_requested": True,
  "active_region_count": 1,
  "admins_bypass_locked_subfolders": True,
  "additional_text_file_types": [
    "example"
  ],
  "text_preview_extensions": [
    "example"
  ],
  "allowed_2fa_method_bypass_for_ftp_sftp_dav": True,
  "allowed_2fa_method_sms": True,
  "allowed_2fa_method_totp": True,
  "allowed_2fa_method_webauthn": True,
  "allowed_2fa_method_yubi": True,
  "allowed_2fa_method_email": True,
  "allowed_2fa_method_static": True,
  "allow_bundle_names": True,
  "allow_user_level_2fa_override": True,
  "require_2fa_exempt_all_sso_users": True,
  "allow_user_level_allowed_ip_override": True,
  "allow_user_level_ssl_override": True,
  "bundle_recipient_blacklist_free_email_domains": True,
  "bundle_recipient_blacklist_domains": [
    "example"
  ],
  "bundle_activity_notifications": "example",
  "bundle_expiration": 1,
  "bundle_password_required": True,
  "bundle_registration_notifications": "example",
  "bundle_require_registration": True,
  "bundle_require_share_recipient": True,
  "bundle_require_note": True,
  "bundle_upload_receipt_notifications": "example",
  "child_site_count_for_plan": 1,
  "desktop_app": True,
  "exavault_api_available": True,
  "feature_bundle_eca": True,
  "feature_bundle_power": True,
  "feature_bundle_premier": True,
  "folder_permissions_groups_only": True,
  "group_admins_can_add_users": True,
  "group_admins_can_delete_users": True,
  "group_admins_can_enable_disable_users": True,
  "group_admins_can_modify_users": True,
  "group_admins_can_bypass_user_lifecycle_rules": True,
  "group_admins_can_reset_passwords": True,
  "group_admins_can_set_user_password": True,
  "has_account": True,
  "hide_billing": True,
  "high_users_count": True,
  "history_unavailable": True,
  "immutable_files": True,
  "intersitial_page": "example",
  "is_child_site": True,
  "left_navigation_visibility": {
    "sharing": {
      "admin": True,
      "all": True
    },
    "automation_flow": {
      "admin": False,
      "all": False
    },
    "integrations": {
      "admin": False,
      "all": False
    },
    "clients_protocols": {
      "admin": False,
      "all": False
    }
  },
  "min_remote_sync_interval": 1,
  "non_sso_groups_allowed": True,
  "non_sso_users_allowed": True,
  "overdue": True,
  "site_unavailable": True,
  "password_min_length": 1,
  "password_require_letter": True,
  "password_require_mixed": True,
  "password_require_number": True,
  "password_require_special": True,
  "password_require_unbreached": True,
  "password_requirements_apply_to_bundles": True,
  "plan_as2_included": True,
  "prevent_root_permissions_for_non_site_admins": True,
  "protocol_access_groups_only": True,
  "public_url": "mygreatwebsite.com",
  "public_sharing_allowed": True,
  "require_2fa": True,
  "root_region": "example",
  "revoke_bundle_access_on_disable_or_delete": True,
  "sharing_enabled": True,
  "snapshot_sharing_enabled": True,
  "staging_site_count_for_plan": 1,
  "trial_flagged_as_duplicate": True,
  "trial_days_left": 1,
  "trial_locked": True,
  "trial_until": "2000-01-01T01:00:00Z",
  "usage_included": 1,
  "users_can_create_api_keys": True,
  "users_can_create_ssh_keys": True,
  "migrate_remote_server_sync_to_sync": True,
  "users_count": 1,
  "session_available_sites": [
    False
  ],
  "impersonator_user_id": 1
}
```

* `image_regex` (string): All supported image types
* `video_regex` (string): All supported video types
* `audio_regex` (string): All supported audio types
* `pdf_regex` (string): All supported PDF types
* `current_language` (string): Current language locale setting
* `current_time` (date-time): Current Time in UTC
* `linode_regions` (array(object)): Region name and description
* `wasabi_regions` (array(object)): Region name and description
* `primary_sub_domain_base` (string): Primary domain name base of the site
* `read_only` (boolean): Is this session read only?
* `reauth` (boolean): Password check skipped?
* `regions` (array(object)): Region name and description
* `s3_regions` (array(object)): Region name and description
* `sales_tax_regions` (array(object)): States with applicable sales tax
* `session_language` (string): Session locale setting
* `tab_config` (string): Deprecated
* `allow_bypassing_2fa_policies` (boolean): Can users bypass 2FA policies?
* `allow_credential_changes` (boolean): Can partner admins manage user credentials?
* `allow_providing_gpg_keys` (boolean): Can partner admins provide their own GPG keys?
* `allow_user_creation` (boolean): Can partner admins create new users?
* `bundle_not_found_message` (string): Custom error message to show when bundle is not found.
* `beta_features` (boolean): Is beta feature 1 available?
* `beta_feature2` (boolean): Is beta feature 2 available?
* `beta_feature3` (boolean): Is beta feature 3 available?
* `calculate_file_checksums_crc32` (boolean): Calculate CRC32 checksum for incoming files?
* `calculate_file_checksums_md5` (boolean): Calculate MD5 checksum for incoming files?
* `calculate_file_checksums_sha1` (boolean): Calculate SHA1 checksum for incoming files?
* `calculate_file_checksums_sha256` (boolean): Calculate SHA256 checksum for incoming files?
* `color2_left` (string): Page link and button color
* `color2_link` (string): Top bar link color
* `color2_text` (string): Page link and button color
* `color2_top` (string): Top bar background color
* `color2_top_text` (string): Top bar text color
* `document_edits_in_bundle_allowed` (boolean): If true, allow public viewers of Bundles with full permissions to use document editing integrations.
* `domain` (string): Custom domain
* `disable_password_reset` (boolean): Is password reset disabled?
* `login_clickwrap_body` (string): Clickwrap body text to show on every web login.
* `pending_clickwrap_id` (int64): ID of clickwrap the user must accept.
* `pending_clickwrap_body` (string): Body of clickwrap the user must accept.
* `disable_drive_mounting` (boolean): Whether the desktop app should hide drive mounting, prevent new drive mounts, and unmount active drive mounts.
* `desktop_drive_mappings` (object): Mappings from drive letters to paths for the desktop application.
* `remote_desktop_debug_logging_enabled` (boolean): Whether remote desktop debug log upload is enabled for this user.
* `remote_desktop_debug_logging_expires_at` (date-time): When remote desktop debug logging expires for this user.
* `has_workspaces` (boolean): True if the current user can access any named Workspaces (id > 0).
* `has_accessible_gpg_keys` (boolean): True if the current user has access to any GPG keys.
* `default_workspace_id` (int64): Workspace ID the user should land in by default when more than one Workspace is available.
* `legacy_checksums_mode` (boolean): Use legacy checksums mode?
* `login_help_text` (string): Login help text (as HTML).  Unsafe! Deprecated! Do Not Use!
* `login_help_text_markdown` (string): Login help text (as Markdown)
* `site_name` (string): Site name
* `office_integration_type` (string): Which document editing integration to support. Files.com Editor or Microsoft Office for the Web.
* `office_integration_enabled` (boolean): If true, allows users to use a document editing integration.
* `office_integration_host` (string): Document editing integration hostname for API calls.
* `oncehub_link` (string): Link to scheduling a meeting with our Sales team
* `office_integration_available` (boolean): If true, allows users to use a document editing integration.
* `require_logout_from_bundles_and_inboxes` (boolean): If true, we will hide the 'Remember Me' box on Inbox and Bundle registration pages, requiring that the user logout and log back in every time they visit the page.
* `self_signup_eligible` (boolean): Is self signup available?
* `show_request_access_link` (boolean): Show request access link for users without access?
* `site_footer_markdown` (string): Site footer for branding (as Markdown) on authenticated (logged-in) user pages
* `site_header_markdown` (string): Site header for branding (as Markdown) on authenticated (logged-in) user pages
* `email_footer_custom_text_markdown` (string): Custom footer text for system-generated emails. Supports strftime patterns like %Y (4-digit year), %m (month), %d (day).
* `site_public_header_markdown` (string): Site header for branding (as Markdown) on public (unauthenticated) pages.
* `site_public_footer_markdown` (string): Site footer for branding (as Markdown) on public (unauthenticated) pages.
* `site_language` (string): Site language locale
* `site_id` (int64): Site ID
* `sso_strategies` (SsoStrategy): SSO strategies in use
* `subdomain` (string): Site subdomain
* `use_provided_modified_at` (boolean): Allow setting provided_modified_at?
* `user_requests_enabled` (boolean): Is the user requests feature enabled?
* `welcome_screen` (string): Does the welcome screen appear? Can be `enabled`, `hidden`, or `disabled`
* `icon128` (Image): Branded icon 128x128
* `icon16` (Image): Branded icon 16x16
* `icon32` (Image): Branded icon 32x32
* `icon48` (Image): Branded icon 48x48
* `logo` (Image): Branded logo
* `login_page_background_image` (Image): Branded login page background
* `logo_thumbnail` (Image): Branded Logo thumbnail
* `login_page_background_image_thumbnail` (Image): Branded login page background thumbnail
* `attachments_permission` (boolean): 
* `authentication_method` (string): Authentication method for the user.  Can be `password`, `sso`, or `none`
* `avatar_url` (string): URL holding the user's avatar
* `billing_permission` (boolean): Allow this user to perform operations on the account, payments, and invoices?
* `cached_permissions` (array(object)): All permissions applicable to this user, including permissions inherited via groups.
* `can_admin_somewhere` (boolean): If true, user has admin permissions somewhere on the site.
* `can_bundle_somewhere` (boolean): If true, user has bundle permissions somewhere on the site.
* `can_write_somewhere` (boolean): If true, user has write, full, or admin permissions somewhere on the site.
* `dav_permission` (boolean): Can the user connect with WebDAV?
* `days_remaining_until_password_expire` (int64): Number of days remaining until password expires
* `email` (email): User email address
* `ftp_permission` (boolean): Can the user access with FTP/FTPS?
* `group_admin` (boolean): Is a group administrator?
* `header_text` (string): Text to display to the user in the header of the UI
* `in_app_ai_assistant_available` (boolean): Is the in-app AI assistant available to the current user?
* `ai_assistant_personality_id` (int64): AI Assistant Personality ID for the in-app AI Assistant.
* `ai_assistant_personality_system_prompt` (string): System prompt for the in-app AI Assistant.
* `file_transform_capabilities` (object): Supported file transform input and output formats
* `id` (int64): User ID
* `last_read_announcements_at` (date-time): The last date/time this user has read announcements
* `name` (string): User name
* `notification_daily_send_time` (int64): Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
* `notify_on_all_site_warnings` (boolean): Should the user receive site warnings via email?
* `notify_on_all_sso_failures` (boolean): Should the user receive sso/scim/ldap configuration/sync failures via email?
* `notify_on_all_user_security_events` (boolean): Should the user receive user security events via email?
* `notify_on_all_pending_work_failures` (boolean): Should the user receive pending work failures via email?
* `notify_on_all_siem_http_destination_failures` (boolean): Should the user receive siem failures via email?
* `notify_on_all_sync_failures` (boolean): Should the user receive sync failures via email?
* `notify_on_all_automation_failures` (boolean): Should the user receive automation failures via email?
* `notify_on_all_expectation_failures` (boolean): Should the user receive expectation failures and misses via email?
* `partner_admin` (boolean): Is this user a Partner administrator?
* `primary_group_id` (int64): Primary group ID for Group Admin scoping
* `partner_id` (int64): Partner ID, if applicable.
* `root_folder_restricted` (boolean): Does this user use a File System Layout that restricts creating Files, Folders, or Settings in the Root Folder?
* `self_managed` (boolean): Does this user manage it's own credentials?
* `sftp_permission` (boolean): Can the user access with SFTP?
* `site_admin` (boolean): Is the user an administrator for this site?
* `readonly_site_admin` (boolean): Is the user a read-only administrator for this site?
* `skip_welcome_screen` (boolean): Skip the welcome screen?
* `externally_managed` (boolean): Is this user automatically managed?
* `time_zone` (string): User time zone
* `type_of_2fa` (string): 2fa type
* `reauth_2fa` (string): 2fa type
* `user_id` (int64): User ID
* `user_language` (string): Preferred language
* `user_login_url` (string): URL where this user can login
* `user_root` (string): User filesystem root
* `username` (string): User's username
* `web_root` (string): Root web folder
* `workspace_admin` (boolean): Is the user a Workspace administrator?
* `workspace_scoped` (boolean): Is the current response scoped to a specific workspace?
* `nps_response_requested` (boolean): Has the user been asked to respond to an NPS survey?
* `active_region_count` (int64): Number of active Storage Regions in use
* `admins_bypass_locked_subfolders` (boolean): Allow admins to bypass the locked subfolders setting.
* `additional_text_file_types` (array(string)): Additional extensions that are considered text files
* `text_preview_extensions` (array(string)): Extensions that are treated as text previews.
* `allowed_2fa_method_bypass_for_ftp_sftp_dav` (boolean): Are users allowed to configure their two factor authentication to be bypassed for FTP/SFTP/WebDAV?
* `allowed_2fa_method_sms` (boolean): Is SMS two factor authentication allowed?
* `allowed_2fa_method_totp` (boolean): Is TOTP two factor authentication allowed?
* `allowed_2fa_method_webauthn` (boolean): Is WebAuthn two factor authentication allowed?
* `allowed_2fa_method_yubi` (boolean): Is yubikey two factor authentication allowed?
* `allowed_2fa_method_email` (boolean): Is OTP via email two factor authentication allowed?
* `allowed_2fa_method_static` (boolean): Is OTP via static codes for two factor authentication allowed?
* `allow_bundle_names` (boolean): Are manual Bundle names allowed?
* `allow_user_level_2fa_override` (boolean): Allow the site-wide two-factor authentication requirement to be overriden on a per-user-basis?
* `require_2fa_exempt_all_sso_users` (boolean): If true, SSO users using the default user-level two-factor authentication setting are exempt from the site-wide two-factor authentication requirement.
* `allow_user_level_allowed_ip_override` (boolean): Allow the site-wide allowed IP restriction to be overriden on a per-user-basis?
* `allow_user_level_ssl_override` (boolean): Allow the site-wide FTP SSL requirement to be overriden on a per-user-basis?
* `bundle_recipient_blacklist_free_email_domains` (boolean): Are free email domains allowed for bundle and inbox recipients?
* `bundle_recipient_blacklist_domains` (array(string)): List of domains that are not allowed for bundle and inbox recipients
* `bundle_activity_notifications` (string): Do Bundle owners receive activity notifications?
* `bundle_expiration` (int64): Site-wide bundle expiration in days
* `bundle_password_required` (boolean): Do bundle shares require password protection?
* `bundle_registration_notifications` (string): Do Bundle owners receive registration notification?
* `bundle_require_registration` (boolean): Do Bundles require registration?
* `bundle_require_share_recipient` (boolean): Do bundles require recipients for sharing?
* `bundle_require_note` (boolean): Do bundles require a note?
* `bundle_upload_receipt_notifications` (string): Do Bundle uploaders receive upload confirmation notification?
* `child_site_count_for_plan` (int64): Number of child sites available
* `desktop_app` (boolean): Is the desktop app enabled?
* `exavault_api_available` (boolean): Is legacy ExaVault API Available?
* `feature_bundle_eca` (boolean): Does the site's plan include the ECA Feature bundle?
* `feature_bundle_power` (boolean): Does the site's plan include the Power Feature bundle?
* `feature_bundle_premier` (boolean): Does the site's plan include the Enterprise Feature bundle?
* `folder_permissions_groups_only` (boolean): If true, permissions for this site must be bound to a group (not a user).
* `group_admins_can_add_users` (boolean): Allow group admins to create users in their groups
* `group_admins_can_delete_users` (boolean): Allow group admins to delete users in their groups
* `group_admins_can_enable_disable_users` (boolean): Allow group admins to enable or disable users in their groups
* `group_admins_can_modify_users` (boolean): Allow group admins to modify users in their groups
* `group_admins_can_bypass_user_lifecycle_rules` (boolean): Allow group admins to exempt users in their groups from lifecycle rules
* `group_admins_can_reset_passwords` (boolean): Allow group admins to reset passwords for users in their groups
* `group_admins_can_set_user_password` (boolean): Allow group admins set password authentication method
* `has_account` (boolean): Connected to an account?
* `hide_billing` (boolean): Hide billing information?
* `high_users_count` (boolean): Does the site have a large number of users?  (Used to hide some UI features that may be slow in this case.)
* `history_unavailable` (boolean): Is history unavailable?
* `immutable_files` (boolean): Are files protected from modification?
* `intersitial_page` (string): Intersitial page to show
* `is_child_site` (boolean): Is this a child site?
* `left_navigation_visibility` (object): Visibility settings for account navigation
* `min_remote_sync_interval` (int64): Minimum remote server sync interval allowed by plan (in minutes)
* `non_sso_groups_allowed` (boolean): If true, groups can be manually created / modified / deleted by Site Admins. Otherwise, groups can only be managed via your SSO provider.
* `non_sso_users_allowed` (boolean): If true, users can be manually created / modified / deleted by Site Admins. Otherwise, users can only be managed via your SSO provider.
* `overdue` (boolean): Is billing overdue?
* `site_unavailable` (boolean): Is the site unavailable?
* `password_min_length` (int64): Shortest password length for users
* `password_require_letter` (boolean): Require a letter in passwords?
* `password_require_mixed` (boolean): Require lower and upper case letters in passwords?
* `password_require_number` (boolean): Require a number in passwords?
* `password_require_special` (boolean): Require special characters in password?
* `password_require_unbreached` (boolean): Require passwords that have not been previously breached? (see https://haveibeenpwned.com/)
* `password_requirements_apply_to_bundles` (boolean): Do site-wide password requirements apply to bundles?
* `plan_as2_included` (boolean): Does current plan include AS2 functionality?
* `prevent_root_permissions_for_non_site_admins` (boolean): Prevent regular users to be granted with root folder permissions
* `protocol_access_groups_only` (boolean): If `true`, protocol access permissions on users will be ignored, and only protocol access permissions set on Groups will be honored.  Make sure that your current user is a member of a group with API permission when changing this value to avoid locking yourself out of your site.
* `public_url` (string): Site public url
* `public_sharing_allowed` (boolean): Is public sharing allowed?
* `require_2fa` (boolean): Require two-factor authentication for the current user?
* `root_region` (string): Root region of site.  Used for SSL certificate termination, IP Address assignment, and regional pinning of remote servers.  If blank, assume us-east-1.
* `revoke_bundle_access_on_disable_or_delete` (boolean): Auto-removes bundles for disabled/deleted users and enforces bundle expiry within user access period.
* `sharing_enabled` (boolean): Allow bundle creation
* `snapshot_sharing_enabled` (boolean): Allow snapshot bundle creation
* `staging_site_count_for_plan` (int64): Number of child sites available
* `trial_flagged_as_duplicate` (boolean): Has this site been flagged as a duplicate of another trial?
* `trial_days_left` (int64): Number of days left in trial
* `trial_locked` (boolean): Is this site a free trial that is locked due to fraud concerns?
* `trial_until` (date-time): When does this Site trial expire?
* `usage_included` (int64): Usage included in site's plan, in GB
* `users_can_create_api_keys` (boolean): Allow users to create their own API keys?
* `users_can_create_ssh_keys` (boolean): Allow users to create their own SSH keys?
* `migrate_remote_server_sync_to_sync` (boolean): If true, we will migrate all remote server syncs to the new Sync model.
* `users_count` (int64): Count of users on the site.  Only exposed for site admins.
* `session_available_sites` (array(object)): All sites that this user has access to.
* `impersonator_user_id` (int64): User ID of the Site Admin who initiated a Read-Only session impersonating this session's user
