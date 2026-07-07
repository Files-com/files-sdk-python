import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class CustomDomainForProxy:
    default_attributes = {
        "id": None,  # int64 - Custom Domain ID.
        "domain": None,  # string - Customer-owned domain name.
        "destination": None,  # string - Routing destination: `site_alias`, `public_hosting`, or `s3_endpoint`.
        "ssl_certificate_id": None,  # int64 - Attached SslCertificate ID.
        "certificate": None,  # string - The text of the certificate itself.
        "private_key": None,  # string - Private key used to generate the certificate.
        "intermediates": None,  # string - Intermediate certificates, if available.
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
        ) in CustomDomainForProxy.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in CustomDomainForProxy.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


def new(*args, **kwargs):
    return CustomDomainForProxy(*args, **kwargs)
