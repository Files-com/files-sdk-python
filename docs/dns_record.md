# DnsRecord

## Example DnsRecord Object

The API sends each `DnsRecord` record as JSON, such as:

```json
{
  "id": "customdomain.com-CNAME-site.files.com",
  "domain": "my-custom-domain.com",
  "rrtype": "CNAME",
  "value": "mysite.files.com"
}
```

* `id` (string): Unique label for DNS record; used by Zapier and other integrations.
* `domain` (string): DNS record domain name
* `rrtype` (string): DNS record type
* `value` (string): DNS record value

The functions below use the module's settings. Each is also a method of a client's
`client.dns_record` resource, such as
`client.dns_record.list(...)`,
which uses that client's configuration instead.


---

## Show Site DNS Configuration

```python
files_sdk.dns_record.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
