# DnsRecord

## Example DnsRecord Object

```
{
  "id": "example",
  "domain": "my-custom-domain.com",
  "rrtype": "CNAME",
  "value": "mysite.files.com"
}
```

* `id` (string): Unique label for DNS record; used by Zapier and other integrations.
* `domain` (string): DNS record domain name
* `rrtype` (string): DNS record type
* `value` (string): DNS record value


---

## Show site DNS configuration

```
files_sdk.dns_record.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
