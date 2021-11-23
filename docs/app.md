# App

## Example App Object

```
{
  "name": "",
  "extended_description": "",
  "short_description": "",
  "documentation_links": "Important Info => http://files.test/learn-more",
  "icon_url": "",
  "logo_url": "",
  "screenshot_list_urls": [
    ""
  ],
  "logo_thumbnail_url": "",
  "sso_strategy_type": "",
  "remote_server_type": "",
  "folder_behavior_type": "",
  "external_homepage_url": "",
  "marketing_youtube_url": "",
  "tutorial_youtube_url": "",
  "app_type": "",
  "featured": True
}
```

* `name` (string): Name of the App
* `extended_description` (string): Long form description of the App
* `short_description` (string): Short description of the App
* `documentation_links` (object): Collection of named links to documentation
* `icon_url` (string): App icon
* `logo_url` (string): Full size logo for the App
* `screenshot_list_urls` (string): Screenshots of the App
* `logo_thumbnail_url` (string): Logo thumbnail for the App
* `sso_strategy_type` (string): Associated SSO Strategy type, if any
* `remote_server_type` (string): Associated Remote Server type, if any
* `folder_behavior_type` (string): Associated Folder Behavior type, if any
* `external_homepage_url` (string): Link to external homepage
* `marketing_youtube_url` (string): Marketing video page
* `tutorial_youtube_url` (string): Tutorial video page
* `app_type` (string): The type of the App
* `featured` (boolean): Is featured on the App listing?


---

## List Apps

```
files_sdk.app.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `name` and `app_type`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `name` and `app_type`. Valid field combinations are `[ name, app_type ]` and `[ app_type, name ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `name` and `app_type`. Valid field combinations are `[ name, app_type ]` and `[ app_type, name ]`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal to the supplied value. Valid fields are `name` and `app_type`. Valid field combinations are `[ name, app_type ]` and `[ app_type, name ]`.
* `filter_like` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `name` and `app_type`. Valid field combinations are `[ name, app_type ]` and `[ app_type, name ]`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `name` and `app_type`. Valid field combinations are `[ name, app_type ]` and `[ app_type, name ]`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal to the supplied value. Valid fields are `name` and `app_type`. Valid field combinations are `[ name, app_type ]` and `[ app_type, name ]`.
