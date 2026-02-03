# InvoiceLineItem

## Example InvoiceLineItem Object

```
{
  "id": 1,
  "amount": "1.0",
  "created_at": "2000-01-01T01:00:00Z",
  "description": "Service from 2019-01-01 through 2019-12-31",
  "type": "invoice",
  "service_end_at": "2000-01-01T01:00:00Z",
  "service_start_at": "2000-01-01T01:00:00Z",
  "plan": "Premier",
  "site": "My site",
  "prepaid_bytes": 1,
  "prepaid_bytes_expire_at": "2000-01-01T01:00:00Z",
  "prepaid_bytes_used": 1,
  "prepaid_bytes_available": 1
}
```

* `id` (int64): Invoice Line item Id
* `amount` (decimal): Invoice line item amount
* `created_at` (date-time): Invoice line item created at date/time
* `description` (string): Invoice line item description
* `type` (string): Invoice line item type
* `service_end_at` (date-time): Invoice line item service end date/time
* `service_start_at` (date-time): Invoice line item service start date/time
* `plan` (string): Plan name
* `site` (string): Site name
* `prepaid_bytes` (int64): Prepaid bytes purchased for this invoice line item
* `prepaid_bytes_expire_at` (date-time): When the prepaid bytes expire
* `prepaid_bytes_used` (int64): Total prepaid bytes used for this invoice line item
* `prepaid_bytes_available` (int64): Available prepaid bytes for this invoice line item
