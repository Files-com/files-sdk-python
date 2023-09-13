import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class As2Station:
    default_attributes = {
        "id": None,  # int64 - Id of the AS2 Station.
        "name": None,  # string - The station's formal AS2 name.
        "uri": None,  # string - Public URI for sending AS2 message to.
        "domain": None,  # string - The station's AS2 domain name.
        "hex_public_certificate_serial": None,  # string - Serial of public certificate used for message security in hex format.
        "public_certificate_md5": None,  # string - MD5 hash of public certificate used for message security.
        "private_key_md5": None,  # string - MD5 hash of private key used for message security.
        "public_certificate_subject": None,  # string - Subject of public certificate used for message security.
        "public_certificate_issuer": None,  # string - Issuer of public certificate used for message security.
        "public_certificate_serial": None,  # string - Serial of public certificate used for message security.
        "public_certificate_not_before": None,  # string - Not before value of public certificate used for message security.
        "public_certificate_not_after": None,  # string - Not after value of public certificate used for message security.
        "private_key_password_md5": None,  # string - MD5 hash of private key password used for message security.
        "public_certificate": None,  # string
        "private_key": None,  # string
        "private_key_password": None,  # string
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in As2Station.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in As2Station.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   name - string - AS2 Name
    #   public_certificate - string
    #   private_key - string
    #   private_key_password - string
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
        response, _options = Api.send_request(
            "PATCH",
            "/as2_stations/{id}".format(id=params["id"]),
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
            "/as2_stations/{id}".format(id=params["id"]),
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
    return ListObj(As2Station, "GET", "/as2_stations", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - As2 Station ID.
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
        "GET", "/as2_stations/{id}".format(id=params["id"]), params, options
    )
    return As2Station(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   name (required) - string - AS2 Name
#   public_certificate (required) - string
#   private_key (required) - string
#   private_key_password - string
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "public_certificate" in params and not isinstance(
        params["public_certificate"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: public_certificate must be an str"
        )
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError(
            "Bad parameter: private_key must be an str"
        )
    if "private_key_password" in params and not isinstance(
        params["private_key_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: private_key_password must be an str"
        )
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    if "public_certificate" not in params:
        raise MissingParameterError("Parameter missing: public_certificate")
    if "private_key" not in params:
        raise MissingParameterError("Parameter missing: private_key")
    response, options = Api.send_request(
        "POST", "/as2_stations", params, options
    )
    return As2Station(response.data, options)


# Parameters:
#   name - string - AS2 Name
#   public_certificate - string
#   private_key - string
#   private_key_password - string
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
    if "public_certificate" in params and not isinstance(
        params["public_certificate"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: public_certificate must be an str"
        )
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError(
            "Bad parameter: private_key must be an str"
        )
    if "private_key_password" in params and not isinstance(
        params["private_key_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: private_key_password must be an str"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH", "/as2_stations/{id}".format(id=params["id"]), params, options
    )
    return As2Station(response.data, options)


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
        "DELETE", "/as2_stations/{id}".format(id=params["id"]), params, options
    )
    return response.data


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return As2Station(*args, **kwargs)
