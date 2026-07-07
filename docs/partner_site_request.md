# PartnerSiteRequest

## Example PartnerSiteRequest Object

```
{
  "id": 1,
  "host_partner_id": 1,
  "guest_site_url": "https://example.files.com",
  "status": "pending",
  "host_site_name": "Acme Site",
  "pairing_key": "abc123xyz",
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Partner Site Request ID
* `host_partner_id` (int64): Host Partner ID
* `guest_site_url` (string): Guest Site URL
* `status` (string): Request status (pending, approved, rejected)
* `host_site_name` (string): Host Site Name
* `pairing_key` (string): Pairing key used to approve this request on the Guest Site
* `created_at` (date-time): Request creation date/time
* `updated_at` (date-time): Request last updated date/time


---

## List Partner Site Requests

```
files_sdk.partner_site_request.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `host_partner_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `host_partner_id`.


---

## Find partner site request by pairing key

```
files_sdk.partner_site_request.find_by_pairing_key({
  "pairing_key": "pairing_key"
})
```

### Parameters

* `pairing_key` (string): Required - Pairing key for the partner site request


---

## Create Partner Site Request

```
files_sdk.partner_site_request.create({
  "host_partner_id": 1,
  "guest_site_url": "guest_site_url"
})
```

### Parameters

* `host_partner_id` (int64): Required - Host Partner ID to link with
* `guest_site_url` (string): Required - Guest Site URL to link to


---

## Reject partner site request

```
files_sdk.partner_site_request.reject({
  "pairing_key": "pairing_key"
})
```

### Parameters

* `pairing_key` (string): Required - Pairing key for the partner site request


---

## Approve partner site request

```
files_sdk.partner_site_request.approve({
  "pairing_key": "pairing_key"
})
```

### Parameters

* `pairing_key` (string): Required - Pairing key for the partner site request


---

## Create an export CSV of Partner Site Request resources

```
files_sdk.partner_site_request.create_export()
```

### Parameters

* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `host_partner_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `host_partner_id`.


---

## Delete Partner Site Request

```
files_sdk.partner_site_request.delete(id)
```

### Parameters

* `id` (int64): Required - Partner Site Request ID.


---

## Delete Partner Site Request

```
partner_site_request = files_sdk.partner_site_request.list.first
partner_site_request.delete()
```

### Parameters

* `id` (int64): Required - Partner Site Request ID.
