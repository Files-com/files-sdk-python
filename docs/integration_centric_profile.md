# IntegrationCentricProfile

## Example IntegrationCentricProfile Object

The API sends each `IntegrationCentricProfile` record as JSON, such as:

```json
{
  "id": 1,
  "name": "Business Systems Onboarding",
  "workspace_id": 1,
  "use_for_all_users": false,
  "expected_remote_servers": [
    {
      "server_type": "dropbox",
      "name": "Dropbox"
    }
  ]
}
```

* `id` (int64): Integration Centric Profile ID
* `name` (string): Profile name
* `workspace_id` (int64): Workspace ID
* `use_for_all_users` (boolean): Whether this profile applies to all users in the Workspace by default
* `expected_remote_servers` (array(object)): Remote Server integrations the user is expected to add and connect. Each entry requires `server_type` and may include a display `name`.

The functions below use the module's settings. Each is also a method of a client's
`client.integration_centric_profile` resource, such as
`client.integration_centric_profile.list(...)`,
which uses that client's configuration instead.


---

## List Integration Centric Profiles

```python
files_sdk.integration_centric_profile.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `name`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`.


---

## Show Integration Centric Profile

```python
files_sdk.integration_centric_profile.find(id)
```

### Parameters

* `id` (int64): Required - Integration Centric Profile ID.


---

## Create Integration Centric Profile

```python
files_sdk.integration_centric_profile.create({
  "name": "Business Systems Onboarding",
  "expected_remote_servers": [{"server_type": "dropbox", "name": "Dropbox"}],
  "workspace_id": 1,
  "use_for_all_users": False
})
```

### Parameters

* `name` (string): Required - Profile name
* `expected_remote_servers` (array(object)): Required - Remote Server integrations the user is expected to add and connect. Each entry requires `server_type` and may include a display `name`.
* `workspace_id` (int64): Workspace ID
* `use_for_all_users` (boolean): Whether this profile applies to all users in the Workspace by default


---

## Update Integration Centric Profile

```python
files_sdk.integration_centric_profile.update(id, {
  "name": "Business Systems Onboarding",
  "workspace_id": 1,
  "expected_remote_servers": [{"server_type": "dropbox", "name": "Dropbox"}],
  "use_for_all_users": False
})
```

### Parameters

* `id` (int64): Required - Integration Centric Profile ID.
* `name` (string): Profile name
* `workspace_id` (int64): Workspace ID
* `expected_remote_servers` (array(object)): Remote Server integrations the user is expected to add and connect. Each entry requires `server_type` and may include a display `name`.
* `use_for_all_users` (boolean): Whether this profile applies to all users in the Workspace by default


---

## Delete Integration Centric Profile

```python
files_sdk.integration_centric_profile.delete(id)
```

### Parameters

* `id` (int64): Required - Integration Centric Profile ID.


---

## Update Integration Centric Profile

```python
integration_centric_profile = files_sdk.integration_centric_profile.find(id)
integration_centric_profile.update({
  "name": "Business Systems Onboarding",
  "workspace_id": 1,
  "expected_remote_servers": [{"server_type": "dropbox", "name": "Dropbox"}],
  "use_for_all_users": False
})
```

### Parameters

* `id` (int64): Required - Integration Centric Profile ID.
* `name` (string): Profile name
* `workspace_id` (int64): Workspace ID
* `expected_remote_servers` (array(object)): Remote Server integrations the user is expected to add and connect. Each entry requires `server_type` and may include a display `name`.
* `use_for_all_users` (boolean): Whether this profile applies to all users in the Workspace by default


---

## Delete Integration Centric Profile

```python
integration_centric_profile = files_sdk.integration_centric_profile.find(id)
integration_centric_profile.delete()
```

### Parameters

* `id` (int64): Required - Integration Centric Profile ID.
