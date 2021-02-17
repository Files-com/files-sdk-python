import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class SsoStrategy:
    default_attributes = {
        'protocol': None,     # array - SSO Protocol
        'provider': None,     # string - Provider name
        'label': None,     # string - Custom label for the SSO provider on the login page.
        'logo_url': None,     # string - URL holding a custom logo for the SSO provider on the login page.
        'id': None,     # int64 - ID
        'saml_provider_cert_fingerprint': None,     # string - Identity provider sha256 cert fingerprint if saml_provider_metadata_url is not available.
        'saml_provider_issuer_url': None,     # string - Identity provider issuer url
        'saml_provider_metadata_content': None,     # string - Custom identity provider metadata
        'saml_provider_metadata_url': None,     # string - Metadata URL for the SAML identity provider
        'saml_provider_slo_target_url': None,     # string - Identity provider SLO endpoint
        'saml_provider_sso_target_url': None,     # string - Identity provider SSO endpoint if saml_provider_metadata_url is not available.
        'scim_authentication_method': None,     # string - SCIM authentication type.
        'scim_username': None,     # string - SCIM username.
        'scim_oauth_access_token': None,     # string - SCIM OAuth Access Token.
        'scim_oauth_access_token_expires_at': None,     # string - SCIM OAuth Access Token Expiration Time.
        'subdomain': None,     # string - Subdomain
        'provision_users': None,     # boolean - Auto-provision users?
        'provision_groups': None,     # boolean - Auto-provision group membership based on group memberships on the SSO side?
        'deprovision_users': None,     # boolean - Auto-deprovision users?
        'deprovision_groups': None,     # boolean - Auto-deprovision group membership based on group memberships on the SSO side?
        'deprovision_behavior': None,     # string - Method used for deprovisioning users.
        'provision_group_default': None,     # string - Comma-separated list of group names for groups to automatically add all auto-provisioned users to.
        'provision_group_exclusion': None,     # string - Comma-separated list of group names for groups (with optional wildcards) that will be excluded from auto-provisioning.
        'provision_group_inclusion': None,     # string - Comma-separated list of group names for groups (with optional wildcards) that will be auto-provisioned.
        'provision_group_required': None,     # string - Comma or newline separated list of group names (with optional wildcards) to require membership for user provisioning.
        'provision_site_admin_groups': None,     # string - Comma-separated list of group names whose members will be created as Site Admins.
        'provision_attachments_permission': None,     # boolean - DEPRECATED: Auto-provisioned users get Sharing permission. Use a Group with the Bundle permission instead.
        'provision_dav_permission': None,     # boolean - Auto-provisioned users get WebDAV permission?
        'provision_ftp_permission': None,     # boolean - Auto-provisioned users get FTP permission?
        'provision_sftp_permission': None,     # boolean - Auto-provisioned users get SFTP permission?
        'provision_time_zone': None,     # string - Default time zone for auto provisioned users.
        'provision_company': None,     # string - Default company for auto provisioned users.
        'ldap_base_dn': None,     # string - Base DN for looking up users in LDAP server
        'ldap_domain': None,     # string - Domain name that will be appended to LDAP usernames
        'enabled': None,     # boolean - Is strategy enabled?
        'ldap_host': None,     # string - LDAP host
        'ldap_host_2': None,     # string - LDAP backup host
        'ldap_host_3': None,     # string - LDAP backup host
        'ldap_port': None,     # int64 - LDAP port
        'ldap_secure': None,     # boolean - Use secure LDAP?
        'ldap_username': None,     # string - Username for signing in to LDAP server.
        'ldap_username_field': None,     # string - LDAP username field
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in SsoStrategy.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in SsoStrategy.default_attributes if getattr(self, k, None) is not None}


# Parameters:
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
def list(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(SsoStrategy,"GET", "/sso_strategies", params, options)

def all(params = None, options = None):
    list(params, options)

# Parameters:
#   id (required) - int64 - Sso Strategy ID.
def find(id, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("GET", "/sso_strategies/{id}".format(id=params['id']), params, options)
    return SsoStrategy(response.data, options)

def get(id, params = None, options = None):
    find(id, params, options)

def new(*args, **kwargs):
    return SsoStrategy(*args, **kwargs)