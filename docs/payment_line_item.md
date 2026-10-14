# PaymentLineItem

## Example PaymentLineItem Object

The API sends each `PaymentLineItem` record as JSON, such as:

```json
{
  "amount": "1.0",
  "created_at": "2000-01-01T01:00:00Z",
  "invoice_id": 1,
  "payment_id": 1
}
```

* `amount` (decimal): Payment line item amount
* `created_at` (date-time): Payment line item created at date/time
* `invoice_id` (int64): Invoice ID
* `payment_id` (int64): Payment ID
