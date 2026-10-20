import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
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


class SsoStrategy:
    """A sso strategy record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        protocol: string - SSO Protocol
        provider: string - Provider name
        label: string - Custom label for the SSO provider on the login page.
        logo_url: string - URL holding a custom logo for the SSO provider on the login page.
        id: int64 - ID
        enabled: boolean - Is strategy enabled? This may become automatically set to `false` after a high number and duration of failures.
        user_count: int64 - Count of users with this SSO Strategy
        saml_provider_cert_fingerprint: string - Identity provider sha256 cert fingerprint if saml_provider_metadata_url is not available.
        saml_provider_issuer_url: string - Identity provider issuer url
        saml_provider_metadata_content: string - Custom identity provider metadata
        saml_provider_metadata_url: string - Metadata URL for the SAML identity provider
        saml_provider_slo_target_url: string - Identity provider SLO endpoint
        saml_provider_sso_target_url: string - Identity provider SSO endpoint if saml_provider_metadata_url is not available.
        scim_authentication_method: string - SCIM authentication type.
        scim_username: string - SCIM username.
        scim_oauth_access_token: string - SCIM OAuth Access Token. Only returned when the token is first issued or reset.
        scim_oauth_access_token_expires_at: string - SCIM OAuth Access Token Expiration Time.
        subdomain: string - Subdomain or domain name for your auth provider. Example: `https://[subdomain].okta.com/`
        provision_users: boolean - Auto-provision users?
        provision_groups: boolean - Auto-provision group membership based on group memberships on the SSO side?
        deprovision_users: boolean - Auto-deprovision users?
        deprovision_groups: boolean - Auto-deprovision group membership based on group memberships on the SSO side?
        deprovision_behavior: string - Method used for deprovisioning users.
        provision_group_default: string - Comma-separated list of group names for groups to automatically add all auto-provisioned users to.
        provision_group_exclusion: string - Comma-separated list of group names for groups (with optional wildcards) that will be excluded from auto-provisioning.
        provision_group_inclusion: string - Comma-separated list of group names for groups (with optional wildcards) that will be auto-provisioned.
        provision_group_required: string - Comma or newline separated list of group names (with optional wildcards) to require membership for user provisioning.
        provision_email_signup_groups: string - Comma-separated list of group names whose members will be created with email_signup authentication.
        provision_readonly_site_admin_groups: string - Comma-separated list of group names used to grant or remove Read-Only Site Admin access for users on this SSO provider. When this list is nonempty and a directory sync changes a user's group membership, membership in at least one listed group grants this access; membership in none removes it, including access granted manually. Directory syncs include SCIM requests from any provider on the site, LDAP syncs, and sign-ins that set the user's groups from the identity provider. Membership changes made any other way, including through the web app, API, SDKs, or CLI, do not affect administrator access.
        provision_site_admin_groups: string - Comma-separated list of group names used to grant or remove Site Admin access for users on this SSO provider. When this list is nonempty and a directory sync changes a user's group membership, membership in at least one listed group grants this access; membership in none removes it, including access granted manually. Directory syncs include SCIM requests from any provider on the site, LDAP syncs, and sign-ins that set the user's groups from the identity provider. Membership changes made any other way, including through the web app, API, SDKs, or CLI, do not affect administrator access.
        provision_group_admin_groups: string - Comma-separated list of group names whose members will be provisioned as Group Admins.
        provision_attachments_permission: boolean
        provision_dav_permission: boolean - Auto-provisioned users get WebDAV permission?
        provision_ftp_permission: boolean - Auto-provisioned users get FTP permission?
        provision_sftp_permission: boolean - Auto-provisioned users get SFTP permission?
        provision_time_zone: string - Default time zone for auto provisioned users.
        provision_company: string - Default company for auto provisioned users.
        provision_require_2fa: string - 2FA required setting for auto provisioned users. `use_system_setting` uses the site-wide setting, including SSO exemptions. `always_require` and `never_require` override the site-wide setting when user-level overrides are allowed.
        provision_filesystem_layout: string - File System layout to use for auto provisioned users.
        provider_identifier: string - URL-friendly, unique identifier for Azure SAML configuration
        ldap_base_dn: string - Base DN for looking up users in LDAP server
        ldap_domain: string - Domain name that will be appended to LDAP usernames
        display_on_login_page: boolean - Should this strategy be displayed on the login page?
        ldap_host: string - LDAP host
        ldap_host_2: string - LDAP backup host
        ldap_host_3: string - LDAP backup host
        ldap_port: int64 - LDAP port
        ldap_provisioning_enabled: boolean - Use LDAP server settings for scheduled provisioning while using this SSO provider for authentication?
        ldap_secure: boolean - Use secure LDAP?
        ldap_server_certificate: string - How to validate the LDAP server certificate. `require_match` validates the certificate chain and hostname; `allow_any` disables certificate validation.
        ldap_type: string - LDAP server type
        ldap_username: string - Username for signing in to LDAP server.
        ldap_username_field: string - LDAP username field
    """

    default_attributes = {
        "protocol": None,  # string - SSO Protocol
        "provider": None,  # string - Provider name
        "label": None,  # string - Custom label for the SSO provider on the login page.
        "logo_url": None,  # string - URL holding a custom logo for the SSO provider on the login page.
        "id": None,  # int64 - ID
        "enabled": None,  # boolean - Is strategy enabled?  This may become automatically set to `false` after a high number and duration of failures.
        "user_count": None,  # int64 - Count of users with this SSO Strategy
        "saml_provider_cert_fingerprint": None,  # string - Identity provider sha256 cert fingerprint if saml_provider_metadata_url is not available.
        "saml_provider_issuer_url": None,  # string - Identity provider issuer url
        "saml_provider_metadata_content": None,  # string - Custom identity provider metadata
        "saml_provider_metadata_url": None,  # string - Metadata URL for the SAML identity provider
        "saml_provider_slo_target_url": None,  # string - Identity provider SLO endpoint
        "saml_provider_sso_target_url": None,  # string - Identity provider SSO endpoint if saml_provider_metadata_url is not available.
        "scim_authentication_method": None,  # string - SCIM authentication type.
        "scim_username": None,  # string - SCIM username.
        "scim_oauth_access_token": None,  # string - SCIM OAuth Access Token. Only returned when the token is first issued or reset.
        "scim_oauth_access_token_expires_at": None,  # string - SCIM OAuth Access Token Expiration Time.
        "subdomain": None,  # string - Subdomain or domain name for your auth provider.   Example: `https://[subdomain].okta.com/`
        "provision_users": None,  # boolean - Auto-provision users?
        "provision_groups": None,  # boolean - Auto-provision group membership based on group memberships on the SSO side?
        "deprovision_users": None,  # boolean - Auto-deprovision users?
        "deprovision_groups": None,  # boolean - Auto-deprovision group membership based on group memberships on the SSO side?
        "deprovision_behavior": None,  # string - Method used for deprovisioning users.
        "provision_group_default": None,  # string - Comma-separated list of group names for groups to automatically add all auto-provisioned users to.
        "provision_group_exclusion": None,  # string - Comma-separated list of group names for groups (with optional wildcards) that will be excluded from auto-provisioning.
        "provision_group_inclusion": None,  # string - Comma-separated list of group names for groups (with optional wildcards) that will be auto-provisioned.
        "provision_group_required": None,  # string - Comma or newline separated list of group names (with optional wildcards) to require membership for user provisioning.
        "provision_email_signup_groups": None,  # string - Comma-separated list of group names whose members will be created with email_signup authentication.
        "provision_readonly_site_admin_groups": None,  # string - Comma-separated list of group names used to grant or remove Read-Only Site Admin access for users on this SSO provider. When this list is nonempty and a directory sync changes a user's group membership, membership in at least one listed group grants this access; membership in none removes it, including access granted manually. Directory syncs include SCIM requests from any provider on the site, LDAP syncs, and sign-ins that set the user's groups from the identity provider. Membership changes made any other way, including through the web app, API, SDKs, or CLI, do not affect administrator access.
        "provision_site_admin_groups": None,  # string - Comma-separated list of group names used to grant or remove Site Admin access for users on this SSO provider. When this list is nonempty and a directory sync changes a user's group membership, membership in at least one listed group grants this access; membership in none removes it, including access granted manually. Directory syncs include SCIM requests from any provider on the site, LDAP syncs, and sign-ins that set the user's groups from the identity provider. Membership changes made any other way, including through the web app, API, SDKs, or CLI, do not affect administrator access.
        "provision_group_admin_groups": None,  # string - Comma-separated list of group names whose members will be provisioned as Group Admins.
        "provision_attachments_permission": None,  # boolean
        "provision_dav_permission": None,  # boolean - Auto-provisioned users get WebDAV permission?
        "provision_ftp_permission": None,  # boolean - Auto-provisioned users get FTP permission?
        "provision_sftp_permission": None,  # boolean - Auto-provisioned users get SFTP permission?
        "provision_time_zone": None,  # string - Default time zone for auto provisioned users.
        "provision_company": None,  # string - Default company for auto provisioned users.
        "provision_require_2fa": None,  # string - 2FA required setting for auto provisioned users. `use_system_setting` uses the site-wide setting, including SSO exemptions. `always_require` and `never_require` override the site-wide setting when user-level overrides are allowed.
        "provision_filesystem_layout": None,  # string - File System layout to use for auto provisioned users.
        "provider_identifier": None,  # string - URL-friendly, unique identifier for Azure SAML configuration
        "ldap_base_dn": None,  # string - Base DN for looking up users in LDAP server
        "ldap_domain": None,  # string - Domain name that will be appended to LDAP usernames
        "display_on_login_page": None,  # boolean - Should this strategy be displayed on the login page?
        "ldap_host": None,  # string - LDAP host
        "ldap_host_2": None,  # string - LDAP backup host
        "ldap_host_3": None,  # string - LDAP backup host
        "ldap_port": None,  # int64 - LDAP port
        "ldap_provisioning_enabled": None,  # boolean - Use LDAP server settings for scheduled provisioning while using this SSO provider for authentication?
        "ldap_secure": None,  # boolean - Use secure LDAP?
        "ldap_server_certificate": None,  # string - How to validate the LDAP server certificate. `require_match` validates the certificate chain and hostname; `allow_any` disables certificate validation.
        "ldap_type": None,  # string - LDAP server type
        "ldap_username": None,  # string - Username for signing in to LDAP server.
        "ldap_username_field": None,  # string - LDAP username field
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    protocol: str | None
    provider: str | None
    label: str | None
    logo_url: str | None
    id: int | None
    enabled: bool | None
    user_count: int | None
    saml_provider_cert_fingerprint: str | None
    saml_provider_issuer_url: str | None
    saml_provider_metadata_content: str | None
    saml_provider_metadata_url: str | None
    saml_provider_slo_target_url: str | None
    saml_provider_sso_target_url: str | None
    scim_authentication_method: str | None
    scim_username: str | None
    scim_oauth_access_token: str | None
    scim_oauth_access_token_expires_at: str | None
    subdomain: str | None
    provision_users: bool | None
    provision_groups: bool | None
    deprovision_users: bool | None
    deprovision_groups: bool | None
    deprovision_behavior: str | None
    provision_group_default: str | None
    provision_group_exclusion: str | None
    provision_group_inclusion: str | None
    provision_group_required: str | None
    provision_email_signup_groups: str | None
    provision_readonly_site_admin_groups: str | None
    provision_site_admin_groups: str | None
    provision_group_admin_groups: str | None
    provision_attachments_permission: bool | None
    provision_dav_permission: bool | None
    provision_ftp_permission: bool | None
    provision_sftp_permission: bool | None
    provision_time_zone: str | None
    provision_company: str | None
    provision_require_2fa: str | None
    provision_filesystem_layout: str | None
    provider_identifier: str | None
    ldap_base_dn: str | None
    ldap_domain: str | None
    display_on_login_page: bool | None
    ldap_host: str | None
    ldap_host_2: str | None
    ldap_host_3: str | None
    ldap_port: int | None
    ldap_provisioning_enabled: bool | None
    ldap_secure: bool | None
    ldap_server_certificate: str | None
    ldap_type: str | None
    ldap_username: str | None
    ldap_username_field: str | None

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
        for attribute, default_value in SsoStrategy.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SsoStrategy.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def sync(self, params: dict[str, Any] | None = None) -> None:
        """Synchronize provisioning data with the SSO remote server"""
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
            "/sso_strategies/" + path_value(params["id"]) + "/sync",
            params,
        )


