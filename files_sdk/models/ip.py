import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Ip:
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
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Ip.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Ip.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return Ip(*args, **kwargs)
