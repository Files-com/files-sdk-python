import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Automation:
    default_attributes = {
        "id": None,  # int64 - Automation ID
        "automation": None,  # string - Automation type
        "deleted": None,  # boolean - Indicates if the automation has been deleted.
        "disabled": None,  # boolean - If true, this automation will not run.
        "trigger": None,  # string - How this automation is triggered to run.
        "interval": None,  # string - If trigger is `daily`, this specifies how often to run this automation.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
        "last_modified_at": None,  # date-time - Time when automation was last modified. Does not change for name or description updates.
        "name": None,  # string - Name for this automation.
        "schedule": None,  # object - If trigger is `custom_schedule`, Custom schedule description for when the automation should be run.
        "source": None,  # string - Source Path
        "destinations": None,  # array - Destination Paths
        "destination_replace_from": None,  # string - If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
        "destination_replace_to": None,  # string - If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
        "description": None,  # string - Description for the this Automation.
        "recurring_day": None,  # int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        "path": None,  # string - Path on which this Automation runs.  Supports globs, except on remote mounts. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "user_id": None,  # int64 - User ID of the Automation's creator.
        "sync_ids": None,  # array - IDs of remote sync folder behaviors to run by this Automation
        "user_ids": None,  # array - IDs of Users for the Automation (i.e. who to Request File from)
        "group_ids": None,  # array - IDs of Groups for the Automation (i.e. who to Request File from)
        "webhook_url": None,  # string - If trigger is `webhook`, this is the URL of the webhook to trigger the Automation.
        "trigger_actions": None,  # array - If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, read, update, destroy, move, copy
        "value": None,  # object - A Hash of attributes specific to the automation type.
        "destination": None,  # string - DEPRECATED: Destination Path. Use `destinations` instead.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Automation.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Automation.default_attributes
            if getattr(self, k, None) is not None
        }

    # Manually run automation
    def manual_run(self, params=None):
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
            "/automations/{id}/manual_run".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    # Parameters:
    #   source - string - Source Path
    #   destination - string - DEPRECATED: Destination Path. Use `destinations` instead.
    #   destinations - array(string) - A list of String destination paths or Hash of folder_path and optional file_path.
    #   destination_replace_from - string - If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
    #   destination_replace_to - string - If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
    #   interval - string - How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
    #   path - string - Path on which this Automation runs.  Supports globs.
    #   sync_ids - string - A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
    #   user_ids - string - A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
    #   group_ids - string - A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
    #   schedule - object - Custom schedule for running this automation.
    #   description - string - Description for the this Automation.
    #   disabled - boolean - If true, this automation will not run.
    #   name - string - Name for this automation.
    #   trigger - string - How this automation is triggered to run.
    #   trigger_actions - array(string) - If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, read, update, destroy, move, copy
    #   value - object - A Hash of attributes specific to the automation type.
    #   recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
    #   automation - string - Automation type
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
        if "source" in params and not isinstance(params["source"], str):
            raise InvalidParameterError("Bad parameter: source must be an str")
        if "destination" in params and not isinstance(
            params["destination"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination must be an str"
            )
        if "destinations" in params and not isinstance(
            params["destinations"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: destinations must be an list"
            )
        if "destination_replace_from" in params and not isinstance(
            params["destination_replace_from"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination_replace_from must be an str"
            )
        if "destination_replace_to" in params and not isinstance(
            params["destination_replace_to"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination_replace_to must be an str"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
            )
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "sync_ids" in params and not isinstance(params["sync_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: sync_ids must be an str"
            )
        if "user_ids" in params and not isinstance(params["user_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: user_ids must be an str"
            )
        if "group_ids" in params and not isinstance(params["group_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an str"
            )
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "trigger" in params and not isinstance(params["trigger"], str):
            raise InvalidParameterError(
                "Bad parameter: trigger must be an str"
            )
        if "trigger_actions" in params and not isinstance(
            params["trigger_actions"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: trigger_actions must be an list"
            )
        if "recurring_day" in params and not isinstance(
            params["recurring_day"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: recurring_day must be an int"
            )
        if "automation" in params and not isinstance(
            params["automation"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: automation must be an str"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/automations/{id}".format(id=params["id"]),
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
        response, _options = Api.send_request(
            "DELETE",
            "/automations/{id}".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[automation]=desc`). Valid fields are `automation`, `disabled`, `last_modified_at` or `name`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled`, `last_modified_at` or `automation`. Valid field combinations are `[ automation, disabled ]` and `[ disabled, automation ]`.
#   filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `last_modified_at`.
#   filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `last_modified_at`.
#   filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `last_modified_at`.
#   filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `last_modified_at`.
#   with_deleted - boolean - Set to true to include deleted automations in the results.
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
    if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
        raise InvalidParameterError("Bad parameter: filter_gt must be an dict")
    if "filter_gteq" in params and not isinstance(params["filter_gteq"], dict):
        raise InvalidParameterError(
            "Bad parameter: filter_gteq must be an dict"
        )
    if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
        raise InvalidParameterError("Bad parameter: filter_lt must be an dict")
    if "filter_lteq" in params and not isinstance(params["filter_lteq"], dict):
        raise InvalidParameterError(
            "Bad parameter: filter_lteq must be an dict"
        )
    return ListObj(Automation, "GET", "/automations", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Automation ID.
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
        "GET", "/automations/{id}".format(id=params["id"]), params, options
    )
    return Automation(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   source - string - Source Path
#   destination - string - DEPRECATED: Destination Path. Use `destinations` instead.
#   destinations - array(string) - A list of String destination paths or Hash of folder_path and optional file_path.
#   destination_replace_from - string - If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
#   destination_replace_to - string - If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
#   interval - string - How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
#   path - string - Path on which this Automation runs.  Supports globs.
#   sync_ids - string - A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
#   user_ids - string - A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
#   group_ids - string - A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
#   schedule - object - Custom schedule for running this automation.
#   description - string - Description for the this Automation.
#   disabled - boolean - If true, this automation will not run.
#   name - string - Name for this automation.
#   trigger - string - How this automation is triggered to run.
#   trigger_actions - array(string) - If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, read, update, destroy, move, copy
#   value - object - A Hash of attributes specific to the automation type.
#   recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
#   automation (required) - string - Automation type
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "source" in params and not isinstance(params["source"], str):
        raise InvalidParameterError("Bad parameter: source must be an str")
    if "destination" in params and not isinstance(params["destination"], str):
        raise InvalidParameterError(
            "Bad parameter: destination must be an str"
        )
    if "destinations" in params and not isinstance(
        params["destinations"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: destinations must be an list"
        )
    if "destination_replace_from" in params and not isinstance(
        params["destination_replace_from"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: destination_replace_from must be an str"
        )
    if "destination_replace_to" in params and not isinstance(
        params["destination_replace_to"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: destination_replace_to must be an str"
        )
    if "interval" in params and not isinstance(params["interval"], str):
        raise InvalidParameterError("Bad parameter: interval must be an str")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "sync_ids" in params and not isinstance(params["sync_ids"], str):
        raise InvalidParameterError("Bad parameter: sync_ids must be an str")
    if "user_ids" in params and not isinstance(params["user_ids"], str):
        raise InvalidParameterError("Bad parameter: user_ids must be an str")
    if "group_ids" in params and not isinstance(params["group_ids"], str):
        raise InvalidParameterError("Bad parameter: group_ids must be an str")
    if "schedule" in params and not isinstance(params["schedule"], dict):
        raise InvalidParameterError("Bad parameter: schedule must be an dict")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "trigger" in params and not isinstance(params["trigger"], str):
        raise InvalidParameterError("Bad parameter: trigger must be an str")
    if "trigger_actions" in params and not isinstance(
        params["trigger_actions"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: trigger_actions must be an list"
        )
    if "value" in params and not isinstance(params["value"], dict):
        raise InvalidParameterError("Bad parameter: value must be an dict")
    if "recurring_day" in params and not isinstance(
        params["recurring_day"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: recurring_day must be an int"
        )
    if "automation" in params and not isinstance(params["automation"], str):
        raise InvalidParameterError("Bad parameter: automation must be an str")
    if "automation" not in params:
        raise MissingParameterError("Parameter missing: automation")
    response, options = Api.send_request(
        "POST", "/automations", params, options
    )
    return Automation(response.data, options)


# Manually run automation
def manual_run(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request(
        "POST",
        "/automations/{id}/manual_run".format(id=params["id"]),
        params,
        options,
    )
    return response.data


# Parameters:
#   source - string - Source Path
#   destination - string - DEPRECATED: Destination Path. Use `destinations` instead.
#   destinations - array(string) - A list of String destination paths or Hash of folder_path and optional file_path.
#   destination_replace_from - string - If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
#   destination_replace_to - string - If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
#   interval - string - How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
#   path - string - Path on which this Automation runs.  Supports globs.
#   sync_ids - string - A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
#   user_ids - string - A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
#   group_ids - string - A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
#   schedule - object - Custom schedule for running this automation.
#   description - string - Description for the this Automation.
#   disabled - boolean - If true, this automation will not run.
#   name - string - Name for this automation.
#   trigger - string - How this automation is triggered to run.
#   trigger_actions - array(string) - If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, read, update, destroy, move, copy
#   value - object - A Hash of attributes specific to the automation type.
#   recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
#   automation - string - Automation type
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "source" in params and not isinstance(params["source"], str):
        raise InvalidParameterError("Bad parameter: source must be an str")
    if "destination" in params and not isinstance(params["destination"], str):
        raise InvalidParameterError(
            "Bad parameter: destination must be an str"
        )
    if "destinations" in params and not isinstance(
        params["destinations"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: destinations must be an list"
        )
    if "destination_replace_from" in params and not isinstance(
        params["destination_replace_from"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: destination_replace_from must be an str"
        )
    if "destination_replace_to" in params and not isinstance(
        params["destination_replace_to"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: destination_replace_to must be an str"
        )
    if "interval" in params and not isinstance(params["interval"], str):
        raise InvalidParameterError("Bad parameter: interval must be an str")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "sync_ids" in params and not isinstance(params["sync_ids"], str):
        raise InvalidParameterError("Bad parameter: sync_ids must be an str")
    if "user_ids" in params and not isinstance(params["user_ids"], str):
        raise InvalidParameterError("Bad parameter: user_ids must be an str")
    if "group_ids" in params and not isinstance(params["group_ids"], str):
        raise InvalidParameterError("Bad parameter: group_ids must be an str")
    if "schedule" in params and not isinstance(params["schedule"], dict):
        raise InvalidParameterError("Bad parameter: schedule must be an dict")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "trigger" in params and not isinstance(params["trigger"], str):
        raise InvalidParameterError("Bad parameter: trigger must be an str")
    if "trigger_actions" in params and not isinstance(
        params["trigger_actions"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: trigger_actions must be an list"
        )
    if "value" in params and not isinstance(params["value"], dict):
        raise InvalidParameterError("Bad parameter: value must be an dict")
    if "recurring_day" in params and not isinstance(
        params["recurring_day"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: recurring_day must be an int"
        )
    if "automation" in params and not isinstance(params["automation"], str):
        raise InvalidParameterError("Bad parameter: automation must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH", "/automations/{id}".format(id=params["id"]), params, options
    )
    return Automation(response.data, options)


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
    response, _options = Api.send_request(
        "DELETE", "/automations/{id}".format(id=params["id"]), params, options
    )
    return response.data


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return Automation(*args, **kwargs)
