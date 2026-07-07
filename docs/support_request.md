# SupportRequest

## Example SupportRequest Object

```
{
  "id": 1,
  "subject": "example",
  "comment": "example",
  "created_at": "2000-01-01T01:00:00Z",
  "access_until": "2000-01-01T01:00:00Z",
  "customer_success_access": "`no`",
  "priority": "`low`",
  "name": "John Doe",
  "phone_number": "555-555-5555"
}
```

* `id` (int64): ID
* `subject` (string): Subject of the support request.
* `comment` (string): Main body of the support request.
* `created_at` (date): When this support request was made.
* `access_until` (date): Customer Support can access your user account up through this date/time.
* `customer_success_access` (string): Enable Customer Support access to your user account?
* `priority` (string): Priority. Can be `low` (e.g. general or billing/account questions), `normal` (e.g. the system is impaired), `high` (e.g. a production workflow or business process is impaired), `urgent` (e.g. a production workflow or business process is down), `critical` (e.g. a business-critical workflow or business process is down)
* `name` (string): Support Request name
* `phone_number` (string): Support Request phone number
* `access_reset` (boolean): If set to `true`, will reset the customer success access window.
* `email` (string): Email address of the user requesting support.
* `attachments_files` (array(file)): 


---

## List Support Requests

```
files_sdk.support_request.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .


---

## Create Support Request

```
files_sdk.support_request.create({
  "customer_success_access": "`no`",
  "access_reset": False,
  "email": "email",
  "subject": "example",
  "comment": "example",
  "priority": "`low`",
  "phone_number": "555-555-5555",
  "name": "John Doe"
})
```

### Parameters

* `customer_success_access` (string): Enable Customer Support access to your user account?
* `access_reset` (boolean): If set to `true`, will reset the customer success access window.
* `email` (string): Required - Email address of the user requesting support.
* `subject` (string): Required - Subject of the support request.
* `comment` (string): Required - Main body of the support request.
* `priority` (string): Priority. Can be `low` (e.g. general or billing/account questions), `normal` (e.g. the system is impaired), `high` (e.g. a production workflow or business process is impaired), `urgent` (e.g. a production workflow or business process is down), `critical` (e.g. a business-critical workflow or business process is down)
* `phone_number` (string): Support Request phone number
* `name` (string): Support Request name
* `attachments_files` (array(file)): 


---

## Create an export CSV of Support Request resources

```
files_sdk.support_request.create_export()
```

### Parameters

* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .


---

## Update Support Request

```
files_sdk.support_request.update(id, {
  "customer_success_access": "`no`",
  "access_reset": False
})
```

### Parameters

* `id` (int64): Required - Support Request ID.
* `customer_success_access` (string): Enable Customer Support access to your user account?
* `access_reset` (boolean): If set to `true`, will reset the customer success access window.


---

## Update Support Request

```
support_request = files_sdk.support_request.list.first
support_request.update({
  "customer_success_access": "`no`",
  "access_reset": False
})
```

### Parameters

* `id` (int64): Required - Support Request ID.
* `customer_success_access` (string): Enable Customer Support access to your user account?
* `access_reset` (boolean): If set to `true`, will reset the customer success access window.
