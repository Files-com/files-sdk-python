# Partner

## Example Partner Object

```
{
  "allow_bypassing_2fa_policies": True,
  "allow_credential_changes": True,
  "allow_user_creation": True,
  "id": 1,
  "name": "Acme Corp",
  "notes": "This is a note about the partner.",
  "root_folder": "/AcmeCorp",
  "tags": "example"
}
```

* `allow_bypassing_2fa_policies` (boolean): Allow users created under this Partner to bypass Two-Factor Authentication policies.
* `allow_credential_changes` (boolean): Allow Partner Admins to change or reset credentials for users belonging to this Partner.
* `allow_user_creation` (boolean): Allow Partner Admins to create users.
* `id` (int64): The unique ID of the Partner.
* `name` (string): The name of the Partner.
* `notes` (string): Notes about this Partner.
* `root_folder` (string): The root folder path for this Partner.
* `tags` (string): Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.


---

## List Partners

```
files_sdk.partner.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`.


---

## Show Partner

```
files_sdk.partner.find(id)
```

### Parameters

* `id` (int64): Required - Partner ID.


---

## Create Partner

```
files_sdk.partner.create({
  "name": "Acme Corp",
  "allow_bypassing_2fa_policies": False,
  "allow_credential_changes": False,
  "allow_user_creation": False,
  "notes": "This is a note about the partner.",
  "root_folder": "/AcmeCorp",
  "tags": "example"
})
```

### Parameters

* `name` (string): The name of the Partner.
* `allow_bypassing_2fa_policies` (boolean): Allow users created under this Partner to bypass Two-Factor Authentication policies.
* `allow_credential_changes` (boolean): Allow Partner Admins to change or reset credentials for users belonging to this Partner.
* `allow_user_creation` (boolean): Allow Partner Admins to create users.
* `notes` (string): Notes about this Partner.
* `root_folder` (string): The root folder path for this Partner.
* `tags` (string): Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.


---

## Update Partner

```
files_sdk.partner.update(id, {
  "name": "Acme Corp",
  "allow_bypassing_2fa_policies": False,
  "allow_credential_changes": False,
  "allow_user_creation": False,
  "notes": "This is a note about the partner.",
  "root_folder": "/AcmeCorp",
  "tags": "example"
})
```

### Parameters

* `id` (int64): Required - Partner ID.
* `name` (string): The name of the Partner.
* `allow_bypassing_2fa_policies` (boolean): Allow users created under this Partner to bypass Two-Factor Authentication policies.
* `allow_credential_changes` (boolean): Allow Partner Admins to change or reset credentials for users belonging to this Partner.
* `allow_user_creation` (boolean): Allow Partner Admins to create users.
* `notes` (string): Notes about this Partner.
* `root_folder` (string): The root folder path for this Partner.
* `tags` (string): Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.


---

## Delete Partner

```
files_sdk.partner.delete(id)
```

### Parameters

* `id` (int64): Required - Partner ID.


---

## Update Partner

```
partner = files_sdk.partner.find(id)
partner.update({
  "name": "Acme Corp",
  "allow_bypassing_2fa_policies": False,
  "allow_credential_changes": False,
  "allow_user_creation": False,
  "notes": "This is a note about the partner.",
  "root_folder": "/AcmeCorp",
  "tags": "example"
})
```

### Parameters

* `id` (int64): Required - Partner ID.
* `name` (string): The name of the Partner.
* `allow_bypassing_2fa_policies` (boolean): Allow users created under this Partner to bypass Two-Factor Authentication policies.
* `allow_credential_changes` (boolean): Allow Partner Admins to change or reset credentials for users belonging to this Partner.
* `allow_user_creation` (boolean): Allow Partner Admins to create users.
* `notes` (string): Notes about this Partner.
* `root_folder` (string): The root folder path for this Partner.
* `tags` (string): Comma-separated list of Tags for this Partner. Tags are used for other features, such as UserLifecycleRules, which can target specific tags.  Tags must only contain lowercase letters, numbers, and hyphens.


---

## Delete Partner

```
partner = files_sdk.partner.find(id)
partner.delete()
```

### Parameters

* `id` (int64): Required - Partner ID.
