# SsoStrategy

## Example SsoStrategy Object

```
{
  "protocol": "oauth2",
  "provider": "okta",
  "label": "My Corporate SSO Provider",
  "logo_url": "https://mysite.files.com/.../logo.png",
  "id": 1,
  "user_count": 1,
  "saml_provider_cert_fingerprint": "example",
  "saml_provider_issuer_url": "example",
  "saml_provider_metadata_content": "example",
  "saml_provider_metadata_url": "example",
  "saml_provider_slo_target_url": "example",
  "saml_provider_sso_target_url": "example",
  "scim_authentication_method": "example",
  "scim_username": "example",
  "scim_oauth_access_token": "example",
  "scim_oauth_access_token_expires_at": "example",
  "subdomain": "my-site",
  "provision_users": True,
  "provision_groups": True,
  "deprovision_users": True,
  "deprovision_groups": True,
  "deprovision_behavior": "disable",
  "provision_group_default": "Employees",
  "provision_group_exclusion": "Employees",
  "provision_group_inclusion": "Employees",
  "provision_group_required": "example",
  "provision_email_signup_groups": "Employees",
  "provision_site_admin_groups": "Employees",
  "provision_group_admin_groups": "Employees",
  "provision_attachments_permission": True,
  "provision_dav_permission": True,
  "provision_ftp_permission": True,
  "provision_sftp_permission": True,
  "provision_time_zone": "Eastern Time (US & Canada)",
  "provision_company": "ACME Corp.",
  "provision_require_2fa": "always_require",
  "ldap_base_dn": "example",
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

* `protocol` (string): SSO Protocol
* `provider` (string): Provider name
* `label` (string): Custom label for the SSO provider on the login page.
* `logo_url` (string): URL holding a custom logo for the SSO provider on the login page.
* `id` (int64): ID
* `user_count` (int64): Count of users with this SSO Strategy
* `saml_provider_cert_fingerprint` (string): Identity provider sha256 cert fingerprint if saml_provider_metadata_url is not available.
* `saml_provider_issuer_url` (string): Identity provider issuer url
* `saml_provider_metadata_content` (string): Custom identity provider metadata
* `saml_provider_metadata_url` (string): Metadata URL for the SAML identity provider
* `saml_provider_slo_target_url` (string): Identity provider SLO endpoint
* `saml_provider_sso_target_url` (string): Identity provider SSO endpoint if saml_provider_metadata_url is not available.
* `scim_authentication_method` (string): SCIM authentication type.
* `scim_username` (string): SCIM username.
* `scim_oauth_access_token` (string): SCIM OAuth Access Token.
* `scim_oauth_access_token_expires_at` (string): SCIM OAuth Access Token Expiration Time.
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
* `provision_email_signup_groups` (string): Comma-separated list of group names whose members will be created with email_signup authentication.
* `provision_site_admin_groups` (string): Comma-separated list of group names whose members will be created as Site Admins.
* `provision_group_admin_groups` (string): Comma-separated list of group names whose members will be provisioned as Group Admins.
* `provision_attachments_permission` (boolean): DEPRECATED: Auto-provisioned users get Sharing permission. Use a Group with the Bundle permission instead.
* `provision_dav_permission` (boolean): Auto-provisioned users get WebDAV permission?
* `provision_ftp_permission` (boolean): Auto-provisioned users get FTP permission?
* `provision_sftp_permission` (boolean): Auto-provisioned users get SFTP permission?
* `provision_time_zone` (string): Default time zone for auto provisioned users.
* `provision_company` (string): Default company for auto provisioned users.
* `provision_require_2fa` (string): 2FA required setting for auto provisioned users.
* `ldap_base_dn` (string): Base DN for looking up users in LDAP server
* `ldap_domain` (string): Domain name that will be appended to LDAP usernames
* `enabled` (boolean): Is strategy enabled?  This may become automatically set to `false` after a high number and duration of failures.
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
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show Sso Strategy

```
files_sdk.sso_strategy.find(id)
```

### Parameters

* `id` (int64): Required - Sso Strategy ID.


---

## Synchronize provisioning data with the SSO remote server

```
files_sdk.sso_strategy.sync(id)
```

### Parameters

* `id` (int64): Required - Sso Strategy ID.


---

## Synchronize provisioning data with the SSO remote server

```
sso_strategy = files_sdk.sso_strategy.list.first
sso_strategy.sync()
```

### Parameters

* `id` (int64): Required - Sso Strategy ID.
