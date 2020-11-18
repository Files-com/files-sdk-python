import datetime
from files_sdk.models.file import File
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class RemoteServer:
    default_attributes = {
        'id': None,     # int64 - Remote server ID
        'authentication_method': None,     # string - Type of authentication method
        'hostname': None,     # string - Hostname or IP address
        'name': None,     # string - Internal name for your reference
        'port': None,     # int64 - Port for remote server.  Not needed for S3.
        'max_connections': None,     # int64 - Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
        's3_bucket': None,     # string - S3 bucket name
        's3_region': None,     # string - S3 region
        'server_certificate': None,     # string - Remote server certificate
        'server_host_key': None,     # string - Remote server SSH Host Key. If provided, we will require that the server host key matches the provided key. Uses OpenSSH format similar to what would go into ~/.ssh/known_hosts
        'server_type': None,     # string - Remote server type.
        'ssl': None,     # string - Should we require SSL?
        'username': None,     # string - Remote server username.  Not needed for S3 buckets.
        'google_cloud_storage_bucket': None,     # string - Google Cloud Storage bucket name
        'google_cloud_storage_project_id': None,     # string - Google Cloud Project ID
        'backblaze_b2_s3_endpoint': None,     # string - Backblaze B2 Cloud Storage S3 Endpoint
        'backblaze_b2_bucket': None,     # string - Backblaze B2 Cloud Storage Bucket name
        'wasabi_bucket': None,     # string - Wasabi region
        'wasabi_region': None,     # string - Wasabi Bucket name
        'rackspace_username': None,     # string - Rackspace username used to login to the Rackspace Cloud Control Panel.
        'rackspace_region': None,     # string - Three letter airport code for Rackspace region. See https://support.rackspace.com/how-to/about-regions/
        'rackspace_container': None,     # string - The name of the container (top level directory) where files will sync.
        'auth_setup_link': None,     # string - Returns link to login with an Oauth provider
        'auth_status': None,     # string - Either `in_setup` or `complete`
        'auth_account_name': None,     # string - Describes the authorized account
        'one_drive_account_type': None,     # string - Either personal or business_other account types
        'azure_blob_storage_account': None,     # string - Azure Blob Storage Account name
        'azure_blob_storage_container': None,     # string - Azure Blob Storage Container name
        'aws_access_key': None,     # string - AWS Access Key.
        'aws_secret_key': None,     # string - AWS secret key.
        'password': None,     # string - Password if needed.
        'private_key': None,     # string - Private key if needed.
        'ssl_certificate': None,     # string - SSL client certificate.
        'google_cloud_storage_credentials_json': None,     # string - A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
        'wasabi_access_key': None,     # string - Wasabi access key.
        'wasabi_secret_key': None,     # string - Wasabi secret key.
        'backblaze_b2_key_id': None,     # string - Backblaze B2 Cloud Storage keyID.
        'backblaze_b2_application_key': None,     # string - Backblaze B2 Cloud Storage applicationKey.
        'rackspace_api_key': None,     # string - Rackspace API key from the Rackspace Cloud Control Panel.
        'reset_authentication': None,     # boolean - Reset authenticated account
        'azure_blob_storage_access_key': None,     # string - Azure Blob Storage secret key.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in RemoteServer.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in RemoteServer.default_attributes if getattr(self, k, None) is not None}

    # Parameters:
    #   aws_access_key - string - AWS Access Key.
    #   aws_secret_key - string - AWS secret key.
    #   password - string - Password if needed.
    #   private_key - string - Private key if needed.
    #   ssl_certificate - string - SSL client certificate.
    #   google_cloud_storage_credentials_json - string - A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
    #   wasabi_access_key - string - Wasabi access key.
    #   wasabi_secret_key - string - Wasabi secret key.
    #   backblaze_b2_key_id - string - Backblaze B2 Cloud Storage keyID.
    #   backblaze_b2_application_key - string - Backblaze B2 Cloud Storage applicationKey.
    #   rackspace_api_key - string - Rackspace API key from the Rackspace Cloud Control Panel.
    #   reset_authentication - boolean - Reset authenticated account
    #   azure_blob_storage_access_key - string - Azure Blob Storage secret key.
    #   hostname - string - Hostname or IP address
    #   name - string - Internal name for your reference
    #   max_connections - int64 - Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
    #   port - int64 - Port for remote server.  Not needed for S3.
    #   s3_bucket - string - S3 bucket name
    #   s3_region - string - S3 region
    #   server_certificate - string - Remote server certificate
    #   server_host_key - string - Remote server SSH Host Key. If provided, we will require that the server host key matches the provided key. Uses OpenSSH format similar to what would go into ~/.ssh/known_hosts
    #   server_type - string - Remote server type.
    #   ssl - string - Should we require SSL?
    #   username - string - Remote server username.  Not needed for S3 buckets.
    #   google_cloud_storage_bucket - string - Google Cloud Storage bucket name
    #   google_cloud_storage_project_id - string - Google Cloud Project ID
    #   backblaze_b2_bucket - string - Backblaze B2 Cloud Storage Bucket name
    #   backblaze_b2_s3_endpoint - string - Backblaze B2 Cloud Storage S3 Endpoint
    #   wasabi_bucket - string - Wasabi region
    #   wasabi_region - string - Wasabi Bucket name
    #   rackspace_username - string - Rackspace username used to login to the Rackspace Cloud Control Panel.
    #   rackspace_region - string - Three letter airport code for Rackspace region. See https://support.rackspace.com/how-to/about-regions/
    #   rackspace_container - string - The name of the container (top level directory) where files will sync.
    #   one_drive_account_type - string - Either personal or business_other account types
    #   azure_blob_storage_account - string - Azure Blob Storage Account name
    #   azure_blob_storage_container - string - Azure Blob Storage Container name
    def update(self, params = None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "aws_access_key" in params and not isinstance(params["aws_access_key"], str):
            raise InvalidParameterError("Bad parameter: aws_access_key must be an str")
        if "aws_secret_key" in params and not isinstance(params["aws_secret_key"], str):
            raise InvalidParameterError("Bad parameter: aws_secret_key must be an str")
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError("Bad parameter: password must be an str")
        if "private_key" in params and not isinstance(params["private_key"], str):
            raise InvalidParameterError("Bad parameter: private_key must be an str")
        if "ssl_certificate" in params and not isinstance(params["ssl_certificate"], str):
            raise InvalidParameterError("Bad parameter: ssl_certificate must be an str")
        if "google_cloud_storage_credentials_json" in params and not isinstance(params["google_cloud_storage_credentials_json"], str):
            raise InvalidParameterError("Bad parameter: google_cloud_storage_credentials_json must be an str")
        if "wasabi_access_key" in params and not isinstance(params["wasabi_access_key"], str):
            raise InvalidParameterError("Bad parameter: wasabi_access_key must be an str")
        if "wasabi_secret_key" in params and not isinstance(params["wasabi_secret_key"], str):
            raise InvalidParameterError("Bad parameter: wasabi_secret_key must be an str")
        if "backblaze_b2_key_id" in params and not isinstance(params["backblaze_b2_key_id"], str):
            raise InvalidParameterError("Bad parameter: backblaze_b2_key_id must be an str")
        if "backblaze_b2_application_key" in params and not isinstance(params["backblaze_b2_application_key"], str):
            raise InvalidParameterError("Bad parameter: backblaze_b2_application_key must be an str")
        if "rackspace_api_key" in params and not isinstance(params["rackspace_api_key"], str):
            raise InvalidParameterError("Bad parameter: rackspace_api_key must be an str")
        if "azure_blob_storage_access_key" in params and not isinstance(params["azure_blob_storage_access_key"], str):
            raise InvalidParameterError("Bad parameter: azure_blob_storage_access_key must be an str")
        if "hostname" in params and not isinstance(params["hostname"], str):
            raise InvalidParameterError("Bad parameter: hostname must be an str")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "max_connections" in params and not isinstance(params["max_connections"], int):
            raise InvalidParameterError("Bad parameter: max_connections must be an int")
        if "port" in params and not isinstance(params["port"], int):
            raise InvalidParameterError("Bad parameter: port must be an int")
        if "s3_bucket" in params and not isinstance(params["s3_bucket"], str):
            raise InvalidParameterError("Bad parameter: s3_bucket must be an str")
        if "s3_region" in params and not isinstance(params["s3_region"], str):
            raise InvalidParameterError("Bad parameter: s3_region must be an str")
        if "server_certificate" in params and not isinstance(params["server_certificate"], str):
            raise InvalidParameterError("Bad parameter: server_certificate must be an str")
        if "server_host_key" in params and not isinstance(params["server_host_key"], str):
            raise InvalidParameterError("Bad parameter: server_host_key must be an str")
        if "server_type" in params and not isinstance(params["server_type"], str):
            raise InvalidParameterError("Bad parameter: server_type must be an str")
        if "ssl" in params and not isinstance(params["ssl"], str):
            raise InvalidParameterError("Bad parameter: ssl must be an str")
        if "username" in params and not isinstance(params["username"], str):
            raise InvalidParameterError("Bad parameter: username must be an str")
        if "google_cloud_storage_bucket" in params and not isinstance(params["google_cloud_storage_bucket"], str):
            raise InvalidParameterError("Bad parameter: google_cloud_storage_bucket must be an str")
        if "google_cloud_storage_project_id" in params and not isinstance(params["google_cloud_storage_project_id"], str):
            raise InvalidParameterError("Bad parameter: google_cloud_storage_project_id must be an str")
        if "backblaze_b2_bucket" in params and not isinstance(params["backblaze_b2_bucket"], str):
            raise InvalidParameterError("Bad parameter: backblaze_b2_bucket must be an str")
        if "backblaze_b2_s3_endpoint" in params and not isinstance(params["backblaze_b2_s3_endpoint"], str):
            raise InvalidParameterError("Bad parameter: backblaze_b2_s3_endpoint must be an str")
        if "wasabi_bucket" in params and not isinstance(params["wasabi_bucket"], str):
            raise InvalidParameterError("Bad parameter: wasabi_bucket must be an str")
        if "wasabi_region" in params and not isinstance(params["wasabi_region"], str):
            raise InvalidParameterError("Bad parameter: wasabi_region must be an str")
        if "rackspace_username" in params and not isinstance(params["rackspace_username"], str):
            raise InvalidParameterError("Bad parameter: rackspace_username must be an str")
        if "rackspace_region" in params and not isinstance(params["rackspace_region"], str):
            raise InvalidParameterError("Bad parameter: rackspace_region must be an str")
        if "rackspace_container" in params and not isinstance(params["rackspace_container"], str):
            raise InvalidParameterError("Bad parameter: rackspace_container must be an str")
        if "one_drive_account_type" in params and not isinstance(params["one_drive_account_type"], str):
            raise InvalidParameterError("Bad parameter: one_drive_account_type must be an str")
        if "azure_blob_storage_account" in params and not isinstance(params["azure_blob_storage_account"], str):
            raise InvalidParameterError("Bad parameter: azure_blob_storage_account must be an str")
        if "azure_blob_storage_container" in params and not isinstance(params["azure_blob_storage_container"], str):
            raise InvalidParameterError("Bad parameter: azure_blob_storage_container must be an str")
        response, _options = Api.send_request("PATCH", "/remote_servers/{id}".format(id=params['id']), params, self.options)
        return response.data

    def delete(self, params = None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        response, _options = Api.send_request("DELETE", "/remote_servers/{id}".format(id=params['id']), params, self.options)
        return response.data

    def destroy(self, params = None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
def list(params = None, options = None):
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(RemoteServer,"GET", "/remote_servers", params, options)

def all(params = None, options = None):
    list(params, options)

# Parameters:
#   id (required) - int64 - Remote Server ID.
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
    response, options = Api.send_request("GET", "/remote_servers/{id}".format(id=params['id']), params, options)
    return RemoteServer(response.data, options)

def get(id, params = None, options = None):
    find(id, params, options)

# Parameters:
#   remote_server_id - int64 - RemoteServer ID
#   root - string - Remote path to list
#   aws_access_key - string - AWS Access Key.
#   aws_secret_key - string - AWS secret key.
#   password - string - Password if needed.
#   private_key - string - Private key if needed.
#   ssl_certificate - string - SSL client certificate.
#   google_cloud_storage_credentials_json - string - A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
#   wasabi_access_key - string - Wasabi access key.
#   wasabi_secret_key - string - Wasabi secret key.
#   backblaze_b2_key_id - string - Backblaze B2 Cloud Storage keyID.
#   backblaze_b2_application_key - string - Backblaze B2 Cloud Storage applicationKey.
#   rackspace_api_key - string - Rackspace API key from the Rackspace Cloud Control Panel.
#   reset_authentication - boolean - Reset authenticated account
#   azure_blob_storage_access_key - string - Azure Blob Storage secret key.
#   hostname - string
#   name - string
#   max_connections - int64
#   port - int64
#   s3_bucket - string
#   s3_region - string
#   server_certificate - string
#   server_host_key - string
#   server_type - string
#   ssl - string
#   username - string
#   google_cloud_storage_bucket - string
#   google_cloud_storage_project_id - string
#   backblaze_b2_bucket - string
#   backblaze_b2_s3_endpoint - string
#   wasabi_bucket - string
#   wasabi_region - string
#   rackspace_username - string
#   rackspace_region - string
#   rackspace_container - string
#   one_drive_account_type - string
#   azure_blob_storage_account - string
#   azure_blob_storage_container - string
def list_for_testing(params = None, options = None):
    if "remote_server_id" in params and not isinstance(params["remote_server_id"], int):
        raise InvalidParameterError("Bad parameter: remote_server_id must be an int")
    if "root" in params and not isinstance(params["root"], str):
        raise InvalidParameterError("Bad parameter: root must be an str")
    if "aws_access_key" in params and not isinstance(params["aws_access_key"], str):
        raise InvalidParameterError("Bad parameter: aws_access_key must be an str")
    if "aws_secret_key" in params and not isinstance(params["aws_secret_key"], str):
        raise InvalidParameterError("Bad parameter: aws_secret_key must be an str")
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError("Bad parameter: private_key must be an str")
    if "ssl_certificate" in params and not isinstance(params["ssl_certificate"], str):
        raise InvalidParameterError("Bad parameter: ssl_certificate must be an str")
    if "google_cloud_storage_credentials_json" in params and not isinstance(params["google_cloud_storage_credentials_json"], str):
        raise InvalidParameterError("Bad parameter: google_cloud_storage_credentials_json must be an str")
    if "wasabi_access_key" in params and not isinstance(params["wasabi_access_key"], str):
        raise InvalidParameterError("Bad parameter: wasabi_access_key must be an str")
    if "wasabi_secret_key" in params and not isinstance(params["wasabi_secret_key"], str):
        raise InvalidParameterError("Bad parameter: wasabi_secret_key must be an str")
    if "backblaze_b2_key_id" in params and not isinstance(params["backblaze_b2_key_id"], str):
        raise InvalidParameterError("Bad parameter: backblaze_b2_key_id must be an str")
    if "backblaze_b2_application_key" in params and not isinstance(params["backblaze_b2_application_key"], str):
        raise InvalidParameterError("Bad parameter: backblaze_b2_application_key must be an str")
    if "rackspace_api_key" in params and not isinstance(params["rackspace_api_key"], str):
        raise InvalidParameterError("Bad parameter: rackspace_api_key must be an str")
    if "azure_blob_storage_access_key" in params and not isinstance(params["azure_blob_storage_access_key"], str):
        raise InvalidParameterError("Bad parameter: azure_blob_storage_access_key must be an str")
    if "hostname" in params and not isinstance(params["hostname"], str):
        raise InvalidParameterError("Bad parameter: hostname must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "max_connections" in params and not isinstance(params["max_connections"], int):
        raise InvalidParameterError("Bad parameter: max_connections must be an int")
    if "port" in params and not isinstance(params["port"], int):
        raise InvalidParameterError("Bad parameter: port must be an int")
    if "s3_bucket" in params and not isinstance(params["s3_bucket"], str):
        raise InvalidParameterError("Bad parameter: s3_bucket must be an str")
    if "s3_region" in params and not isinstance(params["s3_region"], str):
        raise InvalidParameterError("Bad parameter: s3_region must be an str")
    if "server_certificate" in params and not isinstance(params["server_certificate"], str):
        raise InvalidParameterError("Bad parameter: server_certificate must be an str")
    if "server_host_key" in params and not isinstance(params["server_host_key"], str):
        raise InvalidParameterError("Bad parameter: server_host_key must be an str")
    if "server_type" in params and not isinstance(params["server_type"], str):
        raise InvalidParameterError("Bad parameter: server_type must be an str")
    if "ssl" in params and not isinstance(params["ssl"], str):
        raise InvalidParameterError("Bad parameter: ssl must be an str")
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    if "google_cloud_storage_bucket" in params and not isinstance(params["google_cloud_storage_bucket"], str):
        raise InvalidParameterError("Bad parameter: google_cloud_storage_bucket must be an str")
    if "google_cloud_storage_project_id" in params and not isinstance(params["google_cloud_storage_project_id"], str):
        raise InvalidParameterError("Bad parameter: google_cloud_storage_project_id must be an str")
    if "backblaze_b2_bucket" in params and not isinstance(params["backblaze_b2_bucket"], str):
        raise InvalidParameterError("Bad parameter: backblaze_b2_bucket must be an str")
    if "backblaze_b2_s3_endpoint" in params and not isinstance(params["backblaze_b2_s3_endpoint"], str):
        raise InvalidParameterError("Bad parameter: backblaze_b2_s3_endpoint must be an str")
    if "wasabi_bucket" in params and not isinstance(params["wasabi_bucket"], str):
        raise InvalidParameterError("Bad parameter: wasabi_bucket must be an str")
    if "wasabi_region" in params and not isinstance(params["wasabi_region"], str):
        raise InvalidParameterError("Bad parameter: wasabi_region must be an str")
    if "rackspace_username" in params and not isinstance(params["rackspace_username"], str):
        raise InvalidParameterError("Bad parameter: rackspace_username must be an str")
    if "rackspace_region" in params and not isinstance(params["rackspace_region"], str):
        raise InvalidParameterError("Bad parameter: rackspace_region must be an str")
    if "rackspace_container" in params and not isinstance(params["rackspace_container"], str):
        raise InvalidParameterError("Bad parameter: rackspace_container must be an str")
    if "one_drive_account_type" in params and not isinstance(params["one_drive_account_type"], str):
        raise InvalidParameterError("Bad parameter: one_drive_account_type must be an str")
    if "azure_blob_storage_account" in params and not isinstance(params["azure_blob_storage_account"], str):
        raise InvalidParameterError("Bad parameter: azure_blob_storage_account must be an str")
    if "azure_blob_storage_container" in params and not isinstance(params["azure_blob_storage_container"], str):
        raise InvalidParameterError("Bad parameter: azure_blob_storage_container must be an str")
    response, options = Api.send_request("GET", "/remote_servers/list_for_testing", params, options)
    return File(response.data, options)

# Parameters:
#   aws_access_key - string - AWS Access Key.
#   aws_secret_key - string - AWS secret key.
#   password - string - Password if needed.
#   private_key - string - Private key if needed.
#   ssl_certificate - string - SSL client certificate.
#   google_cloud_storage_credentials_json - string - A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
#   wasabi_access_key - string - Wasabi access key.
#   wasabi_secret_key - string - Wasabi secret key.
#   backblaze_b2_key_id - string - Backblaze B2 Cloud Storage keyID.
#   backblaze_b2_application_key - string - Backblaze B2 Cloud Storage applicationKey.
#   rackspace_api_key - string - Rackspace API key from the Rackspace Cloud Control Panel.
#   reset_authentication - boolean - Reset authenticated account
#   azure_blob_storage_access_key - string - Azure Blob Storage secret key.
#   hostname - string - Hostname or IP address
#   name - string - Internal name for your reference
#   max_connections - int64 - Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
#   port - int64 - Port for remote server.  Not needed for S3.
#   s3_bucket - string - S3 bucket name
#   s3_region - string - S3 region
#   server_certificate - string - Remote server certificate
#   server_host_key - string - Remote server SSH Host Key. If provided, we will require that the server host key matches the provided key. Uses OpenSSH format similar to what would go into ~/.ssh/known_hosts
#   server_type - string - Remote server type.
#   ssl - string - Should we require SSL?
#   username - string - Remote server username.  Not needed for S3 buckets.
#   google_cloud_storage_bucket - string - Google Cloud Storage bucket name
#   google_cloud_storage_project_id - string - Google Cloud Project ID
#   backblaze_b2_bucket - string - Backblaze B2 Cloud Storage Bucket name
#   backblaze_b2_s3_endpoint - string - Backblaze B2 Cloud Storage S3 Endpoint
#   wasabi_bucket - string - Wasabi region
#   wasabi_region - string - Wasabi Bucket name
#   rackspace_username - string - Rackspace username used to login to the Rackspace Cloud Control Panel.
#   rackspace_region - string - Three letter airport code for Rackspace region. See https://support.rackspace.com/how-to/about-regions/
#   rackspace_container - string - The name of the container (top level directory) where files will sync.
#   one_drive_account_type - string - Either personal or business_other account types
#   azure_blob_storage_account - string - Azure Blob Storage Account name
#   azure_blob_storage_container - string - Azure Blob Storage Container name
def create(params = None, options = None):
    if "aws_access_key" in params and not isinstance(params["aws_access_key"], str):
        raise InvalidParameterError("Bad parameter: aws_access_key must be an str")
    if "aws_secret_key" in params and not isinstance(params["aws_secret_key"], str):
        raise InvalidParameterError("Bad parameter: aws_secret_key must be an str")
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError("Bad parameter: private_key must be an str")
    if "ssl_certificate" in params and not isinstance(params["ssl_certificate"], str):
        raise InvalidParameterError("Bad parameter: ssl_certificate must be an str")
    if "google_cloud_storage_credentials_json" in params and not isinstance(params["google_cloud_storage_credentials_json"], str):
        raise InvalidParameterError("Bad parameter: google_cloud_storage_credentials_json must be an str")
    if "wasabi_access_key" in params and not isinstance(params["wasabi_access_key"], str):
        raise InvalidParameterError("Bad parameter: wasabi_access_key must be an str")
    if "wasabi_secret_key" in params and not isinstance(params["wasabi_secret_key"], str):
        raise InvalidParameterError("Bad parameter: wasabi_secret_key must be an str")
    if "backblaze_b2_key_id" in params and not isinstance(params["backblaze_b2_key_id"], str):
        raise InvalidParameterError("Bad parameter: backblaze_b2_key_id must be an str")
    if "backblaze_b2_application_key" in params and not isinstance(params["backblaze_b2_application_key"], str):
        raise InvalidParameterError("Bad parameter: backblaze_b2_application_key must be an str")
    if "rackspace_api_key" in params and not isinstance(params["rackspace_api_key"], str):
        raise InvalidParameterError("Bad parameter: rackspace_api_key must be an str")
    if "azure_blob_storage_access_key" in params and not isinstance(params["azure_blob_storage_access_key"], str):
        raise InvalidParameterError("Bad parameter: azure_blob_storage_access_key must be an str")
    if "hostname" in params and not isinstance(params["hostname"], str):
        raise InvalidParameterError("Bad parameter: hostname must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "max_connections" in params and not isinstance(params["max_connections"], int):
        raise InvalidParameterError("Bad parameter: max_connections must be an int")
    if "port" in params and not isinstance(params["port"], int):
        raise InvalidParameterError("Bad parameter: port must be an int")
    if "s3_bucket" in params and not isinstance(params["s3_bucket"], str):
        raise InvalidParameterError("Bad parameter: s3_bucket must be an str")
    if "s3_region" in params and not isinstance(params["s3_region"], str):
        raise InvalidParameterError("Bad parameter: s3_region must be an str")
    if "server_certificate" in params and not isinstance(params["server_certificate"], str):
        raise InvalidParameterError("Bad parameter: server_certificate must be an str")
    if "server_host_key" in params and not isinstance(params["server_host_key"], str):
        raise InvalidParameterError("Bad parameter: server_host_key must be an str")
    if "server_type" in params and not isinstance(params["server_type"], str):
        raise InvalidParameterError("Bad parameter: server_type must be an str")
    if "ssl" in params and not isinstance(params["ssl"], str):
        raise InvalidParameterError("Bad parameter: ssl must be an str")
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    if "google_cloud_storage_bucket" in params and not isinstance(params["google_cloud_storage_bucket"], str):
        raise InvalidParameterError("Bad parameter: google_cloud_storage_bucket must be an str")
    if "google_cloud_storage_project_id" in params and not isinstance(params["google_cloud_storage_project_id"], str):
        raise InvalidParameterError("Bad parameter: google_cloud_storage_project_id must be an str")
    if "backblaze_b2_bucket" in params and not isinstance(params["backblaze_b2_bucket"], str):
        raise InvalidParameterError("Bad parameter: backblaze_b2_bucket must be an str")
    if "backblaze_b2_s3_endpoint" in params and not isinstance(params["backblaze_b2_s3_endpoint"], str):
        raise InvalidParameterError("Bad parameter: backblaze_b2_s3_endpoint must be an str")
    if "wasabi_bucket" in params and not isinstance(params["wasabi_bucket"], str):
        raise InvalidParameterError("Bad parameter: wasabi_bucket must be an str")
    if "wasabi_region" in params and not isinstance(params["wasabi_region"], str):
        raise InvalidParameterError("Bad parameter: wasabi_region must be an str")
    if "rackspace_username" in params and not isinstance(params["rackspace_username"], str):
        raise InvalidParameterError("Bad parameter: rackspace_username must be an str")
    if "rackspace_region" in params and not isinstance(params["rackspace_region"], str):
        raise InvalidParameterError("Bad parameter: rackspace_region must be an str")
    if "rackspace_container" in params and not isinstance(params["rackspace_container"], str):
        raise InvalidParameterError("Bad parameter: rackspace_container must be an str")
    if "one_drive_account_type" in params and not isinstance(params["one_drive_account_type"], str):
        raise InvalidParameterError("Bad parameter: one_drive_account_type must be an str")
    if "azure_blob_storage_account" in params and not isinstance(params["azure_blob_storage_account"], str):
        raise InvalidParameterError("Bad parameter: azure_blob_storage_account must be an str")
    if "azure_blob_storage_container" in params and not isinstance(params["azure_blob_storage_container"], str):
        raise InvalidParameterError("Bad parameter: azure_blob_storage_container must be an str")
    response, options = Api.send_request("POST", "/remote_servers", params, options)
    return RemoteServer(response.data, options)

# Parameters:
#   aws_access_key - string - AWS Access Key.
#   aws_secret_key - string - AWS secret key.
#   password - string - Password if needed.
#   private_key - string - Private key if needed.
#   ssl_certificate - string - SSL client certificate.
#   google_cloud_storage_credentials_json - string - A JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
#   wasabi_access_key - string - Wasabi access key.
#   wasabi_secret_key - string - Wasabi secret key.
#   backblaze_b2_key_id - string - Backblaze B2 Cloud Storage keyID.
#   backblaze_b2_application_key - string - Backblaze B2 Cloud Storage applicationKey.
#   rackspace_api_key - string - Rackspace API key from the Rackspace Cloud Control Panel.
#   reset_authentication - boolean - Reset authenticated account
#   azure_blob_storage_access_key - string - Azure Blob Storage secret key.
#   hostname - string - Hostname or IP address
#   name - string - Internal name for your reference
#   max_connections - int64 - Max number of parallel connections.  Ignored for S3 connections (we will parallelize these as much as possible).
#   port - int64 - Port for remote server.  Not needed for S3.
#   s3_bucket - string - S3 bucket name
#   s3_region - string - S3 region
#   server_certificate - string - Remote server certificate
#   server_host_key - string - Remote server SSH Host Key. If provided, we will require that the server host key matches the provided key. Uses OpenSSH format similar to what would go into ~/.ssh/known_hosts
#   server_type - string - Remote server type.
#   ssl - string - Should we require SSL?
#   username - string - Remote server username.  Not needed for S3 buckets.
#   google_cloud_storage_bucket - string - Google Cloud Storage bucket name
#   google_cloud_storage_project_id - string - Google Cloud Project ID
#   backblaze_b2_bucket - string - Backblaze B2 Cloud Storage Bucket name
#   backblaze_b2_s3_endpoint - string - Backblaze B2 Cloud Storage S3 Endpoint
#   wasabi_bucket - string - Wasabi region
#   wasabi_region - string - Wasabi Bucket name
#   rackspace_username - string - Rackspace username used to login to the Rackspace Cloud Control Panel.
#   rackspace_region - string - Three letter airport code for Rackspace region. See https://support.rackspace.com/how-to/about-regions/
#   rackspace_container - string - The name of the container (top level directory) where files will sync.
#   one_drive_account_type - string - Either personal or business_other account types
#   azure_blob_storage_account - string - Azure Blob Storage Account name
#   azure_blob_storage_container - string - Azure Blob Storage Container name
def update(id, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "aws_access_key" in params and not isinstance(params["aws_access_key"], str):
        raise InvalidParameterError("Bad parameter: aws_access_key must be an str")
    if "aws_secret_key" in params and not isinstance(params["aws_secret_key"], str):
        raise InvalidParameterError("Bad parameter: aws_secret_key must be an str")
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError("Bad parameter: private_key must be an str")
    if "ssl_certificate" in params and not isinstance(params["ssl_certificate"], str):
        raise InvalidParameterError("Bad parameter: ssl_certificate must be an str")
    if "google_cloud_storage_credentials_json" in params and not isinstance(params["google_cloud_storage_credentials_json"], str):
        raise InvalidParameterError("Bad parameter: google_cloud_storage_credentials_json must be an str")
    if "wasabi_access_key" in params and not isinstance(params["wasabi_access_key"], str):
        raise InvalidParameterError("Bad parameter: wasabi_access_key must be an str")
    if "wasabi_secret_key" in params and not isinstance(params["wasabi_secret_key"], str):
        raise InvalidParameterError("Bad parameter: wasabi_secret_key must be an str")
    if "backblaze_b2_key_id" in params and not isinstance(params["backblaze_b2_key_id"], str):
        raise InvalidParameterError("Bad parameter: backblaze_b2_key_id must be an str")
    if "backblaze_b2_application_key" in params and not isinstance(params["backblaze_b2_application_key"], str):
        raise InvalidParameterError("Bad parameter: backblaze_b2_application_key must be an str")
    if "rackspace_api_key" in params and not isinstance(params["rackspace_api_key"], str):
        raise InvalidParameterError("Bad parameter: rackspace_api_key must be an str")
    if "azure_blob_storage_access_key" in params and not isinstance(params["azure_blob_storage_access_key"], str):
        raise InvalidParameterError("Bad parameter: azure_blob_storage_access_key must be an str")
    if "hostname" in params and not isinstance(params["hostname"], str):
        raise InvalidParameterError("Bad parameter: hostname must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "max_connections" in params and not isinstance(params["max_connections"], int):
        raise InvalidParameterError("Bad parameter: max_connections must be an int")
    if "port" in params and not isinstance(params["port"], int):
        raise InvalidParameterError("Bad parameter: port must be an int")
    if "s3_bucket" in params and not isinstance(params["s3_bucket"], str):
        raise InvalidParameterError("Bad parameter: s3_bucket must be an str")
    if "s3_region" in params and not isinstance(params["s3_region"], str):
        raise InvalidParameterError("Bad parameter: s3_region must be an str")
    if "server_certificate" in params and not isinstance(params["server_certificate"], str):
        raise InvalidParameterError("Bad parameter: server_certificate must be an str")
    if "server_host_key" in params and not isinstance(params["server_host_key"], str):
        raise InvalidParameterError("Bad parameter: server_host_key must be an str")
    if "server_type" in params and not isinstance(params["server_type"], str):
        raise InvalidParameterError("Bad parameter: server_type must be an str")
    if "ssl" in params and not isinstance(params["ssl"], str):
        raise InvalidParameterError("Bad parameter: ssl must be an str")
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    if "google_cloud_storage_bucket" in params and not isinstance(params["google_cloud_storage_bucket"], str):
        raise InvalidParameterError("Bad parameter: google_cloud_storage_bucket must be an str")
    if "google_cloud_storage_project_id" in params and not isinstance(params["google_cloud_storage_project_id"], str):
        raise InvalidParameterError("Bad parameter: google_cloud_storage_project_id must be an str")
    if "backblaze_b2_bucket" in params and not isinstance(params["backblaze_b2_bucket"], str):
        raise InvalidParameterError("Bad parameter: backblaze_b2_bucket must be an str")
    if "backblaze_b2_s3_endpoint" in params and not isinstance(params["backblaze_b2_s3_endpoint"], str):
        raise InvalidParameterError("Bad parameter: backblaze_b2_s3_endpoint must be an str")
    if "wasabi_bucket" in params and not isinstance(params["wasabi_bucket"], str):
        raise InvalidParameterError("Bad parameter: wasabi_bucket must be an str")
    if "wasabi_region" in params and not isinstance(params["wasabi_region"], str):
        raise InvalidParameterError("Bad parameter: wasabi_region must be an str")
    if "rackspace_username" in params and not isinstance(params["rackspace_username"], str):
        raise InvalidParameterError("Bad parameter: rackspace_username must be an str")
    if "rackspace_region" in params and not isinstance(params["rackspace_region"], str):
        raise InvalidParameterError("Bad parameter: rackspace_region must be an str")
    if "rackspace_container" in params and not isinstance(params["rackspace_container"], str):
        raise InvalidParameterError("Bad parameter: rackspace_container must be an str")
    if "one_drive_account_type" in params and not isinstance(params["one_drive_account_type"], str):
        raise InvalidParameterError("Bad parameter: one_drive_account_type must be an str")
    if "azure_blob_storage_account" in params and not isinstance(params["azure_blob_storage_account"], str):
        raise InvalidParameterError("Bad parameter: azure_blob_storage_account must be an str")
    if "azure_blob_storage_container" in params and not isinstance(params["azure_blob_storage_container"], str):
        raise InvalidParameterError("Bad parameter: azure_blob_storage_container must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("PATCH", "/remote_servers/{id}".format(id=params['id']), params, options)
    return RemoteServer(response.data, options)

def delete(id, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request("DELETE", "/remote_servers/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = None, options = None):
    delete(id, params, options)

def new(*args, **kwargs):
    return RemoteServer(*args, **kwargs)