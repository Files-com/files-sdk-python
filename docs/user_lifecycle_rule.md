# UserLifecycleRule

## Example UserLifecycleRule Object

```
{
  "id": 1,
  "authentication_method": "password",
  "group_ids": [
    1,
    2,
    3
  ],
  "action": "disable",
  "inactivity_days": 12,
  "include_folder_admins": True,
  "include_site_admins": True,
  "name": "password specific rules",
  "partner_tag": "guest",
  "site_id": 1,
  "user_state": "inactive",
  "user_tag": "guest"
}
```

* `id` (int64): User Lifecycle Rule ID
* `authentication_method` (string): User authentication method for which the rule will apply.
* `group_ids` (array(int64)): Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
* `action` (string): Action to take on inactive users (disable or delete)
* `inactivity_days` (int64): Number of days of inactivity before the rule applies
* `include_folder_admins` (boolean): If true, the rule will apply to folder admins.
* `include_site_admins` (boolean): If true, the rule will apply to site admins.
* `name` (string): User Lifecycle Rule name
* `partner_tag` (string): If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
* `site_id` (int64): Site ID
* `user_state` (string): State of the users to apply the rule to (inactive or disabled)
* `user_tag` (string): If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.


---

## List User Lifecycle Rules

```
files_sdk.user_lifecycle_rule.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`.


---

## Show User Lifecycle Rule

```
files_sdk.user_lifecycle_rule.find(id)
```

### Parameters

* `id` (int64): Required - User Lifecycle Rule ID.


---

## Create User Lifecycle Rule

```
files_sdk.user_lifecycle_rule.create({
  "authentication_method": "password",
  "group_ids": [1,2,3],
  "inactivity_days": 12,
  "include_site_admins": True,
  "include_folder_admins": True,
  "name": "password specific rules",
  "partner_tag": "guest",
  "user_state": "inactive",
  "user_tag": "guest"
})
```

### Parameters

* `action` (string): Action to take on inactive users (disable or delete)
* `authentication_method` (string): User authentication method for which the rule will apply.
* `group_ids` (array(int64)): Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
* `inactivity_days` (int64): Number of days of inactivity before the rule applies
* `include_site_admins` (boolean): If true, the rule will apply to site admins.
* `include_folder_admins` (boolean): If true, the rule will apply to folder admins.
* `name` (string): User Lifecycle Rule name
* `partner_tag` (string): If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
* `user_state` (string): State of the users to apply the rule to (inactive or disabled)
* `user_tag` (string): If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.


---

## Update User Lifecycle Rule

```
files_sdk.user_lifecycle_rule.update(id, {
  "authentication_method": "password",
  "group_ids": [1,2,3],
  "inactivity_days": 12,
  "include_site_admins": True,
  "include_folder_admins": True,
  "name": "password specific rules",
  "partner_tag": "guest",
  "user_state": "inactive",
  "user_tag": "guest"
})
```

### Parameters

* `id` (int64): Required - User Lifecycle Rule ID.
* `action` (string): Action to take on inactive users (disable or delete)
* `authentication_method` (string): User authentication method for which the rule will apply.
* `group_ids` (array(int64)): Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
* `inactivity_days` (int64): Number of days of inactivity before the rule applies
* `include_site_admins` (boolean): If true, the rule will apply to site admins.
* `include_folder_admins` (boolean): If true, the rule will apply to folder admins.
* `name` (string): User Lifecycle Rule name
* `partner_tag` (string): If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
* `user_state` (string): State of the users to apply the rule to (inactive or disabled)
* `user_tag` (string): If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.


---

## Delete User Lifecycle Rule

```
files_sdk.user_lifecycle_rule.delete(id)
```

### Parameters

* `id` (int64): Required - User Lifecycle Rule ID.


---

## Update User Lifecycle Rule

```
user_lifecycle_rule = files_sdk.user_lifecycle_rule.find(id)
user_lifecycle_rule.update({
  "authentication_method": "password",
  "group_ids": [1,2,3],
  "inactivity_days": 12,
  "include_site_admins": True,
  "include_folder_admins": True,
  "name": "password specific rules",
  "partner_tag": "guest",
  "user_state": "inactive",
  "user_tag": "guest"
})
```

### Parameters

* `id` (int64): Required - User Lifecycle Rule ID.
* `action` (string): Action to take on inactive users (disable or delete)
* `authentication_method` (string): User authentication method for which the rule will apply.
* `group_ids` (array(int64)): Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
* `inactivity_days` (int64): Number of days of inactivity before the rule applies
* `include_site_admins` (boolean): If true, the rule will apply to site admins.
* `include_folder_admins` (boolean): If true, the rule will apply to folder admins.
* `name` (string): User Lifecycle Rule name
* `partner_tag` (string): If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
* `user_state` (string): State of the users to apply the rule to (inactive or disabled)
* `user_tag` (string): If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.


---

## Delete User Lifecycle Rule

```
user_lifecycle_rule = files_sdk.user_lifecycle_rule.find(id)
user_lifecycle_rule.delete()
```

### Parameters

* `id` (int64): Required - User Lifecycle Rule ID.
