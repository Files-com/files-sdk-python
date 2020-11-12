# Project

## Example Project Object

```
{
  "id": 1,
  "global_access": "none"
}
```

* `id` (int64): Project ID
* `global_access` (string): Global access settings


---

## List Projects

```
files_sdk.project.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show Project

```
files_sdk.project.find(id)
```

### Parameters

* `id` (int64): Required - Project ID.


---

## Create Project

```
files_sdk.project.create({
  "global_access": "global_access"
})
```

### Parameters

* `global_access` (string): Required - Global permissions.  Can be: `none`, `anyone_with_read`, `anyone_with_full`.


---

## Update Project

```
files_sdk.project.update(id, {
  "global_access": "global_access"
})
```

### Parameters

* `id` (int64): Required - Project ID.
* `global_access` (string): Required - Global permissions.  Can be: `none`, `anyone_with_read`, `anyone_with_full`.


---

## Delete Project

```
files_sdk.project.delete(id)
```

### Parameters

* `id` (int64): Required - Project ID.


---

## Update Project

```
project = files_sdk.project.find(1)

project.update({
  "global_access": "global_access"
})
```

### Parameters

* `id` (int64): Required - Project ID.
* `global_access` (string): Required - Global permissions.  Can be: `none`, `anyone_with_read`, `anyone_with_full`.


---

## Delete Project

```
project = files_sdk.project.find(1)

project.delete()
```

### Parameters

* `id` (int64): Required - Project ID.
