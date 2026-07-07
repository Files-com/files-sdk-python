# InboxRecipientRegistration

## Example InboxRecipientRegistration Object

```
{
  "code": "example",
  "inbox_registration_code": "example",
  "recipient": "example",
  "name": "example",
  "company": "example"
}
```

* `code` (string): The inbox recipient registration code. Use this to register for the inbox.
* `inbox_registration_code` (string): If the recipient has already registered for this inbox, this is their registration code to get the inbox contents.
* `recipient` (string): The recipient's email address.
* `name` (string): The recipient's name.
* `company` (string): The recipient's company.
* `inbox_recipient_code` (string): Inbox recipient code


---

## Create Inbox Recipient Registration

```
files_sdk.inbox_recipient_registration.create({
  "inbox_recipient_code": "inbox_recipient_code"
})
```

### Parameters

* `inbox_recipient_code` (string): Required - Inbox recipient code
