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


class Certificate:
    """A certificate record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Certificate ID
        name: string - Descriptive name of certificate
        custom_domain_id: int64 - Custom Domain that owns this certificate, including while the certificate is inactive.
        certificate: string - Full text of SSL certificate
        created_at: date-time - Certificate created at
        display_status: string - Certificate status. (One of `Request Generated`, `New`, `Active`, `Active/Expired`, `Expired`, or `Available`)
        domains: array(string) - Domains on this certificate other than files.com domains
        expires_at: date-time - Certificate expiration date/time
        brick_managed: boolean - Is this certificate automatically managed and renewed by Files.com?
        intermediates: string - Intermediate certificates
        ip_addresses: array(string) - A list of IP addresses associated with this SSL Certificate
        issuer: string - X509 issuer
        key_type: string - Type of key
        request: string - Certificate signing request text
        status: string - Certificate status (Request Generated, New, Active, Active/Expired, Expired, or Available)
        subject: string - X509 Subject name
        certificate_domain: string - Domain for certificate.
        certificate_extra_domains: array(string) - Additional domains for the certificate CSR.
        certificate_country: string - Country.
        certificate_state_or_province: string - State or province.
        certificate_city_or_locale: string - City or locale.
        certificate_company_name: string - Company name.
        csr_ou1: string - Department name or organization unit 1
        csr_ou2: string - Department name or organization unit 2
        csr_ou3: string - Department name or organization unit 3
        certificate_email_address: string - Email address for the certificate owner.
        private_key: string - Certificate private key.
        password: string - Certificate password.
    """

    default_attributes = {
        "id": None,  # int64 - Certificate ID
        "name": None,  # string - Descriptive name of certificate
        "custom_domain_id": None,  # int64 - Custom Domain that owns this certificate, including while the certificate is inactive.
        "certificate": None,  # string - Full text of SSL certificate
        "created_at": None,  # date-time - Certificate created at
        "display_status": None,  # string - Certificate status. (One of `Request Generated`, `New`, `Active`, `Active/Expired`, `Expired`, or `Available`)
        "domains": None,  # array(string) - Domains on this certificate other than files.com domains
        "expires_at": None,  # date-time - Certificate expiration date/time
        "brick_managed": None,  # boolean - Is this certificate automatically managed and renewed by Files.com?
        "intermediates": None,  # string - Intermediate certificates
        "ip_addresses": None,  # array(string) - A list of IP addresses associated with this SSL Certificate
        "issuer": None,  # string - X509 issuer
        "key_type": None,  # string - Type of key
        "request": None,  # string - Certificate signing request text
        "status": None,  # string - Certificate status (Request Generated, New, Active, Active/Expired, Expired, or Available)
        "subject": None,  # string - X509 Subject name
        "certificate_domain": None,  # string - Domain for certificate.
        "certificate_extra_domains": None,  # array(string) - Additional domains for the certificate CSR.
        "certificate_country": None,  # string - Country.
        "certificate_state_or_province": None,  # string - State or province.
        "certificate_city_or_locale": None,  # string - City or locale.
        "certificate_company_name": None,  # string - Company name.
        "csr_ou1": None,  # string - Department name or organization unit 1
        "csr_ou2": None,  # string - Department name or organization unit 2
        "csr_ou3": None,  # string - Department name or organization unit 3
        "certificate_email_address": None,  # string - Email address for the certificate owner.
        "private_key": None,  # string - Certificate private key.
        "password": None,  # string - Certificate password.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    name: str | None
    custom_domain_id: int | None
    certificate: str | None
    created_at: str | None
    display_status: str | None
    domains: builtins.list[str] | None
    expires_at: str | None
    brick_managed: bool | None
    intermediates: str | None
    ip_addresses: builtins.list[str] | None
    issuer: str | None
    key_type: str | None
    request: str | None
    status: str | None
    subject: str | None
    certificate_domain: str | None
    certificate_extra_domains: builtins.list[str] | None
    certificate_country: str | None
    certificate_state_or_province: str | None
    certificate_city_or_locale: str | None
    certificate_company_name: str | None
    csr_ou1: str | None
    csr_ou2: str | None
    csr_ou3: str | None
    certificate_email_address: str | None
    private_key: str | None
    password: str | None

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
        for attribute, default_value in Certificate.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Certificate.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def activate(self, params: dict[str, Any] | None = None) -> None:
        """Activate SSL Certificate

        Parameters:
          replace_cert - string - Leave blank or set to `any` to replace any currently active certificate, if applicable.  Set to `new_ips` to activate this certificate as an additional certificate on your Site by allocating a new set of Dedicated IPs (may require a Plan upgrade).  Set to the ID of a currently active certificate to replace that certificate on its set of dedicated IPs.  A certificate belonging to a Custom Domain activates only for that domain: leave blank, use `any`, or specify that domain's current certificate ID.
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
        if "replace_cert" in params and not isinstance(
            params["replace_cert"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: replace_cert must be an str"
            )
        operation = Operation.start(self._scope())
        operation.request(
            "POST",
            "/certificates/" + path_value(params["id"]) + "/activate",
            params,
        )

    def deactivate(self, params: dict[str, Any] | None = None) -> None:
        """Deactivate SSL Certificate"""
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
            "POST",
            "/certificates/" + path_value(params["id"]) + "/deactivate",
            params,
        )

    def replace_with_files(self, params: dict[str, Any] | None = None) -> None:
        """Replace this active custom SSL Certificate for the Primary Custom Domain with a Files.com SSL Certificate.  The Primary Custom Domain's CNAME record must point at the Site's subdomain.  The Files.com certificate is issued and activated in the background"""
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
            "POST",
            "/certificates/"
            + path_value(params["id"])
            + "/replace_with_files_certificate",
            params,
        )

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          name - string - Internal certificate name.
          intermediates - string - Any intermediate certificates.  PEM or PKCS7 formats accepted.
          certificate - string - The certificate.  PEM or PKCS7 formats accepted.
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
        if "intermediates" in params and not isinstance(
            params["intermediates"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: intermediates must be an str"
            )
        if "certificate" in params and not isinstance(
            params["certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: certificate must be an str"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/certificates/" + path_value(params["id"]), params
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
            "DELETE", "/certificates/" + path_value(params["id"]), params
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
            new_obj = CertificateResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class CertificateResource:
    """Certificate operations that use one client's configuration.

    Get one from a client, such as ``client.certificate``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Certificate]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
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
        operation = Operation.start(self._scope, options)
        return ListObj(Certificate, "GET", "/certificates", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Certificate]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Certificate:
        """Parameters:
        id (required) - int64 - Certificate ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Certificate:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/certificates/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Certificate)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Certificate:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Certificate:
        """Parameters:
        name (required) - string - Internal name of the SSL certificate.
        certificate_domain - string - Domain for certificate.
        certificate_extra_domains - array(string) - Additional domains for the certificate CSR.
        certificate_country - string - Country.
        certificate_state_or_province - string - State or province.
        certificate_city_or_locale - string - City or locale.
        certificate_company_name - string - Company name.
        csr_ou1 - string - Department name or organization unit 1
        csr_ou2 - string - Department name or organization unit 2
        csr_ou3 - string - Department name or organization unit 3
        certificate_email_address - string - Email address for the certificate owner.
        key_type - string - Any supported key type.  Defaults to `RSA-4096`.
        certificate - string - The certificate.  PEM or PKCS7 formats accepted.
        private_key - string - Certificate private key.
        password - string - Certificate password.
        intermediates - string - Intermediate certificates.  PEM or PKCS7 formats accepted.
        """
        params = copy_params(params)
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "certificate_domain" in params and not isinstance(
            params["certificate_domain"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: certificate_domain must be an str"
            )
        if "certificate_extra_domains" in params and not isinstance(
            params["certificate_extra_domains"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: certificate_extra_domains must be an list"
            )
        if "certificate_country" in params and not isinstance(
            params["certificate_country"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: certificate_country must be an str"
            )
        if "certificate_state_or_province" in params and not isinstance(
            params["certificate_state_or_province"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: certificate_state_or_province must be an str"
            )
        if "certificate_city_or_locale" in params and not isinstance(
            params["certificate_city_or_locale"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: certificate_city_or_locale must be an str"
            )
        if "certificate_company_name" in params and not isinstance(
            params["certificate_company_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: certificate_company_name must be an str"
            )
        if "csr_ou1" in params and not isinstance(params["csr_ou1"], str):
            raise InvalidParameterError(
                "Bad parameter: csr_ou1 must be an str"
            )
        if "csr_ou2" in params and not isinstance(params["csr_ou2"], str):
            raise InvalidParameterError(
                "Bad parameter: csr_ou2 must be an str"
            )
        if "csr_ou3" in params and not isinstance(params["csr_ou3"], str):
            raise InvalidParameterError(
                "Bad parameter: csr_ou3 must be an str"
            )
        if "certificate_email_address" in params and not isinstance(
            params["certificate_email_address"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: certificate_email_address must be an str"
            )
        if "key_type" in params and not isinstance(params["key_type"], str):
            raise InvalidParameterError(
                "Bad parameter: key_type must be an str"
            )
        if "certificate" in params and not isinstance(
            params["certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: certificate must be an str"
            )
        if "private_key" in params and not isinstance(
            params["private_key"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: private_key must be an str"
            )
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError(
                "Bad parameter: password must be an str"
            )
        if "intermediates" in params and not isinstance(
            params["intermediates"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: intermediates must be an str"
            )
        if "name" not in params:
            raise MissingParameterError("Parameter missing: name")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/certificates", params)
        return operation.decode_model(response, Certificate)

    def activate(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Activate SSL Certificate

        Parameters:
          replace_cert - string - Leave blank or set to `any` to replace any currently active certificate, if applicable.  Set to `new_ips` to activate this certificate as an additional certificate on your Site by allocating a new set of Dedicated IPs (may require a Plan upgrade).  Set to the ID of a currently active certificate to replace that certificate on its set of dedicated IPs.  A certificate belonging to a Custom Domain activates only for that domain: leave blank, use `any`, or specify that domain's current certificate ID.
        """
        return self.__activate({"id": id}, params, options)

    def __activate(
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
        if "replace_cert" in params and not isinstance(
            params["replace_cert"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: replace_cert must be an str"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "POST",
            "/certificates/" + path_value(params["id"]) + "/activate",
            params,
        )

    def deactivate(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Deactivate SSL Certificate"""
        return self.__deactivate({"id": id}, params, options)

    def __deactivate(
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
            "POST",
            "/certificates/" + path_value(params["id"]) + "/deactivate",
            params,
        )

    def replace_with_files(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Replace this active custom SSL Certificate for the Primary Custom Domain with a Files.com SSL Certificate.  The Primary Custom Domain's CNAME record must point at the Site's subdomain.  The Files.com certificate is issued and activated in the background"""
        return self.__replace_with_files({"id": id}, params, options)

    def __replace_with_files(
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
            "POST",
            "/certificates/"
            + path_value(params["id"])
            + "/replace_with_files_certificate",
            params,
        )

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Certificate:
        """Parameters:
        name - string - Internal certificate name.
        intermediates - string - Any intermediate certificates.  PEM or PKCS7 formats accepted.
        certificate - string - The certificate.  PEM or PKCS7 formats accepted.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Certificate:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "intermediates" in params and not isinstance(
            params["intermediates"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: intermediates must be an str"
            )
        if "certificate" in params and not isinstance(
            params["certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: certificate must be an str"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/certificates/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Certificate)

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
            "DELETE", "/certificates/" + path_value(params["id"]), params
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
    ) -> Certificate:
        """A new Certificate with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Certificate(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = CertificateResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Certificate]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Certificate]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Certificate:
    """Parameters:
    id (required) - int64 - Certificate ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Certificate:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Certificate:
    """Parameters:
    name (required) - string - Internal name of the SSL certificate.
    certificate_domain - string - Domain for certificate.
    certificate_extra_domains - array(string) - Additional domains for the certificate CSR.
    certificate_country - string - Country.
    certificate_state_or_province - string - State or province.
    certificate_city_or_locale - string - City or locale.
    certificate_company_name - string - Company name.
    csr_ou1 - string - Department name or organization unit 1
    csr_ou2 - string - Department name or organization unit 2
    csr_ou3 - string - Department name or organization unit 3
    certificate_email_address - string - Email address for the certificate owner.
    key_type - string - Any supported key type.  Defaults to `RSA-4096`.
    certificate - string - The certificate.  PEM or PKCS7 formats accepted.
    private_key - string - Certificate private key.
    password - string - Certificate password.
    intermediates - string - Intermediate certificates.  PEM or PKCS7 formats accepted.
    """
    return _legacy_resource.create(params, options)


def activate(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Activate SSL Certificate

    Parameters:
      replace_cert - string - Leave blank or set to `any` to replace any currently active certificate, if applicable.  Set to `new_ips` to activate this certificate as an additional certificate on your Site by allocating a new set of Dedicated IPs (may require a Plan upgrade).  Set to the ID of a currently active certificate to replace that certificate on its set of dedicated IPs.  A certificate belonging to a Custom Domain activates only for that domain: leave blank, use `any`, or specify that domain's current certificate ID.
    """
    _legacy_resource.activate(id, params, options)


def deactivate(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Deactivate SSL Certificate"""
    _legacy_resource.deactivate(id, params, options)


def replace_with_files(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Replace this active custom SSL Certificate for the Primary Custom Domain with a Files.com SSL Certificate.  The Primary Custom Domain's CNAME record must point at the Site's subdomain.  The Files.com certificate is issued and activated in the background"""
    _legacy_resource.replace_with_files(id, params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Certificate:
    """Parameters:
    name - string - Internal certificate name.
    intermediates - string - Any intermediate certificates.  PEM or PKCS7 formats accepted.
    certificate - string - The certificate.  PEM or PKCS7 formats accepted.
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


def new(*args, **kwargs) -> Certificate:
    return Certificate(*args, **kwargs)
