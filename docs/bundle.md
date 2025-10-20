# Bundle

## Example Bundle Object

```
{
  "code": "abc123",
  "color_left": "#0066a7",
  "color_link": "#d34f5d",
  "color_text": "#0066a7",
  "color_top": "#000000",
  "color_top_text": "#ffffff",
  "url": "https://subdomain.files.com/f/12345678",
  "description": "The public description of the bundle.",
  "expires_at": "2000-01-01T01:00:00Z",
  "password_protected": True,
  "permissions": "read",
  "preview_only": True,
  "require_registration": True,
  "require_share_recipient": True,
  "require_logout": True,
  "clickwrap_body": "[Legal text]",
  "form_field_set": {
    "id": 1,
    "title": "Sample Form Title",
    "form_layout": [
      1,
      2,
      3,
      4
    ],
    "form_fields": [
      {
        "id": 1,
        "label": "Sample Label",
        "required": True,
        "help_text": "Help Text",
        "field_type": "text",
        "options_for_select": [
          "red",
          "green",
          "blue"
        ],
        "default_option": "red",
        "form_field_set_id": 1
      }
    ],
    "skip_name": True,
    "skip_email": True,
    "skip_company": True,
    "in_use": True
  },
  "skip_name": True,
  "skip_email": True,
  "start_access_on_date": "2000-01-01T01:00:00Z",
  "skip_company": True,
  "id": 1,
  "created_at": "2000-01-01T01:00:00Z",
  "dont_separate_submissions_by_folder": True,
  "max_uses": 1,
  "note": "The internal note on the bundle.",
  "path_template": "{{name}}_{{ip}}",
  "path_template_time_zone": "Eastern Time (US & Canada)",
  "send_email_receipt_to_uploader": True,
  "snapshot_id": 1,
  "user_id": 1,
  "username": "user",
  "clickwrap_id": 1,
  "inbox_id": 1,
  "watermark_attachment": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "watermark_value": {
    "key": "example value"
  },
  "has_inbox": True,
  "dont_allow_folders_in_uploads": True,
  "paths": [
    "file.txt"
  ],
  "bundlepaths": [
    {
      "recursive": True,
      "path": "example"
    }
  ]
}
```

* `code` (string): Bundle code.  This code forms the end part of the Public URL.
* `color_left` (string): Page link and button color
* `color_link` (string): Top bar link color
* `color_text` (string): Page link and button color
* `color_top` (string): Top bar background color
* `color_top_text` (string): Top bar text color
* `url` (string): Public URL of Share Link
* `description` (string): Public description
* `expires_at` (date-time): Bundle expiration date/time
* `password_protected` (boolean): Is this bundle password protected?
* `permissions` (string): Permissions that apply to Folders in this Share Link.
* `preview_only` (boolean): 
* `require_registration` (boolean): Show a registration page that captures the downloader's name and email address?
* `require_share_recipient` (boolean): Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
* `require_logout` (boolean): If true, we will hide the 'Remember Me' box on the Bundle registration page, requiring that the user logout and log back in every time they visit the page.
* `clickwrap_body` (string): Legal text that must be agreed to prior to accessing Bundle.
* `form_field_set` (FormFieldSet): Custom Form to use
* `skip_name` (boolean): BundleRegistrations can be saved without providing name?
* `skip_email` (boolean): BundleRegistrations can be saved without providing email?
* `start_access_on_date` (date-time): Date when share will start to be accessible. If `nil` access granted right after create.
* `skip_company` (boolean): BundleRegistrations can be saved without providing company?
* `id` (int64): Bundle ID
* `created_at` (date-time): Bundle created at date/time
* `dont_separate_submissions_by_folder` (boolean): Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
* `max_uses` (int64): Maximum number of times bundle can be accessed
* `note` (string): Bundle internal note
* `path_template` (string): Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, `strftime` directives, and any custom form data.
* `path_template_time_zone` (string): Timezone to use when rendering timestamps in path templates.
* `send_email_receipt_to_uploader` (boolean): Send delivery receipt to the uploader. Note: For writable share only
* `snapshot_id` (int64): ID of the snapshot containing this bundle's contents.
* `user_id` (int64): Bundle creator user ID
* `username` (string): Bundle creator username
* `clickwrap_id` (int64): ID of the clickwrap to use with this bundle.
* `inbox_id` (int64): ID of the associated inbox, if available.
* `watermark_attachment` (Image): Preview watermark image applied to all bundle items.
* `watermark_value` (object): Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
* `has_inbox` (boolean): Does this bundle have an associated inbox?
* `dont_allow_folders_in_uploads` (boolean): Should folder uploads be prevented?
* `paths` (array(string)): A list of paths in this bundle.  For performance reasons, this is not provided when listing bundles.
* `bundlepaths` (array(object)): A list of bundlepaths in this bundle.  For performance reasons, this is not provided when listing bundles.
* `password` (string): Password for this bundle.
* `form_field_set_id` (int64): Id of Form Field Set to use with this bundle
* `create_snapshot` (boolean): If true, create a snapshot of this bundle's contents.
* `finalize_snapshot` (boolean): If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
* `watermark_attachment_file` (file): Preview watermark image applied to all bundle items.
* `watermark_attachment_delete` (boolean): If true, will delete the file stored in watermark_attachment


