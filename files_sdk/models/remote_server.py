import builtins  # noqa: F401
from files_sdk.models.remote_server_configuration_file import (
    RemoteServerConfigurationFile,
)
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class RemoteServer:
    default_attributes = {
        "id": None,  # int64 - Remote server ID
        "disabled": None,  # boolean - If true, this server has been disabled due to failures.  Make any change or set disabled to false to clear this flag.
        "authentication_method": None,  # string - Type of authentication method
        "hostname": None,  # string - Hostname or IP address
        "remote_home_path": None,  # string - Initial home folder on remote server
        "name": None,  # string - Internal name for your reference
        "port": None,  # int64 - Port for remote server.  Not needed for S3.
        "max_connections": None,  # int64 - Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
        "pin_to_site_region": None,  # boolean - If true, we will ensure that all communications with this remote server are made through the primary region of the site.  This setting can also be overridden by a site-wide setting which will force it to true.
        "pinned_region": None,  # string - If set, all communications with this remote server are made through the provided region.
        "s3_bucket": None,  # string - S3 bucket name
        "s3_region": None,  # string - S3 region
        "aws_access_key": None,  # string - AWS Access Key.
        "server_certificate": None,  # string - Remote server certificate
        "server_host_key": None,  # string - Remote server SSH Host Key. If provided, we will require that the server host key matches the provided key. Uses OpenSSH format similar to what would go into ~/.ssh/known_hosts
        "server_type": None,  # string - Remote server type.
        "ssl": None,  # string - Should we require SSL?
        "username": None,  # string - Remote server username.  Not needed for S3 buckets.
        "google_cloud_storage_bucket": None,  # string - Google Cloud Storage: Bucket Name
        "google_cloud_storage_project_id": None,  # string - Google Cloud Storage: Project ID
        "google_cloud_storage_s3_compatible_access_key": None,  # string - Google Cloud Storage: S3-compatible Access Key.
        "backblaze_b2_s3_endpoint": None,  # string - Backblaze B2 Cloud Storage: S3 Endpoint
        "backblaze_b2_bucket": None,  # string - Backblaze B2 Cloud Storage: Bucket name
        "wasabi_bucket": None,  # string - Wasabi: Bucket name
        "wasabi_region": None,  # string - Wasabi: Region
        "wasabi_access_key": None,  # string - Wasabi: Access Key.
        "rackspace_username": None,  # string - Rackspace: username used to login to the Rackspace Cloud Control Panel.
        "rackspace_region": None,  # string - Rackspace: Three letter code for Rackspace region. See https://support.rackspace.com/how-to/about-regions/
        "rackspace_container": None,  # string - Rackspace: The name of the container (top level directory) where files will sync.
        "auth_status": None,  # string - Either `in_setup` or `complete`
        "auth_account_name": None,  # string - Describes the authorized account
        "one_drive_account_type": None,  # string - OneDrive: Either personal or business_other account types
        "azure_blob_storage_account": None,  # string - Azure Blob Storage: Account name
        "azure_blob_storage_container": None,  # string - Azure Blob Storage: Container name
        "azure_blob_storage_hierarchical_namespace": None,  # boolean - Azure Blob Storage: Does the storage account has hierarchical namespace feature enabled?
        "azure_blob_storage_dns_suffix": None,  # string - Azure Blob Storage: Custom DNS suffix
        "azure_files_storage_account": None,  # string - Azure Files: Storage Account name
        "azure_files_storage_share_name": None,  # string - Azure Files:  Storage Share name
        "azure_files_storage_dns_suffix": None,  # string - Azure Files: Custom DNS suffix
        "s3_compatible_bucket": None,  # string - S3-compatible: Bucket name
        "s3_compatible_endpoint": None,  # string - S3-compatible: endpoint
        "s3_compatible_region": None,  # string - S3-compatible: region
        "s3_compatible_access_key": None,  # string - S3-compatible: Access Key
        "enable_dedicated_ips": None,  # boolean - `true` if remote server only accepts connections from dedicated IPs
        "files_agent_permission_set": None,  # string - Local permissions for files agent. read_only, write_only, or read_write
        "files_agent_root": None,  # string - Agent local root path
        "files_agent_api_token": None,  # string - Files Agent API Token
        "files_agent_version": None,  # string - Files Agent version
        "filebase_bucket": None,  # string - Filebase: Bucket name
        "filebase_access_key": None,  # string - Filebase: Access Key.
        "cloudflare_bucket": None,  # string - Cloudflare: Bucket name
        "cloudflare_access_key": None,  # string - Cloudflare: Access Key.
        "cloudflare_endpoint": None,  # string - Cloudflare: endpoint
        "dropbox_teams": None,  # boolean - Dropbox: If true, list Team folders in root?
        "linode_bucket": None,  # string - Linode: Bucket name
        "linode_access_key": None,  # string - Linode: Access Key
        "linode_region": None,  # string - Linode: region
        "supports_versioning": None,  # boolean - If true, this remote server supports file versioning. This value is determined automatically by Files.com.
        "password": None,  # string - Password, if needed.
        "private_key": None,  # string - Private key, if needed.
        "private_key_passphrase": None,  # string - Passphrase for private key if needed.
        "reset_authentication": None,  # boolean - Reset authenticated account?
        "ssl_certificate": None,  # string - SSL client certificate.
        "aws_secret_key": None,  # string - AWS: secret key.
        "azure_blob_storage_access_key": None,  # string - Azure Blob Storage: Access Key
        "azure_blob_storage_sas_token": None,  # string - Azure Blob Storage: Shared Access Signature (SAS) token
        "azure_files_storage_access_key": None,  # string - Azure File Storage: Access Key
        "azure_files_storage_sas_token": None,  # string - Azure File Storage: Shared Access Signature (SAS) token
        "backblaze_b2_application_key": None,  # string - Backblaze B2 Cloud Storage: applicationKey
        "backblaze_b2_key_id": None,  # string - Backblaze B2 Cloud Storage: keyID
        "cloudflare_secret_key": None,  # string - Cloudflare: Secret Key
        "filebase_secret_key": None,  # string - Filebase: Secret Key
        "google_cloud_storage_credentials_json": None,  # string - Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
        "google_cloud_storage_s3_compatible_secret_key": None,  # string - Google Cloud Storage: S3-compatible secret key
        "linode_secret_key": None,  # string - Linode: Secret Key
        "rackspace_api_key": None,  # string - Rackspace: API key from the Rackspace Cloud Control Panel
        "s3_compatible_secret_key": None,  # string - S3-compatible: Secret Key
        "wasabi_secret_key": None,  # string - Wasabi: Secret Key
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (
            attribute,
            default_value,
        ) in RemoteServer.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in RemoteServer.default_attributes
            if getattr(self, k, None) is not None
        }

    # Post local changes, check in, and download configuration file (used by some Remote Server integrations, such as the Files.com Agent)
    #
    # Parameters:
    #   api_token - string - Files Agent API Token
    #   permission_set - string - The permission set for the agent ['read_write', 'read_only', 'write_only']
    #   root - string - The root directory for the agent
    #   hostname - string
    #   port - int64 - Incoming port for files agent connections
    #   status - string - either running or shutdown
    #   config_version - string - agent config version
    #   private_key - string - The private key for the agent
    #   public_key - string - public key
    #   server_host_key - string
    #   subdomain - string - Files.com subdomain site name
    def configuration_file(self, params=None):
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
        if "api_token" in params and not isinstance(params["api_token"], str):
            raise InvalidParameterError(
                "Bad parameter: api_token must be an str"
            )
        if "permission_set" in params and not isinstance(
            params["permission_set"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: permission_set must be an str"
            )
        if "root" in params and not isinstance(params["root"], str):
            raise InvalidParameterError("Bad parameter: root must be an str")
        if "hostname" in params and not isinstance(params["hostname"], str):
            raise InvalidParameterError(
                "Bad parameter: hostname must be an str"
            )
        if "port" in params and not isinstance(params["port"], int):
            raise InvalidParameterError("Bad parameter: port must be an int")
        if "status" in params and not isinstance(params["status"], str):
            raise InvalidParameterError("Bad parameter: status must be an str")
        if "config_version" in params and not isinstance(
            params["config_version"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: config_version must be an str"
            )
        if "private_key" in params and not isinstance(
            params["private_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key must be an str"
            )
        if "public_key" in params and not isinstance(
            params["public_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: public_key must be an str"
            )
        if "server_host_key" in params and not isinstance(
            params["server_host_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: server_host_key must be an str"
            )
        if "subdomain" in params and not isinstance(params["subdomain"], str):
            raise InvalidParameterError(
                "Bad parameter: subdomain must be an str"
            )
        response, _options = Api.send_request(
            "POST",
            "/remote_servers/{id}/configuration_file".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    # Parameters:
    #   password - string - Password, if needed.
    #   private_key - string - Private key, if needed.
    #   private_key_passphrase - string - Passphrase for private key if needed.
    #   reset_authentication - boolean - Reset authenticated account?
    #   ssl_certificate - string - SSL client certificate.
    #   aws_secret_key - string - AWS: secret key.
    #   azure_blob_storage_access_key - string - Azure Blob Storage: Access Key
    #   azure_blob_storage_sas_token - string - Azure Blob Storage: Shared Access Signature (SAS) token
    #   azure_files_storage_access_key - string - Azure File Storage: Access Key
    #   azure_files_storage_sas_token - string - Azure File Storage: Shared Access Signature (SAS) token
    #   backblaze_b2_application_key - string - Backblaze B2 Cloud Storage: applicationKey
    #   backblaze_b2_key_id - string - Backblaze B2 Cloud Storage: keyID
    #   cloudflare_secret_key - string - Cloudflare: Secret Key
    #   filebase_secret_key - string - Filebase: Secret Key
    #   google_cloud_storage_credentials_json - string - Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
    #   google_cloud_storage_s3_compatible_secret_key - string - Google Cloud Storage: S3-compatible secret key
    #   linode_secret_key - string - Linode: Secret Key
    #   rackspace_api_key - string - Rackspace: API key from the Rackspace Cloud Control Panel
    #   s3_compatible_secret_key - string - S3-compatible: Secret Key
    #   wasabi_secret_key - string - Wasabi: Secret Key
    #   aws_access_key - string - AWS Access Key.
    #   azure_blob_storage_account - string - Azure Blob Storage: Account name
    #   azure_blob_storage_container - string - Azure Blob Storage: Container name
    #   azure_blob_storage_dns_suffix - string - Azure Blob Storage: Custom DNS suffix
    #   azure_blob_storage_hierarchical_namespace - boolean - Azure Blob Storage: Does the storage account has hierarchical namespace feature enabled?
    #   azure_files_storage_account - string - Azure Files: Storage Account name
    #   azure_files_storage_dns_suffix - string - Azure Files: Custom DNS suffix
    #   azure_files_storage_share_name - string - Azure Files:  Storage Share name
    #   backblaze_b2_bucket - string - Backblaze B2 Cloud Storage: Bucket name
    #   backblaze_b2_s3_endpoint - string - Backblaze B2 Cloud Storage: S3 Endpoint
    #   cloudflare_access_key - string - Cloudflare: Access Key.
    #   cloudflare_bucket - string - Cloudflare: Bucket name
    #   cloudflare_endpoint - string - Cloudflare: endpoint
    #   dropbox_teams - boolean - Dropbox: If true, list Team folders in root?
    #   enable_dedicated_ips - boolean - `true` if remote server only accepts connections from dedicated IPs
    #   filebase_access_key - string - Filebase: Access Key.
    #   filebase_bucket - string - Filebase: Bucket name
    #   files_agent_permission_set - string - Local permissions for files agent. read_only, write_only, or read_write
    #   files_agent_root - string - Agent local root path
    #   files_agent_version - string - Files Agent version
    #   google_cloud_storage_bucket - string - Google Cloud Storage: Bucket Name
    #   google_cloud_storage_project_id - string - Google Cloud Storage: Project ID
    #   google_cloud_storage_s3_compatible_access_key - string - Google Cloud Storage: S3-compatible Access Key.
    #   hostname - string - Hostname or IP address
    #   linode_access_key - string - Linode: Access Key
    #   linode_bucket - string - Linode: Bucket name
    #   linode_region - string - Linode: region
    #   max_connections - int64 - Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
    #   name - string - Internal name for your reference
    #   one_drive_account_type - string - OneDrive: Either personal or business_other account types
    #   pin_to_site_region - boolean - If true, we will ensure that all communications with this remote server are made through the primary region of the site.  This setting can also be overridden by a site-wide setting which will force it to true.
    #   port - int64 - Port for remote server.  Not needed for S3.
    #   rackspace_container - string - Rackspace: The name of the container (top level directory) where files will sync.
    #   rackspace_region - string - Rackspace: Three letter code for Rackspace region. See https://support.rackspace.com/how-to/about-regions/
    #   rackspace_username - string - Rackspace: username used to login to the Rackspace Cloud Control Panel.
    #   s3_bucket - string - S3 bucket name
    #   s3_compatible_access_key - string - S3-compatible: Access Key
    #   s3_compatible_bucket - string - S3-compatible: Bucket name
    #   s3_compatible_endpoint - string - S3-compatible: endpoint
    #   s3_compatible_region - string - S3-compatible: region
    #   s3_region - string - S3 region
    #   server_certificate - string - Remote server certificate
    #   server_host_key - string - Remote server SSH Host Key. If provided, we will require that the server host key matches the provided key. Uses OpenSSH format similar to what would go into ~/.ssh/known_hosts
    #   server_type - string - Remote server type.
    #   ssl - string - Should we require SSL?
    #   username - string - Remote server username.  Not needed for S3 buckets.
    #   wasabi_access_key - string - Wasabi: Access Key.
    #   wasabi_bucket - string - Wasabi: Bucket name
    #   wasabi_region - string - Wasabi: Region
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
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError(
                "Bad parameter: password must be an str"
            )
        if "private_key" in params and not isinstance(
            params["private_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key must be an str"
            )
        if "private_key_passphrase" in params and not isinstance(
            params["private_key_passphrase"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key_passphrase must be an str"
            )
        if "ssl_certificate" in params and not isinstance(
            params["ssl_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: ssl_certificate must be an str"
            )
        if "aws_secret_key" in params and not isinstance(
            params["aws_secret_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: aws_secret_key must be an str"
            )
        if "azure_blob_storage_access_key" in params and not isinstance(
            params["azure_blob_storage_access_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_blob_storage_access_key must be an str"
            )
        if "azure_blob_storage_sas_token" in params and not isinstance(
            params["azure_blob_storage_sas_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_blob_storage_sas_token must be an str"
            )
        if "azure_files_storage_access_key" in params and not isinstance(
            params["azure_files_storage_access_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_files_storage_access_key must be an str"
            )
        if "azure_files_storage_sas_token" in params and not isinstance(
            params["azure_files_storage_sas_token"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_files_storage_sas_token must be an str"
            )
        if "backblaze_b2_application_key" in params and not isinstance(
            params["backblaze_b2_application_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: backblaze_b2_application_key must be an str"
            )
        if "backblaze_b2_key_id" in params and not isinstance(
            params["backblaze_b2_key_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: backblaze_b2_key_id must be an str"
            )
        if "cloudflare_secret_key" in params and not isinstance(
            params["cloudflare_secret_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: cloudflare_secret_key must be an str"
            )
        if "filebase_secret_key" in params and not isinstance(
            params["filebase_secret_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: filebase_secret_key must be an str"
            )
        if (
            "google_cloud_storage_credentials_json" in params
            and not isinstance(
                params["google_cloud_storage_credentials_json"], str
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: google_cloud_storage_credentials_json must be an str"
            )
        if (
            "google_cloud_storage_s3_compatible_secret_key" in params
            and not isinstance(
                params["google_cloud_storage_s3_compatible_secret_key"], str
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: google_cloud_storage_s3_compatible_secret_key must be an str"
            )
        if "linode_secret_key" in params and not isinstance(
            params["linode_secret_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: linode_secret_key must be an str"
            )
        if "rackspace_api_key" in params and not isinstance(
            params["rackspace_api_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: rackspace_api_key must be an str"
            )
        if "s3_compatible_secret_key" in params and not isinstance(
            params["s3_compatible_secret_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_compatible_secret_key must be an str"
            )
        if "wasabi_secret_key" in params and not isinstance(
            params["wasabi_secret_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: wasabi_secret_key must be an str"
            )
        if "aws_access_key" in params and not isinstance(
            params["aws_access_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: aws_access_key must be an str"
            )
        if "azure_blob_storage_account" in params and not isinstance(
            params["azure_blob_storage_account"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_blob_storage_account must be an str"
            )
        if "azure_blob_storage_container" in params and not isinstance(
            params["azure_blob_storage_container"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_blob_storage_container must be an str"
            )
        if "azure_blob_storage_dns_suffix" in params and not isinstance(
            params["azure_blob_storage_dns_suffix"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_blob_storage_dns_suffix must be an str"
            )
        if "azure_files_storage_account" in params and not isinstance(
            params["azure_files_storage_account"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_files_storage_account must be an str"
            )
        if "azure_files_storage_dns_suffix" in params and not isinstance(
            params["azure_files_storage_dns_suffix"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_files_storage_dns_suffix must be an str"
            )
        if "azure_files_storage_share_name" in params and not isinstance(
            params["azure_files_storage_share_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_files_storage_share_name must be an str"
            )
        if "backblaze_b2_bucket" in params and not isinstance(
            params["backblaze_b2_bucket"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: backblaze_b2_bucket must be an str"
            )
        if "backblaze_b2_s3_endpoint" in params and not isinstance(
            params["backblaze_b2_s3_endpoint"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: backblaze_b2_s3_endpoint must be an str"
            )
        if "cloudflare_access_key" in params and not isinstance(
            params["cloudflare_access_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: cloudflare_access_key must be an str"
            )
        if "cloudflare_bucket" in params and not isinstance(
            params["cloudflare_bucket"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: cloudflare_bucket must be an str"
            )
        if "cloudflare_endpoint" in params and not isinstance(
            params["cloudflare_endpoint"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: cloudflare_endpoint must be an str"
            )
        if "filebase_access_key" in params and not isinstance(
            params["filebase_access_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: filebase_access_key must be an str"
            )
        if "filebase_bucket" in params and not isinstance(
            params["filebase_bucket"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: filebase_bucket must be an str"
            )
        if "files_agent_permission_set" in params and not isinstance(
            params["files_agent_permission_set"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: files_agent_permission_set must be an str"
            )
        if "files_agent_root" in params and not isinstance(
            params["files_agent_root"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: files_agent_root must be an str"
            )
        if "files_agent_version" in params and not isinstance(
            params["files_agent_version"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: files_agent_version must be an str"
            )
        if "google_cloud_storage_bucket" in params and not isinstance(
            params["google_cloud_storage_bucket"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: google_cloud_storage_bucket must be an str"
            )
        if "google_cloud_storage_project_id" in params and not isinstance(
            params["google_cloud_storage_project_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: google_cloud_storage_project_id must be an str"
            )
        if (
            "google_cloud_storage_s3_compatible_access_key" in params
            and not isinstance(
                params["google_cloud_storage_s3_compatible_access_key"], str
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: google_cloud_storage_s3_compatible_access_key must be an str"
            )
        if "hostname" in params and not isinstance(params["hostname"], str):
            raise InvalidParameterError(
                "Bad parameter: hostname must be an str"
            )
        if "linode_access_key" in params and not isinstance(
            params["linode_access_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: linode_access_key must be an str"
            )
        if "linode_bucket" in params and not isinstance(
            params["linode_bucket"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: linode_bucket must be an str"
            )
        if "linode_region" in params and not isinstance(
            params["linode_region"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: linode_region must be an str"
            )
        if "max_connections" in params and not isinstance(
            params["max_connections"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: max_connections must be an int"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "one_drive_account_type" in params and not isinstance(
            params["one_drive_account_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: one_drive_account_type must be an str"
            )
        if "port" in params and not isinstance(params["port"], int):
            raise InvalidParameterError("Bad parameter: port must be an int")
        if "rackspace_container" in params and not isinstance(
            params["rackspace_container"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: rackspace_container must be an str"
            )
        if "rackspace_region" in params and not isinstance(
            params["rackspace_region"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: rackspace_region must be an str"
            )
        if "rackspace_username" in params and not isinstance(
            params["rackspace_username"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: rackspace_username must be an str"
            )
        if "s3_bucket" in params and not isinstance(params["s3_bucket"], str):
            raise InvalidParameterError(
                "Bad parameter: s3_bucket must be an str"
            )
        if "s3_compatible_access_key" in params and not isinstance(
            params["s3_compatible_access_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_compatible_access_key must be an str"
            )
        if "s3_compatible_bucket" in params and not isinstance(
            params["s3_compatible_bucket"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_compatible_bucket must be an str"
            )
        if "s3_compatible_endpoint" in params and not isinstance(
            params["s3_compatible_endpoint"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_compatible_endpoint must be an str"
            )
        if "s3_compatible_region" in params and not isinstance(
            params["s3_compatible_region"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_compatible_region must be an str"
            )
        if "s3_region" in params and not isinstance(params["s3_region"], str):
            raise InvalidParameterError(
                "Bad parameter: s3_region must be an str"
            )
        if "server_certificate" in params and not isinstance(
            params["server_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: server_certificate must be an str"
            )
        if "server_host_key" in params and not isinstance(
            params["server_host_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: server_host_key must be an str"
            )
        if "server_type" in params and not isinstance(
            params["server_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: server_type must be an str"
            )
        if "ssl" in params and not isinstance(params["ssl"], str):
            raise InvalidParameterError("Bad parameter: ssl must be an str")
        if "username" in params and not isinstance(params["username"], str):
            raise InvalidParameterError(
                "Bad parameter: username must be an str"
            )
        if "wasabi_access_key" in params and not isinstance(
            params["wasabi_access_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: wasabi_access_key must be an str"
            )
        if "wasabi_bucket" in params and not isinstance(
            params["wasabi_bucket"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: wasabi_bucket must be an str"
            )
        if "wasabi_region" in params and not isinstance(
            params["wasabi_region"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: wasabi_region must be an str"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/remote_servers/{id}".format(id=params["id"]),
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
            "/remote_servers/{id}".format(id=params["id"]),
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
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `server_type`, `backblaze_b2_bucket`, `google_cloud_storage_bucket`, `wasabi_bucket`, `s3_bucket`, `rackspace_container`, `azure_blob_storage_container`, `azure_files_storage_share_name`, `s3_compatible_bucket`, `filebase_bucket`, `cloudflare_bucket` or `linode_bucket`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `name`, `server_type`, `backblaze_b2_bucket`, `google_cloud_storage_bucket`, `wasabi_bucket`, `s3_bucket`, `rackspace_container`, `azure_blob_storage_container`, `azure_files_storage_share_name`, `s3_compatible_bucket`, `filebase_bucket`, `cloudflare_bucket` or `linode_bucket`. Valid field combinations are `[ server_type, name ]`, `[ backblaze_b2_bucket, name ]`, `[ google_cloud_storage_bucket, name ]`, `[ wasabi_bucket, name ]`, `[ s3_bucket, name ]`, `[ rackspace_container, name ]`, `[ azure_blob_storage_container, name ]`, `[ azure_files_storage_share_name, name ]`, `[ s3_compatible_bucket, name ]`, `[ filebase_bucket, name ]`, `[ cloudflare_bucket, name ]` or `[ linode_bucket, name ]`.
#   filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`, `backblaze_b2_bucket`, `google_cloud_storage_bucket`, `wasabi_bucket`, `s3_bucket`, `rackspace_container`, `azure_blob_storage_container`, `azure_files_storage_share_name`, `s3_compatible_bucket`, `filebase_bucket`, `cloudflare_bucket` or `linode_bucket`. Valid field combinations are `[ backblaze_b2_bucket, name ]`, `[ google_cloud_storage_bucket, name ]`, `[ wasabi_bucket, name ]`, `[ s3_bucket, name ]`, `[ rackspace_container, name ]`, `[ azure_blob_storage_container, name ]`, `[ azure_files_storage_share_name, name ]`, `[ s3_compatible_bucket, name ]`, `[ filebase_bucket, name ]`, `[ cloudflare_bucket, name ]` or `[ linode_bucket, name ]`.
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
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_prefix" in params and not isinstance(
        params["filter_prefix"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: filter_prefix must be an dict"
        )
    return ListObj(RemoteServer, "GET", "/remote_servers", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Remote Server ID.
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
        "GET", "/remote_servers/{id}".format(id=params["id"]), params, options
    )
    return RemoteServer(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   id (required) - int64 - Remote Server ID.
def find_configuration_file(id, params=None, options=None):
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
        "/remote_servers/{id}/configuration_file".format(id=params["id"]),
        params,
        options,
    )
    return RemoteServerConfigurationFile(response.data, options)


# Parameters:
#   password - string - Password, if needed.
#   private_key - string - Private key, if needed.
#   private_key_passphrase - string - Passphrase for private key if needed.
#   reset_authentication - boolean - Reset authenticated account?
#   ssl_certificate - string - SSL client certificate.
#   aws_secret_key - string - AWS: secret key.
#   azure_blob_storage_access_key - string - Azure Blob Storage: Access Key
#   azure_blob_storage_sas_token - string - Azure Blob Storage: Shared Access Signature (SAS) token
#   azure_files_storage_access_key - string - Azure File Storage: Access Key
#   azure_files_storage_sas_token - string - Azure File Storage: Shared Access Signature (SAS) token
#   backblaze_b2_application_key - string - Backblaze B2 Cloud Storage: applicationKey
#   backblaze_b2_key_id - string - Backblaze B2 Cloud Storage: keyID
#   cloudflare_secret_key - string - Cloudflare: Secret Key
#   filebase_secret_key - string - Filebase: Secret Key
#   google_cloud_storage_credentials_json - string - Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
#   google_cloud_storage_s3_compatible_secret_key - string - Google Cloud Storage: S3-compatible secret key
#   linode_secret_key - string - Linode: Secret Key
#   rackspace_api_key - string - Rackspace: API key from the Rackspace Cloud Control Panel
#   s3_compatible_secret_key - string - S3-compatible: Secret Key
#   wasabi_secret_key - string - Wasabi: Secret Key
#   aws_access_key - string - AWS Access Key.
#   azure_blob_storage_account - string - Azure Blob Storage: Account name
#   azure_blob_storage_container - string - Azure Blob Storage: Container name
#   azure_blob_storage_dns_suffix - string - Azure Blob Storage: Custom DNS suffix
#   azure_blob_storage_hierarchical_namespace - boolean - Azure Blob Storage: Does the storage account has hierarchical namespace feature enabled?
#   azure_files_storage_account - string - Azure Files: Storage Account name
#   azure_files_storage_dns_suffix - string - Azure Files: Custom DNS suffix
#   azure_files_storage_share_name - string - Azure Files:  Storage Share name
#   backblaze_b2_bucket - string - Backblaze B2 Cloud Storage: Bucket name
#   backblaze_b2_s3_endpoint - string - Backblaze B2 Cloud Storage: S3 Endpoint
#   cloudflare_access_key - string - Cloudflare: Access Key.
#   cloudflare_bucket - string - Cloudflare: Bucket name
#   cloudflare_endpoint - string - Cloudflare: endpoint
#   dropbox_teams - boolean - Dropbox: If true, list Team folders in root?
#   enable_dedicated_ips - boolean - `true` if remote server only accepts connections from dedicated IPs
#   filebase_access_key - string - Filebase: Access Key.
#   filebase_bucket - string - Filebase: Bucket name
#   files_agent_permission_set - string - Local permissions for files agent. read_only, write_only, or read_write
#   files_agent_root - string - Agent local root path
#   files_agent_version - string - Files Agent version
#   google_cloud_storage_bucket - string - Google Cloud Storage: Bucket Name
#   google_cloud_storage_project_id - string - Google Cloud Storage: Project ID
#   google_cloud_storage_s3_compatible_access_key - string - Google Cloud Storage: S3-compatible Access Key.
#   hostname - string - Hostname or IP address
#   linode_access_key - string - Linode: Access Key
#   linode_bucket - string - Linode: Bucket name
#   linode_region - string - Linode: region
#   max_connections - int64 - Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
#   name - string - Internal name for your reference
#   one_drive_account_type - string - OneDrive: Either personal or business_other account types
#   pin_to_site_region - boolean - If true, we will ensure that all communications with this remote server are made through the primary region of the site.  This setting can also be overridden by a site-wide setting which will force it to true.
#   port - int64 - Port for remote server.  Not needed for S3.
#   rackspace_container - string - Rackspace: The name of the container (top level directory) where files will sync.
#   rackspace_region - string - Rackspace: Three letter code for Rackspace region. See https://support.rackspace.com/how-to/about-regions/
#   rackspace_username - string - Rackspace: username used to login to the Rackspace Cloud Control Panel.
#   s3_bucket - string - S3 bucket name
#   s3_compatible_access_key - string - S3-compatible: Access Key
#   s3_compatible_bucket - string - S3-compatible: Bucket name
#   s3_compatible_endpoint - string - S3-compatible: endpoint
#   s3_compatible_region - string - S3-compatible: region
#   s3_region - string - S3 region
#   server_certificate - string - Remote server certificate
#   server_host_key - string - Remote server SSH Host Key. If provided, we will require that the server host key matches the provided key. Uses OpenSSH format similar to what would go into ~/.ssh/known_hosts
#   server_type - string - Remote server type.
#   ssl - string - Should we require SSL?
#   username - string - Remote server username.  Not needed for S3 buckets.
#   wasabi_access_key - string - Wasabi: Access Key.
#   wasabi_bucket - string - Wasabi: Bucket name
#   wasabi_region - string - Wasabi: Region
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError(
            "Bad parameter: private_key must be an str"
        )
    if "private_key_passphrase" in params and not isinstance(
        params["private_key_passphrase"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: private_key_passphrase must be an str"
        )
    if "ssl_certificate" in params and not isinstance(
        params["ssl_certificate"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ssl_certificate must be an str"
        )
    if "aws_secret_key" in params and not isinstance(
        params["aws_secret_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: aws_secret_key must be an str"
        )
    if "azure_blob_storage_access_key" in params and not isinstance(
        params["azure_blob_storage_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_blob_storage_access_key must be an str"
        )
    if "azure_blob_storage_sas_token" in params and not isinstance(
        params["azure_blob_storage_sas_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_blob_storage_sas_token must be an str"
        )
    if "azure_files_storage_access_key" in params and not isinstance(
        params["azure_files_storage_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_files_storage_access_key must be an str"
        )
    if "azure_files_storage_sas_token" in params and not isinstance(
        params["azure_files_storage_sas_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_files_storage_sas_token must be an str"
        )
    if "backblaze_b2_application_key" in params and not isinstance(
        params["backblaze_b2_application_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: backblaze_b2_application_key must be an str"
        )
    if "backblaze_b2_key_id" in params and not isinstance(
        params["backblaze_b2_key_id"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: backblaze_b2_key_id must be an str"
        )
    if "cloudflare_secret_key" in params and not isinstance(
        params["cloudflare_secret_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: cloudflare_secret_key must be an str"
        )
    if "filebase_secret_key" in params and not isinstance(
        params["filebase_secret_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: filebase_secret_key must be an str"
        )
    if "google_cloud_storage_credentials_json" in params and not isinstance(
        params["google_cloud_storage_credentials_json"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: google_cloud_storage_credentials_json must be an str"
        )
    if (
        "google_cloud_storage_s3_compatible_secret_key" in params
        and not isinstance(
            params["google_cloud_storage_s3_compatible_secret_key"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: google_cloud_storage_s3_compatible_secret_key must be an str"
        )
    if "linode_secret_key" in params and not isinstance(
        params["linode_secret_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: linode_secret_key must be an str"
        )
    if "rackspace_api_key" in params and not isinstance(
        params["rackspace_api_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: rackspace_api_key must be an str"
        )
    if "s3_compatible_secret_key" in params and not isinstance(
        params["s3_compatible_secret_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: s3_compatible_secret_key must be an str"
        )
    if "wasabi_secret_key" in params and not isinstance(
        params["wasabi_secret_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: wasabi_secret_key must be an str"
        )
    if "aws_access_key" in params and not isinstance(
        params["aws_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: aws_access_key must be an str"
        )
    if "azure_blob_storage_account" in params and not isinstance(
        params["azure_blob_storage_account"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_blob_storage_account must be an str"
        )
    if "azure_blob_storage_container" in params and not isinstance(
        params["azure_blob_storage_container"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_blob_storage_container must be an str"
        )
    if "azure_blob_storage_dns_suffix" in params and not isinstance(
        params["azure_blob_storage_dns_suffix"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_blob_storage_dns_suffix must be an str"
        )
    if "azure_files_storage_account" in params and not isinstance(
        params["azure_files_storage_account"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_files_storage_account must be an str"
        )
    if "azure_files_storage_dns_suffix" in params and not isinstance(
        params["azure_files_storage_dns_suffix"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_files_storage_dns_suffix must be an str"
        )
    if "azure_files_storage_share_name" in params and not isinstance(
        params["azure_files_storage_share_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_files_storage_share_name must be an str"
        )
    if "backblaze_b2_bucket" in params and not isinstance(
        params["backblaze_b2_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: backblaze_b2_bucket must be an str"
        )
    if "backblaze_b2_s3_endpoint" in params and not isinstance(
        params["backblaze_b2_s3_endpoint"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: backblaze_b2_s3_endpoint must be an str"
        )
    if "cloudflare_access_key" in params and not isinstance(
        params["cloudflare_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: cloudflare_access_key must be an str"
        )
    if "cloudflare_bucket" in params and not isinstance(
        params["cloudflare_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: cloudflare_bucket must be an str"
        )
    if "cloudflare_endpoint" in params and not isinstance(
        params["cloudflare_endpoint"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: cloudflare_endpoint must be an str"
        )
    if "filebase_access_key" in params and not isinstance(
        params["filebase_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: filebase_access_key must be an str"
        )
    if "filebase_bucket" in params and not isinstance(
        params["filebase_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: filebase_bucket must be an str"
        )
    if "files_agent_permission_set" in params and not isinstance(
        params["files_agent_permission_set"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: files_agent_permission_set must be an str"
        )
    if "files_agent_root" in params and not isinstance(
        params["files_agent_root"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: files_agent_root must be an str"
        )
    if "files_agent_version" in params and not isinstance(
        params["files_agent_version"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: files_agent_version must be an str"
        )
    if "google_cloud_storage_bucket" in params and not isinstance(
        params["google_cloud_storage_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: google_cloud_storage_bucket must be an str"
        )
    if "google_cloud_storage_project_id" in params and not isinstance(
        params["google_cloud_storage_project_id"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: google_cloud_storage_project_id must be an str"
        )
    if (
        "google_cloud_storage_s3_compatible_access_key" in params
        and not isinstance(
            params["google_cloud_storage_s3_compatible_access_key"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: google_cloud_storage_s3_compatible_access_key must be an str"
        )
    if "hostname" in params and not isinstance(params["hostname"], str):
        raise InvalidParameterError("Bad parameter: hostname must be an str")
    if "linode_access_key" in params and not isinstance(
        params["linode_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: linode_access_key must be an str"
        )
    if "linode_bucket" in params and not isinstance(
        params["linode_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: linode_bucket must be an str"
        )
    if "linode_region" in params and not isinstance(
        params["linode_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: linode_region must be an str"
        )
    if "max_connections" in params and not isinstance(
        params["max_connections"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: max_connections must be an int"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "one_drive_account_type" in params and not isinstance(
        params["one_drive_account_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: one_drive_account_type must be an str"
        )
    if "port" in params and not isinstance(params["port"], int):
        raise InvalidParameterError("Bad parameter: port must be an int")
    if "rackspace_container" in params and not isinstance(
        params["rackspace_container"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: rackspace_container must be an str"
        )
    if "rackspace_region" in params and not isinstance(
        params["rackspace_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: rackspace_region must be an str"
        )
    if "rackspace_username" in params and not isinstance(
        params["rackspace_username"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: rackspace_username must be an str"
        )
    if "s3_bucket" in params and not isinstance(params["s3_bucket"], str):
        raise InvalidParameterError("Bad parameter: s3_bucket must be an str")
    if "s3_compatible_access_key" in params and not isinstance(
        params["s3_compatible_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: s3_compatible_access_key must be an str"
        )
    if "s3_compatible_bucket" in params and not isinstance(
        params["s3_compatible_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: s3_compatible_bucket must be an str"
        )
    if "s3_compatible_endpoint" in params and not isinstance(
        params["s3_compatible_endpoint"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: s3_compatible_endpoint must be an str"
        )
    if "s3_compatible_region" in params and not isinstance(
        params["s3_compatible_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: s3_compatible_region must be an str"
        )
    if "s3_region" in params and not isinstance(params["s3_region"], str):
        raise InvalidParameterError("Bad parameter: s3_region must be an str")
    if "server_certificate" in params and not isinstance(
        params["server_certificate"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: server_certificate must be an str"
        )
    if "server_host_key" in params and not isinstance(
        params["server_host_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: server_host_key must be an str"
        )
    if "server_type" in params and not isinstance(params["server_type"], str):
        raise InvalidParameterError(
            "Bad parameter: server_type must be an str"
        )
    if "ssl" in params and not isinstance(params["ssl"], str):
        raise InvalidParameterError("Bad parameter: ssl must be an str")
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    if "wasabi_access_key" in params and not isinstance(
        params["wasabi_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: wasabi_access_key must be an str"
        )
    if "wasabi_bucket" in params and not isinstance(
        params["wasabi_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: wasabi_bucket must be an str"
        )
    if "wasabi_region" in params and not isinstance(
        params["wasabi_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: wasabi_region must be an str"
        )
    response, options = Api.send_request(
        "POST", "/remote_servers", params, options
    )
    return RemoteServer(response.data, options)


# Post local changes, check in, and download configuration file (used by some Remote Server integrations, such as the Files.com Agent)
#
# Parameters:
#   api_token - string - Files Agent API Token
#   permission_set - string - The permission set for the agent ['read_write', 'read_only', 'write_only']
#   root - string - The root directory for the agent
#   hostname - string
#   port - int64 - Incoming port for files agent connections
#   status - string - either running or shutdown
#   config_version - string - agent config version
#   private_key - string - The private key for the agent
#   public_key - string - public key
#   server_host_key - string
#   subdomain - string - Files.com subdomain site name
def configuration_file(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "api_token" in params and not isinstance(params["api_token"], str):
        raise InvalidParameterError("Bad parameter: api_token must be an str")
    if "permission_set" in params and not isinstance(
        params["permission_set"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: permission_set must be an str"
        )
    if "root" in params and not isinstance(params["root"], str):
        raise InvalidParameterError("Bad parameter: root must be an str")
    if "hostname" in params and not isinstance(params["hostname"], str):
        raise InvalidParameterError("Bad parameter: hostname must be an str")
    if "port" in params and not isinstance(params["port"], int):
        raise InvalidParameterError("Bad parameter: port must be an int")
    if "status" in params and not isinstance(params["status"], str):
        raise InvalidParameterError("Bad parameter: status must be an str")
    if "config_version" in params and not isinstance(
        params["config_version"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: config_version must be an str"
        )
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError(
            "Bad parameter: private_key must be an str"
        )
    if "public_key" in params and not isinstance(params["public_key"], str):
        raise InvalidParameterError("Bad parameter: public_key must be an str")
    if "server_host_key" in params and not isinstance(
        params["server_host_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: server_host_key must be an str"
        )
    if "subdomain" in params and not isinstance(params["subdomain"], str):
        raise InvalidParameterError("Bad parameter: subdomain must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "POST",
        "/remote_servers/{id}/configuration_file".format(id=params["id"]),
        params,
        options,
    )
    return RemoteServerConfigurationFile(response.data, options)


# Parameters:
#   password - string - Password, if needed.
#   private_key - string - Private key, if needed.
#   private_key_passphrase - string - Passphrase for private key if needed.
#   reset_authentication - boolean - Reset authenticated account?
#   ssl_certificate - string - SSL client certificate.
#   aws_secret_key - string - AWS: secret key.
#   azure_blob_storage_access_key - string - Azure Blob Storage: Access Key
#   azure_blob_storage_sas_token - string - Azure Blob Storage: Shared Access Signature (SAS) token
#   azure_files_storage_access_key - string - Azure File Storage: Access Key
#   azure_files_storage_sas_token - string - Azure File Storage: Shared Access Signature (SAS) token
#   backblaze_b2_application_key - string - Backblaze B2 Cloud Storage: applicationKey
#   backblaze_b2_key_id - string - Backblaze B2 Cloud Storage: keyID
#   cloudflare_secret_key - string - Cloudflare: Secret Key
#   filebase_secret_key - string - Filebase: Secret Key
#   google_cloud_storage_credentials_json - string - Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
#   google_cloud_storage_s3_compatible_secret_key - string - Google Cloud Storage: S3-compatible secret key
#   linode_secret_key - string - Linode: Secret Key
#   rackspace_api_key - string - Rackspace: API key from the Rackspace Cloud Control Panel
#   s3_compatible_secret_key - string - S3-compatible: Secret Key
#   wasabi_secret_key - string - Wasabi: Secret Key
#   aws_access_key - string - AWS Access Key.
#   azure_blob_storage_account - string - Azure Blob Storage: Account name
#   azure_blob_storage_container - string - Azure Blob Storage: Container name
#   azure_blob_storage_dns_suffix - string - Azure Blob Storage: Custom DNS suffix
#   azure_blob_storage_hierarchical_namespace - boolean - Azure Blob Storage: Does the storage account has hierarchical namespace feature enabled?
#   azure_files_storage_account - string - Azure Files: Storage Account name
#   azure_files_storage_dns_suffix - string - Azure Files: Custom DNS suffix
#   azure_files_storage_share_name - string - Azure Files:  Storage Share name
#   backblaze_b2_bucket - string - Backblaze B2 Cloud Storage: Bucket name
#   backblaze_b2_s3_endpoint - string - Backblaze B2 Cloud Storage: S3 Endpoint
#   cloudflare_access_key - string - Cloudflare: Access Key.
#   cloudflare_bucket - string - Cloudflare: Bucket name
#   cloudflare_endpoint - string - Cloudflare: endpoint
#   dropbox_teams - boolean - Dropbox: If true, list Team folders in root?
#   enable_dedicated_ips - boolean - `true` if remote server only accepts connections from dedicated IPs
#   filebase_access_key - string - Filebase: Access Key.
#   filebase_bucket - string - Filebase: Bucket name
#   files_agent_permission_set - string - Local permissions for files agent. read_only, write_only, or read_write
#   files_agent_root - string - Agent local root path
#   files_agent_version - string - Files Agent version
#   google_cloud_storage_bucket - string - Google Cloud Storage: Bucket Name
#   google_cloud_storage_project_id - string - Google Cloud Storage: Project ID
#   google_cloud_storage_s3_compatible_access_key - string - Google Cloud Storage: S3-compatible Access Key.
#   hostname - string - Hostname or IP address
#   linode_access_key - string - Linode: Access Key
#   linode_bucket - string - Linode: Bucket name
#   linode_region - string - Linode: region
#   max_connections - int64 - Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
#   name - string - Internal name for your reference
#   one_drive_account_type - string - OneDrive: Either personal or business_other account types
#   pin_to_site_region - boolean - If true, we will ensure that all communications with this remote server are made through the primary region of the site.  This setting can also be overridden by a site-wide setting which will force it to true.
#   port - int64 - Port for remote server.  Not needed for S3.
#   rackspace_container - string - Rackspace: The name of the container (top level directory) where files will sync.
#   rackspace_region - string - Rackspace: Three letter code for Rackspace region. See https://support.rackspace.com/how-to/about-regions/
#   rackspace_username - string - Rackspace: username used to login to the Rackspace Cloud Control Panel.
#   s3_bucket - string - S3 bucket name
#   s3_compatible_access_key - string - S3-compatible: Access Key
#   s3_compatible_bucket - string - S3-compatible: Bucket name
#   s3_compatible_endpoint - string - S3-compatible: endpoint
#   s3_compatible_region - string - S3-compatible: region
#   s3_region - string - S3 region
#   server_certificate - string - Remote server certificate
#   server_host_key - string - Remote server SSH Host Key. If provided, we will require that the server host key matches the provided key. Uses OpenSSH format similar to what would go into ~/.ssh/known_hosts
#   server_type - string - Remote server type.
#   ssl - string - Should we require SSL?
#   username - string - Remote server username.  Not needed for S3 buckets.
#   wasabi_access_key - string - Wasabi: Access Key.
#   wasabi_bucket - string - Wasabi: Bucket name
#   wasabi_region - string - Wasabi: Region
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError(
            "Bad parameter: private_key must be an str"
        )
    if "private_key_passphrase" in params and not isinstance(
        params["private_key_passphrase"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: private_key_passphrase must be an str"
        )
    if "ssl_certificate" in params and not isinstance(
        params["ssl_certificate"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ssl_certificate must be an str"
        )
    if "aws_secret_key" in params and not isinstance(
        params["aws_secret_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: aws_secret_key must be an str"
        )
    if "azure_blob_storage_access_key" in params and not isinstance(
        params["azure_blob_storage_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_blob_storage_access_key must be an str"
        )
    if "azure_blob_storage_sas_token" in params and not isinstance(
        params["azure_blob_storage_sas_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_blob_storage_sas_token must be an str"
        )
    if "azure_files_storage_access_key" in params and not isinstance(
        params["azure_files_storage_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_files_storage_access_key must be an str"
        )
    if "azure_files_storage_sas_token" in params and not isinstance(
        params["azure_files_storage_sas_token"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_files_storage_sas_token must be an str"
        )
    if "backblaze_b2_application_key" in params and not isinstance(
        params["backblaze_b2_application_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: backblaze_b2_application_key must be an str"
        )
    if "backblaze_b2_key_id" in params and not isinstance(
        params["backblaze_b2_key_id"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: backblaze_b2_key_id must be an str"
        )
    if "cloudflare_secret_key" in params and not isinstance(
        params["cloudflare_secret_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: cloudflare_secret_key must be an str"
        )
    if "filebase_secret_key" in params and not isinstance(
        params["filebase_secret_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: filebase_secret_key must be an str"
        )
    if "google_cloud_storage_credentials_json" in params and not isinstance(
        params["google_cloud_storage_credentials_json"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: google_cloud_storage_credentials_json must be an str"
        )
    if (
        "google_cloud_storage_s3_compatible_secret_key" in params
        and not isinstance(
            params["google_cloud_storage_s3_compatible_secret_key"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: google_cloud_storage_s3_compatible_secret_key must be an str"
        )
    if "linode_secret_key" in params and not isinstance(
        params["linode_secret_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: linode_secret_key must be an str"
        )
    if "rackspace_api_key" in params and not isinstance(
        params["rackspace_api_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: rackspace_api_key must be an str"
        )
    if "s3_compatible_secret_key" in params and not isinstance(
        params["s3_compatible_secret_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: s3_compatible_secret_key must be an str"
        )
    if "wasabi_secret_key" in params and not isinstance(
        params["wasabi_secret_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: wasabi_secret_key must be an str"
        )
    if "aws_access_key" in params and not isinstance(
        params["aws_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: aws_access_key must be an str"
        )
    if "azure_blob_storage_account" in params and not isinstance(
        params["azure_blob_storage_account"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_blob_storage_account must be an str"
        )
    if "azure_blob_storage_container" in params and not isinstance(
        params["azure_blob_storage_container"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_blob_storage_container must be an str"
        )
    if "azure_blob_storage_dns_suffix" in params and not isinstance(
        params["azure_blob_storage_dns_suffix"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_blob_storage_dns_suffix must be an str"
        )
    if "azure_files_storage_account" in params and not isinstance(
        params["azure_files_storage_account"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_files_storage_account must be an str"
        )
    if "azure_files_storage_dns_suffix" in params and not isinstance(
        params["azure_files_storage_dns_suffix"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_files_storage_dns_suffix must be an str"
        )
    if "azure_files_storage_share_name" in params and not isinstance(
        params["azure_files_storage_share_name"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_files_storage_share_name must be an str"
        )
    if "backblaze_b2_bucket" in params and not isinstance(
        params["backblaze_b2_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: backblaze_b2_bucket must be an str"
        )
    if "backblaze_b2_s3_endpoint" in params and not isinstance(
        params["backblaze_b2_s3_endpoint"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: backblaze_b2_s3_endpoint must be an str"
        )
    if "cloudflare_access_key" in params and not isinstance(
        params["cloudflare_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: cloudflare_access_key must be an str"
        )
    if "cloudflare_bucket" in params and not isinstance(
        params["cloudflare_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: cloudflare_bucket must be an str"
        )
    if "cloudflare_endpoint" in params and not isinstance(
        params["cloudflare_endpoint"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: cloudflare_endpoint must be an str"
        )
    if "filebase_access_key" in params and not isinstance(
        params["filebase_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: filebase_access_key must be an str"
        )
    if "filebase_bucket" in params and not isinstance(
        params["filebase_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: filebase_bucket must be an str"
        )
    if "files_agent_permission_set" in params and not isinstance(
        params["files_agent_permission_set"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: files_agent_permission_set must be an str"
        )
    if "files_agent_root" in params and not isinstance(
        params["files_agent_root"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: files_agent_root must be an str"
        )
    if "files_agent_version" in params and not isinstance(
        params["files_agent_version"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: files_agent_version must be an str"
        )
    if "google_cloud_storage_bucket" in params and not isinstance(
        params["google_cloud_storage_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: google_cloud_storage_bucket must be an str"
        )
    if "google_cloud_storage_project_id" in params and not isinstance(
        params["google_cloud_storage_project_id"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: google_cloud_storage_project_id must be an str"
        )
    if (
        "google_cloud_storage_s3_compatible_access_key" in params
        and not isinstance(
            params["google_cloud_storage_s3_compatible_access_key"], str
        )
    ):
        raise InvalidParameterError(
            "Bad parameter: google_cloud_storage_s3_compatible_access_key must be an str"
        )
    if "hostname" in params and not isinstance(params["hostname"], str):
        raise InvalidParameterError("Bad parameter: hostname must be an str")
    if "linode_access_key" in params and not isinstance(
        params["linode_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: linode_access_key must be an str"
        )
    if "linode_bucket" in params and not isinstance(
        params["linode_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: linode_bucket must be an str"
        )
    if "linode_region" in params and not isinstance(
        params["linode_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: linode_region must be an str"
        )
    if "max_connections" in params and not isinstance(
        params["max_connections"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: max_connections must be an int"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "one_drive_account_type" in params and not isinstance(
        params["one_drive_account_type"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: one_drive_account_type must be an str"
        )
    if "port" in params and not isinstance(params["port"], int):
        raise InvalidParameterError("Bad parameter: port must be an int")
    if "rackspace_container" in params and not isinstance(
        params["rackspace_container"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: rackspace_container must be an str"
        )
    if "rackspace_region" in params and not isinstance(
        params["rackspace_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: rackspace_region must be an str"
        )
    if "rackspace_username" in params and not isinstance(
        params["rackspace_username"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: rackspace_username must be an str"
        )
    if "s3_bucket" in params and not isinstance(params["s3_bucket"], str):
        raise InvalidParameterError("Bad parameter: s3_bucket must be an str")
    if "s3_compatible_access_key" in params and not isinstance(
        params["s3_compatible_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: s3_compatible_access_key must be an str"
        )
    if "s3_compatible_bucket" in params and not isinstance(
        params["s3_compatible_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: s3_compatible_bucket must be an str"
        )
    if "s3_compatible_endpoint" in params and not isinstance(
        params["s3_compatible_endpoint"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: s3_compatible_endpoint must be an str"
        )
    if "s3_compatible_region" in params and not isinstance(
        params["s3_compatible_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: s3_compatible_region must be an str"
        )
    if "s3_region" in params and not isinstance(params["s3_region"], str):
        raise InvalidParameterError("Bad parameter: s3_region must be an str")
    if "server_certificate" in params and not isinstance(
        params["server_certificate"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: server_certificate must be an str"
        )
    if "server_host_key" in params and not isinstance(
        params["server_host_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: server_host_key must be an str"
        )
    if "server_type" in params and not isinstance(params["server_type"], str):
        raise InvalidParameterError(
            "Bad parameter: server_type must be an str"
        )
    if "ssl" in params and not isinstance(params["ssl"], str):
        raise InvalidParameterError("Bad parameter: ssl must be an str")
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    if "wasabi_access_key" in params and not isinstance(
        params["wasabi_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: wasabi_access_key must be an str"
        )
    if "wasabi_bucket" in params and not isinstance(
        params["wasabi_bucket"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: wasabi_bucket must be an str"
        )
    if "wasabi_region" in params and not isinstance(
        params["wasabi_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: wasabi_region must be an str"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/remote_servers/{id}".format(id=params["id"]),
        params,
        options,
    )
    return RemoteServer(response.data, options)


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
        "/remote_servers/{id}".format(id=params["id"]),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return RemoteServer(*args, **kwargs)
