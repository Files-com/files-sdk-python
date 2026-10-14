import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.attachment import with_attachments
from files_sdk.api import (  # noqa: F401
    LEGACY,
    LegacyScope,
    Operation,
    copy_params,
    decode_record,
    path_value,
)
from files_sdk.api_client import unexpected_response_error  # noqa: F401
from files_sdk.context import RequestOptions  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Bundle:
    """A bundle record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        code: string - Bundle code. This code forms the end part of the Public URL.
        color_left: string - Page link and button color
        color_link: string - Top bar link color
        color_text: string - Page link and button color
        color_top: string - Top bar background color
        color_top_text: string - Top bar text color
        url: string - Public URL of Share Link
        description: string - Public description
        expires_at: date-time - Explicit Bundle expiration date/time. If not set, the site-wide expiration setting may apply.
        password_protected: boolean - Is this bundle password protected?
        permissions: string - Permissions that apply to Folders in this Share Link.
        preview_only: boolean
        require_registration: boolean - Show a registration page that captures the downloader's name and email address?
        require_share_recipient: boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
        require_logout: boolean - If true, we will hide the 'Remember Me' box on the Bundle registration page, requiring that the user logout and log back in every time they visit the page.
        clickwrap_body: string - Legal text that must be agreed to prior to accessing Bundle.
        form_field_set: FormFieldSet - Custom Form to use
        skip_name: boolean - BundleRegistrations can be saved without providing name?
        skip_email: boolean - BundleRegistrations can be saved without providing email?
        start_access_on_date: date-time - Date when share will start to be accessible. If `nil` access granted right after create.
        skip_company: boolean - BundleRegistrations can be saved without providing company?
        id: int64 - Bundle ID
        bypasses_site_expiration_rules: boolean - If true, this Share Link bypasses site-wide expiration rules. Only site admins may set this.
        created_at: date-time - Bundle created at date/time
        deleted: boolean - Indicates if the bundle has been deleted.
        deleted_at: date-time - Bundle deleted at date/time
        dont_separate_submissions_by_folder: boolean - Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
        effective_expires_at: date-time - Read-only expiration date/time, using the explicit expiration or the site-wide setting when applicable. Null when the Share Link does not expire.
        max_uses: int64 - Maximum number of times bundle can be accessed
        internal_name: string - Internal name for identifying this Share Link.
        note: string - Bundle internal note
        path_template: string - Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, `strftime` directives, and any custom form data.
        path_template_time_zone: string - Timezone to use when rendering timestamps in path templates.
        send_email_receipt_to_uploader: boolean - Send delivery receipt to the uploader. Note: For writable share only
        snapshot_id: int64 - ID of the snapshot containing this bundle's contents.
        user_id: int64 - Bundle creator user ID
        username: string - Bundle creator username
        group_id: int64 - Owning group ID. If set, members of this group can view, edit, and share this Share Link.
        clickwrap_id: int64 - ID of the clickwrap to use with this bundle.
        inbox_id: int64 - ID of the associated inbox, if available.
        watermark_attachment: Image - Preview watermark image applied to all bundle items.
        watermark_value: object - Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
        send_one_time_password_to_recipient_at_registration: boolean - If true, require_share_recipient bundles will send a one-time password to the recipient when they register. Cannot be enabled if the bundle has a password set.
        workspace_id: int64 - Workspace ID. `0` means the default workspace.
        has_inbox: boolean - Does this bundle have an associated inbox?
        dont_allow_folders_in_uploads: boolean - Should folder uploads be prevented?
        requested_upload_slots: array(object) - Upload slots requested by the associated Inbox. Each slot contains a name used as its label and destination subfolder name.
        paths: array(string) - A list of paths in this bundle. For performance reasons, this is not provided when listing bundles.
        bundlepaths: array(object) - A list of bundlepaths in this bundle. For performance reasons, this is not provided when listing bundles.
        password: string - Password for this bundle.
        form_field_set_id: int64 - Id of Form Field Set to use with this bundle
        create_snapshot: boolean - If true, create a snapshot of this bundle's contents.
        finalize_snapshot: boolean - If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
        watermark_attachment_file: file - Preview watermark image applied to all bundle items.
        watermark_attachment_delete: boolean - If true, will delete the file stored in watermark_attachment
    """

    default_attributes = {
        "code": None,  # string - Bundle code.  This code forms the end part of the Public URL.
        "color_left": None,  # string - Page link and button color
        "color_link": None,  # string - Top bar link color
        "color_text": None,  # string - Page link and button color
        "color_top": None,  # string - Top bar background color
        "color_top_text": None,  # string - Top bar text color
        "url": None,  # string - Public URL of Share Link
        "description": None,  # string - Public description
        "expires_at": None,  # date-time - Explicit Bundle expiration date/time. If not set, the site-wide expiration setting may apply.
        "password_protected": None,  # boolean - Is this bundle password protected?
        "permissions": None,  # string - Permissions that apply to Folders in this Share Link.
        "preview_only": None,  # boolean
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
        "bypasses_site_expiration_rules": None,  # boolean - If true, this Share Link bypasses site-wide expiration rules. Only site admins may set this.
        "created_at": None,  # date-time - Bundle created at date/time
        "deleted": None,  # boolean - Indicates if the bundle has been deleted.
        "deleted_at": None,  # date-time - Bundle deleted at date/time
        "dont_separate_submissions_by_folder": None,  # boolean - Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
        "effective_expires_at": None,  # date-time - Read-only expiration date/time, using the explicit expiration or the site-wide setting when applicable. Null when the Share Link does not expire.
        "max_uses": None,  # int64 - Maximum number of times bundle can be accessed
        "internal_name": None,  # string - Internal name for identifying this Share Link.
        "note": None,  # string - Bundle internal note
        "path_template": None,  # string - Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, `strftime` directives, and any custom form data.
        "path_template_time_zone": None,  # string - Timezone to use when rendering timestamps in path templates.
        "send_email_receipt_to_uploader": None,  # boolean - Send delivery receipt to the uploader. Note: For writable share only
        "snapshot_id": None,  # int64 - ID of the snapshot containing this bundle's contents.
        "user_id": None,  # int64 - Bundle creator user ID
        "username": None,  # string - Bundle creator username
        "group_id": None,  # int64 - Owning group ID. If set, members of this group can view, edit, and share this Share Link.
        "clickwrap_id": None,  # int64 - ID of the clickwrap to use with this bundle.
        "inbox_id": None,  # int64 - ID of the associated inbox, if available.
        "watermark_attachment": None,  # Image - Preview watermark image applied to all bundle items.
        "watermark_value": None,  # object - Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
        "send_one_time_password_to_recipient_at_registration": None,  # boolean - If true, require_share_recipient bundles will send a one-time password to the recipient when they register. Cannot be enabled if the bundle has a password set.
        "workspace_id": None,  # int64 - Workspace ID. `0` means the default workspace.
        "has_inbox": None,  # boolean - Does this bundle have an associated inbox?
        "dont_allow_folders_in_uploads": None,  # boolean - Should folder uploads be prevented?
        "requested_upload_slots": None,  # array(object) - Upload slots requested by the associated Inbox. Each slot contains a name used as its label and destination subfolder name.
        "paths": None,  # array(string) - A list of paths in this bundle.  For performance reasons, this is not provided when listing bundles.
        "bundlepaths": None,  # array(object) - A list of bundlepaths in this bundle.  For performance reasons, this is not provided when listing bundles.
        "password": None,  # string - Password for this bundle.
        "form_field_set_id": None,  # int64 - Id of Form Field Set to use with this bundle
        "create_snapshot": None,  # boolean - If true, create a snapshot of this bundle's contents.
        "finalize_snapshot": None,  # boolean - If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
        "watermark_attachment_file": None,  # file - Preview watermark image applied to all bundle items.
        "watermark_attachment_delete": None,  # boolean - If true, will delete the file stored in watermark_attachment
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    code: str | None
    color_left: str | None
    color_link: str | None
    color_text: str | None
    color_top: str | None
    color_top_text: str | None
    url: str | None
    description: str | None
    expires_at: str | None
    password_protected: bool | None
    permissions: str | None
    preview_only: bool | None
    require_registration: bool | None
    require_share_recipient: bool | None
    require_logout: bool | None
    clickwrap_body: str | None
    form_field_set: dict[str, Any] | None
    skip_name: bool | None
    skip_email: bool | None
    start_access_on_date: str | None
    skip_company: bool | None
    id: int | None
    bypasses_site_expiration_rules: bool | None
    created_at: str | None
    deleted: bool | None
    deleted_at: str | None
    dont_separate_submissions_by_folder: bool | None
    effective_expires_at: str | None
    max_uses: int | None
    internal_name: str | None
    note: str | None
    path_template: str | None
    path_template_time_zone: str | None
    send_email_receipt_to_uploader: bool | None
    snapshot_id: int | None
    user_id: int | None
    username: str | None
    group_id: int | None
    clickwrap_id: int | None
    inbox_id: int | None
    watermark_attachment: dict[str, Any] | None
    watermark_value: dict[str, Any] | None
    send_one_time_password_to_recipient_at_registration: bool | None
    workspace_id: int | None
    has_inbox: bool | None
    dont_allow_folders_in_uploads: bool | None
    requested_upload_slots: builtins.list[dict[str, Any]] | None
    paths: builtins.list[str] | None
    bundlepaths: builtins.list[dict[str, Any]] | None
    password: str | None
    form_field_set_id: int | None
    create_snapshot: bool | None
    finalize_snapshot: bool | None
    watermark_attachment_file: Any
    watermark_attachment_delete: bool | None

    # The client and settings this object's operations use: those of the
    # operation or client that made it, or the module's when it starts an
    # operation if neither did.
    _context: Any = None

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = dict(options)

    def set_attributes(self, attributes):
        for attribute, default_value in Bundle.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Bundle.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def share(self, params: dict[str, Any] | None = None) -> None:
        """Send email(s) with a link to bundle

        Parameters:
          to - array(string) - A list of email addresses to share this bundle with. Required unless `recipients` is used.
          note - string - Note to include in email.
          recipients - array(object) - A list of recipients to share this bundle with. Required unless `to` is used.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
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
        operation = Operation.start(self._scope())
        operation.request(
            "POST", "/bundles/" + path_value(params["id"]) + "/share", params
        )

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          paths - array(string) - A list of paths to include in this bundle.
          password - string - Password for this bundle.
          bypasses_site_expiration_rules - boolean - If true, this Share Link bypasses site-wide expiration rules. Only site admins may set this.
          form_field_set_id - int64 - Id of Form Field Set to use with this bundle
          clickwrap_id - int64 - ID of the clickwrap to use with this bundle.
          code - string - Bundle code.  This code forms the end part of the Public URL.
          create_snapshot - boolean - If true, create a snapshot of this bundle's contents.
          description - string - Public description
          dont_separate_submissions_by_folder - boolean - Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
          expires_at - string - Explicit Bundle expiration date/time. If not set, the site-wide expiration setting may apply.
          finalize_snapshot - boolean - If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
          inbox_id - int64 - ID of the associated inbox, if available.
          max_uses - int64 - Maximum number of times bundle can be accessed
          group_id - int64 - Owning group ID. If set, members of this group can view, edit, and share this Share Link.
          internal_name - string - Internal name for identifying this Share Link.
          note - string - Bundle internal note
          path_template - string - Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, `strftime` directives, and any custom form data.
          path_template_time_zone - string - Timezone to use when rendering timestamps in path templates.
          permissions - string - Permissions that apply to Folders in this Share Link.
          require_registration - boolean - Show a registration page that captures the downloader's name and email address?
          require_share_recipient - boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
          send_one_time_password_to_recipient_at_registration - boolean - If true, require_share_recipient bundles will send a one-time password to the recipient when they register. Cannot be enabled if the bundle has a password set.
          send_email_receipt_to_uploader - boolean - Send delivery receipt to the uploader. Note: For writable share only
          skip_company - boolean - BundleRegistrations can be saved without providing company?
          start_access_on_date - string - Date when share will start to be accessible. If `nil` access granted right after create.
          skip_email - boolean - BundleRegistrations can be saved without providing email?
          skip_name - boolean - BundleRegistrations can be saved without providing name?
          user_id - int64 - The owning user id. Only site admins can set this.
          watermark_attachment_delete - boolean - If true, will delete the file stored in watermark_attachment
          watermark_attachment_file - file - Preview watermark image applied to all bundle items.
          watermark_value - object - Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
          workspace_id - int64 - Workspace ID. `0` means the default workspace.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "paths" in params and not isinstance(
            params["paths"], builtins.list
        ):
            raise InvalidParameterError("Bad parameter: paths must be an list")
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError(
                "Bad parameter: password must be an str"
            )
        if "bypasses_site_expiration_rules" in params and isinstance(
            params["bypasses_site_expiration_rules"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: bypasses_site_expiration_rules must be an bool"
            )
        if "form_field_set_id" in params and (
            not isinstance(params["form_field_set_id"], int)
            or isinstance(params["form_field_set_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: form_field_set_id must be an int"
            )
        if "clickwrap_id" in params and (
            not isinstance(params["clickwrap_id"], int)
            or isinstance(params["clickwrap_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: clickwrap_id must be an int"
            )
        if "code" in params and not isinstance(params["code"], str):
            raise InvalidParameterError("Bad parameter: code must be an str")
        if "create_snapshot" in params and isinstance(
            params["create_snapshot"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: create_snapshot must be an bool"
            )
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "dont_separate_submissions_by_folder" in params and isinstance(
            params["dont_separate_submissions_by_folder"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: dont_separate_submissions_by_folder must be an bool"
            )
        if "expires_at" in params and not isinstance(
            params["expires_at"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: expires_at must be an str"
            )
        if "finalize_snapshot" in params and isinstance(
            params["finalize_snapshot"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: finalize_snapshot must be an bool"
            )
        if "inbox_id" in params and (
            not isinstance(params["inbox_id"], int)
            or isinstance(params["inbox_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inbox_id must be an int"
            )
        if "max_uses" in params and (
            not isinstance(params["max_uses"], int)
            or isinstance(params["max_uses"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: max_uses must be an int"
            )
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "internal_name" in params and not isinstance(
            params["internal_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: internal_name must be an str"
            )
        if "note" in params and not isinstance(params["note"], str):
            raise InvalidParameterError("Bad parameter: note must be an str")
        if "path_template" in params and not isinstance(
            params["path_template"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: path_template must be an str"
            )
        if "path_template_time_zone" in params and not isinstance(
            params["path_template_time_zone"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: path_template_time_zone must be an str"
            )
        if "permissions" in params and not isinstance(
            params["permissions"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: permissions must be an str"
            )
        if "require_registration" in params and isinstance(
            params["require_registration"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: require_registration must be an bool"
            )
        if "require_share_recipient" in params and isinstance(
            params["require_share_recipient"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: require_share_recipient must be an bool"
            )
        if (
            "send_one_time_password_to_recipient_at_registration" in params
            and isinstance(
                params["send_one_time_password_to_recipient_at_registration"],
                (builtins.list, tuple, dict),
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: send_one_time_password_to_recipient_at_registration must be an bool"
            )
        if "send_email_receipt_to_uploader" in params and isinstance(
            params["send_email_receipt_to_uploader"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: send_email_receipt_to_uploader must be an bool"
            )
        if "skip_company" in params and isinstance(
            params["skip_company"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_company must be an bool"
            )
        if "start_access_on_date" in params and not isinstance(
            params["start_access_on_date"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: start_access_on_date must be an str"
            )
        if "skip_email" in params and isinstance(
            params["skip_email"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_email must be an bool"
            )
        if "skip_name" in params and isinstance(
            params["skip_name"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_name must be an bool"
            )
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "watermark_attachment_delete" in params and isinstance(
            params["watermark_attachment_delete"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: watermark_attachment_delete must be an bool"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        params = with_attachments(params, "watermark_attachment_file")
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/bundles/" + path_value(params["id"]), params
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE", "/bundles/" + path_value(params["id"]), params
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Update this object on the server if it has an id, or else create
        it, taking in place the record the server returns."""
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = BundleResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class BundleResource:
    """Bundle operations that use one client's configuration.

    Get one from a client, such as ``client.bundle``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Bundle]:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `expires_at`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `expires_at`, `code`, `group_id`, `user_id` or `bypasses_site_expiration_rules`. Valid field combinations are `[ group_id, expires_at ]` and `[ user_id, expires_at ]`.
        filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at` and `expires_at`.
        filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at` and `expires_at`.
        filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `code`.
        filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at` and `expires_at`.
        filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at` and `expires_at`.
        deleted - boolean - If true, only list deleted Share Links.
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        if "sort_by" in params and not isinstance(params["sort_by"], dict):
            raise InvalidParameterError(
                "Bad parameter: sort_by must be an dict"
            )
        if "filter" in params and not isinstance(params["filter"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter must be an dict"
            )
        if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter_gt must be an dict"
            )
        if "filter_gteq" in params and not isinstance(
            params["filter_gteq"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_gteq must be an dict"
            )
        if "filter_prefix" in params and not isinstance(
            params["filter_prefix"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_prefix must be an dict"
            )
        if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter_lt must be an dict"
            )
        if "filter_lteq" in params and not isinstance(
            params["filter_lteq"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_lteq must be an dict"
            )
        if "deleted" in params and not isinstance(params["deleted"], bool):
            raise InvalidParameterError(
                "Bad parameter: deleted must be an bool"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(Bundle, "GET", "/bundles", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Bundle]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Bundle:
        """Parameters:
        id (required) - int64 - Bundle ID.
        deleted - boolean - If true, show a deleted Share Link.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Bundle:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "deleted" in params and not isinstance(params["deleted"], bool):
            raise InvalidParameterError(
                "Bad parameter: deleted must be an bool"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/bundles/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Bundle)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Bundle:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Bundle:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        paths (required) - array(string) - A list of paths to include in this bundle.
        password - string - Password for this bundle.
        bypasses_site_expiration_rules - boolean - If true, this Share Link bypasses site-wide expiration rules. Only site admins may set this.
        form_field_set_id - int64 - Id of Form Field Set to use with this bundle
        create_snapshot - boolean - If true, create a snapshot of this bundle's contents.
        dont_separate_submissions_by_folder - boolean - Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
        expires_at - string - Explicit Bundle expiration date/time. If not set, the site-wide expiration setting may apply.
        finalize_snapshot - boolean - If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
        max_uses - int64 - Maximum number of times bundle can be accessed
        group_id - int64 - Owning group ID. If set, members of this group can view, edit, and share this Share Link.
        internal_name - string - Internal name for identifying this Share Link.
        description - string - Public description
        note - string - Bundle internal note
        code - string - Bundle code.  This code forms the end part of the Public URL.
        path_template - string - Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, `strftime` directives, and any custom form data.
        path_template_time_zone - string - Timezone to use when rendering timestamps in path templates.
        permissions - string - Permissions that apply to Folders in this Share Link.
        require_registration - boolean - Show a registration page that captures the downloader's name and email address?
        clickwrap_id - int64 - ID of the clickwrap to use with this bundle.
        inbox_id - int64 - ID of the associated inbox, if available.
        require_share_recipient - boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
        send_one_time_password_to_recipient_at_registration - boolean - If true, require_share_recipient bundles will send a one-time password to the recipient when they register. Cannot be enabled if the bundle has a password set.
        send_email_receipt_to_uploader - boolean - Send delivery receipt to the uploader. Note: For writable share only
        skip_email - boolean - BundleRegistrations can be saved without providing email?
        skip_name - boolean - BundleRegistrations can be saved without providing name?
        skip_company - boolean - BundleRegistrations can be saved without providing company?
        start_access_on_date - string - Date when share will start to be accessible. If `nil` access granted right after create.
        snapshot_id - int64 - ID of the snapshot containing this bundle's contents.
        workspace_id - int64 - Workspace ID. `0` means the default workspace.
        watermark_attachment_file - file - Preview watermark image applied to all bundle items.
        watermark_value - object - Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "paths" in params and not isinstance(
            params["paths"], builtins.list
        ):
            raise InvalidParameterError("Bad parameter: paths must be an list")
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError(
                "Bad parameter: password must be an str"
            )
        if "bypasses_site_expiration_rules" in params and not isinstance(
            params["bypasses_site_expiration_rules"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: bypasses_site_expiration_rules must be an bool"
            )
        if "form_field_set_id" in params and (
            not isinstance(params["form_field_set_id"], int)
            or isinstance(params["form_field_set_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: form_field_set_id must be an int"
            )
        if "create_snapshot" in params and not isinstance(
            params["create_snapshot"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: create_snapshot must be an bool"
            )
        if "dont_separate_submissions_by_folder" in params and not isinstance(
            params["dont_separate_submissions_by_folder"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: dont_separate_submissions_by_folder must be an bool"
            )
        if "expires_at" in params and not isinstance(
            params["expires_at"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: expires_at must be an str"
            )
        if "finalize_snapshot" in params and not isinstance(
            params["finalize_snapshot"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: finalize_snapshot must be an bool"
            )
        if "max_uses" in params and (
            not isinstance(params["max_uses"], int)
            or isinstance(params["max_uses"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: max_uses must be an int"
            )
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "internal_name" in params and not isinstance(
            params["internal_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: internal_name must be an str"
            )
        if "description" in params and not isinstance(
            params["description"], str
        ):
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
        if "path_template_time_zone" in params and not isinstance(
            params["path_template_time_zone"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: path_template_time_zone must be an str"
            )
        if "permissions" in params and not isinstance(
            params["permissions"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: permissions must be an str"
            )
        if "require_registration" in params and not isinstance(
            params["require_registration"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: require_registration must be an bool"
            )
        if "clickwrap_id" in params and (
            not isinstance(params["clickwrap_id"], int)
            or isinstance(params["clickwrap_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: clickwrap_id must be an int"
            )
        if "inbox_id" in params and (
            not isinstance(params["inbox_id"], int)
            or isinstance(params["inbox_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inbox_id must be an int"
            )
        if "require_share_recipient" in params and not isinstance(
            params["require_share_recipient"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: require_share_recipient must be an bool"
            )
        if (
            "send_one_time_password_to_recipient_at_registration" in params
            and not isinstance(
                params["send_one_time_password_to_recipient_at_registration"],
                bool,
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: send_one_time_password_to_recipient_at_registration must be an bool"
            )
        if "send_email_receipt_to_uploader" in params and not isinstance(
            params["send_email_receipt_to_uploader"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: send_email_receipt_to_uploader must be an bool"
            )
        if "skip_email" in params and not isinstance(
            params["skip_email"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_email must be an bool"
            )
        if "skip_name" in params and not isinstance(params["skip_name"], bool):
            raise InvalidParameterError(
                "Bad parameter: skip_name must be an bool"
            )
        if "skip_company" in params and not isinstance(
            params["skip_company"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_company must be an bool"
            )
        if "start_access_on_date" in params and not isinstance(
            params["start_access_on_date"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: start_access_on_date must be an str"
            )
        if "snapshot_id" in params and (
            not isinstance(params["snapshot_id"], int)
            or isinstance(params["snapshot_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: snapshot_id must be an int"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "watermark_value" in params and not isinstance(
            params["watermark_value"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: watermark_value must be an dict"
            )
        if "paths" not in params:
            raise MissingParameterError("Parameter missing: paths")
        params = with_attachments(params, "watermark_attachment_file")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/bundles", params)
        return operation.decode_model(response, Bundle)

    def share(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Send email(s) with a link to bundle

        Parameters:
          to - array(string) - A list of email addresses to share this bundle with. Required unless `recipients` is used.
          note - string - Note to include in email.
          recipients - array(object) - A list of recipients to share this bundle with. Required unless `to` is used.
        """
        return self.__share({"id": id}, params, options)

    def __share(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
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
        operation = Operation.start(self._scope, options)
        operation.request(
            "POST", "/bundles/" + path_value(params["id"]) + "/share", params
        )

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Bundle:
        """Parameters:
        paths - array(string) - A list of paths to include in this bundle.
        password - string - Password for this bundle.
        bypasses_site_expiration_rules - boolean - If true, this Share Link bypasses site-wide expiration rules. Only site admins may set this.
        form_field_set_id - int64 - Id of Form Field Set to use with this bundle
        clickwrap_id - int64 - ID of the clickwrap to use with this bundle.
        code - string - Bundle code.  This code forms the end part of the Public URL.
        create_snapshot - boolean - If true, create a snapshot of this bundle's contents.
        description - string - Public description
        dont_separate_submissions_by_folder - boolean - Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
        expires_at - string - Explicit Bundle expiration date/time. If not set, the site-wide expiration setting may apply.
        finalize_snapshot - boolean - If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
        inbox_id - int64 - ID of the associated inbox, if available.
        max_uses - int64 - Maximum number of times bundle can be accessed
        group_id - int64 - Owning group ID. If set, members of this group can view, edit, and share this Share Link.
        internal_name - string - Internal name for identifying this Share Link.
        note - string - Bundle internal note
        path_template - string - Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, `strftime` directives, and any custom form data.
        path_template_time_zone - string - Timezone to use when rendering timestamps in path templates.
        permissions - string - Permissions that apply to Folders in this Share Link.
        require_registration - boolean - Show a registration page that captures the downloader's name and email address?
        require_share_recipient - boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
        send_one_time_password_to_recipient_at_registration - boolean - If true, require_share_recipient bundles will send a one-time password to the recipient when they register. Cannot be enabled if the bundle has a password set.
        send_email_receipt_to_uploader - boolean - Send delivery receipt to the uploader. Note: For writable share only
        skip_company - boolean - BundleRegistrations can be saved without providing company?
        start_access_on_date - string - Date when share will start to be accessible. If `nil` access granted right after create.
        skip_email - boolean - BundleRegistrations can be saved without providing email?
        skip_name - boolean - BundleRegistrations can be saved without providing name?
        user_id - int64 - The owning user id. Only site admins can set this.
        watermark_attachment_delete - boolean - If true, will delete the file stored in watermark_attachment
        watermark_attachment_file - file - Preview watermark image applied to all bundle items.
        watermark_value - object - Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
        workspace_id - int64 - Workspace ID. `0` means the default workspace.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Bundle:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "paths" in params and not isinstance(
            params["paths"], builtins.list
        ):
            raise InvalidParameterError("Bad parameter: paths must be an list")
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError(
                "Bad parameter: password must be an str"
            )
        if "bypasses_site_expiration_rules" in params and not isinstance(
            params["bypasses_site_expiration_rules"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: bypasses_site_expiration_rules must be an bool"
            )
        if "form_field_set_id" in params and (
            not isinstance(params["form_field_set_id"], int)
            or isinstance(params["form_field_set_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: form_field_set_id must be an int"
            )
        if "clickwrap_id" in params and (
            not isinstance(params["clickwrap_id"], int)
            or isinstance(params["clickwrap_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: clickwrap_id must be an int"
            )
        if "code" in params and not isinstance(params["code"], str):
            raise InvalidParameterError("Bad parameter: code must be an str")
        if "create_snapshot" in params and not isinstance(
            params["create_snapshot"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: create_snapshot must be an bool"
            )
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "dont_separate_submissions_by_folder" in params and not isinstance(
            params["dont_separate_submissions_by_folder"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: dont_separate_submissions_by_folder must be an bool"
            )
        if "expires_at" in params and not isinstance(
            params["expires_at"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: expires_at must be an str"
            )
        if "finalize_snapshot" in params and not isinstance(
            params["finalize_snapshot"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: finalize_snapshot must be an bool"
            )
        if "inbox_id" in params and (
            not isinstance(params["inbox_id"], int)
            or isinstance(params["inbox_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inbox_id must be an int"
            )
        if "max_uses" in params and (
            not isinstance(params["max_uses"], int)
            or isinstance(params["max_uses"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: max_uses must be an int"
            )
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "internal_name" in params and not isinstance(
            params["internal_name"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: internal_name must be an str"
            )
        if "note" in params and not isinstance(params["note"], str):
            raise InvalidParameterError("Bad parameter: note must be an str")
        if "path_template" in params and not isinstance(
            params["path_template"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: path_template must be an str"
            )
        if "path_template_time_zone" in params and not isinstance(
            params["path_template_time_zone"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: path_template_time_zone must be an str"
            )
        if "permissions" in params and not isinstance(
            params["permissions"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: permissions must be an str"
            )
        if "require_registration" in params and not isinstance(
            params["require_registration"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: require_registration must be an bool"
            )
        if "require_share_recipient" in params and not isinstance(
            params["require_share_recipient"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: require_share_recipient must be an bool"
            )
        if (
            "send_one_time_password_to_recipient_at_registration" in params
            and not isinstance(
                params["send_one_time_password_to_recipient_at_registration"],
                bool,
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: send_one_time_password_to_recipient_at_registration must be an bool"
            )
        if "send_email_receipt_to_uploader" in params and not isinstance(
            params["send_email_receipt_to_uploader"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: send_email_receipt_to_uploader must be an bool"
            )
        if "skip_company" in params and not isinstance(
            params["skip_company"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_company must be an bool"
            )
        if "start_access_on_date" in params and not isinstance(
            params["start_access_on_date"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: start_access_on_date must be an str"
            )
        if "skip_email" in params and not isinstance(
            params["skip_email"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: skip_email must be an bool"
            )
        if "skip_name" in params and not isinstance(params["skip_name"], bool):
            raise InvalidParameterError(
                "Bad parameter: skip_name must be an bool"
            )
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "watermark_attachment_delete" in params and not isinstance(
            params["watermark_attachment_delete"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: watermark_attachment_delete must be an bool"
            )
        if "watermark_value" in params and not isinstance(
            params["watermark_value"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: watermark_value must be an dict"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        params = with_attachments(params, "watermark_attachment_file")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/bundles/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Bundle)

    def delete(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        return self.__delete({"id": id}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE", "/bundles/" + path_value(params["id"]), params
        )

    def destroy(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Bundle:
        """A new Bundle with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Bundle(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = BundleResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Bundle]:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `expires_at`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `expires_at`, `code`, `group_id`, `user_id` or `bypasses_site_expiration_rules`. Valid field combinations are `[ group_id, expires_at ]` and `[ user_id, expires_at ]`.
    filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at` and `expires_at`.
    filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at` and `expires_at`.
    filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `code`.
    filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at` and `expires_at`.
    filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at` and `expires_at`.
    deleted - boolean - If true, only list deleted Share Links.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Bundle]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Bundle:
    """Parameters:
    id (required) - int64 - Bundle ID.
    deleted - boolean - If true, show a deleted Share Link.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Bundle:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Bundle:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    paths (required) - array(string) - A list of paths to include in this bundle.
    password - string - Password for this bundle.
    bypasses_site_expiration_rules - boolean - If true, this Share Link bypasses site-wide expiration rules. Only site admins may set this.
    form_field_set_id - int64 - Id of Form Field Set to use with this bundle
    create_snapshot - boolean - If true, create a snapshot of this bundle's contents.
    dont_separate_submissions_by_folder - boolean - Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
    expires_at - string - Explicit Bundle expiration date/time. If not set, the site-wide expiration setting may apply.
    finalize_snapshot - boolean - If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
    max_uses - int64 - Maximum number of times bundle can be accessed
    group_id - int64 - Owning group ID. If set, members of this group can view, edit, and share this Share Link.
    internal_name - string - Internal name for identifying this Share Link.
    description - string - Public description
    note - string - Bundle internal note
    code - string - Bundle code.  This code forms the end part of the Public URL.
    path_template - string - Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, `strftime` directives, and any custom form data.
    path_template_time_zone - string - Timezone to use when rendering timestamps in path templates.
    permissions - string - Permissions that apply to Folders in this Share Link.
    require_registration - boolean - Show a registration page that captures the downloader's name and email address?
    clickwrap_id - int64 - ID of the clickwrap to use with this bundle.
    inbox_id - int64 - ID of the associated inbox, if available.
    require_share_recipient - boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
    send_one_time_password_to_recipient_at_registration - boolean - If true, require_share_recipient bundles will send a one-time password to the recipient when they register. Cannot be enabled if the bundle has a password set.
    send_email_receipt_to_uploader - boolean - Send delivery receipt to the uploader. Note: For writable share only
    skip_email - boolean - BundleRegistrations can be saved without providing email?
    skip_name - boolean - BundleRegistrations can be saved without providing name?
    skip_company - boolean - BundleRegistrations can be saved without providing company?
    start_access_on_date - string - Date when share will start to be accessible. If `nil` access granted right after create.
    snapshot_id - int64 - ID of the snapshot containing this bundle's contents.
    workspace_id - int64 - Workspace ID. `0` means the default workspace.
    watermark_attachment_file - file - Preview watermark image applied to all bundle items.
    watermark_value - object - Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
    """
    return _legacy_resource.create(params, options)


def share(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Send email(s) with a link to bundle

    Parameters:
      to - array(string) - A list of email addresses to share this bundle with. Required unless `recipients` is used.
      note - string - Note to include in email.
      recipients - array(object) - A list of recipients to share this bundle with. Required unless `to` is used.
    """
    _legacy_resource.share(id, params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Bundle:
    """Parameters:
    paths - array(string) - A list of paths to include in this bundle.
    password - string - Password for this bundle.
    bypasses_site_expiration_rules - boolean - If true, this Share Link bypasses site-wide expiration rules. Only site admins may set this.
    form_field_set_id - int64 - Id of Form Field Set to use with this bundle
    clickwrap_id - int64 - ID of the clickwrap to use with this bundle.
    code - string - Bundle code.  This code forms the end part of the Public URL.
    create_snapshot - boolean - If true, create a snapshot of this bundle's contents.
    description - string - Public description
    dont_separate_submissions_by_folder - boolean - Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
    expires_at - string - Explicit Bundle expiration date/time. If not set, the site-wide expiration setting may apply.
    finalize_snapshot - boolean - If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
    inbox_id - int64 - ID of the associated inbox, if available.
    max_uses - int64 - Maximum number of times bundle can be accessed
    group_id - int64 - Owning group ID. If set, members of this group can view, edit, and share this Share Link.
    internal_name - string - Internal name for identifying this Share Link.
    note - string - Bundle internal note
    path_template - string - Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, `strftime` directives, and any custom form data.
    path_template_time_zone - string - Timezone to use when rendering timestamps in path templates.
    permissions - string - Permissions that apply to Folders in this Share Link.
    require_registration - boolean - Show a registration page that captures the downloader's name and email address?
    require_share_recipient - boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
    send_one_time_password_to_recipient_at_registration - boolean - If true, require_share_recipient bundles will send a one-time password to the recipient when they register. Cannot be enabled if the bundle has a password set.
    send_email_receipt_to_uploader - boolean - Send delivery receipt to the uploader. Note: For writable share only
    skip_company - boolean - BundleRegistrations can be saved without providing company?
    start_access_on_date - string - Date when share will start to be accessible. If `nil` access granted right after create.
    skip_email - boolean - BundleRegistrations can be saved without providing email?
    skip_name - boolean - BundleRegistrations can be saved without providing name?
    user_id - int64 - The owning user id. Only site admins can set this.
    watermark_attachment_delete - boolean - If true, will delete the file stored in watermark_attachment
    watermark_attachment_file - file - Preview watermark image applied to all bundle items.
    watermark_value - object - Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
    workspace_id - int64 - Workspace ID. `0` means the default workspace.
    """
    return _legacy_resource.update(id, params, options)


def delete(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    _legacy_resource.delete(id, params, options)


def destroy(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(id, params, options)


def new(*args, **kwargs) -> Bundle:
    return Bundle(*args, **kwargs)