---

## List Share Links

```
files_sdk.bundle.list({
  "user_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `expires_at`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `expires_at`, `code` or `user_id`. Valid field combinations are `[ user_id, expires_at ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at` and `expires_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at` and `expires_at`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `code`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at` and `expires_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at` and `expires_at`.


---

## Show Share Link

```
files_sdk.bundle.find(id)
```

### Parameters

* `id` (int64): Required - Bundle ID.


---

## Create Share Link

```
files_sdk.bundle.create({
  "user_id": 1,
  "paths": ["file.txt"],
  "password": "Password",
  "form_field_set_id": 1,
  "create_snapshot": False,
  "dont_separate_submissions_by_folder": True,
  "expires_at": "2000-01-01T01:00:00Z",
  "finalize_snapshot": False,
  "max_uses": 1,
  "description": "The public description of the bundle.",
  "note": "The internal note on the bundle.",
  "code": "abc123",
  "path_template": "{{name}}_{{ip}}",
  "path_template_time_zone": "Eastern Time (US & Canada)",
  "permissions": "read",
  "require_registration": False,
  "clickwrap_id": 1,
  "inbox_id": 1,
  "require_share_recipient": False,
  "send_email_receipt_to_uploader": True,
  "skip_email": True,
  "skip_name": True,
  "skip_company": True,
  "start_access_on_date": "2000-01-01T01:00:00Z",
  "snapshot_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `paths` (array(string)): Required - A list of paths to include in this bundle.
* `password` (string): Password for this bundle.
* `form_field_set_id` (int64): Id of Form Field Set to use with this bundle
* `create_snapshot` (boolean): If true, create a snapshot of this bundle's contents.
* `dont_separate_submissions_by_folder` (boolean): Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
* `expires_at` (string): Bundle expiration date/time
* `finalize_snapshot` (boolean): If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
* `max_uses` (int64): Maximum number of times bundle can be accessed
* `description` (string): Public description
* `note` (string): Bundle internal note
* `code` (string): Bundle code.  This code forms the end part of the Public URL.
* `path_template` (string): Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, `strftime` directives, and any custom form data.
* `path_template_time_zone` (string): Timezone to use when rendering timestamps in path templates.
* `permissions` (string): Permissions that apply to Folders in this Share Link.
* `require_registration` (boolean): Show a registration page that captures the downloader's name and email address?
* `clickwrap_id` (int64): ID of the clickwrap to use with this bundle.
* `inbox_id` (int64): ID of the associated inbox, if available.
* `require_share_recipient` (boolean): Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
* `send_email_receipt_to_uploader` (boolean): Send delivery receipt to the uploader. Note: For writable share only
* `skip_email` (boolean): BundleRegistrations can be saved without providing email?
* `skip_name` (boolean): BundleRegistrations can be saved without providing name?
* `skip_company` (boolean): BundleRegistrations can be saved without providing company?
* `start_access_on_date` (string): Date when share will start to be accessible. If `nil` access granted right after create.
* `snapshot_id` (int64): ID of the snapshot containing this bundle's contents.
* `watermark_attachment_file` (file): Preview watermark image applied to all bundle items.


---

## Send email(s) with a link to bundle

```
files_sdk.bundle.share(id, {
  "to": ["johndoe@gmail.com"],
  "note": "Just a note.",
  "recipients": [{"name":"John Doe","company":"Acme Ltd","recipient":"johndoe@gmail.com"}]
})
```

### Parameters

* `id` (int64): Required - Bundle ID.
* `to` (array(string)): A list of email addresses to share this bundle with. Required unless `recipients` is used.
* `note` (string): Note to include in email.
* `recipients` (array(object)): A list of recipients to share this bundle with. Required unless `to` is used.


---

## Update Share Link

```
files_sdk.bundle.update(id, {
  "paths": ["file.txt"],
  "password": "Password",
  "form_field_set_id": 1,
  "clickwrap_id": 1,
  "code": "abc123",
  "create_snapshot": False,
  "description": "The public description of the bundle.",
  "dont_separate_submissions_by_folder": True,
  "expires_at": "2000-01-01T01:00:00Z",
  "finalize_snapshot": False,
  "inbox_id": 1,
  "max_uses": 1,
  "note": "The internal note on the bundle.",
  "path_template": "{{name}}_{{ip}}",
  "path_template_time_zone": "Eastern Time (US & Canada)",
  "permissions": "read",
  "require_registration": False,
  "require_share_recipient": False,
  "send_email_receipt_to_uploader": True,
  "skip_company": True,
  "start_access_on_date": "2000-01-01T01:00:00Z",
  "skip_email": True,
  "skip_name": True,
  "watermark_attachment_delete": False
})
```

### Parameters

* `id` (int64): Required - Bundle ID.
* `paths` (array(string)): A list of paths to include in this bundle.
* `password` (string): Password for this bundle.
* `form_field_set_id` (int64): Id of Form Field Set to use with this bundle
* `clickwrap_id` (int64): ID of the clickwrap to use with this bundle.
* `code` (string): Bundle code.  This code forms the end part of the Public URL.
* `create_snapshot` (boolean): If true, create a snapshot of this bundle's contents.
* `description` (string): Public description
* `dont_separate_submissions_by_folder` (boolean): Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
* `expires_at` (string): Bundle expiration date/time
* `finalize_snapshot` (boolean): If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
* `inbox_id` (int64): ID of the associated inbox, if available.
* `max_uses` (int64): Maximum number of times bundle can be accessed
* `note` (string): Bundle internal note
* `path_template` (string): Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, `strftime` directives, and any custom form data.
* `path_template_time_zone` (string): Timezone to use when rendering timestamps in path templates.
* `permissions` (string): Permissions that apply to Folders in this Share Link.
* `require_registration` (boolean): Show a registration page that captures the downloader's name and email address?
* `require_share_recipient` (boolean): Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
* `send_email_receipt_to_uploader` (boolean): Send delivery receipt to the uploader. Note: For writable share only
* `skip_company` (boolean): BundleRegistrations can be saved without providing company?
* `start_access_on_date` (string): Date when share will start to be accessible. If `nil` access granted right after create.
* `skip_email` (boolean): BundleRegistrations can be saved without providing email?
* `skip_name` (boolean): BundleRegistrations can be saved without providing name?
* `watermark_attachment_delete` (boolean): If true, will delete the file stored in watermark_attachment
* `watermark_attachment_file` (file): Preview watermark image applied to all bundle items.


---

## Delete Share Link

```
files_sdk.bundle.delete(id)
```

### Parameters

* `id` (int64): Required - Bundle ID.


---

## Send email(s) with a link to bundle

```
bundle = files_sdk.bundle.find(id)
bundle.share({
  "to": ["johndoe@gmail.com"],
  "note": "Just a note.",
  "recipients": [{"name":"John Doe","company":"Acme Ltd","recipient":"johndoe@gmail.com"}]
})
```

### Parameters

* `id` (int64): Required - Bundle ID.
* `to` (array(string)): A list of email addresses to share this bundle with. Required unless `recipients` is used.
* `note` (string): Note to include in email.
* `recipients` (array(object)): A list of recipients to share this bundle with. Required unless `to` is used.


---

## Update Share Link

```
bundle = files_sdk.bundle.find(id)
bundle.update({
  "paths": ["file.txt"],
  "password": "Password",
  "form_field_set_id": 1,
  "clickwrap_id": 1,
  "code": "abc123",
  "create_snapshot": False,
  "description": "The public description of the bundle.",
  "dont_separate_submissions_by_folder": True,
  "expires_at": "2000-01-01T01:00:00Z",
  "finalize_snapshot": False,
  "inbox_id": 1,
  "max_uses": 1,
  "note": "The internal note on the bundle.",
  "path_template": "{{name}}_{{ip}}",
  "path_template_time_zone": "Eastern Time (US & Canada)",
  "permissions": "read",
  "require_registration": False,
  "require_share_recipient": False,
  "send_email_receipt_to_uploader": True,
  "skip_company": True,
  "start_access_on_date": "2000-01-01T01:00:00Z",
  "skip_email": True,
  "skip_name": True,
  "watermark_attachment_delete": False
})
```

### Parameters

* `id` (int64): Required - Bundle ID.
* `paths` (array(string)): A list of paths to include in this bundle.
* `password` (string): Password for this bundle.
* `form_field_set_id` (int64): Id of Form Field Set to use with this bundle
* `clickwrap_id` (int64): ID of the clickwrap to use with this bundle.
* `code` (string): Bundle code.  This code forms the end part of the Public URL.
* `create_snapshot` (boolean): If true, create a snapshot of this bundle's contents.
* `description` (string): Public description
* `dont_separate_submissions_by_folder` (boolean): Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
* `expires_at` (string): Bundle expiration date/time
* `finalize_snapshot` (boolean): If true, finalize the snapshot of this bundle's contents. Note that `create_snapshot` must also be true.
* `inbox_id` (int64): ID of the associated inbox, if available.
* `max_uses` (int64): Maximum number of times bundle can be accessed
* `note` (string): Bundle internal note
* `path_template` (string): Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, `strftime` directives, and any custom form data.
* `path_template_time_zone` (string): Timezone to use when rendering timestamps in path templates.
* `permissions` (string): Permissions that apply to Folders in this Share Link.
* `require_registration` (boolean): Show a registration page that captures the downloader's name and email address?
* `require_share_recipient` (boolean): Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
* `send_email_receipt_to_uploader` (boolean): Send delivery receipt to the uploader. Note: For writable share only
* `skip_company` (boolean): BundleRegistrations can be saved without providing company?
* `start_access_on_date` (string): Date when share will start to be accessible. If `nil` access granted right after create.
* `skip_email` (boolean): BundleRegistrations can be saved without providing email?
* `skip_name` (boolean): BundleRegistrations can be saved without providing name?
* `watermark_attachment_delete` (boolean): If true, will delete the file stored in watermark_attachment
* `watermark_attachment_file` (file): Preview watermark image applied to all bundle items.


---

## Delete Share Link

```
bundle = files_sdk.bundle.find(id)
bundle.delete()
```

### Parameters

* `id` (int64): Required - Bundle ID.
