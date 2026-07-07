# Preview

## Example Preview Object

```
{
  "id": 1,
  "status": "complete",
  "download_uri": "https://mysite.files.com/...",
  "type": "image",
  "size": "large"
}
```

* `id` (int64): Preview ID
* `status` (string): Preview status.  Can be invalid, not_generated, generating, complete, or file_too_large
* `download_uri` (string): Link to download preview
* `type` (string): Preview type. Can be image, pdf, pdf_native, video, audio, or text
* `size` (string): Preview size


---

## Show many previews at once

```
files_sdk.preview.list({
  "ids": "ids",
  "bundle_registration_code": "abc123",
  "size": "large"
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `ids` (string): Required - Preview IDs.  Comma delimited.
* `bundle_registration_code` (string): Bundle registration cookie code
* `size` (string): Preview Size


---

## Show Preview

```
files_sdk.preview.find(id, {
  "bundle_registration_code": "abc123",
  "size": "large"
})
```

### Parameters

* `id` (int64): Required - Preview ID
* `bundle_registration_code` (string): Bundle registration cookie code
* `size` (string): Preview Size


---

## Show many previews at once

```
files_sdk.preview.create_export({
  "ids": "ids",
  "bundle_registration_code": "abc123"
})
```

### Parameters

* `ids` (string): Required - Preview IDs.  Comma delimited.
* `bundle_registration_code` (string): Bundle registration cookie code
* `size` (string): Preview Size
