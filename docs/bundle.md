# Bundle

## Example Bundle Object

```
{
  "code": "abc123",
  "url": "https://subdomain.files.com/f/12345678",
  "description": "The public description of the bundle.",
  "password_protected": True,
  "permissions": "read",
  "preview_only": True,
  "require_registration": True,
  "require_share_recipient": True,
  "clickwrap_body": "[Legal text]",
  "form_field_set": "",
  "skip_name": True,
  "skip_email": True,
  "skip_company": True,
  "id": 1,
  "created_at": "2000-01-01T01:00:00Z",
  "dont_separate_submissions_by_folder": True,
  "expires_at": "2000-01-01T01:00:00Z",
  "max_uses": 1,
  "note": "The internal note on the bundle.",
  "path_template": "{{name}}_{{ip}}",
  "user_id": 1,
  "username": "user",
  "clickwrap_id": 1,
  "inbox_id": 1,
  "watermark_attachment": "",
  "watermark_value": {
    "key": "example value"
  },
  "has_inbox": True,
  "paths": [
    "file.txt"
  ]
}
```

* `code` (string): Bundle code.  This code forms the end part of the Public URL.
* `url` (string): Public URL of Share Link
* `description` (string): Public description
* `password_protected` (boolean): Is this bundle password protected?
* `permissions` (string): Permissions that apply to Folders in this Share Link.
* `preview_only` (boolean): Restrict users to previewing files only?
* `require_registration` (boolean): Show a registration page that captures the downloader's name and email address?
* `require_share_recipient` (boolean): Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
* `clickwrap_body` (string): Legal text that must be agreed to prior to accessing Bundle.
* `form_field_set` (FormFieldSet): Custom Form to use
* `skip_name` (boolean): BundleRegistrations can be saved without providing name?
* `skip_email` (boolean): BundleRegistrations can be saved without providing email?
* `skip_company` (boolean): BundleRegistrations can be saved without providing company?
* `id` (int64): Bundle ID
* `created_at` (date-time): Bundle created at date/time
* `dont_separate_submissions_by_folder` (boolean): Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
* `expires_at` (date-time): Bundle expiration date/time
* `max_uses` (int64): Maximum number of times bundle can be accessed
* `note` (string): Bundle internal note
* `path_template` (string): Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, and any custom form data.
* `user_id` (int64): Bundle creator user ID
* `username` (string): Bundle creator username
* `clickwrap_id` (int64): ID of the clickwrap to use with this bundle.
* `inbox_id` (int64): ID of the associated inbox, if available.
* `watermark_attachment` (Image): Preview watermark image applied to all bundle items.
* `watermark_value` (object): Preview watermark settings applied to all bundle items. Uses the same keys as Behavior.value
* `has_inbox` (boolean): Does this bundle have an associated inbox?
* `paths` (array): A list of paths in this bundle
* `password` (string): Password for this bundle.
* `form_field_set_id` (int64): Id of Form Field Set to use with this bundle
* `watermark_attachment_file` (file): Preview watermark image applied to all bundle items.
* `watermark_attachment_delete` (boolean): If true, will delete the file stored in watermark_attachment


---

## List Bundles

