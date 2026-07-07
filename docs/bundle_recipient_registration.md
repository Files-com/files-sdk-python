# BundleRecipientRegistration

## Example BundleRecipientRegistration Object

```
{
  "code": "example",
  "bundle_registration_code": "example",
  "recipient": "example",
  "name": "example",
  "company": "example",
  "password_emailed": True,
  "inbox_code": "abc123"
}
```

* `code` (string): The bundle recipient registration code. Use this to register for the bundle.
* `bundle_registration_code` (string): If the recipient has already registered for this bundle, this is their registration code to get the bundle contents.
* `recipient` (string): The recipient's email address.
* `name` (string): The recipient's name.
* `company` (string): The recipient's company.
* `password_emailed` (boolean): Whether a one-time password was emailed to the recipient.
* `inbox_code` (string): InboxRegistration cookie code, if there is an associated InboxRegistration
* `bundle_recipient_code` (string): Bundle recipient code


---

## Create Bundle Recipient Registration

```
files_sdk.bundle_recipient_registration.create({
  "bundle_recipient_code": "bundle_recipient_code"
})
```

### Parameters

* `bundle_recipient_code` (string): Required - Bundle recipient code
