# IpAbuseEntry

* `ip` (string): 
* `list` (string): 
* `hostname` (string): 
* `reason` (string): 


---

## List IP Abuse Entries

```
files_sdk.ip_abuse_entry.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## Create IP Abuse Entry

```
files_sdk.ip_abuse_entry.create({
  "ip": "ip"
})
```

### Parameters

* `ip` (string): Required - 
* `list` (string): 
* `hostname` (string): 
* `reason` (string): 


---

## Create an export CSV of IP Abuse Entry resources

```
files_sdk.ip_abuse_entry.create_export()
```
