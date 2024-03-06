import builtins  # noqa: F401
from files_sdk.models.usage_snapshot import UsageSnapshot
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Site:
    default_attributes = {
        "name": None,  # string - Site name
        "allowed_2fa_method_sms": None,  # boolean - Is SMS two factor authentication allowed?
        "allowed_2fa_method_totp": None,  # boolean - Is TOTP two factor authentication allowed?
        "allowed_2fa_method_u2f": None,  # boolean - Is U2F two factor authentication allowed?
        "allowed_2fa_method_webauthn": None,  # boolean - Is WebAuthn two factor authentication allowed?
        "allowed_2fa_method_yubi": None,  # boolean - Is yubikey two factor authentication allowed?
        "allowed_2fa_method_email": None,  # boolean - Is OTP via email two factor authentication allowed?
        "allowed_2fa_method_bypass_for_ftp_sftp_dav": None,  # boolean - Are users allowed to configure their two factor authentication to be bypassed for FTP/SFTP/WebDAV?
        "admin_user_id": None,  # int64 - User ID for the main site administrator
        "admins_bypass_locked_subfolders": None,  # boolean - Allow admins to bypass the locked subfolders setting.
        "allow_bundle_names": None,  # boolean - Are manual Bundle names allowed?
        "allowed_countries": None,  # string - Comma seperated list of allowed Country codes
        "allowed_ips": None,  # string - List of allowed IP addresses
        "ask_about_overwrites": None,  # boolean - If false, rename conflicting files instead of asking for overwrite confirmation.  Only applies to web interface.
        "bundle_activity_notifications": None,  # string - Do Bundle owners receive activity notifications?
        "bundle_expiration": None,  # int64 - Site-wide Bundle expiration in days
        "bundle_not_found_message": None,  # string - Custom error message to show when bundle is not found.
        "bundle_password_required": None,  # boolean - Do Bundles require password protection?
        "bundle_recipient_blacklist_domains": None,  # array - List of email domains to disallow when entering a Bundle/Inbox recipients
        "bundle_recipient_blacklist_free_email_domains": None,  # boolean - Disallow free email domains for Bundle/Inbox recipients?
        "bundle_registration_notifications": None,  # string - Do Bundle owners receive registration notification?
        "bundle_require_registration": None,  # boolean - Do Bundles require registration?
        "bundle_require_share_recipient": None,  # boolean - Do Bundles require recipients for sharing?
        "bundle_upload_receipt_notifications": None,  # string - Do Bundle uploaders receive upload confirmation notifications?
        "bundle_watermark_attachment": None,  # Image - Preview watermark image applied to all bundle items.
        "bundle_watermark_value": None,  # object - Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
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
        "default_time_zone": None,  # string - Site default time zone
        "desktop_app": None,  # boolean - Is the desktop app enabled?
        "desktop_app_session_ip_pinning": None,  # boolean - Is desktop app session IP pinning enabled?
        "desktop_app_session_lifetime": None,  # int64 - Desktop app session lifetime (in hours)
        "mobile_app": None,  # boolean - Is the mobile app enabled?
        "mobile_app_session_ip_pinning": None,  # boolean - Is mobile app session IP pinning enabled?
        "mobile_app_session_lifetime": None,  # int64 - Mobile app session lifetime (in hours)
        "disallowed_countries": None,  # string - Comma seperated list of disallowed Country codes
        "disable_files_certificate_generation": None,  # boolean - If set, Files.com will not set the CAA records required to generate future SSL certificates for this domain.
        "disable_notifications": None,  # boolean - Are notifications disabled?
        "disable_password_reset": None,  # boolean - Is password reset disabled?
        "domain": None,  # string - Custom domain
        "domain_hsts_header": None,  # boolean - Send HSTS (HTTP Strict Transport Security) header when visitors access the site via a custom domain?
        "domain_letsencrypt_chain": None,  # string - Letsencrypt chain to use when registering SSL Certificate for domain.
        "email": None,  # email - Main email for this site
        "ftp_enabled": None,  # boolean - Is FTP enabled?
        "reply_to_email": None,  # email - Reply-to email for this site
        "non_sso_groups_allowed": None,  # boolean - If true, groups can be manually created / modified / deleted by Site Admins. Otherwise, groups can only be managed via your SSO provider.
        "non_sso_users_allowed": None,  # boolean - If true, users can be manually created / modified / deleted by Site Admins. Otherwise, users can only be managed via your SSO provider.
        "folder_permissions_groups_only": None,  # boolean - If true, permissions for this site must be bound to a group (not a user). Otherwise, permissions must be bound to a user.
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
        "motd_text": None,  # string - A message to show users when they connect via FTP or SFTP.
        "motd_use_for_ftp": None,  # boolean - Show message to users connecting via FTP
        "motd_use_for_sftp": None,  # boolean - Show message to users connecting via SFTP
        "next_billing_amount": None,  # double - Next billing amount
        "next_billing_date": None,  # string - Next billing date
        "office_integration_available": None,  # boolean - Allow users to use Office for the web?
        "office_integration_type": None,  # string - Office integration application used to edit and view the MS Office documents
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
        "require_2fa_stop_time": None,  # date-time - If set, requirement for two-factor authentication has been scheduled to end on this date-time.
        "require_2fa_user_type": None,  # string - What type of user is required to use two-factor authentication (when require_2fa is set to `true` for this site)?
        "require_logout_from_bundles_and_inboxes": None,  # boolean - If true, we will hide the 'Remember Me' box on Inbox and Bundle registration pages, requiring that the user logout and log back in every time they visit the page.
        "session": None,  # Session - Current session
        "session_pinned_by_ip": None,  # boolean - Are sessions locked to the same IP? (i.e. do users need to log in again if they change IPs?)
        "sftp_enabled": None,  # boolean - Is SFTP enabled?
        "sftp_host_key_type": None,  # string - Sftp Host Key Type
        "active_sftp_host_key_id": None,  # int64 - Id of the currently selected custom SFTP Host Key
        "sftp_insecure_ciphers": None,  # boolean - Are Insecure Ciphers allowed for SFTP?  Note:  Settting TLS Disabled -> True will always allow insecure ciphers for SFTP as well.  Enabling this is insecure.
        "sftp_user_root_enabled": None,  # boolean - Use user FTP roots also for SFTP?
        "sharing_enabled": None,  # boolean - Allow bundle creation
        "show_request_access_link": None,  # boolean - Show request access link for users without access?  Currently unused.
        "site_footer": None,  # string - Custom site footer text
        "site_header": None,  # string - Custom site header text
        "smtp_address": None,  # string - SMTP server hostname or IP
        "smtp_authentication": None,  # string - SMTP server authentication type
        "smtp_from": None,  # string - From address to use when mailing through custom SMTP
        "smtp_port": None,  # int64 - SMTP server port
        "smtp_username": None,  # string - SMTP server username
        "session_expiry": None,  # double - Session expiry in hours
        "session_expiry_minutes": None,  # int64 - Session expiry in minutes
        "ssl_required": None,  # boolean - Is SSL required?  Disabling this is insecure.
        "subdomain": None,  # string - Site subdomain
        "switch_to_plan_date": None,  # date-time - If switching plans, when does the new plan take effect?
        "tls_disabled": None,  # boolean - Are Insecure TLS and SFTP Ciphers allowed?  Enabling this is insecure.
        "trial_days_left": None,  # int64 - Number of days left in trial
        "trial_until": None,  # date-time - When does this Site trial expire?
        "use_provided_modified_at": None,  # boolean - Allow uploaders to set `provided_modified_at` for uploaded files?
        "user": None,  # User - User of current session
        "user_lockout": None,  # boolean - Will users be locked out after incorrect login attempts?
        "user_lockout_lock_period": None,  # int64 - How many hours to lock user out for failed password?
        "user_lockout_tries": None,  # int64 - Number of login tries within `user_lockout_within` hours before users are locked out
        "user_lockout_within": None,  # int64 - Number of hours for user lockout window
        "user_requests_enabled": None,  # boolean - Enable User Requests feature
        "user_requests_notify_admins": None,  # boolean - Send email to site admins when a user request is received?
        "welcome_custom_text": None,  # string - Custom text send in user welcome email
        "welcome_email_cc": None,  # email - Include this email in welcome emails if enabled
        "welcome_email_subject": None,  # string - Include this email subject in welcome emails if enabled
        "welcome_email_enabled": None,  # boolean - Will the welcome email be sent to new users?
        "welcome_screen": None,  # string - Does the welcome screen appear?
        "windows_mode_ftp": None,  # boolean - Does FTP user Windows emulation mode?
        "disable_users_from_inactivity_period_days": None,  # int64 - If greater than zero, users will unable to login if they do not show activity within this number of days.
        "group_admins_can_set_user_password": None,  # boolean - Allow group admins set password authentication method
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Site.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Site.default_attributes
            if getattr(self, k, None) is not None
        }


