

---

## retry Action Webhook Failure

```
files_sdk.action_webhook_failure.retry(id)
```

### Parameters

* `id` (int64): Required - Action Webhook Failure ID.


---

## retry Action Webhook Failure

```
action_webhook_failure = files_sdk.action_webhook_failure.list_for(path).first

action_webhook_failure.retry()
```

### Parameters

* `id` (int64): Required - Action Webhook Failure ID.
