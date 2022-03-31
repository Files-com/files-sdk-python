# As2IncomingMessage

## Example As2IncomingMessage Object

```
{
  "id": 1,
  "as2_partner_id": 1,
  "uuid": "",
  "content_type": "",
  "http_headers": "",
  "activity_log": "",
  "processing_result": "",
  "as2_to": "",
  "as2_from": "",
  "message_id": "",
  "subject": "",
  "body_size": "",
  "attachment_filename": "",
  "created_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Id of the AS2 Partner.
* `as2_partner_id` (int64): Id of the AS2 Partner associated with this message.
* `uuid` (string): UUID assigned to this message.
* `content_type` (string): Content Type header of the incoming message.
* `http_headers` (object): HTTP Headers sent with this message.
* `activity_log` (string): JSON Structure of the activity log.
* `processing_result` (string): Result of processing.
* `as2_to` (string): AS2 TO header of message
* `as2_from` (string): AS2 FROM header of message
* `message_id` (string): AS2 Message Id
* `subject` (string): AS2 Subject Header
* `body_size` (string): Encrypted Payload Body Size
* `attachment_filename` (string): Filename of the file being received.
* `created_at` (date-time): Message creation date/time


---

## List As2 Incoming Messages

```
files_sdk.as2_incoming_message.list({
  "per_page": 1,
  "as2_partner_id": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `as2_partner_id` (int64): As2 Partner ID.  If provided, will return message specific to that partner.
