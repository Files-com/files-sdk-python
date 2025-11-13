import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ChildSiteManagementPolicy:
    default_attributes = {
        "id": None,  # int64 - Policy ID.
        "policy_type": None,  # string - Type of policy.  Valid values: `settings`.
        "name": None,  # string - Name for this policy.
        "description": None,  # string - Description for this policy.
        "value": None,  # object - Policy configuration data. Attributes differ by policy type. For more information, refer to the Value Hash section of the developer documentation.
        "applied_child_site_ids": None,  # array(int64) - IDs of child sites that this policy has been applied to. This field is read-only.
        "skip_child_site_ids": None,  # array(int64) - IDs of child sites that this policy has been exempted from. If `skip_child_site_ids` is empty, the policy will be applied to all child sites. To apply a policy to a child site that has been exempted, remove it from `skip_child_site_ids` or set it to an empty array (`[]`).
        "created_at": None,  # date-time - When this policy was created.
        "updated_at": None,  # date-time - When this policy was last updated.
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
        ) in ChildSiteManagementPolicy.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in ChildSiteManagementPolicy.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   value - object - Policy configuration data. Attributes differ by policy type. For more information, refer to the Value Hash section of the developer documentation.
    #   skip_child_site_ids - array(int64) - IDs of child sites that this policy has been exempted from. If `skip_child_site_ids` is empty, the policy will be applied to all child sites. To apply a policy to a child site that has been exempted, remove it from `skip_child_site_ids` or set it to an empty array (`[]`).
    #   policy_type - string - Type of policy.  Valid values: `settings`.
    #   name - string - Name for this policy.
    #   description - string - Description for this policy.
    def update(self, params=None):
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
        if "skip_child_site_ids" in params and not isinstance(
            params["skip_child_site_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_child_site_ids must be an list"
            )
        if "policy_type" in params and not isinstance(
            params["policy_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: policy_type must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/child_site_management_policies/{id}".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

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
            "/child_site_management_policies/{id}".format(id=params["id"]),
            params,
            self.options,
        )

    def destroy(self, params=None):
        self.delete(params)

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
        ChildSiteManagementPolicy,
        "GET",
        "/child_site_management_policies",
        params,
        options,
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Child Site Management Policy ID.
def find(id, params=None, options=None):
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
        "GET",
        "/child_site_management_policies/{id}".format(id=params["id"]),
        params,
        options,
    )
    return ChildSiteManagementPolicy(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   value - object - Policy configuration data. Attributes differ by policy type. For more information, refer to the Value Hash section of the developer documentation.
#   skip_child_site_ids - array(int64) - IDs of child sites that this policy has been exempted from. If `skip_child_site_ids` is empty, the policy will be applied to all child sites. To apply a policy to a child site that has been exempted, remove it from `skip_child_site_ids` or set it to an empty array (`[]`).
#   policy_type (required) - string - Type of policy.  Valid values: `settings`.
#   name - string - Name for this policy.
#   description - string - Description for this policy.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "value" in params and not isinstance(params["value"], dict):
        raise InvalidParameterError("Bad parameter: value must be an dict")
    if "skip_child_site_ids" in params and not isinstance(
        params["skip_child_site_ids"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: skip_child_site_ids must be an list"
        )
    if "policy_type" in params and not isinstance(params["policy_type"], str):
        raise InvalidParameterError(
            "Bad parameter: policy_type must be an str"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "policy_type" not in params:
        raise MissingParameterError("Parameter missing: policy_type")
    response, options = Api.send_request(
        "POST", "/child_site_management_policies", params, options
    )
    return ChildSiteManagementPolicy(response.data, options)


# Parameters:
#   value - object - Policy configuration data. Attributes differ by policy type. For more information, refer to the Value Hash section of the developer documentation.
#   skip_child_site_ids - array(int64) - IDs of child sites that this policy has been exempted from. If `skip_child_site_ids` is empty, the policy will be applied to all child sites. To apply a policy to a child site that has been exempted, remove it from `skip_child_site_ids` or set it to an empty array (`[]`).
#   policy_type - string - Type of policy.  Valid values: `settings`.
#   name - string - Name for this policy.
#   description - string - Description for this policy.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "value" in params and not isinstance(params["value"], dict):
        raise InvalidParameterError("Bad parameter: value must be an dict")
    if "skip_child_site_ids" in params and not isinstance(
        params["skip_child_site_ids"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: skip_child_site_ids must be an list"
        )
    if "policy_type" in params and not isinstance(params["policy_type"], str):
        raise InvalidParameterError(
            "Bad parameter: policy_type must be an str"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/child_site_management_policies/{id}".format(id=params["id"]),
        params,
        options,
    )
    return ChildSiteManagementPolicy(response.data, options)


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
        "/child_site_management_policies/{id}".format(id=params["id"]),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return ChildSiteManagementPolicy(*args, **kwargs)
