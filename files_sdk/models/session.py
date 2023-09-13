import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Session:
    default_attributes = {
        "id": None,  # string - Session ID
        "language": None,  # string - Session language
        "read_only": None,  # boolean - Is this session read only?
        "sftp_insecure_ciphers": None,  # boolean - Are insecure SFTP ciphers allowed for this user? (If this is set to true, the site administrator has signaled that it is ok to use less secure SSH ciphers for this user.)
        "username": None,  # string - Username to sign in as
        "password": None,  # string - Password for sign in
        "otp": None,  # string - If this user has a 2FA device, provide its OTP or code here.
        "partial_session_id": None,  # string - Identifier for a partially-completed login
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Session.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Session.default_attributes
            if getattr(self, k, None) is not None
        }

    def destroy(self, params=None, options=None):
        if not isinstance(params, dict):
            params = {}
        if not isinstance(options, dict):
            options = {}
        options.pop("session_id", None)
        options["session"] = self
        Session.destroy(params, options)

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The Session object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())


# Parameters:
#   username - string - Username to sign in as
#   password - string - Password for sign in
#   otp - string - If this user has a 2FA device, provide its OTP or code here.
#   partial_session_id - string - Identifier for a partially-completed login
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "otp" in params and not isinstance(params["otp"], str):
        raise InvalidParameterError("Bad parameter: otp must be an str")
    if "partial_session_id" in params and not isinstance(
        params["partial_session_id"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: partial_session_id must be an str"
        )
    response, options = Api.send_request("POST", "/sessions", params, options)
    return Session(response.data, options)


def delete(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, _options = Api.send_request(
        "DELETE", "/sessions", params, options
    )
    return response.data


def destroy(params=None, options=None):
    delete(params, options)


def new(*args, **kwargs):
    return Session(*args, **kwargs)
