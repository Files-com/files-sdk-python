# As2OutgoingMessage

## Example As2OutgoingMessage Object

```
{
  "id": 1,
  "as2_partner_id": 1,
  "as2_station_id": 1,
  "uuid": "",
  "http_headers": "",
  "activity_log": "",
  "processing_result": "",
  "mic": "",
  "mic_sha_256": "",
  "as2_to": "",
  "as2_from": "",
  "date": "",
  "message_id": "",
  "body_size": "",
  "attachment_filename": "",
  "created_at": "2000-01-01T01:00:00Z",
  "http_response_code": "",
  "http_response_headers": "",
  "mdn_received": True,
  "mdn_valid": True,
  "mdn_signature_verified": True,
  "mdn_message_id_matched": True,
  "mdn_mic_matched": True,
  "mdn_processing_success": True,
  "raw_uri": "",
  "smime_uri": "",
  "smime_signed_uri": "",
  "encrypted_uri": "",
  "mdn_response_uri": ""
}
```

* `id` (int64): Id of the AS2 Partner.
* `as2_partner_id` (int64): Id of the AS2 Partner associated with this message.
* `as2_station_id` (int64): Id of the AS2 Station associated with this message.
* `uuid` (string): UUID assigned to this message.
* `http_headers` (object): HTTP Headers sent with this message.
* `activity_log` (string): JSON Structure of the activity log.
* `processing_result` (string): Result of processing.
* `mic` (string): AS2 Message Integrity Check SHA1
* `mic_sha_256` (string): AS2 Message Integrity Check SHA256
* `as2_to` (string): AS2 TO
* `as2_from` (string): AS2 FROM
* `date` (string): Date Header
* `message_id` (string): AS2 Message Id
* `body_size` (string): Encrypted Payload Body Size
* `attachment_filename` (string): Filename of the file being sent.
* `created_at` (date-time): Message creation date/time
* `http_response_code` (string): HTTP Response Code received for this message
* `http_response_headers` (object): HTTP Headers received for this message.
* `mdn_received` (boolean): Did the partner give a response body?
* `mdn_valid` (boolean): Is the response in MDN format?
* `mdn_signature_verified` (boolean): MDN signature verified?
* `mdn_message_id_matched` (boolean): MDN message id matched?
* `mdn_mic_matched` (boolean): MDN MIC matched?
* `mdn_processing_success` (boolean): MDN disposition indicate a successful processing?
* `raw_uri` (string): URL to download the original file contents
* `smime_uri` (string): URL to download the file contents encoded as smime
* `smime_signed_uri` (string): URL to download the file contents as smime with signature
* `encrypted_uri` (string): URL to download the encrypted signed smime that is to sent as AS2 body
* `mdn_response_uri` (string): URL to download the http response body


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
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `created_at` and `as2_partner_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal to the supplied value. Valid fields are `created_at`.
* `filter_like` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal to the supplied value. Valid fields are `created_at`.
* `as2_partner_id` (int64): As2 Partner ID.  If provided, will return message specific to that partner.
