# HolidayRegion

## Example HolidayRegion Object

The API sends each `HolidayRegion` record as JSON, such as:

```json
{
  "code": "us_dc",
  "name": "United States - District of Columbia"
}
```

* `code` (string): The code representing a region
* `name` (string): The name of the region

The functions below use the module's settings. Each is also a method of a client's
`client.holiday_region` resource, such as
`client.holiday_region.get_supported(...)`,
which uses that client's configuration instead.


---

## List all possible holiday regions

```python
files_sdk.holiday_region.get_supported()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
