import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class NpsResponse:
    default_attributes = {
        "id": None,  # int64 - NPS response id
        "next_step": None,  # string
        "user_id": None,  # int64 - User ID.  Provide a value of `0` to operate the current session's user.
        "score": None,  # int64 - NPS score
        "skipped": None,  # boolean - NPS skipped
        "comment": None,  # string - NPS comment
        "contact_me": None,  # boolean - NPS contact_me
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in NpsResponse.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in NpsResponse.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    # Parameters:
    #   comment (required) - string - NPS comment
    #   contact_me - boolean - NPS contact_me
    def update(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "comment" not in params:
            raise MissingParameterError("Parameter missing: comment")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "comment" in params and not isinstance(params["comment"], str):
            raise InvalidParameterError(
                "Bad parameter: comment must be an str"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/nps_responses/{id}".format(id=quote(str(params["id"]), safe="")),
            params,
            self.options,
        )
        return response.data

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
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   score - int64 - NPS score
#   skipped - boolean - NPS skipped
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "score" in params and not isinstance(params["score"], int):
        raise InvalidParameterError("Bad parameter: score must be an int")
    if "skipped" in params and not isinstance(params["skipped"], bool):
        raise InvalidParameterError("Bad parameter: skipped must be an bool")
    response, options = Api.send_request(
        "POST", "/nps_responses", params, options
    )
    return NpsResponse(response.data, options)


# Parameters:
#   comment (required) - string - NPS comment
#   contact_me - boolean - NPS contact_me
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "comment" in params and not isinstance(params["comment"], str):
        raise InvalidParameterError("Bad parameter: comment must be an str")
    if "contact_me" in params and not isinstance(params["contact_me"], bool):
        raise InvalidParameterError(
            "Bad parameter: contact_me must be an bool"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    if "comment" not in params:
        raise MissingParameterError("Parameter missing: comment")
    response, options = Api.send_request(
        "PATCH",
        "/nps_responses/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return NpsResponse(response.data, options)


def new(*args, **kwargs):
    return NpsResponse(*args, **kwargs)