class SsoStrategyResource:
    """SsoStrategy operations that use one client's configuration.

    Get one from a client, such as ``client.sso_strategy``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SsoStrategy]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
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
        operation = Operation.start(self._scope, options)
        return ListObj(
            SsoStrategy, "GET", "/sso_strategies", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[SsoStrategy]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SsoStrategy:
        """Parameters:
        id (required) - int64 - Sso Strategy ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> SsoStrategy:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/sso_strategies/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, SsoStrategy)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SsoStrategy:
        """The same as find()."""
        return self.find(id, params, options)

    def sync(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Synchronize provisioning data with the SSO remote server"""
        return self.__sync({"id": id}, params, options)

    def __sync(
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
            "/sso_strategies/" + path_value(params["id"]) + "/sync",
            params,
        )

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> SsoStrategy:
        """A new SsoStrategy with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = SsoStrategy(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = SsoStrategyResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SsoStrategy]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[SsoStrategy]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SsoStrategy:
    """Parameters:
    id (required) - int64 - Sso Strategy ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> SsoStrategy:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def sync(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Synchronize provisioning data with the SSO remote server"""
    _legacy_resource.sync(id, params, options)


def new(*args, **kwargs) -> SsoStrategy:
    return SsoStrategy(*args, **kwargs)
