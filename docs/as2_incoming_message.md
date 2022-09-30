# As2IncomingMessage

## Example As2IncomingMessage Object

```
{
  "id": 1,
  "as2_partner_id": 1,
  "as2_station_id": 1,
  "uuid": "example",
  "content_type": "example",
  "http_headers": {
    "key": "example value"
  },
  "activity_log": "example",
  "processing_result": "example",
  "processing_result_description": "example",
  "mic": "example",
  "mic_algo": "example",
  "as2_to": "example",
  "as2_from": "example",
  "message_id": "example",
  "subject": "example",
  "date": "example",
  "body_size": "example",
  "attachment_filename": "example",
  "ip": "example",
  "created_at": "2000-01-01T01:00:00Z",
  "http_response_code": "example",
  "http_response_headers": {
    "key": "example value"
  },
  "recipient_serial": "example",
  "hex_recipient_serial": "A5:EB:C1:95:DC:D8:2B:E7",
  "recipient_issuer": "example",
  "message_received": True,
  "message_decrypted": True,
  "message_signature_verified": True,
  "message_processing_success": True,
  "message_mdn_returned": True,
  "encrypted_uri": "example",
  "smime_signed_uri": "example",
  "smime_uri": "example",
  "raw_uri": "example",
  "mdn_response_uri": "example"
}
```

* `id` (int64): Id of the AS2 Partner.
* `as2_partner_id` (int64): Id of the AS2 Partner associated with this message.
* `as2_station_id` (int64): Id of the AS2 Station associated with this message.
* `uuid` (string): UUID assigned to this message.
* `content_type` (string): Content Type header of the incoming message.
* `http_headers` (object): HTTP Headers sent with this message.
* `activity_log` (string): JSON Structure of the activity log.
* `processing_result` (string): Result of processing.
* `processing_result_description` (string): Result of processing description.
* `mic` (string): AS2 Message Integrity Check
* `mic_algo` (string): AS2 Message Integrity Check Algorithm Used
* `as2_to` (string): AS2 TO header of message
* `as2_from` (string): AS2 FROM header of message
* `message_id` (string): AS2 Message Id
* `subject` (string): AS2 Subject Header
* `date` (string): Date Header
* `body_size` (string): Encrypted Payload Body Size
* `attachment_filename` (string): Filename of the file being received.
* `ip` (string): IP Address of the Sender
* `created_at` (date-time): Message creation date/time
* `http_response_code` (string): HTTP Response Code sent for this message
* `http_response_headers` (object): HTTP Headers sent for this message.
* `recipient_serial` (string): Incoming Message Recipient(the Client Cert used to encrypt this message)'s serial
* `hex_recipient_serial` (string): Incoming Message Recipient(the Client Cert used to encrypt this message)'s serial in hex format.
* `recipient_issuer` (string): Incoming Message Recipient(the Client Cert used to encrypt this message)'s issuer
* `message_received` (boolean): Message body received?
* `message_decrypted` (boolean): Message decrypted successfully?
* `message_signature_verified` (boolean): Message signature verified?
* `message_processing_success` (boolean): Message processed successfully?
* `message_mdn_returned` (boolean): MDN returned?
* `encrypted_uri` (string): URL to download the encrypted signed smime that is to sent as AS2 body
* `smime_signed_uri` (string): URL to download the file contents as smime with signature
* `smime_uri` (string): URL to download the file contents encoded as smime
* `raw_uri` (string): URL to download the original file contents
* `mdn_response_uri` (string): URL to download the http response body


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
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `created_at` and `as2_partner_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal to the supplied value. Valid fields are `created_at`.
* `filter_like` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal to the supplied value. Valid fields are `created_at`.
* `as2_partner_id` (int64): As2 Partner ID.  If provided, will return message specific to that partner.
