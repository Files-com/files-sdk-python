# PartnerChannelTemplate

## Example PartnerChannelTemplate Object

```
{
  "id": 1,
  "workspace_id": 1,
  "name": "Claims Template",
  "path": "claims/medical",
  "to_partner_folder_name": "outgoing",
  "from_partner_folder_name": "incoming",
  "from_partner_route_path_pattern": "processing/{{partner_name}}/from-partner",
  "to_partner_route_path_pattern": "delivery/{{partner_name}}/to-partner",
  "to_partner_managed_folder_paths": [
    "reports/monthly"
  ],
  "from_partner_managed_folder_paths": [
    "claims/received"
  ],
  "effective_to_partner_folder_name": "outgoing",
  "effective_from_partner_folder_name": "incoming"
}
```

* `id` (int64): The unique ID of the Partner Channel Template.
* `workspace_id` (int64): ID of the Workspace associated with this Partner Channel Template.
* `name` (string): The name of the Partner Channel Template.
* `path` (string): Channel path relative to the Partner root folder. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `to_partner_folder_name` (string): Optional Channel-level to-Partner folder name override.
* `from_partner_folder_name` (string): Optional Channel-level from-Partner folder name override.
* `from_partner_route_path_pattern` (string): Optional route path pattern for files uploaded by the Partner. Supports {{partner_name}}.
* `to_partner_route_path_pattern` (string): Optional route path pattern for files delivered to the Partner. Supports {{partner_name}}.
* `to_partner_managed_folder_paths` (array(string)): Managed folder paths inside the to-Partner folder.
* `from_partner_managed_folder_paths` (array(string)): Managed folder paths inside the from-Partner folder.
* `effective_to_partner_folder_name` (string): Resolved to-Partner folder name after Template override and default.
* `effective_from_partner_folder_name` (string): Resolved from-Partner folder name after Template override and default.


---

## List Partner Channel Templates

```
files_sdk.partner_channel_template.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.


---

## Show Partner Channel Template

```
files_sdk.partner_channel_template.find(id)
```

### Parameters

* `id` (int64): Required - Partner Channel Template ID.


---

## Create Partner Channel Template

```
files_sdk.partner_channel_template.create({
  "from_partner_folder_name": "incoming",
  "from_partner_managed_folder_paths": ["claims/received"],
  "from_partner_route_path_pattern": "processing/{{partner_name}}/from-partner",
  "to_partner_folder_name": "outgoing",
  "to_partner_managed_folder_paths": ["reports/monthly"],
  "to_partner_route_path_pattern": "delivery/{{partner_name}}/to-partner",
  "name": "Claims Template",
  "path": "claims/medical",
  "workspace_id": 0
})
```

### Parameters

* `from_partner_folder_name` (string): Optional Channel-level from-Partner folder name override.
* `from_partner_managed_folder_paths` (array(string)): Managed folder paths inside the from-Partner folder.
* `from_partner_route_path_pattern` (string): Optional route path pattern for files uploaded by the Partner. Supports {{partner_name}}.
* `to_partner_folder_name` (string): Optional Channel-level to-Partner folder name override.
* `to_partner_managed_folder_paths` (array(string)): Managed folder paths inside the to-Partner folder.
* `to_partner_route_path_pattern` (string): Optional route path pattern for files delivered to the Partner. Supports {{partner_name}}.
* `name` (string): Required - The name of the Partner Channel Template.
* `path` (string): Required - Channel path relative to the Partner root folder.
* `workspace_id` (int64): ID of the Workspace associated with this Partner Channel Template.


---

## Update Partner Channel Template

```
files_sdk.partner_channel_template.update(id, {
  "from_partner_folder_name": "incoming",
  "from_partner_managed_folder_paths": ["claims/received"],
  "from_partner_route_path_pattern": "processing/{{partner_name}}/from-partner",
  "to_partner_folder_name": "outgoing",
  "to_partner_managed_folder_paths": ["reports/monthly"],
  "to_partner_route_path_pattern": "delivery/{{partner_name}}/to-partner",
  "name": "Claims Template",
  "path": "claims/medical"
})
```

### Parameters

* `id` (int64): Required - Partner Channel Template ID.
* `from_partner_folder_name` (string): Optional Channel-level from-Partner folder name override.
* `from_partner_managed_folder_paths` (array(string)): Managed folder paths inside the from-Partner folder.
* `from_partner_route_path_pattern` (string): Optional route path pattern for files uploaded by the Partner. Supports {{partner_name}}.
* `to_partner_folder_name` (string): Optional Channel-level to-Partner folder name override.
* `to_partner_managed_folder_paths` (array(string)): Managed folder paths inside the to-Partner folder.
* `to_partner_route_path_pattern` (string): Optional route path pattern for files delivered to the Partner. Supports {{partner_name}}.
* `name` (string): The name of the Partner Channel Template.
* `path` (string): Channel path relative to the Partner root folder.


---

## Delete Partner Channel Template

```
files_sdk.partner_channel_template.delete(id)
```

### Parameters

* `id` (int64): Required - Partner Channel Template ID.


---

## Update Partner Channel Template

```
partner_channel_template = files_sdk.partner_channel_template.find(id)
partner_channel_template.update({
  "from_partner_folder_name": "incoming",
  "from_partner_managed_folder_paths": ["claims/received"],
  "from_partner_route_path_pattern": "processing/{{partner_name}}/from-partner",
  "to_partner_folder_name": "outgoing",
  "to_partner_managed_folder_paths": ["reports/monthly"],
  "to_partner_route_path_pattern": "delivery/{{partner_name}}/to-partner",
  "name": "Claims Template",
  "path": "claims/medical"
})
```

### Parameters

* `id` (int64): Required - Partner Channel Template ID.
* `from_partner_folder_name` (string): Optional Channel-level from-Partner folder name override.
* `from_partner_managed_folder_paths` (array(string)): Managed folder paths inside the from-Partner folder.
* `from_partner_route_path_pattern` (string): Optional route path pattern for files uploaded by the Partner. Supports {{partner_name}}.
* `to_partner_folder_name` (string): Optional Channel-level to-Partner folder name override.
* `to_partner_managed_folder_paths` (array(string)): Managed folder paths inside the to-Partner folder.
* `to_partner_route_path_pattern` (string): Optional route path pattern for files delivered to the Partner. Supports {{partner_name}}.
* `name` (string): The name of the Partner Channel Template.
* `path` (string): Channel path relative to the Partner root folder.


---

## Delete Partner Channel Template

```
partner_channel_template = files_sdk.partner_channel_template.find(id)
partner_channel_template.delete()
```

### Parameters

* `id` (int64): Required - Partner Channel Template ID.
