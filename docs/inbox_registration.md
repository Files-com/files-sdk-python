# InboxRegistration

## Example InboxRegistration Object

```
{
  "code": "abc123",
  "name": "account",
  "company": "Action Verb",
  "email": "john.doe@files.com",
  "ip": "10.1.1.1",
  "clickwrap_body": "example",
  "form_field_set_id": 1,
  "form_field_data": {
    "key": "example value"
  },
  "inbox_id": 1,
  "inbox_recipient_id": 1,
  "inbox_title": "example",
  "created_at": "2000-01-01T01:00:00Z"
}
```

* `code` (string): Registration cookie code
* `name` (string): Registrant name
* `company` (string): Registrant company name
* `email` (string): Registrant email address
* `ip` (string): Registrant IP Address
* `clickwrap_body` (string): Clickwrap text that was shown to the registrant
* `form_field_set_id` (int64): Id of associated form field set
* `form_field_data` (object): Data for form field set with form field ids as keys and user data as values
* `inbox_id` (int64): Id of associated inbox
* `inbox_recipient_id` (int64): Id of associated inbox recipient
* `inbox_title` (string): Title of associated inbox
* `created_at` (date-time): Registration creation date/time


---

## List Inbox Registrations

```
files_sdk.inbox_registration.list({
  "folder_behavior_id": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `folder_behavior_id` (int64): ID of the associated Inbox. This is required if the user is not a site admin.
