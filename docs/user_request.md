# UserRequest

## Example UserRequest Object

```
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@files.com",
  "details": "Changed Departments"
}
```

* `id` (int64): ID
* `name` (string): User's full name
* `email` (email): User email address
* `details` (string): Details of the user's request


---

## List User Requests

```
files_sdk.user_request.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show User Request

```
files_sdk.user_request.find(id)
```

### Parameters

* `id` (int64): Required - User Request ID.


---

## Create User Request

```
files_sdk.user_request.create({
  "name": "name",
  "email": "email",
  "details": "details"
})
```

### Parameters

* `name` (string): Required - Name of user requested
* `email` (string): Required - Email of user requested
* `details` (string): Required - Details of the user request


---

## Delete User Request

```
files_sdk.user_request.delete(id)
```

### Parameters

* `id` (int64): Required - User Request ID.


---

## Delete User Request

```
user_request = files_sdk.user_request.list.first
user_request.delete()
```

### Parameters

* `id` (int64): Required - User Request ID.
