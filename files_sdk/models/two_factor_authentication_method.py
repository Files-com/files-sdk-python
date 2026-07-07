import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.models.webauthn_sign_request import WebauthnSignRequest
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class TwoFactorAuthenticationMethod:
    default_attributes = {
        "id": None,  # int64 - 2fa ID
        "name": None,  # string - 2fa method name
        "method_type": None,  # string - Type of 2fa
        "phone_number": None,  # string - 2fa phone number (if SMS)
        "phone_number_country": None,  # string - 2fa phone number country (if SMS)
        "phone_number_national_format": None,  # string - 2fa phone number national format (if SMS)
        "secret_tokens": None,  # array(string) - For the Static method type, this is the list of tokens which can be used
        "setup_expired": None,  # boolean - 2fa setup expired?
        "setup_complete": None,  # boolean - 2fa setup complete?
        "setup_expires_at": None,  # date-time - 2fa setup expires at this date/time (typically 10 minutes after a new method is created)
        "totp_provisioning_uri": None,  # string - TOTP provisioning URI (if TOTP)
        "webauthn_registration_options": None,  # object - WebAuthn / FIDO 2 registration options (if WebAuthn)
        "bypass_for_ftp_sftp_dav": None,  # boolean - Set true to skip checking this 2FA method when using FTP, SFTP, and DAV
        "otp": None,  # string - Current value of OTP, Yubikey string, or Webauthn response value.
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
        ) in TwoFactorAuthenticationMethod.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in TwoFactorAuthenticationMethod.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    # Parameters:
    #   otp - string - Current value of OTP, Yubikey string, or Webauthn response value.
    #   name - string - 2fa method name
    #   bypass_for_ftp_sftp_dav - boolean - Set true to skip checking this 2FA method when using FTP, SFTP, and DAV
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
        if "otp" in params and not isinstance(params["otp"], str):
            raise InvalidParameterError("Bad parameter: otp must be an str")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        response, _options = Api.send_request(
            "PATCH",
            "/2fa/{id}".format(id=quote(str(params["id"]), safe="")),
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
            "/2fa/{id}".format(id=quote(str(params["id"]), safe="")),
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
def get(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(
        TwoFactorAuthenticationMethod, "GET", "/2fa", params, options
    )


# Parameters:
#   method_type (required) - string - Type of 2fa
#   name - string - 2fa method name
#   phone_number - string - 2fa phone number (if SMS)
#   bypass_for_ftp_sftp_dav - boolean - Set true to skip checking this 2FA method when using FTP, SFTP, and DAV
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "method_type" in params and not isinstance(params["method_type"], str):
        raise InvalidParameterError(
            "Bad parameter: method_type must be an str"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "phone_number" in params and not isinstance(
        params["phone_number"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: phone_number must be an str"
        )
    if "bypass_for_ftp_sftp_dav" in params and not isinstance(
        params["bypass_for_ftp_sftp_dav"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: bypass_for_ftp_sftp_dav must be an bool"
        )
    if "method_type" not in params:
        raise MissingParameterError("Parameter missing: method_type")
    response, options = Api.send_request("POST", "/2fa", params, options)
    return TwoFactorAuthenticationMethod(response.data, options)


# Parameters:
#   webauthn_only - boolean - Set to `true` to only generate an OTP for Webauthn keys and skip things like SMS.
def send_code(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "webauthn_only" in params and not isinstance(
        params["webauthn_only"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: webauthn_only must be an bool"
        )
    response, options = Api.send_request(
        "POST", "/2fa/send_code", params, options
    )
    return WebauthnSignRequest(response.data, options)


def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, options = Api.send_request(
        "POST", "/2fa/create_export", params, options
    )
    return Export(response.data, options)


# Parameters:
#   otp - string - Current value of OTP, Yubikey string, or Webauthn response value.
#   name - string - 2fa method name
#   bypass_for_ftp_sftp_dav - boolean - Set true to skip checking this 2FA method when using FTP, SFTP, and DAV
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "otp" in params and not isinstance(params["otp"], str):
        raise InvalidParameterError("Bad parameter: otp must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "bypass_for_ftp_sftp_dav" in params and not isinstance(
        params["bypass_for_ftp_sftp_dav"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: bypass_for_ftp_sftp_dav must be an bool"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/2fa/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return TwoFactorAuthenticationMethod(response.data, options)


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
        "/2fa/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return TwoFactorAuthenticationMethod(*args, **kwargs)
