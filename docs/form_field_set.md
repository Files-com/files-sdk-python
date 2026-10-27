# FormFieldSet

## Example FormFieldSet Object

The API sends each `FormFieldSet` record as JSON, such as:

```json
{
  "id": 1,
  "title": "Sample Form Title",
  "require_complete_metadata_capture": false,
  "form_layout": [
    1,
    2,
    3,
    4
  ],
  "form_fields": [
    {
      "label": "Department",
      "field_type": "dropdown",
      "required": true,
      "options_for_select": [
        "Finance",
        "Sales"
      ]
    }
  ],
  "skip_name": true,
  "skip_email": true,
  "skip_company": true,
  "in_use": true
}
```

* `id` (int64): Form field set id
* `title` (string): Title to be displayed
* `require_complete_metadata_capture` (boolean): Reject answers over 1024 characters or more than 32 answered custom fields to ensure complete file metadata capture
* `form_layout` (array(int64)): Layout of the form
* `form_fields` (array(object)): Associated form field definitions; authenticated form field set responses include historical definitions, while form_layout identifies current fields
* `skip_name` (boolean): Any associated InboxRegistrations or BundleRegistrations can be saved without providing name
* `skip_email` (boolean): Any associated InboxRegistrations or BundleRegistrations can be saved without providing email
* `skip_company` (boolean): Any associated InboxRegistrations or BundleRegistrations can be saved without providing company
* `in_use` (boolean): Form Field Set is in use by an active Inbox / Bundle / Inbox Registration / Bundle Registration
* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `workspace_id` (int64): Workspace ID

The functions below use the module's settings. Each is also a method of a client's
`client.form_field_set` resource, such as
`client.form_field_set.list(...)`,
which uses that client's configuration instead.


---

## List Form Field Sets

```python
files_sdk.form_field_set.list({
  "user_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## Show Form Field Set

```python
files_sdk.form_field_set.find(id)
```

### Parameters

* `id` (int64): Required - Form Field Set ID.


---

## Create Form Field Set

```python
files_sdk.form_field_set.create({
  "user_id": 1,
  "title": "Sample Form Title",
  "require_complete_metadata_capture": False,
  "workspace_id": 1,
  "skip_email": False,
  "skip_name": False,
  "skip_company": False,
  "form_fields": [{"label": "Department", "field_type": "dropdown", "required": True, "options_for_select": ["Finance", "Sales"]}]
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `title` (string): Title to be displayed
* `require_complete_metadata_capture` (boolean): Reject answers over 1024 characters or more than 32 answered custom fields to ensure complete file metadata capture
* `workspace_id` (int64): Workspace ID
* `skip_email` (boolean): Skip validating form email
* `skip_name` (boolean): Skip validating form name
* `skip_company` (boolean): Skip validating company
* `form_fields` (array(object)): 


---

## Update Form Field Set

```python
files_sdk.form_field_set.update(id, {
  "title": "Sample Form Title",
  "require_complete_metadata_capture": False,
  "workspace_id": 1,
  "skip_email": False,
  "skip_name": False,
  "skip_company": False,
  "form_fields": [{"label": "Department", "field_type": "dropdown", "required": True, "options_for_select": ["Finance", "Sales"]}]
})
```

### Parameters

* `id` (int64): Required - Form Field Set ID.
* `title` (string): Title to be displayed
* `require_complete_metadata_capture` (boolean): Reject answers over 1024 characters or more than 32 answered custom fields to ensure complete file metadata capture
* `workspace_id` (int64): Workspace ID
* `skip_email` (boolean): Skip validating form email
* `skip_name` (boolean): Skip validating form name
* `skip_company` (boolean): Skip validating company
* `form_fields` (array(object)): 


---

## Delete Form Field Set

```python
files_sdk.form_field_set.delete(id)
```

### Parameters

* `id` (int64): Required - Form Field Set ID.


---

## Update Form Field Set

```python
form_field_set = files_sdk.form_field_set.find(id)
form_field_set.update({
  "title": "Sample Form Title",
  "require_complete_metadata_capture": False,
  "workspace_id": 1,
  "skip_email": False,
  "skip_name": False,
  "skip_company": False,
  "form_fields": [{"label": "Department", "field_type": "dropdown", "required": True, "options_for_select": ["Finance", "Sales"]}]
})
```

### Parameters

* `id` (int64): Required - Form Field Set ID.
* `title` (string): Title to be displayed
* `require_complete_metadata_capture` (boolean): Reject answers over 1024 characters or more than 32 answered custom fields to ensure complete file metadata capture
* `workspace_id` (int64): Workspace ID
* `skip_email` (boolean): Skip validating form email
* `skip_name` (boolean): Skip validating form name
* `skip_company` (boolean): Skip validating company
* `form_fields` (array(object)): 


---

## Delete Form Field Set

```python
form_field_set = files_sdk.form_field_set.find(id)
form_field_set.delete()
```

### Parameters

* `id` (int64): Required - Form Field Set ID.
