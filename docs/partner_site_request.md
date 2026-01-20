# PartnerSiteRequest

## Example PartnerSiteRequest Object

```
{
  "id": 1,
  "partner_id": 1,
  "linked_site_id": 1,
  "status": "pending",
  "pairing_key": "abc123xyz",
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Partner Site Request ID
* `partner_id` (int64): Partner ID
* `linked_site_id` (int64): Linked Site ID
* `status` (string): Request status (pending, approved, rejected)
* `pairing_key` (string): Pairing key used to approve this request on the target site
* `created_at` (date-time): Request creation date/time
* `updated_at` (date-time): Request last updated date/time
* `site_url` (string): Site URL to link to


---

## List Partner Site Requests

```
files_sdk.partner_site_request.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


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
  "partner_id": 1,
  "site_url": "site_url"
})
```

### Parameters

* `partner_id` (int64): Required - Partner ID to link with
* `site_url` (string): Required - Site URL to link to


---

## Reject partner site request

```
files_sdk.partner_site_request.reject(id)
```

### Parameters

* `id` (int64): Required - Partner Site Request ID.


---

## Approve partner site request

```
files_sdk.partner_site_request.approve(id)
```

### Parameters

* `id` (int64): Required - Partner Site Request ID.


---

## Delete Partner Site Request

```
files_sdk.partner_site_request.delete(id)
```

### Parameters

* `id` (int64): Required - Partner Site Request ID.


---

## Reject partner site request

```
partner_site_request = files_sdk.partner_site_request.list.first
partner_site_request.reject()
```

### Parameters

* `id` (int64): Required - Partner Site Request ID.


---

## Approve partner site request

```
partner_site_request = files_sdk.partner_site_request.list.first
partner_site_request.approve()
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
