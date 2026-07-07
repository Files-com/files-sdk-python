import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class SslCertificate:
    default_attributes = {
        "name": None,  # string - The name of the site associated with this SSL certificate.
        "certificate": None,  # string - The text of the certificate itself.
        "private_key": None,  # string - Private key used to generate the certificate.
        "key": None,  # object - Private key encrypted with our secret key.
        "intermediates": None,  # string - Intermediate certificates, if available.
        "id": None,  # int64 - ID of the site associated with this certificate, including group id if available.
        "domain_hsts_header": None,  # boolean - True if a HSTS header should be rendered for the site
        "ftps_enabled": None,  # boolean - Whether or not this certificate can be used for FTPS.
        "https_enabled": None,  # boolean - Whether or not this certificate can be used for HTTPS. Always true.
        "sftp_insecure_ciphers": None,  # boolean - True if the site associated with this certificate has the "Allow Insecure SFTP Ciphers" feature turned on.
        "tls_disabled": None,  # boolean - True if the site associated with this certificate has the "Security Opt Out" feature turned on.
        "subdomain": None,  # string - Site subdomain.
        "domains": None,  # array(string) - Domains associated with this certificate.
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
        ) in SslCertificate.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in SslCertificate.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return SslCertificate(*args, **kwargs)
