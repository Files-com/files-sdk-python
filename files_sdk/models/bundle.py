import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Bundle:
    default_attributes = {
        "code": None,  # string - Bundle code.  This code forms the end part of the Public URL.
        "color_left": None,  # string - Page link and button color
        "color_link": None,  # string - Top bar link color
        "color_text": None,  # string - Page link and button color
        "color_top": None,  # string - Top bar background color
        "color_top_text": None,  # string - Top bar text color
        "url": None,  # string - Public URL of Share Link
        "description": None,  # string - Public description
        "expires_at": None,  # date-time - Bundle expiration date/time
        "password_protected": None,  # boolean - Is this bundle password protected?
        "permissions": None,  # string - Permissions that apply to Folders in this Share Link.
        "preview_only": None,  # boolean - DEPRECATED: Restrict users to previewing files only. Use `permissions` instead.
        "require_registration": None,  # boolean - Show a registration page that captures the downloader's name and email address?
        "require_share_recipient": None,  # boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
        "require_logout": None,  # boolean - If true, we will hide the 'Remember Me' box on the Bundle registration page, requiring that the user logout and log back in every time they visit the page.
        "clickwrap_body": None,  # string - Legal text that must be agreed to prior to accessing Bundle.
        "form_field_set": None,  # FormFieldSet - Custom Form to use
        "skip_name": None,  # boolean - BundleRegistrations can be saved without providing name?
        "skip_email": None,  # boolean - BundleRegistrations can be saved without providing email?
        "start_access_on_date": None,  # date-time - Date when share will start to be accessible. If `nil` access granted right after create.
        "skip_company": None,  # boolean - BundleRegistrations can be saved without providing company?
        "id": None,  # int64 - Bundle ID
        "created_at": None,  # date-time - Bundle created at date/time
        "dont_separate_submissions_by_folder": None,  # boolean - Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
        "max_uses": None,  # int64 - Maximum number of times bundle can be accessed
        "note": None,  # string - Bundle internal note
        "path_template": None,  # string - Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, and any custom form data.
        "send_email_receipt_to_uploader": None,  # boolean - Send delivery receipt to the uploader. Note: For writable share only
        "snapshot_id": None,  # int64 - ID of the snapshot containing this bundle's contents.
        "user_id": None,  # int64 - Bundle creator user ID
        "username": None,  # string - Bundle creator username
        "clickwrap_id": None,  # int64 - ID of the clickwrap to use with this bundle.
        "inbox_id": None,  # int64 - ID of the associated inbox, if available.
        "watermark_attachment": None,  # Image - Preview watermark image applied to all bundle items.
        "watermark_value": None,  # object - Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
        "has_inbox": None,  # boolean - Does this bundle have an associated inbox?
        "paths": None,  # array - A list of paths in this bundle.  For performance reasons, this is not provided when listing bundles.
        "password": None,  # string - Password for this bundle.
        "form_field_set_id": None,  # int64 - Id of Form Field Set to use with this bundle
        "create_snapshot": None,  # boolean - If true, create a snapshot of this bundle's contents.
        "finalize_snapshot": None,  # boolean - If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
        "watermark_attachment_file": None,  # file - Preview watermark image applied to all bundle items.
        "watermark_attachment_delete": None,  # boolean - If true, will delete the file stored in watermark_attachment
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Bundle.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Bundle.default_attributes
            if getattr(self, k, None) is not None
        }

    # Send email(s) with a link to bundle
    #
    # Parameters:
    #   to - array(string) - A list of email addresses to share this bundle with. Required unless `recipients` is used.
    #   note - string - Note to include in email.
    #   recipients - array(object) - A list of recipients to share this bundle with. Required unless `to` is used.
    def share(self, params=None):
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
        if "to" in params and not isinstance(params["to"], builtins.list):
            raise InvalidParameterError("Bad parameter: to must be an list")
        if "note" in params and not isinstance(params["note"], str):
            raise InvalidParameterError("Bad parameter: note must be an str")
        if "recipients" in params and not isinstance(
            params["recipients"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: recipients must be an list"
            )
        response, _options = Api.send_request(
            "POST",
            "/bundles/{id}/share".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    # Parameters:
    #   paths - array(string) - A list of paths to include in this bundle.
    #   password - string - Password for this bundle.
    #   form_field_set_id - int64 - Id of Form Field Set to use with this bundle
    #   clickwrap_id - int64 - ID of the clickwrap to use with this bundle.
    #   code - string - Bundle code.  This code forms the end part of the Public URL.
    #   create_snapshot - boolean - If true, create a snapshot of this bundle's contents.
    #   description - string - Public description
    #   dont_separate_submissions_by_folder - boolean - Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
    #   expires_at - string - Bundle expiration date/time
    #   finalize_snapshot - boolean - If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
    #   inbox_id - int64 - ID of the associated inbox, if available.
    #   max_uses - int64 - Maximum number of times bundle can be accessed
    #   note - string - Bundle internal note
    #   path_template - string - Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, and any custom form data.
    #   permissions - string - Permissions that apply to Folders in this Share Link.
    #   preview_only - boolean - DEPRECATED: Restrict users to previewing files only. Use `permissions` instead.
    #   require_registration - boolean - Show a registration page that captures the downloader's name and email address?
    #   require_share_recipient - boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
    #   send_email_receipt_to_uploader - boolean - Send delivery receipt to the uploader. Note: For writable share only
    #   skip_company - boolean - BundleRegistrations can be saved without providing company?
    #   start_access_on_date - string - Date when share will start to be accessible. If `nil` access granted right after create.
    #   skip_email - boolean - BundleRegistrations can be saved without providing email?
    #   skip_name - boolean - BundleRegistrations can be saved without providing name?
    #   watermark_attachment_delete - boolean - If true, will delete the file stored in watermark_attachment
    #   watermark_attachment_file - file - Preview watermark image applied to all bundle items.
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
        if "paths" in params and not isinstance(
            params["paths"], builtins.list
        ):
            raise InvalidParameterError("Bad parameter: paths must be an list")
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError(
                "Bad parameter: password must be an str"
            )
        if "form_field_set_id" in params and not isinstance(
            params["form_field_set_id"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: form_field_set_id must be an int"
            )
        if "clickwrap_id" in params and not isinstance(
            params["clickwrap_id"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: clickwrap_id must be an int"
            )
        if "code" in params and not isinstance(params["code"], str):
            raise InvalidParameterError("Bad parameter: code must be an str")
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "expires_at" in params and not isinstance(
            params["expires_at"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: expires_at must be an str"
            )
        if "inbox_id" in params and not isinstance(params["inbox_id"], int):
            raise InvalidParameterError(
                "Bad parameter: inbox_id must be an int"
            )
        if "max_uses" in params and not isinstance(params["max_uses"], int):
            raise InvalidParameterError(
                "Bad parameter: max_uses must be an int"
            )
        if "note" in params and not isinstance(params["note"], str):
            raise InvalidParameterError("Bad parameter: note must be an str")
        if "path_template" in params and not isinstance(
            params["path_template"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: path_template must be an str"
            )
        if "permissions" in params and not isinstance(
            params["permissions"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: permissions must be an str"
            )
        if "start_access_on_date" in params and not isinstance(
            params["start_access_on_date"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: start_access_on_date must be an str"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/bundles/{id}".format(id=params["id"]),
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
            "/bundles/{id}".format(id=params["id"]),
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
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[created_at]=desc`). Valid fields are `created_at` and `code`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`.
#   filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
#   filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
#   filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
#   filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
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
    return ListObj(Bundle, "GET", "/bundles", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Bundle ID.
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
        "GET", "/bundles/{id}".format(id=params["id"]), params, options
    )
    return Bundle(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   paths (required) - array(string) - A list of paths to include in this bundle.
#   password - string - Password for this bundle.
#   form_field_set_id - int64 - Id of Form Field Set to use with this bundle
#   create_snapshot - boolean - If true, create a snapshot of this bundle's contents.
#   dont_separate_submissions_by_folder - boolean - Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
#   expires_at - string - Bundle expiration date/time
#   finalize_snapshot - boolean - If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
#   max_uses - int64 - Maximum number of times bundle can be accessed
#   description - string - Public description
#   note - string - Bundle internal note
#   code - string - Bundle code.  This code forms the end part of the Public URL.
#   path_template - string - Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, and any custom form data.
#   permissions - string - Permissions that apply to Folders in this Share Link.
#   preview_only - boolean - DEPRECATED: Restrict users to previewing files only. Use `permissions` instead.
#   require_registration - boolean - Show a registration page that captures the downloader's name and email address?
#   clickwrap_id - int64 - ID of the clickwrap to use with this bundle.
#   inbox_id - int64 - ID of the associated inbox, if available.
#   require_share_recipient - boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
#   send_email_receipt_to_uploader - boolean - Send delivery receipt to the uploader. Note: For writable share only
#   skip_email - boolean - BundleRegistrations can be saved without providing email?
#   skip_name - boolean - BundleRegistrations can be saved without providing name?
#   skip_company - boolean - BundleRegistrations can be saved without providing company?
#   start_access_on_date - string - Date when share will start to be accessible. If `nil` access granted right after create.
#   snapshot_id - int64 - ID of the snapshot containing this bundle's contents.
#   watermark_attachment_file - file - Preview watermark image applied to all bundle items.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "paths" in params and not isinstance(params["paths"], builtins.list):
        raise InvalidParameterError("Bad parameter: paths must be an list")
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "form_field_set_id" in params and not isinstance(
        params["form_field_set_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: form_field_set_id must be an int"
        )
    if "expires_at" in params and not isinstance(params["expires_at"], str):
        raise InvalidParameterError("Bad parameter: expires_at must be an str")
    if "max_uses" in params and not isinstance(params["max_uses"], int):
        raise InvalidParameterError("Bad parameter: max_uses must be an int")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "note" in params and not isinstance(params["note"], str):
        raise InvalidParameterError("Bad parameter: note must be an str")
    if "code" in params and not isinstance(params["code"], str):
        raise InvalidParameterError("Bad parameter: code must be an str")
    if "path_template" in params and not isinstance(
        params["path_template"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: path_template must be an str"
        )
    if "permissions" in params and not isinstance(params["permissions"], str):
        raise InvalidParameterError(
            "Bad parameter: permissions must be an str"
        )
    if "clickwrap_id" in params and not isinstance(
        params["clickwrap_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: clickwrap_id must be an int"
        )
    if "inbox_id" in params and not isinstance(params["inbox_id"], int):
        raise InvalidParameterError("Bad parameter: inbox_id must be an int")
    if "start_access_on_date" in params and not isinstance(
        params["start_access_on_date"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: start_access_on_date must be an str"
        )
    if "snapshot_id" in params and not isinstance(params["snapshot_id"], int):
        raise InvalidParameterError(
            "Bad parameter: snapshot_id must be an int"
        )
    if "paths" not in params:
        raise MissingParameterError("Parameter missing: paths")
    response, options = Api.send_request("POST", "/bundles", params, options)
    return Bundle(response.data, options)


# Send email(s) with a link to bundle
#
# Parameters:
#   to - array(string) - A list of email addresses to share this bundle with. Required unless `recipients` is used.
#   note - string - Note to include in email.
#   recipients - array(object) - A list of recipients to share this bundle with. Required unless `to` is used.
def share(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "to" in params and not isinstance(params["to"], builtins.list):
        raise InvalidParameterError("Bad parameter: to must be an list")
    if "note" in params and not isinstance(params["note"], str):
        raise InvalidParameterError("Bad parameter: note must be an str")
    if "recipients" in params and not isinstance(
        params["recipients"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: recipients must be an list"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request(
        "POST", "/bundles/{id}/share".format(id=params["id"]), params, options
    )
    return response.data


# Parameters:
#   paths - array(string) - A list of paths to include in this bundle.
#   password - string - Password for this bundle.
#   form_field_set_id - int64 - Id of Form Field Set to use with this bundle
#   clickwrap_id - int64 - ID of the clickwrap to use with this bundle.
#   code - string - Bundle code.  This code forms the end part of the Public URL.
#   create_snapshot - boolean - If true, create a snapshot of this bundle's contents.
#   description - string - Public description
#   dont_separate_submissions_by_folder - boolean - Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
#   expires_at - string - Bundle expiration date/time
#   finalize_snapshot - boolean - If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
#   inbox_id - int64 - ID of the associated inbox, if available.
#   max_uses - int64 - Maximum number of times bundle can be accessed
#   note - string - Bundle internal note
#   path_template - string - Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, and any custom form data.
#   permissions - string - Permissions that apply to Folders in this Share Link.
#   preview_only - boolean - DEPRECATED: Restrict users to previewing files only. Use `permissions` instead.
#   require_registration - boolean - Show a registration page that captures the downloader's name and email address?
#   require_share_recipient - boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
#   send_email_receipt_to_uploader - boolean - Send delivery receipt to the uploader. Note: For writable share only
#   skip_company - boolean - BundleRegistrations can be saved without providing company?
#   start_access_on_date - string - Date when share will start to be accessible. If `nil` access granted right after create.
#   skip_email - boolean - BundleRegistrations can be saved without providing email?
#   skip_name - boolean - BundleRegistrations can be saved without providing name?
#   watermark_attachment_delete - boolean - If true, will delete the file stored in watermark_attachment
#   watermark_attachment_file - file - Preview watermark image applied to all bundle items.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "paths" in params and not isinstance(params["paths"], builtins.list):
        raise InvalidParameterError("Bad parameter: paths must be an list")
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "form_field_set_id" in params and not isinstance(
        params["form_field_set_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: form_field_set_id must be an int"
        )
    if "clickwrap_id" in params and not isinstance(
        params["clickwrap_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: clickwrap_id must be an int"
        )
    if "code" in params and not isinstance(params["code"], str):
        raise InvalidParameterError("Bad parameter: code must be an str")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "expires_at" in params and not isinstance(params["expires_at"], str):
        raise InvalidParameterError("Bad parameter: expires_at must be an str")
    if "inbox_id" in params and not isinstance(params["inbox_id"], int):
        raise InvalidParameterError("Bad parameter: inbox_id must be an int")
    if "max_uses" in params and not isinstance(params["max_uses"], int):
        raise InvalidParameterError("Bad parameter: max_uses must be an int")
    if "note" in params and not isinstance(params["note"], str):
        raise InvalidParameterError("Bad parameter: note must be an str")
    if "path_template" in params and not isinstance(
        params["path_template"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: path_template must be an str"
        )
    if "permissions" in params and not isinstance(params["permissions"], str):
        raise InvalidParameterError(
            "Bad parameter: permissions must be an str"
        )
    if "start_access_on_date" in params and not isinstance(
        params["start_access_on_date"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: start_access_on_date must be an str"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH", "/bundles/{id}".format(id=params["id"]), params, options
    )
    return Bundle(response.data, options)


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
        "DELETE", "/bundles/{id}".format(id=params["id"]), params, options
    )
    return response.data


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return Bundle(*args, **kwargs)
