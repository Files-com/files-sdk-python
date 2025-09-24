# ChildSiteManagementPolicy

## Example ChildSiteManagementPolicy Object

```
{
  "id": 1,
  "policy_type": "settings",
  "name": "example",
  "description": "example",
  "value": "{ \"color2_left\": \"#000000\" }",
  "applied_child_site_ids": [
    1,
    2
  ],
  "skip_child_site_ids": [
    1,
    2
  ],
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Policy ID.
* `policy_type` (string): Type of policy.  Valid values: `settings`.
* `name` (string): Name for this policy.
* `description` (string): Description for this policy.
* `value` (object): Policy configuration data. Attributes differ by policy type. For more information, refer to the Value Hash section of the developer documentation.
* `applied_child_site_ids` (array(int64)): IDs of child sites that this policy has been applied to. This field is read-only.
* `skip_child_site_ids` (array(int64)): IDs of child sites that this policy has been exempted from. If `skip_child_site_ids` is empty, the policy will be applied to all child sites. To apply a policy to a child site that has been exempted, remove it from `skip_child_site_ids` or set it to an empty array (`[]`).
* `created_at` (date-time): When this policy was created.
* `updated_at` (date-time): When this policy was last updated.


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
  "value": "{ \"color2_left\": \"#000000\" }",
  "skip_child_site_ids": [1,2],
  "policy_type": "settings",
  "name": "example",
  "description": "example"
})
```

### Parameters

* `value` (string): 
* `skip_child_site_ids` (array(int64)): IDs of child sites that this policy has been exempted from. If `skip_child_site_ids` is empty, the policy will be applied to all child sites. To apply a policy to a child site that has been exempted, remove it from `skip_child_site_ids` or set it to an empty array (`[]`).
* `policy_type` (string): Required - Type of policy.  Valid values: `settings`.
* `name` (string): Name for this policy.
* `description` (string): Description for this policy.


---

## Update Child Site Management Policy

```
files_sdk.child_site_management_policy.update(id, {
  "value": "{ \"color2_left\": \"#000000\" }",
  "skip_child_site_ids": [1,2],
  "policy_type": "settings",
  "name": "example",
  "description": "example"
})
```

### Parameters

* `id` (int64): Required - Child Site Management Policy ID.
* `value` (string): 
* `skip_child_site_ids` (array(int64)): IDs of child sites that this policy has been exempted from. If `skip_child_site_ids` is empty, the policy will be applied to all child sites. To apply a policy to a child site that has been exempted, remove it from `skip_child_site_ids` or set it to an empty array (`[]`).
* `policy_type` (string): Type of policy.  Valid values: `settings`.
* `name` (string): Name for this policy.
* `description` (string): Description for this policy.


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
  "value": "{ \"color2_left\": \"#000000\" }",
  "skip_child_site_ids": [1,2],
  "policy_type": "settings",
  "name": "example",
  "description": "example"
})
```

### Parameters

* `id` (int64): Required - Child Site Management Policy ID.
* `value` (string): 
* `skip_child_site_ids` (array(int64)): IDs of child sites that this policy has been exempted from. If `skip_child_site_ids` is empty, the policy will be applied to all child sites. To apply a policy to a child site that has been exempted, remove it from `skip_child_site_ids` or set it to an empty array (`[]`).
* `policy_type` (string): Type of policy.  Valid values: `settings`.
* `name` (string): Name for this policy.
* `description` (string): Description for this policy.


---

## Delete Child Site Management Policy

```
child_site_management_policy = files_sdk.child_site_management_policy.find(id)
child_site_management_policy.delete()
```

### Parameters

* `id` (int64): Required - Child Site Management Policy ID.
