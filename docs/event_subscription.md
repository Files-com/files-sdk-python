# EventSubscription

## Example EventSubscription Object

```
{
  "id": 1,
  "event_channel_id": 1,
  "workspace_id": 1,
  "apply_to_all_workspaces": True,
  "name": "example",
  "subject": "example",
  "message": "example",
  "message_only": True,
  "enabled": True,
  "event_types": [
    "sync_run.failure.v1"
  ],
  "filter": {
    "payload.sync_name": {
      "prefix": "Nightly"
    },
    "payload.event_errors": {
      "exists": True
    }
  },
  "delivery_policy": "example",
  "event_target_ids": [
    1
  ],
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Event Subscription ID
* `event_channel_id` (int64): Event Channel ID
* `workspace_id` (int64): Workspace ID. 0 means the default workspace or site-wide.
* `apply_to_all_workspaces` (boolean): If true, this default-workspace subscription applies to events from all workspaces.
* `name` (string): Event Subscription name.
* `subject` (string): Custom subject line to use for notification emails.
* `message` (string): Custom message to include in notification emails.
* `message_only` (boolean): If true, notification email bodies contain only the custom message, omitting event details and the review button. Requires a custom message, defaults to false, and does not affect non-email targets.
* `enabled` (boolean): Whether this Event Subscription can dispatch events.
* `event_types` (array(string)): Event type strings matched by this subscription. Blank means all event types. Valid values: `automation_run.canceled.v1`, `automation_run.failure.v1`, `automation_run.failure_will_retry.v1`, `automation_run.partial_failure.v1`, `automation_run.partial_failure_will_retry.v1`, `automation_run.skipped.v1`, `automation_run.success.v1`, `expectation_evaluation.invalid.v1`, `expectation_evaluation.late.v1`, `expectation_evaluation.missing.v1`, `expectation_evaluation.success.v1`, `expectation_incident.acknowledged.v1`, `expectation_incident.open.v1`, `expectation_incident.resolved.v1`, `expectation_incident.snoozed.v1`, `external_event.client_log.failure.v1`, `external_event.client_log.partial_failure.v1`, `external_event.client_log.skipped.v1`, `external_event.client_log.success.v1`, `pending_work_event.failure.v1`, `pending_work_event.partial_failure.v1`, `pending_work_event.skipped.v1`, `pending_work_event.success.v1`, `siem_http_destination_event.failure.v1`, `siem_http_destination_event.partial_failure.v1`, `siem_http_destination_event.skipped.v1`, `siem_http_destination_event.success.v1`, `sso_event.ldap_login.failure.v1`, `sso_event.ldap_login.partial_failure.v1`, `sso_event.ldap_login.skipped.v1`, `sso_event.ldap_login.success.v1`, `sso_event.ldap_sync.failure.v1`, `sso_event.ldap_sync.partial_failure.v1`, `sso_event.ldap_sync.skipped.v1`, `sso_event.ldap_sync.success.v1`, `sso_event.saml_login.failure.v1`, `sso_event.saml_login.partial_failure.v1`, `sso_event.saml_login.skipped.v1`, `sso_event.saml_login.success.v1`, `sync_run.failure.v1`, `sync_run.partial_failure.v1`, `sync_run.skipped.v1`, `sync_run.success.v1`, `user_security_event.lockout.v1`
* `filter` (object): Conditions on event fields that an event must meet to be delivered, keyed by dot-notation field path. All conditions must match.
* `delivery_policy` (object): Event Subscription delivery policy.
* `event_target_ids` (array(int64)): Event Target IDs this subscription sends to.
* `created_at` (date-time): Event Subscription create date/time.
* `updated_at` (date-time): Event Subscription update date/time.


---

## List Event Subscriptions

```
files_sdk.event_subscription.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `enabled`, `event_channel_id` or `workspace_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `enabled`, `event_channel_id` or `workspace_id`. Valid field combinations are `[ enabled, event_channel_id ]`, `[ workspace_id, enabled ]` or `[ workspace_id, enabled, event_channel_id ]`.


---

## Show Event Subscription

```
files_sdk.event_subscription.find(id)
```

### Parameters

* `id` (int64): Required - Event Subscription ID.


---

## Create Event Subscription

```
files_sdk.event_subscription.create({
  "event_channel_id": 1,
  "workspace_id": 1,
  "apply_to_all_workspaces": True,
  "name": "example",
  "subject": "example",
  "message": "example",
  "message_only": True,
  "enabled": True,
  "event_types": ["sync_run.failure.v1"],
  "delivery_policy": "example",
  "event_target_ids": [1]
})
```

### Parameters

* `event_channel_id` (int64): Event Channel ID
* `workspace_id` (int64): Workspace ID. 0 means the default workspace or site-wide.
* `apply_to_all_workspaces` (boolean): If true, this default-workspace subscription applies to events from all workspaces.
* `name` (string): Required - Event Subscription name.
* `subject` (string): Custom subject line to use for notification emails.
* `message` (string): Custom message to include in notification emails.
* `message_only` (boolean): If true, notification email bodies contain only the custom message, omitting event details and the review button. Requires a custom message, defaults to false, and does not affect non-email targets.
* `enabled` (boolean): Whether this Event Subscription can dispatch events.
* `event_types` (array(string)): Event type strings matched by this subscription. Blank means all event types. Valid values: `automation_run.canceled.v1`, `automation_run.failure.v1`, `automation_run.failure_will_retry.v1`, `automation_run.partial_failure.v1`, `automation_run.partial_failure_will_retry.v1`, `automation_run.skipped.v1`, `automation_run.success.v1`, `expectation_evaluation.invalid.v1`, `expectation_evaluation.late.v1`, `expectation_evaluation.missing.v1`, `expectation_evaluation.success.v1`, `expectation_incident.acknowledged.v1`, `expectation_incident.open.v1`, `expectation_incident.resolved.v1`, `expectation_incident.snoozed.v1`, `external_event.client_log.failure.v1`, `external_event.client_log.partial_failure.v1`, `external_event.client_log.skipped.v1`, `external_event.client_log.success.v1`, `pending_work_event.failure.v1`, `pending_work_event.partial_failure.v1`, `pending_work_event.skipped.v1`, `pending_work_event.success.v1`, `siem_http_destination_event.failure.v1`, `siem_http_destination_event.partial_failure.v1`, `siem_http_destination_event.skipped.v1`, `siem_http_destination_event.success.v1`, `sso_event.ldap_login.failure.v1`, `sso_event.ldap_login.partial_failure.v1`, `sso_event.ldap_login.skipped.v1`, `sso_event.ldap_login.success.v1`, `sso_event.ldap_sync.failure.v1`, `sso_event.ldap_sync.partial_failure.v1`, `sso_event.ldap_sync.skipped.v1`, `sso_event.ldap_sync.success.v1`, `sso_event.saml_login.failure.v1`, `sso_event.saml_login.partial_failure.v1`, `sso_event.saml_login.skipped.v1`, `sso_event.saml_login.success.v1`, `sync_run.failure.v1`, `sync_run.partial_failure.v1`, `sync_run.skipped.v1`, `sync_run.success.v1`, `user_security_event.lockout.v1`
* `filter` (object): Conditions on event fields that an event must meet to be delivered, keyed by dot-notation field path. All conditions must match.
* `delivery_policy` (object): Event Subscription delivery policy.
* `event_target_ids` (array(int64)): Event Target IDs this subscription sends to.


---

## Update Event Subscription

```
files_sdk.event_subscription.update(id, {
  "event_channel_id": 1,
  "workspace_id": 1,
  "apply_to_all_workspaces": True,
  "name": "example",
  "subject": "example",
  "message": "example",
  "message_only": True,
  "enabled": True,
  "event_types": ["sync_run.failure.v1"],
  "delivery_policy": "example",
  "event_target_ids": [1]
})
```

### Parameters

* `id` (int64): Required - Event Subscription ID.
* `event_channel_id` (int64): Event Channel ID
* `workspace_id` (int64): Workspace ID. 0 means the default workspace or site-wide.
* `apply_to_all_workspaces` (boolean): If true, this default-workspace subscription applies to events from all workspaces.
* `name` (string): Event Subscription name.
* `subject` (string): Custom subject line to use for notification emails.
* `message` (string): Custom message to include in notification emails.
* `message_only` (boolean): If true, notification email bodies contain only the custom message, omitting event details and the review button. Requires a custom message, defaults to false, and does not affect non-email targets.
* `enabled` (boolean): Whether this Event Subscription can dispatch events.
* `event_types` (array(string)): Event type strings matched by this subscription. Blank means all event types. Valid values: `automation_run.canceled.v1`, `automation_run.failure.v1`, `automation_run.failure_will_retry.v1`, `automation_run.partial_failure.v1`, `automation_run.partial_failure_will_retry.v1`, `automation_run.skipped.v1`, `automation_run.success.v1`, `expectation_evaluation.invalid.v1`, `expectation_evaluation.late.v1`, `expectation_evaluation.missing.v1`, `expectation_evaluation.success.v1`, `expectation_incident.acknowledged.v1`, `expectation_incident.open.v1`, `expectation_incident.resolved.v1`, `expectation_incident.snoozed.v1`, `external_event.client_log.failure.v1`, `external_event.client_log.partial_failure.v1`, `external_event.client_log.skipped.v1`, `external_event.client_log.success.v1`, `pending_work_event.failure.v1`, `pending_work_event.partial_failure.v1`, `pending_work_event.skipped.v1`, `pending_work_event.success.v1`, `siem_http_destination_event.failure.v1`, `siem_http_destination_event.partial_failure.v1`, `siem_http_destination_event.skipped.v1`, `siem_http_destination_event.success.v1`, `sso_event.ldap_login.failure.v1`, `sso_event.ldap_login.partial_failure.v1`, `sso_event.ldap_login.skipped.v1`, `sso_event.ldap_login.success.v1`, `sso_event.ldap_sync.failure.v1`, `sso_event.ldap_sync.partial_failure.v1`, `sso_event.ldap_sync.skipped.v1`, `sso_event.ldap_sync.success.v1`, `sso_event.saml_login.failure.v1`, `sso_event.saml_login.partial_failure.v1`, `sso_event.saml_login.skipped.v1`, `sso_event.saml_login.success.v1`, `sync_run.failure.v1`, `sync_run.partial_failure.v1`, `sync_run.skipped.v1`, `sync_run.success.v1`, `user_security_event.lockout.v1`
* `filter` (object): Conditions on event fields that an event must meet to be delivered, keyed by dot-notation field path. All conditions must match.
* `delivery_policy` (object): Event Subscription delivery policy.
* `event_target_ids` (array(int64)): Event Target IDs this subscription sends to.


---

## Delete Event Subscription

```
files_sdk.event_subscription.delete(id)
```

### Parameters

* `id` (int64): Required - Event Subscription ID.


---

## Update Event Subscription

```
event_subscription = files_sdk.event_subscription.find(id)
event_subscription.update({
  "event_channel_id": 1,
  "workspace_id": 1,
  "apply_to_all_workspaces": True,
  "name": "example",
  "subject": "example",
  "message": "example",
  "message_only": True,
  "enabled": True,
  "event_types": ["sync_run.failure.v1"],
  "delivery_policy": "example",
  "event_target_ids": [1]
})
```

### Parameters

* `id` (int64): Required - Event Subscription ID.
* `event_channel_id` (int64): Event Channel ID
* `workspace_id` (int64): Workspace ID. 0 means the default workspace or site-wide.
* `apply_to_all_workspaces` (boolean): If true, this default-workspace subscription applies to events from all workspaces.
* `name` (string): Event Subscription name.
* `subject` (string): Custom subject line to use for notification emails.
* `message` (string): Custom message to include in notification emails.
* `message_only` (boolean): If true, notification email bodies contain only the custom message, omitting event details and the review button. Requires a custom message, defaults to false, and does not affect non-email targets.
* `enabled` (boolean): Whether this Event Subscription can dispatch events.
* `event_types` (array(string)): Event type strings matched by this subscription. Blank means all event types. Valid values: `automation_run.canceled.v1`, `automation_run.failure.v1`, `automation_run.failure_will_retry.v1`, `automation_run.partial_failure.v1`, `automation_run.partial_failure_will_retry.v1`, `automation_run.skipped.v1`, `automation_run.success.v1`, `expectation_evaluation.invalid.v1`, `expectation_evaluation.late.v1`, `expectation_evaluation.missing.v1`, `expectation_evaluation.success.v1`, `expectation_incident.acknowledged.v1`, `expectation_incident.open.v1`, `expectation_incident.resolved.v1`, `expectation_incident.snoozed.v1`, `external_event.client_log.failure.v1`, `external_event.client_log.partial_failure.v1`, `external_event.client_log.skipped.v1`, `external_event.client_log.success.v1`, `pending_work_event.failure.v1`, `pending_work_event.partial_failure.v1`, `pending_work_event.skipped.v1`, `pending_work_event.success.v1`, `siem_http_destination_event.failure.v1`, `siem_http_destination_event.partial_failure.v1`, `siem_http_destination_event.skipped.v1`, `siem_http_destination_event.success.v1`, `sso_event.ldap_login.failure.v1`, `sso_event.ldap_login.partial_failure.v1`, `sso_event.ldap_login.skipped.v1`, `sso_event.ldap_login.success.v1`, `sso_event.ldap_sync.failure.v1`, `sso_event.ldap_sync.partial_failure.v1`, `sso_event.ldap_sync.skipped.v1`, `sso_event.ldap_sync.success.v1`, `sso_event.saml_login.failure.v1`, `sso_event.saml_login.partial_failure.v1`, `sso_event.saml_login.skipped.v1`, `sso_event.saml_login.success.v1`, `sync_run.failure.v1`, `sync_run.partial_failure.v1`, `sync_run.skipped.v1`, `sync_run.success.v1`, `user_security_event.lockout.v1`
* `filter` (object): Conditions on event fields that an event must meet to be delivered, keyed by dot-notation field path. All conditions must match.
* `delivery_policy` (object): Event Subscription delivery policy.
* `event_target_ids` (array(int64)): Event Target IDs this subscription sends to.


---

## Delete Event Subscription

```
event_subscription = files_sdk.event_subscription.find(id)
event_subscription.delete()
```

### Parameters

* `id` (int64): Required - Event Subscription ID.
