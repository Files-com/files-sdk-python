# UserLifecycleRule

## Example UserLifecycleRule Object

```
{
  "id": 1,
  "authentication_method": "password",
  "inactivity_days": 12,
  "include_folder_admins": True,
  "include_site_admins": True,
  "action": "disable",
  "site_id": 1
}
```

* `id` (int64): User Lifecycle Rule ID
* `authentication_method` (string): User authentication method for the rule
* `inactivity_days` (int64): Number of days of inactivity before the rule applies
* `include_folder_admins` (boolean): Include folder admins in the rule
* `include_site_admins` (boolean): Include site admins in the rule
* `action` (string): Action to take on inactive users (disable or delete)
* `site_id` (int64): Site ID


---

## List User Lifecycle Rules

```
files_sdk.user_lifecycle_rule.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


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
  "inactivity_days": 12,
  "include_site_admins": True,
  "include_folder_admins": True
})
```

### Parameters

* `action` (string): Required - Action to take on inactive users (disable or delete)
* `authentication_method` (string): Required - User authentication method for the rule
* `inactivity_days` (int64): Required - Number of days of inactivity before the rule applies
* `include_site_admins` (boolean): Include site admins in the rule
* `include_folder_admins` (boolean): Include folder admins in the rule


---

## Update User Lifecycle Rule

```
files_sdk.user_lifecycle_rule.update(id, {
  "authentication_method": "password",
  "inactivity_days": 12,
  "include_site_admins": True,
  "include_folder_admins": True
})
```

### Parameters

* `id` (int64): Required - User Lifecycle Rule ID.
* `action` (string): Required - Action to take on inactive users (disable or delete)
* `authentication_method` (string): Required - User authentication method for the rule
* `inactivity_days` (int64): Required - Number of days of inactivity before the rule applies
* `include_site_admins` (boolean): Include site admins in the rule
* `include_folder_admins` (boolean): Include folder admins in the rule


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
  "inactivity_days": 12,
  "include_site_admins": True,
  "include_folder_admins": True
})
```

### Parameters

* `id` (int64): Required - User Lifecycle Rule ID.
* `action` (string): Required - Action to take on inactive users (disable or delete)
* `authentication_method` (string): Required - User authentication method for the rule
* `inactivity_days` (int64): Required - Number of days of inactivity before the rule applies
* `include_site_admins` (boolean): Include site admins in the rule
* `include_folder_admins` (boolean): Include folder admins in the rule


---

## Delete User Lifecycle Rule

```
user_lifecycle_rule = files_sdk.user_lifecycle_rule.find(id)
user_lifecycle_rule.delete()
```

### Parameters

* `id` (int64): Required - User Lifecycle Rule ID.
