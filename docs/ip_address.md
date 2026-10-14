# IpAddress

## Example IpAddress Object

The API sends each `IpAddress` record as JSON, such as:

```json
{
  "id": "Site",
  "associated_with": "Site",
  "group_id": 1,
  "ip_addresses": [
    "127.0.0.1"
  ]
}
```

* `id` (string): Unique label for list; used by Zapier and other integrations.
* `associated_with` (string): The object that this public IP address list is associated with.
* `group_id` (int64): Group ID
* `ip_addresses` (array(string)): A list of IP addresses.

The functions below use the module's settings. Each is also a method of a client's
`client.ip_address` resource, such as
`client.ip_address.list(...)`,
which uses that client's configuration instead.


---

## List IP Addresses associated with the current site

```python
files_sdk.ip_address.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## List all possible public SmartFile IP addresses

```python
files_sdk.ip_address.get_smartfile_reserved()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## List all possible public ExaVault IP addresses

```python
files_sdk.ip_address.get_exavault_reserved()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## List all possible public IP addresses

```python
files_sdk.ip_address.get_reserved()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
