# Account

## Example Account Object

```
{
  "name": "account",
  "address": "123 Main St",
  "address_2": "Window 1",
  "card_number": "xxxxxxxxxxxx1234",
  "card_type": "Visa",
  "city": "New York",
  "company_name": "Action Verb",
  "country": "US",
  "created_at": "2000-01-01T01:00:00Z",
  "currency": "USD",
  "email": "john.doe@files.com",
  "phone_number": "555-555-5555",
  "processor_type": "Credit Card",
  "state": "NY",
  "zip": "00000",
  "billing_frequency": 1
}
```

* `name` (string): Account name
* `address` (string): Account address
* `address_2` (string): Account address 2
* `card_number` (string): Account payment card number
* `card_type` (string): Account payment card type
* `city` (string): Account city
* `company_name` (string): Account company name
* `country` (string): Account country
* `created_at` (date-time): Account creation date/time
* `currency` (string): Account preferred currency
* `email` (email): Account email address
* `phone_number` (string): Account phone number
* `processor_type` (string): Type of billing processor.  Can be PayPal, Credit Card, or Manual
* `state` (string): Account state
* `zip` (string): Account zipcode
* `billing_frequency` (int64): Number of usage periods billed at once.  This value will either be 12 representing an annual account of 12 usage periods or 1 representing a monthly account.
* `expiration_year` (string): Expiration year(4 digits).
* `expiration_month` (string): Expiration month(2 digits).
* `start_year` (string): Required for some cards(Switch / Solo).
* `start_month` (string): Required for some cards(Switch / Solo).
* `cvv` (string): 3 digit code on the back of the card.
* `paypal_token` (string): Token for paying with paypal.
* `paypal_payer_id` (string): Paypal payer ID for paying with paypal.
* `plan_id` (int64): Plan ID to switch to immediately.
* `create_account` (boolean): Create account without immediately charging the customer.  (i.e. let the trial complete first.)


---

## Show current (billing) account information

```
files_sdk.account.get()
```


---

## Upgrade current site to paid

```
files_sdk.account.create({
  "name": "account",
  "company_name": "Action Verb",
  "address": "123 Main St",
  "address_2": "Window 1",
  "city": "New York",
  "state": "NY",
  "zip": "00000",
  "country": "US",
  "email": "john.doe@files.com",
  "phone_number": "555-555-5555",
  "card_number": "xxxxxxxxxxxx1234",
  "card_type": "Visa",
  "plan_id": 1,
  "billing_frequency": 1,
  "currency": "USD",
  "create_account": False
})
```

### Parameters

* `name` (string): Internal name.
* `company_name` (string): Company name.
* `address` (string): Address line 1.
* `address_2` (string): Address line 2.
* `city` (string): City.
* `state` (string): State.
* `zip` (string): Zipcode.
* `country` (string): Country.
* `email` (string): Email.
* `phone_number` (string): Primary phone number.
* `card_number` (string): Credit card number.
* `card_type` (string): Credit card type.  Can be visa, master, maestro, solo, switch, american_express, or discover.
* `expiration_year` (string): Expiration year(4 digits).
* `expiration_month` (string): Expiration month(2 digits).
* `start_year` (string): Required for some cards(Switch / Solo).
* `start_month` (string): Required for some cards(Switch / Solo).
* `cvv` (string): 3 digit code on the back of the card.
* `paypal_token` (string): Token for paying with paypal.
* `paypal_payer_id` (string): Paypal payer ID for paying with paypal.
* `plan_id` (int64): Plan ID to switch to immediately.
* `billing_frequency` (int64): The billing frequency, in months, for the site.  Must be 1 (monthly) or 12 (annual).
* `currency` (string): Preferred currency for this account.
* `create_account` (boolean): Create account without immediately charging the customer.  (i.e. let the trial complete first.)


---

## Update account (billing) information

```
files_sdk.account.update({
  "name": "account",
  "company_name": "Action Verb",
  "address": "123 Main St",
  "address_2": "Window 1",
  "city": "New York",
  "state": "NY",
  "zip": "00000",
  "country": "US",
  "email": "john.doe@files.com",
  "phone_number": "555-555-5555",
  "card_number": "xxxxxxxxxxxx1234",
  "card_type": "Visa"
})
```

### Parameters

* `name` (string): Internal name.
* `company_name` (string): Company name.
* `address` (string): Address line 1.
* `address_2` (string): Address line 2.
* `city` (string): City.
* `state` (string): State.
* `zip` (string): Zipcode.
* `country` (string): Country.
* `email` (string): Email.
* `phone_number` (string): Primary phone number.
* `card_number` (string): Credit card number.
* `card_type` (string): Credit card type.  Can be visa, master, maestro, solo, switch, american_express, or discover.
* `expiration_year` (string): Expiration year(4 digits).
* `expiration_month` (string): Expiration month(2 digits).
* `start_year` (string): Required for some cards(Switch / Solo).
* `start_month` (string): Required for some cards(Switch / Solo).
* `cvv` (string): 3 digit code on the back of the card.
* `paypal_token` (string): Token for paying with paypal.
* `paypal_payer_id` (string): Paypal payer ID for paying with paypal.
