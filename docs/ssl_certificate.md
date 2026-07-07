# SslCertificate

## Example SslCertificate Object

```
{
  "name": "example",
  "certificate": "example",
  "private_key": "example",
  "key": null,
  "intermediates": "example",
  "id": 1,
  "domain_hsts_header": True,
  "ftps_enabled": True,
  "https_enabled": True,
  "sftp_insecure_ciphers": True,
  "tls_disabled": True,
  "subdomain": "example",
  "domains": [
    "example"
  ]
}
```

* `name` (string): The name of the site associated with this SSL certificate.
* `certificate` (string): The text of the certificate itself.
* `private_key` (string): Private key used to generate the certificate.
* `key` (object): Private key encrypted with our secret key.
* `intermediates` (string): Intermediate certificates, if available.
* `id` (int64): ID of the site associated with this certificate, including group id if available.
* `domain_hsts_header` (boolean): True if a HSTS header should be rendered for the site
* `ftps_enabled` (boolean): Whether or not this certificate can be used for FTPS.
* `https_enabled` (boolean): Whether or not this certificate can be used for HTTPS. Always true.
* `sftp_insecure_ciphers` (boolean): True if the site associated with this certificate has the "Allow Insecure SFTP Ciphers" feature turned on.
* `tls_disabled` (boolean): True if the site associated with this certificate has the "Security Opt Out" feature turned on.
* `subdomain` (string): Site subdomain.
* `domains` (array(string)): Domains associated with this certificate.
