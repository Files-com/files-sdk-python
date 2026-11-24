# PartnerChannelUploadForm

## Example PartnerChannelUploadForm Object

The API sends each `PartnerChannelUploadForm` record as JSON, such as:

```json
{
  "path": "reports/monthly",
  "form_field_set_id": 1
}
```

* `path` (string): Upload destination path relative to the From Partner folder. Must be a configured leaf managed folder path, or an empty string for the From Partner folder when no managed folders are configured. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `form_field_set_id` (int64): ID of the Form Field Set answered for uploads to this destination. Must be in the same Workspace and contain at least one custom field.
