import builtins  # noqa: F401
from urllib.parse import quote
from decimal import Decimal
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class MoverPackage:
    __decimal_fields = {
        "price",
    }
    __decimal_array_fields = {}
    default_attributes = {
        "id": None,  # int64 - Mover package ID
        "prepaid_bytes": None,  # int64 - Total prepaid bytes included in this package
        "prepaid_expire_in_days": None,  # int64 - Number of days this package is valid for after purchase
        "price": None,  # decimal - Price of this mover package in the site's currency
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
        ) in MoverPackage.default_attributes.items():
            value = attributes.get(attribute, default_value)
            if (
                attribute in MoverPackage.__decimal_fields
                and value is not None
            ):
                value = Decimal(str(value))
            if (
                attribute in MoverPackage.__decimal_array_fields
                and value is not None
            ):
                value = [Decimal(str(v)) for v in (value or [])]
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in MoverPackage.default_attributes
            if getattr(self, k, None) is not None
        }
        for k in list(attrs.keys()):
            if k in MoverPackage.__decimal_fields and attrs[k] is not None:
                attrs[k] = str(attrs[k])
            if (
                k in MoverPackage.__decimal_array_fields
                and attrs[k] is not None
            ):
                attrs[k] = [str(v) for v in (attrs[k] or [])]
        return attrs

    # Purchase a Mover package for the current site
    def purchase(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        response, _options = Api.send_request(
            "POST",
            "/mover_packages/{id}/purchase".format(
                id=quote(str(params["id"]), safe="")
            ),
            params,
            self.options,
        )
        return response.data


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(MoverPackage, "GET", "/mover_packages", params, options)


def all(params=None, options=None):
    list(params, options)


# Purchase a Mover package for the current site
def purchase(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "POST",
        "/mover_packages/{id}/purchase".format(
            id=quote(str(params["id"]), safe="")
        ),
        params,
        options,
    )
    return MoverPackage(response.data, options)


def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, options = Api.send_request(
        "POST", "/mover_packages/create_export", params, options
    )
    return Export(response.data, options)


def new(*args, **kwargs):
    return MoverPackage(*args, **kwargs)
