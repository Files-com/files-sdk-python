# PublicInbox

## Example PublicInbox Object

```
{
  "color_left": "#0066a7",
  "color_link": "#d34f5d",
  "color_text": "#0066a7",
  "color_top": "#000000",
  "color_top_text": "#ffffff",
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
  "require_logout": True,
  "logo": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  },
  "logo_click_href": "https://www.example.com",
  "thumbnail": {
    "name": "My logo",
    "uri": "https://mysite.files.com/.../my_image.png"
  }
}
```

* `color_left` (string): Page link and button color
* `color_link` (string): Top bar link color
* `color_text` (string): Page link and button color
* `color_top` (string): Top bar background color
* `color_top_text` (string): Top bar text color
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
* `require_logout` (boolean): If true, we will hide the 'Remember Me' box on the Inbox registration page, requiring that the user logout and log back in every time they visit the page.
* `logo` (Image): Custom logo for Inbox folder
* `logo_click_href` (string): URL to open when a public visitor clicks the custom logo
* `thumbnail` (Image): Custom logo thumbnail for Inbox folder


---

## List Public Inboxes

```
files_sdk.public_inbox.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## Show Public Inbox

```
files_sdk.public_inbox.get_key(key, {
  "recipient_code": "abc123"
})
```

### Parameters

* `key` (string): Required - Unique key for inbox
* `recipient_code` (string): Inbox recipient code


---

## Create an export CSV of Public Inbox resources

```
files_sdk.public_inbox.create_export()
```
