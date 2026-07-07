# Lead

## Example Lead Object

```
{
  "id": 1,
  "code": "abc123",
  "name": "account",
  "address": "123 Main St",
  "address_2": "Window 1",
  "city": "New York",
  "company_name": "Action Verb",
  "contact_name": "John Doe",
  "country": "US",
  "currency": "USD",
  "email": "john.doe@files.com",
  "language": "en",
  "phone_number": "555-555-5555",
  "state": "NY",
  "zip": "00000",
  "lead_level": "mql",
  "signup_page_split_test_group": "control"
}
```

* `id` (int64): Lead ID
* `code` (string): Lead Cookie Code
* `name` (string): Lead name
* `address` (string): Lead address
* `address_2` (string): Lead address 2
* `city` (string): Lead city
* `company_name` (string): Lead company name
* `contact_name` (string): Contact name at the company
* `country` (string): Lead country
* `currency` (string): Lead preferred currency
* `email` (string): Lead email address
* `language` (string): Lead preferred language
* `phone_number` (string): Lead phone number
* `state` (string): Lead state
* `zip` (string): Lead zipcode
* `lead_level` (string): Quality score of the lead
* `signup_page_split_test_group` (string): Signup page split test group
* `recaptcha_token` (string): 
* `form_name` (string): Signup form name
* `lead_source` (string): Source of the lead
* `opportunity_comment` (string): Opportunity comment
* `opportunity_type` (string): Type of opportunity to create
* `gclid` (string): Google Adwords Click ID
* `original_brand` (string): Brand: `files`, `exavault` or `mover`
* `utm_campaign` (string): Marketing tracking - campaign
* `utm_content` (string): Marketing tracking - content
* `utm_domain` (string): Marketing tracking - domain
* `utm_medium` (string): Marketing tracking - medium
* `utm_source` (string): Marketing tracking - source
* `utm_term` (string): Marketing tracking - term
* `time_zone` (string): Time zone, as returned by Javascript
* `time_zone_offset` (int64): Time zone offset (integer from -12 to 12)


---

## Create Lead

```
files_sdk.lead.create({
  "name": "account",
  "address": "123 Main St",
  "address_2": "Window 1",
  "city": "New York",
  "contact_name": "John Doe",
  "currency": "USD",
  "email": "john.doe@files.com",
  "language": "en",
  "phone_number": "555-555-5555",
  "state": "NY",
  "zip": "00000",
  "time_zone_offset": 1
})
```

### Parameters

* `recaptcha_token` (string): 
* `name` (string): Lead name
* `address` (string): Lead address
* `address_2` (string): Lead address 2
* `city` (string): Lead city
* `contact_name` (string): Contact name at the company
* `currency` (string): Lead preferred currency
* `email` (string): Lead email address
* `language` (string): Lead preferred language
* `phone_number` (string): Lead phone number
* `state` (string): Lead state
* `zip` (string): Lead zipcode
* `form_name` (string): Signup form name
* `lead_source` (string): Source of the lead
* `opportunity_comment` (string): Opportunity comment
* `opportunity_type` (string): Type of opportunity to create
* `gclid` (string): Google Adwords Click ID
* `original_brand` (string): Brand: `files`, `exavault` or `mover`
* `utm_campaign` (string): Marketing tracking - campaign
* `utm_content` (string): Marketing tracking - content
* `utm_domain` (string): Marketing tracking - domain
* `utm_medium` (string): Marketing tracking - medium
* `utm_source` (string): Marketing tracking - source
* `utm_term` (string): Marketing tracking - term
* `time_zone` (string): Time zone, as returned by Javascript
* `time_zone_offset` (int64): Time zone offset (integer from -12 to 12)


---

## Update Lead

```
files_sdk.lead.update(code, {
  "name": "account",
  "address": "123 Main St",
  "address_2": "Window 1",
  "city": "New York",
  "contact_name": "John Doe",
  "currency": "USD",
  "email": "john.doe@files.com",
  "language": "en",
  "phone_number": "555-555-5555",
  "state": "NY",
  "zip": "00000",
  "time_zone_offset": 1
})
```

### Parameters

* `code` (string): Required - Lead lookup code.
* `recaptcha_token` (string): 
* `name` (string): Lead name
* `address` (string): Lead address
* `address_2` (string): Lead address 2
* `city` (string): Lead city
* `contact_name` (string): Contact name at the company
* `currency` (string): Lead preferred currency
* `email` (string): Lead email address
* `language` (string): Lead preferred language
* `phone_number` (string): Lead phone number
* `state` (string): Lead state
* `zip` (string): Lead zipcode
* `form_name` (string): Signup form name
* `lead_source` (string): Source of the lead
* `opportunity_comment` (string): Opportunity comment
* `opportunity_type` (string): Type of opportunity to create
* `gclid` (string): Google Adwords Click ID
* `original_brand` (string): Brand: `files`, `exavault` or `mover`
* `utm_campaign` (string): Marketing tracking - campaign
* `utm_content` (string): Marketing tracking - content
* `utm_domain` (string): Marketing tracking - domain
* `utm_medium` (string): Marketing tracking - medium
* `utm_source` (string): Marketing tracking - source
* `utm_term` (string): Marketing tracking - term
* `time_zone` (string): Time zone, as returned by Javascript
* `time_zone_offset` (int64): Time zone offset (integer from -12 to 12)
