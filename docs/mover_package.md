# MoverPackage

## Example MoverPackage Object

```
{
  "id": 1,
  "prepaid_bytes": 1,
  "prepaid_expire_in_days": 1,
  "price": "1.0"
}
```

* `id` (int64): Mover package ID
* `prepaid_bytes` (int64): Total prepaid bytes included in this package
* `prepaid_expire_in_days` (int64): Number of days this package is valid for after purchase
* `price` (decimal): Price of this mover package in the site's currency


---

## List Mover Packages

```
files_sdk.mover_package.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## Purchase a Mover package for the current site

```
files_sdk.mover_package.purchase(id)
```

### Parameters

* `id` (int64): Required - Mover Package ID.


---

## Create an export CSV of Mover Package resources

```
files_sdk.mover_package.create_export()
```


---

## Purchase a Mover package for the current site

```
mover_package = files_sdk.mover_package.list.first
mover_package.purchase()
```

### Parameters

* `id` (int64): Required - Mover Package ID.
