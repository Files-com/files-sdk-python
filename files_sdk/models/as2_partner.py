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
        "id": None,  # int64 - Id of the AS2 Partner.
        "as2_station_id": None,  # int64 - Id of the AS2 Station associated with this partner.
        "name": None,  # string - The partner's formal AS2 name.
        "uri": None,  # string - Public URI for sending AS2 message to.
        "server_certificate": None,  # string - Remote server certificate security setting
        "enable_dedicated_ips": None,  # boolean - `true` if remote server only accepts connections from dedicated IPs
        "hex_public_certificate_serial": None,  # string - Serial of public certificate used for message security in hex format.
        "public_certificate_md5": None,  # string - MD5 hash of public certificate used for message security.
        "public_certificate_subject": None,  # string - Subject of public certificate used for message security.
        "public_certificate_issuer": None,  # string - Issuer of public certificate used for message security.
        "public_certificate_serial": None,  # string - Serial of public certificate used for message security.
        "public_certificate_not_before": None,  # string - Not before value of public certificate used for message security.
        "public_certificate_not_after": None,  # string - Not after value of public certificate used for message security.
        "public_certificate": None,  # string
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
    #   name - string - AS2 Name
    #   uri - string - URL base for AS2 responses
    #   server_certificate - string - Remote server certificate security setting
    #   public_certificate - string
    #   enable_dedicated_ips - boolean
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
        if "uri" in params and not isinstance(params["uri"], str):
            raise InvalidParameterError("Bad parameter: uri must be an str")
        if "server_certificate" in params and not isinstance(
            params["server_certificate"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: server_certificate must be an str"
            )
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
        response, _options = Api.send_request(
            "DELETE",
            "/as2_partners/{id}".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())


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
#   name (required) - string - AS2 Name
#   uri (required) - string - URL base for AS2 responses
#   public_certificate (required) - string
#   as2_station_id (required) - int64 - Id of As2Station for this partner
#   server_certificate - string - Remote server certificate security setting
#   enable_dedicated_ips - boolean
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
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
    if "as2_station_id" in params and not isinstance(
        params["as2_station_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: as2_station_id must be an int"
        )
    if "server_certificate" in params and not isinstance(
        params["server_certificate"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: server_certificate must be an str"
        )
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    if "uri" not in params:
        raise MissingParameterError("Parameter missing: uri")
    if "public_certificate" not in params:
        raise MissingParameterError("Parameter missing: public_certificate")
    if "as2_station_id" not in params:
        raise MissingParameterError("Parameter missing: as2_station_id")
    response, options = Api.send_request(
        "POST", "/as2_partners", params, options
    )
    return As2Partner(response.data, options)


# Parameters:
#   name - string - AS2 Name
#   uri - string - URL base for AS2 responses
#   server_certificate - string - Remote server certificate security setting
#   public_certificate - string
#   enable_dedicated_ips - boolean
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
    if "uri" in params and not isinstance(params["uri"], str):
        raise InvalidParameterError("Bad parameter: uri must be an str")
    if "server_certificate" in params and not isinstance(
        params["server_certificate"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: server_certificate must be an str"
        )
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
    response, _options = Api.send_request(
        "DELETE", "/as2_partners/{id}".format(id=params["id"]), params, options
    )
    return response.data


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return As2Partner(*args, **kwargs)
