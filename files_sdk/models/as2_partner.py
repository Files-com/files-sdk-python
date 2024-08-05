import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class As2Partner:
    default_attributes = {
        "id": None,  # int64 - ID of the AS2 Partner.
        "as2_station_id": None,  # int64 - ID of the AS2 Station associated with this partner.
        "name": None,  # string - The partner's formal AS2 name.
        "uri": None,  # string - Public URI where we will send the AS2 messages (via HTTP/HTTPS).
        "server_certificate": None,  # string - Should we require that the remote HTTP server have a valid SSL Certificate for HTTPS?
        "http_auth_username": None,  # string - Username to send to server for HTTP Authentication.
        "mdn_validation_level": None,  # string - How should Files.com evaluate message transfer success based on a partner's MDN response?  This setting does not affect MDN storage; all MDNs received from a partner are always stored. `none`: MDN is stored for informational purposes only, a successful HTTPS transfer is a successful AS2 transfer. `weak`: Inspect the MDN for MIC and Disposition only. `normal`: `weak` plus validate MDN signature matches body, `strict`: `normal` but do not allow signatures from self-signed or incorrectly purposed certificates.
        "enable_dedicated_ips": None,  # boolean - If `true`, we will use your site's dedicated IPs for all outbound connections to this AS2 PArtner.
        "hex_public_certificate_serial": None,  # string - Serial of public certificate used for message security in hex format.
        "public_certificate_md5": None,  # string - MD5 hash of public certificate used for message security.
        "public_certificate_subject": None,  # string - Subject of public certificate used for message security.
        "public_certificate_issuer": None,  # string - Issuer of public certificate used for message security.
        "public_certificate_serial": None,  # string - Serial of public certificate used for message security.
        "public_certificate_not_before": None,  # string - Not before value of public certificate used for message security.
        "public_certificate_not_after": None,  # string - Not after value of public certificate used for message security.
        "http_auth_password": None,  # string - Password to send to server for HTTP Authentication.
        "public_certificate": None,  # string - Public certificate for AS2 Partner.  Note: This is the certificate for AS2 message security, not a certificate used for HTTPS authentication.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in As2Partner.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in As2Partner.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   enable_dedicated_ips - boolean - If `true`, we will use your site's dedicated IPs for all outbound connections to this AS2 PArtner.
    #   http_auth_username - string - Username to send to server for HTTP Authentication.
    #   http_auth_password - string - Password to send to server for HTTP Authentication.
    #   mdn_validation_level - string - How should Files.com evaluate message transfer success based on a partner's MDN response?  This setting does not affect MDN storage; all MDNs received from a partner are always stored. `none`: MDN is stored for informational purposes only, a successful HTTPS transfer is a successful AS2 transfer. `weak`: Inspect the MDN for MIC and Disposition only. `normal`: `weak` plus validate MDN signature matches body, `strict`: `normal` but do not allow signatures from self-signed or incorrectly purposed certificates.
    #   server_certificate - string - Should we require that the remote HTTP server have a valid SSL Certificate for HTTPS?
    #   name - string - The partner's formal AS2 name.
    #   uri - string - Public URI where we will send the AS2 messages (via HTTP/HTTPS).
    #   public_certificate - string - Public certificate for AS2 Partner.  Note: This is the certificate for AS2 message security, not a certificate used for HTTPS authentication.
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
        if "server_certificate" in params and not isinstance(
            params["server_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: server_certificate must be an str"
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
        response, _options = Api.send_request(
            "PATCH",
            "/as2_partners/{id}".format(id=params["id"]),
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
            "/as2_partners/{id}".format(id=params["id"]),
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
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(As2Partner, "GET", "/as2_partners", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - As2 Partner ID.
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
        "GET", "/as2_partners/{id}".format(id=params["id"]), params, options
    )
    return As2Partner(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   enable_dedicated_ips - boolean - If `true`, we will use your site's dedicated IPs for all outbound connections to this AS2 PArtner.
#   http_auth_username - string - Username to send to server for HTTP Authentication.
#   http_auth_password - string - Password to send to server for HTTP Authentication.
#   mdn_validation_level - string - How should Files.com evaluate message transfer success based on a partner's MDN response?  This setting does not affect MDN storage; all MDNs received from a partner are always stored. `none`: MDN is stored for informational purposes only, a successful HTTPS transfer is a successful AS2 transfer. `weak`: Inspect the MDN for MIC and Disposition only. `normal`: `weak` plus validate MDN signature matches body, `strict`: `normal` but do not allow signatures from self-signed or incorrectly purposed certificates.
#   server_certificate - string - Should we require that the remote HTTP server have a valid SSL Certificate for HTTPS?
#   as2_station_id (required) - int64 - ID of the AS2 Station associated with this partner.
#   name (required) - string - The partner's formal AS2 name.
#   uri (required) - string - Public URI where we will send the AS2 messages (via HTTP/HTTPS).
#   public_certificate (required) - string - Public certificate for AS2 Partner.  Note: This is the certificate for AS2 message security, not a certificate used for HTTPS authentication.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
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
    if "server_certificate" in params and not isinstance(
        params["server_certificate"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: server_certificate must be an str"
        )
    if "as2_station_id" in params and not isinstance(
        params["as2_station_id"], int
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
    if "as2_station_id" not in params:
        raise MissingParameterError("Parameter missing: as2_station_id")
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    if "uri" not in params:
        raise MissingParameterError("Parameter missing: uri")
    if "public_certificate" not in params:
        raise MissingParameterError("Parameter missing: public_certificate")
    response, options = Api.send_request(
        "POST", "/as2_partners", params, options
    )
    return As2Partner(response.data, options)


# Parameters:
#   enable_dedicated_ips - boolean - If `true`, we will use your site's dedicated IPs for all outbound connections to this AS2 PArtner.
#   http_auth_username - string - Username to send to server for HTTP Authentication.
#   http_auth_password - string - Password to send to server for HTTP Authentication.
#   mdn_validation_level - string - How should Files.com evaluate message transfer success based on a partner's MDN response?  This setting does not affect MDN storage; all MDNs received from a partner are always stored. `none`: MDN is stored for informational purposes only, a successful HTTPS transfer is a successful AS2 transfer. `weak`: Inspect the MDN for MIC and Disposition only. `normal`: `weak` plus validate MDN signature matches body, `strict`: `normal` but do not allow signatures from self-signed or incorrectly purposed certificates.
#   server_certificate - string - Should we require that the remote HTTP server have a valid SSL Certificate for HTTPS?
#   name - string - The partner's formal AS2 name.
#   uri - string - Public URI where we will send the AS2 messages (via HTTP/HTTPS).
#   public_certificate - string - Public certificate for AS2 Partner.  Note: This is the certificate for AS2 message security, not a certificate used for HTTPS authentication.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
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
    if "server_certificate" in params and not isinstance(
        params["server_certificate"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: server_certificate must be an str"
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
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH", "/as2_partners/{id}".format(id=params["id"]), params, options
    )
    return As2Partner(response.data, options)


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
        "DELETE", "/as2_partners/{id}".format(id=params["id"]), params, options
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return As2Partner(*args, **kwargs)
