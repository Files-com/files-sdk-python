import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class BundleRecipientRegistration:
    default_attributes = {
        "code": None,  # string - The bundle recipient registration code. Use this to register for the bundle.
        "bundle_registration_code": None,  # string - If the recipient has already registered for this bundle, this is their registration code to get the bundle contents.
        "recipient": None,  # string - The recipient's email address.
        "name": None,  # string - The recipient's name.
        "company": None,  # string - The recipient's company.
        "password_emailed": None,  # boolean - Whether a one-time password was emailed to the recipient.
        "inbox_code": None,  # string - InboxRegistration cookie code, if there is an associated InboxRegistration
        "bundle_recipient_code": None,  # string - Bundle recipient code
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
        ) in BundleRecipientRegistration.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in BundleRecipientRegistration.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The BundleRecipientRegistration object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   bundle_recipient_code (required) - string - Bundle recipient code
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "bundle_recipient_code" in params and not isinstance(
        params["bundle_recipient_code"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: bundle_recipient_code must be an str"
        )
    if "bundle_recipient_code" not in params:
        raise MissingParameterError("Parameter missing: bundle_recipient_code")
    response, options = Api.send_request(
        "POST", "/bundle_recipient_registrations", params, options
    )
    return BundleRecipientRegistration(response.data, options)


def new(*args, **kwargs):
    return BundleRecipientRegistration(*args, **kwargs)
