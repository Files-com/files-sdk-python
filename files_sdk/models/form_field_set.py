import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class FormFieldSet:
    default_attributes = {
        "id": None,  # int64 - Form field set id
        "title": None,  # string - Title to be displayed
        "form_layout": None,  # array(int64) - Layout of the form
        "form_fields": None,  # array(object) - Associated form fields
        "skip_name": None,  # boolean - Any associated InboxRegistrations or BundleRegistrations can be saved without providing name
        "skip_email": None,  # boolean - Any associated InboxRegistrations or BundleRegistrations can be saved without providing email
        "skip_company": None,  # boolean - Any associated InboxRegistrations or BundleRegistrations can be saved without providing company
        "in_use": None,  # boolean - Form Field Set is in use by an active Inbox / Bundle / Inbox Registration / Bundle Registration
        "user_id": None,  # int64 - User ID.  Provide a value of `0` to operate the current session's user.
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
        ) in FormFieldSet.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in FormFieldSet.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   title - string - Title to be displayed
    #   skip_email - boolean - Skip validating form email
    #   skip_name - boolean - Skip validating form name
    #   skip_company - boolean - Skip validating company
    #   form_fields - array(object)
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
        if "title" in params and not isinstance(params["title"], str):
            raise InvalidParameterError("Bad parameter: title must be an str")
        if "form_fields" in params and not isinstance(
            params["form_fields"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: form_fields must be an list"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/form_field_sets/{id}".format(id=params["id"]),
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
            "/form_field_sets/{id}".format(id=params["id"]),
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
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(FormFieldSet, "GET", "/form_field_sets", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Form Field Set ID.
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
        "GET", "/form_field_sets/{id}".format(id=params["id"]), params, options
    )
    return FormFieldSet(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   title - string - Title to be displayed
#   skip_email - boolean - Skip validating form email
#   skip_name - boolean - Skip validating form name
#   skip_company - boolean - Skip validating company
#   form_fields - array(object)
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "title" in params and not isinstance(params["title"], str):
        raise InvalidParameterError("Bad parameter: title must be an str")
    if "skip_email" in params and not isinstance(params["skip_email"], bool):
        raise InvalidParameterError(
            "Bad parameter: skip_email must be an bool"
        )
    if "skip_name" in params and not isinstance(params["skip_name"], bool):
        raise InvalidParameterError("Bad parameter: skip_name must be an bool")
    if "skip_company" in params and not isinstance(
        params["skip_company"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: skip_company must be an bool"
        )
    if "form_fields" in params and not isinstance(
        params["form_fields"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: form_fields must be an list"
        )
    response, options = Api.send_request(
        "POST", "/form_field_sets", params, options
    )
    return FormFieldSet(response.data, options)


# Parameters:
#   title - string - Title to be displayed
#   skip_email - boolean - Skip validating form email
#   skip_name - boolean - Skip validating form name
#   skip_company - boolean - Skip validating company
#   form_fields - array(object)
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "title" in params and not isinstance(params["title"], str):
        raise InvalidParameterError("Bad parameter: title must be an str")
    if "skip_email" in params and not isinstance(params["skip_email"], bool):
        raise InvalidParameterError(
            "Bad parameter: skip_email must be an bool"
        )
    if "skip_name" in params and not isinstance(params["skip_name"], bool):
        raise InvalidParameterError("Bad parameter: skip_name must be an bool")
    if "skip_company" in params and not isinstance(
        params["skip_company"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: skip_company must be an bool"
        )
    if "form_fields" in params and not isinstance(
        params["form_fields"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: form_fields must be an list"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/form_field_sets/{id}".format(id=params["id"]),
        params,
        options,
    )
    return FormFieldSet(response.data, options)


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
        "/form_field_sets/{id}".format(id=params["id"]),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return FormFieldSet(*args, **kwargs)
