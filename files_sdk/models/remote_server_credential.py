import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class RemoteServerCredential:
    default_attributes = {
        "id": None,  # int64 - Remote Server Credential ID
        "name": None,  # string - Internal name for your reference
        "description": None,  # string - Internal description for your reference
        "server_type": None,  # string - Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
        "aws_access_key": None,  # string - AWS Access Key.
        "google_cloud_storage_s3_compatible_access_key": None,  # string - Google Cloud Storage: S3-compatible Access Key.
        "wasabi_access_key": None,  # string - Wasabi: Access Key.
        "azure_blob_storage_account": None,  # string - Azure Blob Storage: Account name
        "azure_files_storage_account": None,  # string - Azure Files: Storage Account name
        "s3_compatible_access_key": None,  # string - S3-compatible: Access Key
        "filebase_access_key": None,  # string - Filebase: Access Key.
        "cloudflare_access_key": None,  # string - Cloudflare: Access Key.
        "linode_access_key": None,  # string - Linode: Access Key
        "username": None,  # string - Remote server username.
        "password": None,  # string - Password, if needed.
        "private_key": None,  # string - Private key, if needed.
        "private_key_passphrase": None,  # string - Passphrase for private key if needed.
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
        ) in RemoteServerCredential.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in RemoteServerCredential.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   name - string - Internal name for your reference
    #   description - string - Internal description for your reference
    #   server_type - string - Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
    #   aws_access_key - string - AWS Access Key.
    #   azure_blob_storage_account - string - Azure Blob Storage: Account name
    #   azure_files_storage_account - string - Azure Files: Storage Account name
    #   cloudflare_access_key - string - Cloudflare: Access Key.
    #   filebase_access_key - string - Filebase: Access Key.
    #   google_cloud_storage_s3_compatible_access_key - string - Google Cloud Storage: S3-compatible Access Key.
    #   linode_access_key - string - Linode: Access Key
    #   s3_compatible_access_key - string - S3-compatible: Access Key
    #   username - string - Remote server username.
    #   wasabi_access_key - string - Wasabi: Access Key.
    #   password - string - Password, if needed.
    #   private_key - string - Private key, if needed.
    #   private_key_passphrase - string - Passphrase for private key if needed.
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
    #   s3_compatible_secret_key - string - S3-compatible: Secret Key
    #   wasabi_secret_key - string - Wasabi: Secret Key
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
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "server_type" in params and not isinstance(
            params["server_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: server_type must be an str"
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
        if "azure_files_storage_account" in params and not isinstance(
            params["azure_files_storage_account"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: azure_files_storage_account must be an str"
            )
        if "cloudflare_access_key" in params and not isinstance(
            params["cloudflare_access_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: cloudflare_access_key must be an str"
            )
        if "filebase_access_key" in params and not isinstance(
            params["filebase_access_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: filebase_access_key must be an str"
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
        if "linode_access_key" in params and not isinstance(
            params["linode_access_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: linode_access_key must be an str"
            )
        if "s3_compatible_access_key" in params and not isinstance(
            params["s3_compatible_access_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_compatible_access_key must be an str"
            )
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
        response, _options = Api.send_request(
            "PATCH",
            "/remote_server_credentials/{id}".format(id=params["id"]),
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
            "/remote_server_credentials/{id}".format(id=params["id"]),
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
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `name`.
#   filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_prefix" in params and not isinstance(
        params["filter_prefix"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: filter_prefix must be an dict"
        )
    return ListObj(
        RemoteServerCredential,
        "GET",
        "/remote_server_credentials",
        params,
        options,
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Remote Server Credential ID.
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
        "/remote_server_credentials/{id}".format(id=params["id"]),
        params,
        options,
    )
    return RemoteServerCredential(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   name - string - Internal name for your reference
#   description - string - Internal description for your reference
#   server_type - string - Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
#   aws_access_key - string - AWS Access Key.
#   azure_blob_storage_account - string - Azure Blob Storage: Account name
#   azure_files_storage_account - string - Azure Files: Storage Account name
#   cloudflare_access_key - string - Cloudflare: Access Key.
#   filebase_access_key - string - Filebase: Access Key.
#   google_cloud_storage_s3_compatible_access_key - string - Google Cloud Storage: S3-compatible Access Key.
#   linode_access_key - string - Linode: Access Key
#   s3_compatible_access_key - string - S3-compatible: Access Key
#   username - string - Remote server username.
#   wasabi_access_key - string - Wasabi: Access Key.
#   password - string - Password, if needed.
#   private_key - string - Private key, if needed.
#   private_key_passphrase - string - Passphrase for private key if needed.
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
#   s3_compatible_secret_key - string - S3-compatible: Secret Key
#   wasabi_secret_key - string - Wasabi: Secret Key
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "server_type" in params and not isinstance(params["server_type"], str):
        raise InvalidParameterError(
            "Bad parameter: server_type must be an str"
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
    if "azure_files_storage_account" in params and not isinstance(
        params["azure_files_storage_account"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_files_storage_account must be an str"
        )
    if "cloudflare_access_key" in params and not isinstance(
        params["cloudflare_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: cloudflare_access_key must be an str"
        )
    if "filebase_access_key" in params and not isinstance(
        params["filebase_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: filebase_access_key must be an str"
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
    if "linode_access_key" in params and not isinstance(
        params["linode_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: linode_access_key must be an str"
        )
    if "s3_compatible_access_key" in params and not isinstance(
        params["s3_compatible_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: s3_compatible_access_key must be an str"
        )
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    if "wasabi_access_key" in params and not isinstance(
        params["wasabi_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: wasabi_access_key must be an str"
        )
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
    response, options = Api.send_request(
        "POST", "/remote_server_credentials", params, options
    )
    return RemoteServerCredential(response.data, options)


# Parameters:
#   name - string - Internal name for your reference
#   description - string - Internal description for your reference
#   server_type - string - Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
#   aws_access_key - string - AWS Access Key.
#   azure_blob_storage_account - string - Azure Blob Storage: Account name
#   azure_files_storage_account - string - Azure Files: Storage Account name
#   cloudflare_access_key - string - Cloudflare: Access Key.
#   filebase_access_key - string - Filebase: Access Key.
#   google_cloud_storage_s3_compatible_access_key - string - Google Cloud Storage: S3-compatible Access Key.
#   linode_access_key - string - Linode: Access Key
#   s3_compatible_access_key - string - S3-compatible: Access Key
#   username - string - Remote server username.
#   wasabi_access_key - string - Wasabi: Access Key.
#   password - string - Password, if needed.
#   private_key - string - Private key, if needed.
#   private_key_passphrase - string - Passphrase for private key if needed.
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
#   s3_compatible_secret_key - string - S3-compatible: Secret Key
#   wasabi_secret_key - string - Wasabi: Secret Key
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "server_type" in params and not isinstance(params["server_type"], str):
        raise InvalidParameterError(
            "Bad parameter: server_type must be an str"
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
    if "azure_files_storage_account" in params and not isinstance(
        params["azure_files_storage_account"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: azure_files_storage_account must be an str"
        )
    if "cloudflare_access_key" in params and not isinstance(
        params["cloudflare_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: cloudflare_access_key must be an str"
        )
    if "filebase_access_key" in params and not isinstance(
        params["filebase_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: filebase_access_key must be an str"
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
    if "linode_access_key" in params and not isinstance(
        params["linode_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: linode_access_key must be an str"
        )
    if "s3_compatible_access_key" in params and not isinstance(
        params["s3_compatible_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: s3_compatible_access_key must be an str"
        )
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    if "wasabi_access_key" in params and not isinstance(
        params["wasabi_access_key"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: wasabi_access_key must be an str"
        )
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
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/remote_server_credentials/{id}".format(id=params["id"]),
        params,
        options,
    )
    return RemoteServerCredential(response.data, options)


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
        "/remote_server_credentials/{id}".format(id=params["id"]),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return RemoteServerCredential(*args, **kwargs)
