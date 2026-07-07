import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Certificate:
    default_attributes = {
        "id": None,  # int64 - Certificate ID
        "name": None,  # string - Descriptive name of certificate
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

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

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

    # Deactivate SSL Certificate
    def deactivate(self, params=None):
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
            "POST",
            "/certificates/{id}/deactivate".format(
                id=quote(str(params["id"]), safe="")
            ),
            params,
            self.options,
        )

    # Activate SSL Certificate
    #
    # Parameters:
    #   replace_cert - string - Leave blank or set to `any` to replace any currently active certificate, if applicable.  Set to `new_ips` to activate this certificate as an additional certificate on your Site by allocating a new set of Dedicated IPs (may require a Plan upgrade).  Set to the ID of a currently active certificate to replace that certificate on its set of dedicated IPs.
    def activate(self, params=None):
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
        if "replace_cert" in params and not isinstance(
            params["replace_cert"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: replace_cert must be an str"
            )
        Api.send_request(
            "POST",
            "/certificates/{id}/activate".format(
                id=quote(str(params["id"]), safe="")
            ),
            params,
            self.options,
        )

    # Parameters:
    #   name - string - Internal certificate name.
    #   intermediates - string - Any intermediate certificates.  PEM or PKCS7 formats accepted.
    #   certificate - string - The certificate.  PEM or PKCS7 formats accepted.
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
        response, _options = Api.send_request(
            "PATCH",
            "/certificates/{id}".format(id=quote(str(params["id"]), safe="")),
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
            "/certificates/{id}".format(id=quote(str(params["id"]), safe="")),
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
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(Certificate, "GET", "/certificates", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Certificate ID.
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
        "/certificates/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return Certificate(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   name (required) - string - Internal name of the SSL certificate.
#   certificate_domain - string - Domain for certificate.
#   certificate_extra_domains - array(string) - Additional domains for the certificate CSR.
#   certificate_country - string - Country.
#   certificate_state_or_province - string - State or province.
#   certificate_city_or_locale - string - City or locale.
#   certificate_company_name - string - Company name.
#   csr_ou1 - string - Department name or organization unit 1
#   csr_ou2 - string - Department name or organization unit 2
#   csr_ou3 - string - Department name or organization unit 3
#   certificate_email_address - string - Email address for the certificate owner.
#   key_type - string - Any supported key type.  Defaults to `RSA-4096`.
#   certificate - string - The certificate.  PEM or PKCS7 formats accepted.
#   private_key - string - Certificate private key.
#   password - string - Certificate password.
#   intermediates - string - Intermediate certificates.  PEM or PKCS7 formats accepted.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
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
        raise InvalidParameterError("Bad parameter: csr_ou1 must be an str")
    if "csr_ou2" in params and not isinstance(params["csr_ou2"], str):
        raise InvalidParameterError("Bad parameter: csr_ou2 must be an str")
    if "csr_ou3" in params and not isinstance(params["csr_ou3"], str):
        raise InvalidParameterError("Bad parameter: csr_ou3 must be an str")
    if "certificate_email_address" in params and not isinstance(
        params["certificate_email_address"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: certificate_email_address must be an str"
        )
    if "key_type" in params and not isinstance(params["key_type"], str):
        raise InvalidParameterError("Bad parameter: key_type must be an str")
    if "certificate" in params and not isinstance(params["certificate"], str):
        raise InvalidParameterError(
            "Bad parameter: certificate must be an str"
        )
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError(
            "Bad parameter: private_key must be an str"
        )
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "intermediates" in params and not isinstance(
        params["intermediates"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: intermediates must be an str"
        )
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    response, options = Api.send_request(
        "POST", "/certificates", params, options
    )
    return Certificate(response.data, options)


# Deactivate SSL Certificate
def deactivate(id, params=None, options=None):
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
        "POST",
        "/certificates/{id}/deactivate".format(
            id=quote(str(params["id"]), safe="")
        ),
        params,
        options,
    )


# Activate SSL Certificate
#
# Parameters:
#   replace_cert - string - Leave blank or set to `any` to replace any currently active certificate, if applicable.  Set to `new_ips` to activate this certificate as an additional certificate on your Site by allocating a new set of Dedicated IPs (may require a Plan upgrade).  Set to the ID of a currently active certificate to replace that certificate on its set of dedicated IPs.
def activate(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "replace_cert" in params and not isinstance(
        params["replace_cert"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: replace_cert must be an str"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    Api.send_request(
        "POST",
        "/certificates/{id}/activate".format(
            id=quote(str(params["id"]), safe="")
        ),
        params,
        options,
    )


def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, options = Api.send_request(
        "POST", "/certificates/create_export", params, options
    )
    return Export(response.data, options)


# Parameters:
#   name - string - Internal certificate name.
#   intermediates - string - Any intermediate certificates.  PEM or PKCS7 formats accepted.
#   certificate - string - The certificate.  PEM or PKCS7 formats accepted.
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
    if "intermediates" in params and not isinstance(
        params["intermediates"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: intermediates must be an str"
        )
    if "certificate" in params and not isinstance(params["certificate"], str):
        raise InvalidParameterError(
            "Bad parameter: certificate must be an str"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/certificates/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return Certificate(response.data, options)


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
        "/certificates/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return Certificate(*args, **kwargs)
