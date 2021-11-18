# As2Key

## Example As2Key Object

```
{
  "id": 1,
  "as2_partnership_name": "Test",
  "created_at": "2000-01-01T01:00:00Z",
  "fingerprint": "cf:cb:d3:26:52:6c:55:88:83:17:13:cf:e7:70:eb:1b:32:37:38:c0"
}
```

* `id` (int64): AS2 Key ID
* `as2_partnership_name` (string): AS2 Partnership Name
* `created_at` (date-time): AS2 Key created at date/time
* `fingerprint` (string): Public key fingerprint
* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `public_key` (string): Actual contents of Public key.


---

## List As2 Keys

```
files_sdk.as2_key.list({
  "user_id": 1,
  "per_page": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show As2 Key

```
files_sdk.as2_key.find(id)
```

### Parameters

* `id` (int64): Required - As2 Key ID.


---

## Create As2 Key

```
files_sdk.as2_key.create({
  "user_id": 1,
  "as2_partnership_name": "Test",
  "public_key": "public_key"
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `as2_partnership_name` (string): Required - AS2 Partnership Name
* `public_key` (string): Required - Actual contents of Public key.


---

## Update As2 Key

```
files_sdk.as2_key.update(id, {
  "as2_partnership_name": "Test"
})
```

### Parameters

* `id` (int64): Required - As2 Key ID.
* `as2_partnership_name` (string): Required - AS2 Partnership Name


---

## Delete As2 Key

```
files_sdk.as2_key.delete(id)
```

### Parameters

* `id` (int64): Required - As2 Key ID.


---

## Update As2 Key

```
as2_key = files_sdk.as2_key.list.first
as2_key.update({
  "as2_partnership_name": "Test"
})
```

### Parameters

* `id` (int64): Required - As2 Key ID.
* `as2_partnership_name` (string): Required - AS2 Partnership Name


---

## Delete As2 Key

```
as2_key = files_sdk.as2_key.list.first
as2_key.delete()
```

### Parameters

* `id` (int64): Required - As2 Key ID.
