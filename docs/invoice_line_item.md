# InvoiceLineItem

## Example InvoiceLineItem Object

```
{
  "id": 1,
  "amount": 1.0,
  "created_at": "2000-01-01T01:00:00Z",
  "description": "Service from 2019-01-01 through 2019-12-31",
  "type": "invoice",
  "service_end_at": "2000-01-01T01:00:00Z",
  "service_start_at": "2000-01-01T01:00:00Z",
  "plan": "Premier",
  "site": "My site"
}
```

* `id` (int64): Invoice Line item Id
* `amount` (double): Invoice line item amount
* `created_at` (date-time): Invoice line item created at date/time
* `description` (string): Invoice line item description
* `type` (string): Invoice line item type
* `service_end_at` (date-time): Invoice line item service end date/time
* `service_start_at` (date-time): Invoice line item service start date/time
* `plan` (string): Plan name
* `site` (string): Site name
