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


class As2Station:
    """A as2 station record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Id of the AS2 Station.
        workspace_id: int64 - ID of the Workspace associated with this AS2 Station.
        name: string - The station's formal AS2 name.
        uri: string - Public URI for sending AS2 message to.
        domain: string - The station's AS2 domain name.
        hex_public_certificate_serial: string - Serial of public certificate used for message security in hex format.
        public_certificate_md5: string - MD5 hash of public certificate used for message security.
        public_certificate: string - Public certificate used for message security.
        private_key_md5: string - MD5 hash of private key used for message security.
        public_certificate_subject: string - Subject of public certificate used for message security.
        public_certificate_issuer: string - Issuer of public certificate used for message security.
        public_certificate_serial: string - Serial of public certificate used for message security.
        public_certificate_not_before: string - Not before value of public certificate used for message security.
        public_certificate_not_after: string - Not after value of public certificate used for message security.
        private_key_password_md5: string - MD5 hash of private key password used for message security.
        private_key: string - PEM-encoded private key matching public_certificate.
        private_key_password: string - Password for the PEM-encoded private key.
        pkcs12: string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the identity's certificate and private key. Provide this instead of public_certificate and private_key.
        pkcs12_password: string - Password for pkcs12. The file and password are used only for import; the extracted certificate and private key are stored as PEM.
    """

    default_attributes = {
        "id": None,  # int64 - Id of the AS2 Station.
        "workspace_id": None,  # int64 - ID of the Workspace associated with this AS2 Station.
        "name": None,  # string - The station's formal AS2 name.
        "uri": None,  # string - Public URI for sending AS2 message to.
        "domain": None,  # string - The station's AS2 domain name.
        "hex_public_certificate_serial": None,  # string - Serial of public certificate used for message security in hex format.
        "public_certificate_md5": None,  # string - MD5 hash of public certificate used for message security.
        "public_certificate": None,  # string - Public certificate used for message security.
        "private_key_md5": None,  # string - MD5 hash of private key used for message security.
        "public_certificate_subject": None,  # string - Subject of public certificate used for message security.
        "public_certificate_issuer": None,  # string - Issuer of public certificate used for message security.
        "public_certificate_serial": None,  # string - Serial of public certificate used for message security.
        "public_certificate_not_before": None,  # string - Not before value of public certificate used for message security.
        "public_certificate_not_after": None,  # string - Not after value of public certificate used for message security.
        "private_key_password_md5": None,  # string - MD5 hash of private key password used for message security.
        "private_key": None,  # string - PEM-encoded private key matching public_certificate.
        "private_key_password": None,  # string - Password for the PEM-encoded private key.
        "pkcs12": None,  # string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the identity's certificate and private key. Provide this instead of public_certificate and private_key.
        "pkcs12_password": None,  # string - Password for pkcs12. The file and password are used only for import; the extracted certificate and private key are stored as PEM.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    workspace_id: int | None
    name: str | None
    uri: str | None
    domain: str | None
    hex_public_certificate_serial: str | None
    public_certificate_md5: str | None
    public_certificate: str | None
    private_key_md5: str | None
    public_certificate_subject: str | None
    public_certificate_issuer: str | None
    public_certificate_serial: str | None
    public_certificate_not_before: str | None
    public_certificate_not_after: str | None
    private_key_password_md5: str | None
    private_key: str | None
    private_key_password: str | None
    pkcs12: str | None
    pkcs12_password: str | None

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
        for attribute, default_value in As2Station.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in As2Station.default_attributes
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
          name - string - The station's formal AS2 name.
          public_certificate - string - Public certificate used for message security.
          private_key - string - PEM-encoded private key matching public_certificate.
          private_key_password - string - Password for the PEM-encoded private key.
          pkcs12 - string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the identity's replacement certificate and private key. Provide this instead of public_certificate and private_key.
          pkcs12_password - string - Password for pkcs12. The file and password are used only for import; the extracted certificate and private key are stored as PEM.
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
        if "public_certificate" in params and not isinstance(
            params["public_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: public_certificate must be an str"
            )
        if "private_key" in params and not isinstance(
            params["private_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key must be an str"
            )
        if "private_key_password" in params and not isinstance(
            params["private_key_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key_password must be an str"
            )
        if "pkcs12" in params and not isinstance(params["pkcs12"], str):
            raise InvalidParameterError("Bad parameter: pkcs12 must be an str")
        if "pkcs12_password" in params and not isinstance(
            params["pkcs12_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: pkcs12_password must be an str"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/as2_stations/" + path_value(params["id"]), params
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
            "DELETE", "/as2_stations/" + path_value(params["id"]), params
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
            new_obj = As2StationResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class As2StationResource:
    """As2Station operations that use one client's configuration.

    Get one from a client, such as ``client.as2_station``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[As2Station]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.
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
        operation = Operation.start(self._scope, options)
        return ListObj(As2Station, "GET", "/as2_stations", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[As2Station]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> As2Station:
        """Parameters:
        id (required) - int64 - As2 Station ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> As2Station:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/as2_stations/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, As2Station)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> As2Station:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> As2Station:
        """Parameters:
        name (required) - string - The station's formal AS2 name.
        workspace_id - int64 - ID of the Workspace associated with this AS2 Station.
        public_certificate - string - Public certificate used for message security.
        private_key - string - PEM-encoded private key matching public_certificate.
        private_key_password - string - Password for the PEM-encoded private key.
        pkcs12 - string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the identity's certificate and private key. Provide this instead of public_certificate and private_key.
        pkcs12_password - string - Password for pkcs12. The file and password are used only for import; the extracted certificate and private key are stored as PEM.
        """
        params = copy_params(params)
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "public_certificate" in params and not isinstance(
            params["public_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: public_certificate must be an str"
            )
        if "private_key" in params and not isinstance(
            params["private_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key must be an str"
            )
        if "private_key_password" in params and not isinstance(
            params["private_key_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key_password must be an str"
            )
        if "pkcs12" in params and not isinstance(params["pkcs12"], str):
            raise InvalidParameterError("Bad parameter: pkcs12 must be an str")
        if "pkcs12_password" in params and not isinstance(
            params["pkcs12_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: pkcs12_password must be an str"
            )
        if "name" not in params:
            raise MissingParameterError("Parameter missing: name")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/as2_stations", params)
        return operation.decode_model(response, As2Station)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> As2Station:
        """Parameters:
        name - string - The station's formal AS2 name.
        public_certificate - string - Public certificate used for message security.
        private_key - string - PEM-encoded private key matching public_certificate.
        private_key_password - string - Password for the PEM-encoded private key.
        pkcs12 - string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the identity's replacement certificate and private key. Provide this instead of public_certificate and private_key.
        pkcs12_password - string - Password for pkcs12. The file and password are used only for import; the extracted certificate and private key are stored as PEM.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> As2Station:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "public_certificate" in params and not isinstance(
            params["public_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: public_certificate must be an str"
            )
        if "private_key" in params and not isinstance(
            params["private_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key must be an str"
            )
        if "private_key_password" in params and not isinstance(
            params["private_key_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key_password must be an str"
            )
        if "pkcs12" in params and not isinstance(params["pkcs12"], str):
            raise InvalidParameterError("Bad parameter: pkcs12 must be an str")
        if "pkcs12_password" in params and not isinstance(
            params["pkcs12_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: pkcs12_password must be an str"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/as2_stations/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, As2Station)

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
            "DELETE", "/as2_stations/" + path_value(params["id"]), params
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
    ) -> As2Station:
        """A new As2Station with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = As2Station(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = As2StationResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[As2Station]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[As2Station]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> As2Station:
    """Parameters:
    id (required) - int64 - As2 Station ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> As2Station:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> As2Station:
    """Parameters:
    name (required) - string - The station's formal AS2 name.
    workspace_id - int64 - ID of the Workspace associated with this AS2 Station.
    public_certificate - string - Public certificate used for message security.
    private_key - string - PEM-encoded private key matching public_certificate.
    private_key_password - string - Password for the PEM-encoded private key.
    pkcs12 - string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the identity's certificate and private key. Provide this instead of public_certificate and private_key.
    pkcs12_password - string - Password for pkcs12. The file and password are used only for import; the extracted certificate and private key are stored as PEM.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> As2Station:
    """Parameters:
    name - string - The station's formal AS2 name.
    public_certificate - string - Public certificate used for message security.
    private_key - string - PEM-encoded private key matching public_certificate.
    private_key_password - string - Password for the PEM-encoded private key.
    pkcs12 - string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the identity's replacement certificate and private key. Provide this instead of public_certificate and private_key.
    pkcs12_password - string - Password for pkcs12. The file and password are used only for import; the extracted certificate and private key are stored as PEM.
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


def new(*args, **kwargs) -> As2Station:
    return As2Station(*args, **kwargs)
