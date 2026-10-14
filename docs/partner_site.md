
The functions below use the module's settings. Each is also a method of a client's
`client.partner_site` resource, such as
`client.partner_site.delete(...)`,
which uses that client's configuration instead.


---

## Delete Partner Site

```python
files_sdk.partner_site.delete(id)
```

### Parameters

* `id` (int64): Required - Partner Site ID.


---

## Delete Partner Site

A `PartnerSite` record from the API does not include its `id`,
so set the `id` you already know before calling `delete()`.

```python
partner_site = files_sdk.partner_site.new()
partner_site.id = id
partner_site.delete()
```

### Parameters

* `id` (int64): Required - Partner Site ID.
