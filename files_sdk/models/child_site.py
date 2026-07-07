import builtins  # noqa: F401
from decimal import Decimal
from files_sdk.models.site import Site
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ChildSite:
    __decimal_fields = {
        "next_billing_amount",
    }
    __decimal_array_fields = {}
    default_attributes = {
        "id": None,  # int64 - Site Id
        "name": None,  # string - Site name
        "additional_text_file_types": None,  # array(string) - Additional extensions that are considered text files
        "ai_feature_availability": None,  # object - Availability settings for AI features by user class
        "allowed_2fa_method_sms": None,  # boolean - Is SMS two factor authentication allowed?
        "allowed_2fa_method_totp": None,  # boolean - Is TOTP two factor authentication allowed?
        "allowed_2fa_method_webauthn": None,  # boolean - Is WebAuthn two factor authentication allowed?
        "allowed_2fa_method_yubi": None,  # boolean - Is yubikey two factor authentication allowed?
        "allowed_2fa_method_email": None,  # boolean - Is OTP via email two factor authentication allowed?
        "allowed_2fa_method_static": None,  # boolean - Is OTP via static codes for two factor authentication allowed?
        "allowed_2fa_method_bypass_for_ftp_sftp_dav": None,  # boolean - Are users allowed to configure their two factor authentication to be bypassed for FTP/SFTP/WebDAV?
        "admin_user_id": None,  # int64 - User ID for the main site administrator
        "admins_bypass_locked_subfolders": None,  # boolean - Allow admins to bypass the locked subfolders setting.
        "allow_bundle_names": None,  # boolean - Are manual Bundle names allowed?
        "allow_user_level_2fa_override": None,  # boolean - Allow the site-wide two-factor authentication requirement to be overriden on a per-user-basis?
        "allow_user_level_allowed_ip_override": None,  # boolean - Allow the site-wide allowed IP restriction to be overriden on a per-user-basis?
        "allow_user_level_ssl_override": None,  # boolean - Allow the site-wide FTP SSL requirement to be overriden on a per-user-basis?
        "allowed_countries": None,  # string - Comma separated list of allowed Country codes
        "allowed_ips": None,  # string - List of allowed IP addresses
        "always_mkdir_parents": None,  # boolean - Create parent directories if they do not exist during uploads?  This is primarily used to work around broken upload clients that assume servers will perform this step.
        "as2_message_retention_days": None,  # int64 - Number of days to retain AS2 messages (incoming and outgoing).
        "ask_about_overwrites": None,  # boolean - If false, rename conflicting files instead of asking for overwrite confirmation.  Only applies to web interface.
        "bundle_activity_notifications": None,  # string - Do Bundle owners receive activity notifications?
        "bundle_expiration": None,  # int64 - Site-wide Bundle expiration in days
        "bundle_not_found_message": None,  # string - Custom error message to show when bundle is not found.
        "bundle_password_required": None,  # boolean - Do Bundles require password protection?
        "bundles_default_owned_by_primary_group": None,  # boolean - If true, new Share Links created by a user with a primary group will default to that group as owner.
        "bundle_recipient_blacklist_domains": None,  # array(string) - List of email domains to disallow when entering a Bundle/Inbox recipients
        "bundle_recipient_blacklist_free_email_domains": None,  # boolean - Disallow free email domains for Bundle/Inbox recipients?
        "bundle_registration_notifications": None,  # string - Do Bundle owners receive registration notification?
        "bundle_require_registration": None,  # boolean - Do Bundles require registration?
        "bundle_require_share_recipient": None,  # boolean - Do Bundles require recipients for sharing?
        "bundle_require_note": None,  # boolean - Do Bundles require internal notes?
        "bundle_send_shared_receipts": None,  # boolean - Do Bundle creators receive receipts of invitations?
        "bundle_upload_receipt_notifications": None,  # string - Do Bundle uploaders receive upload confirmation notifications?
        "bundle_watermark_attachment": None,  # Image - Preview watermark image applied to all bundle items.
        "bundle_watermark_value": None,  # object - Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
        "calculate_file_checksums_crc32": None,  # boolean - Calculate CRC32 checksums for files?
        "calculate_file_checksums_md5": None,  # boolean - Calculate MD5 checksums for files?
        "calculate_file_checksums_sha1": None,  # boolean - Calculate SHA1 checksums for files?
        "calculate_file_checksums_sha256": None,  # boolean - Calculate SHA256 checksums for files?
        "uploads_via_email_authentication": None,  # boolean - Do incoming emails in the Inboxes require checking for SPF/DKIM/DMARC?
        "color2_left": None,  # string - Page link and button color
        "color2_link": None,  # string - Top bar link color
        "color2_text": None,  # string - Page link and button color
        "color2_top": None,  # string - Top bar background color
        "color2_top_text": None,  # string - Top bar text color
        "contact_name": None,  # string - Site main contact name
        "created_at": None,  # date-time - Time this site was created
        "currency": None,  # string - Preferred currency
        "custom_namespace": None,  # boolean - Is this site using a custom namespace for users?
        "dav_enabled": None,  # boolean - Is WebDAV enabled?
        "dav_user_root_enabled": None,  # boolean - Use user FTP roots also for WebDAV?
        "days_to_retain_backups": None,  # int64 - Number of days to keep deleted files
        "document_edits_in_bundle_allowed": None,  # boolean - If true, allow public viewers of Bundles with full permissions to use document editing integrations.
        "default_time_zone": None,  # string - Site default time zone
        "desktop_app": None,  # boolean - Is the desktop app enabled?
        "desktop_app_session_ip_pinning": None,  # boolean - Is desktop app session IP pinning enabled?
        "desktop_app_session_lifetime": None,  # int64 - Desktop app session lifetime (in hours)
        "legacy_checksums_mode": None,  # boolean - Use legacy checksums mode?
        "migrate_remote_server_sync_to_sync": None,  # boolean - If true, we will migrate all remote server syncs to the new Sync model.
        "mcp_dcr_enabled": None,  # boolean - Is OAuth DCR (dynamic client registration) for MCP enabled?
        "mobile_app": None,  # boolean - Is the mobile app enabled?
        "mobile_app_session_ip_pinning": None,  # boolean - Is mobile app session IP pinning enabled?
        "mobile_app_session_lifetime": None,  # int64 - Mobile app session lifetime (in hours)
        "disallowed_countries": None,  # string - Comma separated list of disallowed Country codes
        "disable_all_ai_features": None,  # boolean - If true, all AI features are disabled for this site.
        "disable_files_certificate_generation": None,  # boolean - If set, Files.com will not set the CAA records required to generate future SSL certificates for this domain.
        "disable_notifications": None,  # boolean - Are notifications disabled?
        "disable_password_reset": None,  # boolean - Is password reset disabled?
        "domain": None,  # string - Custom domain
        "domain_hsts_header": None,  # boolean - Send HSTS (HTTP Strict Transport Security) header when visitors access the site via a custom domain?
        "domain_letsencrypt_chain": None,  # string - Letsencrypt chain to use when registering SSL Certificate for domain. No longer used as of 2026.
        "email": None,  # email - Main email for this site
        "ftp_enabled": None,  # boolean - Is FTP enabled?
        "reply_to_email": None,  # email - Reply-to email for this site
        "non_sso_groups_allowed": None,  # boolean - If true, groups can be manually created / modified / deleted by Site Admins. Otherwise, groups can only be managed via your SSO provider.
        "non_sso_users_allowed": None,  # boolean - If true, users can be manually created / modified / deleted by Site Admins. Otherwise, users can only be managed via your SSO provider.
        "folder_permissions_groups_only": None,  # boolean - If true, permissions for this site must be bound to a group (not a user).
        "group_admins_can_add_users": None,  # boolean - Allow group admins to create users in their groups
        "group_admins_can_delete_users": None,  # boolean - Allow group admins to delete users in their groups
        "group_admins_can_enable_disable_users": None,  # boolean - Allow group admins to enable or disable users in their groups
        "group_admins_can_modify_users": None,  # boolean - Allow group admins to modify users in their groups
        "group_admins_can_bypass_user_lifecycle_rules": None,  # boolean - Allow group admins to exempt users in their groups from lifecycle rules
        "group_admins_can_reset_passwords": None,  # boolean - Allow group admins to reset passwords for users in their groups
        "group_admins_can_set_user_password": None,  # boolean - Allow group admins to set password authentication method
        "hipaa": None,  # boolean - Is there a signed HIPAA BAA between Files.com and this site?
        "icon128": None,  # Image - Branded icon 128x128
        "icon16": None,  # Image - Branded icon 16x16
        "icon32": None,  # Image - Branded icon 32x32
        "icon48": None,  # Image - Branded icon 48x48
        "immutable_files_set_at": None,  # date-time - Can files be modified?
        "include_password_in_welcome_email": None,  # boolean - Include password in emails to new users?
        "language": None,  # string - Site default language
        "ldap_base_dn": None,  # string - Base DN for looking up users in LDAP server
        "ldap_domain": None,  # string - Domain name that will be appended to usernames
        "ldap_enabled": None,  # boolean - Main LDAP setting: is LDAP enabled?
        "ldap_group_action": None,  # string - Should we sync groups from LDAP server?
        "ldap_group_exclusion": None,  # string - Comma or newline separated list of group names (with optional wildcards) to exclude when syncing.
        "ldap_group_inclusion": None,  # string - Comma or newline separated list of group names (with optional wildcards) to include when syncing.
        "ldap_host": None,  # string - LDAP host
        "ldap_host_2": None,  # string - LDAP backup host
        "ldap_host_3": None,  # string - LDAP backup host
        "ldap_port": None,  # int64 - LDAP port
        "ldap_secure": None,  # boolean - Use secure LDAP?
        "ldap_type": None,  # string - LDAP type
        "ldap_user_action": None,  # string - Should we sync users from LDAP server?
        "ldap_user_include_groups": None,  # string - Comma or newline separated list of group names (with optional wildcards) - if provided, only users in these groups will be added or synced.
        "ldap_username": None,  # string - Username for signing in to LDAP server.
        "ldap_username_field": None,  # string - LDAP username field
        "login_help_text": None,  # string - Login help text
        "logo": None,  # Image - Branded logo
        "login_page_background_image": None,  # Image - Branded login page background
        "max_prior_passwords": None,  # int64 - Number of prior passwords to disallow
        "managed_site_settings": None,  # object - List of site settings managed by the parent site
        "motd_text": None,  # string - A message to show users when they connect via FTP or SFTP.
        "motd_use_for_ftp": None,  # boolean - Show message to users connecting via FTP
        "motd_use_for_sftp": None,  # boolean - Show message to users connecting via SFTP
        "next_billing_amount": None,  # decimal - Next billing amount
        "next_billing_date": None,  # string - Next billing date
        "office_integration_available": None,  # boolean - If true, allows users to use a document editing integration.
        "office_integration_type": None,  # string - Which document editing integration to support. Files.com Editor or Microsoft Office for the Web.
        "oncehub_link": None,  # string - Link to scheduling a meeting with our Sales team
        "opt_out_global": None,  # boolean - Use servers in the USA only?
        "overdue": None,  # boolean - Is this site's billing overdue?
        "password_min_length": None,  # int64 - Shortest password length for users
        "password_require_letter": None,  # boolean - Require a letter in passwords?
        "password_require_mixed": None,  # boolean - Require lower and upper case letters in passwords?
        "password_require_number": None,  # boolean - Require a number in passwords?
        "password_require_special": None,  # boolean - Require special characters in password?
        "password_require_unbreached": None,  # boolean - Require passwords that have not been previously breached? (see https://haveibeenpwned.com/)
        "password_requirements_apply_to_bundles": None,  # boolean - Require bundles' passwords, and passwords for other items (inboxes, public shares, etc.) to conform to the same requirements as users' passwords?
        "password_validity_days": None,  # int64 - Number of days password is valid
        "phone": None,  # string - Site phone number
        "pin_all_remote_servers_to_site_region": None,  # boolean - If true, we will ensure that all internal communications with any remote server are made through the primary region of the site. This setting overrides individual remote server settings.
        "prevent_root_permissions_for_non_site_admins": None,  # boolean - If true, we will prevent non-administrators from receiving any permissions directly on the root folder.  This is commonly used to prevent the accidental application of permissions.
        "protocol_access_groups_only": None,  # boolean - If true, protocol access permissions on users will be ignored, and only protocol access permissions set on Groups will be honored.  Make sure that your current user is a member of a group with API permission when changing this value to avoid locking yourself out of your site.
        "require_2fa": None,  # boolean - Require two-factor authentication for all users?
        "require_2fa_exempt_all_sso_users": None,  # boolean - If true, SSO users using the default user-level two-factor authentication setting are exempt from the site-wide two-factor authentication requirement.
        "require_2fa_stop_time": None,  # date-time - If set, requirement for two-factor authentication has been scheduled to end on this date-time.
        "revoke_bundle_access_on_disable_or_delete": None,  # boolean - Auto-removes bundles for disabled/deleted users and enforces bundle expiry within user access period.
        "require_2fa_user_type": None,  # string - What type of user is required to use two-factor authentication (when require_2fa is set to `true` for this site)?
        "require_logout_from_bundles_and_inboxes": None,  # boolean - If true, we will hide the 'Remember Me' box on Inbox and Bundle registration pages, requiring that the user logout and log back in every time they visit the page.
        "session": None,  # Session - Current session
        "sftp_enabled": None,  # boolean - Is SFTP enabled?
        "sftp_finalize_partial_uploads": None,  # boolean - Finalize partial SFTP uploads from interrupted connections? Default: true.
        "sftp_host_key_type": None,  # string - Sftp Host Key Type
        "active_sftp_host_key_id": None,  # int64 - Id of the currently selected custom SFTP Host Key
        "sftp_insecure_ciphers": None,  # boolean - If true, we will allow weak and known insecure ciphers to be used for SFTP connections.  Enabling this setting severely weakens the security of your site and it is not recommend, except as a last resort for compatibility.
        "sftp_insecure_diffie_hellman": None,  # boolean - If true, we will allow weak Diffie Hellman parameters to be used within ciphers for SFTP that are otherwise on our secure list.  This has the effect of making the cipher weaker than our normal threshold for security, but is required to support certain legacy or broken SSH and MFT clients.  Enabling this weakens security, but not nearly as much as enabling the full `sftp_insecure_ciphers` option.
        "sftp_user_root_enabled": None,  # boolean - Use user FTP roots also for SFTP?
        "sharing_enabled": None,  # boolean - Allow bundle creation
        "show_user_notifications_log_in_link": None,  # boolean - Show log in link in user notifications?
        "show_request_access_link": None,  # boolean - Show request access link for users without access?  Currently unused.
        "site_footer": None,  # string - Custom site footer text for authenticated pages
        "site_header": None,  # string - Custom site header text for authenticated pages
        "site_public_footer": None,  # string - Custom site footer text for public pages
        "site_public_header": None,  # string - Custom site header text for public pages
        "smtp_address": None,  # string - SMTP server hostname or IP
        "smtp_authentication": None,  # string - SMTP server authentication type
        "smtp_from": None,  # string - From address to use when mailing through custom SMTP
        "smtp_port": None,  # int64 - SMTP server port
        "smtp_username": None,  # string - SMTP server username
        "session_expiry_minutes": None,  # int64 - Session expiry in minutes
        "snapshot_sharing_enabled": None,  # boolean - Allow snapshot share links creation
        "ssl_required": None,  # boolean - Is SSL required?  Disabling this is insecure.
        "subdomain": None,  # string - Site subdomain
        "switch_to_plan_date": None,  # date-time - If switching plans, when does the new plan take effect?
        "trial_days_left": None,  # int64 - Number of days left in trial
        "trial_until": None,  # date-time - When does this Site trial expire?
        "use_dedicated_ips_for_smtp": None,  # boolean - If using custom SMTP, should we use dedicated IPs to deliver emails?
        "use_provided_modified_at": None,  # boolean - Allow uploaders to set `provided_modified_at` for uploaded files?
        "user": None,  # User - User of current session
        "user_lockout": None,  # boolean - Will users be locked out after incorrect login attempts?
        "user_lockout_lock_period": None,  # int64 - How many hours to lock user out for failed password?
        "user_lockout_tries": None,  # int64 - Number of login tries within `user_lockout_within` hours before users are locked out
        "user_lockout_within": None,  # int64 - Number of hours for user lockout window
        "user_requests_enabled": None,  # boolean - Enable User Requests feature
        "user_requests_notify_admins": None,  # boolean - Send email to site admins when a user request is received?
        "users_can_create_api_keys": None,  # boolean - Allow users to create their own API keys?
        "users_can_create_ssh_keys": None,  # boolean - Allow users to create their own SSH keys?
        "username_display": None,  # string - How usernames are displayed in the web UI. Can be `username_only`, `full_name_only`, `full_name_username`, `full_name_company`, or `full_name_username_company`.
        "welcome_custom_text": None,  # string - Custom text send in user welcome email
        "email_footer_custom_text": None,  # string - Custom footer text for system-generated emails. Supports standard strftime date/time patterns like %Y (4-digit year), %m (month), %d (day).
        "welcome_email_cc": None,  # email - Include this email in welcome emails if enabled
        "welcome_email_subject": None,  # string - Include this email subject in welcome emails if enabled
        "welcome_email_enabled": None,  # boolean - Will the welcome email be sent to new users?
        "welcome_screen": None,  # string - Does the welcome screen appear?
        "windows_mode_ftp": None,  # boolean - Does FTP user Windows emulation mode?
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in ChildSite.default_attributes.items():
            value = attributes.get(attribute, default_value)
            if attribute in ChildSite.__decimal_fields and value is not None:
                value = Decimal(str(value))
            if (
                attribute in ChildSite.__decimal_array_fields
                and value is not None
            ):
                value = [Decimal(str(v)) for v in (value or [])]
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ChildSite.default_attributes
            if getattr(self, k, None) is not None
        }
        for k in list(attrs.keys()):
            if k in ChildSite.__decimal_fields and attrs[k] is not None:
                attrs[k] = str(attrs[k])
            if k in ChildSite.__decimal_array_fields and attrs[k] is not None:
                attrs[k] = [str(v) for v in (attrs[k] or [])]
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The ChildSite object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(Site, "GET", "/child_sites", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   name (required) - string
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    response, options = Api.send_request(
        "POST", "/child_sites", params, options
    )
    return Site(response.data, options)


def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, options = Api.send_request(
        "POST", "/child_sites/create_export", params, options
    )
    return Export(response.data, options)


def new(*args, **kwargs):
    return ChildSite(*args, **kwargs)
