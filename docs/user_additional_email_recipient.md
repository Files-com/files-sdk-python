# UserAdditionalEmailRecipient

## Example UserAdditionalEmailRecipient Object

```
{
  "id": 1,
  "user_id": 1,
  "workspace_id": 1,
  "email": "user-copy@example.com",
  "created_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): User additional email recipient ID
* `user_id` (int64): User ID
* `workspace_id` (int64): Workspace ID (0 for default workspace).
* `email` (string): Additional email recipient address
* `created_at` (date-time): Created at date/time


---

## List User Additional Email Recipients

```
files_sdk.user_additional_email_recipient.list({
  "user_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `email`, `user_id` or `workspace_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `email` and `workspace_id`. Valid field combinations are `[ workspace_id, email ]`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `email`.


---

## Show User Additional Email Recipient

```
files_sdk.user_additional_email_recipient.find(id)
```

### Parameters

* `id` (int64): Required - User Additional Email Recipient ID.


---

## Create User Additional Email Recipient

```
files_sdk.user_additional_email_recipient.create({
  "user_id": 1,
  "email": "user-copy@example.com"
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `email` (string): Required - Additional email recipient address


---

## Update User Additional Email Recipient

```
files_sdk.user_additional_email_recipient.update(id, {
  "email": "user-copy@example.com"
})
```

### Parameters

* `id` (int64): Required - User Additional Email Recipient ID.
* `email` (string): Additional email recipient address


---

## Delete User Additional Email Recipient

```
files_sdk.user_additional_email_recipient.delete(id)
```

### Parameters

* `id` (int64): Required - User Additional Email Recipient ID.


---

## Update User Additional Email Recipient

```
user_additional_email_recipient = files_sdk.user_additional_email_recipient.find(id)
user_additional_email_recipient.update({
  "email": "user-copy@example.com"
})
```

### Parameters

* `id` (int64): Required - User Additional Email Recipient ID.
* `email` (string): Additional email recipient address


---

## Delete User Additional Email Recipient

```
user_additional_email_recipient = files_sdk.user_additional_email_recipient.find(id)
user_additional_email_recipient.delete()
```

### Parameters

* `id` (int64): Required - User Additional Email Recipient ID.
