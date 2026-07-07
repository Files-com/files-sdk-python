# Announcement

## Example Announcement Object

```
{
  "id": 1,
  "headline": "Files.com Now Supports In-App Announcements!",
  "body": "This is the body.",
  "button_text": "View Blog Post",
  "button_url": "https://www.files.com/blog/",
  "html_body": "<p>This is the HTML version of the body.</p>",
  "label": "New Feature",
  "label_color": "#000000",
  "publish_at": "2000-01-01T01:00:00Z",
  "slug": "new-feature"
}
```

* `id` (int64): Announcement Id
* `headline` (string): Announcement headline
* `body` (string): Announcement body
* `button_text` (string): Text to go on the CTA button
* `button_url` (string): URL to link to when CTA button is clicked
* `html_body` (string): Body converted to HTML
* `label` (string): Text for a label that can be added to the announcement
* `label_color` (string): Color for label on announcement
* `publish_at` (date-time): When was this announcement published?
* `slug` (string): URL slug for announcement


---

## List in-app announcements that are shown in the header of the UI

```
files_sdk.announcement.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .


---

## List in-app announcements that are shown in the header of the UI

```
files_sdk.announcement.create_export()
```

### Parameters

* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
