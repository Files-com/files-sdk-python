# HolidayRegion

## Example HolidayRegion Object

```
{
  "code": "us_dc",
  "name": "United States - District of Columbia"
}
```

* `code` (string): The code representing a region
* `name` (string): The name of the region


---

## List all possible holiday regions

```
files_sdk.holiday_region.get_supported()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
