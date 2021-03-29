import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Session:
    default_attributes = {
        'id': None,     # string - Session ID
        'language': None,     # string - Session language
        'login_token': None,     # string - Login token. If set, this token will allow your user to log in via browser at the domain in `login_token_domain`.
        'login_token_domain': None,     # string - Domain to use with `login_token`.
        'max_dir_listing_size': None,     # int64 - Maximum number of files to retrieve per folder for a directory listing.  This is based on the user's plan.
        'multiple_regions': None,     # boolean - Can access multiple regions?
        'read_only': None,     # boolean - Is this session read only?
        'root_path': None,     # string - Initial root path to start the user's session in.
        'site_id': None,     # int64 - Site ID
        'ssl_required': None,     # boolean - Is SSL required for this user?  (If so, ensure all your communications with this user use SSL.)
        'tls_disabled': None,     # boolean - Is strong TLS disabled for this user? (If this is set to true, the site administrator has signaled that it is ok to use less secure TLS versions for this user.)
        'two_factor_setup_needed': None,     # boolean - If true, this user needs to add a Two Factor Authentication method before performing any further actions.
        'allowed_2fa_method_sms': None,     # boolean - Sent only if 2FA setup is needed. Is SMS two factor authentication allowed?
        'allowed_2fa_method_totp': None,     # boolean - Sent only if 2FA setup is needed. Is TOTP two factor authentication allowed?
        'allowed_2fa_method_u2f': None,     # boolean - Sent only if 2FA setup is needed. Is U2F two factor authentication allowed?
        'allowed_2fa_method_yubi': None,     # boolean - Sent only if 2FA setup is needed. Is Yubikey two factor authentication allowed?
        'use_provided_modified_at': None,     # boolean - Allow the user to provide file/folder modified at dates?  If false, the server will always use the current date/time.
        'windows_mode_ftp': None,     # boolean - Does this user want to use Windows line-ending emulation?  (CR vs CRLF)
        'username': None,     # string - Username to sign in as
        'password': None,     # string - Password for sign in
        'otp': None,     # string - If this user has a 2FA device, provide its OTP or code here.
        'partial_session_id': None,     # string - Identifier for a partially-completed login
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Session.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Session.default_attributes if getattr(self, k, None) is not None}

    def destroy(self, params = None, options = None):
        if not isinstance(params, dict):
            params = {}
        if not isinstance(options, dict):
            options = {}
        options.pop("session_id", None)
        options["session"] = self
        Session.destroy(params, options)

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError("The Session object doesn't support updates.")
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   username - string - Username to sign in as
#   password - string - Password for sign in
#   otp - string - If this user has a 2FA device, provide its OTP or code here.
#   partial_session_id - string - Identifier for a partially-completed login
def create(params = None, options = None):
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
    if "partial_session_id" in params and not isinstance(params["partial_session_id"], str):
        raise InvalidParameterError("Bad parameter: partial_session_id must be an str")
    response, options = Api.send_request("POST", "/sessions", params, options)
    return Session(response.data, options)

def delete(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, _options = Api.send_request("DELETE", "/sessions", params, options)
    return response.data

def destroy(params = None, options = None):
    delete(params, options)

def new(*args, **kwargs):
    return Session(*args, **kwargs)