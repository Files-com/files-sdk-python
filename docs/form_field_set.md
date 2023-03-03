# FormFieldSet

## Example FormFieldSet Object

```
{
  "id": 1,
  "title": "Sample Form Title",
  "form_layout": [
    1,
    2,
    3,
    4
  ],
  "form_fields": [
    null
  ],
  "skip_name": True,
  "skip_email": True,
  "skip_company": True
}
```

* `id` (int64): Form field set id
* `title` (string): Title to be displayed
* `form_layout` (array): Layout of the form
* `form_fields` (array): Associated form fields
* `skip_name` (boolean): Any associated InboxRegistrations or BundleRegistrations can be saved without providing name
* `skip_email` (boolean): Any associated InboxRegistrations or BundleRegistrations can be saved without providing email
* `skip_company` (boolean): Any associated InboxRegistrations or BundleRegistrations can be saved without providing company
* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.


---

## List Form Field Sets

```
files_sdk.form_field_set.list({
  "user_id": 1,
  "per_page": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show Form Field Set

```
files_sdk.form_field_set.find(id)
```

### Parameters

* `id` (int64): Required - Form Field Set ID.


---

## Create Form Field Set

```
files_sdk.form_field_set.create({
  "user_id": 1,
  "title": "Sample Form Title",
  "skip_email": True,
  "skip_name": True,
  "skip_company": True,
  "form_fields": [null]
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `title` (string): Title to be displayed
* `skip_email` (boolean): Skip validating form email
* `skip_name` (boolean): Skip validating form name
* `skip_company` (boolean): Skip validating company
* `form_fields` (array(object)): 


---

## Update Form Field Set

```
files_sdk.form_field_set.update(id, {
  "title": "Sample Form Title",
  "skip_email": True,
  "skip_name": True,
  "skip_company": True,
  "form_fields": [null]
})
```

### Parameters

* `id` (int64): Required - Form Field Set ID.
* `title` (string): Title to be displayed
* `skip_email` (boolean): Skip validating form email
* `skip_name` (boolean): Skip validating form name
* `skip_company` (boolean): Skip validating company
* `form_fields` (array(object)): 


---

## Delete Form Field Set

```
files_sdk.form_field_set.delete(id)
```

### Parameters

* `id` (int64): Required - Form Field Set ID.


---

## Update Form Field Set

```
form_field_set = files_sdk.form_field_set.list.first
form_field_set.update({
  "title": "Sample Form Title",
  "skip_email": True,
  "skip_name": True,
  "skip_company": True,
  "form_fields": [null]
})
```

### Parameters

* `id` (int64): Required - Form Field Set ID.
* `title` (string): Title to be displayed
* `skip_email` (boolean): Skip validating form email
* `skip_name` (boolean): Skip validating form name
* `skip_company` (boolean): Skip validating company
* `form_fields` (array(object)): 


---

## Delete Form Field Set

```
form_field_set = files_sdk.form_field_set.list.first
form_field_set.delete()
```

### Parameters

* `id` (int64): Required - Form Field Set ID.
