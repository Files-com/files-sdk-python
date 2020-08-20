# SsoStrategy

## Example SsoStrategy Object

```
{
  "protocol": [

  ],
  "provider": "okta",
  "label": "My Corporate SSO Provider",
  "logo_url": "https://mysite.files.com/.../logo.png",
  "id": 1,
  "saml_provider_cert_fingerprint": "",
  "saml_provider_issuer_url": "",
  "saml_provider_metadata_url": "",
  "saml_provider_slo_target_url": "",
  "saml_provider_sso_target_url": "",
  "scim_authentication_method": "",
  "scim_username": "",
  "subdomain": "my-site",
  "provision_users": True,
  "provision_groups": True,
  "deprovision_users": True,
  "deprovision_groups": True,
  "deprovision_behavior": "disable",
  "provision_group_default": "Employees",
  "provision_group_exclusion": "Employees",
  "provision_group_inclusion": "Employees",
  "provision_group_required": "",
  "provision_attachments_permission": True,
  "provision_dav_permission": True,
  "provision_ftp_permission": True,
  "provision_sftp_permission": True,
  "provision_time_zone": "Eastern Time (US & Canada)",
  "ldap_base_dn": "",
  "ldap_domain": "mysite.com",
  "enabled": True,
  "ldap_host": "ldap.site.com",
  "ldap_host_2": "ldap2.site.com",
  "ldap_host_3": "ldap3.site.com",
  "ldap_port": 1,
  "ldap_secure": True,
  "ldap_username": "[ldap username]",
  "ldap_username_field": "sAMAccountName"
}
```

* `protocol` (array): SSO Protocol
* `provider` (string): Provider name
* `label` (string): Custom label for the SSO provider on the login page.
* `logo_url` (string): URL holding a custom logo for the SSO provider on the login page.
* `id` (int64): ID
* `saml_provider_cert_fingerprint` (string): Identity provider sha256 cert fingerprint if saml_provider_metadata_url is not available.
* `saml_provider_issuer_url` (string): Identity provider issuer url
* `saml_provider_metadata_url` (string): Metadata URL for the SAML identity provider
* `saml_provider_slo_target_url` (string): Identity provider SLO endpoint
* `saml_provider_sso_target_url` (string): Identity provider SSO endpoint if saml_provider_metadata_url is not available.
* `scim_authentication_method` (string): SCIM authentication type.
* `scim_username` (string): SCIM username.
* `subdomain` (string): Subdomain
* `provision_users` (boolean): Auto-provision users?
* `provision_groups` (boolean): Auto-provision group membership based on group memberships on the SSO side?
* `deprovision_users` (boolean): Auto-deprovision users?
* `deprovision_groups` (boolean): Auto-deprovision group membership based on group memberships on the SSO side?
* `deprovision_behavior` (string): Method used for deprovisioning users.
* `provision_group_default` (string): Comma-separated list of group names for groups to automatically add all auto-provisioned users to.
* `provision_group_exclusion` (string): Comma-separated list of group names for groups (with optional wildcards) that will be excluded from auto-provisioning.
* `provision_group_inclusion` (string): Comma-separated list of group names for groups (with optional wildcards) that will be auto-provisioned.
* `provision_group_required` (string): Comma or newline separated list of group names (with optional wildcards) to require membership for user provisioning.
* `provision_attachments_permission` (boolean): Auto-provisioned users get Sharing permission?
* `provision_dav_permission` (boolean): Auto-provisioned users get WebDAV permission?
* `provision_ftp_permission` (boolean): Auto-provisioned users get FTP permission?
* `provision_sftp_permission` (boolean): Auto-provisioned users get SFTP permission?
* `provision_time_zone` (string): Default time zone for auto provisioned users.
* `ldap_base_dn` (string): Base DN for looking up users in LDAP server
* `ldap_domain` (string): Domain name that will be appended to LDAP usernames
* `enabled` (boolean): Is strategy enabled?
* `ldap_host` (string): LDAP host
* `ldap_host_2` (string): LDAP backup host
* `ldap_host_3` (string): LDAP backup host
* `ldap_port` (int64): LDAP port
* `ldap_secure` (boolean): Use secure LDAP?
* `ldap_username` (string): Username for signing in to LDAP server.
* `ldap_username_field` (string): LDAP username field


---

## List Sso Strategies

```
files_sdk.sso_strategy.list({
  "page": 1,
  "per_page": 1
})
```

### Parameters

* `page` (int64): Current page number.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
* `cursor` (string): Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.


---

## Show Sso Strategy

```
files_sdk.sso_strategy.find(id)
```

### Parameters

* `id` (int64): Required - Sso Strategy ID.
