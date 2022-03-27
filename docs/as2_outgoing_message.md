# As2OutgoingMessage

## Example As2OutgoingMessage Object

```
{
  "id": 1,
  "as2_partner_id": 1,
  "uuid": "",
  "http_headers": "",
  "activity_log": "",
  "processing_result": "",
  "mic": "",
  "message_id": "",
  "body_size": "",
  "attachment_filename": "",
  "created_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Id of the AS2 Partner.
* `as2_partner_id` (int64): Id of the AS2 Partner associated with this message.
* `uuid` (string): UUID assigned to this message.
* `http_headers` (object): HTTP Headers sent with this message.
* `activity_log` (string): JSON Structure of the activity log.
* `processing_result` (string): Result of processing. Valid values: `send_failed`, `send_success`, `send_no_mdn`
* `mic` (string): AS2 Message Integrity Check
* `message_id` (string): AS2 Message Id
* `body_size` (string): Encrypted Payload Body Size
* `attachment_filename` (string): Filename of the file being sent.
* `created_at` (date-time): Message creation date/time


---

## List As2 Outgoing Messages

```
files_sdk.as2_outgoing_message.list({
  "per_page": 1,
  "as2_partner_id": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `as2_partner_id` (int64): As2 Partner ID.  If provided, will return message specific to that partner.
