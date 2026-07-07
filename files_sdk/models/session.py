import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.models.public_hosting_session_pairing import (
    PublicHostingSessionPairing,
)
from files_sdk.models.paired_api_key import PairedApiKey
from files_sdk.models.oauth_redirect import OauthRedirect
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
        "aws_secret_key": None,  # string - AWS Secret Key for validating AWS-style signatures in the Inbound S3 endpoint.
        "ai_assistant_personality_id": None,  # int64 - AI Assistant Personality ID for the in-app AI Assistant.
        "ai_assistant_personality_system_prompt": None,  # string - System prompt for the in-app AI Assistant.
        "login_token": None,  # string - Login token. If set, this token will allow your user to log in via browser at the domain in `login_token_domain`.
        "login_token_domain": None,  # string - Domain to use with `login_token`.
        "default_workspace_id": None,  # int64 - Workspace ID the user should land in by default when more than one Workspace is available.
        "max_dir_listing_size": None,  # int64 - Maximum number of files to retrieve per folder for a directory listing.  This is based on the user's plan.
        "multiple_regions": None,  # boolean - Can access multiple regions?
        "read_only": None,  # boolean - Is this session read only?
        "root_path": None,  # string - Root path to restrict the user's session to.
        "home_path": None,  # string - Initial path to start the user's session in.
        "sftp_insecure_ciphers": None,  # boolean - Are insecure SFTP ciphers allowed for this user? (If this is set to true, the site administrator has signaled that it is ok to use less secure SSH ciphers for this user.)
        "site_id": None,  # int64 - Site ID
        "ssl_required": None,  # boolean - Is SSL required for this user?  (If so, ensure all your communications with this user use SSL.)
        "timeout_at": None,  # date-time - Session timeout datetime
        "trusted": None,  # boolean - Can this session tolerate IP and User-Agent mismatches?
        "two_factor_setup_needed": None,  # boolean - If true, this user needs to add a Two Factor Authentication method before performing any further actions.
        "allowed_2fa_method_sms": None,  # boolean - Sent only if 2FA setup is needed. Is SMS two factor authentication allowed?
        "allowed_2fa_method_totp": None,  # boolean - Sent only if 2FA setup is needed. Is TOTP two factor authentication allowed?
        "allowed_2fa_method_webauthn": None,  # boolean - Sent only if 2FA setup is needed. Is WebAuthn two factor authentication allowed?
        "allowed_2fa_method_yubi": None,  # boolean - Sent only if 2FA setup is needed. Is Yubikey two factor authentication allowed?
        "calculate_file_checksums_crc32": None,  # boolean - Calculate CRC32 checksum for incoming files?
        "calculate_file_checksums_md5": None,  # boolean - Calculate MD5 checksum for incoming files?
        "calculate_file_checksums_sha1": None,  # boolean - Calculate SHA1 checksum for incoming files?
        "calculate_file_checksums_sha256": None,  # boolean - Calculate SHA256 checksum for incoming files?
        "legacy_checksums_mode": None,  # boolean - Use legacy checksums mode?
        "finalize_partial_uploads": None,  # boolean - Finalize partial SFTP uploads?
        "use_provided_modified_at": None,  # boolean - Allow the user to provide file/folder modified at dates?  If false, the server will always use the current date/time.
        "windows_mode_ftp": None,  # boolean - Does this user want to use Windows line-ending emulation?  (CR vs CRLF)
        "user_belongs_to_parent_site": None,  # boolean
        "impersonator_user_id": None,  # int64 - User ID of the Site Admin who initiated a Read-Only session impersonating this session's user
        "username": None,  # string - Username to sign in as
        "password": None,  # string - Password for sign in
        "aws_access_key_id": None,  # string - AWS Access Key ID for signing in with AWS credentials
        "change_password": None,  # string
        "change_password_confirmation": None,  # string
        "interface": None,  # string
        "ssh_client_identification": None,  # string
        "locale": None,  # string
        "no_cookie": None,  # boolean
        "oauth_provider": None,  # string
        "oauth_label": None,  # string
        "oauth_code": None,  # string
        "oauth_state": None,  # string
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
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Session.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

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
            return True


