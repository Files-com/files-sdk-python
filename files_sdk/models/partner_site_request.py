import builtins  # noqa: F401
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
        "partner_id": None,  # int64 - Partner ID
        "linked_site_id": None,  # int64 - Linked Site ID
        "status": None,  # string - Request status (pending, approved, rejected)
        "pairing_key": None,  # string - Pairing key used to approve this request on the target site
        "created_at": None,  # date-time - Request creation date/time
        "updated_at": None,  # date-time - Request last updated date/time
        "site_url": None,  # string - Site URL to link to
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
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in PartnerSiteRequest.default_attributes
            if getattr(self, k, None) is not None
        }

    # Reject partner site request
    def reject(self, params=None):
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
            "POST",
            "/partner_site_requests/{id}/reject".format(id=params["id"]),
            params,
            self.options,
        )

    # Approve partner site request
    def approve(self, params=None):
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
            "POST",
            "/partner_site_requests/{id}/approve".format(id=params["id"]),
            params,
            self.options,
        )

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
            "/partner_site_requests/{id}".format(id=params["id"]),
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
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
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
#   partner_id (required) - int64 - Partner ID to link with
#   site_url (required) - string - Site URL to link to
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "partner_id" in params and not isinstance(params["partner_id"], int):
        raise InvalidParameterError("Bad parameter: partner_id must be an int")
    if "site_url" in params and not isinstance(params["site_url"], str):
        raise InvalidParameterError("Bad parameter: site_url must be an str")
    if "partner_id" not in params:
        raise MissingParameterError("Parameter missing: partner_id")
    if "site_url" not in params:
        raise MissingParameterError("Parameter missing: site_url")
    response, options = Api.send_request(
        "POST", "/partner_site_requests", params, options
    )
    return PartnerSiteRequest(response.data, options)


# Reject partner site request
def reject(id, params=None, options=None):
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
        "POST",
        "/partner_site_requests/{id}/reject".format(id=params["id"]),
        params,
        options,
    )


# Approve partner site request
def approve(id, params=None, options=None):
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
        "POST",
        "/partner_site_requests/{id}/approve".format(id=params["id"]),
        params,
        options,
    )


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
        "/partner_site_requests/{id}".format(id=params["id"]),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return PartnerSiteRequest(*args, **kwargs)
