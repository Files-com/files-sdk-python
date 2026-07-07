# CustomDomainForProxy

## Example CustomDomainForProxy Object

```
{
  "id": 1,
  "domain": "example",
  "destination": "example",
  "ssl_certificate_id": 1,
  "certificate": "example",
  "private_key": "example",
  "intermediates": "example"
}
```

* `id` (int64): Custom Domain ID.
* `domain` (string): Customer-owned domain name.
* `destination` (string): Routing destination: `site_alias`, `public_hosting`, or `s3_endpoint`.
* `ssl_certificate_id` (int64): Attached SslCertificate ID.
* `certificate` (string): The text of the certificate itself.
* `private_key` (string): Private key used to generate the certificate.
* `intermediates` (string): Intermediate certificates, if available.
