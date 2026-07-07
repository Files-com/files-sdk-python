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


class PartnerSiteRequest:
    default_attributes = {
        "id": None,  # int64 - Partner Site Request ID
        "host_partner_id": None,  # int64 - Host Partner ID
        "guest_site_url": None,  # string - Guest Site URL
        "status": None,  # string - Request status (pending, approved, rejected)
        "host_site_name": None,  # string - Host Site Name
        "pairing_key": None,  # string - Pairing key used to approve this request on the Guest Site
        "created_at": None,  # date-time - Request creation date/time
        "updated_at": None,  # date-time - Request last updated date/time
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
        ) in PartnerSiteRequest.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in PartnerSiteRequest.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def delete(self, params=None):
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
        Api.send_request(
            "DELETE",
            "/partner_site_requests/{id}".format(
                id=quote(str(params["id"]), safe="")
            ),
            params,
            self.options,
        )

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The PartnerSiteRequest object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `host_partner_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `host_partner_id`.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    return ListObj(
        PartnerSiteRequest, "GET", "/partner_site_requests", params, options
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   pairing_key (required) - string - Pairing key for the partner site request
def find_by_pairing_key(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "pairing_key" in params and not isinstance(params["pairing_key"], str):
        raise InvalidParameterError(
            "Bad parameter: pairing_key must be an str"
        )
    if "pairing_key" not in params:
        raise MissingParameterError("Parameter missing: pairing_key")
    Api.send_request(
        "GET", "/partner_site_requests/find_by_pairing_key", params, options
    )


# Parameters:
#   host_partner_id (required) - int64 - Host Partner ID to link with
#   guest_site_url (required) - string - Guest Site URL to link to
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "host_partner_id" in params and not isinstance(
        params["host_partner_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: host_partner_id must be an int"
        )
    if "guest_site_url" in params and not isinstance(
        params["guest_site_url"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: guest_site_url must be an str"
        )
    if "host_partner_id" not in params:
        raise MissingParameterError("Parameter missing: host_partner_id")
    if "guest_site_url" not in params:
        raise MissingParameterError("Parameter missing: guest_site_url")
    response, options = Api.send_request(
        "POST", "/partner_site_requests", params, options
    )
    return PartnerSiteRequest(response.data, options)


# Parameters:
#   pairing_key (required) - string - Pairing key for the partner site request
def reject(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "pairing_key" in params and not isinstance(params["pairing_key"], str):
        raise InvalidParameterError(
            "Bad parameter: pairing_key must be an str"
        )
    if "pairing_key" not in params:
        raise MissingParameterError("Parameter missing: pairing_key")
    Api.send_request("POST", "/partner_site_requests/reject", params, options)


# Parameters:
#   pairing_key (required) - string - Pairing key for the partner site request
def approve(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "pairing_key" in params and not isinstance(params["pairing_key"], str):
        raise InvalidParameterError(
            "Bad parameter: pairing_key must be an str"
        )
    if "pairing_key" not in params:
        raise MissingParameterError("Parameter missing: pairing_key")
    Api.send_request("POST", "/partner_site_requests/approve", params, options)


# Parameters:
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `host_partner_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `host_partner_id`.
def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    response, options = Api.send_request(
        "POST", "/partner_site_requests/create_export", params, options
    )
    return Export(response.data, options)


def delete(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    Api.send_request(
        "DELETE",
        "/partner_site_requests/{id}".format(
            id=quote(str(params["id"]), safe="")
        ),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return PartnerSiteRequest(*args, **kwargs)
