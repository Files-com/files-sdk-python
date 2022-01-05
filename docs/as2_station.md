# As2Station

## Example As2Station Object

```
{
  "id": 1,
  "name": "AS2 Station Name",
  "uri": "",
  "domain": "domain.test",
  "public_certificate": "",
  "public_certificate_md5": "",
  "private_key_md5": ""
}
```

* `id` (int64): Id of the AS2 Station.
* `name` (string): The station's formal AS2 name.
* `uri` (string): Public URI for sending AS2 message to.
* `domain` (string): The station's AS2 domain name.
* `public_certificate` (string): Public certificate used for message security.
* `public_certificate_md5` (string): MD5 hash of public certificate used for message security.
* `private_key_md5` (string): MD5 hash of private key used for message security.
* `private_key` (string): 


---

## List As2 Stations

```
files_sdk.as2_station.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
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
  "domain": "domain",
  "uri": "uri",
  "public_certificate": "public_certificate",
  "private_key": "private_key"
})
```

### Parameters

* `name` (string): Required - AS2 Name
* `domain` (string): Required - AS2 Domain
* `uri` (string): Required - URL base for AS2 responses
* `public_certificate` (string): Required - 
* `private_key` (string): Required - 


---

## Update As2 Station

```
files_sdk.as2_station.update(id, {
  "name": "AS2 Station Name",
  "domain": "domain.test"
})
```

### Parameters

* `id` (int64): Required - As2 Station ID.
* `name` (string): AS2 Name
* `domain` (string): AS2 Domain
* `uri` (string): URL base for AS2 responses
* `public_certificate` (string): 
* `private_key` (string): 


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
as2_station = files_sdk.as2_station.list.first
as2_station.update({
  "name": "AS2 Station Name",
  "domain": "domain.test"
})
```

### Parameters

* `id` (int64): Required - As2 Station ID.
* `name` (string): AS2 Name
* `domain` (string): AS2 Domain
* `uri` (string): URL base for AS2 responses
* `public_certificate` (string): 
* `private_key` (string): 


---

## Delete As2 Station

```
as2_station = files_sdk.as2_station.list.first
as2_station.delete()
```

### Parameters

* `id` (int64): Required - As2 Station ID.
