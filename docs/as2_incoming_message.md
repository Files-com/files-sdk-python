# As2IncomingMessage

## Example As2IncomingMessage Object

```
{
  "id": 1,
  "as2_partner_id": 1,
  "as2_station_id": 1,
  "uuid": "",
  "content_type": "",
  "http_headers": "",
  "activity_log": "",
  "processing_result": "",
  "mic": "",
  "mic_algo": "",
  "as2_to": "",
  "as2_from": "",
  "message_id": "",
  "subject": "",
  "date": "",
  "body_size": "",
  "attachment_filename": "",
  "ip": "",
  "created_at": "2000-01-01T01:00:00Z",
  "http_response_code": "",
  "http_response_headers": "",
  "recipient_serial": "",
  "hex_recipient_serial": "A5:EB:C1:95:DC:D8:2B:E7",
  "recipient_issuer": "",
  "message_received": True,
  "message_decrypted": True,
  "message_signature_verified": True,
  "message_processing_success": True,
  "message_mdn_returned": True,
  "encrypted_uri": "",
  "smime_signed_uri": "",
  "smime_uri": "",
  "raw_uri": "",
  "mdn_response_uri": ""
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
* `as2_partner_id` (int64): As2 Partner ID.  If provided, will return message specific to that partner.
