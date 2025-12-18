# KeyLifecycleRule

## Example KeyLifecycleRule Object

```
{
  "id": 1,
  "key_type": "gpg",
  "inactivity_days": 12,
  "name": "inactive gpg keys"
}
```

* `id` (int64): Key Lifecycle Rule ID
* `key_type` (string): Key type for which the rule will apply (gpg or ssh).
* `inactivity_days` (int64): Number of days of inactivity before the rule applies.
* `name` (string): Key Lifecycle Rule name


---

## List Key Lifecycle Rules

```
files_sdk.key_lifecycle_rule.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .


---

## Show Key Lifecycle Rule

```
files_sdk.key_lifecycle_rule.find(id)
```

### Parameters

* `id` (int64): Required - Key Lifecycle Rule ID.


---

## Create Key Lifecycle Rule

```
files_sdk.key_lifecycle_rule.create({
  "key_type": "gpg",
  "inactivity_days": 12,
  "name": "inactive gpg keys"
})
```

### Parameters

* `key_type` (string): Key type for which the rule will apply (gpg or ssh).
* `inactivity_days` (int64): Number of days of inactivity before the rule applies.
* `name` (string): Key Lifecycle Rule name


---

## Update Key Lifecycle Rule

```
files_sdk.key_lifecycle_rule.update(id, {
  "key_type": "gpg",
  "inactivity_days": 12,
  "name": "inactive gpg keys"
})
```

### Parameters

* `id` (int64): Required - Key Lifecycle Rule ID.
* `key_type` (string): Key type for which the rule will apply (gpg or ssh).
* `inactivity_days` (int64): Number of days of inactivity before the rule applies.
* `name` (string): Key Lifecycle Rule name


---

## Delete Key Lifecycle Rule

```
files_sdk.key_lifecycle_rule.delete(id)
```

### Parameters

* `id` (int64): Required - Key Lifecycle Rule ID.


---

## Update Key Lifecycle Rule

```
key_lifecycle_rule = files_sdk.key_lifecycle_rule.find(id)
key_lifecycle_rule.update({
  "key_type": "gpg",
  "inactivity_days": 12,
  "name": "inactive gpg keys"
})
```

### Parameters

* `id` (int64): Required - Key Lifecycle Rule ID.
* `key_type` (string): Key type for which the rule will apply (gpg or ssh).
* `inactivity_days` (int64): Number of days of inactivity before the rule applies.
* `name` (string): Key Lifecycle Rule name


---

## Delete Key Lifecycle Rule

```
key_lifecycle_rule = files_sdk.key_lifecycle_rule.find(id)
key_lifecycle_rule.delete()
```

### Parameters

* `id` (int64): Required - Key Lifecycle Rule ID.
