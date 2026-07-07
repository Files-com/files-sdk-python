# EmailPreference

## Example EmailPreference Object

```
{
  "email": "john.doe@files.com",
  "notifications": [
    {
      "id": 1,
      "path": "example",
      "send_interval": "fifteen_minutes",
      "unsubscribed": True
    }
  ],
  "bundle_notifications": [
    {
      "id": 1,
      "bundle_code": "example",
      "unsubscribed": True
    }
  ],
  "receive_admin_alerts": True,
  "notify_on_all_site_warnings": True,
  "notify_on_all_sso_failures": True,
  "notify_on_all_user_security_events": True,
  "notify_on_all_pending_work_failures": True,
  "notify_on_all_siem_http_destination_failures": True,
  "notify_on_all_sync_failures": True,
  "notify_on_all_automation_failures": True,
  "notify_on_all_expectation_failures": True,
  "receive_marketing_mail": True,
  "receive_transactional_mail": True
}
```

* `email` (email): Email address
* `notifications` (array(object)): A list of notifications
* `bundle_notifications` (array(object)): A list of bundle notifications
* `receive_admin_alerts` (boolean): Deprecated. Use granular admin email preferences instead.
* `notify_on_all_site_warnings` (boolean): Receive site warnings?
* `notify_on_all_sso_failures` (boolean): Receive sso/scim/ldap configuration/sync failures?
* `notify_on_all_user_security_events` (boolean): Receive user security events?
* `notify_on_all_pending_work_failures` (boolean): Receive pending work failures?
* `notify_on_all_siem_http_destination_failures` (boolean): Receive siem failures?
* `notify_on_all_sync_failures` (boolean): Receive sync failures?
* `notify_on_all_automation_failures` (boolean): Receive automation failures?
* `notify_on_all_expectation_failures` (boolean): Receive expectation failures and misses?
* `receive_marketing_mail` (boolean): Receive marketing mail?
* `receive_transactional_mail` (boolean): Receive transactional (service-related) mail?


---

## Show Email Preference

```
files_sdk.email_preference.get(token)
```

### Parameters

* `token` (string): Required - Email preferences token.


---

## Update Email Preference

```
files_sdk.email_preference.update(token, {
  "user[receive_admin_alerts]": False,
  "user[notify_on_all_site_warnings]": False,
  "user[notify_on_all_sso_failures]": False,
  "user[notify_on_all_user_security_events]": False,
  "user[notify_on_all_pending_work_failures]": False,
  "user[notify_on_all_siem_http_destination_failures]": False,
  "user[notify_on_all_sync_failures]": False,
  "user[notify_on_all_automation_failures]": False,
  "user[notify_on_all_expectation_failures]": False,
  "user[unsubscribe_marketing]": False,
  "user[unsubscribe_transactional]": False,
  "user[unsubscribe]": False,
  "user[notifications][send_interval]": "hour"
})
```

### Parameters

* `token` (string): Required - Email preferences token.
* `user[receive_admin_alerts]` (boolean): 
* `user[notify_on_all_site_warnings]` (boolean): 
* `user[notify_on_all_sso_failures]` (boolean): 
* `user[notify_on_all_user_security_events]` (boolean): 
* `user[notify_on_all_pending_work_failures]` (boolean): 
* `user[notify_on_all_siem_http_destination_failures]` (boolean): 
* `user[notify_on_all_sync_failures]` (boolean): 
* `user[notify_on_all_automation_failures]` (boolean): 
* `user[notify_on_all_expectation_failures]` (boolean): 
* `user[unsubscribe_marketing]` (boolean): 
* `user[unsubscribe_transactional]` (boolean): 
* `user[unsubscribe]` (boolean): 
* `user[notifications][id]` (array(int64)): 
* `user[notifications][group]` (array(boolean)): 
* `user[notifications][send_interval]` (array(string)): 
* `user[notifications][unsubscribe]` (array(boolean)): 
* `user[bundle_notifications][id]` (array(int64)): 
* `user[bundle_notifications][unsubscribe]` (array(boolean)): 
