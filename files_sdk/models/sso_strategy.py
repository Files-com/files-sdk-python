import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class SsoStrategy:
    default_attributes = {
        "protocol": None,  # string - SSO Protocol
        "provider": None,  # string - Provider name
        "label": None,  # string - Custom label for the SSO provider on the login page.
        "logo_url": None,  # string - URL holding a custom logo for the SSO provider on the login page.
        "id": None,  # int64 - ID
        "user_count": None,  # int64 - Count of users with this SSO Strategy
        "saml_provider_cert_fingerprint": None,  # string - Identity provider sha256 cert fingerprint if saml_provider_metadata_url is not available.
        "saml_provider_issuer_url": None,  # string - Identity provider issuer url
        "saml_provider_metadata_content": None,  # string - Custom identity provider metadata
        "saml_provider_metadata_url": None,  # string - Metadata URL for the SAML identity provider
        "saml_provider_slo_target_url": None,  # string - Identity provider SLO endpoint
        "saml_provider_sso_target_url": None,  # string - Identity provider SSO endpoint if saml_provider_metadata_url is not available.
        "scim_authentication_method": None,  # string - SCIM authentication type.
        "scim_username": None,  # string - SCIM username.
        "scim_oauth_access_token": None,  # string - SCIM OAuth Access Token.
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
        "provision_readonly_site_admin_groups": None,  # string - Comma-separated list of group names whose members will be created as Read-Only Site Admins.
        "provision_site_admin_groups": None,  # string - Comma-separated list of group names whose members will be created as Site Admins.
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
        "enabled": None,  # boolean - Is strategy enabled?  This may become automatically set to `false` after a high number and duration of failures.
        "display_on_login_page": None,  # boolean - Should this strategy be displayed on the login page?
        "ldap_host": None,  # string - LDAP host
        "ldap_host_2": None,  # string - LDAP backup host
        "ldap_host_3": None,  # string - LDAP backup host
        "ldap_port": None,  # int64 - LDAP port
        "ldap_provisioning_enabled": None,  # boolean - Use LDAP server settings for scheduled provisioning while using this SSO provider for authentication?
        "ldap_secure": None,  # boolean - Use secure LDAP?
        "ldap_type": None,  # string - LDAP server type
        "ldap_username": None,  # string - Username for signing in to LDAP server.
        "ldap_username_field": None,  # string - LDAP username field
        "client_id": None,  # string - OAuth Client ID for your auth provider.
        "client_secret": None,  # string - OAuth Client Secret for your auth provider.
        "ldap_password": None,  # string - Password for signing in to LDAP server.
        "logo_delete": None,  # boolean - If true, the logo will be deleted.
        "logo_file": None,  # file - A logo to display on the login page.
        "reset_scim_oauth_access_token": None,  # boolean - If true, perform a reset on SCIM OAuth access token
        "scim_password": None,  # string - SCIM password applicable to basic authentication.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

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

    # Synchronize provisioning data with the SSO remote server
    def sync(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        Api.send_request(
            "POST",
            "/sso_strategies/{id}/sync".format(
                id=quote(str(params["id"]), safe="")
            ),
            params,
            self.options,
        )

    # Parameters:
    #   client_id - string - OAuth Client ID for your auth provider.
    #   client_secret - string - OAuth Client Secret for your auth provider.
    #   ldap_password - string - Password for signing in to LDAP server.
    #   logo_delete - boolean - If true, the logo will be deleted.
    #   logo_file - file - A logo to display on the login page.
    #   reset_scim_oauth_access_token - boolean - If true, perform a reset on SCIM OAuth access token
    #   scim_password - string - SCIM password applicable to basic authentication.
    #   deprovision_behavior - string - Method used for deprovisioning users.
    #   deprovision_groups - boolean - Auto-deprovision group membership based on group memberships on the SSO side?
    #   deprovision_users - boolean - Auto-deprovision users?
    #   display_on_login_page - boolean - Should this strategy be displayed on the login page?
    #   enabled - boolean - Is strategy enabled?  This may become automatically set to `false` after a high number and duration of failures.
    #   label - string - Custom label for the SSO provider on the login page.
    #   ldap_base_dn - string - Base DN for looking up users in LDAP server
    #   ldap_domain - string - Domain name that will be appended to LDAP usernames
    #   ldap_host - string - LDAP host
    #   ldap_host_2 - string - LDAP backup host
    #   ldap_host_3 - string - LDAP backup host
    #   ldap_port - int64 - LDAP port
    #   ldap_provisioning_enabled - boolean - Use LDAP server settings for scheduled provisioning while using this SSO provider for authentication?
    #   ldap_secure - boolean - Use secure LDAP?
    #   ldap_type - string - LDAP server type
    #   ldap_username - string - Username for signing in to LDAP server.
    #   ldap_username_field - string - LDAP username field
    #   protocol - string - SSO Protocol
    #   provider - string - Provider name
    #   provider_identifier - string - URL-friendly, unique identifier for Azure SAML configuration
    #   provision_company - string - Default company for auto provisioned users.
    #   provision_dav_permission - boolean - Auto-provisioned users get WebDAV permission?
    #   provision_email_signup_groups - string - Comma-separated list of group names whose members will be created with email_signup authentication.
    #   provision_filesystem_layout - string - File System layout to use for auto provisioned users.
    #   provision_ftp_permission - boolean - Auto-provisioned users get FTP permission?
    #   provision_group_admin_groups - string - Comma-separated list of group names whose members will be provisioned as Group Admins.
    #   provision_group_default - string - Comma-separated list of group names for groups to automatically add all auto-provisioned users to.
    #   provision_group_exclusion - string - Comma-separated list of group names for groups (with optional wildcards) that will be excluded from auto-provisioning.
    #   provision_group_inclusion - string - Comma-separated list of group names for groups (with optional wildcards) that will be auto-provisioned.
    #   provision_group_required - string - Comma or newline separated list of group names (with optional wildcards) to require membership for user provisioning.
    #   provision_groups - boolean - Auto-provision group membership based on group memberships on the SSO side?
    #   provision_readonly_site_admin_groups - string - Comma-separated list of group names whose members will be created as Read-Only Site Admins.
    #   provision_require_2fa - string - 2FA required setting for auto provisioned users. `use_system_setting` uses the site-wide setting, including SSO exemptions. `always_require` and `never_require` override the site-wide setting when user-level overrides are allowed.
    #   provision_sftp_permission - boolean - Auto-provisioned users get SFTP permission?
    #   provision_site_admin_groups - string - Comma-separated list of group names whose members will be created as Site Admins.
    #   provision_time_zone - string - Default time zone for auto provisioned users.
    #   provision_users - boolean - Auto-provision users?
    #   saml_provider_cert_fingerprint - string - Identity provider sha256 cert fingerprint if saml_provider_metadata_url is not available.
    #   saml_provider_issuer_url - string - Identity provider issuer url
    #   saml_provider_metadata_content - string - Custom identity provider metadata
    #   saml_provider_metadata_url - string - Metadata URL for the SAML identity provider
    #   saml_provider_slo_target_url - string - Identity provider SLO endpoint
    #   saml_provider_sso_target_url - string - Identity provider SSO endpoint if saml_provider_metadata_url is not available.
    #   scim_authentication_method - string - SCIM authentication type.
    #   scim_oauth_access_token_expires_at - string - SCIM OAuth Access Token Expiration Time.
    #   scim_username - string - SCIM username.
    #   subdomain - string - Subdomain or domain name for your auth provider.   Example: `https://[subdomain].okta.com/`
    def update(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "client_id" in params and not isinstance(params["client_id"], str):
            raise InvalidParameterError(
                "Bad parameter: client_id must be an str"
            )
        if "client_secret" in params and not isinstance(
            params["client_secret"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: client_secret must be an str"
            )
        if "ldap_password" in params and not isinstance(
            params["ldap_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: ldap_password must be an str"
            )
        if "scim_password" in params and not isinstance(
            params["scim_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: scim_password must be an str"
            )
        if "deprovision_behavior" in params and not isinstance(
            params["deprovision_behavior"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: deprovision_behavior must be an str"
            )
        if "label" in params and not isinstance(params["label"], str):
            raise InvalidParameterError("Bad parameter: label must be an str")
        if "ldap_base_dn" in params and not isinstance(
            params["ldap_base_dn"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: ldap_base_dn must be an str"
            )
        if "ldap_domain" in params and not isinstance(
            params["ldap_domain"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: ldap_domain must be an str"
            )
        if "ldap_host" in params and not isinstance(params["ldap_host"], str):
            raise InvalidParameterError(
                "Bad parameter: ldap_host must be an str"
            )
        if "ldap_host_2" in params and not isinstance(
            params["ldap_host_2"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: ldap_host_2 must be an str"
            )
        if "ldap_host_3" in params and not isinstance(
            params["ldap_host_3"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: ldap_host_3 must be an str"
            )
        if "ldap_port" in params and not isinstance(params["ldap_port"], int):
            raise InvalidParameterError(
                "Bad parameter: ldap_port must be an int"
            )
        if "ldap_type" in params and not isinstance(params["ldap_type"], str):
            raise InvalidParameterError(
                "Bad parameter: ldap_type must be an str"
            )
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
        if "protocol" in params and not isinstance(params["protocol"], str):
            raise InvalidParameterError(
                "Bad parameter: protocol must be an str"
            )
        if "provider" in params and not isinstance(params["provider"], str):
            raise InvalidParameterError(
                "Bad parameter: provider must be an str"
            )
        if "provider_identifier" in params and not isinstance(
            params["provider_identifier"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provider_identifier must be an str"
            )
        if "provision_company" in params and not isinstance(
            params["provision_company"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provision_company must be an str"
            )
        if "provision_email_signup_groups" in params and not isinstance(
            params["provision_email_signup_groups"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provision_email_signup_groups must be an str"
            )
        if "provision_filesystem_layout" in params and not isinstance(
            params["provision_filesystem_layout"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provision_filesystem_layout must be an str"
            )
        if "provision_group_admin_groups" in params and not isinstance(
            params["provision_group_admin_groups"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provision_group_admin_groups must be an str"
            )
        if "provision_group_default" in params and not isinstance(
            params["provision_group_default"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provision_group_default must be an str"
            )
        if "provision_group_exclusion" in params and not isinstance(
            params["provision_group_exclusion"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provision_group_exclusion must be an str"
            )
        if "provision_group_inclusion" in params and not isinstance(
            params["provision_group_inclusion"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provision_group_inclusion must be an str"
            )
        if "provision_group_required" in params and not isinstance(
            params["provision_group_required"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provision_group_required must be an str"
            )
        if (
            "provision_readonly_site_admin_groups" in params
            and not isinstance(
                params["provision_readonly_site_admin_groups"], str
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: provision_readonly_site_admin_groups must be an str"
            )
        if "provision_require_2fa" in params and not isinstance(
            params["provision_require_2fa"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provision_require_2fa must be an str"
            )
        if "provision_site_admin_groups" in params and not isinstance(
            params["provision_site_admin_groups"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provision_site_admin_groups must be an str"
            )
        if "provision_time_zone" in params and not isinstance(
            params["provision_time_zone"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: provision_time_zone must be an str"
            )
        if "saml_provider_cert_fingerprint" in params and not isinstance(
            params["saml_provider_cert_fingerprint"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: saml_provider_cert_fingerprint must be an str"
            )
        if "saml_provider_issuer_url" in params and not isinstance(
            params["saml_provider_issuer_url"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: saml_provider_issuer_url must be an str"
            )
        if "saml_provider_metadata_content" in params and not isinstance(
            params["saml_provider_metadata_content"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: saml_provider_metadata_content must be an str"
            )
        if "saml_provider_metadata_url" in params and not isinstance(
            params["saml_provider_metadata_url"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: saml_provider_metadata_url must be an str"
            )
        if "saml_provider_slo_target_url" in params and not isinstance(
            params["saml_provider_slo_target_url"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: saml_provider_slo_target_url must be an str"
            )
        if "saml_provider_sso_target_url" in params and not isinstance(
            params["saml_provider_sso_target_url"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: saml_provider_sso_target_url must be an str"
            )
        if "scim_authentication_method" in params and not isinstance(
            params["scim_authentication_method"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: scim_authentication_method must be an str"
            )
        if "scim_oauth_access_token_expires_at" in params and not isinstance(
            params["scim_oauth_access_token_expires_at"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: scim_oauth_access_token_expires_at must be an str"
            )
        if "scim_username" in params and not isinstance(
            params["scim_username"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: scim_username must be an str"
            )
        if "subdomain" in params and not isinstance(params["subdomain"], str):
            raise InvalidParameterError(
                "Bad parameter: subdomain must be an str"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/sso_strategies/{id}".format(
                id=quote(str(params["id"]), safe="")
            ),
            params,
            self.options,
        )
        return response.data

    def delete(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        Api.send_request(
            "DELETE",
            "/sso_strategies/{id}".format(
                id=quote(str(params["id"]), safe="")
            ),
            params,
            self.options,
        )

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            new_obj = self.update(self.get_attributes())
            self.set_attributes(new_obj.get_attributes())
            return True
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    return ListObj(SsoStrategy, "GET", "/sso_strategies", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Sso Strategy ID.
def find(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "GET",
        "/sso_strategies/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return SsoStrategy(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   client_id - string - OAuth Client ID for your auth provider.
#   client_secret - string - OAuth Client Secret for your auth provider.
#   ldap_password - string - Password for signing in to LDAP server.
#   logo_delete - boolean - If true, the logo will be deleted.
#   logo_file - file - A logo to display on the login page.
#   reset_scim_oauth_access_token - boolean - If true, perform a reset on SCIM OAuth access token
#   scim_password - string - SCIM password applicable to basic authentication.
#   deprovision_behavior - string - Method used for deprovisioning users.
#   deprovision_groups - boolean - Auto-deprovision group membership based on group memberships on the SSO side?
#   deprovision_users - boolean - Auto-deprovision users?
#   display_on_login_page - boolean - Should this strategy be displayed on the login page?
#   enabled - boolean - Is strategy enabled?  This may become automatically set to `false` after a high number and duration of failures.
#   label - string - Custom label for the SSO provider on the login page.
#   ldap_base_dn - string - Base DN for looking up users in LDAP server
#   ldap_domain - string - Domain name that will be appended to LDAP usernames
#   ldap_host - string - LDAP host
#   ldap_host_2 - string - LDAP backup host
#   ldap_host_3 - string - LDAP backup host
#   ldap_port - int64 - LDAP port
#   ldap_provisioning_enabled - boolean - Use LDAP server settings for scheduled provisioning while using this SSO provider for authentication?
#   ldap_secure - boolean - Use secure LDAP?
#   ldap_type - string - LDAP server type
#   ldap_username - string - Username for signing in to LDAP server.
#   ldap_username_field - string - LDAP username field
#   protocol - string - SSO Protocol
#   provider - string - Provider name
#   provider_identifier - string - URL-friendly, unique identifier for Azure SAML configuration
#   provision_company - string - Default company for auto provisioned users.
#   provision_dav_permission - boolean - Auto-provisioned users get WebDAV permission?
#   provision_email_signup_groups - string - Comma-separated list of group names whose members will be created with email_signup authentication.
#   provision_filesystem_layout - string - File System layout to use for auto provisioned users.
#   provision_ftp_permission - boolean - Auto-provisioned users get FTP permission?
#   provision_group_admin_groups - string - Comma-separated list of group names whose members will be provisioned as Group Admins.
#   provision_group_default - string - Comma-separated list of group names for groups to automatically add all auto-provisioned users to.
#   provision_group_exclusion - string - Comma-separated list of group names for groups (with optional wildcards) that will be excluded from auto-provisioning.
#   provision_group_inclusion - string - Comma-separated list of group names for groups (with optional wildcards) that will be auto-provisioned.
#   provision_group_required - string - Comma or newline separated list of group names (with optional wildcards) to require membership for user provisioning.
#   provision_groups - boolean - Auto-provision group membership based on group memberships on the SSO side?
#   provision_readonly_site_admin_groups - string - Comma-separated list of group names whose members will be created as Read-Only Site Admins.
#   provision_require_2fa - string - 2FA required setting for auto provisioned users. `use_system_setting` uses the site-wide setting, including SSO exemptions. `always_require` and `never_require` override the site-wide setting when user-level overrides are allowed.
#   provision_sftp_permission - boolean - Auto-provisioned users get SFTP permission?
#   provision_site_admin_groups - string - Comma-separated list of group names whose members will be created as Site Admins.
#   provision_time_zone - string - Default time zone for auto provisioned users.
#   provision_users - boolean - Auto-provision users?
#   saml_provider_cert_fingerprint - string - Identity provider sha256 cert fingerprint if saml_provider_metadata_url is not available.
#   saml_provider_issuer_url - string - Identity provider issuer url
#   saml_provider_metadata_content - string - Custom identity provider metadata
#   saml_provider_metadata_url - string - Metadata URL for the SAML identity provider
#   saml_provider_slo_target_url - string - Identity provider SLO endpoint
#   saml_provider_sso_target_url - string - Identity provider SSO endpoint if saml_provider_metadata_url is not available.
#   scim_authentication_method - string - SCIM authentication type.
#   scim_oauth_access_token_expires_at - string - SCIM OAuth Access Token Expiration Time.
#   scim_username - string - SCIM username.
#   subdomain - string - Subdomain or domain name for your auth provider.   Example: `https://[subdomain].okta.com/`
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "client_id" in params and not isinstance(params["client_id"], str):
        raise InvalidParameterError("Bad parameter: client_id must be an str")
    if "client_secret" in params and not isinstance(
        params["client_secret"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: client_secret must be an str"
        )
    if "ldap_password" in params and not isinstance(
        params["ldap_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_password must be an str"
        )
    if "logo_delete" in params and not isinstance(params["logo_delete"], bool):
        raise InvalidParameterError(
            "Bad parameter: logo_delete must be an bool"
        )
    if "reset_scim_oauth_access_token" in params and not isinstance(
        params["reset_scim_oauth_access_token"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: reset_scim_oauth_access_token must be an bool"
        )
    if "scim_password" in params and not isinstance(
        params["scim_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: scim_password must be an str"
        )
    if "deprovision_behavior" in params and not isinstance(
        params["deprovision_behavior"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: deprovision_behavior must be an str"
        )
    if "deprovision_groups" in params and not isinstance(
        params["deprovision_groups"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: deprovision_groups must be an bool"
        )
    if "deprovision_users" in params and not isinstance(
        params["deprovision_users"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: deprovision_users must be an bool"
        )
    if "display_on_login_page" in params and not isinstance(
        params["display_on_login_page"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: display_on_login_page must be an bool"
        )
    if "enabled" in params and not isinstance(params["enabled"], bool):
        raise InvalidParameterError("Bad parameter: enabled must be an bool")
    if "label" in params and not isinstance(params["label"], str):
        raise InvalidParameterError("Bad parameter: label must be an str")
    if "ldap_base_dn" in params and not isinstance(
        params["ldap_base_dn"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_base_dn must be an str"
        )
    if "ldap_domain" in params and not isinstance(params["ldap_domain"], str):
        raise InvalidParameterError(
            "Bad parameter: ldap_domain must be an str"
        )
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
    if "ldap_provisioning_enabled" in params and not isinstance(
        params["ldap_provisioning_enabled"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_provisioning_enabled must be an bool"
        )
    if "ldap_secure" in params and not isinstance(params["ldap_secure"], bool):
        raise InvalidParameterError(
            "Bad parameter: ldap_secure must be an bool"
        )
    if "ldap_type" in params and not isinstance(params["ldap_type"], str):
        raise InvalidParameterError("Bad parameter: ldap_type must be an str")
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
    if "protocol" in params and not isinstance(params["protocol"], str):
        raise InvalidParameterError("Bad parameter: protocol must be an str")
    if "provider" in params and not isinstance(params["provider"], str):
        raise InvalidParameterError("Bad parameter: provider must be an str")
    if "provider_identifier" in params and not isinstance(
        params["provider_identifier"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provider_identifier must be an str"
        )
    if "provision_company" in params and not isinstance(
        params["provision_company"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_company must be an str"
        )
    if "provision_dav_permission" in params and not isinstance(
        params["provision_dav_permission"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_dav_permission must be an bool"
        )
    if "provision_email_signup_groups" in params and not isinstance(
        params["provision_email_signup_groups"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_email_signup_groups must be an str"
        )
    if "provision_filesystem_layout" in params and not isinstance(
        params["provision_filesystem_layout"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_filesystem_layout must be an str"
        )
    if "provision_ftp_permission" in params and not isinstance(
        params["provision_ftp_permission"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_ftp_permission must be an bool"
        )
    if "provision_group_admin_groups" in params and not isinstance(
        params["provision_group_admin_groups"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_group_admin_groups must be an str"
        )
    if "provision_group_default" in params and not isinstance(
        params["provision_group_default"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_group_default must be an str"
        )
    if "provision_group_exclusion" in params and not isinstance(
        params["provision_group_exclusion"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_group_exclusion must be an str"
        )
    if "provision_group_inclusion" in params and not isinstance(
        params["provision_group_inclusion"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_group_inclusion must be an str"
        )
    if "provision_group_required" in params and not isinstance(
        params["provision_group_required"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_group_required must be an str"
        )
    if "provision_groups" in params and not isinstance(
        params["provision_groups"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_groups must be an bool"
        )
    if "provision_readonly_site_admin_groups" in params and not isinstance(
        params["provision_readonly_site_admin_groups"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_readonly_site_admin_groups must be an str"
        )
    if "provision_require_2fa" in params and not isinstance(
        params["provision_require_2fa"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_require_2fa must be an str"
        )
    if "provision_sftp_permission" in params and not isinstance(
        params["provision_sftp_permission"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_sftp_permission must be an bool"
        )
    if "provision_site_admin_groups" in params and not isinstance(
        params["provision_site_admin_groups"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_site_admin_groups must be an str"
        )
    if "provision_time_zone" in params and not isinstance(
        params["provision_time_zone"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_time_zone must be an str"
        )
    if "provision_users" in params and not isinstance(
        params["provision_users"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_users must be an bool"
        )
    if "saml_provider_cert_fingerprint" in params and not isinstance(
        params["saml_provider_cert_fingerprint"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: saml_provider_cert_fingerprint must be an str"
        )
    if "saml_provider_issuer_url" in params and not isinstance(
        params["saml_provider_issuer_url"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: saml_provider_issuer_url must be an str"
        )
    if "saml_provider_metadata_content" in params and not isinstance(
        params["saml_provider_metadata_content"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: saml_provider_metadata_content must be an str"
        )
    if "saml_provider_metadata_url" in params and not isinstance(
        params["saml_provider_metadata_url"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: saml_provider_metadata_url must be an str"
        )
    if "saml_provider_slo_target_url" in params and not isinstance(
        params["saml_provider_slo_target_url"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: saml_provider_slo_target_url must be an str"
        )
    if "saml_provider_sso_target_url" in params and not isinstance(
        params["saml_provider_sso_target_url"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: saml_provider_sso_target_url must be an str"
        )
    if "scim_authentication_method" in params and not isinstance(
        params["scim_authentication_method"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: scim_authentication_method must be an str"
        )
    if "scim_oauth_access_token_expires_at" in params and not isinstance(
        params["scim_oauth_access_token_expires_at"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: scim_oauth_access_token_expires_at must be an str"
        )
    if "scim_username" in params and not isinstance(
        params["scim_username"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: scim_username must be an str"
        )
    if "subdomain" in params and not isinstance(params["subdomain"], str):
        raise InvalidParameterError("Bad parameter: subdomain must be an str")
    response, options = Api.send_request(
        "POST", "/sso_strategies", params, options
    )
    return SsoStrategy(response.data, options)


# Synchronize provisioning data with the SSO remote server
def sync(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    Api.send_request(
        "POST",
        "/sso_strategies/{id}/sync".format(
            id=quote(str(params["id"]), safe="")
        ),
        params,
        options,
    )


# Parameters:
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    response, options = Api.send_request(
        "POST", "/sso_strategies/create_export", params, options
    )
    return Export(response.data, options)


# Parameters:
#   client_id - string - OAuth Client ID for your auth provider.
#   client_secret - string - OAuth Client Secret for your auth provider.
#   ldap_password - string - Password for signing in to LDAP server.
#   logo_delete - boolean - If true, the logo will be deleted.
#   logo_file - file - A logo to display on the login page.
#   reset_scim_oauth_access_token - boolean - If true, perform a reset on SCIM OAuth access token
#   scim_password - string - SCIM password applicable to basic authentication.
#   deprovision_behavior - string - Method used for deprovisioning users.
#   deprovision_groups - boolean - Auto-deprovision group membership based on group memberships on the SSO side?
#   deprovision_users - boolean - Auto-deprovision users?
#   display_on_login_page - boolean - Should this strategy be displayed on the login page?
#   enabled - boolean - Is strategy enabled?  This may become automatically set to `false` after a high number and duration of failures.
#   label - string - Custom label for the SSO provider on the login page.
#   ldap_base_dn - string - Base DN for looking up users in LDAP server
#   ldap_domain - string - Domain name that will be appended to LDAP usernames
#   ldap_host - string - LDAP host
#   ldap_host_2 - string - LDAP backup host
#   ldap_host_3 - string - LDAP backup host
#   ldap_port - int64 - LDAP port
#   ldap_provisioning_enabled - boolean - Use LDAP server settings for scheduled provisioning while using this SSO provider for authentication?
#   ldap_secure - boolean - Use secure LDAP?
#   ldap_type - string - LDAP server type
#   ldap_username - string - Username for signing in to LDAP server.
#   ldap_username_field - string - LDAP username field
#   protocol - string - SSO Protocol
#   provider - string - Provider name
#   provider_identifier - string - URL-friendly, unique identifier for Azure SAML configuration
#   provision_company - string - Default company for auto provisioned users.
#   provision_dav_permission - boolean - Auto-provisioned users get WebDAV permission?
#   provision_email_signup_groups - string - Comma-separated list of group names whose members will be created with email_signup authentication.
#   provision_filesystem_layout - string - File System layout to use for auto provisioned users.
#   provision_ftp_permission - boolean - Auto-provisioned users get FTP permission?
#   provision_group_admin_groups - string - Comma-separated list of group names whose members will be provisioned as Group Admins.
#   provision_group_default - string - Comma-separated list of group names for groups to automatically add all auto-provisioned users to.
#   provision_group_exclusion - string - Comma-separated list of group names for groups (with optional wildcards) that will be excluded from auto-provisioning.
#   provision_group_inclusion - string - Comma-separated list of group names for groups (with optional wildcards) that will be auto-provisioned.
#   provision_group_required - string - Comma or newline separated list of group names (with optional wildcards) to require membership for user provisioning.
#   provision_groups - boolean - Auto-provision group membership based on group memberships on the SSO side?
#   provision_readonly_site_admin_groups - string - Comma-separated list of group names whose members will be created as Read-Only Site Admins.
#   provision_require_2fa - string - 2FA required setting for auto provisioned users. `use_system_setting` uses the site-wide setting, including SSO exemptions. `always_require` and `never_require` override the site-wide setting when user-level overrides are allowed.
#   provision_sftp_permission - boolean - Auto-provisioned users get SFTP permission?
#   provision_site_admin_groups - string - Comma-separated list of group names whose members will be created as Site Admins.
#   provision_time_zone - string - Default time zone for auto provisioned users.
#   provision_users - boolean - Auto-provision users?
#   saml_provider_cert_fingerprint - string - Identity provider sha256 cert fingerprint if saml_provider_metadata_url is not available.
#   saml_provider_issuer_url - string - Identity provider issuer url
#   saml_provider_metadata_content - string - Custom identity provider metadata
#   saml_provider_metadata_url - string - Metadata URL for the SAML identity provider
#   saml_provider_slo_target_url - string - Identity provider SLO endpoint
#   saml_provider_sso_target_url - string - Identity provider SSO endpoint if saml_provider_metadata_url is not available.
#   scim_authentication_method - string - SCIM authentication type.
#   scim_oauth_access_token_expires_at - string - SCIM OAuth Access Token Expiration Time.
#   scim_username - string - SCIM username.
#   subdomain - string - Subdomain or domain name for your auth provider.   Example: `https://[subdomain].okta.com/`
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "client_id" in params and not isinstance(params["client_id"], str):
        raise InvalidParameterError("Bad parameter: client_id must be an str")
    if "client_secret" in params and not isinstance(
        params["client_secret"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: client_secret must be an str"
        )
    if "ldap_password" in params and not isinstance(
        params["ldap_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_password must be an str"
        )
    if "logo_delete" in params and not isinstance(params["logo_delete"], bool):
        raise InvalidParameterError(
            "Bad parameter: logo_delete must be an bool"
        )
    if "reset_scim_oauth_access_token" in params and not isinstance(
        params["reset_scim_oauth_access_token"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: reset_scim_oauth_access_token must be an bool"
        )
    if "scim_password" in params and not isinstance(
        params["scim_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: scim_password must be an str"
        )
    if "deprovision_behavior" in params and not isinstance(
        params["deprovision_behavior"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: deprovision_behavior must be an str"
        )
    if "deprovision_groups" in params and not isinstance(
        params["deprovision_groups"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: deprovision_groups must be an bool"
        )
    if "deprovision_users" in params and not isinstance(
        params["deprovision_users"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: deprovision_users must be an bool"
        )
    if "display_on_login_page" in params and not isinstance(
        params["display_on_login_page"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: display_on_login_page must be an bool"
        )
    if "enabled" in params and not isinstance(params["enabled"], bool):
        raise InvalidParameterError("Bad parameter: enabled must be an bool")
    if "label" in params and not isinstance(params["label"], str):
        raise InvalidParameterError("Bad parameter: label must be an str")
    if "ldap_base_dn" in params and not isinstance(
        params["ldap_base_dn"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_base_dn must be an str"
        )
    if "ldap_domain" in params and not isinstance(params["ldap_domain"], str):
        raise InvalidParameterError(
            "Bad parameter: ldap_domain must be an str"
        )
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
    if "ldap_provisioning_enabled" in params and not isinstance(
        params["ldap_provisioning_enabled"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: ldap_provisioning_enabled must be an bool"
        )
    if "ldap_secure" in params and not isinstance(params["ldap_secure"], bool):
        raise InvalidParameterError(
            "Bad parameter: ldap_secure must be an bool"
        )
    if "ldap_type" in params and not isinstance(params["ldap_type"], str):
        raise InvalidParameterError("Bad parameter: ldap_type must be an str")
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
    if "protocol" in params and not isinstance(params["protocol"], str):
        raise InvalidParameterError("Bad parameter: protocol must be an str")
    if "provider" in params and not isinstance(params["provider"], str):
        raise InvalidParameterError("Bad parameter: provider must be an str")
    if "provider_identifier" in params and not isinstance(
        params["provider_identifier"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provider_identifier must be an str"
        )
    if "provision_company" in params and not isinstance(
        params["provision_company"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_company must be an str"
        )
    if "provision_dav_permission" in params and not isinstance(
        params["provision_dav_permission"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_dav_permission must be an bool"
        )
    if "provision_email_signup_groups" in params and not isinstance(
        params["provision_email_signup_groups"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_email_signup_groups must be an str"
        )
    if "provision_filesystem_layout" in params and not isinstance(
        params["provision_filesystem_layout"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_filesystem_layout must be an str"
        )
    if "provision_ftp_permission" in params and not isinstance(
        params["provision_ftp_permission"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_ftp_permission must be an bool"
        )
    if "provision_group_admin_groups" in params and not isinstance(
        params["provision_group_admin_groups"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_group_admin_groups must be an str"
        )
    if "provision_group_default" in params and not isinstance(
        params["provision_group_default"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_group_default must be an str"
        )
    if "provision_group_exclusion" in params and not isinstance(
        params["provision_group_exclusion"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_group_exclusion must be an str"
        )
    if "provision_group_inclusion" in params and not isinstance(
        params["provision_group_inclusion"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_group_inclusion must be an str"
        )
    if "provision_group_required" in params and not isinstance(
        params["provision_group_required"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_group_required must be an str"
        )
    if "provision_groups" in params and not isinstance(
        params["provision_groups"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_groups must be an bool"
        )
    if "provision_readonly_site_admin_groups" in params and not isinstance(
        params["provision_readonly_site_admin_groups"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_readonly_site_admin_groups must be an str"
        )
    if "provision_require_2fa" in params and not isinstance(
        params["provision_require_2fa"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_require_2fa must be an str"
        )
    if "provision_sftp_permission" in params and not isinstance(
        params["provision_sftp_permission"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_sftp_permission must be an bool"
        )
    if "provision_site_admin_groups" in params and not isinstance(
        params["provision_site_admin_groups"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_site_admin_groups must be an str"
        )
    if "provision_time_zone" in params and not isinstance(
        params["provision_time_zone"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_time_zone must be an str"
        )
    if "provision_users" in params and not isinstance(
        params["provision_users"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: provision_users must be an bool"
        )
    if "saml_provider_cert_fingerprint" in params and not isinstance(
        params["saml_provider_cert_fingerprint"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: saml_provider_cert_fingerprint must be an str"
        )
    if "saml_provider_issuer_url" in params and not isinstance(
        params["saml_provider_issuer_url"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: saml_provider_issuer_url must be an str"
        )
    if "saml_provider_metadata_content" in params and not isinstance(
        params["saml_provider_metadata_content"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: saml_provider_metadata_content must be an str"
        )
    if "saml_provider_metadata_url" in params and not isinstance(
        params["saml_provider_metadata_url"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: saml_provider_metadata_url must be an str"
        )
    if "saml_provider_slo_target_url" in params and not isinstance(
        params["saml_provider_slo_target_url"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: saml_provider_slo_target_url must be an str"
        )
    if "saml_provider_sso_target_url" in params and not isinstance(
        params["saml_provider_sso_target_url"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: saml_provider_sso_target_url must be an str"
        )
    if "scim_authentication_method" in params and not isinstance(
        params["scim_authentication_method"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: scim_authentication_method must be an str"
        )
    if "scim_oauth_access_token_expires_at" in params and not isinstance(
        params["scim_oauth_access_token_expires_at"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: scim_oauth_access_token_expires_at must be an str"
        )
    if "scim_username" in params and not isinstance(
        params["scim_username"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: scim_username must be an str"
        )
    if "subdomain" in params and not isinstance(params["subdomain"], str):
        raise InvalidParameterError("Bad parameter: subdomain must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/sso_strategies/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return SsoStrategy(response.data, options)


def delete(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    Api.send_request(
        "DELETE",
        "/sso_strategies/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return SsoStrategy(*args, **kwargs)
