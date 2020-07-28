# IpAddress

## Example IpAddress Object

```
{
  "id": "Site",
  "associated_with": "Site",
  "group_id": 1,
  "ip_addresses": [

  ]
}
```

* `id` (string): Unique label for list; used by Zapier and other integrations.
* `associated_with` (string): The object that this public IP address list is associated with.
* `group_id` (int64): Group ID
* `ip_addresses` (array): A list of IP addresses.


---

## List IP Addresses associated with the current site

```
files_sdk.ip_address.list({
  "page": 1,
  "per_page": 1
})
```

### Parameters

* `page` (int64): Current page number.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): Deprecated: If set to `count` returns a count of matching records rather than the records themselves.


---

## List all possible public IP addresses

```
files_sdk.ip_address.get_reserved({
  "page": 1,
  "per_page": 1
})
```

### Parameters

* `page` (int64): Current page number.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
