# BundleRecipient

## Example BundleRecipient Object

```
{
  "company": "Acme Inc.",
  "name": "John Doe",
  "note": "Some note.",
  "recipient": "john.doe@example.com",
  "sent_at": "2000-01-01T01:00:00Z"
}
```

* `company` (string): The recipient's company.
* `name` (string): The recipient's name.
* `note` (string): A note sent to the recipient with the bundle.
* `recipient` (string): The recipient's email address.
* `sent_at` (date-time): When the Bundle was shared with this recipient.
* `bundle_id` (int64): Bundle to share.
* `share_after_create` (boolean): Set to true to share the link with the recipient upon creation.


---

## List Bundle Recipients

```
files_sdk.bundle_recipient.list({
  "bundle_id": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `has_registrations`.
* `bundle_id` (int64): Required - List recipients for the bundle with this ID.


---

## Create Bundle Recipient

```
files_sdk.bundle_recipient.create({
  "bundle_id": 1,
  "recipient": "johndoe@gmail.com",
  "name": "John Smith",
  "company": "Acme Ltd",
  "note": "Just a note.",
  "share_after_create": True
})
```

### Parameters

* `bundle_id` (int64): Required - Bundle to share.
* `recipient` (string): Required - Email addresses to share this bundle with.
* `name` (string): Name of recipient.
* `company` (string): Company of recipient.
* `note` (string): Note to include in email.
* `share_after_create` (boolean): Set to true to share the link with the recipient upon creation.


---

## Create an export CSV of Bundle Recipient resources

```
files_sdk.bundle_recipient.create_export({
  "bundle_id": 1
})
```

### Parameters

* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `has_registrations`.
* `bundle_id` (int64): Required - List recipients for the bundle with this ID.
