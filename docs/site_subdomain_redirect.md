# SiteSubdomainRedirect

## Example SiteSubdomainRedirect Object

```
{
  "id": 1,
  "subdomain": "old-company",
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Site subdomain redirect ID.
* `subdomain` (string): Files.com subdomain that continues to route to the current site subdomain.
* `created_at` (date-time): When this redirect was created.
* `updated_at` (date-time): When this redirect was last updated.


---

## List Site Subdomain Redirects

```
files_sdk.site_subdomain_redirect.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `id`.


---

## Show Site Subdomain Redirect

```
files_sdk.site_subdomain_redirect.find(id)
```

### Parameters

* `id` (int64): Required - Site Subdomain Redirect ID.


---

## Delete Site Subdomain Redirect

```
files_sdk.site_subdomain_redirect.delete(id)
```

### Parameters

* `id` (int64): Required - Site Subdomain Redirect ID.


---

## Delete Site Subdomain Redirect

```
site_subdomain_redirect = files_sdk.site_subdomain_redirect.find(id)
site_subdomain_redirect.delete()
```

### Parameters

* `id` (int64): Required - Site Subdomain Redirect ID.
