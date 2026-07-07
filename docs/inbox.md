# Inbox

## Example Inbox Object

```
{
  "title": "example",
  "description": "My inbox",
  "help_text": "If you need any help submitting your application, please call our front desk.",
  "key": "application-form",
  "show_on_login_page": True,
  "has_password": True,
  "require_registration": True,
  "dont_allow_folders_in_uploads": True,
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
  "notify_senders_on_successful_uploads_via_email": True,
  "notify_senders_on_successful_uploads_via_web": True,
  "allow_whitelisting": True,
  "whitelist": [
    "example"
  ],
  "disable_web_upload": True,
  "inbound_email_address": "example"
}
```

* `title` (string): Inbox title
* `description` (string): User description
* `help_text` (string): Text that will be shown to the users on the Inbox.  Use this field to provide custom instructions.
* `key` (string): Unique key for inbox
* `show_on_login_page` (boolean): Show this inbox on site login page?
* `has_password` (boolean): Is this inbox password protected?
* `require_registration` (boolean): Does this inbox require registration?
* `dont_allow_folders_in_uploads` (boolean): Should folder uploads be prevented?
* `clickwrap_body` (string): Legal text that must be agreed to prior to accessing Inbox.
* `form_field_set` (FormFieldSet): Custom Form to use
* `notify_senders_on_successful_uploads_via_email` (boolean): Notify senders on successful uploads via email
* `notify_senders_on_successful_uploads_via_web` (boolean): Notify senders on successful uploads via web
* `allow_whitelisting` (boolean): allow/disallow whitelist
* `whitelist` (array(string)): A list of emails and domain names for whitelisting
* `disable_web_upload` (boolean): This will disable the upload URL and can only be done if uploads via email are enabled
* `inbound_email_address` (string): inbound email address to the inbox


---

## List Inboxes

```
files_sdk.inbox.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `allow_whitelisting`.


---

## Create an export CSV of Inbox resources

```
files_sdk.inbox.create_export()
```

### Parameters

* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `allow_whitelisting`.
