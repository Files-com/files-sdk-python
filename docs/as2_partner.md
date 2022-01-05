# As2Partner

## Example As2Partner Object

```
{
  "id": 1,
  "as2_station_id": 1,
  "name": "AS2 Partner Name",
  "uri": "",
  "public_certificate_md5": ""
}
```

* `id` (int64): Id of the AS2 Partner.
* `as2_station_id` (int64): Id of the AS2 Station associated with this partner.
* `name` (string): The partner's formal AS2 name.
* `uri` (string): Public URI for sending AS2 message to.
* `public_certificate_md5` (string): MD5 hash of public certificate used for message security.
* `public_certificate` (string): 


---

## List As2 Partners

```
files_sdk.as2_partner.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show As2 Partner

```
files_sdk.as2_partner.find(id)
```

### Parameters

* `id` (int64): Required - As2 Partner ID.


---

## Create As2 Partner

```
files_sdk.as2_partner.create({
  "name": "name",
  "uri": "uri",
  "public_certificate": "public_certificate",
  "as2_station_id": 1
})
```

### Parameters

* `name` (string): Required - AS2 Name
* `uri` (string): Required - URL base for AS2 responses
* `public_certificate` (string): Required - 
* `as2_station_id` (int64): Required - Id of As2Station for this partner


---

## Update As2 Partner

```
files_sdk.as2_partner.update(id, {
  "name": "AS2 Partner Name"
})
```

### Parameters

* `id` (int64): Required - As2 Partner ID.
* `name` (string): AS2 Name
* `uri` (string): URL base for AS2 responses
* `public_certificate` (string): 


---

## Delete As2 Partner

```
files_sdk.as2_partner.delete(id)
```

### Parameters

* `id` (int64): Required - As2 Partner ID.


---

## Update As2 Partner

```
as2_partner = files_sdk.as2_partner.list.first
as2_partner.update({
  "name": "AS2 Partner Name"
})
```

### Parameters

* `id` (int64): Required - As2 Partner ID.
* `name` (string): AS2 Name
* `uri` (string): URL base for AS2 responses
* `public_certificate` (string): 


---

## Delete As2 Partner

```
as2_partner = files_sdk.as2_partner.list.first
as2_partner.delete()
```

### Parameters

* `id` (int64): Required - As2 Partner ID.