# Parameters:
#   username - string - Username to sign in as
#   password - string - Password for sign in
#   aws_access_key_id - string - AWS Access Key ID for signing in with AWS credentials
#   change_password - string
#   change_password_confirmation - string
#   interface - string
#   ssh_client_identification - string
#   locale - string
#   no_cookie - boolean
#   oauth_provider - string
#   oauth_label - string
#   oauth_code - string
#   oauth_state - string
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
    if "aws_access_key_id" in params and not isinstance(
        params["aws_access_key_id"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: aws_access_key_id must be an str"
        )
    if "change_password" in params and not isinstance(
        params["change_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: change_password must be an str"
        )
    if "change_password_confirmation" in params and not isinstance(
        params["change_password_confirmation"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: change_password_confirmation must be an str"
        )
    if "interface" in params and not isinstance(params["interface"], str):
        raise InvalidParameterError("Bad parameter: interface must be an str")
    if "ssh_client_identification" in params and not isinstance(
        params["ssh_client_identification"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: ssh_client_identification must be an str"
        )
    if "locale" in params and not isinstance(params["locale"], str):
        raise InvalidParameterError("Bad parameter: locale must be an str")
    if "no_cookie" in params and not isinstance(params["no_cookie"], bool):
        raise InvalidParameterError("Bad parameter: no_cookie must be an bool")
    if "oauth_provider" in params and not isinstance(
        params["oauth_provider"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: oauth_provider must be an str"
        )
    if "oauth_label" in params and not isinstance(params["oauth_label"], str):
        raise InvalidParameterError(
            "Bad parameter: oauth_label must be an str"
        )
    if "oauth_code" in params and not isinstance(params["oauth_code"], str):
        raise InvalidParameterError("Bad parameter: oauth_code must be an str")
    if "oauth_state" in params and not isinstance(params["oauth_state"], str):
        raise InvalidParameterError(
            "Bad parameter: oauth_state must be an str"
        )
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


# Parameters:
#   subdomain (required) - string - Site subdomain to login to
def subdomain(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "subdomain" in params and not isinstance(params["subdomain"], str):
        raise InvalidParameterError("Bad parameter: subdomain must be an str")
    if "subdomain" not in params:
        raise MissingParameterError("Parameter missing: subdomain")
    response, options = Api.send_request(
        "POST", "/sessions/subdomain", params, options
    )
    return Session(response.data, options)


# Parameters:
#   user_id (required) - string - User id to login as
def as_user(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], str):
        raise InvalidParameterError("Bad parameter: user_id must be an str")
    if "user_id" not in params:
        raise MissingParameterError("Parameter missing: user_id")
    response, options = Api.send_request(
        "POST", "/sessions/as_user", params, options
    )
    return Session(response.data, options)


# Parameters:
#   session_id (required) - string - Session ID to convert to a trusted session
def trusted(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "session_id" in params and not isinstance(params["session_id"], str):
        raise InvalidParameterError("Bad parameter: session_id must be an str")
    if "session_id" not in params:
        raise MissingParameterError("Parameter missing: session_id")
    response, options = Api.send_request(
        "POST", "/sessions/trusted", params, options
    )
    return Session(response.data, options)


# Parameters:
#   code (required) - string
#   password (required) - string
#   confirm_password - string
#   interface - string
#   locale - string
#   otp - string
def forgot_reset(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "code" in params and not isinstance(params["code"], str):
        raise InvalidParameterError("Bad parameter: code must be an str")
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "confirm_password" in params and not isinstance(
        params["confirm_password"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: confirm_password must be an str"
        )
    if "interface" in params and not isinstance(params["interface"], str):
        raise InvalidParameterError("Bad parameter: interface must be an str")
    if "locale" in params and not isinstance(params["locale"], str):
        raise InvalidParameterError("Bad parameter: locale must be an str")
    if "otp" in params and not isinstance(params["otp"], str):
        raise InvalidParameterError("Bad parameter: otp must be an str")
    if "code" not in params:
        raise MissingParameterError("Parameter missing: code")
    if "password" not in params:
        raise MissingParameterError("Parameter missing: password")
    Api.send_request("POST", "/sessions/forgot/reset", params, options)


# Parameters:
#   code (required) - string
def forgot_validate(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "code" in params and not isinstance(params["code"], str):
        raise InvalidParameterError("Bad parameter: code must be an str")
    if "code" not in params:
        raise MissingParameterError("Parameter missing: code")
    Api.send_request("POST", "/sessions/forgot/validate", params, options)


# Parameters:
#   email - string
#   username - string
#   username_or_email - string
def forgot(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "email" in params and not isinstance(params["email"], str):
        raise InvalidParameterError("Bad parameter: email must be an str")
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    if "username_or_email" in params and not isinstance(
        params["username_or_email"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: username_or_email must be an str"
        )
    Api.send_request("POST", "/sessions/forgot", params, options)


# Parameters:
#   return_to (required) - string - Public Hosting URL to return to after authentication
def public_hosting(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "return_to" in params and not isinstance(params["return_to"], str):
        raise InvalidParameterError("Bad parameter: return_to must be an str")
    if "return_to" not in params:
        raise MissingParameterError("Parameter missing: return_to")
    response, options = Api.send_request(
        "POST", "/sessions/public_hosting", params, options
    )
    return PublicHostingSessionPairing(response.data, options)


# Parameters:
#   key (required) - string - The pairing key to reserve for login.  Cannot be reused
def pairing_key(key, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["key"] = key
    if "key" in params and not isinstance(params["key"], str):
        raise InvalidParameterError("Bad parameter: key must be an str")
    if "key" not in params:
        raise MissingParameterError("Parameter missing: key")
    response, options = Api.send_request(
        "POST",
        "/sessions/pairing_key/{key}".format(
            key=quote(str(params["key"]), safe="")
        ),
        params,
        options,
    )
    return PairedApiKey(response.data, options)


# Parameters:
#   provider (required) - string
#   label - string
#   state - string
#   host - string
def oauth(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "provider" in params and not isinstance(params["provider"], str):
        raise InvalidParameterError("Bad parameter: provider must be an str")
    if "label" in params and not isinstance(params["label"], str):
        raise InvalidParameterError("Bad parameter: label must be an str")
    if "state" in params and not isinstance(params["state"], str):
        raise InvalidParameterError("Bad parameter: state must be an str")
    if "host" in params and not isinstance(params["host"], str):
        raise InvalidParameterError("Bad parameter: host must be an str")
    if "provider" not in params:
        raise MissingParameterError("Parameter missing: provider")
    response, options = Api.send_request(
        "POST", "/sessions/oauth", params, options
    )
    return OauthRedirect(response.data, options)


def delete(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    Api.send_request("DELETE", "/sessions", params, options)


def destroy(params=None, options=None):
    delete(params, options)


def new(*args, **kwargs):
    return Session(*args, **kwargs)
