# PartnerChannel

## Example PartnerChannel Object

```
{
  "id": 1,
  "workspace_id": 1,
  "partner_id": 1,
  "path": "claims/medical",
  "to_partner_folder_name": "outgoing",
  "from_partner_folder_name": "incoming",
  "from_partner_route_path": "processing/from-partner",
  "to_partner_route_path": "delivery/to-partner",
  "effective_to_partner_folder_name": "outgoing",
  "effective_from_partner_folder_name": "incoming",
  "channel_path": "partners/acme/claims/medical",
  "to_partner_folder_path": "partners/acme/claims/medical/outgoing",
  "from_partner_folder_path": "partners/acme/claims/medical/incoming"
}
```

* `id` (int64): The unique ID of the Partner Channel.
* `workspace_id` (int64): ID of the Workspace associated with this Partner Channel.
* `partner_id` (int64): ID of the Partner this Channel belongs to.
* `path` (string): Channel path relative to the Partner root folder. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `to_partner_folder_name` (string): Optional Channel-level to-Partner folder name override.
* `from_partner_folder_name` (string): Optional Channel-level from-Partner folder name override.
* `from_partner_route_path` (string): Optional route path for files uploaded by the Partner.
* `to_partner_route_path` (string): Optional route path for files delivered to the Partner.
* `effective_to_partner_folder_name` (string): Resolved to-Partner folder name after Channel override and default.
* `effective_from_partner_folder_name` (string): Resolved from-Partner folder name after Channel override and default.
* `channel_path` (string): Resolved Channel folder path.
* `to_partner_folder_path` (string): Resolved to-Partner folder path.
* `from_partner_folder_path` (string): Resolved from-Partner folder path.


---

## List Partner Channels

```
files_sdk.partner_channel.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `path` or `partner_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `partner_id` and `workspace_id`. Valid field combinations are `[ workspace_id, partner_id ]`.


---

## Show Partner Channel

```
files_sdk.partner_channel.find(id)
```

### Parameters

* `id` (int64): Required - Partner Channel ID.


---

## Create Partner Channel

```
files_sdk.partner_channel.create({
  "from_partner_folder_name": "incoming",
  "from_partner_route_path": "processing/from-partner",
  "to_partner_folder_name": "outgoing",
  "to_partner_route_path": "delivery/to-partner",
  "partner_id": 1,
  "path": "claims/medical",
  "workspace_id": 0
})
```

### Parameters

* `from_partner_folder_name` (string): Optional Channel-level from-Partner folder name override.
* `from_partner_route_path` (string): Optional route path for files uploaded by the Partner.
* `to_partner_folder_name` (string): Optional Channel-level to-Partner folder name override.
* `to_partner_route_path` (string): Optional route path for files delivered to the Partner.
* `partner_id` (int64): Required - ID of the Partner this Channel belongs to.
* `path` (string): Required - Channel path relative to the Partner root folder.
* `workspace_id` (int64): ID of the Workspace associated with this Partner Channel.


---

## Create an export CSV of Partner Channel resources

```
files_sdk.partner_channel.create_export()
```

### Parameters

* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `path` or `partner_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `partner_id` and `workspace_id`. Valid field combinations are `[ workspace_id, partner_id ]`.


---

## Update Partner Channel

```
files_sdk.partner_channel.update(id, {
  "from_partner_folder_name": "incoming",
  "from_partner_route_path": "processing/from-partner",
  "to_partner_folder_name": "outgoing",
  "to_partner_route_path": "delivery/to-partner",
  "path": "claims/medical"
})
```

### Parameters

* `id` (int64): Required - Partner Channel ID.
* `from_partner_folder_name` (string): Optional Channel-level from-Partner folder name override.
* `from_partner_route_path` (string): Optional route path for files uploaded by the Partner.
* `to_partner_folder_name` (string): Optional Channel-level to-Partner folder name override.
* `to_partner_route_path` (string): Optional route path for files delivered to the Partner.
* `path` (string): Channel path relative to the Partner root folder.


---

## Delete Partner Channel

```
files_sdk.partner_channel.delete(id)
```

### Parameters

* `id` (int64): Required - Partner Channel ID.


---

## Update Partner Channel

```
partner_channel = files_sdk.partner_channel.find(id)
partner_channel.update({
  "from_partner_folder_name": "incoming",
  "from_partner_route_path": "processing/from-partner",
  "to_partner_folder_name": "outgoing",
  "to_partner_route_path": "delivery/to-partner",
  "path": "claims/medical"
})
```

### Parameters

* `id` (int64): Required - Partner Channel ID.
* `from_partner_folder_name` (string): Optional Channel-level from-Partner folder name override.
* `from_partner_route_path` (string): Optional route path for files uploaded by the Partner.
* `to_partner_folder_name` (string): Optional Channel-level to-Partner folder name override.
* `to_partner_route_path` (string): Optional route path for files delivered to the Partner.
* `path` (string): Channel path relative to the Partner root folder.


---

## Delete Partner Channel

```
partner_channel = files_sdk.partner_channel.find(id)
partner_channel.delete()
```

### Parameters

* `id` (int64): Required - Partner Channel ID.
