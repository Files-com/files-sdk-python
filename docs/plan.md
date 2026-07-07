# Plan

## Example Plan Object

```
{
  "id": 1,
  "activation_cost": "10.0",
  "addon_description": "FTP/SFTP/WebDAV addon",
  "annually": "2988.0",
  "annually_addon": "2988.0",
  "automation_and_sync_flow_overage_cost": "25.0",
  "automation_and_sync_flows": 2,
  "child_sites": 1,
  "currency": "USD",
  "dedicated_ip": True,
  "dedicated_ips": 1,
  "domain_count": 1,
  "feature_bundle_eca": True,
  "feature_bundle_power": True,
  "feature_bundle_premier": True,
  "feature_bundle_starter": True,
  "monthly": "249.0",
  "monthly_addon": "249.0",
  "name": "Power",
  "outbound_connections": 1,
  "preview_page_limit": 100,
  "regions_included": 2,
  "remote_sync_interval": 1,
  "signup_page_marketing_text": "example",
  "system_users": 1,
  "staging_sites": 1,
  "transformation_and_ai_credit_overage_cost_per_million": "0.1",
  "transformation_and_ai_credits": 1,
  "trial_days": 30,
  "user_cost": "5.0",
  "usage_cost": "0.1",
  "usage_included": 1,
  "users": 1
}
```

* `id` (int64): Plan ID
* `activation_cost` (decimal): Activation cost (upfront)
* `addon_description` (string): Description of add on charges
* `annually` (string): Price annually
* `annually_addon` (string): Addons price annually
* `automation_and_sync_flow_overage_cost` (string): Cost per additional automation and sync flow
* `automation_and_sync_flows` (int64): Number of automation and sync flows included. 0 means unlimited.
* `child_sites` (int64): Number of child sites available
* `currency` (string): Currency
* `dedicated_ip` (boolean): Offers dedicated ip?
* `dedicated_ips` (int64): Number of dedicated IPs
* `domain_count` (int64): Number of custom domains
* `feature_bundle_eca` (boolean): Does this plan include the ECA feature bundle?
* `feature_bundle_power` (boolean): Does this plan include the Power feature bundle?
* `feature_bundle_premier` (boolean): Does this plan include the Enterprise feature bundle?
* `feature_bundle_starter` (boolean): Does this plan include the Starter feature bundle?
* `monthly` (string): Price monthly
* `monthly_addon` (string): Addons price monthly
* `name` (string): Plan name
* `outbound_connections` (int64): Number of outbound connections
* `preview_page_limit` (int64): Number of previews available
* `regions_included` (int64): Number of storage regions included
* `remote_sync_interval` (int64): Number of minutes between remote sync
* `signup_page_marketing_text` (string): Additional marketing text to show on signup page
* `system_users` (int64): # of System Users included.  0 means that system users are included in the normal user quota.
* `staging_sites` (int64): Number of child sites available
* `transformation_and_ai_credit_overage_cost_per_million` (string): Cost per million additional transformation and AI credits
* `transformation_and_ai_credits` (int64): Transformation and AI credits included
* `trial_days` (int64): # of trial days included. Values of 0 or less mean no trial is offered.
* `user_cost` (string): Cost per additional user
* `usage_cost` (string): Usage cost per GB of overage
* `usage_included` (int64): Usage included per month, in GB
* `users` (int64): # of users included.  0 or -1 mean unlimited.


---

## List Plans

```
files_sdk.plan.list({
  "currency": "USD"
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `currency` (string): Currency.


---

## Create an export CSV of Plan resources

```
files_sdk.plan.create_export({
  "currency": ""
})
```

### Parameters

* `currency` (string): Currency.
