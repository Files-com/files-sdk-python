# Invoice

## Example Invoice Object

```
{
  "id": 1,
  "amount": 1.0,
  "balance": 1.0,
  "created_at": "2000-01-01T01:00:00Z",
  "currency": "USD",
  "download_uri": "https://url...",
  "invoice_line_items": [
    {
      "id": 1,
      "amount": 1.0,
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
  ],
  "method": "paypal",
  "payment_line_items": [
    {
      "amount": 1.0,
      "created_at": "2000-01-01T01:00:00Z",
      "invoice_id": 1,
      "payment_id": 1
    }
  ],
  "payment_reversed_at": "2000-01-01T01:00:00Z",
  "payment_type": "example",
  "site_name": "My Site",
  "type": "invoice"
}
```

* `id` (int64): Line item Id
* `amount` (double): Line item amount
* `balance` (double): Line item balance
* `created_at` (date-time): Line item created at
* `currency` (string): Line item currency
* `download_uri` (string): Line item download uri
* `invoice_line_items` (array(object)): Associated invoice line items
* `method` (string): Line item payment method
* `payment_line_items` (array(object)): Associated payment line items
* `payment_reversed_at` (date-time): Date/time payment was reversed if applicable
* `payment_type` (string): Type of payment if applicable
* `site_name` (string): Site name this line item is for
* `type` (string): Type of line item, either payment or invoice


---

## List Invoices

```
files_sdk.invoice.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show Invoice

```
files_sdk.invoice.find(id)
```

### Parameters

* `id` (int64): Required - Invoice ID.
