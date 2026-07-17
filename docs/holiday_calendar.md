# HolidayCalendar

## Example HolidayCalendar Object

```
{
  "id": 1,
  "name": "Company Holidays",
  "definition": "example",
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Holiday Calendar ID. Use `custom_<id>` as a scheduled resource's `holiday_region`.
* `name` (string): Holiday Calendar name.
* `definition` (object): Holiday rules for the calendar. For more information, refer to the Holiday Calendars section of the Files.com documentation.
* `created_at` (date-time): Creation time.
* `updated_at` (date-time): Last update time.


---

## List Holiday Calendars

```
files_sdk.holiday_calendar.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .


---

## Show Holiday Calendar

```
files_sdk.holiday_calendar.find(id)
```

### Parameters

* `id` (int64): Required - Holiday Calendar ID.


---

## Create Holiday Calendar

```
files_sdk.holiday_calendar.create({
  "name": "Company Holidays"
})
```

### Parameters

* `name` (string): Required - Holiday Calendar name.


---

## Update Holiday Calendar

```
files_sdk.holiday_calendar.update(id, {
  "name": "Company Holidays"
})
```

### Parameters

* `id` (int64): Required - Holiday Calendar ID.
* `name` (string): Holiday Calendar name.


---

## Delete Holiday Calendar

```
files_sdk.holiday_calendar.delete(id)
```

### Parameters

* `id` (int64): Required - Holiday Calendar ID.


---

## Update Holiday Calendar

```
holiday_calendar = files_sdk.holiday_calendar.find(id)
holiday_calendar.update({
  "name": "Company Holidays"
})
```

### Parameters

* `id` (int64): Required - Holiday Calendar ID.
* `name` (string): Holiday Calendar name.


---

## Delete Holiday Calendar

```
holiday_calendar = files_sdk.holiday_calendar.find(id)
holiday_calendar.delete()
```

### Parameters

* `id` (int64): Required - Holiday Calendar ID.
