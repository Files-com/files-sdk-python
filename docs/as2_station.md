# As2Station

## Example As2Station Object

```
{
  "id": 1,
  "name": "AS2 Station Name",
  "uri": "example",
  "domain": "domain.test",
  "hex_public_certificate_serial": "A5:EB:C1:95:DC:D8:2B:E7",
  "public_certificate_md5": "example",
  "private_key_md5": "example",
  "public_certificate_subject": "example",
  "public_certificate_issuer": "example",
  "public_certificate_serial": "example",
  "public_certificate_not_before": "example",
  "public_certificate_not_after": "example",
  "private_key_password_md5": "example"
}
```

* `id` (int64): Id of the AS2 Station.
* `name` (string): The station's formal AS2 name.
* `uri` (string): Public URI for sending AS2 message to.
* `domain` (string): The station's AS2 domain name.
* `hex_public_certificate_serial` (string): Serial of public certificate used for message security in hex format.
* `public_certificate_md5` (string): MD5 hash of public certificate used for message security.
* `private_key_md5` (string): MD5 hash of private key used for message security.
* `public_certificate_subject` (string): Subject of public certificate used for message security.
* `public_certificate_issuer` (string): Issuer of public certificate used for message security.
* `public_certificate_serial` (string): Serial of public certificate used for message security.
* `public_certificate_not_before` (string): Not before value of public certificate used for message security.
* `public_certificate_not_after` (string): Not after value of public certificate used for message security.
* `private_key_password_md5` (string): MD5 hash of private key password used for message security.
* `public_certificate` (string): 
* `private_key` (string): 
* `private_key_password` (string): 


---

## List As2 Stations

```
files_sdk.as2_station.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show As2 Station

```
files_sdk.as2_station.find(id)
```

### Parameters

* `id` (int64): Required - As2 Station ID.


---

## Create As2 Station

```
files_sdk.as2_station.create({
  "name": "name",
  "public_certificate": "public_certificate",
  "private_key": "private_key"
})
```

### Parameters

* `name` (string): Required - AS2 Name
* `public_certificate` (string): Required - 
* `private_key` (string): Required - 
* `private_key_password` (string): 


---

## Update As2 Station

```
files_sdk.as2_station.update(id, {
  "name": "AS2 Station Name"
})
```

### Parameters

* `id` (int64): Required - As2 Station ID.
* `name` (string): AS2 Name
* `public_certificate` (string): 
* `private_key` (string): 
* `private_key_password` (string): 


---

## Delete As2 Station

```
files_sdk.as2_station.delete(id)
```

### Parameters

* `id` (int64): Required - As2 Station ID.


---

## Update As2 Station

```
as2_station = files_sdk.as2_station.find(id)
as2_station.update({
  "name": "AS2 Station Name"
})
```

### Parameters

* `id` (int64): Required - As2 Station ID.
* `name` (string): AS2 Name
* `public_certificate` (string): 
* `private_key` (string): 
* `private_key_password` (string): 


---

## Delete As2 Station

```
as2_station = files_sdk.as2_station.find(id)
as2_station.delete()
```

### Parameters

* `id` (int64): Required - As2 Station ID.
