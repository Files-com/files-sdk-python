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


class RemoteServerCredential:
    """A remote server credential record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Remote Server Credential ID
        workspace_id: int64 - Workspace ID (0 for default workspace)
        name: string - Internal name for your reference
        description: string - Internal description for your reference
        server_type: string - Remote server type. Remote Server Credentials are only valid for a single type of Remote Server.
        aws_access_key: string - AWS Access Key.
        s3_assume_role_arn: string - AWS IAM Role ARN for AssumeRole authentication.
        s3_assume_role_duration_seconds: int64 - Session duration in seconds for AssumeRole authentication (900-43200).
        s3_assume_role_external_id: string - External ID for AssumeRole authentication.
        google_cloud_storage_s3_compatible_access_key: string - Google Cloud Storage: S3-compatible Access Key.
        wasabi_access_key: string - Wasabi: Access Key.
        s3_compatible_access_key: string - S3-compatible: Access Key
        filebase_access_key: string - Filebase: Access Key.
        cloudflare_access_key: string - Cloudflare: Access Key.
        linode_access_key: string - Linode: Access Key
        sharepoint_tenant_id: string - SharePoint: Microsoft Entra tenant ID for app-only authentication.
        sharepoint_client_id: string - SharePoint: Microsoft Entra application client ID for app-only authentication.
        sharepoint_app_credential_type: string - SharePoint: App-only credential type. Either secret or certificate.
        username: string - Remote server username.
        password: string - Password, if needed.
        private_key: string - Private key, if needed.
        private_key_passphrase: string - Passphrase for private key if needed.
        aws_secret_key: string - AWS: secret key.
        azure_blob_storage_access_key: string - Azure Blob Storage: Access Key
        azure_blob_storage_sas_token: string - Azure Blob Storage: Shared Access Signature (SAS) token
        azure_files_storage_access_key: string - Azure File Storage: Access Key
        azure_files_storage_sas_token: string - Azure File Storage: Shared Access Signature (SAS) token
        backblaze_b2_application_key: string - Backblaze B2 Cloud Storage: applicationKey
        backblaze_b2_key_id: string - Backblaze B2 Cloud Storage: keyID
        cloudflare_secret_key: string - Cloudflare: Secret Key
        filebase_secret_key: string - Filebase: Secret Key
        google_cloud_storage_credentials_json: string - Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
        google_cloud_storage_s3_compatible_secret_key: string - Google Cloud Storage: S3-compatible secret key
        linode_secret_key: string - Linode: Secret Key
        s3_compatible_secret_key: string - S3-compatible: Secret Key
        sharepoint_client_certificate: string - SharePoint: PEM-encoded certificate and unencrypted private key for app-only authentication.
        sharepoint_client_secret: string - SharePoint: Microsoft Entra application client secret for app-only authentication.
        wasabi_secret_key: string - Wasabi: Secret Key
        copy_values_from_credential_id: int64 - ID of Remote Server Credential to copy omitted values from.
    """

    default_attributes = {
        "id": None,  # int64 - Remote Server Credential ID
        "workspace_id": None,  # int64 - Workspace ID (0 for default workspace)
        "name": None,  # string - Internal name for your reference
        "description": None,  # string - Internal description for your reference
        "server_type": None,  # string - Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
        "aws_access_key": None,  # string - AWS Access Key.
        "s3_assume_role_arn": None,  # string - AWS IAM Role ARN for AssumeRole authentication.
        "s3_assume_role_duration_seconds": None,  # int64 - Session duration in seconds for AssumeRole authentication (900-43200).
        "s3_assume_role_external_id": None,  # string - External ID for AssumeRole authentication.
        "google_cloud_storage_s3_compatible_access_key": None,  # string - Google Cloud Storage: S3-compatible Access Key.
        "wasabi_access_key": None,  # string - Wasabi: Access Key.
        "s3_compatible_access_key": None,  # string - S3-compatible: Access Key
        "filebase_access_key": None,  # string - Filebase: Access Key.
        "cloudflare_access_key": None,  # string - Cloudflare: Access Key.
        "linode_access_key": None,  # string - Linode: Access Key
        "sharepoint_tenant_id": None,  # string - SharePoint: Microsoft Entra tenant ID for app-only authentication.
        "sharepoint_client_id": None,  # string - SharePoint: Microsoft Entra application client ID for app-only authentication.
        "sharepoint_app_credential_type": None,  # string - SharePoint: App-only credential type. Either secret or certificate.
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
        "sharepoint_client_certificate": None,  # string - SharePoint: PEM-encoded certificate and unencrypted private key for app-only authentication.
        "sharepoint_client_secret": None,  # string - SharePoint: Microsoft Entra application client secret for app-only authentication.
        "wasabi_secret_key": None,  # string - Wasabi: Secret Key
        "copy_values_from_credential_id": None,  # int64 - ID of Remote Server Credential to copy omitted values from.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    workspace_id: int | None
    name: str | None
    description: str | None
    server_type: str | None
    aws_access_key: str | None
    s3_assume_role_arn: str | None
    s3_assume_role_duration_seconds: int | None
    s3_assume_role_external_id: str | None
    google_cloud_storage_s3_compatible_access_key: str | None
    wasabi_access_key: str | None
    s3_compatible_access_key: str | None
    filebase_access_key: str | None
    cloudflare_access_key: str | None
    linode_access_key: str | None
    sharepoint_tenant_id: str | None
    sharepoint_client_id: str | None
    sharepoint_app_credential_type: str | None
    username: str | None
    password: str | None
    private_key: str | None
    private_key_passphrase: str | None
    aws_secret_key: str | None
    azure_blob_storage_access_key: str | None
    azure_blob_storage_sas_token: str | None
    azure_files_storage_access_key: str | None
    azure_files_storage_sas_token: str | None
    backblaze_b2_application_key: str | None
    backblaze_b2_key_id: str | None
    cloudflare_secret_key: str | None
    filebase_secret_key: str | None
    google_cloud_storage_credentials_json: str | None
    google_cloud_storage_s3_compatible_secret_key: str | None
    linode_secret_key: str | None
    s3_compatible_secret_key: str | None
    sharepoint_client_certificate: str | None
    sharepoint_client_secret: str | None
    wasabi_secret_key: str | None
    copy_values_from_credential_id: int | None

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
        for (
            attribute,
            default_value,
        ) in RemoteServerCredential.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in RemoteServerCredential.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          name - string - Internal name for your reference
          description - string - Internal description for your reference
          server_type - string - Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
          aws_access_key - string - AWS Access Key.
          s3_assume_role_arn - string - AWS IAM Role ARN for AssumeRole authentication.
          s3_assume_role_duration_seconds - int64 - Session duration in seconds for AssumeRole authentication (900-43200).
          cloudflare_access_key - string - Cloudflare: Access Key.
          filebase_access_key - string - Filebase: Access Key.
          google_cloud_storage_s3_compatible_access_key - string - Google Cloud Storage: S3-compatible Access Key.
          linode_access_key - string - Linode: Access Key
          s3_compatible_access_key - string - S3-compatible: Access Key
          sharepoint_client_id - string - SharePoint: Microsoft Entra application client ID for app-only authentication.
          sharepoint_tenant_id - string - SharePoint: Microsoft Entra tenant ID for app-only authentication.
          username - string - Remote server username.
          wasabi_access_key - string - Wasabi: Access Key.
          password - string - Password, if needed.
          private_key - string - Private key, if needed.
          private_key_passphrase - string - Passphrase for private key if needed.
          aws_secret_key - string - AWS: secret key.
          azure_blob_storage_access_key - string - Azure Blob Storage: Access Key
          azure_blob_storage_sas_token - string - Azure Blob Storage: Shared Access Signature (SAS) token
          azure_files_storage_access_key - string - Azure File Storage: Access Key
          azure_files_storage_sas_token - string - Azure File Storage: Shared Access Signature (SAS) token
          backblaze_b2_application_key - string - Backblaze B2 Cloud Storage: applicationKey
          backblaze_b2_key_id - string - Backblaze B2 Cloud Storage: keyID
          cloudflare_secret_key - string - Cloudflare: Secret Key
          filebase_secret_key - string - Filebase: Secret Key
          google_cloud_storage_credentials_json - string - Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
          google_cloud_storage_s3_compatible_secret_key - string - Google Cloud Storage: S3-compatible secret key
          linode_secret_key - string - Linode: Secret Key
          s3_compatible_secret_key - string - S3-compatible: Secret Key
          sharepoint_client_certificate - string - SharePoint: PEM-encoded certificate and unencrypted private key for app-only authentication.
          sharepoint_client_secret - string - SharePoint: Microsoft Entra application client secret for app-only authentication.
          wasabi_secret_key - string - Wasabi: Secret Key
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
        if "s3_assume_role_arn" in params and not isinstance(
            params["s3_assume_role_arn"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_assume_role_arn must be an str"
            )
        if "s3_assume_role_duration_seconds" in params and (
            not isinstance(params["s3_assume_role_duration_seconds"], int)
            or isinstance(params["s3_assume_role_duration_seconds"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_assume_role_duration_seconds must be an int"
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
        if "sharepoint_client_id" in params and not isinstance(
            params["sharepoint_client_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: sharepoint_client_id must be an str"
            )
        if "sharepoint_tenant_id" in params and not isinstance(
            params["sharepoint_tenant_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: sharepoint_tenant_id must be an str"
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
        if "sharepoint_client_certificate" in params and not isinstance(
            params["sharepoint_client_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: sharepoint_client_certificate must be an str"
            )
        if "sharepoint_client_secret" in params and not isinstance(
            params["sharepoint_client_secret"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: sharepoint_client_secret must be an str"
            )
        if "wasabi_secret_key" in params and not isinstance(
            params["wasabi_secret_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: wasabi_secret_key must be an str"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH",
            "/remote_server_credentials/" + path_value(params["id"]),
            params,
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

    def delete(self, params: dict[str, Any] | None = None) -> None:
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
            "DELETE",
            "/remote_server_credentials/" + path_value(params["id"]),
            params,
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
            new_obj = RemoteServerCredentialResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class RemoteServerCredentialResource:
    """RemoteServerCredential operations that use one client's configuration.

    Get one from a client, such as ``client.remote_server_credential``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[RemoteServerCredential]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id` and `name`. Valid field combinations are `[ workspace_id, name ]`.
        filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.
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
        if "filter_prefix" in params and not isinstance(
            params["filter_prefix"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_prefix must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(
            RemoteServerCredential,
            "GET",
            "/remote_server_credentials",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[RemoteServerCredential]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> RemoteServerCredential:
        """Parameters:
        id (required) - int64 - Remote Server Credential ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> RemoteServerCredential:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET",
            "/remote_server_credentials/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, RemoteServerCredential)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> RemoteServerCredential:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> RemoteServerCredential:
        """Parameters:
        name - string - Internal name for your reference
        description - string - Internal description for your reference
        server_type - string - Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
        aws_access_key - string - AWS Access Key.
        s3_assume_role_arn - string - AWS IAM Role ARN for AssumeRole authentication.
        s3_assume_role_duration_seconds - int64 - Session duration in seconds for AssumeRole authentication (900-43200).
        cloudflare_access_key - string - Cloudflare: Access Key.
        filebase_access_key - string - Filebase: Access Key.
        google_cloud_storage_s3_compatible_access_key - string - Google Cloud Storage: S3-compatible Access Key.
        linode_access_key - string - Linode: Access Key
        s3_compatible_access_key - string - S3-compatible: Access Key
        sharepoint_client_id - string - SharePoint: Microsoft Entra application client ID for app-only authentication.
        sharepoint_tenant_id - string - SharePoint: Microsoft Entra tenant ID for app-only authentication.
        username - string - Remote server username.
        wasabi_access_key - string - Wasabi: Access Key.
        password - string - Password, if needed.
        private_key - string - Private key, if needed.
        private_key_passphrase - string - Passphrase for private key if needed.
        aws_secret_key - string - AWS: secret key.
        azure_blob_storage_access_key - string - Azure Blob Storage: Access Key
        azure_blob_storage_sas_token - string - Azure Blob Storage: Shared Access Signature (SAS) token
        azure_files_storage_access_key - string - Azure File Storage: Access Key
        azure_files_storage_sas_token - string - Azure File Storage: Shared Access Signature (SAS) token
        backblaze_b2_application_key - string - Backblaze B2 Cloud Storage: applicationKey
        backblaze_b2_key_id - string - Backblaze B2 Cloud Storage: keyID
        cloudflare_secret_key - string - Cloudflare: Secret Key
        filebase_secret_key - string - Filebase: Secret Key
        google_cloud_storage_credentials_json - string - Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
        google_cloud_storage_s3_compatible_secret_key - string - Google Cloud Storage: S3-compatible secret key
        linode_secret_key - string - Linode: Secret Key
        s3_compatible_secret_key - string - S3-compatible: Secret Key
        sharepoint_client_certificate - string - SharePoint: PEM-encoded certificate and unencrypted private key for app-only authentication.
        sharepoint_client_secret - string - SharePoint: Microsoft Entra application client secret for app-only authentication.
        wasabi_secret_key - string - Wasabi: Secret Key
        workspace_id - int64 - Workspace ID (0 for default workspace)
        copy_values_from_credential_id - int64 - ID of Remote Server Credential to copy omitted values from.
        """
        params = copy_params(params)
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
        if "s3_assume_role_arn" in params and not isinstance(
            params["s3_assume_role_arn"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_assume_role_arn must be an str"
            )
        if "s3_assume_role_duration_seconds" in params and (
            not isinstance(params["s3_assume_role_duration_seconds"], int)
            or isinstance(params["s3_assume_role_duration_seconds"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_assume_role_duration_seconds must be an int"
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
        if "sharepoint_client_id" in params and not isinstance(
            params["sharepoint_client_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: sharepoint_client_id must be an str"
            )
        if "sharepoint_tenant_id" in params and not isinstance(
            params["sharepoint_tenant_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: sharepoint_tenant_id must be an str"
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
        if "sharepoint_client_certificate" in params and not isinstance(
            params["sharepoint_client_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: sharepoint_client_certificate must be an str"
            )
        if "sharepoint_client_secret" in params and not isinstance(
            params["sharepoint_client_secret"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: sharepoint_client_secret must be an str"
            )
        if "wasabi_secret_key" in params and not isinstance(
            params["wasabi_secret_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: wasabi_secret_key must be an str"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "copy_values_from_credential_id" in params and (
            not isinstance(params["copy_values_from_credential_id"], int)
            or isinstance(params["copy_values_from_credential_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: copy_values_from_credential_id must be an int"
            )
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST", "/remote_server_credentials", params
        )
        return operation.decode_model(response, RemoteServerCredential)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> RemoteServerCredential:
        """Parameters:
        name - string - Internal name for your reference
        description - string - Internal description for your reference
        server_type - string - Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
        aws_access_key - string - AWS Access Key.
        s3_assume_role_arn - string - AWS IAM Role ARN for AssumeRole authentication.
        s3_assume_role_duration_seconds - int64 - Session duration in seconds for AssumeRole authentication (900-43200).
        cloudflare_access_key - string - Cloudflare: Access Key.
        filebase_access_key - string - Filebase: Access Key.
        google_cloud_storage_s3_compatible_access_key - string - Google Cloud Storage: S3-compatible Access Key.
        linode_access_key - string - Linode: Access Key
        s3_compatible_access_key - string - S3-compatible: Access Key
        sharepoint_client_id - string - SharePoint: Microsoft Entra application client ID for app-only authentication.
        sharepoint_tenant_id - string - SharePoint: Microsoft Entra tenant ID for app-only authentication.
        username - string - Remote server username.
        wasabi_access_key - string - Wasabi: Access Key.
        password - string - Password, if needed.
        private_key - string - Private key, if needed.
        private_key_passphrase - string - Passphrase for private key if needed.
        aws_secret_key - string - AWS: secret key.
        azure_blob_storage_access_key - string - Azure Blob Storage: Access Key
        azure_blob_storage_sas_token - string - Azure Blob Storage: Shared Access Signature (SAS) token
        azure_files_storage_access_key - string - Azure File Storage: Access Key
        azure_files_storage_sas_token - string - Azure File Storage: Shared Access Signature (SAS) token
        backblaze_b2_application_key - string - Backblaze B2 Cloud Storage: applicationKey
        backblaze_b2_key_id - string - Backblaze B2 Cloud Storage: keyID
        cloudflare_secret_key - string - Cloudflare: Secret Key
        filebase_secret_key - string - Filebase: Secret Key
        google_cloud_storage_credentials_json - string - Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
        google_cloud_storage_s3_compatible_secret_key - string - Google Cloud Storage: S3-compatible secret key
        linode_secret_key - string - Linode: Secret Key
        s3_compatible_secret_key - string - S3-compatible: Secret Key
        sharepoint_client_certificate - string - SharePoint: PEM-encoded certificate and unencrypted private key for app-only authentication.
        sharepoint_client_secret - string - SharePoint: Microsoft Entra application client secret for app-only authentication.
        wasabi_secret_key - string - Wasabi: Secret Key
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> RemoteServerCredential:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
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
        if "s3_assume_role_arn" in params and not isinstance(
            params["s3_assume_role_arn"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_assume_role_arn must be an str"
            )
        if "s3_assume_role_duration_seconds" in params and (
            not isinstance(params["s3_assume_role_duration_seconds"], int)
            or isinstance(params["s3_assume_role_duration_seconds"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: s3_assume_role_duration_seconds must be an int"
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
        if "sharepoint_client_id" in params and not isinstance(
            params["sharepoint_client_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: sharepoint_client_id must be an str"
            )
        if "sharepoint_tenant_id" in params and not isinstance(
            params["sharepoint_tenant_id"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: sharepoint_tenant_id must be an str"
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
        if "sharepoint_client_certificate" in params and not isinstance(
            params["sharepoint_client_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: sharepoint_client_certificate must be an str"
            )
        if "sharepoint_client_secret" in params and not isinstance(
            params["sharepoint_client_secret"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: sharepoint_client_secret must be an str"
            )
        if "wasabi_secret_key" in params and not isinstance(
            params["wasabi_secret_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: wasabi_secret_key must be an str"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH",
            "/remote_server_credentials/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, RemoteServerCredential)

    def delete(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
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
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE",
            "/remote_server_credentials/" + path_value(params["id"]),
            params,
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
    ) -> RemoteServerCredential:
        """A new RemoteServerCredential with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = RemoteServerCredential(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = RemoteServerCredentialResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[RemoteServerCredential]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id` and `name`. Valid field combinations are `[ workspace_id, name ]`.
    filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[RemoteServerCredential]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> RemoteServerCredential:
    """Parameters:
    id (required) - int64 - Remote Server Credential ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> RemoteServerCredential:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> RemoteServerCredential:
    """Parameters:
    name - string - Internal name for your reference
    description - string - Internal description for your reference
    server_type - string - Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
    aws_access_key - string - AWS Access Key.
    s3_assume_role_arn - string - AWS IAM Role ARN for AssumeRole authentication.
    s3_assume_role_duration_seconds - int64 - Session duration in seconds for AssumeRole authentication (900-43200).
    cloudflare_access_key - string - Cloudflare: Access Key.
    filebase_access_key - string - Filebase: Access Key.
    google_cloud_storage_s3_compatible_access_key - string - Google Cloud Storage: S3-compatible Access Key.
    linode_access_key - string - Linode: Access Key
    s3_compatible_access_key - string - S3-compatible: Access Key
    sharepoint_client_id - string - SharePoint: Microsoft Entra application client ID for app-only authentication.
    sharepoint_tenant_id - string - SharePoint: Microsoft Entra tenant ID for app-only authentication.
    username - string - Remote server username.
    wasabi_access_key - string - Wasabi: Access Key.
    password - string - Password, if needed.
    private_key - string - Private key, if needed.
    private_key_passphrase - string - Passphrase for private key if needed.
    aws_secret_key - string - AWS: secret key.
    azure_blob_storage_access_key - string - Azure Blob Storage: Access Key
    azure_blob_storage_sas_token - string - Azure Blob Storage: Shared Access Signature (SAS) token
    azure_files_storage_access_key - string - Azure File Storage: Access Key
    azure_files_storage_sas_token - string - Azure File Storage: Shared Access Signature (SAS) token
    backblaze_b2_application_key - string - Backblaze B2 Cloud Storage: applicationKey
    backblaze_b2_key_id - string - Backblaze B2 Cloud Storage: keyID
    cloudflare_secret_key - string - Cloudflare: Secret Key
    filebase_secret_key - string - Filebase: Secret Key
    google_cloud_storage_credentials_json - string - Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
    google_cloud_storage_s3_compatible_secret_key - string - Google Cloud Storage: S3-compatible secret key
    linode_secret_key - string - Linode: Secret Key
    s3_compatible_secret_key - string - S3-compatible: Secret Key
    sharepoint_client_certificate - string - SharePoint: PEM-encoded certificate and unencrypted private key for app-only authentication.
    sharepoint_client_secret - string - SharePoint: Microsoft Entra application client secret for app-only authentication.
    wasabi_secret_key - string - Wasabi: Secret Key
    workspace_id - int64 - Workspace ID (0 for default workspace)
    copy_values_from_credential_id - int64 - ID of Remote Server Credential to copy omitted values from.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> RemoteServerCredential:
    """Parameters:
    name - string - Internal name for your reference
    description - string - Internal description for your reference
    server_type - string - Remote server type.  Remote Server Credentials are only valid for a single type of Remote Server.
    aws_access_key - string - AWS Access Key.
    s3_assume_role_arn - string - AWS IAM Role ARN for AssumeRole authentication.
    s3_assume_role_duration_seconds - int64 - Session duration in seconds for AssumeRole authentication (900-43200).
    cloudflare_access_key - string - Cloudflare: Access Key.
    filebase_access_key - string - Filebase: Access Key.
    google_cloud_storage_s3_compatible_access_key - string - Google Cloud Storage: S3-compatible Access Key.
    linode_access_key - string - Linode: Access Key
    s3_compatible_access_key - string - S3-compatible: Access Key
    sharepoint_client_id - string - SharePoint: Microsoft Entra application client ID for app-only authentication.
    sharepoint_tenant_id - string - SharePoint: Microsoft Entra tenant ID for app-only authentication.
    username - string - Remote server username.
    wasabi_access_key - string - Wasabi: Access Key.
    password - string - Password, if needed.
    private_key - string - Private key, if needed.
    private_key_passphrase - string - Passphrase for private key if needed.
    aws_secret_key - string - AWS: secret key.
    azure_blob_storage_access_key - string - Azure Blob Storage: Access Key
    azure_blob_storage_sas_token - string - Azure Blob Storage: Shared Access Signature (SAS) token
    azure_files_storage_access_key - string - Azure File Storage: Access Key
    azure_files_storage_sas_token - string - Azure File Storage: Shared Access Signature (SAS) token
    backblaze_b2_application_key - string - Backblaze B2 Cloud Storage: applicationKey
    backblaze_b2_key_id - string - Backblaze B2 Cloud Storage: keyID
    cloudflare_secret_key - string - Cloudflare: Secret Key
    filebase_secret_key - string - Filebase: Secret Key
    google_cloud_storage_credentials_json - string - Google Cloud Storage: JSON file that contains the private key. To generate see https://cloud.google.com/storage/docs/json_api/v1/how-tos/authorizing#APIKey
    google_cloud_storage_s3_compatible_secret_key - string - Google Cloud Storage: S3-compatible secret key
    linode_secret_key - string - Linode: Secret Key
    s3_compatible_secret_key - string - S3-compatible: Secret Key
    sharepoint_client_certificate - string - SharePoint: PEM-encoded certificate and unencrypted private key for app-only authentication.
    sharepoint_client_secret - string - SharePoint: Microsoft Entra application client secret for app-only authentication.
    wasabi_secret_key - string - Wasabi: Secret Key
    """
    return _legacy_resource.update(id, params, options)


def delete(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    _legacy_resource.delete(id, params, options)


def destroy(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(id, params, options)


def new(*args, **kwargs) -> RemoteServerCredential:
    return RemoteServerCredential(*args, **kwargs)
