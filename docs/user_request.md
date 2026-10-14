# UserRequest

## Example UserRequest Object

The API sends each `UserRequest` record as JSON, such as:

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@files.com",
  "details": "Changed Departments",
  "company": "Acme Inc."
}
```

* `id` (int64): ID
* `name` (string): User's full name
* `email` (email): User email address
* `details` (string): Details of the user's request
* `company` (string): User's company name

The functions below use the module's settings. Each is also a method of a client's
`client.user_request` resource, such as
`client.user_request.list(...)`,
which uses that client's configuration instead.


---

## List User Requests

```python
files_sdk.user_request.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## Show User Request

```python
files_sdk.user_request.find(id)
```

### Parameters

* `id` (int64): Required - User Request ID.


---

## Create User Request

```python
files_sdk.user_request.create({
  "name": "name",
  "email": "email",
  "details": "details",
  "company": "Acme Inc."
})
```

### Parameters

* `name` (string): Required - Name of user requested
* `email` (string): Required - Email of user requested
* `details` (string): Required - Details of the user request
* `company` (string): Company of the user requested


---

## Delete User Request

```python
files_sdk.user_request.delete(id)
```

### Parameters

* `id` (int64): Required - User Request ID.


---

## Delete User Request

```python
user_request = files_sdk.user_request.find(id)
user_request.delete()
```

### Parameters

* `id` (int64): Required - User Request ID.
