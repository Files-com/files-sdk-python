# SettingsChange

## Example SettingsChange Object

```
{
  "change_details": "{ domain: [\"olddomain.com', \"newdomain.com\"] }",
  "created_at": "2000-01-01T01:00:00Z",
  "user_id": 1
}
```

* `change_details` (object): Specifics on what changed.
* `created_at` (date-time): The time this change was made
* `user_id` (int64): The user id responsible for this change


---

## List Settings Changes

```
files_sdk.settings_change.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `api_key_id`, `created_at` or `user_id`.
* `filter` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `api_key_id` and `user_id`.
* `filter_gt` (object): If set, return records where the specifiied field is greater than the supplied value. Valid fields are `api_key_id` and `user_id`.
* `filter_gteq` (object): If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `api_key_id` and `user_id`.
* `filter_like` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `api_key_id` and `user_id`.
* `filter_lt` (object): If set, return records where the specifiied field is less than the supplied value. Valid fields are `api_key_id` and `user_id`.
* `filter_lteq` (object): If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `api_key_id` and `user_id`.
