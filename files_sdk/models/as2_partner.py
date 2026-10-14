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


class As2Partner:
    """A as2 partner record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - ID of the AS2 Partner.
        workspace_id: int64 - ID of the Workspace associated with this AS2 Partner.
        as2_station_id: int64 - ID of the AS2 Station associated with this partner.
        name: string - The partner's formal AS2 name.
        uri: string - Public URI where we will send the AS2 messages (via HTTP/HTTPS).
        server_certificate: string - Should we require that the remote HTTP server have a valid SSL Certificate for HTTPS? (This only applies to Outgoing AS2 message from Files.com to a Partner.)
        http_auth_username: string - Username to send to server for HTTP Authentication.
        additional_http_headers: object - Additional HTTP Headers for outgoing message sent to this partner.
        default_mime_type: string - Default mime type of the file attached to the encrypted message
        mdn_validation_level: string - How should Files.com evaluate message transfer success based on a partner's MDN response? This setting does not affect MDN storage; all MDNs received from a partner are always stored. `none`: MDN is stored for informational purposes only, a successful HTTPS transfer is a successful AS2 transfer. `weak`: Inspect the MDN for MIC and Disposition only. `normal`: `weak` plus validate MDN signature matches body, `strict`: `normal` but do not allow signatures from self-signed or incorrectly purposed certificates. `auto`: Automatically set the correct value for this setting based on next mdn received.
        signature_validation_level: string - Should Files.com require signatures on incoming AS2 messages? `normal`: require that incoming messages are signed with a valid matching signature. `none`: Unsigned incoming messages are allowed. `auto`: A one-time starting state. The next message received is always accepted and switches this to `normal` if it carries a valid signature, or `none` if it does not.
        enable_dedicated_ips: boolean - If `true`, we will use your site's dedicated IPs for all outbound connections to this AS2 Partner.
        hex_public_certificate_serial: string - Serial of public certificate used for message security in hex format.
        public_certificate: string - Public certificate used for message security.
        public_certificate_md5: string - MD5 hash of public certificate used for message security.
        public_certificate_subject: string - Subject of public certificate used for message security.
        public_certificate_issuer: string - Issuer of public certificate used for message security.
        public_certificate_serial: string - Serial of public certificate used for message security.
        public_certificate_not_before: string - Not before value of public certificate used for message security.
        public_certificate_not_after: string - Not after value of public certificate used for message security.
        http_auth_password: string - Password to send to server for HTTP Authentication.
        pkcs12: string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the partner's public certificate. Provide this instead of public_certificate. Any private key in the file is discarded. A public-only file must contain exactly one certificate.
        pkcs12_password: string - Password for pkcs12. The file and password are used only for import; the extracted public certificate is stored as PEM.
    """

    default_attributes = {
        "id": None,  # int64 - ID of the AS2 Partner.
        "workspace_id": None,  # int64 - ID of the Workspace associated with this AS2 Partner.
        "as2_station_id": None,  # int64 - ID of the AS2 Station associated with this partner.
        "name": None,  # string - The partner's formal AS2 name.
        "uri": None,  # string - Public URI where we will send the AS2 messages (via HTTP/HTTPS).
        "server_certificate": None,  # string - Should we require that the remote HTTP server have a valid SSL Certificate for HTTPS? (This only applies to Outgoing AS2 message from Files.com to a Partner.)
        "http_auth_username": None,  # string - Username to send to server for HTTP Authentication.
        "additional_http_headers": None,  # object - Additional HTTP Headers for outgoing message sent to this partner.
        "default_mime_type": None,  # string - Default mime type of the file attached to the encrypted message
        "mdn_validation_level": None,  # string - How should Files.com evaluate message transfer success based on a partner's MDN response?  This setting does not affect MDN storage; all MDNs received from a partner are always stored. `none`: MDN is stored for informational purposes only, a successful HTTPS transfer is a successful AS2 transfer. `weak`: Inspect the MDN for MIC and Disposition only. `normal`: `weak` plus validate MDN signature matches body, `strict`: `normal` but do not allow signatures from self-signed or incorrectly purposed certificates. `auto`: Automatically set the correct value for this setting based on next mdn received.
        "signature_validation_level": None,  # string - Should Files.com require signatures on incoming AS2 messages?  `normal`: require that incoming messages are signed with a valid matching signature. `none`: Unsigned incoming messages are allowed. `auto`: A one-time starting state. The next message received is always accepted and switches this to `normal` if it carries a valid signature, or `none` if it does not.
        "enable_dedicated_ips": None,  # boolean - If `true`, we will use your site's dedicated IPs for all outbound connections to this AS2 Partner.
        "hex_public_certificate_serial": None,  # string - Serial of public certificate used for message security in hex format.
        "public_certificate": None,  # string - Public certificate used for message security.
        "public_certificate_md5": None,  # string - MD5 hash of public certificate used for message security.
        "public_certificate_subject": None,  # string - Subject of public certificate used for message security.
        "public_certificate_issuer": None,  # string - Issuer of public certificate used for message security.
        "public_certificate_serial": None,  # string - Serial of public certificate used for message security.
        "public_certificate_not_before": None,  # string - Not before value of public certificate used for message security.
        "public_certificate_not_after": None,  # string - Not after value of public certificate used for message security.
        "http_auth_password": None,  # string - Password to send to server for HTTP Authentication.
        "pkcs12": None,  # string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the partner's public certificate. Provide this instead of public_certificate. Any private key in the file is discarded. A public-only file must contain exactly one certificate.
        "pkcs12_password": None,  # string - Password for pkcs12. The file and password are used only for import; the extracted public certificate is stored as PEM.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    workspace_id: int | None
    as2_station_id: int | None
    name: str | None
    uri: str | None
    server_certificate: str | None
    http_auth_username: str | None
    additional_http_headers: dict[str, Any] | None
    default_mime_type: str | None
    mdn_validation_level: str | None
    signature_validation_level: str | None
    enable_dedicated_ips: bool | None
    hex_public_certificate_serial: str | None
    public_certificate: str | None
    public_certificate_md5: str | None
    public_certificate_subject: str | None
    public_certificate_issuer: str | None
    public_certificate_serial: str | None
    public_certificate_not_before: str | None
    public_certificate_not_after: str | None
    http_auth_password: str | None
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
        for attribute, default_value in As2Partner.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in As2Partner.default_attributes
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
          enable_dedicated_ips - boolean - If `true`, we will use your site's dedicated IPs for all outbound connections to this AS2 Partner.
          http_auth_username - string - Username to send to server for HTTP Authentication.
          http_auth_password - string - Password to send to server for HTTP Authentication.
          mdn_validation_level - string - How should Files.com evaluate message transfer success based on a partner's MDN response?  This setting does not affect MDN storage; all MDNs received from a partner are always stored. `none`: MDN is stored for informational purposes only, a successful HTTPS transfer is a successful AS2 transfer. `weak`: Inspect the MDN for MIC and Disposition only. `normal`: `weak` plus validate MDN signature matches body, `strict`: `normal` but do not allow signatures from self-signed or incorrectly purposed certificates. `auto`: Automatically set the correct value for this setting based on next mdn received.
          signature_validation_level - string - Should Files.com require signatures on incoming AS2 messages?  `normal`: require that incoming messages are signed with a valid matching signature. `none`: Unsigned incoming messages are allowed. `auto`: A one-time starting state. The next message received is always accepted and switches this to `normal` if it carries a valid signature, or `none` if it does not.
          server_certificate - string - Should we require that the remote HTTP server have a valid SSL Certificate for HTTPS? (This only applies to Outgoing AS2 message from Files.com to a Partner.)
          default_mime_type - string - Default mime type of the file attached to the encrypted message
          additional_http_headers - object - Additional HTTP Headers for outgoing message sent to this partner.
          name - string - The partner's formal AS2 name.
          uri - string - Public URI where we will send the AS2 messages (via HTTP/HTTPS).
          public_certificate - string - Public certificate for AS2 Partner.  Note: This is the certificate for AS2 message security, not a certificate used for HTTPS authentication.
          pkcs12 - string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the partner's public certificate. Provide this instead of public_certificate. Any private key in the file is discarded. A public-only file must contain exactly one certificate.
          pkcs12_password - string - Password for pkcs12. The file and password are used only for import; the extracted public certificate is stored as PEM.
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
        if "enable_dedicated_ips" in params and isinstance(
            params["enable_dedicated_ips"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: enable_dedicated_ips must be an bool"
            )
        if "http_auth_username" in params and not isinstance(
            params["http_auth_username"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: http_auth_username must be an str"
            )
        if "http_auth_password" in params and not isinstance(
            params["http_auth_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: http_auth_password must be an str"
            )
        if "mdn_validation_level" in params and not isinstance(
            params["mdn_validation_level"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: mdn_validation_level must be an str"
            )
        if "signature_validation_level" in params and not isinstance(
            params["signature_validation_level"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: signature_validation_level must be an str"
            )
        if "server_certificate" in params and not isinstance(
            params["server_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: server_certificate must be an str"
            )
        if "default_mime_type" in params and not isinstance(
            params["default_mime_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: default_mime_type must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "uri" in params and not isinstance(params["uri"], str):
            raise InvalidParameterError("Bad parameter: uri must be an str")
        if "public_certificate" in params and not isinstance(
            params["public_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: public_certificate must be an str"
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
            "PATCH", "/as2_partners/" + path_value(params["id"]), params
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
            "DELETE", "/as2_partners/" + path_value(params["id"]), params
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
            new_obj = As2PartnerResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class As2PartnerResource:
    """As2Partner operations that use one client's configuration.

    Get one from a client, such as ``client.as2_partner``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[As2Partner]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `as2_station_id` or `name`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `as2_station_id` and `workspace_id`. Valid field combinations are `[ workspace_id, as2_station_id ]`.
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
        return ListObj(As2Partner, "GET", "/as2_partners", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[As2Partner]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> As2Partner:
        """Parameters:
        id (required) - int64 - As2 Partner ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> As2Partner:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/as2_partners/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, As2Partner)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> As2Partner:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> As2Partner:
        """Parameters:
        enable_dedicated_ips - boolean - If `true`, we will use your site's dedicated IPs for all outbound connections to this AS2 Partner.
        http_auth_username - string - Username to send to server for HTTP Authentication.
        http_auth_password - string - Password to send to server for HTTP Authentication.
        mdn_validation_level - string - How should Files.com evaluate message transfer success based on a partner's MDN response?  This setting does not affect MDN storage; all MDNs received from a partner are always stored. `none`: MDN is stored for informational purposes only, a successful HTTPS transfer is a successful AS2 transfer. `weak`: Inspect the MDN for MIC and Disposition only. `normal`: `weak` plus validate MDN signature matches body, `strict`: `normal` but do not allow signatures from self-signed or incorrectly purposed certificates. `auto`: Automatically set the correct value for this setting based on next mdn received.
        signature_validation_level - string - Should Files.com require signatures on incoming AS2 messages?  `normal`: require that incoming messages are signed with a valid matching signature. `none`: Unsigned incoming messages are allowed. `auto`: A one-time starting state. The next message received is always accepted and switches this to `normal` if it carries a valid signature, or `none` if it does not.
        server_certificate - string - Should we require that the remote HTTP server have a valid SSL Certificate for HTTPS? (This only applies to Outgoing AS2 message from Files.com to a Partner.)
        default_mime_type - string - Default mime type of the file attached to the encrypted message
        additional_http_headers - object - Additional HTTP Headers for outgoing message sent to this partner.
        as2_station_id (required) - int64 - ID of the AS2 Station associated with this partner.
        name (required) - string - The partner's formal AS2 name.
        uri (required) - string - Public URI where we will send the AS2 messages (via HTTP/HTTPS).
        public_certificate - string - Public certificate for AS2 Partner.  Note: This is the certificate for AS2 message security, not a certificate used for HTTPS authentication.
        pkcs12 - string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the partner's public certificate. Provide this instead of public_certificate. Any private key in the file is discarded. A public-only file must contain exactly one certificate.
        pkcs12_password - string - Password for pkcs12. The file and password are used only for import; the extracted public certificate is stored as PEM.
        """
        params = copy_params(params)
        if "enable_dedicated_ips" in params and not isinstance(
            params["enable_dedicated_ips"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: enable_dedicated_ips must be an bool"
            )
        if "http_auth_username" in params and not isinstance(
            params["http_auth_username"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: http_auth_username must be an str"
            )
        if "http_auth_password" in params and not isinstance(
            params["http_auth_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: http_auth_password must be an str"
            )
        if "mdn_validation_level" in params and not isinstance(
            params["mdn_validation_level"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: mdn_validation_level must be an str"
            )
        if "signature_validation_level" in params and not isinstance(
            params["signature_validation_level"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: signature_validation_level must be an str"
            )
        if "server_certificate" in params and not isinstance(
            params["server_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: server_certificate must be an str"
            )
        if "default_mime_type" in params and not isinstance(
            params["default_mime_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: default_mime_type must be an str"
            )
        if "additional_http_headers" in params and not isinstance(
            params["additional_http_headers"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: additional_http_headers must be an dict"
            )
        if "as2_station_id" in params and (
            not isinstance(params["as2_station_id"], int)
            or isinstance(params["as2_station_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: as2_station_id must be an int"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "uri" in params and not isinstance(params["uri"], str):
            raise InvalidParameterError("Bad parameter: uri must be an str")
        if "public_certificate" in params and not isinstance(
            params["public_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: public_certificate must be an str"
            )
        if "pkcs12" in params and not isinstance(params["pkcs12"], str):
            raise InvalidParameterError("Bad parameter: pkcs12 must be an str")
        if "pkcs12_password" in params and not isinstance(
            params["pkcs12_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: pkcs12_password must be an str"
            )
        if "as2_station_id" not in params:
            raise MissingParameterError("Parameter missing: as2_station_id")
        if "name" not in params:
            raise MissingParameterError("Parameter missing: name")
        if "uri" not in params:
            raise MissingParameterError("Parameter missing: uri")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/as2_partners", params)
        return operation.decode_model(response, As2Partner)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> As2Partner:
        """Parameters:
        enable_dedicated_ips - boolean - If `true`, we will use your site's dedicated IPs for all outbound connections to this AS2 Partner.
        http_auth_username - string - Username to send to server for HTTP Authentication.
        http_auth_password - string - Password to send to server for HTTP Authentication.
        mdn_validation_level - string - How should Files.com evaluate message transfer success based on a partner's MDN response?  This setting does not affect MDN storage; all MDNs received from a partner are always stored. `none`: MDN is stored for informational purposes only, a successful HTTPS transfer is a successful AS2 transfer. `weak`: Inspect the MDN for MIC and Disposition only. `normal`: `weak` plus validate MDN signature matches body, `strict`: `normal` but do not allow signatures from self-signed or incorrectly purposed certificates. `auto`: Automatically set the correct value for this setting based on next mdn received.
        signature_validation_level - string - Should Files.com require signatures on incoming AS2 messages?  `normal`: require that incoming messages are signed with a valid matching signature. `none`: Unsigned incoming messages are allowed. `auto`: A one-time starting state. The next message received is always accepted and switches this to `normal` if it carries a valid signature, or `none` if it does not.
        server_certificate - string - Should we require that the remote HTTP server have a valid SSL Certificate for HTTPS? (This only applies to Outgoing AS2 message from Files.com to a Partner.)
        default_mime_type - string - Default mime type of the file attached to the encrypted message
        additional_http_headers - object - Additional HTTP Headers for outgoing message sent to this partner.
        name - string - The partner's formal AS2 name.
        uri - string - Public URI where we will send the AS2 messages (via HTTP/HTTPS).
        public_certificate - string - Public certificate for AS2 Partner.  Note: This is the certificate for AS2 message security, not a certificate used for HTTPS authentication.
        pkcs12 - string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the partner's public certificate. Provide this instead of public_certificate. Any private key in the file is discarded. A public-only file must contain exactly one certificate.
        pkcs12_password - string - Password for pkcs12. The file and password are used only for import; the extracted public certificate is stored as PEM.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> As2Partner:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "enable_dedicated_ips" in params and not isinstance(
            params["enable_dedicated_ips"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: enable_dedicated_ips must be an bool"
            )
        if "http_auth_username" in params and not isinstance(
            params["http_auth_username"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: http_auth_username must be an str"
            )
        if "http_auth_password" in params and not isinstance(
            params["http_auth_password"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: http_auth_password must be an str"
            )
        if "mdn_validation_level" in params and not isinstance(
            params["mdn_validation_level"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: mdn_validation_level must be an str"
            )
        if "signature_validation_level" in params and not isinstance(
            params["signature_validation_level"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: signature_validation_level must be an str"
            )
        if "server_certificate" in params and not isinstance(
            params["server_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: server_certificate must be an str"
            )
        if "default_mime_type" in params and not isinstance(
            params["default_mime_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: default_mime_type must be an str"
            )
        if "additional_http_headers" in params and not isinstance(
            params["additional_http_headers"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: additional_http_headers must be an dict"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "uri" in params and not isinstance(params["uri"], str):
            raise InvalidParameterError("Bad parameter: uri must be an str")
        if "public_certificate" in params and not isinstance(
            params["public_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: public_certificate must be an str"
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
            "PATCH", "/as2_partners/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, As2Partner)

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
            "DELETE", "/as2_partners/" + path_value(params["id"]), params
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
    ) -> As2Partner:
        """A new As2Partner with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = As2Partner(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = As2PartnerResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[As2Partner]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `as2_station_id` or `name`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `as2_station_id` and `workspace_id`. Valid field combinations are `[ workspace_id, as2_station_id ]`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[As2Partner]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> As2Partner:
    """Parameters:
    id (required) - int64 - As2 Partner ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> As2Partner:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> As2Partner:
    """Parameters:
    enable_dedicated_ips - boolean - If `true`, we will use your site's dedicated IPs for all outbound connections to this AS2 Partner.
    http_auth_username - string - Username to send to server for HTTP Authentication.
    http_auth_password - string - Password to send to server for HTTP Authentication.
    mdn_validation_level - string - How should Files.com evaluate message transfer success based on a partner's MDN response?  This setting does not affect MDN storage; all MDNs received from a partner are always stored. `none`: MDN is stored for informational purposes only, a successful HTTPS transfer is a successful AS2 transfer. `weak`: Inspect the MDN for MIC and Disposition only. `normal`: `weak` plus validate MDN signature matches body, `strict`: `normal` but do not allow signatures from self-signed or incorrectly purposed certificates. `auto`: Automatically set the correct value for this setting based on next mdn received.
    signature_validation_level - string - Should Files.com require signatures on incoming AS2 messages?  `normal`: require that incoming messages are signed with a valid matching signature. `none`: Unsigned incoming messages are allowed. `auto`: A one-time starting state. The next message received is always accepted and switches this to `normal` if it carries a valid signature, or `none` if it does not.
    server_certificate - string - Should we require that the remote HTTP server have a valid SSL Certificate for HTTPS? (This only applies to Outgoing AS2 message from Files.com to a Partner.)
    default_mime_type - string - Default mime type of the file attached to the encrypted message
    additional_http_headers - object - Additional HTTP Headers for outgoing message sent to this partner.
    as2_station_id (required) - int64 - ID of the AS2 Station associated with this partner.
    name (required) - string - The partner's formal AS2 name.
    uri (required) - string - Public URI where we will send the AS2 messages (via HTTP/HTTPS).
    public_certificate - string - Public certificate for AS2 Partner.  Note: This is the certificate for AS2 message security, not a certificate used for HTTPS authentication.
    pkcs12 - string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the partner's public certificate. Provide this instead of public_certificate. Any private key in the file is discarded. A public-only file must contain exactly one certificate.
    pkcs12_password - string - Password for pkcs12. The file and password are used only for import; the extracted public certificate is stored as PEM.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> As2Partner:
    """Parameters:
    enable_dedicated_ips - boolean - If `true`, we will use your site's dedicated IPs for all outbound connections to this AS2 Partner.
    http_auth_username - string - Username to send to server for HTTP Authentication.
    http_auth_password - string - Password to send to server for HTTP Authentication.
    mdn_validation_level - string - How should Files.com evaluate message transfer success based on a partner's MDN response?  This setting does not affect MDN storage; all MDNs received from a partner are always stored. `none`: MDN is stored for informational purposes only, a successful HTTPS transfer is a successful AS2 transfer. `weak`: Inspect the MDN for MIC and Disposition only. `normal`: `weak` plus validate MDN signature matches body, `strict`: `normal` but do not allow signatures from self-signed or incorrectly purposed certificates. `auto`: Automatically set the correct value for this setting based on next mdn received.
    signature_validation_level - string - Should Files.com require signatures on incoming AS2 messages?  `normal`: require that incoming messages are signed with a valid matching signature. `none`: Unsigned incoming messages are allowed. `auto`: A one-time starting state. The next message received is always accepted and switches this to `normal` if it carries a valid signature, or `none` if it does not.
    server_certificate - string - Should we require that the remote HTTP server have a valid SSL Certificate for HTTPS? (This only applies to Outgoing AS2 message from Files.com to a Partner.)
    default_mime_type - string - Default mime type of the file attached to the encrypted message
    additional_http_headers - object - Additional HTTP Headers for outgoing message sent to this partner.
    name - string - The partner's formal AS2 name.
    uri - string - Public URI where we will send the AS2 messages (via HTTP/HTTPS).
    public_certificate - string - Public certificate for AS2 Partner.  Note: This is the certificate for AS2 message security, not a certificate used for HTTPS authentication.
    pkcs12 - string - Base64-encoded PKCS#12 (.pfx or .p12) file containing the partner's public certificate. Provide this instead of public_certificate. Any private key in the file is discarded. A public-only file must contain exactly one certificate.
    pkcs12_password - string - Password for pkcs12. The file and password are used only for import; the extracted public certificate is stored as PEM.
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


def new(*args, **kwargs) -> As2Partner:
    return As2Partner(*args, **kwargs)
