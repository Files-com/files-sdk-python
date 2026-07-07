import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Preview:
    default_attributes = {
        "id": None,  # int64 - Preview ID
        "status": None,  # string - Preview status.  Can be invalid, not_generated, generating, complete, or file_too_large
        "download_uri": None,  # string - Link to download preview
        "type": None,  # string - Preview type. Can be image, pdf, pdf_native, video, audio, or text
        "size": None,  # string - Preview size
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Preview.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Preview.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
#   ids (required) - string - Preview IDs.  Comma delimited.
#   bundle_registration_code - string - Bundle registration cookie code
#   size - string - Preview Size
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "ids" in params and not isinstance(params["ids"], str):
        raise InvalidParameterError("Bad parameter: ids must be an str")
    if "bundle_registration_code" in params and not isinstance(
        params["bundle_registration_code"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: bundle_registration_code must be an str"
        )
    if "size" in params and not isinstance(params["size"], str):
        raise InvalidParameterError("Bad parameter: size must be an str")
    if "ids" not in params:
        raise MissingParameterError("Parameter missing: ids")
    return ListObj(Preview, "GET", "/previews", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Preview ID
#   bundle_registration_code - string - Bundle registration cookie code
#   size - string - Preview Size
def find(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "bundle_registration_code" in params and not isinstance(
        params["bundle_registration_code"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: bundle_registration_code must be an str"
        )
    if "size" in params and not isinstance(params["size"], str):
        raise InvalidParameterError("Bad parameter: size must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "GET",
        "/previews/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return Preview(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   ids (required) - string - Preview IDs.  Comma delimited.
#   bundle_registration_code - string - Bundle registration cookie code
#   size - string - Preview Size
def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "ids" in params and not isinstance(params["ids"], str):
        raise InvalidParameterError("Bad parameter: ids must be an str")
    if "bundle_registration_code" in params and not isinstance(
        params["bundle_registration_code"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: bundle_registration_code must be an str"
        )
    if "size" in params and not isinstance(params["size"], str):
        raise InvalidParameterError("Bad parameter: size must be an str")
    if "ids" not in params:
        raise MissingParameterError("Parameter missing: ids")
    response, options = Api.send_request(
        "POST", "/previews/create_export", params, options
    )
    return Export(response.data, options)


def new(*args, **kwargs):
    return Preview(*args, **kwargs)
