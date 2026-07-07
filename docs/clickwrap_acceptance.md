# ClickwrapAcceptance

## Example ClickwrapAcceptance Object

```
{
  "id": 1,
  "clickwrap_id": 1,
  "created_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Clickwrap Acceptance ID
* `clickwrap_id` (int64): Clickwrap ID
* `created_at` (date-time): Acceptance timestamp


---

## Create Clickwrap Acceptance

```
files_sdk.clickwrap_acceptance.create({
  "clickwrap_id": 1
})
```

### Parameters

* `clickwrap_id` (int64): Required - 
