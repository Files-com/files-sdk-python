# Certificate

## Example Certificate Object

```
{
  "id": 1,
  "name": "My Certificate",
  "certificate": "[certificate]",
  "created_at": "2000-01-01T01:00:00Z",
  "display_status": "Available",
  "domains": [

  ],
  "expires_at": "2000-01-01T01:00:00Z",
  "brick_managed": True,
  "intermediates": "[certificates]",
  "ip_addresses": [

  ],
  "issuer": "example",
  "key_type": "RSA-4096",
  "request": "[CSR]",
  "status": "Available",
  "subject": "my-custom-domain.com"
}
```

* `id` (int64): Certificate ID
* `name` (string): Descriptive name of certificate
* `certificate` (string): Full text of SSL certificate
* `created_at` (date-time): Certificate created at
* `display_status` (string): Certificate status. (One of `Request Generated`, `New`, `Active`, `Active/Expired`, `Expired`, or `Available`)
* `domains` (array(string)): Domains on this certificate other than files.com domains
* `expires_at` (date-time): Certificate expiration date/time
* `brick_managed` (boolean): Is this certificate automatically managed and renewed by Files.com?
* `intermediates` (string): Intermediate certificates
* `ip_addresses` (array(string)): A list of IP addresses associated with this SSL Certificate
* `issuer` (string): X509 issuer
* `key_type` (string): Type of key
* `request` (string): Certificate signing request text
* `status` (string): Certificate status (Request Generated, New, Active, Active/Expired, Expired, or Available)
* `subject` (string): X509 Subject name
* `certificate_domain` (string): Domain for certificate.
* `certificate_extra_domains` (array(string)): Additional domains for the certificate CSR.
* `certificate_country` (string): Country.
* `certificate_state_or_province` (string): State or province.
* `certificate_city_or_locale` (string): City or locale.
* `certificate_company_name` (string): Company name.
* `csr_ou1` (string): Department name or organization unit 1
* `csr_ou2` (string): Department name or organization unit 2
* `csr_ou3` (string): Department name or organization unit 3
* `certificate_email_address` (string): Email address for the certificate owner.
* `private_key` (string): Certificate private key.
* `password` (string): Certificate password.


---

## List Certificates

```
files_sdk.certificate.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## Show Certificate

```
files_sdk.certificate.find(id)
```

### Parameters

* `id` (int64): Required - Certificate ID.


---

## Create CSR or import existing SSL Certificate

```
files_sdk.certificate.create({
  "name": "Name",
  "certificate_domain": "domain.com",
  "certificate_extra_domains": ["www.domain.com"],
  "key_type": "RSA-4096",
  "certificate": "[certificate]",
  "intermediates": "[certificates]"
})
```

### Parameters

* `name` (string): Required - Internal name of the SSL certificate.
* `certificate_domain` (string): Domain for certificate.
* `certificate_extra_domains` (array(string)): Additional domains for the certificate CSR.
* `certificate_country` (string): Country.
* `certificate_state_or_province` (string): State or province.
* `certificate_city_or_locale` (string): City or locale.
* `certificate_company_name` (string): Company name.
* `csr_ou1` (string): Department name or organization unit 1
* `csr_ou2` (string): Department name or organization unit 2
* `csr_ou3` (string): Department name or organization unit 3
* `certificate_email_address` (string): Email address for the certificate owner.
* `key_type` (string): Any supported key type.  Defaults to `RSA-4096`.
* `certificate` (string): The certificate.  PEM or PKCS7 formats accepted.
* `private_key` (string): Certificate private key.
* `password` (string): Certificate password.
* `intermediates` (string): Intermediate certificates.  PEM or PKCS7 formats accepted.


---

## Deactivate SSL Certificate

```
files_sdk.certificate.deactivate(id)
```

### Parameters

* `id` (int64): Required - Certificate ID.


---

## Activate SSL Certificate

```
files_sdk.certificate.activate(id, {
  "replace_cert": ""
})
```

### Parameters

* `id` (int64): Required - Certificate ID.
* `replace_cert` (string): Leave blank or set to `any` to replace any currently active certificate, if applicable.  Set to `new_ips` to activate this certificate as an additional certificate on your Site by allocating a new set of Dedicated IPs (may require a Plan upgrade).  Set to the ID of a currently active certificate to replace that certificate on its set of dedicated IPs.


---

## Create an export CSV of Certificate resources

```
files_sdk.certificate.create_export()
```


---

## Update Certificate

```
files_sdk.certificate.update(id, {
  "name": "My Certificate",
  "intermediates": "[certificates]",
  "certificate": "[certificate]"
})
```

### Parameters

* `id` (int64): Required - Certificate ID.
* `name` (string): Internal certificate name.
* `intermediates` (string): Any intermediate certificates.  PEM or PKCS7 formats accepted.
* `certificate` (string): The certificate.  PEM or PKCS7 formats accepted.


---

## Delete Certificate

```
files_sdk.certificate.delete(id)
```

### Parameters

* `id` (int64): Required - Certificate ID.


---

## Deactivate SSL Certificate

```
certificate = files_sdk.certificate.find(id)
certificate.deactivate()
```

### Parameters

* `id` (int64): Required - Certificate ID.


---

## Activate SSL Certificate

```
certificate = files_sdk.certificate.find(id)
certificate.activate({
  "replace_cert": ""
})
```

### Parameters

* `id` (int64): Required - Certificate ID.
* `replace_cert` (string): Leave blank or set to `any` to replace any currently active certificate, if applicable.  Set to `new_ips` to activate this certificate as an additional certificate on your Site by allocating a new set of Dedicated IPs (may require a Plan upgrade).  Set to the ID of a currently active certificate to replace that certificate on its set of dedicated IPs.


---

## Update Certificate

```
certificate = files_sdk.certificate.find(id)
certificate.update({
  "name": "My Certificate",
  "intermediates": "[certificates]",
  "certificate": "[certificate]"
})
```

### Parameters

* `id` (int64): Required - Certificate ID.
* `name` (string): Internal certificate name.
* `intermediates` (string): Any intermediate certificates.  PEM or PKCS7 formats accepted.
* `certificate` (string): The certificate.  PEM or PKCS7 formats accepted.


---

## Delete Certificate

```
certificate = files_sdk.certificate.find(id)
certificate.delete()
```

### Parameters

* `id` (int64): Required - Certificate ID.
