# DesktopConfigurationProfile

## Example DesktopConfigurationProfile Object

```
{
  "id": 1,
  "name": "North America Desktop Profile",
  "workspace_id": 1,
  "use_for_all_users": True,
  "mount_mappings": {
    "key": "example value"
  }
}
```

* `id` (int64): Desktop Configuration Profile ID
* `name` (string): Profile name
* `workspace_id` (int64): Workspace ID
* `use_for_all_users` (boolean): Whether this profile applies to all users in the Workspace by default
* `mount_mappings` (object): Mount point mappings for the desktop app. Keys are mount points (e.g. drive letters) and values are paths in Files.com that the mount points map to.


---

## List Desktop Configuration Profiles

```
files_sdk.desktop_configuration_profile.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.


---

## Show Desktop Configuration Profile

```
files_sdk.desktop_configuration_profile.find(id)
```

### Parameters

* `id` (int64): Required - Desktop Configuration Profile ID.


---

## Create Desktop Configuration Profile

```
files_sdk.desktop_configuration_profile.create({
  "name": "North America Desktop Profile",
  "mount_mappings": {"key":"example value"},
  "workspace_id": 1,
  "use_for_all_users": False
})
```

### Parameters

* `name` (string): Required - Profile name
* `mount_mappings` (object): Required - Mount point mappings for the desktop app. Keys are mount points (e.g. drive letters) and values are paths in Files.com that the mount points map to.
* `workspace_id` (int64): Workspace ID
* `use_for_all_users` (boolean): Whether this profile applies to all users in the Workspace by default


---

## Update Desktop Configuration Profile

```
files_sdk.desktop_configuration_profile.update(id, {
  "name": "North America Desktop Profile",
  "workspace_id": 1,
  "mount_mappings": {"key":"example value"},
  "use_for_all_users": False
})
```

### Parameters

* `id` (int64): Required - Desktop Configuration Profile ID.
* `name` (string): Profile name
* `workspace_id` (int64): Workspace ID
* `mount_mappings` (object): Mount point mappings for the desktop app. Keys are mount points (e.g. drive letters) and values are paths in Files.com that the mount points map to.
* `use_for_all_users` (boolean): Whether this profile applies to all users in the Workspace by default


---

## Delete Desktop Configuration Profile

```
files_sdk.desktop_configuration_profile.delete(id)
```

### Parameters

* `id` (int64): Required - Desktop Configuration Profile ID.


---

## Update Desktop Configuration Profile

```
desktop_configuration_profile = files_sdk.desktop_configuration_profile.find(id)
desktop_configuration_profile.update({
  "name": "North America Desktop Profile",
  "workspace_id": 1,
  "mount_mappings": {"key":"example value"},
  "use_for_all_users": False
})
```

### Parameters

* `id` (int64): Required - Desktop Configuration Profile ID.
* `name` (string): Profile name
* `workspace_id` (int64): Workspace ID
* `mount_mappings` (object): Mount point mappings for the desktop app. Keys are mount points (e.g. drive letters) and values are paths in Files.com that the mount points map to.
* `use_for_all_users` (boolean): Whether this profile applies to all users in the Workspace by default


---

## Delete Desktop Configuration Profile

```
desktop_configuration_profile = files_sdk.desktop_configuration_profile.find(id)
desktop_configuration_profile.delete()
```

### Parameters

* `id` (int64): Required - Desktop Configuration Profile ID.
