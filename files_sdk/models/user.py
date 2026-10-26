import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.attachment import with_attachments
from files_sdk.api import (  # noqa: F401
    LEGACY,
    LegacyScope,
    Operation,
    copy_params,
    decode_record,
    path_value,
)
from files_sdk.api_client import unexpected_response_error  # noqa: F401
from files_sdk.context import RequestOptions  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class User:
    """A user record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - User ID
        username: string - User's username
        admin_group_ids: array(int64) - List of group IDs of which this user is an administrator
        allowed_ips: string - A list of allowed IPs if applicable. Newline delimited
        attachments_permission: boolean - If `true`, the user can user create Bundles (aka Share Links). Use the bundle permission instead.
        api_keys_count: int64 - Number of API keys associated with this user
        authenticate_until: date-time - Scheduled Date/Time at which user will be deactivated
        authentication_method: string - How is this user authenticated?
        avatar_url: string - URL holding the user's avatar
        billable: boolean - Is this a billable user record?
        billing_permission: boolean - Allow this user to perform operations on the account, payments, and invoices?
        bypass_site_allowed_ips: boolean - Allow this user to skip site-wide IP blacklists?
        bypass_user_lifecycle_rules: boolean - Exempt this user from user lifecycle rules?
        created_at: date-time - When this user was created
        dav_permission: boolean - Can the user connect with WebDAV?
        disabled: boolean - Is user disabled? Disabled users cannot log in, and do not count for billing purposes. Users can be automatically disabled after an inactivity period via a Site setting or schedule to be deactivated after specific date.
        disabled_expired_or_inactive: boolean - Computed property that returns true if user disabled or expired or inactive.
        ai_assistant_personality_id: int64 - AI Assistant Personality ID assigned directly to this user, if any.
        desktop_configuration_profile_id: int64 - Desktop Configuration Profile ID assigned directly to this user, if any.
        integration_centric_profile_id: int64 - Integration Centric Profile ID assigned directly to this user, if any.
        email: email - User email address
        filesystem_layout: string - File system layout
        first_login_at: date-time - User's first login time
        ftp_permission: boolean - Can the user access with FTP/FTPS?
        group_ids: string - Comma-separated list of group IDs of which this user is a member
        header_text: string - Text to display to the user in the header of the UI
        language: string - Preferred language
        last_login_at: date-time - User's most recent login time via any protocol
        last_web_login_at: date-time - User's most recent login time via web
        last_ftp_login_at: date-time - User's most recent login time via FTP
        last_sftp_login_at: date-time - User's most recent login time via SFTP
        last_dav_login_at: date-time - User's most recent login time via WebDAV
        last_desktop_login_at: date-time - User's most recent login time via Desktop app
        last_restapi_login_at: date-time - User's most recent login time via Rest API
        last_api_use_at: date-time - User's most recent API use time
        last_active_at: date-time - User's most recent activity time, which is the latest of most recent login, most recent API use, enablement, or creation
        last_protocol_cipher: string - The most recent protocol and cipher used
        lockout_expires: date-time - Time in the future that the user will no longer be locked out if applicable
        name: string - User's full name
        company: string - User's company
        notes: string - Any internal notes on the user
        notification_daily_send_time: int64 - Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
        office_integration_enabled: boolean - Enable integration with Office for the web?
        partner_admin: boolean - Is this user a Partner administrator?
        partner_id: int64 - Partner ID if this user belongs to a Partner
        partner_name: string - Name of the Partner if this user belongs to a Partner
        password_set_at: date-time - Last time the user's password was set
        password_validity_days: int64 - Number of days to allow user to use the same password
        primary_group_id: int64 - Primary group ID for Group Admin scoping
        public_keys_count: int64 - Number of public keys associated with this user
        receive_admin_alerts: boolean - Deprecated. Use notify_on_all_site_warnings and granular failure notification preferences instead.
        notify_on_all_site_warnings: boolean - Should the user receive site warnings via email?
        notify_on_all_sso_failures: boolean - Should the user receive sso/scim/ldap configuration/sync failures via email?
        notify_on_all_user_security_events: boolean - Should the user receive user security events via email?
        notify_on_all_pending_work_failures: boolean - Should the user receive pending work failures via email?
        notify_on_all_siem_http_destination_failures: boolean - Should the user receive siem failures via email?
        notify_on_all_sync_failures: boolean - Should the user receive sync failures via email?
        notify_on_all_automation_failures: boolean - Should the user receive automation failures via email?
        notify_on_all_expectation_failures: boolean - Should the user receive expectation failures and misses via email?
        require_2fa: string - 2FA required setting. `use_system_setting` uses the site-wide setting, including SSO exemptions. `always_require` and `never_require` override the site-wide setting when user-level overrides are allowed.
        require_login_by: date-time - Require user to login by specified date otherwise it will be disabled.
        active_2fa: boolean - Is 2fa active for the user?
        require_password_change: boolean - Is a password change required upon next user login?
        password_expired: boolean - Is user's password expired?
        responsible_group_id: int64 - ID of the internal Group responsible for this Partner User, overriding the Partner default.
        responsible_user_id: int64 - ID of the internal User responsible for this Partner User, overriding the Partner default.
        readonly_site_admin: boolean - Is the user an allowed to view all (non-billing) site configuration for this site?
        restapi_permission: boolean - Can this user access the Web app, Desktop app, SDKs, or REST API? (All of these tools use the API internally, so this is one unified permission set.)
        s3_compatible_endpoint_permission: boolean - Can the user access the S3-compatible endpoint? Defaults to true.
        self_managed: boolean - Does this user manage it's own credentials or is it a shared/bot user?
        sftp_permission: boolean - Can the user access with SFTP?
        site_admin: boolean - Is the user an administrator for this site?
        workspace_admin: boolean - Whether the user is an administrator of their own Custom Workspace. Does not reflect administration granted through Permissions.
        site_id: int64 - Site ID
        workspace_id: int64 - ID of the Workspace the user belongs to. 0 is the Default Workspace.
        default_workspace_id: int64 - Workspace ID the user should land in by default when more than one Workspace is available.
        skip_welcome_screen: boolean - Skip Welcome page in the UI?
        ssl_required: string - SSL required setting
        sso_strategy_id: int64 - SSO (Single Sign On) strategy ID for the user, if applicable.
        externally_managed: boolean - Is this user managed by a SsoStrategy?
        tags: string - Comma-separated list of Tags for this user. Tags are used for other features, such as UserLifecycleRules, which can target specific tags. Tags must only contain lowercase letters, numbers, and hyphens.
        time_zone: string - User time zone
        type_of_2fa: string - Type(s) of 2FA methods in use, for programmatic use. Will be either `sms`, `totp`, `webauthn`, `yubi`, `email`, or multiple values sorted alphabetically and joined by an underscore. Does not specify whether user has more than one of a given method.
        type_of_2fa_for_display: string - Type(s) of 2FA methods in use, formatted for displaying in the UI. Unlike `type_of_2fa`, this value will make clear when a user has more than 1 of the same type of method.
        user_root: string - If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.
        user_home: string - Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.
        days_remaining_until_password_expire: int64 - Number of days remaining until password expires
        password_expire_at: date-time - Password expiration datetime
        avatar_file: file - An image file for your user avatar.
        avatar_delete: boolean - If true, the avatar will be deleted.
        change_password: string - Used for changing a password on an existing user.
        change_password_confirmation: string - Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
        grant_permission: string - Permission to grant on the User Root upon creation, or on the Workspace root when the User Root is blank. For the Default Workspace, a blank User Root uses the site root. `admin` on a Custom Workspace's root grants Workspace Administrator access; on a subfolder it grants Folder Admin access. Can be blank or `admin`, `full`, `read`, `write`, `list`, `read+write`, `list+write`, or `history`.
        group_id: int64 - Group ID to associate this user with.
        imported_password_hash: string - Pre-calculated hash of the user's password. If supplied, this will be used to authenticate the user on first login. Supported hash methods are MD5, SHA1, and SHA256.
        password: string - User password.
        password_confirmation: string - Optional, but if provided, we will ensure that it matches the value sent in `password`.
        announcements_read: boolean - Signifies that the user has read all the announcements in the UI.
        clear_2fa: boolean - If true when changing authentication_method from `password` to `sso`, remove all two-factor methods. Ignored in all other cases.
        convert_to_partner_user: boolean - Required when assigning a Partner to an existing non-Partner user. If true, convert the user by assigning the partner_id provided.
    """

    default_attributes = {
        "id": None,  # int64 - User ID
        "username": None,  # string - User's username
        "admin_group_ids": None,  # array(int64) - List of group IDs of which this user is an administrator
        "allowed_ips": None,  # string - A list of allowed IPs if applicable.  Newline delimited
        "attachments_permission": None,  # boolean - If `true`, the user can user create Bundles (aka Share Links). Use the bundle permission instead.
        "api_keys_count": None,  # int64 - Number of API keys associated with this user
        "authenticate_until": None,  # date-time - Scheduled Date/Time at which user will be deactivated
        "authentication_method": None,  # string - How is this user authenticated?
        "avatar_url": None,  # string - URL holding the user's avatar
        "billable": None,  # boolean - Is this a billable user record?
        "billing_permission": None,  # boolean - Allow this user to perform operations on the account, payments, and invoices?
        "bypass_site_allowed_ips": None,  # boolean - Allow this user to skip site-wide IP blacklists?
        "bypass_user_lifecycle_rules": None,  # boolean - Exempt this user from user lifecycle rules?
        "created_at": None,  # date-time - When this user was created
        "dav_permission": None,  # boolean - Can the user connect with WebDAV?
        "disabled": None,  # boolean - Is user disabled? Disabled users cannot log in, and do not count for billing purposes. Users can be automatically disabled after an inactivity period via a Site setting or schedule to be deactivated after specific date.
        "disabled_expired_or_inactive": None,  # boolean - Computed property that returns true if user disabled or expired or inactive.
        "ai_assistant_personality_id": None,  # int64 - AI Assistant Personality ID assigned directly to this user, if any.
        "desktop_configuration_profile_id": None,  # int64 - Desktop Configuration Profile ID assigned directly to this user, if any.
        "integration_centric_profile_id": None,  # int64 - Integration Centric Profile ID assigned directly to this user, if any.
        "email": None,  # email - User email address
        "filesystem_layout": None,  # string - File system layout
        "first_login_at": None,  # date-time - User's first login time
        "ftp_permission": None,  # boolean - Can the user access with FTP/FTPS?
        "group_ids": None,  # string - Comma-separated list of group IDs of which this user is a member
        "header_text": None,  # string - Text to display to the user in the header of the UI
        "language": None,  # string - Preferred language
        "last_login_at": None,  # date-time - User's most recent login time via any protocol
        "last_web_login_at": None,  # date-time - User's most recent login time via web
        "last_ftp_login_at": None,  # date-time - User's most recent login time via FTP
        "last_sftp_login_at": None,  # date-time - User's most recent login time via SFTP
        "last_dav_login_at": None,  # date-time - User's most recent login time via WebDAV
        "last_desktop_login_at": None,  # date-time - User's most recent login time via Desktop app
        "last_restapi_login_at": None,  # date-time - User's most recent login time via Rest API
        "last_api_use_at": None,  # date-time - User's most recent API use time
        "last_active_at": None,  # date-time - User's most recent activity time, which is the latest of most recent login, most recent API use, enablement, or creation
        "last_protocol_cipher": None,  # string - The most recent protocol and cipher used
        "lockout_expires": None,  # date-time - Time in the future that the user will no longer be locked out if applicable
        "name": None,  # string - User's full name
        "company": None,  # string - User's company
        "notes": None,  # string - Any internal notes on the user
        "notification_daily_send_time": None,  # int64 - Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
        "office_integration_enabled": None,  # boolean - Enable integration with Office for the web?
        "partner_admin": None,  # boolean - Is this user a Partner administrator?
        "partner_id": None,  # int64 - Partner ID if this user belongs to a Partner
        "partner_name": None,  # string - Name of the Partner if this user belongs to a Partner
        "password_set_at": None,  # date-time - Last time the user's password was set
        "password_validity_days": None,  # int64 - Number of days to allow user to use the same password
        "primary_group_id": None,  # int64 - Primary group ID for Group Admin scoping
        "public_keys_count": None,  # int64 - Number of public keys associated with this user
        "receive_admin_alerts": None,  # boolean - Deprecated. Use notify_on_all_site_warnings and granular failure notification preferences instead.
        "notify_on_all_site_warnings": None,  # boolean - Should the user receive site warnings via email?
        "notify_on_all_sso_failures": None,  # boolean - Should the user receive sso/scim/ldap configuration/sync failures via email?
        "notify_on_all_user_security_events": None,  # boolean - Should the user receive user security events via email?
        "notify_on_all_pending_work_failures": None,  # boolean - Should the user receive pending work failures via email?
        "notify_on_all_siem_http_destination_failures": None,  # boolean - Should the user receive siem failures via email?
        "notify_on_all_sync_failures": None,  # boolean - Should the user receive sync failures via email?
        "notify_on_all_automation_failures": None,  # boolean - Should the user receive automation failures via email?
        "notify_on_all_expectation_failures": None,  # boolean - Should the user receive expectation failures and misses via email?
        "require_2fa": None,  # string - 2FA required setting. `use_system_setting` uses the site-wide setting, including SSO exemptions. `always_require` and `never_require` override the site-wide setting when user-level overrides are allowed.
        "require_login_by": None,  # date-time - Require user to login by specified date otherwise it will be disabled.
        "active_2fa": None,  # boolean - Is 2fa active for the user?
        "require_password_change": None,  # boolean - Is a password change required upon next user login?
        "password_expired": None,  # boolean - Is user's password expired?
        "responsible_group_id": None,  # int64 - ID of the internal Group responsible for this Partner User, overriding the Partner default.
        "responsible_user_id": None,  # int64 - ID of the internal User responsible for this Partner User, overriding the Partner default.
        "readonly_site_admin": None,  # boolean - Is the user an allowed to view all (non-billing) site configuration for this site?
        "restapi_permission": None,  # boolean - Can this user access the Web app, Desktop app, SDKs, or REST API?  (All of these tools use the API internally, so this is one unified permission set.)
        "s3_compatible_endpoint_permission": None,  # boolean - Can the user access the S3-compatible endpoint? Defaults to true.
        "self_managed": None,  # boolean - Does this user manage it's own credentials or is it a shared/bot user?
        "sftp_permission": None,  # boolean - Can the user access with SFTP?
        "site_admin": None,  # boolean - Is the user an administrator for this site?
        "workspace_admin": None,  # boolean - Whether the user is an administrator of their own Custom Workspace. Does not reflect administration granted through Permissions.
        "site_id": None,  # int64 - Site ID
        "workspace_id": None,  # int64 - ID of the Workspace the user belongs to. 0 is the Default Workspace.
        "default_workspace_id": None,  # int64 - Workspace ID the user should land in by default when more than one Workspace is available.
        "skip_welcome_screen": None,  # boolean - Skip Welcome page in the UI?
        "ssl_required": None,  # string - SSL required setting
        "sso_strategy_id": None,  # int64 - SSO (Single Sign On) strategy ID for the user, if applicable.
        "externally_managed": None,  # boolean - Is this user managed by a SsoStrategy?
        "tags": None,  # string - Comma-separated list of Tags for this user. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
        "time_zone": None,  # string - User time zone
        "type_of_2fa": None,  # string - Type(s) of 2FA methods in use, for programmatic use.  Will be either `sms`, `totp`, `webauthn`, `yubi`, `email`, or multiple values sorted alphabetically and joined by an underscore.  Does not specify whether user has more than one of a given method.
        "type_of_2fa_for_display": None,  # string - Type(s) of 2FA methods in use, formatted for displaying in the UI.  Unlike `type_of_2fa`, this value will make clear when a user has more than 1 of the same type of method.
        "user_root": None,  # string - If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.
        "user_home": None,  # string - Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.
        "days_remaining_until_password_expire": None,  # int64 - Number of days remaining until password expires
        "password_expire_at": None,  # date-time - Password expiration datetime
        "avatar_file": None,  # file - An image file for your user avatar.
        "avatar_delete": None,  # boolean - If true, the avatar will be deleted.
        "change_password": None,  # string - Used for changing a password on an existing user.
        "change_password_confirmation": None,  # string - Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
        "grant_permission": None,  # string - Permission to grant on the User Root upon creation, or on the Workspace root when the User Root is blank. For the Default Workspace, a blank User Root uses the site root. `admin` on a Custom Workspace's root grants Workspace Administrator access; on a subfolder it grants Folder Admin access. Can be blank or `admin`, `full`, `read`, `write`, `list`, `read+write`, `list+write`, or `history`.
        "group_id": None,  # int64 - Group ID to associate this user with.
        "imported_password_hash": None,  # string - Pre-calculated hash of the user's password. If supplied, this will be used to authenticate the user on first login. Supported hash methods are MD5, SHA1, and SHA256.
        "password": None,  # string - User password.
        "password_confirmation": None,  # string - Optional, but if provided, we will ensure that it matches the value sent in `password`.
        "announcements_read": None,  # boolean - Signifies that the user has read all the announcements in the UI.
        "clear_2fa": None,  # boolean - If true when changing authentication_method from `password` to `sso`, remove all two-factor methods. Ignored in all other cases.
        "convert_to_partner_user": None,  # boolean - Required when assigning a Partner to an existing non-Partner user. If true, convert the user by assigning the partner_id provided.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    username: str | None
    admin_group_ids: builtins.list[int] | None
    allowed_ips: str | None
    attachments_permission: bool | None
    api_keys_count: int | None
    authenticate_until: str | None
    authentication_method: str | None
    avatar_url: str | None
    billable: bool | None
    billing_permission: bool | None
    bypass_site_allowed_ips: bool | None
    bypass_user_lifecycle_rules: bool | None
    created_at: str | None
    dav_permission: bool | None
    disabled: bool | None
    disabled_expired_or_inactive: bool | None
    ai_assistant_personality_id: int | None
    desktop_configuration_profile_id: int | None
    integration_centric_profile_id: int | None
    email: str | None
    filesystem_layout: str | None
    first_login_at: str | None
    ftp_permission: bool | None
    group_ids: str | None
    header_text: str | None
    language: str | None
    last_login_at: str | None
    last_web_login_at: str | None
    last_ftp_login_at: str | None
    last_sftp_login_at: str | None
    last_dav_login_at: str | None
    last_desktop_login_at: str | None
    last_restapi_login_at: str | None
    last_api_use_at: str | None
    last_active_at: str | None
    last_protocol_cipher: str | None
    lockout_expires: str | None
    name: str | None
    company: str | None
    notes: str | None
    notification_daily_send_time: int | None
    office_integration_enabled: bool | None
    partner_admin: bool | None
    partner_id: int | None
    partner_name: str | None
    password_set_at: str | None
    password_validity_days: int | None
    primary_group_id: int | None
    public_keys_count: int | None
    receive_admin_alerts: bool | None
    notify_on_all_site_warnings: bool | None
    notify_on_all_sso_failures: bool | None
    notify_on_all_user_security_events: bool | None
    notify_on_all_pending_work_failures: bool | None
    notify_on_all_siem_http_destination_failures: bool | None
    notify_on_all_sync_failures: bool | None
    notify_on_all_automation_failures: bool | None
    notify_on_all_expectation_failures: bool | None
    require_2fa: str | None
    require_login_by: str | None
    active_2fa: bool | None
    require_password_change: bool | None
    password_expired: bool | None
    responsible_group_id: int | None
    responsible_user_id: int | None
    readonly_site_admin: bool | None
    restapi_permission: bool | None
    s3_compatible_endpoint_permission: bool | None
    self_managed: bool | None
    sftp_permission: bool | None
    site_admin: bool | None
    workspace_admin: bool | None
    site_id: int | None
    workspace_id: int | None
    default_workspace_id: int | None
    skip_welcome_screen: bool | None
    ssl_required: str | None
    sso_strategy_id: int | None
    externally_managed: bool | None
    tags: str | None
    time_zone: str | None
    type_of_2fa: str | None
    type_of_2fa_for_display: str | None
    user_root: str | None
    user_home: str | None
    days_remaining_until_password_expire: int | None
    password_expire_at: str | None
    avatar_file: Any
    avatar_delete: bool | None
    change_password: str | None
    change_password_confirmation: str | None
    grant_permission: str | None
    group_id: int | None
    imported_password_hash: str | None
    password: str | None
    password_confirmation: str | None
    announcements_read: bool | None
    clear_2fa: bool | None
    convert_to_partner_user: bool | None

    # The client and settings this object's operations use: those of the
    # operation or client that made it, or the module's when it starts an
    # operation if neither did.
    _context: Any = None

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = dict(options)

    def set_attributes(self, attributes):
        for attribute, default_value in User.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in User.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def unlock(self, params: dict[str, Any] | None = None) -> None:
        """Unlock user who has been locked out due to failed logins"""
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "POST", "/users/" + path_value(params["id"]) + "/unlock", params
        )

    def resend_welcome_email(
        self, params: dict[str, Any] | None = None
    ) -> None:
        """Resend user welcome email"""
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "POST",
            "/users/" + path_value(params["id"]) + "/resend_welcome_email",
            params,
        )

    def user_2fa_reset(self, params: dict[str, Any] | None = None) -> None:
        """Trigger 2FA Reset process for user who has lost access to their existing 2FA methods"""
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "POST", "/users/" + path_value(params["id"]) + "/2fa/reset", params
        )

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          avatar_file - file - An image file for your user avatar.
          avatar_delete - boolean - If true, the avatar will be deleted.
          change_password - string - Used for changing a password on an existing user.
          change_password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
          email - string - User's email.
          grant_permission - string - Permission to grant on the User Root upon creation, or on the Workspace root when the User Root is blank. For the Default Workspace, a blank User Root uses the site root. `admin` on a Custom Workspace's root grants Workspace Administrator access; on a subfolder it grants Folder Admin access. Can be blank or `admin`, `full`, `read`, `write`, `list`, `read+write`, `list+write`, or `history`.
          group_id - int64 - Group ID to associate this user with.
          group_ids - string - A list of group ids to associate this user with.  Comma delimited.
          imported_password_hash - string - Pre-calculated hash of the user's password. If supplied, this will be used to authenticate the user on first login. Supported hash methods are MD5, SHA1, and SHA256.
          password - string - User password.
          password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `password`.
          announcements_read - boolean - Signifies that the user has read all the announcements in the UI.
          ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned directly to this user, if any.
          allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
          attachments_permission - boolean - DEPRECATED: If `true`, the user can user create Bundles (aka Share Links). Use the bundle permission instead.
          authenticate_until - string - Scheduled Date/Time at which user will be deactivated
          authentication_method - string - How is this user authenticated?
          billing_permission - boolean - Allow this user to perform operations on the account, payments, and invoices?
          bypass_user_lifecycle_rules - boolean - Exempt this user from user lifecycle rules?
          bypass_site_allowed_ips - boolean - Allow this user to skip site-wide IP blacklists?
          dav_permission - boolean - Can the user connect with WebDAV?
          desktop_configuration_profile_id - int64 - Desktop Configuration Profile ID assigned directly to this user, if any.
          default_workspace_id - int64 - Workspace ID the user should land in by default when more than one Workspace is available.
          disabled - boolean - Is user disabled? Disabled users cannot log in, and do not count for billing purposes. Users can be automatically disabled after an inactivity period via a Site setting or schedule to be deactivated after specific date.
          filesystem_layout - string - File system layout
          ftp_permission - boolean - Can the user access with FTP/FTPS?
          header_text - string - Text to display to the user in the header of the UI
          integration_centric_profile_id - int64 - Integration Centric Profile ID assigned directly to this user, if any.
          language - string - Preferred language
          notification_daily_send_time - int64 - Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
          name - string - User's full name
          company - string - User's company
          notes - string - Any internal notes on the user
          office_integration_enabled - boolean - Enable integration with Office for the web?
          partner_admin - boolean - Is this user a Partner administrator?
          partner_id - int64 - Partner ID if this user belongs to a Partner
          password_validity_days - int64 - Number of days to allow user to use the same password
          primary_group_id - int64 - Primary group ID for Group Admin scoping
          readonly_site_admin - boolean - Is the user an allowed to view all (non-billing) site configuration for this site?
          receive_admin_alerts - boolean - Deprecated. Use notify_on_all_site_warnings and granular failure notification preferences instead.
          notify_on_all_site_warnings - boolean - Should the user receive site warnings via email?
          notify_on_all_sso_failures - boolean - Should the user receive sso/scim/ldap configuration/sync failures via email?
          notify_on_all_user_security_events - boolean - Should the user receive user security events via email?
          notify_on_all_pending_work_failures - boolean - Should the user receive pending work failures via email?
          notify_on_all_siem_http_destination_failures - boolean - Should the user receive siem failures via email?
          notify_on_all_sync_failures - boolean - Should the user receive sync failures via email?
          notify_on_all_automation_failures - boolean - Should the user receive automation failures via email?
          notify_on_all_expectation_failures - boolean - Should the user receive expectation failures and misses via email?
          require_login_by - string - Require user to login by specified date otherwise it will be disabled.
          require_password_change - boolean - Is a password change required upon next user login?
          responsible_group_id - int64 - ID of the internal Group responsible for this Partner User, overriding the Partner default.
          responsible_user_id - int64 - ID of the internal User responsible for this Partner User, overriding the Partner default.
          restapi_permission - boolean - Can this user access the Web app, Desktop app, SDKs, or REST API?  (All of these tools use the API internally, so this is one unified permission set.)
          s3_compatible_endpoint_permission - boolean - Can the user access the S3-compatible endpoint? Defaults to true.
          self_managed - boolean - Does this user manage it's own credentials or is it a shared/bot user?
          sftp_permission - boolean - Can the user access with SFTP?
          site_admin - boolean - Is the user an administrator for this site?
          skip_welcome_screen - boolean - Skip Welcome page in the UI?
          ssl_required - string - SSL required setting
          sso_strategy_id - int64 - SSO (Single Sign On) strategy ID for the user, if applicable.
          require_2fa - string - 2FA required setting. `use_system_setting` uses the site-wide setting, including SSO exemptions. `always_require` and `never_require` override the site-wide setting when user-level overrides are allowed.
          tags - string - Comma-separated list of Tags for this user. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
          time_zone - string - User time zone
          user_root - string - If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.
          user_home - string - Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.
          workspace_admin - boolean - Whether the user is an administrator of their own Custom Workspace. Does not reflect administration granted through Permissions.
          username - string - User's username
          workspace_id - int64 - Workspace ID. Only Site Administrators can change this field. Values supplied by Workspace Administrators, Group Administrators, or other non-Site Administrators using `/user` are ignored.
          clear_2fa - boolean - If true when changing authentication_method from `password` to `sso`, remove all two-factor methods. Ignored in all other cases.
          convert_to_partner_user - boolean - Required when assigning a Partner to an existing non-Partner user. If true, convert the user by assigning the partner_id provided.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "avatar_delete" in params and isinstance(
            params["avatar_delete"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: avatar_delete must be an bool"
            )
        if "change_password" in params and not isinstance(
            params["change_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: change_password must be an str"
            )
        if "change_password_confirmation" in params and not isinstance(
            params["change_password_confirmation"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: change_password_confirmation must be an str"
            )
        if "email" in params and not isinstance(params["email"], str):
            raise InvalidParameterError("Bad parameter: email must be an str")
        if "grant_permission" in params and not isinstance(
            params["grant_permission"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: grant_permission must be an str"
            )
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "group_ids" in params and not isinstance(params["group_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an str"
            )
        if "imported_password_hash" in params and not isinstance(
            params["imported_password_hash"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: imported_password_hash must be an str"
            )
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError(
                "Bad parameter: password must be an str"
            )
        if "password_confirmation" in params and not isinstance(
            params["password_confirmation"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: password_confirmation must be an str"
            )
        if "announcements_read" in params and isinstance(
            params["announcements_read"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: announcements_read must be an bool"
            )
        if "ai_assistant_personality_id" in params and (
            not isinstance(params["ai_assistant_personality_id"], int)
            or isinstance(params["ai_assistant_personality_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: ai_assistant_personality_id must be an int"
            )
        if "allowed_ips" in params and not isinstance(
            params["allowed_ips"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: allowed_ips must be an str"
            )
        if "attachments_permission" in params and isinstance(
            params["attachments_permission"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: attachments_permission must be an bool"
            )
        if "authenticate_until" in params and not isinstance(
            params["authenticate_until"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: authenticate_until must be an str"
            )
        if "authentication_method" in params and not isinstance(
            params["authentication_method"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: authentication_method must be an str"
            )
        if "billing_permission" in params and isinstance(
            params["billing_permission"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: billing_permission must be an bool"
            )
        if "bypass_user_lifecycle_rules" in params and isinstance(
            params["bypass_user_lifecycle_rules"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: bypass_user_lifecycle_rules must be an bool"
            )
        if "bypass_site_allowed_ips" in params and isinstance(
            params["bypass_site_allowed_ips"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: bypass_site_allowed_ips must be an bool"
            )
        if "dav_permission" in params and isinstance(
            params["dav_permission"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: dav_permission must be an bool"
            )
        if "desktop_configuration_profile_id" in params and (
            not isinstance(params["desktop_configuration_profile_id"], int)
            or isinstance(params["desktop_configuration_profile_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: desktop_configuration_profile_id must be an int"
            )
        if "default_workspace_id" in params and (
            not isinstance(params["default_workspace_id"], int)
            or isinstance(params["default_workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: default_workspace_id must be an int"
            )
        if "disabled" in params and isinstance(
            params["disabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
            )
        if "filesystem_layout" in params and not isinstance(
            params["filesystem_layout"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: filesystem_layout must be an str"
            )
        if "ftp_permission" in params and isinstance(
            params["ftp_permission"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: ftp_permission must be an bool"
            )
        if "header_text" in params and not isinstance(
            params["header_text"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: header_text must be an str"
            )
        if "integration_centric_profile_id" in params and (
            not isinstance(params["integration_centric_profile_id"], int)
            or isinstance(params["integration_centric_profile_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: integration_centric_profile_id must be an int"
            )
        if "language" in params and not isinstance(params["language"], str):
            raise InvalidParameterError(
                "Bad parameter: language must be an str"
            )
        if "notification_daily_send_time" in params and (
            not isinstance(params["notification_daily_send_time"], int)
            or isinstance(params["notification_daily_send_time"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: notification_daily_send_time must be an int"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "company" in params and not isinstance(params["company"], str):
            raise InvalidParameterError(
                "Bad parameter: company must be an str"
            )
        if "notes" in params and not isinstance(params["notes"], str):
            raise InvalidParameterError("Bad parameter: notes must be an str")
        if "office_integration_enabled" in params and isinstance(
            params["office_integration_enabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: office_integration_enabled must be an bool"
            )
        if "partner_admin" in params and isinstance(
            params["partner_admin"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_admin must be an bool"
            )
        if "partner_id" in params and (
            not isinstance(params["partner_id"], int)
            or isinstance(params["partner_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_id must be an int"
            )
        if "password_validity_days" in params and (
            not isinstance(params["password_validity_days"], int)
            or isinstance(params["password_validity_days"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: password_validity_days must be an int"
            )
        if "primary_group_id" in params and (
            not isinstance(params["primary_group_id"], int)
            or isinstance(params["primary_group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: primary_group_id must be an int"
            )
        if "readonly_site_admin" in params and isinstance(
            params["readonly_site_admin"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: readonly_site_admin must be an bool"
            )
        if "receive_admin_alerts" in params and isinstance(
            params["receive_admin_alerts"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: receive_admin_alerts must be an bool"
            )
        if "notify_on_all_site_warnings" in params and isinstance(
            params["notify_on_all_site_warnings"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_site_warnings must be an bool"
            )
        if "notify_on_all_sso_failures" in params and isinstance(
            params["notify_on_all_sso_failures"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_sso_failures must be an bool"
            )
        if "notify_on_all_user_security_events" in params and isinstance(
            params["notify_on_all_user_security_events"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_user_security_events must be an bool"
            )
        if "notify_on_all_pending_work_failures" in params and isinstance(
            params["notify_on_all_pending_work_failures"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_pending_work_failures must be an bool"
            )
        if (
            "notify_on_all_siem_http_destination_failures" in params
            and isinstance(
                params["notify_on_all_siem_http_destination_failures"],
                (builtins.list, tuple, dict),
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_siem_http_destination_failures must be an bool"
            )
        if "notify_on_all_sync_failures" in params and isinstance(
            params["notify_on_all_sync_failures"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_sync_failures must be an bool"
            )
        if "notify_on_all_automation_failures" in params and isinstance(
            params["notify_on_all_automation_failures"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_automation_failures must be an bool"
            )
        if "notify_on_all_expectation_failures" in params and isinstance(
            params["notify_on_all_expectation_failures"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_expectation_failures must be an bool"
            )
        if "require_login_by" in params and not isinstance(
            params["require_login_by"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: require_login_by must be an str"
            )
        if "require_password_change" in params and isinstance(
            params["require_password_change"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: require_password_change must be an bool"
            )
        if "responsible_group_id" in params and (
            not isinstance(params["responsible_group_id"], int)
            or isinstance(params["responsible_group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: responsible_group_id must be an int"
            )
        if "responsible_user_id" in params and (
            not isinstance(params["responsible_user_id"], int)
            or isinstance(params["responsible_user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: responsible_user_id must be an int"
            )
        if "restapi_permission" in params and isinstance(
            params["restapi_permission"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: restapi_permission must be an bool"
            )
        if "s3_compatible_endpoint_permission" in params and isinstance(
            params["s3_compatible_endpoint_permission"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_compatible_endpoint_permission must be an bool"
            )
        if "self_managed" in params and isinstance(
            params["self_managed"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: self_managed must be an bool"
            )
        if "sftp_permission" in params and isinstance(
            params["sftp_permission"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: sftp_permission must be an bool"
            )
        if "site_admin" in params and isinstance(
            params["site_admin"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: site_admin must be an bool"
            )
        if "skip_welcome_screen" in params and isinstance(
            params["skip_welcome_screen"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_welcome_screen must be an bool"
            )
        if "ssl_required" in params and not isinstance(
            params["ssl_required"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: ssl_required must be an str"
            )
        if "sso_strategy_id" in params and (
            not isinstance(params["sso_strategy_id"], int)
            or isinstance(params["sso_strategy_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: sso_strategy_id must be an int"
            )
        if "require_2fa" in params and not isinstance(
            params["require_2fa"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: require_2fa must be an str"
            )
        if "tags" in params and not isinstance(params["tags"], str):
            raise InvalidParameterError("Bad parameter: tags must be an str")
        if "time_zone" in params and not isinstance(params["time_zone"], str):
            raise InvalidParameterError(
                "Bad parameter: time_zone must be an str"
            )
        if "user_root" in params and not isinstance(params["user_root"], str):
            raise InvalidParameterError(
                "Bad parameter: user_root must be an str"
            )
        if "user_home" in params and not isinstance(params["user_home"], str):
            raise InvalidParameterError(
                "Bad parameter: user_home must be an str"
            )
        if "workspace_admin" in params and isinstance(
            params["workspace_admin"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_admin must be an bool"
            )
        if "username" in params and not isinstance(params["username"], str):
            raise InvalidParameterError(
                "Bad parameter: username must be an str"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "clear_2fa" in params and isinstance(
            params["clear_2fa"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: clear_2fa must be an bool"
            )
        if "convert_to_partner_user" in params and isinstance(
            params["convert_to_partner_user"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: convert_to_partner_user must be an bool"
            )
        params = with_attachments(params, "avatar_file")
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/users/" + path_value(params["id"]), params
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        """Parameters:
        new_owner_id - int64 - Provide a User ID here to transfer ownership of certain resources such as Automations and Share Links (Bundles) to that new user.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "new_owner_id" in params and (
            not isinstance(params["new_owner_id"], int)
            or isinstance(params["new_owner_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: new_owner_id must be an int"
            )
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE", "/users/" + path_value(params["id"]), params
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Update this object on the server if it has an id, or else create
        it, taking in place the record the server returns."""
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = UserResource(self._scope()).create(self.get_attributes())
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class UserResource:
    """User operations that use one client's configuration.

    Get one from a client, such as ``client.user``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[User]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `workspace_id`, `company`, `name`, `disabled`, `authenticate_until`, `username`, `email`, `site_admin`, `last_desktop_login_at`, `last_login_at`, `password_validity_days` or `ssl_required`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `username`, `name`, `email`, `company`, `site_admin`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until`, `not_site_admin`, `disabled`, `partner_id`, `primary_group_id` or `workspace_id`. Valid field combinations are `[ site_admin, username ]`, `[ not_site_admin, username ]`, `[ workspace_id, username ]`, `[ company, name ]`, `[ workspace_id, name ]`, `[ workspace_id, email ]`, `[ workspace_id, company ]`, `[ workspace_id, site_admin ]`, `[ workspace_id, not_site_admin ]`, `[ workspace_id, disabled ]`, `[ workspace_id, partner_id ]`, `[ workspace_id, site_admin, username ]`, `[ workspace_id, not_site_admin, username ]`, `[ workspace_id, disabled, username ]`, `[ workspace_id, partner_id, username ]` or `[ workspace_id, company, name ]`.
        filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `password_validity_days`, `last_login_at` or `authenticate_until`.
        filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `password_validity_days`, `last_login_at` or `authenticate_until`.
        filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `username`, `name`, `email` or `company`. Valid field combinations are `[ company, name ]`.
        filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `password_validity_days`, `last_login_at` or `authenticate_until`.
        filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `password_validity_days`, `last_login_at` or `authenticate_until`.
        ids - string - comma-separated list of User IDs
        include_parent_site_users - boolean - Include users from the parent site.
        include_default_workspace_users - boolean - When scoped to a Custom Workspace, include Default Workspace users who have permissions in that Workspace. Available to Site Administrators, and to Workspace Administrators and Folder Admins in that Workspace when the site shares its Default Workspace directory with Workspaces.
        search - string - Searches for partial matches of name, username, or email.
        """
        params = copy_params(params)
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        if "sort_by" in params and not isinstance(params["sort_by"], dict):
            raise InvalidParameterError(
                "Bad parameter: sort_by must be an dict"
            )
        if "filter" in params and not isinstance(params["filter"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter must be an dict"
            )
        if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter_gt must be an dict"
            )
        if "filter_gteq" in params and not isinstance(
            params["filter_gteq"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_gteq must be an dict"
            )
        if "filter_prefix" in params and not isinstance(
            params["filter_prefix"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_prefix must be an dict"
            )
        if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter_lt must be an dict"
            )
        if "filter_lteq" in params and not isinstance(
            params["filter_lteq"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_lteq must be an dict"
            )
        if "ids" in params and not isinstance(params["ids"], str):
            raise InvalidParameterError("Bad parameter: ids must be an str")
        if "include_parent_site_users" in params and not isinstance(
            params["include_parent_site_users"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: include_parent_site_users must be an bool"
            )
        if "include_default_workspace_users" in params and not isinstance(
            params["include_default_workspace_users"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: include_default_workspace_users must be an bool"
            )
        if "search" in params and not isinstance(params["search"], str):
            raise InvalidParameterError("Bad parameter: search must be an str")
        operation = Operation.start(self._scope, options)
        return ListObj(User, "GET", "/users", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[User]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> User:
        """Parameters:
        id (required) - int64 - User ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> User:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/users/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, User)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> User:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> User:
        """Parameters:
        avatar_file - file - An image file for your user avatar.
        avatar_delete - boolean - If true, the avatar will be deleted.
        change_password - string - Used for changing a password on an existing user.
        change_password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
        email - string - User's email.
        grant_permission - string - Permission to grant on the User Root upon creation, or on the Workspace root when the User Root is blank. For the Default Workspace, a blank User Root uses the site root. `admin` on a Custom Workspace's root grants Workspace Administrator access; on a subfolder it grants Folder Admin access. Can be blank or `admin`, `full`, `read`, `write`, `list`, `read+write`, `list+write`, or `history`.
        group_id - int64 - Group ID to associate this user with.
        group_ids - string - A list of group ids to associate this user with.  Comma delimited.
        imported_password_hash - string - Pre-calculated hash of the user's password. If supplied, this will be used to authenticate the user on first login. Supported hash methods are MD5, SHA1, and SHA256.
        password - string - User password.
        password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `password`.
        announcements_read - boolean - Signifies that the user has read all the announcements in the UI.
        ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned directly to this user, if any.
        allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
        attachments_permission - boolean - DEPRECATED: If `true`, the user can user create Bundles (aka Share Links). Use the bundle permission instead.
        authenticate_until - string - Scheduled Date/Time at which user will be deactivated
        authentication_method - string - How is this user authenticated?
        billing_permission - boolean - Allow this user to perform operations on the account, payments, and invoices?
        bypass_user_lifecycle_rules - boolean - Exempt this user from user lifecycle rules?
        bypass_site_allowed_ips - boolean - Allow this user to skip site-wide IP blacklists?
        dav_permission - boolean - Can the user connect with WebDAV?
        desktop_configuration_profile_id - int64 - Desktop Configuration Profile ID assigned directly to this user, if any.
        default_workspace_id - int64 - Workspace ID the user should land in by default when more than one Workspace is available.
        disabled - boolean - Is user disabled? Disabled users cannot log in, and do not count for billing purposes. Users can be automatically disabled after an inactivity period via a Site setting or schedule to be deactivated after specific date.
        filesystem_layout - string - File system layout
        ftp_permission - boolean - Can the user access with FTP/FTPS?
        header_text - string - Text to display to the user in the header of the UI
        integration_centric_profile_id - int64 - Integration Centric Profile ID assigned directly to this user, if any.
        language - string - Preferred language
        notification_daily_send_time - int64 - Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
        name - string - User's full name
        company - string - User's company
        notes - string - Any internal notes on the user
        office_integration_enabled - boolean - Enable integration with Office for the web?
        partner_admin - boolean - Is this user a Partner administrator?
        partner_id - int64 - Partner ID if this user belongs to a Partner
        password_validity_days - int64 - Number of days to allow user to use the same password
        primary_group_id - int64 - Primary group ID for Group Admin scoping
        readonly_site_admin - boolean - Is the user an allowed to view all (non-billing) site configuration for this site?
        receive_admin_alerts - boolean - Deprecated. Use notify_on_all_site_warnings and granular failure notification preferences instead.
        notify_on_all_site_warnings - boolean - Should the user receive site warnings via email?
        notify_on_all_sso_failures - boolean - Should the user receive sso/scim/ldap configuration/sync failures via email?
        notify_on_all_user_security_events - boolean - Should the user receive user security events via email?
        notify_on_all_pending_work_failures - boolean - Should the user receive pending work failures via email?
        notify_on_all_siem_http_destination_failures - boolean - Should the user receive siem failures via email?
        notify_on_all_sync_failures - boolean - Should the user receive sync failures via email?
        notify_on_all_automation_failures - boolean - Should the user receive automation failures via email?
        notify_on_all_expectation_failures - boolean - Should the user receive expectation failures and misses via email?
        require_login_by - string - Require user to login by specified date otherwise it will be disabled.
        require_password_change - boolean - Is a password change required upon next user login?
        responsible_group_id - int64 - ID of the internal Group responsible for this Partner User, overriding the Partner default.
        responsible_user_id - int64 - ID of the internal User responsible for this Partner User, overriding the Partner default.
        restapi_permission - boolean - Can this user access the Web app, Desktop app, SDKs, or REST API?  (All of these tools use the API internally, so this is one unified permission set.)
        s3_compatible_endpoint_permission - boolean - Can the user access the S3-compatible endpoint? Defaults to true.
        self_managed - boolean - Does this user manage it's own credentials or is it a shared/bot user?
        sftp_permission - boolean - Can the user access with SFTP?
        site_admin - boolean - Is the user an administrator for this site?
        skip_welcome_screen - boolean - Skip Welcome page in the UI?
        ssl_required - string - SSL required setting
        sso_strategy_id - int64 - SSO (Single Sign On) strategy ID for the user, if applicable.
        require_2fa - string - 2FA required setting. `use_system_setting` uses the site-wide setting, including SSO exemptions. `always_require` and `never_require` override the site-wide setting when user-level overrides are allowed.
        tags - string - Comma-separated list of Tags for this user. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
        time_zone - string - User time zone
        user_root - string - If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.
        user_home - string - Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.
        workspace_admin - boolean - Whether the user is an administrator of their own Custom Workspace. Does not reflect administration granted through Permissions.
        username (required) - string - User's username
        workspace_id - int64 - ID of the Workspace the user belongs to. 0 is the Default Workspace.
        """
        params = copy_params(params)
        if "avatar_delete" in params and not isinstance(
            params["avatar_delete"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: avatar_delete must be an bool"
            )
        if "change_password" in params and not isinstance(
            params["change_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: change_password must be an str"
            )
        if "change_password_confirmation" in params and not isinstance(
            params["change_password_confirmation"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: change_password_confirmation must be an str"
            )
        if "email" in params and not isinstance(params["email"], str):
            raise InvalidParameterError("Bad parameter: email must be an str")
        if "grant_permission" in params and not isinstance(
            params["grant_permission"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: grant_permission must be an str"
            )
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "group_ids" in params and not isinstance(params["group_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an str"
            )
        if "imported_password_hash" in params and not isinstance(
            params["imported_password_hash"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: imported_password_hash must be an str"
            )
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError(
                "Bad parameter: password must be an str"
            )
        if "password_confirmation" in params and not isinstance(
            params["password_confirmation"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: password_confirmation must be an str"
            )
        if "announcements_read" in params and not isinstance(
            params["announcements_read"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: announcements_read must be an bool"
            )
        if "ai_assistant_personality_id" in params and (
            not isinstance(params["ai_assistant_personality_id"], int)
            or isinstance(params["ai_assistant_personality_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: ai_assistant_personality_id must be an int"
            )
        if "allowed_ips" in params and not isinstance(
            params["allowed_ips"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: allowed_ips must be an str"
            )
        if "attachments_permission" in params and not isinstance(
            params["attachments_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: attachments_permission must be an bool"
            )
        if "authenticate_until" in params and not isinstance(
            params["authenticate_until"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: authenticate_until must be an str"
            )
        if "authentication_method" in params and not isinstance(
            params["authentication_method"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: authentication_method must be an str"
            )
        if "billing_permission" in params and not isinstance(
            params["billing_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: billing_permission must be an bool"
            )
        if "bypass_user_lifecycle_rules" in params and not isinstance(
            params["bypass_user_lifecycle_rules"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: bypass_user_lifecycle_rules must be an bool"
            )
        if "bypass_site_allowed_ips" in params and not isinstance(
            params["bypass_site_allowed_ips"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: bypass_site_allowed_ips must be an bool"
            )
        if "dav_permission" in params and not isinstance(
            params["dav_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: dav_permission must be an bool"
            )
        if "desktop_configuration_profile_id" in params and (
            not isinstance(params["desktop_configuration_profile_id"], int)
            or isinstance(params["desktop_configuration_profile_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: desktop_configuration_profile_id must be an int"
            )
        if "default_workspace_id" in params and (
            not isinstance(params["default_workspace_id"], int)
            or isinstance(params["default_workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: default_workspace_id must be an int"
            )
        if "disabled" in params and not isinstance(params["disabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
            )
        if "filesystem_layout" in params and not isinstance(
            params["filesystem_layout"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: filesystem_layout must be an str"
            )
        if "ftp_permission" in params and not isinstance(
            params["ftp_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: ftp_permission must be an bool"
            )
        if "header_text" in params and not isinstance(
            params["header_text"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: header_text must be an str"
            )
        if "integration_centric_profile_id" in params and (
            not isinstance(params["integration_centric_profile_id"], int)
            or isinstance(params["integration_centric_profile_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: integration_centric_profile_id must be an int"
            )
        if "language" in params and not isinstance(params["language"], str):
            raise InvalidParameterError(
                "Bad parameter: language must be an str"
            )
        if "notification_daily_send_time" in params and (
            not isinstance(params["notification_daily_send_time"], int)
            or isinstance(params["notification_daily_send_time"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: notification_daily_send_time must be an int"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "company" in params and not isinstance(params["company"], str):
            raise InvalidParameterError(
                "Bad parameter: company must be an str"
            )
        if "notes" in params and not isinstance(params["notes"], str):
            raise InvalidParameterError("Bad parameter: notes must be an str")
        if "office_integration_enabled" in params and not isinstance(
            params["office_integration_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: office_integration_enabled must be an bool"
            )
        if "partner_admin" in params and not isinstance(
            params["partner_admin"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_admin must be an bool"
            )
        if "partner_id" in params and (
            not isinstance(params["partner_id"], int)
            or isinstance(params["partner_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_id must be an int"
            )
        if "password_validity_days" in params and (
            not isinstance(params["password_validity_days"], int)
            or isinstance(params["password_validity_days"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: password_validity_days must be an int"
            )
        if "primary_group_id" in params and (
            not isinstance(params["primary_group_id"], int)
            or isinstance(params["primary_group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: primary_group_id must be an int"
            )
        if "readonly_site_admin" in params and not isinstance(
            params["readonly_site_admin"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: readonly_site_admin must be an bool"
            )
        if "receive_admin_alerts" in params and not isinstance(
            params["receive_admin_alerts"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: receive_admin_alerts must be an bool"
            )
        if "notify_on_all_site_warnings" in params and not isinstance(
            params["notify_on_all_site_warnings"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_site_warnings must be an bool"
            )
        if "notify_on_all_sso_failures" in params and not isinstance(
            params["notify_on_all_sso_failures"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_sso_failures must be an bool"
            )
        if "notify_on_all_user_security_events" in params and not isinstance(
            params["notify_on_all_user_security_events"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_user_security_events must be an bool"
            )
        if "notify_on_all_pending_work_failures" in params and not isinstance(
            params["notify_on_all_pending_work_failures"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_pending_work_failures must be an bool"
            )
        if (
            "notify_on_all_siem_http_destination_failures" in params
            and not isinstance(
                params["notify_on_all_siem_http_destination_failures"], bool
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_siem_http_destination_failures must be an bool"
            )
        if "notify_on_all_sync_failures" in params and not isinstance(
            params["notify_on_all_sync_failures"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_sync_failures must be an bool"
            )
        if "notify_on_all_automation_failures" in params and not isinstance(
            params["notify_on_all_automation_failures"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_automation_failures must be an bool"
            )
        if "notify_on_all_expectation_failures" in params and not isinstance(
            params["notify_on_all_expectation_failures"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_expectation_failures must be an bool"
            )
        if "require_login_by" in params and not isinstance(
            params["require_login_by"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: require_login_by must be an str"
            )
        if "require_password_change" in params and not isinstance(
            params["require_password_change"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: require_password_change must be an bool"
            )
        if "responsible_group_id" in params and (
            not isinstance(params["responsible_group_id"], int)
            or isinstance(params["responsible_group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: responsible_group_id must be an int"
            )
        if "responsible_user_id" in params and (
            not isinstance(params["responsible_user_id"], int)
            or isinstance(params["responsible_user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: responsible_user_id must be an int"
            )
        if "restapi_permission" in params and not isinstance(
            params["restapi_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: restapi_permission must be an bool"
            )
        if "s3_compatible_endpoint_permission" in params and not isinstance(
            params["s3_compatible_endpoint_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_compatible_endpoint_permission must be an bool"
            )
        if "self_managed" in params and not isinstance(
            params["self_managed"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: self_managed must be an bool"
            )
        if "sftp_permission" in params and not isinstance(
            params["sftp_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sftp_permission must be an bool"
            )
        if "site_admin" in params and not isinstance(
            params["site_admin"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: site_admin must be an bool"
            )
        if "skip_welcome_screen" in params and not isinstance(
            params["skip_welcome_screen"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_welcome_screen must be an bool"
            )
        if "ssl_required" in params and not isinstance(
            params["ssl_required"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: ssl_required must be an str"
            )
        if "sso_strategy_id" in params and (
            not isinstance(params["sso_strategy_id"], int)
            or isinstance(params["sso_strategy_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: sso_strategy_id must be an int"
            )
        if "require_2fa" in params and not isinstance(
            params["require_2fa"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: require_2fa must be an str"
            )
        if "tags" in params and not isinstance(params["tags"], str):
            raise InvalidParameterError("Bad parameter: tags must be an str")
        if "time_zone" in params and not isinstance(params["time_zone"], str):
            raise InvalidParameterError(
                "Bad parameter: time_zone must be an str"
            )
        if "user_root" in params and not isinstance(params["user_root"], str):
            raise InvalidParameterError(
                "Bad parameter: user_root must be an str"
            )
        if "user_home" in params and not isinstance(params["user_home"], str):
            raise InvalidParameterError(
                "Bad parameter: user_home must be an str"
            )
        if "workspace_admin" in params and not isinstance(
            params["workspace_admin"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_admin must be an bool"
            )
        if "username" in params and not isinstance(params["username"], str):
            raise InvalidParameterError(
                "Bad parameter: username must be an str"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "username" not in params:
            raise MissingParameterError("Parameter missing: username")
        params = with_attachments(params, "avatar_file")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/users", params)
        return operation.decode_model(response, User)

    def unlock(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Unlock user who has been locked out due to failed logins"""
        return self.__unlock({"id": id}, params, options)

    def __unlock(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "POST", "/users/" + path_value(params["id"]) + "/unlock", params
        )

    def resend_welcome_email(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Resend user welcome email"""
        return self.__resend_welcome_email({"id": id}, params, options)

    def __resend_welcome_email(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "POST",
            "/users/" + path_value(params["id"]) + "/resend_welcome_email",
            params,
        )

    def user_2fa_reset(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Trigger 2FA Reset process for user who has lost access to their existing 2FA methods"""
        return self.__user_2fa_reset({"id": id}, params, options)

    def __user_2fa_reset(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "POST", "/users/" + path_value(params["id"]) + "/2fa/reset", params
        )

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> User:
        """Parameters:
        avatar_file - file - An image file for your user avatar.
        avatar_delete - boolean - If true, the avatar will be deleted.
        change_password - string - Used for changing a password on an existing user.
        change_password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
        email - string - User's email.
        grant_permission - string - Permission to grant on the User Root upon creation, or on the Workspace root when the User Root is blank. For the Default Workspace, a blank User Root uses the site root. `admin` on a Custom Workspace's root grants Workspace Administrator access; on a subfolder it grants Folder Admin access. Can be blank or `admin`, `full`, `read`, `write`, `list`, `read+write`, `list+write`, or `history`.
        group_id - int64 - Group ID to associate this user with.
        group_ids - string - A list of group ids to associate this user with.  Comma delimited.
        imported_password_hash - string - Pre-calculated hash of the user's password. If supplied, this will be used to authenticate the user on first login. Supported hash methods are MD5, SHA1, and SHA256.
        password - string - User password.
        password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `password`.
        announcements_read - boolean - Signifies that the user has read all the announcements in the UI.
        ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned directly to this user, if any.
        allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
        attachments_permission - boolean - DEPRECATED: If `true`, the user can user create Bundles (aka Share Links). Use the bundle permission instead.
        authenticate_until - string - Scheduled Date/Time at which user will be deactivated
        authentication_method - string - How is this user authenticated?
        billing_permission - boolean - Allow this user to perform operations on the account, payments, and invoices?
        bypass_user_lifecycle_rules - boolean - Exempt this user from user lifecycle rules?
        bypass_site_allowed_ips - boolean - Allow this user to skip site-wide IP blacklists?
        dav_permission - boolean - Can the user connect with WebDAV?
        desktop_configuration_profile_id - int64 - Desktop Configuration Profile ID assigned directly to this user, if any.
        default_workspace_id - int64 - Workspace ID the user should land in by default when more than one Workspace is available.
        disabled - boolean - Is user disabled? Disabled users cannot log in, and do not count for billing purposes. Users can be automatically disabled after an inactivity period via a Site setting or schedule to be deactivated after specific date.
        filesystem_layout - string - File system layout
        ftp_permission - boolean - Can the user access with FTP/FTPS?
        header_text - string - Text to display to the user in the header of the UI
        integration_centric_profile_id - int64 - Integration Centric Profile ID assigned directly to this user, if any.
        language - string - Preferred language
        notification_daily_send_time - int64 - Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
        name - string - User's full name
        company - string - User's company
        notes - string - Any internal notes on the user
        office_integration_enabled - boolean - Enable integration with Office for the web?
        partner_admin - boolean - Is this user a Partner administrator?
        partner_id - int64 - Partner ID if this user belongs to a Partner
        password_validity_days - int64 - Number of days to allow user to use the same password
        primary_group_id - int64 - Primary group ID for Group Admin scoping
        readonly_site_admin - boolean - Is the user an allowed to view all (non-billing) site configuration for this site?
        receive_admin_alerts - boolean - Deprecated. Use notify_on_all_site_warnings and granular failure notification preferences instead.
        notify_on_all_site_warnings - boolean - Should the user receive site warnings via email?
        notify_on_all_sso_failures - boolean - Should the user receive sso/scim/ldap configuration/sync failures via email?
        notify_on_all_user_security_events - boolean - Should the user receive user security events via email?
        notify_on_all_pending_work_failures - boolean - Should the user receive pending work failures via email?
        notify_on_all_siem_http_destination_failures - boolean - Should the user receive siem failures via email?
        notify_on_all_sync_failures - boolean - Should the user receive sync failures via email?
        notify_on_all_automation_failures - boolean - Should the user receive automation failures via email?
        notify_on_all_expectation_failures - boolean - Should the user receive expectation failures and misses via email?
        require_login_by - string - Require user to login by specified date otherwise it will be disabled.
        require_password_change - boolean - Is a password change required upon next user login?
        responsible_group_id - int64 - ID of the internal Group responsible for this Partner User, overriding the Partner default.
        responsible_user_id - int64 - ID of the internal User responsible for this Partner User, overriding the Partner default.
        restapi_permission - boolean - Can this user access the Web app, Desktop app, SDKs, or REST API?  (All of these tools use the API internally, so this is one unified permission set.)
        s3_compatible_endpoint_permission - boolean - Can the user access the S3-compatible endpoint? Defaults to true.
        self_managed - boolean - Does this user manage it's own credentials or is it a shared/bot user?
        sftp_permission - boolean - Can the user access with SFTP?
        site_admin - boolean - Is the user an administrator for this site?
        skip_welcome_screen - boolean - Skip Welcome page in the UI?
        ssl_required - string - SSL required setting
        sso_strategy_id - int64 - SSO (Single Sign On) strategy ID for the user, if applicable.
        require_2fa - string - 2FA required setting. `use_system_setting` uses the site-wide setting, including SSO exemptions. `always_require` and `never_require` override the site-wide setting when user-level overrides are allowed.
        tags - string - Comma-separated list of Tags for this user. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
        time_zone - string - User time zone
        user_root - string - If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.
        user_home - string - Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.
        workspace_admin - boolean - Whether the user is an administrator of their own Custom Workspace. Does not reflect administration granted through Permissions.
        username - string - User's username
        workspace_id - int64 - Workspace ID. Only Site Administrators can change this field. Values supplied by Workspace Administrators, Group Administrators, or other non-Site Administrators using `/user` are ignored.
        clear_2fa - boolean - If true when changing authentication_method from `password` to `sso`, remove all two-factor methods. Ignored in all other cases.
        convert_to_partner_user - boolean - Required when assigning a Partner to an existing non-Partner user. If true, convert the user by assigning the partner_id provided.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> User:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "avatar_delete" in params and not isinstance(
            params["avatar_delete"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: avatar_delete must be an bool"
            )
        if "change_password" in params and not isinstance(
            params["change_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: change_password must be an str"
            )
        if "change_password_confirmation" in params and not isinstance(
            params["change_password_confirmation"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: change_password_confirmation must be an str"
            )
        if "email" in params and not isinstance(params["email"], str):
            raise InvalidParameterError("Bad parameter: email must be an str")
        if "grant_permission" in params and not isinstance(
            params["grant_permission"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: grant_permission must be an str"
            )
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "group_ids" in params and not isinstance(params["group_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an str"
            )
        if "imported_password_hash" in params and not isinstance(
            params["imported_password_hash"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: imported_password_hash must be an str"
            )
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError(
                "Bad parameter: password must be an str"
            )
        if "password_confirmation" in params and not isinstance(
            params["password_confirmation"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: password_confirmation must be an str"
            )
        if "announcements_read" in params and not isinstance(
            params["announcements_read"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: announcements_read must be an bool"
            )
        if "ai_assistant_personality_id" in params and (
            not isinstance(params["ai_assistant_personality_id"], int)
            or isinstance(params["ai_assistant_personality_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: ai_assistant_personality_id must be an int"
            )
        if "allowed_ips" in params and not isinstance(
            params["allowed_ips"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: allowed_ips must be an str"
            )
        if "attachments_permission" in params and not isinstance(
            params["attachments_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: attachments_permission must be an bool"
            )
        if "authenticate_until" in params and not isinstance(
            params["authenticate_until"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: authenticate_until must be an str"
            )
        if "authentication_method" in params and not isinstance(
            params["authentication_method"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: authentication_method must be an str"
            )
        if "billing_permission" in params and not isinstance(
            params["billing_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: billing_permission must be an bool"
            )
        if "bypass_user_lifecycle_rules" in params and not isinstance(
            params["bypass_user_lifecycle_rules"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: bypass_user_lifecycle_rules must be an bool"
            )
        if "bypass_site_allowed_ips" in params and not isinstance(
            params["bypass_site_allowed_ips"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: bypass_site_allowed_ips must be an bool"
            )
        if "dav_permission" in params and not isinstance(
            params["dav_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: dav_permission must be an bool"
            )
        if "desktop_configuration_profile_id" in params and (
            not isinstance(params["desktop_configuration_profile_id"], int)
            or isinstance(params["desktop_configuration_profile_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: desktop_configuration_profile_id must be an int"
            )
        if "default_workspace_id" in params and (
            not isinstance(params["default_workspace_id"], int)
            or isinstance(params["default_workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: default_workspace_id must be an int"
            )
        if "disabled" in params and not isinstance(params["disabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
            )
        if "filesystem_layout" in params and not isinstance(
            params["filesystem_layout"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: filesystem_layout must be an str"
            )
        if "ftp_permission" in params and not isinstance(
            params["ftp_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: ftp_permission must be an bool"
            )
        if "header_text" in params and not isinstance(
            params["header_text"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: header_text must be an str"
            )
        if "integration_centric_profile_id" in params and (
            not isinstance(params["integration_centric_profile_id"], int)
            or isinstance(params["integration_centric_profile_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: integration_centric_profile_id must be an int"
            )
        if "language" in params and not isinstance(params["language"], str):
            raise InvalidParameterError(
                "Bad parameter: language must be an str"
            )
        if "notification_daily_send_time" in params and (
            not isinstance(params["notification_daily_send_time"], int)
            or isinstance(params["notification_daily_send_time"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: notification_daily_send_time must be an int"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "company" in params and not isinstance(params["company"], str):
            raise InvalidParameterError(
                "Bad parameter: company must be an str"
            )
        if "notes" in params and not isinstance(params["notes"], str):
            raise InvalidParameterError("Bad parameter: notes must be an str")
        if "office_integration_enabled" in params and not isinstance(
            params["office_integration_enabled"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: office_integration_enabled must be an bool"
            )
        if "partner_admin" in params and not isinstance(
            params["partner_admin"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_admin must be an bool"
            )
        if "partner_id" in params and (
            not isinstance(params["partner_id"], int)
            or isinstance(params["partner_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_id must be an int"
            )
        if "password_validity_days" in params and (
            not isinstance(params["password_validity_days"], int)
            or isinstance(params["password_validity_days"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: password_validity_days must be an int"
            )
        if "primary_group_id" in params and (
            not isinstance(params["primary_group_id"], int)
            or isinstance(params["primary_group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: primary_group_id must be an int"
            )
        if "readonly_site_admin" in params and not isinstance(
            params["readonly_site_admin"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: readonly_site_admin must be an bool"
            )
        if "receive_admin_alerts" in params and not isinstance(
            params["receive_admin_alerts"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: receive_admin_alerts must be an bool"
            )
        if "notify_on_all_site_warnings" in params and not isinstance(
            params["notify_on_all_site_warnings"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_site_warnings must be an bool"
            )
        if "notify_on_all_sso_failures" in params and not isinstance(
            params["notify_on_all_sso_failures"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_sso_failures must be an bool"
            )
        if "notify_on_all_user_security_events" in params and not isinstance(
            params["notify_on_all_user_security_events"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_user_security_events must be an bool"
            )
        if "notify_on_all_pending_work_failures" in params and not isinstance(
            params["notify_on_all_pending_work_failures"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_pending_work_failures must be an bool"
            )
        if (
            "notify_on_all_siem_http_destination_failures" in params
            and not isinstance(
                params["notify_on_all_siem_http_destination_failures"], bool
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_siem_http_destination_failures must be an bool"
            )
        if "notify_on_all_sync_failures" in params and not isinstance(
            params["notify_on_all_sync_failures"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_sync_failures must be an bool"
            )
        if "notify_on_all_automation_failures" in params and not isinstance(
            params["notify_on_all_automation_failures"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_automation_failures must be an bool"
            )
        if "notify_on_all_expectation_failures" in params and not isinstance(
            params["notify_on_all_expectation_failures"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_all_expectation_failures must be an bool"
            )
        if "require_login_by" in params and not isinstance(
            params["require_login_by"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: require_login_by must be an str"
            )
        if "require_password_change" in params and not isinstance(
            params["require_password_change"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: require_password_change must be an bool"
            )
        if "responsible_group_id" in params and (
            not isinstance(params["responsible_group_id"], int)
            or isinstance(params["responsible_group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: responsible_group_id must be an int"
            )
        if "responsible_user_id" in params and (
            not isinstance(params["responsible_user_id"], int)
            or isinstance(params["responsible_user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: responsible_user_id must be an int"
            )
        if "restapi_permission" in params and not isinstance(
            params["restapi_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: restapi_permission must be an bool"
            )
        if "s3_compatible_endpoint_permission" in params and not isinstance(
            params["s3_compatible_endpoint_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_compatible_endpoint_permission must be an bool"
            )
        if "self_managed" in params and not isinstance(
            params["self_managed"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: self_managed must be an bool"
            )
        if "sftp_permission" in params and not isinstance(
            params["sftp_permission"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: sftp_permission must be an bool"
            )
        if "site_admin" in params and not isinstance(
            params["site_admin"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: site_admin must be an bool"
            )
        if "skip_welcome_screen" in params and not isinstance(
            params["skip_welcome_screen"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_welcome_screen must be an bool"
            )
        if "ssl_required" in params and not isinstance(
            params["ssl_required"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: ssl_required must be an str"
            )
        if "sso_strategy_id" in params and (
            not isinstance(params["sso_strategy_id"], int)
            or isinstance(params["sso_strategy_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: sso_strategy_id must be an int"
            )
        if "require_2fa" in params and not isinstance(
            params["require_2fa"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: require_2fa must be an str"
            )
        if "tags" in params and not isinstance(params["tags"], str):
            raise InvalidParameterError("Bad parameter: tags must be an str")
        if "time_zone" in params and not isinstance(params["time_zone"], str):
            raise InvalidParameterError(
                "Bad parameter: time_zone must be an str"
            )
        if "user_root" in params and not isinstance(params["user_root"], str):
            raise InvalidParameterError(
                "Bad parameter: user_root must be an str"
            )
        if "user_home" in params and not isinstance(params["user_home"], str):
            raise InvalidParameterError(
                "Bad parameter: user_home must be an str"
            )
        if "workspace_admin" in params and not isinstance(
            params["workspace_admin"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_admin must be an bool"
            )
        if "username" in params and not isinstance(params["username"], str):
            raise InvalidParameterError(
                "Bad parameter: username must be an str"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "clear_2fa" in params and not isinstance(params["clear_2fa"], bool):
            raise InvalidParameterError(
                "Bad parameter: clear_2fa must be an bool"
            )
        if "convert_to_partner_user" in params and not isinstance(
            params["convert_to_partner_user"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: convert_to_partner_user must be an bool"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        params = with_attachments(params, "avatar_file")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/users/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, User)

    def delete(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Parameters:
        new_owner_id - int64 - Provide a User ID here to transfer ownership of certain resources such as Automations and Share Links (Bundles) to that new user.
        """
        return self.__delete({"id": id}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "new_owner_id" in params and (
            not isinstance(params["new_owner_id"], int)
            or isinstance(params["new_owner_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: new_owner_id must be an int"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE", "/users/" + path_value(params["id"]), params
        )

    def destroy(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> User:
        """A new User with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = User(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = UserResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[User]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `workspace_id`, `company`, `name`, `disabled`, `authenticate_until`, `username`, `email`, `site_admin`, `last_desktop_login_at`, `last_login_at`, `password_validity_days` or `ssl_required`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `username`, `name`, `email`, `company`, `site_admin`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until`, `not_site_admin`, `disabled`, `partner_id`, `primary_group_id` or `workspace_id`. Valid field combinations are `[ site_admin, username ]`, `[ not_site_admin, username ]`, `[ workspace_id, username ]`, `[ company, name ]`, `[ workspace_id, name ]`, `[ workspace_id, email ]`, `[ workspace_id, company ]`, `[ workspace_id, site_admin ]`, `[ workspace_id, not_site_admin ]`, `[ workspace_id, disabled ]`, `[ workspace_id, partner_id ]`, `[ workspace_id, site_admin, username ]`, `[ workspace_id, not_site_admin, username ]`, `[ workspace_id, disabled, username ]`, `[ workspace_id, partner_id, username ]` or `[ workspace_id, company, name ]`.
    filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `password_validity_days`, `last_login_at` or `authenticate_until`.
    filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `password_validity_days`, `last_login_at` or `authenticate_until`.
    filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `username`, `name`, `email` or `company`. Valid field combinations are `[ company, name ]`.
    filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `password_validity_days`, `last_login_at` or `authenticate_until`.
    filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `password_validity_days`, `last_login_at` or `authenticate_until`.
    ids - string - comma-separated list of User IDs
    include_parent_site_users - boolean - Include users from the parent site.
    include_default_workspace_users - boolean - When scoped to a Custom Workspace, include Default Workspace users who have permissions in that Workspace. Available to Site Administrators, and to Workspace Administrators and Folder Admins in that Workspace when the site shares its Default Workspace directory with Workspaces.
    search - string - Searches for partial matches of name, username, or email.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[User]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> User:
    """Parameters:
    id (required) - int64 - User ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> User:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> User:
    """Parameters:
    avatar_file - file - An image file for your user avatar.
    avatar_delete - boolean - If true, the avatar will be deleted.
    change_password - string - Used for changing a password on an existing user.
    change_password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
    email - string - User's email.
    grant_permission - string - Permission to grant on the User Root upon creation, or on the Workspace root when the User Root is blank. For the Default Workspace, a blank User Root uses the site root. `admin` on a Custom Workspace's root grants Workspace Administrator access; on a subfolder it grants Folder Admin access. Can be blank or `admin`, `full`, `read`, `write`, `list`, `read+write`, `list+write`, or `history`.
    group_id - int64 - Group ID to associate this user with.
    group_ids - string - A list of group ids to associate this user with.  Comma delimited.
    imported_password_hash - string - Pre-calculated hash of the user's password. If supplied, this will be used to authenticate the user on first login. Supported hash methods are MD5, SHA1, and SHA256.
    password - string - User password.
    password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `password`.
    announcements_read - boolean - Signifies that the user has read all the announcements in the UI.
    ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned directly to this user, if any.
    allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
    attachments_permission - boolean - DEPRECATED: If `true`, the user can user create Bundles (aka Share Links). Use the bundle permission instead.
    authenticate_until - string - Scheduled Date/Time at which user will be deactivated
    authentication_method - string - How is this user authenticated?
    billing_permission - boolean - Allow this user to perform operations on the account, payments, and invoices?
    bypass_user_lifecycle_rules - boolean - Exempt this user from user lifecycle rules?
    bypass_site_allowed_ips - boolean - Allow this user to skip site-wide IP blacklists?
    dav_permission - boolean - Can the user connect with WebDAV?
    desktop_configuration_profile_id - int64 - Desktop Configuration Profile ID assigned directly to this user, if any.
    default_workspace_id - int64 - Workspace ID the user should land in by default when more than one Workspace is available.
    disabled - boolean - Is user disabled? Disabled users cannot log in, and do not count for billing purposes. Users can be automatically disabled after an inactivity period via a Site setting or schedule to be deactivated after specific date.
    filesystem_layout - string - File system layout
    ftp_permission - boolean - Can the user access with FTP/FTPS?
    header_text - string - Text to display to the user in the header of the UI
    integration_centric_profile_id - int64 - Integration Centric Profile ID assigned directly to this user, if any.
    language - string - Preferred language
    notification_daily_send_time - int64 - Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
    name - string - User's full name
    company - string - User's company
    notes - string - Any internal notes on the user
    office_integration_enabled - boolean - Enable integration with Office for the web?
    partner_admin - boolean - Is this user a Partner administrator?
    partner_id - int64 - Partner ID if this user belongs to a Partner
    password_validity_days - int64 - Number of days to allow user to use the same password
    primary_group_id - int64 - Primary group ID for Group Admin scoping
    readonly_site_admin - boolean - Is the user an allowed to view all (non-billing) site configuration for this site?
    receive_admin_alerts - boolean - Deprecated. Use notify_on_all_site_warnings and granular failure notification preferences instead.
    notify_on_all_site_warnings - boolean - Should the user receive site warnings via email?
    notify_on_all_sso_failures - boolean - Should the user receive sso/scim/ldap configuration/sync failures via email?
    notify_on_all_user_security_events - boolean - Should the user receive user security events via email?
    notify_on_all_pending_work_failures - boolean - Should the user receive pending work failures via email?
    notify_on_all_siem_http_destination_failures - boolean - Should the user receive siem failures via email?
    notify_on_all_sync_failures - boolean - Should the user receive sync failures via email?
    notify_on_all_automation_failures - boolean - Should the user receive automation failures via email?
    notify_on_all_expectation_failures - boolean - Should the user receive expectation failures and misses via email?
    require_login_by - string - Require user to login by specified date otherwise it will be disabled.
    require_password_change - boolean - Is a password change required upon next user login?
    responsible_group_id - int64 - ID of the internal Group responsible for this Partner User, overriding the Partner default.
    responsible_user_id - int64 - ID of the internal User responsible for this Partner User, overriding the Partner default.
    restapi_permission - boolean - Can this user access the Web app, Desktop app, SDKs, or REST API?  (All of these tools use the API internally, so this is one unified permission set.)
    s3_compatible_endpoint_permission - boolean - Can the user access the S3-compatible endpoint? Defaults to true.
    self_managed - boolean - Does this user manage it's own credentials or is it a shared/bot user?
    sftp_permission - boolean - Can the user access with SFTP?
    site_admin - boolean - Is the user an administrator for this site?
    skip_welcome_screen - boolean - Skip Welcome page in the UI?
    ssl_required - string - SSL required setting
    sso_strategy_id - int64 - SSO (Single Sign On) strategy ID for the user, if applicable.
    require_2fa - string - 2FA required setting. `use_system_setting` uses the site-wide setting, including SSO exemptions. `always_require` and `never_require` override the site-wide setting when user-level overrides are allowed.
    tags - string - Comma-separated list of Tags for this user. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
    time_zone - string - User time zone
    user_root - string - If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.
    user_home - string - Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.
    workspace_admin - boolean - Whether the user is an administrator of their own Custom Workspace. Does not reflect administration granted through Permissions.
    username (required) - string - User's username
    workspace_id - int64 - ID of the Workspace the user belongs to. 0 is the Default Workspace.
    """
    return _legacy_resource.create(params, options)


def unlock(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Unlock user who has been locked out due to failed logins"""
    _legacy_resource.unlock(id, params, options)


def resend_welcome_email(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Resend user welcome email"""
    _legacy_resource.resend_welcome_email(id, params, options)


def user_2fa_reset(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Trigger 2FA Reset process for user who has lost access to their existing 2FA methods"""
    _legacy_resource.user_2fa_reset(id, params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> User:
    """Parameters:
    avatar_file - file - An image file for your user avatar.
    avatar_delete - boolean - If true, the avatar will be deleted.
    change_password - string - Used for changing a password on an existing user.
    change_password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
    email - string - User's email.
    grant_permission - string - Permission to grant on the User Root upon creation, or on the Workspace root when the User Root is blank. For the Default Workspace, a blank User Root uses the site root. `admin` on a Custom Workspace's root grants Workspace Administrator access; on a subfolder it grants Folder Admin access. Can be blank or `admin`, `full`, `read`, `write`, `list`, `read+write`, `list+write`, or `history`.
    group_id - int64 - Group ID to associate this user with.
    group_ids - string - A list of group ids to associate this user with.  Comma delimited.
    imported_password_hash - string - Pre-calculated hash of the user's password. If supplied, this will be used to authenticate the user on first login. Supported hash methods are MD5, SHA1, and SHA256.
    password - string - User password.
    password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `password`.
    announcements_read - boolean - Signifies that the user has read all the announcements in the UI.
    ai_assistant_personality_id - int64 - AI Assistant Personality ID assigned directly to this user, if any.
    allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
    attachments_permission - boolean - DEPRECATED: If `true`, the user can user create Bundles (aka Share Links). Use the bundle permission instead.
    authenticate_until - string - Scheduled Date/Time at which user will be deactivated
    authentication_method - string - How is this user authenticated?
    billing_permission - boolean - Allow this user to perform operations on the account, payments, and invoices?
    bypass_user_lifecycle_rules - boolean - Exempt this user from user lifecycle rules?
    bypass_site_allowed_ips - boolean - Allow this user to skip site-wide IP blacklists?
    dav_permission - boolean - Can the user connect with WebDAV?
    desktop_configuration_profile_id - int64 - Desktop Configuration Profile ID assigned directly to this user, if any.
    default_workspace_id - int64 - Workspace ID the user should land in by default when more than one Workspace is available.
    disabled - boolean - Is user disabled? Disabled users cannot log in, and do not count for billing purposes. Users can be automatically disabled after an inactivity period via a Site setting or schedule to be deactivated after specific date.
    filesystem_layout - string - File system layout
    ftp_permission - boolean - Can the user access with FTP/FTPS?
    header_text - string - Text to display to the user in the header of the UI
    integration_centric_profile_id - int64 - Integration Centric Profile ID assigned directly to this user, if any.
    language - string - Preferred language
    notification_daily_send_time - int64 - Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
    name - string - User's full name
    company - string - User's company
    notes - string - Any internal notes on the user
    office_integration_enabled - boolean - Enable integration with Office for the web?
    partner_admin - boolean - Is this user a Partner administrator?
    partner_id - int64 - Partner ID if this user belongs to a Partner
    password_validity_days - int64 - Number of days to allow user to use the same password
    primary_group_id - int64 - Primary group ID for Group Admin scoping
    readonly_site_admin - boolean - Is the user an allowed to view all (non-billing) site configuration for this site?
    receive_admin_alerts - boolean - Deprecated. Use notify_on_all_site_warnings and granular failure notification preferences instead.
    notify_on_all_site_warnings - boolean - Should the user receive site warnings via email?
    notify_on_all_sso_failures - boolean - Should the user receive sso/scim/ldap configuration/sync failures via email?
    notify_on_all_user_security_events - boolean - Should the user receive user security events via email?
    notify_on_all_pending_work_failures - boolean - Should the user receive pending work failures via email?
    notify_on_all_siem_http_destination_failures - boolean - Should the user receive siem failures via email?
    notify_on_all_sync_failures - boolean - Should the user receive sync failures via email?
    notify_on_all_automation_failures - boolean - Should the user receive automation failures via email?
    notify_on_all_expectation_failures - boolean - Should the user receive expectation failures and misses via email?
    require_login_by - string - Require user to login by specified date otherwise it will be disabled.
    require_password_change - boolean - Is a password change required upon next user login?
    responsible_group_id - int64 - ID of the internal Group responsible for this Partner User, overriding the Partner default.
    responsible_user_id - int64 - ID of the internal User responsible for this Partner User, overriding the Partner default.
    restapi_permission - boolean - Can this user access the Web app, Desktop app, SDKs, or REST API?  (All of these tools use the API internally, so this is one unified permission set.)
    s3_compatible_endpoint_permission - boolean - Can the user access the S3-compatible endpoint? Defaults to true.
    self_managed - boolean - Does this user manage it's own credentials or is it a shared/bot user?
    sftp_permission - boolean - Can the user access with SFTP?
    site_admin - boolean - Is the user an administrator for this site?
    skip_welcome_screen - boolean - Skip Welcome page in the UI?
    ssl_required - string - SSL required setting
    sso_strategy_id - int64 - SSO (Single Sign On) strategy ID for the user, if applicable.
    require_2fa - string - 2FA required setting. `use_system_setting` uses the site-wide setting, including SSO exemptions. `always_require` and `never_require` override the site-wide setting when user-level overrides are allowed.
    tags - string - Comma-separated list of Tags for this user. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.
    time_zone - string - User time zone
    user_root - string - If filesystem layout is user_root, this path is the root path the user is fixed to for all interfaces. If the filesystem layout is site_root or partner_root, this acts as a root folder only for FTP and SFTP (SFTP applicability also requires a site-wide setting to be set). For partner_root layout, this path is relative to the Partner root folder for all callers and blank opts out of an additional protocol root. In this situation, this path is not applied to the API, Desktop, or Web interface.
    user_home - string - Home folder for FTP/SFTP. For users with the partner_root filesystem layout, this path is relative to the Partner root folder. In all other cases, it is an absolute path. Only applies to FTP and SFTP, and not any other interface.
    workspace_admin - boolean - Whether the user is an administrator of their own Custom Workspace. Does not reflect administration granted through Permissions.
    username - string - User's username
    workspace_id - int64 - Workspace ID. Only Site Administrators can change this field. Values supplied by Workspace Administrators, Group Administrators, or other non-Site Administrators using `/user` are ignored.
    clear_2fa - boolean - If true when changing authentication_method from `password` to `sso`, remove all two-factor methods. Ignored in all other cases.
    convert_to_partner_user - boolean - Required when assigning a Partner to an existing non-Partner user. If true, convert the user by assigning the partner_id provided.
    """
    return _legacy_resource.update(id, params, options)


def delete(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Parameters:
    new_owner_id - int64 - Provide a User ID here to transfer ownership of certain resources such as Automations and Share Links (Bundles) to that new user.
    """
    _legacy_resource.delete(id, params, options)


def destroy(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(id, params, options)


def new(*args, **kwargs) -> User:
    return User(*args, **kwargs)
