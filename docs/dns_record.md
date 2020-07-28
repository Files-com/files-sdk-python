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
  "page": 1,
  "per_page": 1
})
```

### Parameters

* `page` (int64): Current page number.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
