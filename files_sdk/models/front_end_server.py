import builtins  # noqa: F401
from files_sdk.models.ip import Ip
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class FrontEndServer:
    default_attributes = {
        "ip": None,  # string - Private IP of the server.
        "external_ip": None,  # string - Public IP of the server.
        "assigned": None,  # boolean - Flag to signal to other systems to use this config
        "site": None,  # SslCertificate - SSL certificate information for the site associated with this IP, if available.
        "ftp_enabled": None,  # boolean
        "sftp_enabled": None,  # boolean
        "sftp_host_key_type": None,  # string - Which SFTP host key to use.
        "sftp_host_key_private_key": None,  # string - SFTP Host Key private key if using a custom key.
        "site_id": None,  # int64 - Site Id
        "motd_text": None,  # string - A message to show users when they connect via FTP or SFTP.
        "motd_use_for_ftp": None,  # boolean - Show message to users connecting via FTP
        "motd_use_for_sftp": None,  # boolean - Show message to users connecting via SFTP
        "custom_domains": None,  # array(object) - Active Custom Domains for the site associated with this IP, with their attached SSL certificate content.
        "pair_type": None,  # string - Pair type for General Use Public IPs
        "name": None,  # string - Server's short name.
        "hostname": None,  # string - Server's full hostname.
        "zone": None,  # string - Availability zone where this server lives.
        "ips": None,  # array(string) - An array of public and private ip address pairs.
        "primary_ip": None,  # string - Primary Internal IP.
        "primary_ip_public": None,  # string - Primary Public IP.
        "soo_ip": None,  # string - Security Opt Out Internal IP.
        "soo_ip_public": None,  # string - Security Opt Out Public IP.
        "exavault_ip": None,  # string - Exavault Internal IP.
        "exavault_ip_public": None,  # string - Exavault Public IP.
        "exavault_soo_ip": None,  # string - Exavault Security Opt Out Internal IP.
        "exavault_soo_ip_public": None,  # string - Exavault Security Opt Out Public IP.
        "smartfile_ip": None,  # string - Smartfile Internal IP.
        "smartfile_ip_public": None,  # string - Smartfile Public IP.
        "smartfile_soo_ip": None,  # string - Smartfile Security Opt Out Internal IP.
        "smartfile_soo_ip_public": None,  # string - Smartfile Security Opt Out Public IP.
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
        ) in FrontEndServer.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in FrontEndServer.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The FrontEndServer object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   name (required) - string - Server's short name.
#   hostname - string - Server's full hostname.
#   zone - string - Availability zone where this server lives.
#   ips - array(string) - An array of public and private ip address pairs.
#   ips[private_ip] (required) - array(string) - Private IP address associated with the server.
#   ips[public_ip] - array(string) - Public IP address associated with the server.
#   primary_ip - string - Primary Internal IP.
#   primary_ip_public - string - Primary Public IP.
#   soo_ip - string - Security Opt Out Internal IP.
#   soo_ip_public - string - Security Opt Out Public IP.
#   exavault_ip - string - Exavault Internal IP.
#   exavault_ip_public - string - Exavault Public IP.
#   exavault_soo_ip - string - Exavault Security Opt Out Internal IP.
#   exavault_soo_ip_public - string - Exavault Security Opt Out Public IP.
#   smartfile_ip - string - Smartfile Internal IP.
#   smartfile_ip_public - string - Smartfile Public IP.
#   smartfile_soo_ip - string - Smartfile Security Opt Out Internal IP.
#   smartfile_soo_ip_public - string - Smartfile Security Opt Out Public IP.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "hostname" in params and not isinstance(params["hostname"], str):
        raise InvalidParameterError("Bad parameter: hostname must be an str")
    if "zone" in params and not isinstance(params["zone"], str):
        raise InvalidParameterError("Bad parameter: zone must be an str")
    if "ips" in params and not isinstance(params["ips"], builtins.list):
        raise InvalidParameterError("Bad parameter: ips must be an list")
    if "primary_ip" in params and not isinstance(params["primary_ip"], str):
        raise InvalidParameterError("Bad parameter: primary_ip must be an str")
    if "primary_ip_public" in params and not isinstance(
        params["primary_ip_public"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: primary_ip_public must be an str"
        )
    if "soo_ip" in params and not isinstance(params["soo_ip"], str):
        raise InvalidParameterError("Bad parameter: soo_ip must be an str")
    if "soo_ip_public" in params and not isinstance(
        params["soo_ip_public"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: soo_ip_public must be an str"
        )
    if "exavault_ip" in params and not isinstance(params["exavault_ip"], str):
        raise InvalidParameterError(
            "Bad parameter: exavault_ip must be an str"
        )
    if "exavault_ip_public" in params and not isinstance(
        params["exavault_ip_public"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: exavault_ip_public must be an str"
        )
    if "exavault_soo_ip" in params and not isinstance(
        params["exavault_soo_ip"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: exavault_soo_ip must be an str"
        )
    if "exavault_soo_ip_public" in params and not isinstance(
        params["exavault_soo_ip_public"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: exavault_soo_ip_public must be an str"
        )
    if "smartfile_ip" in params and not isinstance(
        params["smartfile_ip"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: smartfile_ip must be an str"
        )
    if "smartfile_ip_public" in params and not isinstance(
        params["smartfile_ip_public"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: smartfile_ip_public must be an str"
        )
    if "smartfile_soo_ip" in params and not isinstance(
        params["smartfile_soo_ip"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: smartfile_soo_ip must be an str"
        )
    if "smartfile_soo_ip_public" in params and not isinstance(
        params["smartfile_soo_ip_public"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: smartfile_soo_ip_public must be an str"
        )
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    response, options = Api.send_request(
        "POST", "/front_end_servers", params, options
    )
    return Ip(response.data, options)


def new(*args, **kwargs):
    return FrontEndServer(*args, **kwargs)
