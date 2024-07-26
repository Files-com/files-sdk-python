# Clickwrap

## Example Clickwrap Object

```
{
  "id": 1,
  "name": "Example Site NDA for Files.com Use",
  "body": "[Legal body text]",
  "use_with_users": "example",
  "use_with_bundles": "example",
  "use_with_inboxes": "example"
}
```

* `id` (int64): Clickwrap ID
* `name` (string): Name of the Clickwrap agreement (used when selecting from multiple Clickwrap agreements.)
* `body` (string): Body text of Clickwrap (supports Markdown formatting).
* `use_with_users` (string): Use this Clickwrap for User Registrations?  Note: This only applies to User Registrations where the User is invited to your Files.com site using an E-Mail invitation process where they then set their own password.
* `use_with_bundles` (string): Use this Clickwrap for Bundles?
* `use_with_inboxes` (string): Use this Clickwrap for Inboxes?


---

## List Clickwraps

```
files_sdk.clickwrap.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): 
* `page` (int64): 


---

## Show Clickwrap

```
files_sdk.clickwrap.find(id)
```

### Parameters

* `id` (int64): Required - Clickwrap ID.


---

## Create Clickwrap

```
files_sdk.clickwrap.create({
  "name": "Example Site NDA for Files.com Use",
  "body": "[Legal body text]",
  "use_with_bundles": "example",
  "use_with_inboxes": "example",
  "use_with_users": "example"
})
```

### Parameters

* `name` (string): Name of the Clickwrap agreement (used when selecting from multiple Clickwrap agreements.)
* `body` (string): Body text of Clickwrap (supports Markdown formatting).
* `use_with_bundles` (string): Use this Clickwrap for Bundles?
* `use_with_inboxes` (string): Use this Clickwrap for Inboxes?
* `use_with_users` (string): Use this Clickwrap for User Registrations?  Note: This only applies to User Registrations where the User is invited to your Files.com site using an E-Mail invitation process where they then set their own password.


---

## Update Clickwrap

```
files_sdk.clickwrap.update(id, {
  "name": "Example Site NDA for Files.com Use",
  "body": "[Legal body text]",
  "use_with_bundles": "example",
  "use_with_inboxes": "example",
  "use_with_users": "example"
})
```

### Parameters

* `id` (int64): Required - Clickwrap ID.
* `name` (string): Name of the Clickwrap agreement (used when selecting from multiple Clickwrap agreements.)
* `body` (string): Body text of Clickwrap (supports Markdown formatting).
* `use_with_bundles` (string): Use this Clickwrap for Bundles?
* `use_with_inboxes` (string): Use this Clickwrap for Inboxes?
* `use_with_users` (string): Use this Clickwrap for User Registrations?  Note: This only applies to User Registrations where the User is invited to your Files.com site using an E-Mail invitation process where they then set their own password.


---

## Delete Clickwrap

```
files_sdk.clickwrap.delete(id)
```

### Parameters

* `id` (int64): Required - Clickwrap ID.


---

## Update Clickwrap

```
clickwrap = files_sdk.clickwrap.find(id)
clickwrap.update({
  "name": "Example Site NDA for Files.com Use",
  "body": "[Legal body text]",
  "use_with_bundles": "example",
  "use_with_inboxes": "example",
  "use_with_users": "example"
})
```

### Parameters

* `id` (int64): Required - Clickwrap ID.
* `name` (string): Name of the Clickwrap agreement (used when selecting from multiple Clickwrap agreements.)
* `body` (string): Body text of Clickwrap (supports Markdown formatting).
* `use_with_bundles` (string): Use this Clickwrap for Bundles?
* `use_with_inboxes` (string): Use this Clickwrap for Inboxes?
* `use_with_users` (string): Use this Clickwrap for User Registrations?  Note: This only applies to User Registrations where the User is invited to your Files.com site using an E-Mail invitation process where they then set their own password.


---

## Delete Clickwrap

```
clickwrap = files_sdk.clickwrap.find(id)
clickwrap.delete()
```

### Parameters

* `id` (int64): Required - Clickwrap ID.
