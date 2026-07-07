import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ClickwrapAcceptance:
    default_attributes = {
        "id": None,  # int64 - Clickwrap Acceptance ID
        "clickwrap_id": None,  # int64 - Clickwrap ID
        "created_at": None,  # date-time - Acceptance timestamp
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
        ) in ClickwrapAcceptance.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ClickwrapAcceptance.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The ClickwrapAcceptance object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   clickwrap_id (required) - int64
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "clickwrap_id" in params and not isinstance(
        params["clickwrap_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: clickwrap_id must be an int"
        )
    if "clickwrap_id" not in params:
        raise MissingParameterError("Parameter missing: clickwrap_id")
    response, options = Api.send_request(
        "POST", "/clickwrap_acceptances", params, options
    )
    return ClickwrapAcceptance(response.data, options)


def new(*args, **kwargs):
    return ClickwrapAcceptance(*args, **kwargs)
