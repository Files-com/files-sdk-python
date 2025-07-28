# ChildSiteManagementPolicy

## Example ChildSiteManagementPolicy Object

```
{
  "id": 1,
  "site_id": 1,
  "site_setting_name": "color2_left",
  "managed_value": "#FF0000",
  "skip_child_site_ids": [
    1,
    5
  ]
}
```

* `id` (int64): ChildSiteManagementPolicy ID
* `site_id` (int64): ID of the Site managing the policy
* `site_setting_name` (string): The name of the setting that is managed by the policy
* `managed_value` (string): The value for the setting that will be enforced for all child sites that are not exempt
* `skip_child_site_ids` (array(int64)): The list of child site IDs that are exempt from this policy


---

## List Child Site Management Policies

```
files_sdk.child_site_management_policy.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show Child Site Management Policy

```
files_sdk.child_site_management_policy.find(id)
```

### Parameters

* `id` (int64): Required - Child Site Management Policy ID.


---

## Create Child Site Management Policy

```
files_sdk.child_site_management_policy.create({
  "site_setting_name": "color2_left",
  "managed_value": "#FF0000",
  "skip_child_site_ids": [1,5]
})
```

### Parameters

* `site_setting_name` (string): Required - The name of the setting that is managed by the policy
* `managed_value` (string): Required - The value for the setting that will be enforced for all child sites that are not exempt
* `skip_child_site_ids` (array(int64)): The list of child site IDs that are exempt from this policy


---

## Update Child Site Management Policy

```
files_sdk.child_site_management_policy.update(id, {
  "site_setting_name": "color2_left",
  "managed_value": "#FF0000",
  "skip_child_site_ids": [1,5]
})
```

### Parameters

* `id` (int64): Required - Child Site Management Policy ID.
* `site_setting_name` (string): Required - The name of the setting that is managed by the policy
* `managed_value` (string): Required - The value for the setting that will be enforced for all child sites that are not exempt
* `skip_child_site_ids` (array(int64)): The list of child site IDs that are exempt from this policy


---

## Delete Child Site Management Policy

```
files_sdk.child_site_management_policy.delete(id)
```

### Parameters

* `id` (int64): Required - Child Site Management Policy ID.


---

## Update Child Site Management Policy

```
child_site_management_policy = files_sdk.child_site_management_policy.find(id)
child_site_management_policy.update({
  "site_setting_name": "color2_left",
  "managed_value": "#FF0000",
  "skip_child_site_ids": [1,5]
})
```

### Parameters

* `id` (int64): Required - Child Site Management Policy ID.
* `site_setting_name` (string): Required - The name of the setting that is managed by the policy
* `managed_value` (string): Required - The value for the setting that will be enforced for all child sites that are not exempt
* `skip_child_site_ids` (array(int64)): The list of child site IDs that are exempt from this policy


---

## Delete Child Site Management Policy

```
child_site_management_policy = files_sdk.child_site_management_policy.find(id)
child_site_management_policy.delete()
```

### Parameters

* `id` (int64): Required - Child Site Management Policy ID.