def get(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, options = Api.send_request("GET", "/site", params, options)
    return Site(response.data, options)


def get_usage(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, options = Api.send_request("GET", "/site/usage", params, options)
    return UsageSnapshot(response.data, options)


# Parameters:
#   name - string - Site name
#   subdomain - string - Site subdomain
#   domain - string - Custom domain
#   domain_hsts_header - boolean - Send HSTS (HTTP Strict Transport Security) header when visitors access the site via a custom domain?
#   domain_letsencrypt_chain - string - Letsencrypt chain to use when registering SSL Certificate for domain.
#   email - string - Main email for this site
#   reply_to_email - string - Reply-to email for this site
#   allow_bundle_names - boolean - Are manual Bundle names allowed?
#   bundle_expiration - int64 - Site-wide Bundle expiration in days
#   welcome_email_enabled - boolean - Will the welcome email be sent to new users?
#   ask_about_overwrites - boolean - If false, rename conflicting files instead of asking for overwrite confirmation.  Only applies to web interface.
#   show_request_access_link - boolean - Show request access link for users without access?  Currently unused.
#   welcome_email_cc - string - Include this email in welcome emails if enabled
#   welcome_email_subject - string - Include this email subject in welcome emails if enabled
#   welcome_custom_text - string - Custom text send in user welcome email
#   language - string - Site default language
#   windows_mode_ftp - boolean - Does FTP user Windows emulation mode?
#   default_time_zone - string - Site default time zone
#   desktop_app - boolean - Is the desktop app enabled?
#   desktop_app_session_ip_pinning - boolean - Is desktop app session IP pinning enabled?
#   desktop_app_session_lifetime - int64 - Desktop app session lifetime (in hours)
#   mobile_app - boolean - Is the mobile app enabled?
#   mobile_app_session_ip_pinning - boolean - Is mobile app session IP pinning enabled?
#   mobile_app_session_lifetime - int64 - Mobile app session lifetime (in hours)
#   folder_permissions_groups_only - boolean - If true, permissions for this site must be bound to a group (not a user). Otherwise, permissions must be bound to a user.
#   welcome_screen - string - Does the welcome screen appear?
#   office_integration_available - boolean - Allow users to use Office for the web?
#   office_integration_type - string - Office integration application used to edit and view the MS Office documents
#   pin_all_remote_servers_to_site_region - boolean - If true, we will ensure that all internal communications with any remote server are made through the primary region of the site. This setting overrides individual remote server settings.
#   motd_text - string - A message to show users when they connect via FTP or SFTP.
#   motd_use_for_ftp - boolean - Show message to users connecting via FTP
#   motd_use_for_sftp - boolean - Show message to users connecting via SFTP
#   left_navigation_visibility - object - Visibility settings for account navigation
#   session_expiry - double - Session expiry in hours
#   ssl_required - boolean - Is SSL required?  Disabling this is insecure.
#   tls_disabled - boolean - Are Insecure TLS and SFTP Ciphers allowed?  Enabling this is insecure.
#   sftp_insecure_ciphers - boolean - Are Insecure Ciphers allowed for SFTP?  Note:  Settting TLS Disabled -> True will always allow insecure ciphers for SFTP as well.  Enabling this is insecure.
#   disable_files_certificate_generation - boolean - If set, Files.com will not set the CAA records required to generate future SSL certificates for this domain.
#   user_lockout - boolean - Will users be locked out after incorrect login attempts?
#   user_lockout_tries - int64 - Number of login tries within `user_lockout_within` hours before users are locked out
#   user_lockout_within - int64 - Number of hours for user lockout window
#   user_lockout_lock_period - int64 - How many hours to lock user out for failed password?
#   include_password_in_welcome_email - boolean - Include password in emails to new users?
#   allowed_countries - string - Comma seperated list of allowed Country codes
#   allowed_ips - string - List of allowed IP addresses
#   disallowed_countries - string - Comma seperated list of disallowed Country codes
#   days_to_retain_backups - int64 - Number of days to keep deleted files
#   max_prior_passwords - int64 - Number of prior passwords to disallow
#   password_validity_days - int64 - Number of days password is valid
#   password_min_length - int64 - Shortest password length for users
#   password_require_letter - boolean - Require a letter in passwords?
#   password_require_mixed - boolean - Require lower and upper case letters in passwords?
#   password_require_special - boolean - Require special characters in password?
#   password_require_number - boolean - Require a number in passwords?
#   password_require_unbreached - boolean - Require passwords that have not been previously breached? (see https://haveibeenpwned.com/)
#   require_logout_from_bundles_and_inboxes - boolean - If true, we will hide the 'Remember Me' box on Inbox and Bundle registration pages, requiring that the user logout and log back in every time they visit the page.
#   dav_user_root_enabled - boolean - Use user FTP roots also for WebDAV?
#   sftp_user_root_enabled - boolean - Use user FTP roots also for SFTP?
#   disable_password_reset - boolean - Is password reset disabled?
#   immutable_files - boolean - Are files protected from modification?
#   session_pinned_by_ip - boolean - Are sessions locked to the same IP? (i.e. do users need to log in again if they change IPs?)
#   bundle_not_found_message - string - Custom error message to show when bundle is not found.
#   bundle_password_required - boolean - Do Bundles require password protection?
#   bundle_require_registration - boolean - Do Bundles require registration?
#   bundle_require_share_recipient - boolean - Do Bundles require recipients for sharing?
#   bundle_registration_notifications - string - Do Bundle owners receive registration notification?
#   bundle_activity_notifications - string - Do Bundle owners receive activity notifications?
#   bundle_upload_receipt_notifications - string - Do Bundle uploaders receive upload confirmation notifications?
#   password_requirements_apply_to_bundles - boolean - Require bundles' passwords, and passwords for other items (inboxes, public shares, etc.) to conform to the same requirements as users' passwords?
#   prevent_root_permissions_for_non_site_admins - boolean - If true, we will prevent non-administrators from receiving any permissions directly on the root folder.  This is commonly used to prevent the accidental application of permissions.
#   opt_out_global - boolean - Use servers in the USA only?
#   use_provided_modified_at - boolean - Allow uploaders to set `provided_modified_at` for uploaded files?
#   custom_namespace - boolean - Is this site using a custom namespace for users?
#   disable_users_from_inactivity_period_days - int64 - If greater than zero, users will unable to login if they do not show activity within this number of days.
#   non_sso_groups_allowed - boolean - If true, groups can be manually created / modified / deleted by Site Admins. Otherwise, groups can only be managed via your SSO provider.
#   non_sso_users_allowed - boolean - If true, users can be manually created / modified / deleted by Site Admins. Otherwise, users can only be managed via your SSO provider.
#   sharing_enabled - boolean - Allow bundle creation
#   user_requests_enabled - boolean - Enable User Requests feature
#   user_requests_notify_admins - boolean - Send email to site admins when a user request is received?
#   dav_enabled - boolean - Is WebDAV enabled?
#   ftp_enabled - boolean - Is FTP enabled?
#   sftp_enabled - boolean - Is SFTP enabled?
#   sftp_host_key_type - string - Sftp Host Key Type
#   active_sftp_host_key_id - int64 - Id of the currently selected custom SFTP Host Key
#   protocol_access_groups_only - boolean - If true, protocol access permissions on users will be ignored, and only protocol access permissions set on Groups will be honored.  Make sure that your current user is a member of a group with API permission when changing this value to avoid locking yourself out of your site.
#   bundle_watermark_value - object - Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
#   group_admins_can_set_user_password - boolean - Allow group admins set password authentication method
#   bundle_recipient_blacklist_free_email_domains - boolean - Disallow free email domains for Bundle/Inbox recipients?
#   bundle_recipient_blacklist_domains - array(string) - List of email domains to disallow when entering a Bundle/Inbox recipients
#   admins_bypass_locked_subfolders - boolean - Allow admins to bypass the locked subfolders setting.
#   allowed_2fa_method_sms - boolean - Is SMS two factor authentication allowed?
#   allowed_2fa_method_u2f - boolean - Is U2F two factor authentication allowed?
#   allowed_2fa_method_totp - boolean - Is TOTP two factor authentication allowed?
#   allowed_2fa_method_webauthn - boolean - Is WebAuthn two factor authentication allowed?
#   allowed_2fa_method_yubi - boolean - Is yubikey two factor authentication allowed?
#   allowed_2fa_method_email - boolean - Is OTP via email two factor authentication allowed?
#   allowed_2fa_method_bypass_for_ftp_sftp_dav - boolean - Are users allowed to configure their two factor authentication to be bypassed for FTP/SFTP/WebDAV?
#   require_2fa - boolean - Require two-factor authentication for all users?
#   require_2fa_user_type - string - What type of user is required to use two-factor authentication (when require_2fa is set to `true` for this site)?
#   color2_top - string - Top bar background color
#   color2_left - string - Page link and button color
#   color2_link - string - Top bar link color
#   color2_text - string - Page link and button color
#   color2_top_text - string - Top bar text color
#   site_header - string - Custom site header text
#   site_footer - string - Custom site footer text
#   login_help_text - string - Login help text
#   smtp_address - string - SMTP server hostname or IP
#   smtp_authentication - string - SMTP server authentication type
#   smtp_from - string - From address to use when mailing through custom SMTP
#   smtp_username - string - SMTP server username
#   smtp_port - int64 - SMTP server port
#   ldap_enabled - boolean - Main LDAP setting: is LDAP enabled?
#   ldap_type - string - LDAP type
#   ldap_host - string - LDAP host
#   ldap_host_2 - string - LDAP backup host
#   ldap_host_3 - string - LDAP backup host
#   ldap_port - int64 - LDAP port
#   ldap_secure - boolean - Use secure LDAP?
#   ldap_username - string - Username for signing in to LDAP server.
#   ldap_username_field - string - LDAP username field
#   ldap_domain - string - Domain name that will be appended to usernames
#   ldap_user_action - string - Should we sync users from LDAP server?
#   ldap_group_action - string - Should we sync groups from LDAP server?
#   ldap_user_include_groups - string - Comma or newline separated list of group names (with optional wildcards) - if provided, only users in these groups will be added or synced.
#   ldap_group_exclusion - string - Comma or newline separated list of group names (with optional wildcards) to exclude when syncing.
#   ldap_group_inclusion - string - Comma or newline separated list of group names (with optional wildcards) to include when syncing.
#   ldap_base_dn - string - Base DN for looking up users in LDAP server
#   uploads_via_email_authentication - boolean - Do incoming emails in the Inboxes require checking for SPF/DKIM/DMARC?
#   icon16_file - file
#   icon16_delete - boolean - If true, will delete the file stored in icon16
#   icon32_file - file
#   icon32_delete - boolean - If true, will delete the file stored in icon32
#   icon48_file - file
#   icon48_delete - boolean - If true, will delete the file stored in icon48
#   icon128_file - file
#   icon128_delete - boolean - If true, will delete the file stored in icon128
#   logo_file - file
#   logo_delete - boolean - If true, will delete the file stored in logo
#   bundle_watermark_attachment_file - file
#   bundle_watermark_attachment_delete - boolean - If true, will delete the file stored in bundle_watermark_attachment
#   login_page_background_image_file - file
#   login_page_background_image_delete - boolean - If true, will delete the file stored in login_page_background_image
#   disable_2fa_with_delay - boolean - If set to true, we will begin the process of disabling 2FA on this site.
#   ldap_password_change - string - New LDAP password.
#   ldap_password_change_confirmation - string - Confirm new LDAP password.
#   smtp_password - string - Password for SMTP server.
#   session_expiry_minutes - int64 - Session expiry in minutes
def update(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "subdomain" in params and not isinstance(params["subdomain"], str):
        raise InvalidParameterError("Bad parameter: subdomain must be an str")
    if "domain" in params and not isinstance(params["domain"], str):
        raise InvalidParameterError("Bad parameter: domain must be an str")
    if "domain_letsencrypt_chain" in params and not isinstance(
        params["domain_letsencrypt_chain"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: domain_letsencrypt_chain must be an str"
        )
    if "email" in params and not isinstance(params["email"], str):
        raise InvalidParameterError("Bad parameter: email must be an str")
    if "reply_to_email" in params and not isinstance(
        params["reply_to_email"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: reply_to_email must be an str"
        )
    if "bundle_expiration" in params and not isinstance(
        params["bundle_expiration"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: bundle_expiration must be an int"
        )
    if "welcome_email_cc" in params and not isinstance(
        params["welcome_email_cc"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: welcome_email_cc must be an str"
        )
    if "welcome_email_subject" in params and not isinstance(
        params["welcome_email_subject"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: welcome_email_subject must be an str"
        )
    if "welcome_custom_text" in params and not isinstance(
        params["welcome_custom_text"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: welcome_custom_text must be an str"
        )
    if "language" in params and not isinstance(params["language"], str):
        raise InvalidParameterError("Bad parameter: language must be an str")
    if "default_time_zone" in params and not isinstance(
        params["default_time_zone"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: default_time_zone must be an str"
        )
    if "desktop_app_session_lifetime" in params and not isinstance(
        params["desktop_app_session_lifetime"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: desktop_app_session_lifetime must be an int"
        )
    if "mobile_app_session_lifetime" in params and not isinstance(
        params["mobile_app_session_lifetime"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: mobile_app_session_lifetime must be an int"
        )
    if "welcome_screen" in params and not isinstance(
        params["welcome_screen"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: welcome_screen must be an str"
        )
    if "office_integration_type" in params and not isinstance(
        params["office_integration_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: office_integration_type must be an str"
        )
    if "motd_text" in params and not isinstance(params["motd_text"], str):
        raise InvalidParameterError("Bad parameter: motd_text must be an str")
    if "left_navigation_visibility" in params and not isinstance(
        params["left_navigation_visibility"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: left_navigation_visibility must be an dict"
        )
    if "session_expiry" in params and not isinstance(
        params["session_expiry"], float
    ):
        raise InvalidParameterError(
            "Bad parameter: session_expiry must be an float"
        )
    if "user_lockout_tries" in params and not isinstance(
        params["user_lockout_tries"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: user_lockout_tries must be an int"
        )
    if "user_lockout_within" in params and not isinstance(
        params["user_lockout_within"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: user_lockout_within must be an int"
        )
    if "user_lockout_lock_period" in params and not isinstance(
        params["user_lockout_lock_period"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: user_lockout_lock_period must be an int"
        )
    if "allowed_countries" in params and not isinstance(
        params["allowed_countries"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: allowed_countries must be an str"
        )
    if "allowed_ips" in params and not isinstance(params["allowed_ips"], str):
        raise InvalidParameterError(
            "Bad parameter: allowed_ips must be an str"
        )
    if "disallowed_countries" in params and not isinstance(
        params["disallowed_countries"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: disallowed_countries must be an str"
        )
    if "days_to_retain_backups" in params and not isinstance(
        params["days_to_retain_backups"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: days_to_retain_backups must be an int"
        )
    if "max_prior_passwords" in params and not isinstance(
        params["max_prior_passwords"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: max_prior_passwords must be an int"
        )
    if "password_validity_days" in params and not isinstance(
        params["password_validity_days"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: password_validity_days must be an int"
        )
    if "password_min_length" in params and not isinstance(
        params["password_min_length"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: password_min_length must be an int"
        )
    if "bundle_not_found_message" in params and not isinstance(
        params["bundle_not_found_message"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: bundle_not_found_message must be an str"
        )
    if "bundle_registration_notifications" in params and not isinstance(
        params["bundle_registration_notifications"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: bundle_registration_notifications must be an str"
        )
    if "bundle_activity_notifications" in params and not isinstance(
        params["bundle_activity_notifications"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: bundle_activity_notifications must be an str"
        )
    if "bundle_upload_receipt_notifications" in params and not isinstance(
        params["bundle_upload_receipt_notifications"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: bundle_upload_receipt_notifications must be an str"
        )
    if (
        "disable_users_from_inactivity_period_days" in params
        and not isinstance(
            params["disable_users_from_inactivity_period_days"], int
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: disable_users_from_inactivity_period_days must be an int"
        )
    if "sftp_host_key_type" in params and not isinstance(
        params["sftp_host_key_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: sftp_host_key_type must be an str"
        )
    if "active_sftp_host_key_id" in params and not isinstance(
        params["active_sftp_host_key_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: active_sftp_host_key_id must be an int"
        )
    if "bundle_watermark_value" in params and not isinstance(
        params["bundle_watermark_value"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: bundle_watermark_value must be an dict"
        )
    if "bundle_recipient_blacklist_domains" in params and not isinstance(
        params["bundle_recipient_blacklist_domains"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: bundle_recipient_blacklist_domains must be an list"
        )
    if "require_2fa_user_type" in params and not isinstance(
        params["require_2fa_user_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: require_2fa_user_type must be an str"
        )
    if "color2_top" in params and not isinstance(params["color2_top"], str):
        raise InvalidParameterError("Bad parameter: color2_top must be an str")
    if "color2_left" in params and not isinstance(params["color2_left"], str):
        raise InvalidParameterError(
            "Bad parameter: color2_left must be an str"
        )
    if "color2_link" in params and not isinstance(params["color2_link"], str):
        raise InvalidParameterError(
            "Bad parameter: color2_link must be an str"
        )
    if "color2_text" in params and not isinstance(params["color2_text"], str):
        raise InvalidParameterError(
            "Bad parameter: color2_text must be an str"
        )
    if "color2_top_text" in params and not isinstance(
        params["color2_top_text"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: color2_top_text must be an str"
        )
    if "site_header" in params and not isinstance(params["site_header"], str):
        raise InvalidParameterError(
            "Bad parameter: site_header must be an str"
        )
    if "site_footer" in params and not isinstance(params["site_footer"], str):
        raise InvalidParameterError(
            "Bad parameter: site_footer must be an str"
        )
    if "login_help_text" in params and not isinstance(
        params["login_help_text"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: login_help_text must be an str"
        )
    if "smtp_address" in params and not isinstance(
        params["smtp_address"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: smtp_address must be an str"
        )
    if "smtp_authentication" in params and not isinstance(
        params["smtp_authentication"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: smtp_authentication must be an str"
        )
    if "smtp_from" in params and not isinstance(params["smtp_from"], str):
        raise InvalidParameterError("Bad parameter: smtp_from must be an str")
    if "smtp_username" in params and not isinstance(
        params["smtp_username"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: smtp_username must be an str"
        )
    if "smtp_port" in params and not isinstance(params["smtp_port"], int):
        raise InvalidParameterError("Bad parameter: smtp_port must be an int")
    if "ldap_type" in params and not isinstance(params["ldap_type"], str):
        raise InvalidParameterError("Bad parameter: ldap_type must be an str")
    if "ldap_host" in params and not isinstance(params["ldap_host"], str):
        raise InvalidParameterError("Bad parameter: ldap_host must be an str")
    if "ldap_host_2" in params and not isinstance(params["ldap_host_2"], str):
        raise InvalidParameterError(
            "Bad parameter: ldap_host_2 must be an str"
        )
    if "ldap_host_3" in params and not isinstance(params["ldap_host_3"], str):
        raise InvalidParameterError(
            "Bad parameter: ldap_host_3 must be an str"
        )
    if "ldap_port" in params and not isinstance(params["ldap_port"], int):
        raise InvalidParameterError("Bad parameter: ldap_port must be an int")
    if "ldap_username" in params and not isinstance(
        params["ldap_username"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_username must be an str"
        )
    if "ldap_username_field" in params and not isinstance(
        params["ldap_username_field"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_username_field must be an str"
        )
    if "ldap_domain" in params and not isinstance(params["ldap_domain"], str):
        raise InvalidParameterError(
            "Bad parameter: ldap_domain must be an str"
        )
    if "ldap_user_action" in params and not isinstance(
        params["ldap_user_action"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_user_action must be an str"
        )
    if "ldap_group_action" in params and not isinstance(
        params["ldap_group_action"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_group_action must be an str"
        )
    if "ldap_user_include_groups" in params and not isinstance(
        params["ldap_user_include_groups"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_user_include_groups must be an str"
        )
    if "ldap_group_exclusion" in params and not isinstance(
        params["ldap_group_exclusion"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_group_exclusion must be an str"
        )
    if "ldap_group_inclusion" in params and not isinstance(
        params["ldap_group_inclusion"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_group_inclusion must be an str"
        )
    if "ldap_base_dn" in params and not isinstance(
        params["ldap_base_dn"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_base_dn must be an str"
        )
    if "ldap_password_change" in params and not isinstance(
        params["ldap_password_change"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_password_change must be an str"
        )
    if "ldap_password_change_confirmation" in params and not isinstance(
        params["ldap_password_change_confirmation"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_password_change_confirmation must be an str"
        )
    if "smtp_password" in params and not isinstance(
        params["smtp_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: smtp_password must be an str"
        )
    if "session_expiry_minutes" in params and not isinstance(
        params["session_expiry_minutes"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: session_expiry_minutes must be an int"
        )
    response, options = Api.send_request("PATCH", "/site", params, options)
    return Site(response.data, options)


def new(*args, **kwargs):
    return Site(*args, **kwargs)
