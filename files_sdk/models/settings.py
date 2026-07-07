import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Settings:
    default_attributes = {
        "image_regex": None,  # string - All supported image types
        "video_regex": None,  # string - All supported video types
        "audio_regex": None,  # string - All supported audio types
        "pdf_regex": None,  # string - All supported PDF types
        "current_language": None,  # string - Current language locale setting
        "current_time": None,  # date-time - Current Time in UTC
        "linode_regions": None,  # array(object) - Region name and description
        "wasabi_regions": None,  # array(object) - Region name and description
        "primary_sub_domain_base": None,  # string - Primary domain name base of the site
        "read_only": None,  # boolean - Is this session read only?
        "reauth": None,  # boolean - Password check skipped?
        "regions": None,  # array(object) - Region name and description
        "s3_regions": None,  # array(object) - Region name and description
        "sales_tax_regions": None,  # array(object) - States with applicable sales tax
        "session_language": None,  # string - Session locale setting
        "tab_config": None,  # string - Deprecated
        "allow_bypassing_2fa_policies": None,  # boolean - Can users bypass 2FA policies?
        "allow_credential_changes": None,  # boolean - Can partner admins manage user credentials?
        "allow_providing_gpg_keys": None,  # boolean - Can partner admins provide their own GPG keys?
        "allow_user_creation": None,  # boolean - Can partner admins create new users?
        "bundle_not_found_message": None,  # string - Custom error message to show when bundle is not found.
        "beta_features": None,  # boolean - Is beta feature 1 available?
        "beta_feature2": None,  # boolean - Is beta feature 2 available?
        "beta_feature3": None,  # boolean - Is beta feature 3 available?
        "calculate_file_checksums_crc32": None,  # boolean - Calculate CRC32 checksum for incoming files?
        "calculate_file_checksums_md5": None,  # boolean - Calculate MD5 checksum for incoming files?
        "calculate_file_checksums_sha1": None,  # boolean - Calculate SHA1 checksum for incoming files?
        "calculate_file_checksums_sha256": None,  # boolean - Calculate SHA256 checksum for incoming files?
        "color2_left": None,  # string - Page link and button color
        "color2_link": None,  # string - Top bar link color
        "color2_text": None,  # string - Page link and button color
        "color2_top": None,  # string - Top bar background color
        "color2_top_text": None,  # string - Top bar text color
        "document_edits_in_bundle_allowed": None,  # boolean - If true, allow public viewers of Bundles with full permissions to use document editing integrations.
        "domain": None,  # string - Custom domain
        "disable_password_reset": None,  # boolean - Is password reset disabled?
        "login_clickwrap_body": None,  # string - Clickwrap body text to show on every web login.
        "pending_clickwrap_id": None,  # int64 - ID of clickwrap the user must accept.
        "pending_clickwrap_body": None,  # string - Body of clickwrap the user must accept.
        "disable_drive_mounting": None,  # boolean - Whether the desktop app should hide drive mounting, prevent new drive mounts, and unmount active drive mounts.
        "desktop_drive_mappings": None,  # object - Mappings from drive letters to paths for the desktop application.
        "remote_desktop_debug_logging_enabled": None,  # boolean - Whether remote desktop debug log upload is enabled for this user.
        "remote_desktop_debug_logging_expires_at": None,  # date-time - When remote desktop debug logging expires for this user.
        "has_workspaces": None,  # boolean - True if the current user can access any named Workspaces (id > 0).
        "has_accessible_gpg_keys": None,  # boolean - True if the current user has access to any GPG keys.
        "default_workspace_id": None,  # int64 - Workspace ID the user should land in by default when more than one Workspace is available.
        "legacy_checksums_mode": None,  # boolean - Use legacy checksums mode?
        "login_help_text": None,  # string - Login help text (as HTML).  Unsafe! Deprecated! Do Not Use!
        "login_help_text_markdown": None,  # string - Login help text (as Markdown)
        "site_name": None,  # string - Site name
        "office_integration_type": None,  # string - Which document editing integration to support. Files.com Editor or Microsoft Office for the Web.
        "office_integration_enabled": None,  # boolean - If true, allows users to use a document editing integration.
        "office_integration_host": None,  # string - Document editing integration hostname for API calls.
        "oncehub_link": None,  # string - Link to scheduling a meeting with our Sales team
        "office_integration_available": None,  # boolean - If true, allows users to use a document editing integration.
        "require_logout_from_bundles_and_inboxes": None,  # boolean - If true, we will hide the 'Remember Me' box on Inbox and Bundle registration pages, requiring that the user logout and log back in every time they visit the page.
        "self_signup_eligible": None,  # boolean - Is self signup available?
        "show_request_access_link": None,  # boolean - Show request access link for users without access?
        "site_footer_markdown": None,  # string - Site footer for branding (as Markdown) on authenticated (logged-in) user pages
        "site_header_markdown": None,  # string - Site header for branding (as Markdown) on authenticated (logged-in) user pages
        "email_footer_custom_text_markdown": None,  # string - Custom footer text for system-generated emails. Supports strftime patterns like %Y (4-digit year), %m (month), %d (day).
        "site_public_header_markdown": None,  # string - Site header for branding (as Markdown) on public (unauthenticated) pages.
        "site_public_footer_markdown": None,  # string - Site footer for branding (as Markdown) on public (unauthenticated) pages.
        "site_language": None,  # string - Site language locale
        "site_id": None,  # int64 - Site ID
        "sso_strategies": None,  # SsoStrategy - SSO strategies in use
        "subdomain": None,  # string - Site subdomain
        "use_provided_modified_at": None,  # boolean - Allow setting provided_modified_at?
        "user_requests_enabled": None,  # boolean - Is the user requests feature enabled?
        "welcome_screen": None,  # string - Does the welcome screen appear? Can be `enabled`, `hidden`, or `disabled`
        "icon128": None,  # Image - Branded icon 128x128
        "icon16": None,  # Image - Branded icon 16x16
        "icon32": None,  # Image - Branded icon 32x32
        "icon48": None,  # Image - Branded icon 48x48
        "logo": None,  # Image - Branded logo
        "login_page_background_image": None,  # Image - Branded login page background
        "logo_thumbnail": None,  # Image - Branded Logo thumbnail
        "login_page_background_image_thumbnail": None,  # Image - Branded login page background thumbnail
        "attachments_permission": None,  # boolean
        "authentication_method": None,  # string - Authentication method for the user.  Can be `password`, `sso`, or `none`
        "avatar_url": None,  # string - URL holding the user's avatar
        "billing_permission": None,  # boolean - Allow this user to perform operations on the account, payments, and invoices?
        "cached_permissions": None,  # array(object) - All permissions applicable to this user, including permissions inherited via groups.
        "can_admin_somewhere": None,  # boolean - If true, user has admin permissions somewhere on the site.
        "can_bundle_somewhere": None,  # boolean - If true, user has bundle permissions somewhere on the site.
        "can_write_somewhere": None,  # boolean - If true, user has write, full, or admin permissions somewhere on the site.
        "dav_permission": None,  # boolean - Can the user connect with WebDAV?
        "days_remaining_until_password_expire": None,  # int64 - Number of days remaining until password expires
        "email": None,  # email - User email address
        "ftp_permission": None,  # boolean - Can the user access with FTP/FTPS?
        "group_admin": None,  # boolean - Is a group administrator?
        "header_text": None,  # string - Text to display to the user in the header of the UI
        "in_app_ai_assistant_available": None,  # boolean - Is the in-app AI assistant available to the current user?
        "ai_assistant_personality_id": None,  # int64 - AI Assistant Personality ID for the in-app AI Assistant.
        "ai_assistant_personality_system_prompt": None,  # string - System prompt for the in-app AI Assistant.
        "file_transform_capabilities": None,  # object - Supported file transform input and output formats
        "id": None,  # int64 - User ID
        "last_read_announcements_at": None,  # date-time - The last date/time this user has read announcements
        "name": None,  # string - User name
        "notification_daily_send_time": None,  # int64 - Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
        "notify_on_all_site_warnings": None,  # boolean - Should the user receive site warnings via email?
        "notify_on_all_sso_failures": None,  # boolean - Should the user receive sso/scim/ldap configuration/sync failures via email?
        "notify_on_all_user_security_events": None,  # boolean - Should the user receive user security events via email?
        "notify_on_all_pending_work_failures": None,  # boolean - Should the user receive pending work failures via email?
        "notify_on_all_siem_http_destination_failures": None,  # boolean - Should the user receive siem failures via email?
        "notify_on_all_sync_failures": None,  # boolean - Should the user receive sync failures via email?
        "notify_on_all_automation_failures": None,  # boolean - Should the user receive automation failures via email?
        "notify_on_all_expectation_failures": None,  # boolean - Should the user receive expectation failures and misses via email?
        "partner_admin": None,  # boolean - Is this user a Partner administrator?
        "primary_group_id": None,  # int64 - Primary group ID for Group Admin scoping
        "partner_id": None,  # int64 - Partner ID, if applicable.
        "root_folder_restricted": None,  # boolean - Does this user use a File System Layout that restricts creating Files, Folders, or Settings in the Root Folder?
        "self_managed": None,  # boolean - Does this user manage it's own credentials?
        "sftp_permission": None,  # boolean - Can the user access with SFTP?
        "site_admin": None,  # boolean - Is the user an administrator for this site?
        "readonly_site_admin": None,  # boolean - Is the user a read-only administrator for this site?
        "skip_welcome_screen": None,  # boolean - Skip the welcome screen?
        "externally_managed": None,  # boolean - Is this user automatically managed?
        "time_zone": None,  # string - User time zone
        "type_of_2fa": None,  # string - 2fa type
        "reauth_2fa": None,  # string - 2fa type
        "user_id": None,  # int64 - User ID
        "user_language": None,  # string - Preferred language
        "user_login_url": None,  # string - URL where this user can login
        "user_root": None,  # string - User filesystem root
        "username": None,  # string - User's username
        "web_root": None,  # string - Root web folder
        "workspace_admin": None,  # boolean - Is the user a Workspace administrator?
        "workspace_scoped": None,  # boolean - Is the current response scoped to a specific workspace?
        "nps_response_requested": None,  # boolean - Has the user been asked to respond to an NPS survey?
        "active_region_count": None,  # int64 - Number of active Storage Regions in use
        "admins_bypass_locked_subfolders": None,  # boolean - Allow admins to bypass the locked subfolders setting.
        "additional_text_file_types": None,  # array(string) - Additional extensions that are considered text files
        "text_preview_extensions": None,  # array(string) - Extensions that are treated as text previews.
        "allowed_2fa_method_bypass_for_ftp_sftp_dav": None,  # boolean - Are users allowed to configure their two factor authentication to be bypassed for FTP/SFTP/WebDAV?
        "allowed_2fa_method_sms": None,  # boolean - Is SMS two factor authentication allowed?
        "allowed_2fa_method_totp": None,  # boolean - Is TOTP two factor authentication allowed?
        "allowed_2fa_method_webauthn": None,  # boolean - Is WebAuthn two factor authentication allowed?
        "allowed_2fa_method_yubi": None,  # boolean - Is yubikey two factor authentication allowed?
        "allowed_2fa_method_email": None,  # boolean - Is OTP via email two factor authentication allowed?
        "allowed_2fa_method_static": None,  # boolean - Is OTP via static codes for two factor authentication allowed?
        "allow_bundle_names": None,  # boolean - Are manual Bundle names allowed?
        "allow_user_level_2fa_override": None,  # boolean - Allow the site-wide two-factor authentication requirement to be overriden on a per-user-basis?
        "require_2fa_exempt_all_sso_users": None,  # boolean - If true, SSO users using the default user-level two-factor authentication setting are exempt from the site-wide two-factor authentication requirement.
        "allow_user_level_allowed_ip_override": None,  # boolean - Allow the site-wide allowed IP restriction to be overriden on a per-user-basis?
        "allow_user_level_ssl_override": None,  # boolean - Allow the site-wide FTP SSL requirement to be overriden on a per-user-basis?
        "bundle_recipient_blacklist_free_email_domains": None,  # boolean - Are free email domains allowed for bundle and inbox recipients?
        "bundle_recipient_blacklist_domains": None,  # array(string) - List of domains that are not allowed for bundle and inbox recipients
        "bundle_activity_notifications": None,  # string - Do Bundle owners receive activity notifications?
        "bundle_expiration": None,  # int64 - Site-wide bundle expiration in days
        "bundle_password_required": None,  # boolean - Do bundle shares require password protection?
        "bundle_registration_notifications": None,  # string - Do Bundle owners receive registration notification?
        "bundle_require_registration": None,  # boolean - Do Bundles require registration?
        "bundle_require_share_recipient": None,  # boolean - Do bundles require recipients for sharing?
        "bundle_require_note": None,  # boolean - Do bundles require a note?
        "bundle_upload_receipt_notifications": None,  # string - Do Bundle uploaders receive upload confirmation notification?
        "child_site_count_for_plan": None,  # int64 - Number of child sites available
        "desktop_app": None,  # boolean - Is the desktop app enabled?
        "exavault_api_available": None,  # boolean - Is legacy ExaVault API Available?
        "feature_bundle_eca": None,  # boolean - Does the site's plan include the ECA Feature bundle?
        "feature_bundle_power": None,  # boolean - Does the site's plan include the Power Feature bundle?
        "feature_bundle_premier": None,  # boolean - Does the site's plan include the Enterprise Feature bundle?
        "folder_permissions_groups_only": None,  # boolean - If true, permissions for this site must be bound to a group (not a user).
        "group_admins_can_add_users": None,  # boolean - Allow group admins to create users in their groups
        "group_admins_can_delete_users": None,  # boolean - Allow group admins to delete users in their groups
        "group_admins_can_enable_disable_users": None,  # boolean - Allow group admins to enable or disable users in their groups
        "group_admins_can_modify_users": None,  # boolean - Allow group admins to modify users in their groups
        "group_admins_can_bypass_user_lifecycle_rules": None,  # boolean - Allow group admins to exempt users in their groups from lifecycle rules
        "group_admins_can_reset_passwords": None,  # boolean - Allow group admins to reset passwords for users in their groups
        "group_admins_can_set_user_password": None,  # boolean - Allow group admins set password authentication method
        "has_account": None,  # boolean - Connected to an account?
        "hide_billing": None,  # boolean - Hide billing information?
        "high_users_count": None,  # boolean - Does the site have a large number of users?  (Used to hide some UI features that may be slow in this case.)
        "history_unavailable": None,  # boolean - Is history unavailable?
        "immutable_files": None,  # boolean - Are files protected from modification?
        "intersitial_page": None,  # string - Intersitial page to show
        "is_child_site": None,  # boolean - Is this a child site?
        "left_navigation_visibility": None,  # object - Visibility settings for account navigation
        "min_remote_sync_interval": None,  # int64 - Minimum remote server sync interval allowed by plan (in minutes)
        "non_sso_groups_allowed": None,  # boolean - If true, groups can be manually created / modified / deleted by Site Admins. Otherwise, groups can only be managed via your SSO provider.
        "non_sso_users_allowed": None,  # boolean - If true, users can be manually created / modified / deleted by Site Admins. Otherwise, users can only be managed via your SSO provider.
        "overdue": None,  # boolean - Is billing overdue?
        "site_unavailable": None,  # boolean - Is the site unavailable?
        "password_min_length": None,  # int64 - Shortest password length for users
        "password_require_letter": None,  # boolean - Require a letter in passwords?
        "password_require_mixed": None,  # boolean - Require lower and upper case letters in passwords?
        "password_require_number": None,  # boolean - Require a number in passwords?
        "password_require_special": None,  # boolean - Require special characters in password?
        "password_require_unbreached": None,  # boolean - Require passwords that have not been previously breached? (see https://haveibeenpwned.com/)
        "password_requirements_apply_to_bundles": None,  # boolean - Do site-wide password requirements apply to bundles?
        "plan_as2_included": None,  # boolean - Does current plan include AS2 functionality?
        "prevent_root_permissions_for_non_site_admins": None,  # boolean - Prevent regular users to be granted with root folder permissions
        "protocol_access_groups_only": None,  # boolean - If `true`, protocol access permissions on users will be ignored, and only protocol access permissions set on Groups will be honored.  Make sure that your current user is a member of a group with API permission when changing this value to avoid locking yourself out of your site.
        "public_url": None,  # string - Site public url
        "public_sharing_allowed": None,  # boolean - Is public sharing allowed?
        "require_2fa": None,  # boolean - Require two-factor authentication for the current user?
        "root_region": None,  # string - Root region of site.  Used for SSL certificate termination, IP Address assignment, and regional pinning of remote servers.  If blank, assume us-east-1.
        "revoke_bundle_access_on_disable_or_delete": None,  # boolean - Auto-removes bundles for disabled/deleted users and enforces bundle expiry within user access period.
        "sharing_enabled": None,  # boolean - Allow bundle creation
        "snapshot_sharing_enabled": None,  # boolean - Allow snapshot bundle creation
        "staging_site_count_for_plan": None,  # int64 - Number of child sites available
        "trial_flagged_as_duplicate": None,  # boolean - Has this site been flagged as a duplicate of another trial?
        "trial_days_left": None,  # int64 - Number of days left in trial
        "trial_locked": None,  # boolean - Is this site a free trial that is locked due to fraud concerns?
        "trial_until": None,  # date-time - When does this Site trial expire?
        "usage_included": None,  # int64 - Usage included in site's plan, in GB
        "users_can_create_api_keys": None,  # boolean - Allow users to create their own API keys?
        "users_can_create_ssh_keys": None,  # boolean - Allow users to create their own SSH keys?
        "migrate_remote_server_sync_to_sync": None,  # boolean - If true, we will migrate all remote server syncs to the new Sync model.
        "users_count": None,  # int64 - Count of users on the site.  Only exposed for site admins.
        "session_available_sites": None,  # array(object) - All sites that this user has access to.
        "impersonator_user_id": None,  # int64 - User ID of the Site Admin who initiated a Read-Only session impersonating this session's user
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Settings.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Settings.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return Settings(*args, **kwargs)
