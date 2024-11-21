import builtins  # noqa: F401
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Message:
    default_attributes = {
        "id": None,  # int64 - Message ID
        "subject": None,  # string - Message subject.
        "body": None,  # string - Message body.
        "comments": None,  # array(object) - Comments.
        "user_id": None,  # int64 - User ID.  Provide a value of `0` to operate the current session's user.
        "project_id": None,  # int64 - Project to which the message should be attached.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Message.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Message.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   project_id (required) - int64 - Project to which the message should be attached.
    #   subject (required) - string - Message subject.
    #   body (required) - string - Message body.
    def update(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "project_id" not in params:
            raise MissingParameterError("Parameter missing: project_id")
        if "subject" not in params:
            raise MissingParameterError("Parameter missing: subject")
        if "body" not in params:
            raise MissingParameterError("Parameter missing: body")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "project_id" in params and not isinstance(
            params["project_id"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: project_id must be an int"
            )
        if "subject" in params and not isinstance(params["subject"], str):
            raise InvalidParameterError(
                "Bad parameter: subject must be an str"
            )
        if "body" in params and not isinstance(params["body"], str):
            raise InvalidParameterError("Bad parameter: body must be an str")
        response, _options = Api.send_request(
            "PATCH",
            "/messages/{id}".format(id=params["id"]),
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
            "/messages/{id}".format(id=params["id"]),
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
#   project_id (required) - int64 - Project for which to return messages.
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
    if "project_id" in params and not isinstance(params["project_id"], int):
        raise InvalidParameterError("Bad parameter: project_id must be an int")
    if "project_id" not in params:
        raise MissingParameterError("Parameter missing: project_id")
    return ListObj(Message, "GET", "/messages", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Message ID.
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
        "GET", "/messages/{id}".format(id=params["id"]), params, options
    )
    return Message(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   project_id (required) - int64 - Project to which the message should be attached.
#   subject (required) - string - Message subject.
#   body (required) - string - Message body.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "project_id" in params and not isinstance(params["project_id"], int):
        raise InvalidParameterError("Bad parameter: project_id must be an int")
    if "subject" in params and not isinstance(params["subject"], str):
        raise InvalidParameterError("Bad parameter: subject must be an str")
    if "body" in params and not isinstance(params["body"], str):
        raise InvalidParameterError("Bad parameter: body must be an str")
    if "project_id" not in params:
        raise MissingParameterError("Parameter missing: project_id")
    if "subject" not in params:
        raise MissingParameterError("Parameter missing: subject")
    if "body" not in params:
        raise MissingParameterError("Parameter missing: body")
    response, options = Api.send_request("POST", "/messages", params, options)
    return Message(response.data, options)


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   project_id (required) - int64 - Project for which to return messages.
def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "project_id" in params and not isinstance(params["project_id"], int):
        raise InvalidParameterError("Bad parameter: project_id must be an int")
    if "project_id" not in params:
        raise MissingParameterError("Parameter missing: project_id")
    response, options = Api.send_request(
        "POST", "/messages/create_export", params, options
    )
    return [Export(entity_data, options) for entity_data in response.data]


# Parameters:
#   project_id (required) - int64 - Project to which the message should be attached.
#   subject (required) - string - Message subject.
#   body (required) - string - Message body.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "project_id" in params and not isinstance(params["project_id"], int):
        raise InvalidParameterError("Bad parameter: project_id must be an int")
    if "subject" in params and not isinstance(params["subject"], str):
        raise InvalidParameterError("Bad parameter: subject must be an str")
    if "body" in params and not isinstance(params["body"], str):
        raise InvalidParameterError("Bad parameter: body must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    if "project_id" not in params:
        raise MissingParameterError("Parameter missing: project_id")
    if "subject" not in params:
        raise MissingParameterError("Parameter missing: subject")
    if "body" not in params:
        raise MissingParameterError("Parameter missing: body")
    response, options = Api.send_request(
        "PATCH", "/messages/{id}".format(id=params["id"]), params, options
    )
    return Message(response.data, options)


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
        "DELETE", "/messages/{id}".format(id=params["id"]), params, options
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return Message(*args, **kwargs)