```
files_sdk.bundle.list({
  "user_id": 1,
  "per_page": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `created_at` and `code`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal to the supplied value. Valid fields are `created_at`.
* `filter_like` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal to the supplied value. Valid fields are `created_at`.


---

## Show Bundle

```
files_sdk.bundle.find(id)
```

### Parameters

* `id` (int64): Required - Bundle ID.


---

## Create Bundle

```
files_sdk.bundle.create({
  "user_id": 1,
  "paths": ["file.txt"],
  "password": "Password",
  "form_field_set_id": 1,
  "dont_separate_submissions_by_folder": True,
  "expires_at": "2000-01-01T01:00:00Z",
  "max_uses": 1,
  "description": "The public description of the bundle.",
  "note": "The internal note on the bundle.",
  "code": "abc123",
  "path_template": "{{name}}_{{ip}}",
  "permissions": "read",
  "preview_only": True,
  "require_registration": True,
  "clickwrap_id": 1,
  "inbox_id": 1,
  "require_share_recipient": True,
  "skip_email": True,
  "skip_name": True,
  "skip_company": True
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `paths` (array(string)): Required - A list of paths to include in this bundle.
* `password` (string): Password for this bundle.
* `form_field_set_id` (int64): Id of Form Field Set to use with this bundle
* `dont_separate_submissions_by_folder` (boolean): Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
* `expires_at` (string): Bundle expiration date/time
* `max_uses` (int64): Maximum number of times bundle can be accessed
* `description` (string): Public description
* `note` (string): Bundle internal note
* `code` (string): Bundle code.  This code forms the end part of the Public URL.
* `path_template` (string): Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, and any custom form data.
* `permissions` (string): Permissions that apply to Folders in this Share Link.
* `preview_only` (boolean): Restrict users to previewing files only?
* `require_registration` (boolean): Show a registration page that captures the downloader's name and email address?
* `clickwrap_id` (int64): ID of the clickwrap to use with this bundle.
* `inbox_id` (int64): ID of the associated inbox, if available.
* `require_share_recipient` (boolean): Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
* `skip_email` (boolean): BundleRegistrations can be saved without providing email?
* `skip_name` (boolean): BundleRegistrations can be saved without providing name?
* `skip_company` (boolean): BundleRegistrations can be saved without providing company?
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

## Update Bundle

```
files_sdk.bundle.update(id, {
  "paths": ["file.txt"],
  "password": "Password",
  "form_field_set_id": 1,
  "clickwrap_id": 1,
  "code": "abc123",
  "description": "The public description of the bundle.",
  "dont_separate_submissions_by_folder": True,
  "expires_at": "2000-01-01T01:00:00Z",
  "inbox_id": 1,
  "max_uses": 1,
  "note": "The internal note on the bundle.",
  "path_template": "{{name}}_{{ip}}",
  "permissions": "read",
  "preview_only": True,
  "require_registration": True,
  "require_share_recipient": True,
  "skip_email": True,
  "skip_name": True,
  "skip_company": True,
  "watermark_attachment_delete": True
})
```

### Parameters

* `id` (int64): Required - Bundle ID.
* `paths` (array(string)): A list of paths to include in this bundle.
* `password` (string): Password for this bundle.
* `form_field_set_id` (int64): Id of Form Field Set to use with this bundle
* `clickwrap_id` (int64): ID of the clickwrap to use with this bundle.
* `code` (string): Bundle code.  This code forms the end part of the Public URL.
* `description` (string): Public description
* `dont_separate_submissions_by_folder` (boolean): Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
* `expires_at` (string): Bundle expiration date/time
* `inbox_id` (int64): ID of the associated inbox, if available.
* `max_uses` (int64): Maximum number of times bundle can be accessed
* `note` (string): Bundle internal note
* `path_template` (string): Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, and any custom form data.
* `permissions` (string): Permissions that apply to Folders in this Share Link.
* `preview_only` (boolean): Restrict users to previewing files only?
* `require_registration` (boolean): Show a registration page that captures the downloader's name and email address?
* `require_share_recipient` (boolean): Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
* `skip_email` (boolean): BundleRegistrations can be saved without providing email?
* `skip_name` (boolean): BundleRegistrations can be saved without providing name?
* `skip_company` (boolean): BundleRegistrations can be saved without providing company?
* `watermark_attachment_delete` (boolean): If true, will delete the file stored in watermark_attachment
* `watermark_attachment_file` (file): Preview watermark image applied to all bundle items.


---

## Delete Bundle

```
files_sdk.bundle.delete(id)
```

### Parameters

* `id` (int64): Required - Bundle ID.


---

## Send email(s) with a link to bundle

```
bundle = files_sdk.bundle.list.first
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

## Update Bundle

```
bundle = files_sdk.bundle.list.first
bundle.update({
  "paths": ["file.txt"],
  "password": "Password",
  "form_field_set_id": 1,
  "clickwrap_id": 1,
  "code": "abc123",
  "description": "The public description of the bundle.",
  "dont_separate_submissions_by_folder": True,
  "expires_at": "2000-01-01T01:00:00Z",
  "inbox_id": 1,
  "max_uses": 1,
  "note": "The internal note on the bundle.",
  "path_template": "{{name}}_{{ip}}",
  "permissions": "read",
  "preview_only": True,
  "require_registration": True,
  "require_share_recipient": True,
  "skip_email": True,
  "skip_name": True,
  "skip_company": True,
  "watermark_attachment_delete": True
})
```

### Parameters

* `id` (int64): Required - Bundle ID.
* `paths` (array(string)): A list of paths to include in this bundle.
* `password` (string): Password for this bundle.
* `form_field_set_id` (int64): Id of Form Field Set to use with this bundle
* `clickwrap_id` (int64): ID of the clickwrap to use with this bundle.
* `code` (string): Bundle code.  This code forms the end part of the Public URL.
* `description` (string): Public description
* `dont_separate_submissions_by_folder` (boolean): Do not create subfolders for files uploaded to this share. Note: there are subtle security pitfalls with allowing anonymous uploads from multiple users to live in the same folder. We strongly discourage use of this option unless absolutely required.
* `expires_at` (string): Bundle expiration date/time
* `inbox_id` (int64): ID of the associated inbox, if available.
* `max_uses` (int64): Maximum number of times bundle can be accessed
* `note` (string): Bundle internal note
* `path_template` (string): Template for creating submission subfolders. Can use the uploader's name, email address, ip, company, and any custom form data.
* `permissions` (string): Permissions that apply to Folders in this Share Link.
* `preview_only` (boolean): Restrict users to previewing files only?
* `require_registration` (boolean): Show a registration page that captures the downloader's name and email address?
* `require_share_recipient` (boolean): Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
* `skip_email` (boolean): BundleRegistrations can be saved without providing email?
* `skip_name` (boolean): BundleRegistrations can be saved without providing name?
* `skip_company` (boolean): BundleRegistrations can be saved without providing company?
* `watermark_attachment_delete` (boolean): If true, will delete the file stored in watermark_attachment
* `watermark_attachment_file` (file): Preview watermark image applied to all bundle items.


---

## Delete Bundle

```
bundle = files_sdk.bundle.list.first
bundle.delete()
```

### Parameters

* `id` (int64): Required - Bundle ID.
