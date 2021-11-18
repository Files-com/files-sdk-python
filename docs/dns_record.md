# DnsRecord

## Example DnsRecord Object

```
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


---

## Show site DNS configuration

```
files_sdk.dns_record.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
