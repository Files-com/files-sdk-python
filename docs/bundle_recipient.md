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


---

## List Bundle Recipients

```
files_sdk.bundle_recipient.list({
  "user_id": 1,
  "per_page": 1,
  "bundle_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `has_registrations`.
* `filter` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `has_registrations`.
* `filter_gt` (object): If set, return records where the specifiied field is greater than the supplied value. Valid fields are `has_registrations`.
* `filter_gteq` (object): If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `has_registrations`.
* `filter_like` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `has_registrations`.
* `filter_lt` (object): If set, return records where the specifiied field is less than the supplied value. Valid fields are `has_registrations`.
* `filter_lteq` (object): If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `has_registrations`.
* `bundle_id` (int64): Required - List recipients for the bundle with this ID.
