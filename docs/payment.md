# Payment

## Example Payment Object

```
{
  "id": 1,
  "amount": 1.0,
  "balance": 1.0,
  "created_at": "2000-01-01T01:00:00Z",
  "currency": "USD",
  "download_uri": "https://url...",
  "invoice_line_items": {
    "amount": 1.0,
    "created_at": "2000-01-01T01:00:00Z",
    "description": "Service from 2019-01-01 through 2019-12-31",
    "type": "invoice",
    "service_end_at": "2000-01-01T01:00:00Z",
    "service_start_at": "2000-01-01T01:00:00Z",
    "updated_at": "2000-01-01T01:00:00Z",
    "plan": "Enterprise",
    "site": "My site"
  },
  "method": "paypal",
  "payment_line_items": {
    "amount": 1.0,
    "created_at": "2000-01-01T01:00:00Z",
    "invoice_id": 1,
    "payment_id": 1,
    "updated_at": "2000-01-01T01:00:00Z"
  },
  "payment_reversed_at": "2000-01-01T01:00:00Z",
  "payment_type": "",
  "site_name": "My Site",
  "type": "invoice",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Line item Id
* `amount` (double): Line item amount
* `balance` (double): Line item balance
* `created_at` (date-time): Line item created at
* `currency` (string): Line item currency
* `download_uri` (string): Line item download uri
* `invoice_line_items`: Associated invoice line items
* `method` (string): Line item payment method
* `payment_line_items`: Associated payment line items
* `payment_reversed_at` (date-time): Date/time payment was reversed if applicable
* `payment_type` (string): Type of payment if applicable
* `site_name` (string): Site name this line item is for
* `type` (string): Type of line item, either payment or invoice
* `updated_at` (date-time): Line item updated at


---

## List Payments

```
files_sdk.payment.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show Payment

```
files_sdk.payment.find(id)
```

### Parameters

* `id` (int64): Required - Payment ID.
